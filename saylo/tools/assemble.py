"""Assemble a Saylo video from a shot plan: picture track, music, SFX, voiceover.

Usage:
    python3 saylo/tools/assemble.py <plan.json> <out.mp4> [--from SEC] [--to SEC]

plan.json:
{
  "assets": "<folder with source files>",
  "voiceover": "<voiceover-full.mp3>",
  "segments": [                       # in order; each fills [start, end) on the timeline
     {"start": 0.0, "end": 4.6, "card": [["MAY 31, 2003","type"],["3:30 AM","amber"]], "bg": "loc-murphy-street.png"},
     {"start": 4.6, "end": 8.2, "src": "loc-murphy-street.png"},              # photo → slow push-in
     {"start": 8.2, "end": 11.9, "src": "A clip.mp4", "in": 0.0},             # video → trimmed (frozen if short)
     {"start": 16.8, "end": 21.0, "src": "04 postell clip.mp4", "tag": ["JEFF POSTELL", "Murphy police officer, 21"]}
  ],
  "music": [{"start": 0, "end": 112, "bed": "bed-A.mp3", "gain": -20}],     # dB under full scale before ducking
  "sfx": [{"at": 0.0, "file": "sfx-typewriter-keys-medium.mp3", "gain": -8}],
  "silence": [[1026.2, 1030.7]]       # music fully out here
}
Segments are rendered once to <out>.parts/ and reused on later runs (delete a part to re-render it).
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_card import card, overlay, lower_third, number_build, photo_stack  # noqa: E402

FPS = 30
VENC = ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]
GRADE = "eq=contrast=1.04:saturation=0.85:brightness=-0.02"
FILL = ("[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
        "boxblur=30:5,eq=brightness=-0.16[bg];[b]scale=1920:1080:force_original_aspect_ratio=decrease[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2")


def run(args):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-800:])


def is_video(path):
    return path.lower().endswith((".mp4", ".mov", ".webm", ".mkv"))


def still_png(src, out):
    run(["-i", src, "-frames:v", "1", out])  # handles avif/webp/jpg/png


MOTIONS = ["push_in", "pan_right", "pull_out", "pan_left"]


def _zoompan(motion, n):
    """zoompan expressions on a 2x-res frame: stronger moves + a slight handheld drift."""
    drift_x = f"+sin(on/{FPS}*0.9)*iw*0.004"
    drift_y = f"+cos(on/{FPS}*0.7)*ih*0.004"
    cx, cy = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if motion == "push_in":
        return f"1.02+0.20*on/{n}", cx + drift_x, cy + drift_y
    if motion == "pull_out":
        return f"1.22-0.20*on/{n}", cx + drift_x, cy + drift_y
    if motion == "pan_right":
        return "1.20", f"(iw-iw/zoom)*(0.1+0.8*on/{n})", cy + drift_y
    if motion == "pan_left":
        return "1.20", f"(iw-iw/zoom)*(0.9-0.8*on/{n})", cy + drift_y
    return "1.0", cx, cy


def _fx_chain(fx):
    """Atmosphere on stills: grain always; optional flicker (night lights) and fog drift."""
    chain = ["noise=alls=7:allf=t"]
    if "flicker" in fx:
        chain.append("eq=brightness='-0.03+0.025*sin(t*13)*sin(t*3.1)':eval=frame")
    return ",".join(chain)


def render_photo(src, dur, out, tmp, motion="push_in", fx=()):
    png = tmp + ".png"
    still_png(src, png)
    big = tmp + "_big.png"
    run(["-i", png, "-filter_complex", FILL.replace("1920:1080", "3840:2160"), "-frames:v", "1", big])
    n = max(1, int(round(dur * FPS)))
    z, x, y = _zoompan(motion, n)
    base = (f"[0:v]zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1920x1080:fps={FPS},{GRADE},{_fx_chain(fx)}")
    if "fog" in fx:
        # slow drifting fog: blurred noise layer scrolling sideways, screened on top
        run(["-loop", "1", "-i", big, "-f", "lavfi", "-i", f"color=c=gray:s=2400x1080:d={dur:.3f},noise=alls=100:allf=t+u",
             "-t", f"{dur:.3f}", "-filter_complex",
             base + "[b];[1:v]trim=end_frame=1,loop=loop=-1:size=1,gblur=sigma=60,eq=contrast=2.2:brightness=-0.25,"
             f"crop=1920:1080:x='t*{400 / max(dur, 1):.2f}':y=0,format=gbrp[f];[b]format=gbrp[bb];"
             "[bb][f]blend=all_mode=screen:all_opacity=0.35,format=yuv420p",
             *VENC, "-an", out])
        return
    run(["-loop", "1", "-i", big, "-t", f"{dur:.3f}", "-filter_complex", base, *VENC, "-an", out])


def render_video(src, dur, out, start=0.0, crop=None):
    fill = FILL.replace("[0:v]split", f"[0:v]crop={crop},split") if crop else FILL
    run(["-ss", f"{start:.3f}", "-i", src, "-t", f"{dur:.3f}", "-filter_complex",
         fill + f",{GRADE},fps={FPS},tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f}",
         *VENC, "-an", out])


def add_tag(clip, dur, tag, out, tmp):
    mov = tmp + "_tag.mov"
    lower_third(mov, tag[0], tag[1] if len(tag) > 1 else "", min(dur, 4.2))
    run(["-i", clip, "-i", mov, "-filter_complex", "[0:v][1:v]overlay=eof_action=pass", *VENC, "-an", out])


EFFECTS = os.environ.get("SAYLO_EFFECTS", "")  # path to the Template Library's .claude/effects folder
_EFFECT_LIMITS = {}


def _effect_limits(eid):
    if eid not in _EFFECT_LIMITS:
        r = subprocess.run(["node", "render_effect.mjs", "--schema", eid], cwd=EFFECTS, capture_output=True, text=True)
        d = json.loads(r.stdout)["duration"]
        _EFFECT_LIMITS[eid] = (d["min"], d["max"])
    return _EFFECT_LIMITS[eid]


def render_effect(seg, assets, dur, out, tmp):
    """Render a Template Library effect with overrides (image paths relative to the assets folder)."""
    lo, hi = _effect_limits(seg["effect"])
    edur = min(max(dur, lo), hi)
    ov = os.path.join(assets, "_ov_" + os.path.basename(tmp) + ".json")
    json.dump(seg.get("ov", {}), open(ov, "w"))
    raw = tmp + "_fx.mp4"
    r = subprocess.run(["node", "render_effect.mjs", "--id", seg["effect"], "--overrides", ov, "--duration", f"{edur:.2f}",
                        "--out", raw], cwd=EFFECTS, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-600:])
    run(["-i", raw, "-filter_complex",
         f"[0:v]scale=1920:1080,fps={FPS},tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},format=yuv420p",
         *VENC, "-an", out])


def render_segment(seg, assets, out, tmp):
    dur = seg["end"] - seg["start"]
    if "effect" in seg:
        render_effect(seg, assets, dur, out if "tag" not in seg else tmp + "_base.mp4", tmp)
        if "tag" in seg:
            add_tag(tmp + "_base.mp4", dur, seg["tag"], out, tmp)
        return
    if "number" in seg:
        nb = seg["number"]
        number_build(out, nb["value"], dur, nb.get("prefix", ""), nb.get("suffix", ""), nb.get("label", ""), nb.get("land", 2.0))
        return
    if "stack" in seg:
        st = seg["stack"]
        photo_stack(out, [os.path.join(assets, x) for x in st["photos"]], dur, st["date"], st.get("where", ""), st.get("beat", 1.6))
        return
    if "card" in seg:
        bg = os.path.join(assets, seg["bg"]) if seg.get("bg") else None
        if bg and is_video(bg):
            still_png(bg, tmp + "_bg.png")
            bg = tmp + "_bg.png"
        card(out, [tuple(x) for x in seg["card"]], dur, bg=bg)
        return
    src = os.path.join(assets, seg["src"])
    base = out if "tag" not in seg else tmp + "_base.mp4"
    if is_video(src):
        render_video(src, dur, base, seg.get("in", 0.0), seg.get("crop"))
    else:
        render_photo(src, dur, base, tmp, seg.get("motion", "push_in"), seg.get("fx", ()))
    if "tag" in seg:
        add_tag(base, dur, seg["tag"], out, tmp)


def build_audio(plan, t0, t1, out, tmp):
    """VO + ducked music beds + SFX, cut to [t0, t1]."""
    music_dir = plan["music_dir"]
    sfx_dir = plan["sfx_dir"]
    inputs = ["-ss", f"{t0}", "-t", f"{t1 - t0}", "-i", plan["voiceover"]]
    parts, n = [], 1
    for m in plan["music"]:
        s, e = max(m["start"], t0), min(m["end"], t1)
        if e <= s:
            continue
        inputs += ["-stream_loop", "-1", "-i", os.path.join(music_dir, m["bed"])]
        fade = m.get("fade", 1.5)
        parts.append(f"[{n}:a]atrim=0:{e - s:.3f},asetpts=PTS-STARTPTS,volume={m.get('gain', -20)}dB,"
                     f"afade=t=in:d={fade},afade=t=out:st={max(0, e - s - fade):.3f}:d={fade},"
                     f"adelay={int((s - t0) * 1000)}|{int((s - t0) * 1000)}[m{n}]")
        n += 1
    music_labels = [f"[m{i}]" for i in range(1, n)]
    sfx_labels = []
    for x in plan["sfx"]:
        if not (t0 <= x["at"] < t1):
            continue
        inputs += ["-i", os.path.join(sfx_dir, x["file"])]
        d = int((x["at"] - t0) * 1000)
        parts.append(f"[{n}:a]volume={x.get('gain', -10)}dB,adelay={d}|{d}[s{n}]")
        sfx_labels.append(f"[s{n}]")
        n += 1
    graph = ";".join(parts)
    vo = "[0:a]aformat=channel_layouts=stereo,asplit=2[vo][key]"
    graph = vo + (";" + graph if graph else "")
    if music_labels:
        graph += f";{''.join(music_labels)}amix=inputs={len(music_labels)}:normalize=0[mus]"
        # silence windows (music fully out)
        cur = "mus"
        for k, (a, b) in enumerate(plan.get("silence", [])):
            if b > t0 and a < t1:
                graph += f";[{cur}]volume=0:enable='between(t,{max(0, a - t0):.2f},{b - t0:.2f})'[mus{k}]"
                cur = f"mus{k}"
        graph += f";[{cur}][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck]"
        mix = ["[vo]", "[duck]"] + sfx_labels
    else:
        graph += ";[key]anullsink"
        mix = ["[vo]"] + sfx_labels
    graph += f";{''.join(mix)}amix=inputs={len(mix)}:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=11[out]"
    run([*inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{t1 - t0}", out])


def main(argv):
    plan = json.load(open(argv[0]))
    out = argv[1]
    t0 = float(argv[argv.index("--from") + 1]) if "--from" in argv else 0.0
    t1 = float(argv[argv.index("--to") + 1]) if "--to" in argv else plan["segments"][-1]["end"]
    parts_dir = out + ".parts"
    os.makedirs(parts_dir, exist_ok=True)
    listing = []
    for i, seg in enumerate(plan["segments"]):
        seg.setdefault("motion", MOTIONS[i % len(MOTIONS)])
        if seg["end"] <= t0 or seg["start"] >= t1:
            continue
        p = os.path.join(parts_dir, f"{i:04d}.mp4")
        if not os.path.exists(p):
            print(f"render {i:04d} {seg['start']:.1f}-{seg['end']:.1f} {seg.get('src') or 'card'}", flush=True)
            render_segment(seg, plan["assets"], p, os.path.join(parts_dir, f"_{i:04d}"))
        listing.append(p)
    lst = out + ".list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in listing))
    t0 = max(t0, min(s["start"] for s in plan["segments"] if s["end"] > t0))
    video = out + ".video.mp4"
    run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])
    audio = out + ".audio.m4a"
    build_audio(plan, t0, t1, audio, parts_dir)
    run(["-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest", out])
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1:])
