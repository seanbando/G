"""Estimate when every spoken word lands in a joined narration track, for free.

Usage:
    python3 tools/word_times.py <script.md> <clips_dir> <out.json> [--tight] [--fit <track.mp3>]

Rebuilds the line layout exactly as build_track.py joins it (same gaps and
pauses, using the trimmed clips it wrote) and spreads each line's words over
the clip by their length. Accurate to a few tenths of a second, which is
enough for punch-ins and captions, and costs nothing (ElevenLabs
speech-to-text is more exact but uses credits). Use the same --tight setting
as the build; tracks built with --punch --speed 1.0 keep their timing.

--fit scales every time so the last word ends with the real track (the
limiter and encoder can shift the length by a few tenths of a second).

Output: {"lines": [{"id", "start", "end", "text"}], "words": [{"text", "start", "end", "line"}]}
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_voiceover import parse  # noqa: E402


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", path], capture_output=True, text=True).stdout)


def main(script, clips, out, tight=False, fit=None):
    same_gap, change_gap, scale = (0.1, 0.15, 0.6) if tight else (0.3, 0.4, 1.0)
    t, prev, lines, words = 0.0, None, [], []
    for line_id, voice, text, cues in parse(script)[1]:
        if prev:
            t += same_gap if voice == prev else change_gap
        t += scale * sum(float(x) for c in cues if c.startswith("⏸")
                         for x in re.findall(r"([\d.]+)\s*second", c))
        clip = os.path.join(clips, "trimmed", f"{line_id}_{voice.replace(' ', '_')}.mp3")
        d = duration(clip)
        lines.append(dict(id=line_id, start=round(t, 3), end=round(t + d, 3), text=text))
        toks = text.split()
        weights = [len(re.sub(r"[^\w]", "", w)) + 1 for w in toks]
        total, acc = sum(weights), 0.0
        for w, k in zip(toks, weights):
            s = t + d * acc / total
            acc += k
            words.append(dict(text=w, start=round(s, 3), end=round(t + d * acc / total, 3), line=line_id))
        t += d
        prev = voice
    if fit:
        k = (duration(fit) - 0.05) / t
        for item in lines + words:
            item["start"] = round(item["start"] * k, 3)
            item["end"] = round(item["end"] * k, 3)
        t *= k
    json.dump(dict(lines=lines, words=words), open(out, "w"), indent=1)
    print(f"{out}: {len(lines)} lines, {len(words)} words, ends at {t:.1f} s")


if __name__ == "__main__":
    argv = sys.argv[1:]
    fit = None
    if "--fit" in argv:
        i = argv.index("--fit")
        fit = argv[i + 1]
        del argv[i:i + 2]
    argv = [a for a in argv if a != "--tight"]
    if len(argv) != 3:
        sys.exit(__doc__)
    main(*argv, tight="--tight" in sys.argv, fit=fit)
