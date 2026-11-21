"""Screenshot game: a stock card flashes fast on top, YOU reacts below. ~7.2 s seamless loop, no voice.

Usage: python3 build_screenshot.py <out.mp4>
"""
import math
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SECS = 7.2
STEP = 6  # frames per card (0.2 s -> 5 cards a second)
HERE = __file__.rsplit("/", 1)[0] or "."
ROOT = HERE + "/../../.."
INTER = "/usr/share/fonts/opentype/inter/"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# $1,000 at the 12/31/2020 close -> 12/31/2025 close, dividends reinvested (see fact-check.md)
STOCKS = [
    ("NVDA", "Nvidia", 14313, "🤑"), ("PLTR", "Palantir", 7549, "🚀"), ("XOM", "Exxon Mobil", 3573, "🛢️"),
    ("JPM", "JPMorgan Chase", 2888, "🏦"), ("META", "Meta", 2433, "📱"), ("AMD", "AMD", 2335, "💻"),
    ("GLD", "Gold ETF", 2222, "🪙"), ("QQQ", "Nasdaq-100 ETF", 2018, "📈"), ("SPY", "S&P 500 ETF", 1954, "📊"),
    ("TSLA", "Tesla", 1912, "🚗"), ("NFLX", "Netflix", 1734, "🍿"), ("KO", "Coca-Cola", 1482, "🥤"),
    ("PFE", "Pfizer", 863, "💀"), ("DIS", "Disney", 643, "😭"), ("SPCX", "SpaceX", 1017, "🛰️"),
]


def font(name, size):
    return ImageFont.truetype(INTER + name, size)


def emoji(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)


def centered(d, y, text, f, fill, stroke=0, sfill=None):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)


def top_bg():
    im = Image.new("RGB", (W, 960), (238, 240, 244))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, 960)], fill=(226, 229, 235), width=2)
    for y in range(0, 960, 60):
        d.line([(0, y), (W, y)], fill=(226, 229, 235), width=2)
    rnd = random.Random(3)
    for k in range(3):  # faint chart lines behind the card
        pts, y = [], 700 - k * 120
        for x in range(0, W + 40, 40):
            y += rnd.uniform(-38, 30)
            pts.append((x, y))
        d.line(pts, fill=(205, 215, 228), width=6)
    return im


def card(s):
    tick, name, val, emo = s
    up = val >= 1000
    col = (22, 163, 74) if up else (220, 38, 38)
    cw, ch = 900, 600
    im = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 30, cw + 20, ch + 30], 48, fill=(0, 0, 0, 70))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    border = (234, 179, 8) if tick == "NVDA" else col
    d.rounded_rectangle([20, 20, cw + 20, ch + 20], 48, fill=(255, 255, 255), outline=border, width=14 if tick == "NVDA" else 8)
    ft = font("Inter-Black.otf" if False else "Inter-ExtraBold.otf", 170)
    d.text((70, 50), tick, font=ft, fill=(17, 24, 39))
    d.text((76, 240), name, font=font("Inter-SemiBold.otf", 50), fill=(100, 110, 125))
    e = emoji(emo, 150)
    im.alpha_composite(e, (cw - 150, 70))
    label = "$1,000 at June IPO →" if tick == "SPCX" else "$1,000 in 2021 →"
    d.text((76, 330), label, font=font("Inter-SemiBold.otf", 52), fill=(55, 65, 81))
    vtxt = ("≈ " if tick == "SPCX" else "") + f"${val:,}"
    d.text((70, 395), vtxt, font=font("Inter-ExtraBold.otf", 150), fill=col)
    chip = "JACKPOT" if tick == "NVDA" else ("LOST MONEY" if not up else ("FLAT" if tick == "SPCX" else None))
    if chip:
        fc = font("Inter-ExtraBold.otf", 40)
        tw = d.textlength(chip, font=fc)
        x0, y0 = cw + 20 - tw - 90, 290
        d.rounded_rectangle([x0, y0, x0 + tw + 50, y0 + 66], 33, fill=(234, 179, 8) if tick == "NVDA" else ((107, 114, 128) if tick == "SPCX" else col))
        d.text((x0 + 25, y0 + 9), chip, font=fc, fill=(255, 255, 255))
    return im


def you_nervous():
    y = Image.open(HERE + "/../10-three-kids/3d/sprites/you.png").convert("RGBA").crop((0, 0, 560, 731))
    d = ImageDraw.Draw(y)
    skin = (252, 208, 168, 255)
    d.ellipse([245, 372, 355, 425], fill=skin)  # remove the calm smile
    # tight cringe grin with teeth
    d.chord([240, 360, 360, 440], 0, 180, fill=(255, 255, 255, 255), outline=(30, 30, 30, 255), width=5)
    for x in range(262, 345, 16):
        d.line([(x, 400), (x, 432)], fill=(60, 60, 60, 255), width=3)
    d.line([(244, 400), (356, 400)], fill=(30, 30, 30, 255), width=5)
    # worried eyebrows (tilted up in the middle)
    d.polygon([(190, 238), (275, 212), (280, 228), (194, 252)], fill=(25, 25, 25, 255))
    d.polygon([(325, 212), (410, 238), (406, 252), (320, 228)], fill=(25, 25, 25, 255))
    return y


def sweat(size):
    im = Image.new("RGBA", (size, int(size * 1.5)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, size * 0.5, size, size * 1.5], fill=(120, 190, 255, 255), outline=(40, 90, 160, 255), width=4)
    d.polygon([(size * 0.5, 0), (size * 0.08, size * 0.85), (size * 0.92, size * 0.85)], fill=(120, 190, 255, 255))
    d.ellipse([size * 0.25, size * 0.8, size * 0.45, size * 1.05], fill=(235, 248, 255, 255))
    return im


def bottom_bg():
    im = Image.new("RGB", (W, 960))
    a = np.linspace(0, 1, 960)[:, None]
    top = np.array([62, 48, 92]); bot = np.array([24, 18, 40])
    arr = (top * (1 - a) + bot * a)[:, None, :].repeat(W, 1).astype("uint8")
    im = Image.fromarray(arr)
    g = Image.new("L", (W, 960), 0)
    ImageDraw.Draw(g).ellipse([140, 120, 940, 960], fill=110)
    im.paste((255, 200, 140), (0, 0), g.filter(ImageFilter.GaussianBlur(120)))
    return im


def main(out):
    rnd = random.Random(7)
    n = int(SECS * FPS)
    order = []
    while len(order) < n // STEP:
        batch = STOCKS[:]
        rnd.shuffle(batch)
        if order and batch[0][0] == order[-1][0]:
            batch.append(batch.pop(0))
        order += batch
    order = order[: n // STEP]
    if order[-1][0] == order[0][0]:
        order[-1], order[-2] = order[-2], order[-1]
    cards = {s[0]: card(s) for s in STOCKS}
    tb, bb = top_bg(), bottom_bg()
    you = you_nervous()
    scale = 1.55
    you = you.resize((int(you.width * scale), int(you.height * scale)), Image.LANCZOS)
    drop = sweat(46)
    ftxt = font("Inter-ExtraBold.otf", 64)
    fsmall = font("Inter-Medium.otf", 30)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out + ".v.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        ph = 2 * math.pi * t / SECS  # one full cycle per loop -> seamless
        frame = Image.new("RGB", (W, H))
        frame.paste(tb, (0, 0))
        k = i % STEP
        c = cards[order[i // STEP][0]]
        pop = 1.0 + 0.06 * max(0, 1 - k / 2)  # tiny pop when a new card lands
        cc = c.resize((int(c.width * pop), int(c.height * pop)), Image.BILINEAR)
        frame.paste(cc, ((W - cc.width) // 2, 215 - (cc.height - c.height) // 2), cc)
        d = ImageDraw.Draw(frame)
        centered(d, 870, "Historical: end of 2020 to end of 2025, dividends reinvested.", fsmall, (110, 118, 130))
        centered(d, 908, "SpaceX since its June 2026 IPO. Not financial advice.", fsmall, (110, 118, 130))
        frame.paste(bb, (0, 960))
        bob = 10 * math.sin(ph * 3)
        sway = 6 * math.sin(ph * 2)
        frame.paste(you, (int((W - you.width) / 2 + sway), int(1960 - you.height + 190 + bob)), you)
        dy = int((t * 140) % 140)  # sweat drop slides and repeats
        cx = int((W - you.width) / 2 + sway + 455 * scale)
        frame.paste(drop, (cx, int(1960 - you.height + 190 + bob + 240 * scale + dy)), drop)
        d = ImageDraw.Draw(frame)
        for j, ln in enumerate(["The stock you screenshot", "is what your $1,000", "turned into"]):
            centered(d, 975 + j * 80, ln, ftxt, (255, 255, 255), 7, (0, 0, 0))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    # ticks: one click per card change, plus a soft low hum bed
    sr = 44100
    a = np.zeros(int(SECS * sr), np.float32)
    clk = (np.sin(2 * np.pi * 1800 * np.arange(int(0.025 * sr)) / sr) * np.exp(-np.arange(int(0.025 * sr)) / (0.004 * sr))).astype(np.float32)
    for j in range(len(order)):
        s = int(j * STEP / FPS * sr)
        a[s:s + len(clk)] += 0.5 * clk[: len(a) - s]
    tt = np.arange(len(a)) / sr
    a += 0.06 * np.sin(2 * np.pi * 55 * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / SECS))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".v.mp4", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out], input=a.tobytes(), check=True)
    subprocess.run(["rm", "-f", out + ".v.mp4"])
    print("wrote", out, len(order), "cards")


if __name__ == "__main__":
    main(sys.argv[1])
