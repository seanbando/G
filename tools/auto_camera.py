"""Write continuous camera cues so a short never sits still (reference-short style).

Usage:
    python3 tools/auto_camera.py <video.mp4> <captions.srt> [--start 0.6] [--max-zoom 1.6] [--calm 7.3-14.9,31.5-39.7] > camera.txt

Splits the video into shots at every caption phrase start (about every 0.8-1.5 s), so each
phrase gets a new framing: it cycles wide -> medium -> close (about 1.0 / 1.3 / 1.55x),
aimed at the content of that moment (centre of the non-background pixels, so nothing
important is cropped), and every shot keeps moving: a slow push-in or pull-back of
about 6-8%. --calm gives time ranges (3D scenes, number reveals) that stay
at full frame, still drifting, so nothing important is cropped. Output is `cam` cues for tools/edit_short.py; add transitions/punches after.
"""
import re
import subprocess
import sys

import numpy as np


def srt_starts(path):
    out = []
    for block in re.split(r"\n\s*\n", open(path).read().strip()):
        rows = block.splitlines()
        if len(rows) >= 2 and "-->" in rows[1]:
            h, m, rest = rows[1].split("-->")[0].strip().split(":")
            sec, ms = rest.split(",")
            out.append(int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000)
    return out


def frame(path, t, w=270, h=480):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(int) if len(raw) == w * h * 3 else None


def content_box(img):
    """Centre and size of everything that isn't background (ignores the caption band)."""
    h, w, _ = img.shape
    body = img[: int(h * 0.80)]
    bg = np.median(body.reshape(-1, 3), axis=0)
    mask = np.abs(body - bg).sum(2) > 60
    ys, xs = np.nonzero(mask)
    if len(xs) < 50:
        return 0.5, 0.45, 1.0, 1.0
    x0, x1 = np.percentile(xs, [1, 99]) / w
    y0, y1 = np.percentile(ys, [1, 99]) / h
    return (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, 0.2), max(y1 - y0, 0.2)


def main(video, srt, start=0.6, max_zoom=1.6, calm=""):
    calm_ranges = [tuple(float(x) for x in r.split("-")) for r in calm.split(",") if r]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True).stdout)
    cuts = [t for t in srt_starts(srt) if t >= start] + [dur]
    cuts = [start] + [t for t in cuts if t - start > 0.4]
    levels = [1.0, 1.3, 1.55]
    print("# auto camera: new framing on every caption phrase, always moving")
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        img = frame(video, (a + b) / 2)
        cx, cy, bw, bh = content_box(img) if img is not None else (0.5, 0.45, 1, 1)
        fit = min(1 / bw, 1 / bh) * 0.92  # zoom that still shows all the content
        z = max(1.0, min(levels[i % 3], fit, max_zoom))
        if any(a < ce and b > cs for cs, ce in calm_ranges):  # data reveals / 3D: keep it all in frame
            z = 1.0
        push_in = i % 2 == 0
        z0, z1 = (z, z * 1.07) if push_in else (z * 1.07, z)
        print(f"{a:.2f} cam {b:.2f} {z0:.3f} {z1:.3f} {cx:.3f} {cy:.3f}")


if __name__ == "__main__":
    argv = sys.argv[1:]
    opts = {"--start": 0.6, "--max-zoom": 1.6}
    calm = ""
    if "--calm" in argv:
        j = argv.index("--calm")
        calm = argv[j + 1]
        del argv[j:j + 2]
    for k in list(opts):
        if k in argv:
            j = argv.index(k)
            opts[k] = float(argv[j + 1])
            del argv[j:j + 2]
    if len(argv) != 2:
        sys.exit(__doc__)
    main(*argv, start=opts["--start"], max_zoom=opts["--max-zoom"], calm=calm)
