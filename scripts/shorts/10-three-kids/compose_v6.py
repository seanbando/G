"""Compose three-friends v6: 3D film frames + 3D chart/stacks windows + frame-1 slam card.

Usage: python3 compose_v6.py <film_dir> <chart_dir> <stacks_dir> <out.mp4>
Chart and stacks windows get a slow push-in so they never sit still.
"""
import json
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS, W, H = 30, 1080, 1920
HERE = __file__.rsplit("/", 1)[0] or "."
lines = {l["id"]: l for l in json.load(open(f"{HERE}/words.json"))["lines"]}
CHART = (lines["VO-03"]["start"] - 0.05, lines["VO-04"]["start"] - 0.05)
STACKS = (lines["VO-08"]["start"] - 0.1, lines["VO-09"]["start"] - 0.05)
SLAM = 0.5  # seconds the finished slam card holds before the film hook starts
FONT = "/usr/share/fonts/opentype/inter/Inter-Black.otf"


def font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", size)


def push(im, u, z0=1.0, z1=1.09, aim=(0.5, 0.45)):
    z = z0 + (z1 - z0) * u
    cw, ch = W / z, H / z
    x = min(max(aim[0] * W - cw / 2, 0), W - cw)
    y = min(max(aim[1] * H - ch / 2, 0), H - ch)
    return im.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.LANCZOS)


def slam(bg):
    im = bg.filter(ImageFilter.GaussianBlur(18))
    im = Image.blend(im, Image.new("RGB", (W, H), (8, 10, 24)), 0.55)
    d = ImageDraw.Draw(im)
    rows = [("SAME $1,000", (255, 255, 255), 150), ("SAME S&P 500", (255, 255, 255), 118),
            ("10X", (60, 230, 120), 420), ("DIFFERENT", (60, 230, 120), 150)]
    y = 360
    for text, col, size in rows:
        f = font(size)
        bw = d.textbbox((0, 0), text, font=f)
        x = (W - (bw[2] - bw[0])) / 2 - bw[0]
        d.text((x + 8, y + 10 - bw[1]), text, font=f, fill=(0, 0, 0))
        d.text((x, y - bw[1]), text, font=f, fill=col)
        y += (bw[3] - bw[1]) + 60
    return im


def frame_from(dirname, i):
    return Image.open(f"{dirname}/f{i:04d}.jpg").convert("RGB").resize((W, H))


def main(film, chart, stacks, out):
    import os
    n = len([f for f in os.listdir(film) if f.endswith(".jpg")])
    nc = len(os.listdir(chart))
    ns = len(os.listdir(stacks))
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "audio/three-friends-v4-FULL.mp3",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-c:a", "aac", "-b:a", "192k",
                            "-shortest", out], stdin=subprocess.PIPE, cwd=os.path.abspath(f"{HERE}/../../.."))
    card = slam(frame_from(film, int(SLAM * FPS)))
    for i in range(n):
        t = i / FPS
        if t < SLAM:
            im = card
        elif CHART[0] <= t < CHART[1]:
            k = min(int((t - CHART[0]) * FPS), nc - 1)
            im = push(frame_from(chart, k), (t - CHART[0]) / (CHART[1] - CHART[0]))
        elif STACKS[0] <= t < STACKS[1]:
            k = min(int((t - STACKS[0]) * FPS), ns - 1)
            im = push(frame_from(stacks, k), (t - STACKS[0]) / (STACKS[1] - STACKS[0]), 1.0, 1.08, (0.5, 0.5))
        else:
            im = frame_from(film, i)
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    enc.wait()
    print("wrote", out, n, "frames")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    import os
    main(*[os.path.abspath(a) for a in sys.argv[1:5]])
