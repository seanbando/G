"""Join the whole Frein film and mix ONE soundtrack for it.

Picture: every section's build/render/<dir>/_picture.mp4 (left by assemble.py), in plan order, as a plain concat.
Sound, mixed once over the full length (same levels as the section review mixes, so nothing shifts):
  - voiceover-full.mp3, untouched (approved; never regenerated)
  - one continuous music bed (bed-A, looped) at 0.15 under everything; the section mixes start it at start % 150,
    so the music lines up with what the creator already heard
  - night-forest ambience under the cold open only
  - typewriter keys at every typed text, from every plan's "types"
  - loudnorm to -14 LUFS, true peak -1.5

  python final.py                 # all sections must have a _picture.mp4; -> build/render/frein_final.mp4
  python final.py --partial       # join the rendered sections from 0:00 up to the first missing one
  python final.py --render DIR    # read the _picture.mp4 files from DIR/<dir>/ instead (testing)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(HERE, "..", ".."))
REPO = os.path.normpath(os.path.join(VID, "..", "..", ".."))
SOUND = os.path.join(REPO, "saylo", "videos", "01-olympic-bomber", "sound")
PLANS = [f"shots{i}.json" for i in range(2, 10)]          # cold open .. handoff + outro, in film order
BED, BED_LEN, BED_VOL = os.path.join(SOUND, "music", "bed-A.mp3"), 150.0, 0.15
FF = ["ffmpeg", "-hide_banner", "-loglevel", os.environ.get("FFLOG", "error"), "-y", "-nostdin"]

args = sys.argv[1:]
PARTIAL = "--partial" in args
RENDER = os.path.join(VID, "build", "render")
if "--render" in args:
    RENDER = os.path.abspath(args[args.index("--render") + 1])


def run(cmd, what):
    print("..", what, flush=True)
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)


def graph_opt():
    """ffmpeg 7+ reads an option's value from a file with "-/option"; older builds only know -filter_complex_script."""
    v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split()[2]
    try:
        major = int(v.split(".")[0].lstrip("n"))
    except ValueError:                                     # git builds ("N-12345-g...") are new
        major = 99
    return "-/filter_complex" if major >= 7 else "-filter_complex_script"


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


# 1. collect the sections and check each picture is the length its plan says
sections, missing = [], []
fps = None
for name in PLANS:
    cfg = json.load(open(os.path.join(HERE, name), encoding="utf-8"))
    fps = fps or cfg["fps"]
    if cfg["fps"] != fps:
        sys.exit(f"{name}: fps {cfg['fps']} differs from {fps}")
    start = cfg.get("start", 0.0)
    want = (round(cfg["end"] * fps) - round(start * fps)) / fps
    pic = os.path.join(RENDER, cfg.get("dir", "shots"), "_picture.mp4")
    if not os.path.exists(pic):
        missing.append(name)
        continue
    if missing:                                            # a gap before this one: the film cannot be joined past it
        continue
    got = probe(pic)
    if abs(got - want) > 1.5 / fps:
        sys.exit(f"{name}: _picture.mp4 is {got:.3f} s, plan says {want:.3f} s. Re-run: python assemble.py {name} --picture")
    if sections and abs(sections[-1]["end"] - start) > 1e-6:
        sys.exit(f"{name}: starts at {start}, previous section ends at {sections[-1]['end']}")
    sections.append({"plan": name, "pic": pic, "start": start, "end": cfg["end"], "types": cfg.get("types", [])})

if missing and not PARTIAL:
    sys.exit("No _picture.mp4 yet for: " + ", ".join(missing) +
             "\nRender them (build.ps1 -Plan ...) or run with --partial to join what exists.")
if not sections:
    sys.exit("Nothing rendered yet.")
END = sections[-1]["end"]
DUR = round(END * fps) / fps
tag = "final" if not missing else f"0000_{int(END // 60):02d}{int(END % 60):02d}"
out = os.path.join(RENDER, f"frein_{tag}.mp4")
print(f"{len(sections)} sections, 0:00-{int(END // 60)}:{END % 60:04.1f}" + (f"  (missing: {', '.join(missing)})" if missing else ""))

# 2. picture: plain concat (same codec settings in every section, so stream copy)
lst = os.path.join(RENDER, "_final_list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for s in sections:
        fh.write("file '" + s["pic"].replace("\\", "/").replace("'", "'\\''") + "'\n")
pic = os.path.join(RENDER, "_final_picture.mp4")
run(FF + ["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-t", f"{DUR:.4f}", pic], "picture")

# 3. one soundtrack over the whole length
sfx = os.path.join(SOUND, "sfx")
a_in = ["-t", f"{DUR:.4f}", "-i", os.path.join(VID, "voiceover-full.mp3"),
        "-stream_loop", "-1", "-t", f"{DUR:.4f}", "-i", BED]
a_f = ["[0:a]volume=1.0,apad[vo]",
       f"[1:a]volume={BED_VOL},afade=t=in:d=0.6,afade=t=out:st={DUR - 2.0:.3f}:d=2.0[bed]"]
mix = ["[vo]", "[bed]"]
ni = 2
if sections[0]["start"] == 0:                              # the cold open's woods ambience (as approved in v7)
    a_in += ["-stream_loop", "-1", "-t", "34", "-i", os.path.join(sfx, "sfx-night-forest.mp3")]
    a_f.append(f"[{ni}:a]volume=0.10,afade=t=in:d=0.8,afade=t=out:st=33.2:d=0.7[amb]")
    mix.append("[amb]")
    ni += 1
clicks = [(t, k) for s in sections for t, k in s["types"]]
for i, (t, kind) in enumerate(clicks):
    a_in += ["-t", "1.1", "-i", os.path.join(sfx, f"sfx-typewriter-keys-{kind}.mp3")]
    ms = max(0, int(t * 1000))
    a_f.append(f"[{ni + i}:a]afade=t=out:st=0.8:d=0.3,volume=0.3,adelay={ms}|{ms}[k{i}]")
    mix.append(f"[k{i}]")
a_f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{DUR:.4f},"
           "loudnorm=I=-14:TP=-1.5:LRA=11[a]")
graph = os.path.join(RENDER, "_final_sound.txt")            # long graph: pass it as a file (Windows command-line limit)
with open(graph, "w", encoding="utf-8") as fh:
    fh.write(";\n".join(a_f))
snd = os.path.join(RENDER, "_final_sound.wav")
run(FF + a_in + [graph_opt(), graph, "-map", "[a]", "-t", f"{DUR:.4f}", "-ar", "48000", snd],
    f"sound ({len(clicks)} typed texts)")

# 4. mux
run(FF + ["-i", pic, "-i", snd, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
          "-t", f"{DUR:.4f}", "-movflags", "+faststart", out], "mux")
print(out)
