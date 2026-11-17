#!/usr/bin/env python3
"""Voiceover gate: compare a word-timed transcript of the finished voiceover
against the script and flag every stutter, wrong/missing/extra word, dead air
and rushed or dragging line. A voiceover may only be used when this reports
ZERO problems (and the creator has listened once start to finish).

Usage:
  python3 saylo/tools/check_vo.py WORDS.json SCRIPT.txt [SCRIPT2.txt ...] [--out report.md]

WORDS.json = [{"w": "Three", "s": 0.06, "e": 0.24}, ...]  (ElevenLabs scribe
word timestamps of the FINAL mixed voiceover file, e.g. vo-words.json).
SCRIPT.txt = the exact text that was sent to the voice (voiceover-part*.txt).
Lines in [brackets] and markdown headings are ignored. A pause marked
[PAUSE] or "..." in the script is allowed to be long.
"""
import json, re, sys, statistics, difflib

MID_GAP = 0.75     # silence inside a sentence longer than this = delay/hesitation
END_GAP = 1.60     # silence between sentences longer than this = dead air
RUSHED = 0.06      # less than this between sentences = no breath, sounds glued
PACE_SD = 2.2      # sentence pace this many SDs from the mean = rushed/dragging


def norm(t):
    t = t.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9']", "", t)


CONTRACT = {"'ve": " have", "'ll": " will", "'re": " are", "'d": " would", "n't": " not", "'m": " am"}


def same_words(a, b):
    def flat(t):
        t = t.lower().replace("’", "'")
        for k, val in CONTRACT.items():
            t = t.replace(k, val)
        return re.sub(r"[^a-z0-9]", "", t)
    fa, fb = flat(a), flat(b)
    return fa == fb or (fa and fb and difflib.SequenceMatcher(None, fa, fb).ratio() > 0.93 and abs(len(fa) - len(fb)) <= 2)


def script_tokens(paths):
    toks = []  # (normalized, raw, sentence_end, pause_ok)
    for p in paths:
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pause_line = "[PAUSE" in line.upper()
            line = re.sub(r"\[[^\]]*\]", " ", line)
            for raw in line.split():
                n = norm(raw)
                if not n:
                    continue
                end = bool(re.search(r"[.!?…]['\"”’)]*$", raw)) and not re.fullmatch(r"(?:[A-Za-z]\.){2,}[,]?", raw)
                pause = pause_line or raw.endswith("...") or raw.endswith("…") or raw.endswith("—")
                toks.append((n, raw, end, pause))
    return toks


def ts(x):
    return f"{int(x // 60)}:{x % 60:05.2f}"


def main():
    args = sys.argv[1:]
    out = None
    if "--out" in args:
        i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
    words = json.load(open(args[0]))
    stoks = script_tokens(args[1:])
    v = [norm(w["w"]) for w in words]
    s = [t[0] for t in stoks]
    problems = []

    # 1. wrong / missing / extra words (number formatting differences are ignored)
    sm = difflib.SequenceMatcher(None, s, v, autojunk=False)
    vpos_for_s = {}
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            for k in range(a2 - a1):
                vpos_for_s[a1 + k] = b1 + k
            continue
        sa = " ".join(t[1] for t in stoks[a1:a2]); vb = " ".join(w["w"] for w in words[b1:b2])
        if any(c.isdigit() for c in sa + vb):
            continue  # "1998" vs "nineteen ninety-eight"
        if same_words(sa, vb):
            continue  # "should've" vs "should have", "half-remembered" vs "half remembered"
        at = words[min(b1, len(words) - 1)]["s"] if words else 0
        if op == "insert":
            # repeated word = stutter
            kind = "STUTTER/REPEAT" if b1 > 0 and v[b1] == v[b1 - 1] else "EXTRA WORD"
            problems.append((at, kind, f'heard "{vb}" that is not in the script'))
        elif op == "delete":
            problems.append((at, "MISSING", f'script says "{sa}" but it was not heard'))
        else:
            problems.append((at, "WRONG WORD", f'script "{sa}" → heard "{vb}"'))

    # 2. cut-off / partial words
    for w in words:
        if re.search(r"\w-$", w["w"]) or w["w"].endswith("--"):
            problems.append((w["s"], "STUTTER/CUT WORD", f'"{w["w"]}"'))

    # 3. gaps: hesitation mid-sentence, dead air between sentences, glued sentences
    end_after = {}
    for si, vi in vpos_for_s.items():
        end_after[vi] = (stoks[si][2], stoks[si][3])
    for i in range(len(words) - 1):
        gap = words[i + 1]["s"] - words[i]["e"]
        is_end, pause_ok = end_after.get(i, (bool(re.search(r"[.!?]$", words[i]["w"])), False))
        if pause_ok:
            continue
        if not is_end and gap > MID_GAP and not words[i]["w"].endswith((",", ":", ";")):
            problems.append((words[i]["e"], "DELAY", f'{gap:.2f}s silence inside a sentence after "{words[i]["w"]}"'))
        elif not is_end and gap > MID_GAP * 1.6:
            problems.append((words[i]["e"], "DELAY", f'{gap:.2f}s silence after "{words[i]["w"]}"'))
        elif is_end and gap > END_GAP:
            problems.append((words[i]["e"], "DEAD AIR", f'{gap:.2f}s silence after "{words[i]["w"]}"'))
        elif is_end and gap < RUSHED:
            problems.append((words[i]["e"], "GLUED", f'no breath after "{words[i]["w"]}" ({gap:.2f}s)'))

    # 4. sentence pace outliers
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.!?]$", w["w"]):
            sents.append(cur); cur = []
    rates = [(len(x) / max(0.3, x[-1]["e"] - x[0]["s"]), x) for x in sents if len(x) >= 7]
    if len(rates) > 5:
        mu = statistics.mean(r for r, _ in rates); sd = statistics.pstdev(r for r, _ in rates)
        for r, x in rates:
            if abs(r - mu) > PACE_SD * sd:
                kind = "RUSHED" if r > mu else "DRAGGING"
                txt = " ".join(w["w"] for w in x)
                problems.append((x[0]["s"], kind, f"{r * 60:.0f} wpm (avg {mu * 60:.0f}): {txt[:90]}"))

    problems.sort()
    lines = [f"# Voiceover gate: {len(problems)} problem(s)", ""]
    if problems:
        lines += ["| Time | Problem | Detail |", "|---|---|---|"]
        lines += [f"| {ts(t)} | {k} | {d} |" for t, k, d in problems]
        lines += ["", "Fix every row (regenerate that line/chunk, or trim the gap), re-transcribe, and run this again until it says 0."]
    else:
        lines += ["PASS: no stutters, wrong words, delays or dead air found. Now the creator listens once, start to finish."]
    rep = "\n".join(lines)
    print(rep)
    if out:
        open(out, "w").write(rep + "\n")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
