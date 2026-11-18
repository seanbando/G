"""Make a Saylo source caption: transparent 1920x1080 PNG, small text bottom-right.

Matches the house style from the editing style pack: JetBrains Mono Medium 22px,
off-white (232,230,225) at ~67% opacity, no box, 70px from the right edge and
60px from the bottom. Put it on the track above the clip for the whole clip.

Content: the source name only, e.g. "WNEP" or "FBI". Creative Commons: "Author · CC BY-SA 4.0".
  "WNEP"
  "SounderBruce · CC BY-SA 4.0"

Usage:
  python3 saylo/tools/make_source_tag.py "WNEP" [out.png]
"""
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONTS = ["/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
FILL = (232, 230, 225, 170)


def make(text, out=None):
    font = next((ImageFont.truetype(f, 22) for f in FONTS if os.path.exists(f)), ImageFont.load_default())
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    b = d.textbbox((0, 0), text, font=font)
    d.text((W - 70 - (b[2] - b[0]) - b[0], H - 60 - (b[3] - b[1]) - b[1]), text, font=font, fill=FILL)
    out = out or "caption-" + re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] + ".png"
    img.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(make(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
