"""Join the whole Frein film from the chapters' finished pictures and mix ONE soundtrack for it.
  python final.py            -> build/render/frein_full_v1.mp4   (1080p30, -14 LUFS)
  python final.py v2         -> build/render/frein_full_v2.mp4
Needs every chapter's build/render/<dir>/_picture.mp4 (made by assemble.py).
Sound: the approved voiceover untouched, four music beds rotated by chapter (out for two holds), the woods ambience
under the cold open, a typewriter click for every typed text, and a few effects (helicopter, low hit, paper)."""
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

# 3. the mix: a different bed per chapter (cross-faded), music out at two holds, a few effects on the picture
MUSIC = os.path.join(OB, "sound", "music")
GAIN = {"A": 0.15, "B": 1.2, "C": 0.22, "D": 0.185}          # the four beds are mastered at very different levels
BEDS = [("A", 0.0, 52.8, 0), ("B", 52.8, 108.9, 0), ("A", 108.9, 174.1, 40), ("C", 174.1, 220.1, 0),
        ("B", 220.1, 262.3, 20), ("D", 262.3, 326.6, 0), ("B", 326.6, 394.35, 30), ("D", 394.35, 443.07, 50),
        ("A", 443.07, 556.55, 20), ("C", 556.55, 600.67, 30), ("B", 600.67, 655.47, 60), ("A", 655.47, 684.5, 0),
        ("C", 684.5, DUR, 60)]                                 # (bed, from, to, where in the track it starts)
OUTS = [(259.2, 262.3, 0.3), MUSIC_OUT + (1.5,)]               # "What they didn't have was Eric Frein." / the handcuffs
HIT, HELI, SHUT, PAPER = "sfx-low-hit.mp3", "sfx-helicopter-distant.mp3", "sfx-camera-shutter.mp3", "sfx-paper-slide.mp3"
FX = [(HELI, 68.3, 12.0, 2.2), (HELI, 443.07, 12.0, 2.6), (HELI, 655.47, 12.0, 3.6),          # real helicopter views
      (HIT, 149.25, 0.35, 1.48), (HIT, 167.0, 0.35, 1.48), (HIT, 676.8, 0.4, 1.48),             # two rifle flashes, the handcuffs
      (SHUT, 262.3, 0.15, 1.0)] + \
     [(PAPER, t, 0.1, 1.0) for t in (96.58, 199.96, 276.86, 320.98, 419.29, 550.63, 606.55)]    # documents sliding in
a_in = ["-t", f"{DUR:.4f}", "-i", os.path.join(VID, "voiceover-full.mp3"),
        "-stream_loop", "-1", "-t", "34.5", "-i", os.path.join(sfx, "sfx-night-forest.mp3")]
a_f = ["[0:a]volume=1.0[vo]", "[1:a]volume=0.10,afade=t=in:d=0.8,afade=t=out:st=33.2:d=0.7[amb]"]
mix, n = ["[vo]", "[amb]"], 2
bmix = []
for bed, t0, t1, ss in BEDS:
    st = max(0.0, t0 - 0.5)
    ln = min(DUR, t1 + 0.5) - st
    a_in += ["-ss", str(ss), "-stream_loop", "-1", "-t", f"{ln:.3f}", "-i", os.path.join(MUSIC, f"bed-{bed}.mp3")]
    ms = int(st * 1000)
    a_f.append(f"[{n}:a]aresample=48000,volume={GAIN[bed]},afade=t=in:d=1.0,afade=t=out:st={ln - 1.0:.3f}:d=1.0,adelay={ms}|{ms}[b{n}]")
    bmix.append(f"[b{n}]")
    n += 1
duck = "*".join(f"(1-clip((t-{a})/0.5\\,0\\,1)+clip((t-{b})/{r}\\,0\\,1))" for a, b, r in OUTS)
a_f.append("".join(bmix) + f"amix=inputs={len(bmix)}:normalize=0:duration=longest,apad,atrim=0:{DUR:.4f},"
           f"volume='{duck}':eval=frame,afade=t=out:st={DUR - 2.5:.3f}:d=2.5[bed]")
mix.append("[bed]")
for name, t, vol, ln in FX:
    a_in += ["-t", str(ln), "-i", os.path.join(sfx, name)]
    ms = int(t * 1000)
    a_f.append(f"[{n}:a]aresample=48000,afade=t=in:d=0.05,afade=t=out:st={ln - 0.4:.2f}:d=0.4,volume={vol},adelay={ms}|{ms}[f{n}]")
    mix.append(f"[f{n}]")
    n += 1
for s_ in stems:
    a_in += ["-i", s_]
    mix.append(f"[{n}:a]")
    n += 1
a_f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{DUR:.4f},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
snd = os.path.join(R, "_full_sound.wav")
run(FF + a_in + ["-filter_complex", ";".join(a_f), "-map", "[a]", "-t", f"{DUR:.4f}", "-ar", "48000", snd], "sound")

# 4. mux
run(FF + ["-i", pic, "-i", snd, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
          "-t", f"{DUR:.4f}", "-movflags", "+faststart", OUT], "mux")
print(OUT)
