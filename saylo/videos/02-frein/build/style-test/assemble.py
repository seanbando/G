"""Join a Frein cold-open cut: rendered 3D shots + real clips and freeze frames (cut from the full-length downloads at
the seconds in the plan), the source watermark burned into every real clip / photo / map shot, the name-tag overlay,
the approved narration (untouched), a quiet music bed and typewriter clicks for every typed text.
  python assemble.py [shots2.json]
Output: build/render/<plan "out"> (1080p30, -14 LUFS).
Watermarks are burned into each shot's own file first (step 1), so the final join is a plain concat: a chain of
enable-timed overlays over the whole timeline stalled ffmpeg once the plan grew past eight tags."""
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
FPS, END = cfg["fps"], cfg["end"]
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


def push_filter(r):
    """Slow push on real footage (Retraced: about 2% a second)."""
    return [f"scale=w='2*trunc(960*(1+{r}*t))':h='2*trunc(540*(1+{r}*t))':eval=frame:flags=bicubic", "crop=1920:1080"]


def with_tag(pre_inputs, vf, s, n, dst):
    """Encode one shot of n frames from pre_inputs through vf, with its source tag (if any) burned in."""
    cmd = FF + pre_inputs
    chain = ",".join(vf) if vf else "null"
    if s.get("tag"):
        cmd += ["-i", os.path.join(TAGS, s["tag"])]
        k = sum(1 for a in pre_inputs if a == "-i")
        fc = f"[0:v]{chain}[m];[m][{k}:v]overlay=0:0:eof_action=repeat,format=yuv420p[v]"
    else:
        fc = f"[0:v]{chain},format=yuv420p[v]"
    run(cmd + ["-filter_complex", fc, "-map", "[v]", "-frames:v", str(n)] + ENC + [dst], os.path.basename(dst))


# 1. one finished file per shot: F<id>.mp4
files = []
for s in cfg["shots"]:
    n = frames(s)
    sid = f"{s['id']:02d}"
    dst = os.path.join(shots_dir, f"F{sid}.mp4")
    files.append(dst)
    if s["kind"] == "image":                           # a photo file, cropped to 16:9, with a push
        png = os.path.join(VID, *s["img"].split("/"))
        vf = ([f"crop={s['crop']}"] if s.get("crop") else []) + ["scale=1920:1080:flags=lanczos", "setsar=1", f"fps={FPS}"] \
            + push_filter(s.get("push", 0.05)) + [GRADE]
        with_tag(["-loop", "1", "-framerate", str(FPS), "-t", str(n / FPS + 0.5), "-i", png], vf, s, n, dst)
    elif s["kind"] == "still":                         # freeze frame from the source at s["at"], with a quick push
        src = os.path.join(VID, "media", "src", s["src"])
        png = os.path.join(shots_dir, f"S{sid}-frame.png")
        run(FF + ["-ss", str(s["at"]), "-i", src, "-frames:v", "1", png], f"frame S{sid}")
        vf = ["scale=1920:1080:flags=lanczos", "setsar=1", f"fps={FPS}"] + push_filter(s.get("push", 0.08)) + [GRADE]
        with_tag(["-loop", "1", "-framerate", str(FPS), "-t", str(n / FPS + 0.5), "-i", png], vf, s, n, dst)
    elif s["kind"] == "clip":                          # real clip: cut on the source seconds, muted, fitted to the shot
        src = os.path.join(VID, "media", "src", s["src"])
        stretch = (n / FPS) / (s["out"] - s["in"])
        vf = [f"crop={s['crop']}"] if s.get("crop") else []      # e.g. cut a station banner or a taskbar out of frame
        if s.get("zoom"):
            z = s["zoom"]
            vf.append(f"crop=iw/{z}:ih/{z}:(iw-iw/{z})*{s['cx']}:(ih-ih/{z})*{s['cy']}")
        vf += ["scale=1920:1080:flags=lanczos", "setsar=1", f"setpts={stretch:.5f}*(PTS-STARTPTS)", f"fps={FPS}"]
        if s.get("push"):
            vf += push_filter(s["push"])
        vf.append(GRADE)
        with_tag(["-ss", str(s["in"]), "-t", str(s["out"] - s["in"] + 0.2), "-i", src], vf, s, n, dst)
    else:                                              # rendered shot: re-wrap, burning the tag in if it has one
        with_tag(["-i", os.path.join(shots_dir, f"S{sid}.mp4")], [], s, n, dst)

# 2. picture: plain concat, plus the name-tag overlays (alpha clips rendered by O_tag.py)
lst = os.path.join(shots_dir, "list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for p in files:
        fh.write(f"file '{os.path.basename(p)}'\n")
v_in = ["-f", "concat", "-safe", "0", "-i", lst]
v_f, last, k = [], "0:v", 1
for s in cfg["shots"]:
    if s.get("nametag"):
        t0, t1 = round(s["start"] * FPS) / FPS, round(s["end"] * FPS) / FPS
        v_in += ["-i", os.path.join(shots_dir, f"S{s['id']:02d}-tag.mov")]
        v_f.append(f"[{k}:v]setpts=PTS+{t0:.4f}/TB[nt{k}]")
        v_f.append(f"[{last}][nt{k}]overlay=0:0:eof_action=pass:enable='gte(t,{t0:.4f})*lt(t,{t1 - 0.001:.4f})'[v{k}]")
        last, k = f"v{k}", k + 1
if not v_f:
    v_f.append("[0:v]null[v0]")
    last = "v0"
tmp_v = os.path.join(shots_dir, "_picture.mp4")
run(FF + v_in + ["-filter_complex", ";".join(v_f), "-map", f"[{last}]", "-t", str(END), "-an",
                 "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp_v], "picture")

# 3. sound, in its own pass (picture + sound in one filter graph stalled ffmpeg): the approved voiceover as is,
#    music bed under it, key clicks where text types on
TYPES = [tuple(t) for t in cfg.get("types", [])]
sfx = os.path.join(OB, "sound", "sfx")
a_in = ["-t", str(END), "-i", os.path.join(VID, "voiceover-full.mp3"),
        "-stream_loop", "-1", "-t", str(END), "-i", os.path.join(OB, "sound", "music", "bed-A.mp3"),
        "-stream_loop", "-1", "-t", str(END), "-i", os.path.join(sfx, "sfx-night-forest.mp3")]
a_f = ["[0:a]volume=1.0[vo]",
       f"[1:a]volume=0.15,afade=t=in:d=0.6,afade=t=out:st={END - 1.0}:d=1.0[bed]",
       "[2:a]volume=0.10,afade=t=in:d=0.8,afade=t=out:st=33.2:d=0.7[amb]"]
mix = ["[vo]", "[bed]", "[amb]"]
for i, (t, kind) in enumerate(TYPES):
    a_in += ["-t", "1.1", "-i", os.path.join(sfx, f"sfx-typewriter-keys-{kind}.mp3")]
    a_f.append(f"[{3 + i}:a]afade=t=out:st=0.8:d=0.3,volume=0.3,adelay={int(t * 1000)}|{int(t * 1000)}[k{i}]")
    mix.append(f"[k{i}]")
a_f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
tmp_a = os.path.join(shots_dir, "_sound.wav")
run(FF + a_in + ["-filter_complex", ";".join(a_f), "-map", "[a]", "-t", str(END), "-ar", "48000", tmp_a], "sound")

# 4. mux
run(FF + ["-i", tmp_v, "-i", tmp_a, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
          "-t", str(END), "-movflags", "+faststart", out], "mux")
print(out)
