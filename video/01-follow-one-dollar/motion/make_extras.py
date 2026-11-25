"""Writes the upload extras for the master: captions (SRT) and YouTube chapters.

Usage: python3 video/01-follow-one-dollar/motion/make_extras.py
Both come straight from the script and the voiceover timings, so they match the video.
"""
import json
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
FINAL = os.path.join(HERE, "..", "final")
T = json.load(open(os.path.join(ROOT, "audio", "follow-one-dollar-v6", "timings.json")))
L = T["lines"]


def stamp(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


out = []
for i, l in enumerate(L):
    nxt = L[i + 1]["start"] if i + 1 < len(L) else T["duration"]
    end = min(nxt - 0.05, l["end"] + 1.2)   # numbers at the end of a line are spoken after the last timed word
    out.append(f"{i + 1}\n{stamp(l['start'])} --> {stamp(end)}\n" + "\n".join(textwrap.wrap(l["text"], 42)) + "\n")
os.makedirs(FINAL, exist_ok=True)
open(os.path.join(FINAL, "captions.srt"), "w").write("\n".join(out))

CHAPTERS = [("S001", "Where does your dollar actually go?"), ("S012", "What your dollar buys: shares explained with pizza"), ("S031", "Stop 1: Your investing app"),
            ("S040", "Stop 2: The market maker"), ("S055", "Stop 3: The stock exchange"), ("S072", "Stop 4: The seller (quiz: how much does Apple get?)"), ("S086", "Stop 5: Making it official (DTCC, Cede & Co.)"),
            ("S106", "How a share makes money"), ("S127", "Index funds: the basket"), ("S142", "Three checks before you tap buy"), ("S154", "Recap and my first stock")]
start = {l["id"]: l["start"] for l in L}
lines = []
for k, (sid, title) in enumerate(CHAPTERS):
    t = 0 if k == 0 else start[sid]
    lines.append(f"{int(t // 60)}:{int(t % 60):02d} {title}")
open(os.path.join(FINAL, "youtube-chapters.txt"), "w").write("\n".join(lines) + "\n\nNot financial advice. For education only.\n")
print("\n".join(lines))
