"""Finish the approved Saylo thumbnail: base image + finishing tweaks + Anton overlay, exported for YouTube.

    python saylo/tools/make_thumbnail.py <base image> <out.jpg> --text "5 YEARS" --amber "5"
        [--dim x,y,r,strength ...] [--darken x0,y0,x1,y1,amount ...]

--dim     radial darkening of bright pixels (e.g. a lamp): centre x,y, radius r (px of the base), strength 0-1
--darken  darken a box by `amount` (0.10 = 10%), sparing saturated (amber) pixels so the accent stays bright
Text: Anton, off-white, centred in the top of the frame; the words listed in --amber are drawn in the accent
colour (sampled from the brightest amber in the image unless --accent is given). Output: 1920x1080 JPEG < 2 MB
(4:4:4 colour, light sharpening; --size / --sharpen to change),
plus a 168 px-wide phone preview next to it (`*_phone.png`).
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "Anton-Regular.ttf")
OFF_WHITE = (237, 232, 221)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base"); ap.add_argument("out")
    ap.add_argument("--text", required=True)
    ap.add_argument("--amber", default="")
    ap.add_argument("--accent", default="")
    ap.add_argument("--dim", action="append", default=[])
    ap.add_argument("--darken", action="append", default=[])
    ap.add_argument("--cap", type=float, default=0.17, help="cap height as a share of the frame height")
    ap.add_argument("--top", type=float, default=0.06, help="top margin as a share of the frame height")
    ap.add_argument("--align", default="center", choices=["center", "left"], help="text position in the top of the frame")
    ap.add_argument("--left", type=float, default=0.05, help="left margin (share of width) when --align left")
    ap.add_argument("--arrow", default="", help="x0,y0,x1,y1 as shares of the frame: an off-white arrow pointing at x1,y1")
    ap.add_argument("--size", default="1920x1080", help="output size, 16:9 (YouTube allows up to 2 MB)")
    ap.add_argument("--sharpen", type=float, default=70, help="unsharp-mask strength in percent, 0 = off")
    a = ap.parse_args()

    im = Image.open(a.base).convert("RGB")
    px = np.asarray(im).astype(np.float32) / 255.0
    h, w, _ = px.shape
    yy, xx = np.mgrid[0:h, 0:w]
    lum = px.mean(axis=2)
    sat = px.max(axis=2) - px.min(axis=2)

    for spec in a.dim:                      # lamp: darken only what's bright, fading out radially
        x, y, r, s = [float(v) for v in spec.split(",")]
        d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2)
        fall = np.clip(1 - d / r, 0, 1) ** 1.5
        bright = np.clip((lum - 0.25) / 0.5, 0, 1)
        px *= (1 - s * fall * bright)[..., None]

    for spec in a.darken:                   # box darken, sparing the saturated accent
        x0, y0, x1, y1, amt = [float(v) for v in spec.split(",")]
        mask = np.zeros((h, w), np.float32)
        mask[int(y0):int(y1), int(x0):int(x1)] = 1.0
        mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(25))) / 255.0
        spare = np.clip((sat - 0.15) / 0.2, 0, 1)
        px *= (1 - amt * mask * (1 - spare))[..., None]

    if a.accent:
        accent = tuple(int(a.accent.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    else:                                   # brightest strongly saturated orange in the image
        hue_ok = (px[..., 0] > px[..., 1]) & (px[..., 1] > px[..., 2])
        score = np.where(hue_ok & (sat > 0.45), lum, 0)
        iy, ix = np.unravel_index(np.argmax(score), score.shape)
        accent = tuple(int(c * 255) for c in px[iy, ix])

    # 1920x1080 by default: YouTube re-compresses thumbnails, and a bigger, sharper upload survives it far better
    # than 1280x720 (creator: the 1280 version looked blurry once posted). Light unsharp mask after the resize.
    OW, OH = (int(v) for v in a.size.lower().split("x"))
    im = Image.fromarray((np.clip(px, 0, 1) * 255).astype(np.uint8)).resize((OW, OH), Image.LANCZOS)
    if a.sharpen > 0:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=int(a.sharpen), threshold=2))
    W, H = im.size

    # text: size the font so the cap height is `cap` of the frame
    words = a.text.split()
    amber_words = set(a.amber.split())
    size = 200
    font = ImageFont.truetype(FONT, size)
    cap_px = font.getbbox("H")[3] - font.getbbox("H")[1]
    size = int(size * (a.cap * H) / cap_px)
    font = ImageFont.truetype(FONT, size)
    space = font.getlength(" ")
    widths = [font.getlength(wd) for wd in words]
    total = sum(widths) + space * (len(words) - 1)
    x = (W - total) / 2 if a.align == "center" else a.left * W
    top_off = font.getbbox("H")[1]
    y = a.top * H - top_off

    shadow = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shadow)
    xs = x
    for wd, ww in zip(words, widths):
        sd.text((xs, y + 4 * H / 720), wd, font=font, fill=200)
        xs += ww + space
    arrow = None
    if a.arrow:                             # shaft + head polygon, drawn into the shadow mask too
        x0, y0, x1, y1 = [float(v) for v in a.arrow.split(",")]
        x0, y0, x1, y1 = x0 * W, y0 * H, x1 * W, y1 * H
        L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        nx, ny = -uy, ux
        hw, hl, sw = 0.034 * H, 0.06 * H, 0.0095 * H     # head half-width, head length, shaft half-width
        bx, by = x1 - ux * hl, y1 - uy * hl
        shaft = [(x0 + nx * sw, y0 + ny * sw), (bx + nx * sw, by + ny * sw), (bx - nx * sw, by - ny * sw), (x0 - nx * sw, y0 - ny * sw)]
        head = [(x1, y1), (bx + nx * hw, by + ny * hw), (bx - nx * hw, by - ny * hw)]
        arrow = (shaft, head)
        off = 4 * H / 720
        for poly in arrow:
            sd.polygon([(px_ + 0, py_ + off) for px_, py_ in poly], fill=200)
    shadow = shadow.filter(ImageFilter.GaussianBlur(10 * H / 720))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shadow)

    d = ImageDraw.Draw(im)
    if arrow:
        for poly in arrow:
            d.polygon(poly, fill=OFF_WHITE)
    for wd, ww in zip(words, widths):
        d.text((x, y), wd, font=font, fill=accent if wd in amber_words else OFF_WHITE)
        x += ww + space

    q = 95
    while True:
        # subsampling=0 (4:4:4): full colour resolution, so the amber "5" and the beam keep hard edges
        im.save(a.out, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0)
        if os.path.getsize(a.out) < 2_000_000 or q <= 70:
            break
        q -= 5
    im.resize((168, 95), Image.LANCZOS).save(os.path.splitext(a.out)[0] + "_phone.png")
    print("wrote", a.out, os.path.getsize(a.out), "bytes, accent", accent)


if __name__ == "__main__":
    main()
