"""Write motion cues for tools/edit_short.py from word timings.

Usage:
    python3 tools/auto_punch.py <words.json> [--every 1.6] > motion.txt

Gives the Jensen-short feel of something changing about every second:
- a punch-in on the first word of every money amount or percentage
  (words like "dollars", "percent", "hundred", "thousand", digits)
- a "reframe" (a jump to a slightly different framing, like a cut) roughly
  every --every seconds in between, never within 0.6 s of a punch
Paste the output into a short's transitions file, then add the hand-placed
transitions (zoomthru, whip) and cards on top.
"""
import json
import re
import sys

NUM = re.compile(r"^(\$?\d|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                 r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|"
                 r"forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|"
                 r"trillion|percent|dollars?)", re.I)


def main(path, every=1.6):
    words = json.load(open(path))["words"]
    punches, prev_num = [], False
    for w in words:
        is_num = bool(NUM.match(w["text"].strip(".,?!\"'")))
        if is_num and not prev_num:
            punches.append(w["start"])
        prev_num = is_num and not re.search(r"[.,?!]$", w["text"])
    end = words[-1]["end"]
    print("# Auto motion from tools/auto_punch.py")
    for p in punches:
        print(f"{p:.2f}  punch")
    t, k = 0.8, 0
    while t < end - 0.5:
        if all(abs(t - p) > 0.6 for p in punches):
            print(f"{t:.2f}  reframe {k % 3}")
            k += 1
        t += every


if __name__ == "__main__":
    argv = sys.argv[1:]
    every = 1.6
    if "--every" in argv:
        i = argv.index("--every")
        every = float(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) != 1:
        sys.exit(__doc__)
    main(argv[0], every)
