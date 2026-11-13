"""Make a captions file (.srt) with $ and % numbers from line timings.

Usage:
    python3 tools/make_captions.py <words.json> <display.txt> <out.srt> [--max-words 3]

display.txt has one line per voice-over line, "VO-01 <text as viewers should
read it>", with amounts written the on-screen way ($1,600, 6.2%). Each line
is cut into captions of up to --max-words words (2 or 3 reads best), timed
across that line's span from words.json (tools/word_times.py or ElevenLabs
speech-to-text converted to the same shape).
"""
import json
import re
import sys


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main(words_json, display, out, max_words=3):
    lines = {l["id"]: l for l in json.load(open(words_json))["lines"]}
    shown = {}
    for raw in open(display):
        raw = raw.strip()
        if raw and not raw.startswith("#"):
            k, text = raw.split(None, 1)
            shown[k] = text
    cues = []
    for k, line in lines.items():
        toks = shown.get(k, line["text"]).split()
        chunks, cur = [], []
        for tok in toks:
            cur.append(tok)
            if len(cur) >= max_words or re.search(r"[.,?!]$", tok):
                chunks.append(cur)
                cur = []
        if cur:
            if chunks and len(cur) == 1 and len(chunks[-1]) < max_words + 1:
                chunks[-1] += cur
            else:
                chunks.append(cur)
        weights = [sum(len(t) + 1 for t in c) for c in chunks]
        total, acc, span = sum(weights), 0.0, line["end"] - line["start"]
        for c, wgt in zip(chunks, weights):
            s = line["start"] + span * acc / total
            acc += wgt
            e = line["start"] + span * acc / total
            text = " ".join(re.sub(r"[,.]$", "", t) for t in c)
            cues.append((s, e, text))
    with open(out, "w") as f:
        for n, (s, e, text) in enumerate(cues, 1):
            f.write(f"{n}\n{ts(s)} --> {ts(e)}\n{text}\n\n")
    print(f"{out}: {len(cues)} captions")


if __name__ == "__main__":
    argv = sys.argv[1:]
    mw = 3
    if "--max-words" in argv:
        i = argv.index("--max-words")
        mw = int(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) != 3:
        sys.exit(__doc__)
    main(*argv, max_words=mw)
