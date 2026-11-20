"""Cut dead space between words, using measured word timings (tools/stt_words.py).

Usage:
    python3 tools/tighten_gaps.py <in.mp3> <words.json> <out.mp3> [--sentence 0.13] [--comma 0.08] [--word 0.05]

Every gap between two words is shrunk to a short breath: --sentence after . ? !,
--comma after , ; : and --word otherwise. Only audio that is really quiet is removed
(each cut is checked against the loudness around it), and every cut gets a 10 ms
equal-power crossfade, so there are no clicks. Nothing inside a word is touched.
"""
import argparse
import json
import subprocess

import numpy as np

SR = 44100


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def quiet_span(x, a, b, thresh):
    """Shrink [a, b) (samples) to its quiet core: trim edges louder than thresh (5 ms windows)."""
    w = int(0.005 * SR)
    while a + w < b and np.sqrt(np.mean(x[a:a + w] ** 2)) > thresh:
        a += w
    while b - w > a and np.sqrt(np.mean(x[b - w:b] ** 2)) > thresh:
        b -= w
    return a, b


def main():
    p = argparse.ArgumentParser()
    p.add_argument("inp"), p.add_argument("words"), p.add_argument("out")
    p.add_argument("--sentence", type=float, default=0.13)
    p.add_argument("--comma", type=float, default=0.08)
    p.add_argument("--word", type=float, default=0.05)
    a = p.parse_args()
    x = load(a.inp)
    words = json.load(open(a.words))["words"]
    rms = np.sqrt(np.mean(x ** 2))
    thresh = rms * 0.12  # well under speech level
    cuts = []
    for w0, w1 in zip(words, words[1:]):
        end = w0["text"].rstrip()[-1:]
        keep = a.sentence if end in ".?!" else a.comma if end in ",;:" else a.word
        g = w1["start"] - w0["end"]
        if g <= keep + 0.02:
            continue
        s = int((w0["end"] + keep / 2) * SR)
        e = int((w1["start"] - keep / 2) * SR)
        s, e = quiet_span(x, s, e, thresh)
        if e - s > int(0.02 * SR):
            cuts.append((s, e))
    fade = int(0.01 * SR)
    ramp = np.sin(np.linspace(0, np.pi / 2, fade)) ** 2
    out, pos, removed = [], 0, 0
    for s, e in cuts:
        seg = x[pos:s + fade].copy()
        nxt = x[e:e + fade]
        seg[-fade:] = seg[-fade:] * (1 - ramp) + nxt * ramp
        out.append(seg)
        pos = e + fade
        removed += e - s
    out.append(x[pos:])
    y = np.concatenate(out)
    lead = int(max(0, words[0]["start"] - 0.06) * SR)  # no dead air before the first word
    y = y[lead:]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "192k", a.out], input=y.tobytes(), check=True)
    print(f"{len(cuts)} gaps cut, {removed / SR + lead / SR:.2f} s removed, {len(y) / SR:.2f} s long")


if __name__ == "__main__":
    main()
