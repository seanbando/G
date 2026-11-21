"""Join one section of the Frein edit from its plan: rendered 3D shots, maps, cards and object close-ups + real clips,
freeze frames and photos (cut from the full-length downloads exactly as the plan says), the source watermark and any
typed name tag / stamp burned into each shot, then the approved narration for that stretch (untouched), a quiet
music bed and typewriter clicks for every typed text.
  python assemble.py shots3.json            -> build/render/<plan "out">   (1080p30, -14 LUFS)
Also leaves build/render/<dir>/_picture.mp4 (no sound): final.py joins those for the whole film and mixes one soundtrack.
Each shot is finished as its own file first (F<id>.mp4), so the join is a plain concat."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(HERE, "..", ".."))
REPO = os.path.normpath(os.path.join(VID, "..", "..", ".."))
OB = os.path.join(REPO, "saylo", "videos", "01-olympic-bomber")
TAGS = os.path.join(REPO, "saylo", "assets", "source-tags")
cfg = json.load(open(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "shots.json"), encoding="utf-8"))
ONLY_PICTURE = "--picture" in sys.argv
FPS, START, END = cfg["fps"], cfg.get("start", 0.0), cfg["end"]
DUR = round(END * FPS) / FPS - round(START * FPS) / FPS
SRC = cfg.get("src", {})
shots_dir = os.path.join(VID, "build", "render", cfg.get("dir", "shots"))
out = os.path.join(VID, "build", "render", cfg.get("out", "frein_cold_open_style_test.mp4"))
FF = ["ffmpeg", "-hide_banner", "-loglevel", os.environ.get("FFLOG", "error"), "-y", "-nostdin"]
ENC = ["-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]
GRADE = "eq=saturation=0.72:contrast=1.06:brightness=-0.03"


def run(cmd, what):
    print("..", what, flush=True)
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)


def frames(s):
    return round(s["end"] * FPS) - round(s["start"] * FPS)


def src_path(s):
    return os.path.join(VID, "media", "src", SRC.get(s["src"], s["src"]))


def push_filter(r):
    """Slow push on real footage (Retraced: about 2% a second)."""
    if not r:
        return []
    return [f"scale=w='2*trunc(960*(1+{r}*t))':h='2*trunc(540*(1+{r}*t))':eval=frame:flags=bicubic", "crop=1920:1080"]


def fit(s):
    if s.get("crop"):
        return [f"crop={s['crop']}", "scale=1920:1080:flags=lanczos", "setsar=1"]
    if s.get("fit") == "contain":
        return ["scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos",
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0A0F1B", "setsar=1"]
    return ["scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos", "crop=1920:1080", "setsar=1"]


def overlay_file(s):
    """The shot's typed overlay (name tag / stamp) rendered with alpha by O_text.py (or O_tag.py for the cold open)."""
    for name in (f"O{s['id']:02d}.mov", f"S{s['id']:02d}-tag.mov"):
        p = os.path.join(shots_dir, name)
        if os.path.exists(p):
            return p
    return None


def finish(pre_inputs, vf, s, n, dst):
    """Encode one shot of n frames from pre_inputs through vf, burning in its source tag and typed overlay."""
    cmd = FF + pre_inputs
    chain = ",".join(vf) if vf else "null"
    k = sum(1 for a in pre_inputs if a == "-i")
    fc, last = f"[0:v]{chain}[m0]", "m0"
    if s.get("tag"):
        cmd += ["-i", os.path.join(TAGS, s["tag"])]
        fc += f";[{last}][{k}:v]overlay=0:0:eof_action=repeat[m1]"
        last, k = "m1", k + 1
    ov = overlay_file(s) if (s.get("nametag") or s.get("stamp")) and s["kind"] in ("clip", "image", "still") else None
    if (s.get("nametag") or s.get("stamp")) and s["kind"] in ("clip", "image", "still") and not ov:
        raise SystemExit(f"shot {s['id']}: its typed overlay has not been rendered (run build.ps1 for this plan first)")
    if ov:
        cmd += ["-i", ov]
        fc += f";[{last}][{k}:v]overlay=0:0:eof_action=repeat[m2]"
        last = "m2"
    fc += f";[{last}]format=yuv420p[v]"
    run(cmd + ["-filter_complex", fc, "-map", "[v]", "-frames:v", str(n)] + ENC + [dst], os.path.basename(dst))


# 1. one finished file per shot: F<id>.mp4
files = []
for s in cfg["shots"]:
    n = frames(s)
    sid = f"{s['id']:02d}"
    dst = os.path.join(shots_dir, f"F{sid}.mp4")
    files.append(dst)
    k = s["kind"]
    if k == "image":                                   # a photo file with a push
        png = os.path.join(VID, *s["img"].split("/"))
        vf = fit(s) + [f"fps={FPS}"] + push_filter(s.get("push", 0.05)) + [GRADE]
        finish(["-loop", "1", "-framerate", str(FPS), "-t", str(n / FPS + 0.5), "-i", png], vf, s, n, dst)
    elif k == "still":                                 # freeze frame from the source at s["at"], with a push
        png = os.path.join(shots_dir, f"S{sid}-frame.png")
        run(FF + ["-ss", str(s["at"]), "-i", src_path(s), "-frames:v", "1", png], f"frame S{sid}")
        vf = ([f"crop={s['crop']}"] if s.get("crop") else []) + ["scale=1920:1080:flags=lanczos", "setsar=1", f"fps={FPS}"] \
            + push_filter(s.get("push", 0.08)) + [GRADE]
        finish(["-loop", "1", "-framerate", str(FPS), "-t", str(n / FPS + 0.5), "-i", png], vf, s, n, dst)
    elif k == "clip":                                  # real clip: cut on the source seconds, muted, fitted to the shot
        stretch = (n / FPS) / (s["out"] - s["in"])
        vf = [f"crop={s['crop']}"] if s.get("crop") else []      # e.g. cut a station banner or a taskbar out of frame
        if s.get("zoom"):
            z = s["zoom"]
            vf.append(f"crop=iw/{z}:ih/{z}:(iw-iw/{z})*{s['cx']}:(ih-ih/{z})*{s['cy']}")
        vf += ["scale=1920:1080:flags=lanczos", "setsar=1", f"setpts={stretch:.5f}*(PTS-STARTPTS)", f"fps={FPS}"]
        vf += push_filter(s.get("push"))
        vf.append(GRADE)
        finish(["-ss", str(s["in"]), "-t", str(s["out"] - s["in"] + 0.2), "-i", src_path(s)], vf, s, n, dst)
    elif k == "reuse":                                 # a callback: part of a shot already rendered for another section
        src = os.path.join(VID, "build", "render", *s["from"].split("/"))
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                 capture_output=True, text=True).stdout.strip())
        at = min(s.get("at", 0.0), max(0.0, d - 0.3))
        have = d - at
        stretch = max(1.0, (n / FPS) / have + 0.02)    # never faster; slowed a little only if the source is too short
        finish(["-ss", str(at), "-i", src], [f"setpts={stretch:.4f}*(PTS-STARTPTS)", f"fps={FPS}", "setsar=1"], s, n, dst)
    else:                                              # rendered shot (3D, map, card, object): re-wrap, burn the tag in
        finish(["-i", os.path.join(shots_dir, f"S{sid}.mp4")], ["setsar=1"], s, n, dst)

# 2. picture: plain concat
lst = os.path.join(shots_dir, "list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for p in files:
        fh.write(f"file '{os.path.basename(p)}'\n")
tmp_v = os.path.join(shots_dir, "_picture.mp4")
run(FF + ["-f", "concat", "-safe", "0", "-i", lst, "-t", f"{DUR:.4f}", "-an",
          "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp_v], "picture")
if ONLY_PICTURE:
    print(tmp_v)
    sys.exit(0)

# 3. sound for this section alone (a review mix; the film's real soundtrack is mixed once in final.py):
#    the approved voiceover as is, the music bed under it, key clicks where text types on
TYPES = [tuple(t) for t in cfg.get("types", [])]
sfx = os.path.join(OB, "sound", "sfx")
a_in = ["-ss", f"{START:.3f}", "-t", f"{DUR:.4f}", "-i", os.path.join(VID, "voiceover-full.mp3"),
        "-stream_loop", "-1", "-ss", f"{START % 150.0:.3f}", "-t", f"{DUR:.4f}", "-i", os.path.join(OB, "sound", "music", "bed-A.mp3")]
a_f = ["[0:a]volume=1.0[vo]", f"[1:a]volume=0.15,afade=t=in:d=0.6,afade=t=out:st={DUR - 1.0:.3f}:d=1.0[bed]"]
mix = ["[vo]", "[bed]"]
ni = 2
if START == 0:                                         # the cold open's woods ambience
    a_in += ["-stream_loop", "-1", "-t", f"{DUR:.4f}", "-i", os.path.join(sfx, "sfx-night-forest.mp3")]
    a_f.append(f"[{ni}:a]volume=0.10,afade=t=in:d=0.8,afade=t=out:st=33.2:d=0.7[amb]")
    mix.append("[amb]")
    ni += 1
for i, (t, kind) in enumerate(TYPES):
    a_in += ["-t", "1.1", "-i", os.path.join(sfx, f"sfx-typewriter-keys-{kind}.mp3")]
    ms = max(0, int((t - START) * 1000))
    a_f.append(f"[{ni + i}:a]afade=t=out:st=0.8:d=0.3,volume=0.3,adelay={ms}|{ms}[k{i}]")
    mix.append(f"[k{i}]")
a_f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{DUR:.4f},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
tmp_a = os.path.join(shots_dir, "_sound.wav")
run(FF + a_in + ["-filter_complex", ";".join(a_f), "-map", "[a]", "-t", f"{DUR:.4f}", "-ar", "48000", tmp_a], "sound")

# 4. mux
run(FF + ["-i", tmp_v, "-i", tmp_a, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
          "-t", f"{DUR:.4f}", "-movflags", "+faststart", out], "mux")
print(out)
