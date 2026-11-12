"""Quick writing check for a script: stock AI phrasing, repeated openers,
lists of three, and how much sentence length varies.

Usage: python3 tools/check_script.py <script.md>
"""
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_voiceover import parse  # noqa: E402

FLAGGED = ["delve", "furthermore", "moreover", "consequently", "hence", "thus", "it may seem",
           "some might argue", "remains to be seen", "leverage", "optimize", "synergy", "robust",
           "comprehensive", "holistic", "in today's world", "at the end of the day",
           "it's important to note", "it is important to note", "without further ado", "crucial",
           "in the world of", "digital age", "navigate", "landscape", "realm", "tapestry",
           "seamless", "unlock", "game-changer"]


def main(path):
    _, lines = parse(path)
    text = " ".join(l[2] for l in lines)
    hits = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", text, re.I)) for w in FLAGGED}
    hits = {w: n for w, n in hits.items() if n}
    sents = [s for s in re.split(r"(?<=[.?!])\s+", text) if s]
    lens = [len(s.split()) for s in sents]
    mid = sum(1 for n in lens if 15 <= n <= 25) / len(lens)
    cv = st.pstdev(lens) / st.mean(lens)
    openers = len(re.findall(r"\b(?:So here's|Here's)\b", text))
    threes = len(re.findall(r"\w+, \w+(?: \w+)?, and \w+", text))

    print(f"Flagged phrases: {hits or 'none'}")
    print(f"Sentences: {len(lens)}, {min(lens)} to {max(lens)} words, average {st.mean(lens):.1f}")
    print(f"Share in the 15-25 word range: {mid:.0%} (lower is less uniform)")
    print(f"Length variation (stdev / mean): {cv:.2f} (around 0.5 or more is varied)")
    print(f"'Here's' openers: {openers} (aim for 2 or fewer)")
    print(f"Lists of three: {threes}")


if __name__ == "__main__":
    main(sys.argv[1])
