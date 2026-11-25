"""Tighten the pauses between lines of a recorded narration, without touching the voice.

Usage: python3 tools/tighten_track.py <in-dir> <out-dir> [--same 0.22] [--change 0.30] [--first S001 --last S011]

<in-dir> holds narration.mp3 and timings.json (from tools/record_natural.py). Between each
pair of lines, and at long pauses inside a sentence, the tool finds the real silence, and if it is longer than the target it cuts
the middle out (tiny fades, so no click). Speech is never cut or sped up. Planned pauses
(the quiz pause) are left alone. Writes narration.mp3 and a re-timed timings.json to <out-dir>.

  --same    pause to leave between two lines by the same voice (seconds)
  --change  pause to leave when the voice changes (Buck or Hamlet cutting in)
  --first/--last  only tighten this range of lines (default: the whole track)
"""
import argparse
import json
import os
import subprocess

import numpy as np

SR = 44100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--same", type=float, default=0.22)
    ap.add_argument("--change", type=float, default=0.30)
    ap.add_argument("--inner", type=float, default=0.26, help="pause to leave at a long mid-sentence pause (only pauses over --inner-min are touched)")
    ap.add_argument("--inner-min", type=float, default=0.42)
    ap.add_argument("--first"); ap.add_argument("--last")
    a = ap.parse_args()
    T = json.load(open(os.path.join(a.src, "timings.json")))
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", os.path.join(a.src, "narration.mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    x = np.frombuffer(pcm, dtype=np.float32).copy()
    win = int(0.005 * SR)
    n = len(x) // win
    db = 20 * np.log10(np.abs(x[:n * win]).reshape(n, win).max(axis=1) + 1e-9)
    quiet = db < -42
    L = T["lines"]
    ids = [l["id"] for l in L]
    lo = ids.index(a.first) if a.first else 0
    hi = ids.index(a.last) if a.last else len(L) - 1
    cuts = []  # (start_sample, end_sample, from, to, pause) to remove

    def consider(t_end, t_start, target, a_name, b_name, margin=0.15):
        w0, w1 = max(0, int((t_end - margin) / 0.005)), min(n, int((t_start + margin) / 0.005))
        best, cur = None, None  # longest quiet run between the two points
        for k in range(w0, w1):
            if quiet[k]:
                cur = (cur[0], k + 1) if cur else (k, k + 1)
                if not best or cur[1] - cur[0] > best[1] - best[0]:
                    best = cur
            else:
                cur = None
        if not best:
            return
        run = (best[1] - best[0]) * 0.005
        if run > target + 0.04:
            keep = target * SR
            cuts.append((int(best[0] * win + keep / 2), int(best[1] * win - keep / 2), a_name, b_name, run))

    for i in range(lo, hi + 1):
        p = L[i]
        ws = p["words"]
        for u, v in zip(ws, ws[1:]):  # long pauses inside the sentence (commas)
            if v["start"] - u["end"] > a.inner_min:
                consider(u["end"], v["start"], a.inner, f'{p["id"]} "{u["word"]}"', f'"{v["word"]}"', margin=0.05)
        if i + 1 < len(L):
            q = L[i + 1]
            if any(pa["start"] < q["start"] + 0.2 and pa["end"] > p["end"] - 0.2 for pa in T.get("pauses", [])):
                continue  # a planned pause lives here
            consider(p["end"], q["start"], a.same if p["voice"] == q["voice"] else a.change, p["id"], q["id"])
    cuts.sort()
    out, pos, fade = [], 0, int(0.008 * SR)
    for s, e, *_ in cuts:
        seg = x[pos:s].copy(); seg[-fade:] *= np.linspace(1, 0, fade); out.append(seg)
        x[e:e + fade] *= np.linspace(0, 1, fade)
        pos = e
    out.append(x[pos:])
    y = np.concatenate(out)

    def shift(t):
        return round(t - sum((min(e, int(t * SR)) - s) for s, e, *_ in cuts if int(t * SR) > s) / SR, 3)
    for l in L:
        l["start"], l["end"] = shift(l["start"]), shift(l["end"])
        for w in l["words"]:
            w["start"], w["end"] = shift(w["start"]), shift(w["end"])
    for pa in T.get("pauses", []):
        pa["start"], pa["end"] = shift(pa["start"]), shift(pa["end"])
    os.makedirs(a.dst, exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "libmp3lame", "-b:a", "160k",
                    os.path.join(a.dst, "narration.mp3")], input=y.tobytes(), check=True)
    T["duration"] = round(len(y) / SR, 3)
    json.dump(T, open(os.path.join(a.dst, "timings.json"), "w"), indent=1)
    saved = (len(x) - len(y)) / SR
    print(f"tightened {len(cuts)} pauses, saved {saved:.1f} s ({len(x) / SR:.1f} s -> {len(y) / SR:.1f} s)")
    for s, e, p, q, run in cuts[:40]:
        print(f"  {p} -> {q}: pause {run:.2f} s -> {run - (e - s) / SR:.2f} s")


if __name__ == "__main__":
    main()
