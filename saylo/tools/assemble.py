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
from make_card import card, overlay  # noqa: E402

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


def render_photo(src, dur, out, tmp):
    png = tmp + ".png"
    still_png(src, png)
    # compose a 2x-res 16:9 frame (blurred fill for odd shapes), then a slow push-in 100% -> 112%
    big = tmp + "_big.png"
    run(["-i", png, "-filter_complex", FILL.replace("1920:1080", "3840:2160").replace("1920:1080", "3840:2160"),
         "-frames:v", "1", big])
    n = max(1, int(round(dur * FPS)))
    run(["-loop", "1", "-i", big, "-t", f"{dur:.3f}", "-filter_complex",
         f"[0:v]zoompan=z='1+0.12*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps={FPS},{GRADE}",
         *VENC, "-an", out])


def render_video(src, dur, out, start=0.0, crop=None):
    fill = FILL.replace("[0:v]split", f"[0:v]crop={crop},split") if crop else FILL
    run(["-ss", f"{start:.3f}", "-i", src, "-t", f"{dur:.3f}", "-filter_complex",
         fill + f",{GRADE},fps={FPS},tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f}",
         *VENC, "-an", out])


def add_tag(clip, dur, tag, out, tmp):
    mov = tmp + "_tag.mov"
    overlay(mov, tag[0], min(dur, 4.0), "tag", sub=tag[1] if len(tag) > 1 else None)
    run(["-i", clip, "-i", mov, "-filter_complex", "[0:v][1:v]overlay=eof_action=pass", *VENC, "-an", out])


def render_segment(seg, assets, out, tmp):
    dur = seg["end"] - seg["start"]
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
        render_photo(src, dur, base, tmp)
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
