"""Measure the real start/end time of every spoken word (ElevenLabs speech-to-text).

Usage:
    python3 tools/stt_words.py <script.md> <track.mp3> <out_words.json>

Sends the finished narration track to ElevenLabs Scribe with word timestamps (uses a small
amount of credits), keeps the raw result next to the output (<out>.stt-raw.json, reused if it
exists so a rerun costs nothing), then aligns the recognized words to the script's words
in order. Script words the recognizer wrote differently (numbers as digits, names) get times
interpolated between their matched neighbours. Output has the same shape as
tools/word_times.py: {"lines": [{id, start, end, text}], "words": [{text, start, end, line}]}.
"""
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_voiceover import parse  # noqa: E402


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def transcribe(track, raw_path):
    if os.path.exists(raw_path):
        return json.load(open(raw_path))
    from elevenlabs.client import ElevenLabs
    client = ElevenLabs()
    with open(track, "rb") as f:
        res = client.speech_to_text.convert(model_id="scribe_v1", file=f, language_code="en",
                                            timestamps_granularity="word", tag_audio_events=False)
    words = [dict(text=w.text, start=w.start, end=w.end) for w in res.words if getattr(w, "type", "word") == "word"]
    json.dump(dict(text=res.text, words=words), open(raw_path, "w"), indent=1)
    return dict(text=res.text, words=words)


def main(script, track, out):
    raw = transcribe(track, out + ".stt-raw.json")
    rec = raw["words"]
    sw = []  # (line_id, text)
    for line_id, voice, text, _ in parse(script)[1]:
        for tok in text.split():
            sw.append((line_id, tok))
    a = [norm(t) for _, t in sw]
    b = [norm(w["text"]) for w in rec]
    times = [None] * len(sw)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            r = rec[blk.b + k]
            times[blk.a + k] = (r["start"], r["end"])
    matched = sum(t is not None for t in times)
    # interpolate unmatched words between neighbours
    i = 0
    while i < len(times):
        if times[i] is None:
            j = i
            while j < len(times) and times[j] is None:
                j += 1
            t0 = times[i - 1][1] if i > 0 else 0.0
            t1 = times[j][0] if j < len(times) else (rec[-1]["end"] if rec else t0 + 0.3 * (j - i))
            step = (t1 - t0) / (j - i)
            for k in range(i, j):
                times[k] = (t0 + step * (k - i), t0 + step * (k - i + 1))
            i = j
        else:
            i += 1
    words = [dict(text=t, start=round(s, 3), end=round(e, 3), line=lid) for (lid, t), (s, e) in zip(sw, times)]
    lines = []
    for lid in dict.fromkeys(l for l, _ in sw):
        ws = [w for w in words if w["line"] == lid]
        lines.append(dict(id=lid, start=ws[0]["start"], end=ws[-1]["end"], text=" ".join(w["text"] for w in ws)))
    json.dump(dict(lines=lines, words=words), open(out, "w"), indent=1)
    print(f"{out}: {len(words)} words, {matched} measured directly, {len(words) - matched} interpolated")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
