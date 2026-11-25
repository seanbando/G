"""Join the whole Frein film from the chapters' finished pictures and mix ONE soundtrack for it.
  python final.py            -> build/render/frein_full_v1.mp4   (1080p30, -14 LUFS)
  python final.py v2         -> build/render/frein_full_v2.mp4
Needs every chapter's build/render/<dir>/_picture.mp4 (made by assemble.py).
Sound: the approved voiceover untouched, one music bed under the whole film (out for the handcuffs landing),
the woods ambience under the cold open, and a typewriter click for every typed text in every plan."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(HERE, "..", ".."))
REPO = os.path.normpath(os.path.join(VID, "..", "..", ".."))
OB = os.path.join(REPO, "saylo", "videos", "01-olympic-bomber")
R = os.path.join(VID, "build", "render")
PLANS = [f"shots{n}.json" for n in range(2, 10)]
TAG = sys.argv[1] if len(sys.argv) > 1 else "v1"
OUT = os.path.join(R, f"frein_full_{TAG}.mp4")
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-nostdin"]
MUSIC_OUT = (675.6, 684.5)        # the camera lands on the handcuffs: the bed drops out, then returns


def run(cmd, what):
    print("..", what, flush=True)
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)


cfgs = [json.load(open(os.path.join(HERE, p), encoding="utf-8")) for p in PLANS]
END = cfgs[-1]["end"]
FPS = cfgs[0]["fps"]
DUR = round(END * FPS) / FPS

# 1. picture: the chapters end to end (same encoder settings, so a straight copy)
lst = os.path.join(R, "full_list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for c in cfgs:
        p = os.path.join(R, c["dir"], "_picture.mp4")
        if not os.path.exists(p):
            raise SystemExit(f"missing {p}: run assemble.py for that plan first")
        fh.write("file '" + p.replace("\\", "/") + "'\n")
pic = os.path.join(R, "_full_picture.mp4")
run(FF + ["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-an", pic], "picture")

# 2. typewriter clicks, mixed chapter by chapter into one stem each (keeps every ffmpeg graph small)
sfx = os.path.join(OB, "sound", "sfx")
stems = []
for c in cfgs:
    types = [tuple(t) for t in c.get("types", [])]
    if not types:
        continue
    a_in, a_f, mix = [], [], []
    for i, (t, kind) in enumerate(types):
        a_in += ["-t", "1.1", "-i", os.path.join(sfx, f"sfx-typewriter-keys-{kind}.mp3")]
        ms = max(0, int(t * 1000))
        a_f.append(f"[{i}:a]afade=t=out:st=0.8:d=0.3,volume=0.3,adelay={ms}|{ms}[k{i}]")
        mix.append(f"[k{i}]")
    a_f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,apad,atrim=0:{DUR:.4f}[a]")
    stem = os.path.join(R, f"_keys_{c['dir']}.wav")
    run(FF + a_in + ["-filter_complex", ";".join(a_f), "-map", "[a]", "-ar", "48000", "-ac", "2", stem], f"keys {c['dir']}")
    stems.append(stem)

# 3. the mix
a, b = MUSIC_OUT
bed_vol = f"0.15*(1-clip((t-{a})/0.5\\,0\\,1)+clip((t-{b})/1.5\\,0\\,1))"
a_in = ["-t", f"{DUR:.4f}", "-i", os.path.join(VID, "voiceover-full.mp3"),
        "-stream_loop", "-1", "-t", f"{DUR:.4f}", "-i", os.path.join(OB, "sound", "music", "bed-A.mp3"),
        "-stream_loop", "-1", "-t", "34.5", "-i", os.path.join(sfx, "sfx-night-forest.mp3")]
a_f = ["[0:a]volume=1.0[vo]",
       f"[1:a]volume='{bed_vol}':eval=frame,afade=t=in:d=0.6,afade=t=out:st={DUR - 2.5:.3f}:d=2.5[bed]",
       "[2:a]volume=0.10,afade=t=in:d=0.8,afade=t=out:st=33.2:d=0.7[amb]"]
mix = ["[vo]", "[bed]", "[amb]"]
for i, s in enumerate(stems):
    a_in += ["-i", s]
    mix.append(f"[{3 + i}:a]")
a_f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{DUR:.4f},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
snd = os.path.join(R, "_full_sound.wav")
run(FF + a_in + ["-filter_complex", ";".join(a_f), "-map", "[a]", "-t", f"{DUR:.4f}", "-ar", "48000", snd], "sound")

# 4. mux
run(FF + ["-i", pic, "-i", snd, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
          "-t", f"{DUR:.4f}", "-movflags", "+faststart", OUT], "mux")
print(OUT)
