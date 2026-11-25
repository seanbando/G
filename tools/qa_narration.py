"""Listen to a finished narration and flag timing and wording problems.

Usage: python3 tools/qa_narration.py <script.md> <narration.mp3> [--model small.en] [--report out.md]

Transcribes the audio with Whisper (faster-whisper, word timestamps), lines
the words up against the script and reports, with timestamps and line IDs:

- pauses in the middle of a sentence
- long gaps between sentences or between lines (intended [PAUSE] beats are allowed)
- stretched words (one word held far too long)
- sentences read too slowly or too fast
- missing, extra or different words compared with the script

Works with both script formats: "ROLE: text" paragraphs (make_voiceover.py)
and "**S012 · NARRATOR · ~5 s**" lines (make_voiceover_v2.py).
Whisper writes numbers as digits ("250") while scripts spell them out, so
differences that only involve digits are counted, not flagged.
"""
import argparse
import difflib
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(__file__))

# Thresholds (seconds / words per minute).
GAP_MID_SENTENCE = 0.55   # silence inside a sentence, between words with no punctuation
GAP_AT_COMMA = 0.85       # a breath at a comma is natural
GAP_BETWEEN_SENTENCES = 1.0
GAP_BETWEEN_LINES = 1.1
STRETCHED_WORD = 1.0      # a single word held this long (short words only)
SLOW_WPM = 140           # sentences that drag ("slow motion")
FAST_WPM = 320           # only truly rushed sentences; fast natural delivery is fine
# Words Whisper hears as a sound-alike; not counted as wording errors.
SOUND_ALIKES = {("cede", "seed"), ("virtu", "virtue"), ("cede", "seeding")}
MIN_SENTENCE_WORDS = 6    # pace is only judged on sentences this long


def load_script(path):
    """Return a list of (line_id, text, pause_seconds_before)."""
    text = open(path).read()
    if re.search(r"^\*\*S\d+ · ", text, re.M):
        from make_voiceover_v2 import parse as parse_v2
        _, items = parse_v2(path)
        out, pause = [], 0.0
        for it in items:
            if it[0] == "pause":
                m = re.search(r"([\d.]+)\s*second", it[1])
                pause += float(m.group(1)) if m else 0.0
            elif it[0] == "line":
                out.append((it[1], it[4], pause))
                pause = 0.0
        return out
    from make_voiceover import parse as parse_v1
    _, lines = parse_v1(path)
    out = []
    for line_id, _, txt, cues in lines:
        pause = sum(float(m) for c in cues if c.startswith("⏸") for m in re.findall(r"([\d.]+)\s*second", c))
        out.append((line_id, txt, pause))
    return out


def norm_tokens(text):
    """Lowercase word tokens; letter-by-letter spellings (D-T-C-C, U.S.) collapse into one token."""
    text = text.replace("&", " and ").replace("’", "'")
    # Letter-by-letter spellings (D-T-C-C, S-I-P-C, U.S.) become one token.
    text = re.sub(r"\b(?:[A-Za-z][-.]){1,}[A-Za-z]\b\.?", lambda m: re.sub(r"[-.]", "", m.group(0)), text)
    raw = re.findall(r"[A-Za-z0-9']+", text.replace("-", " ").replace(".", " "))
    out = []
    for w in raw:
        w = w.lower().strip("'")
        if not w:
            continue
        if len(w) == 1 and w.isalpha() and w not in ("a", "i") and out and out[-1].startswith("§"):
            out[-1] += w
        elif len(w) == 1 and w.isalpha() and w not in ("a", "i"):
            out.append("§" + w)
        else:
            out.append(w)
    return [w.lstrip("§") for w in out]


def expected_words(script):
    """Flatten the script into tokens with line id, sentence-end flag and line-start flag."""
    toks = []
    for line_id, text, pause in script:
        sentences = re.split(r"(?<=[.?!])\s+", text.strip())
        first = True
        for s in sentences:
            ws = norm_tokens(s)
            commas = set()
            n = 0
            for part in re.split(r"(,|;|:)", s):
                if part in (",", ";", ":"):
                    commas.add(n - 1)
                else:
                    n += len(norm_tokens(part))
            for i, w in enumerate(ws):
                toks.append({"w": w, "line": line_id, "end": i == len(ws) - 1, "comma": i in commas,
                             "line_start": first and i == 0, "pause": pause if first and i == 0 else 0.0})
            first = False
    return toks


def transcribe(audio, model_name):
    from faster_whisper import WhisperModel
    import subprocess
    import numpy as np
    # Decode with ffmpeg (16 kHz mono) instead of faster-whisper's own decoder,
    # which breaks with some versions of the PyAV library.
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    samples = np.frombuffer(pcm, dtype=np.float32)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(samples, word_timestamps=True, beam_size=5, vad_filter=False,
                                   condition_on_previous_text=False)
    words = []
    for seg in segments:
        for w in seg.words or []:
            for t in norm_tokens(w.word) or [w.word.strip().lower()]:
                words.append({"w": t, "start": w.start, "end": w.end})
    return words


def ts(sec):
    return f"{int(sec // 60)}:{sec % 60:05.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("audio")
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--report")
    args = ap.parse_args()

    script = load_script(args.script)
    exp = expected_words(script)
    heard = transcribe(args.audio, args.model)

    sm = difflib.SequenceMatcher(a=[e["w"] for e in exp], b=[h["w"] for h in heard], autojunk=False)
    match = {}  # expected index -> heard index
    word_issues, digit_diffs = [], 0
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            for k in range(a2 - a1):
                match[a1 + k] = b1 + k
            continue
        said = " ".join(h["w"] for h in heard[b1:b2])
        wanted = " ".join(e["w"] for e in exp[a1:a2])
        if re.search(r"\d", said):
            digit_diffs += 1
            continue
        if (wanted, said) in SOUND_ALIKES:
            continue
        where = heard[b1]["start"] if b1 < len(heard) else (heard[-1]["end"] if heard else 0)
        line = exp[a1]["line"] if a1 < len(exp) else exp[-1]["line"]
        kind = {"replace": "different words", "delete": "missing words", "insert": "extra words"}[op]
        word_issues.append((where, line, f"{kind}: script \"{wanted}\" / heard \"{said}\""))

    gaps, stretched = [], []
    durs = [h["end"] - h["start"] for h in heard]
    for i in range(1, len(exp)):
        if i not in match or (i - 1) not in match:
            continue
        prev, cur = heard[match[i - 1]], heard[match[i]]
        gap = cur["start"] - prev["end"]
        e = exp[i]
        if e["line_start"]:
            limit, label = GAP_BETWEEN_LINES + e["pause"], "gap between lines"
        elif exp[i - 1]["end"]:
            limit, label = GAP_BETWEEN_SENTENCES, "gap between sentences"
        elif exp[i - 1]["comma"]:
            limit, label = GAP_AT_COMMA, "long pause at a comma"
        else:
            limit, label = GAP_MID_SENTENCE, "pause in the middle of a sentence"
        if gap > limit:
            gaps.append((prev["end"], e["line"], f"{label}: {gap:.2f} s after \"{exp[i - 1]['w']}\", before \"{e['w']}\""))
    for i, j in match.items():
        h = heard[j]
        d = h["end"] - h["start"]
        if d > STRETCHED_WORD and len(h["w"]) <= 8:
            stretched.append((h["start"], exp[i]["line"], f"stretched word: \"{h['w']}\" held {d:.2f} s"))

    pace = []
    i = 0
    while i < len(exp):
        j = i
        while j < len(exp) and not exp[j]["end"]:
            j += 1
        idx = [k for k in range(i, j + 1) if k in match]
        # Only judge pace when the sentence's first and last words were both heard,
        # and count every script word (numbers included) over that span.
        if j - i + 1 >= MIN_SENTENCE_WORDS and i in match and j in match:
            start, end = heard[match[i]]["start"], heard[match[j]]["end"]
            wpm = (j - i + 1) / max(end - start, 0.01) * 60
            if wpm < SLOW_WPM or wpm > FAST_WPM:
                pace.append((start, exp[i]["line"], f"{'slow' if wpm < SLOW_WPM else 'fast'} sentence: {wpm:.0f} wpm"))
        i = j + 1

    issues = sorted(gaps + stretched + pace + word_issues)
    matched_pct = len(match) / max(len(exp), 1) * 100
    lines = [f"# Narration check: {os.path.basename(args.audio)}", "",
             f"- Script words matched in the audio: {matched_pct:.1f}% ({len(match)} of {len(exp)})",
             f"- Differences involving only numbers written as digits (not flagged): {digit_diffs}",
             f"- Median word length: {st.median(durs):.2f} s" if durs else "- No words heard",
             f"- Issues found: {len(issues)}", ""]
    groups = [("Pauses and gaps", gaps), ("Stretched words", stretched), ("Pace", pace), ("Wording", word_issues)]
    for title, rows in groups:
        lines.append(f"## {title} ({len(rows)})")
        lines += [f"- **{ts(t)}** · {line} · {msg}" for t, line, msg in sorted(rows)] or ["- none"]
        lines.append("")
    report = "\n".join(lines)
    print(report)
    if args.report:
        open(args.report, "w").write(report + "\n")


if __name__ == "__main__":
    main()
