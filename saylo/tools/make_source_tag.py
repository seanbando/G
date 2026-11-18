"""Make a Saylo source tag: a transparent 1920x1080 PNG overlay for real footage.

Usage:
  python3 saylo/tools/make_source_tag.py "WNEP" "OCT 30, 2014" [out.png]
  python3 saylo/tools/make_source_tag.py "PA SUPREME COURT" "2019 OPINION"

Drop the PNG on the track above the clip, full frame. Style: bottom-left, small dark
pill, amber dot, typewriter font — matches the timestamp cards. Keep it on screen for
the whole clip.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
AMBER = (255, 150, 40, 255)
TEXT = (235, 235, 230, 255)
DIM = (170, 170, 165, 255)
BG = (10, 10, 10, 170)
MONO = ["/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]


def font(size):
    for f in MONO:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def make(source, detail="", out=None):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f1, f2 = font(26), font(22)
    label = f"SOURCE: {source.upper()}"
    sub = detail.upper()
    w1 = d.textlength(label, font=f1)
    w2 = d.textlength("  ·  " + sub, font=f2) if sub else 0
    pad, dot = 18, 12
    bw = int(pad + dot + 14 + w1 + w2 + pad)
    bh = 50
    x, y = 60, H - 60 - bh          # inside title-safe area, bottom-left
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=10, fill=BG)
    cy = y + bh // 2
    d.ellipse([x + pad, cy - dot // 2, x + pad + dot, cy + dot // 2], fill=AMBER)
    tx = x + pad + dot + 14
    d.text((tx, cy), label, font=f1, fill=TEXT, anchor="lm")
    if sub:
        d.text((tx + w1, cy + 1), "  ·  " + sub, font=f2, fill=DIM, anchor="lm")
    out = out or f"source-{source.lower().replace(' ', '-').replace('.', '')}.png"
    img.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(make(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "", sys.argv[3] if len(sys.argv) > 3 else None))
