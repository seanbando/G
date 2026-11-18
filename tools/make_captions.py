"""Make a captions file (.srt) with $ and % numbers from line timings.

Usage:
    python3 tools/make_captions.py <words.json> <display.txt> <out.srt> [--max-words 3]

display.txt has one line per voice-over line, "VO-01 <text as viewers should
read it>", with amounts written the on-screen way ($1,600, 6.2%). Each line
is cut into captions of up to --max-words words (2 or 3 reads best), timed
from the real word timings in words.json when present (else spread across the line) (tools/word_times.py or ElevenLabs
speech-to-text converted to the same shape).
"""
import json
import re
import sys


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main(words_json, display, out, max_words=3):
    data = json.load(open(words_json))
    lines = {l["id"]: l for l in data["lines"]}
    by_line = {}
    for w in data.get("words", []):
        by_line.setdefault(w["line"], []).append(w)

    def time_at(line_id, frac):
        """Map a 0..1 position in the line's text to a time using the real word timings."""
        ws = by_line.get(line_id)
        line = lines[line_id]
        if not ws:
            return line["start"] + (line["end"] - line["start"]) * frac
        total = sum(len(w["text"]) + 1 for w in ws)
        acc = 0.0
        for w in ws:
            k = (len(w["text"]) + 1) / total
            if frac <= acc + k:
                u = (frac - acc) / k if k else 0
                return w["start"] + (w["end"] - w["start"]) * u
            acc += k
        return ws[-1]["end"]
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
        total, acc = sum(weights), 0.0
        ws, ptr = by_line.get(k, []), 0
        starts = []
        for c, wgt in zip(chunks, weights):
            s = time_at(k, acc / total)
            first = re.sub(r"[^a-z0-9]", "", c[0].lower())
            for j in range(ptr, len(ws)):  # snap to the real start of the same spoken word
                if first and re.sub(r"[^a-z0-9]", "", ws[j]["text"].lower()) == first:
                    s, ptr = ws[j]["start"], j + 1
                    break
            starts.append(s)
            acc += wgt
        ends = starts[1:] + [line["end"]]
        for c, s, e in zip(chunks, starts, ends):
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
