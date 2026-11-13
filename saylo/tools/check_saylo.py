"""Check a Saylo script against the style sheet.

Usage: python3 saylo/tools/check_saylo.py <script.md>

Ignores headings, [VISUAL ...] notes, [PART 2] and the metadata lines at the top.
Reports blocked words, length/runtime, sentence-length spread, and the size of
each half (voice tools often cap at 10,000 characters).
"""
import re
import statistics as st
import sys

BLOCKED = [
    "in conclusion", "important to note", "furthermore", "moreover", "consequently", "in summary",
    "wrap things up", "dive in", "dive into", "without further ado", "worth noting", "conversely",
    "notably", "additionally", "subsequently", "unlocking", "embark", "game-changer", "ultimate guide",
    "master the art", "landscape", "realm", "tapestry", "testament", "beacon of hope", "unleash",
    "elevate", "navigating", "various factors", "on one hand", "remains to be seen", "ideally",
    "typically", "generally speaking", "while it may seem", "remember to always", "crucial", "foster",
    "paramount", "have you ever wondered", "fast-paced", "digital age", "modern world", "welcome back",
    "delve", "underscore", "nuanced", "unlock", "optimization", "leverage", "holistic", "synergy",
    "robust", "streamline", "revolutionize", "carefully orchestrated", "multifaceted", "this isn't just",
]
META = re.compile(r"^(#.*|---|Thumbnail.*|Test against.*)$", re.M)


def spoken(text):
    text = re.sub(r"\[VISUAL[^\]]*\]|\[PART 2\]", "", text)
    return META.sub("", text)


def main(path):
    raw = open(path, encoding="utf-8").read()
    body = spoken(raw)
    low = body.lower()
    hits = [w for w in BLOCKED if re.search(r"\b" + re.escape(w), low)]
    words = len(body.split())
    sents = [s for s in re.split(r"(?<=[.!?])\s+|\n+", body) if s.split()]
    lens = [len(s.split()) for s in sents]
    print(f"Blocked words: {', '.join(hits) if hits else 'none'}")
    print(f"Words: {words}  (~{words/160:.1f} min at 160 wpm; target 2,900-3,400)")
    if len(lens) > 1:
        print(f"Sentences: {len(lens)}  mean {st.mean(lens):.1f}  stdev {st.stdev(lens):.1f}  "
              f"range {min(lens)}-{max(lens)}  <=5 words {sum(l <= 5 for l in lens)*100//len(lens)}%  "
              f">=25 words {sum(l >= 25 for l in lens)*100//len(lens)}%")
    if "[PART 2]" in raw:
        a, b = raw.split("[PART 2]", 1)
        print(f"Part 1: {len(spoken(a)):,} chars  Part 2: {len(spoken(b)):,} chars  (voice-tool limit ~10,000)")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
