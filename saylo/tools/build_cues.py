"""Build the edit cue sheet: when each shot starts, timed to the voiceover.

Usage: python3 saylo/tools/build_cues.py saylo/videos/NN-slug

Reads <video>/cue-anchors.txt (one line per shot: number|first words of the narration it starts on|file name;
use CLIP:<word> to start a shot at a clip slot whose label contains <word>) and <video>/vo-timings.tsv.
Writes <video>/edit-cues.md and edit-cues.csv. Rerun after any voiceover rebuild.
"""
import os
import re
import sys

NOTES = {"911": "no narration: 911 call audio plays here if you find the real released recording; otherwise trim this gap",
         "blast": "no narration: blast clip audio", "apartment": "no narration: news clip audio plays",
         "Bobi": "no narration: her press-conference audio plays", "60 Minutes": "no narration: Jewell's interview audio plays",
         "manhunt": "no narration: news clip audio plays"}


def main(video):
    tim = [l.split("\t") for l in open(os.path.join(video, "vo-timings.tsv")).read().splitlines()[1:]]
    sec = lambda s: int(s.split(":")[0]) * 60 + float(s.split(":")[1])
    fmt = lambda s: f"{int(s // 60)}:{s % 60:05.2f}"
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("—", " ").replace("-", " ").replace("'", ""))
    chunks = [(r[0], sec(r[2]), sec(r[3]), r[4]) for r in tim]
    total = sec(tim[-1][3])
    shots, missing = [], []
    for line in open(os.path.join(video, "cue-anchors.txt")):
        if not line.strip():
            continue
        n, a, f = line.rstrip("\n").split("|")
        t = None
        if a.startswith("CLIP:"):
            word = a[5:]
            t = next(c[1] for c in chunks if c[0] == "CLIP" and word in c[3])
            a = f"({word} clip, music out)"
        else:
            key = norm(a).split()
            for cid, s0, s1, txt in chunks:
                if cid == "CLIP":
                    continue
                ws = norm(txt).split()
                hit = next((i for i in range(len(ws) - len(key) + 1) if ws[i:i + len(key)] == key), None)
                if hit is not None:
                    t = s0 + (s1 - s0) * hit / len(ws)
                    break
        if t is None:
            missing.append(n)
            continue
        shots.append([n, t, a, f])
    shots.sort(key=lambda x: x[1])
    for i, s in enumerate(shots):
        s.append(shots[i + 1][1] if i + 1 < len(shots) else total)
    clips = [c for c in chunks if c[0] == "CLIP"]
    md = ["# Edit Cues: when each shot starts", "",
          f"Timed to `voiceover-full.mp3` (**{fmt(total)}**). Shot numbers and file names match the Shot List doc. Sorted by time, so a few shots come out of number order when the narration says them in a different order.", "",
          "- **Start**: put the shot's first frame here (when the narration reaches the cue words).",
          "- **End**: where the next shot starts. Hold or trim the file to fit.",
          "- **⏸ rows**: the narration pauses so a clip's own audio can play. Music drops out. The shot above keeps running through it.",
          "- Line starts are exact; cues in the middle of a line are estimated from word position (±0.3 s).", "",
          "| Shot | Start | End | Narration cue | File |", "|---|---|---|---|---|"]
    csv = ["shot,start_sec,end_sec,start,end,cue,file"]
    rows = [(s[1], 0, s) for s in shots] + [(c[1], 1, c) for c in clips]
    for t, k, x in sorted(rows, key=lambda r: (r[0], -r[1])):
        if k == 0:
            n, t, a, f, e = x
            md.append(f"| {n} | {fmt(t)} | {fmt(e)} | {a} | {f} |")
            csv.append(f'{n},{t:.2f},{e:.2f},{fmt(t)},{fmt(e)},"{a}","{f}"')
        else:
            lab = next((v for k2, v in NOTES.items() if k2 in x[3]), "no narration: clip audio plays")
            md.append(f"| ⏸ | {fmt(x[1])} | {fmt(x[2])} | *{lab}* | |")
            csv.append(f'PAUSE,{x[1]:.2f},{x[2]:.2f},{fmt(x[1])},{fmt(x[2])},"{lab}",""')
    md += ["", "**Music out** also for the 4.5 s after \"He was 44.\" (shot 82)."]
    open(os.path.join(video, "edit-cues.md"), "w").write("\n".join(md) + "\n")
    open(os.path.join(video, "edit-cues.csv"), "w").write("\n".join(csv) + "\n")
    print(f"{len(shots)} shots, {len(clips)} clip pauses, total {fmt(total)}" + (f"; NOT FOUND: {missing}" if missing else ""))


if __name__ == "__main__":
    main(sys.argv[1].rstrip("/"))
