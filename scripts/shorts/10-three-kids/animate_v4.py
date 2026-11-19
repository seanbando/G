"""Flat vector animation for "Same $1,000, Same S&P 500, 3 Different Endings" (three friends).

Usage: python3 scripts/shorts/10-three-kids/animate.py <out.mp4>
Draws every frame with Pillow (dark navy style, like the broke/rocket short), timed to
words.json (v2 voiceover), and muxes audio/three-kids-FULL-v2.mp3. Captions are burned
separately afterwards (tools/burn_captions.py).
"""
import json
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W, H, FPS = 1080, 1920, 30
AUDIO = os.path.join(ROOT, "audio", "three-friends-v4-FULL.mp3")
CHART3D = os.environ.get("CHART3D")  # 3D chart frames for VO-03
STACKS3D = os.environ.get("STACKS3D")  # 3D coin stacks frames for VO-08
WORDS = json.load(open(os.path.join(HERE, "words.json")))
F_BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
F_BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"

BG = (17, 22, 48)
WHITE = (245, 245, 250)
RED = (235, 72, 82)
YEL = (250, 204, 64)
GRN = (64, 196, 110)
GOLD = (255, 196, 60)
GREY = (150, 160, 190)
SKIN_L, SKIN_D = (247, 206, 170), (150, 98, 66)

_fonts = {}


def font(size, black=False):
    size = max(1, int(size))
    k = (size, black)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(F_BLACK if black else F_BOLD, size)
    return _fonts[k]


def word_time(line, text, nth=0):
    hits = [w["start"] for w in WORDS["words"] if w["line"] == line and w["text"].lower().strip(".,?!") == text.lower()]
    return hits[nth]


LINES = {l["id"]: (l["start"], l["end"]) for l in WORDS["lines"]}
END = WORDS["lines"][-1]["end"] + 0.35

# key moments
T_ONE = word_time("VO-01", "one")
T_TEN = word_time("VO-01", "ten")
T_SHOE = word_time("VO-04", "shoebox")
T_26 = word_time("VO-05", "twenty-six")
T_2009 = word_time("VO-05", "later")
T_MISTAKE = word_time("VO-09", "shoebox")
T_MAYA_COST = word_time("VO-09", "maya")
T_JAY9 = word_time("VO-08", "jay")
T_MAYA9 = word_time("VO-08", "maya")
T_SAM9 = word_time("VO-08", "sam")

random.seed(7)
STARS = [(random.randint(0, W), random.randint(0, H), random.choice([2, 2, 3])) for _ in range(140)]


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def pop(t, t0, d=0.25):
    """0 before t0, overshoot pop to 1."""
    u = (t - t0) / d
    if u <= 0:
        return 0.0
    if u >= 1:
        return 1.0
    return 1.0 + 0.18 * math.sin(u * math.pi) * (1 - u) if u > 0.6 else ease(u / 0.6) * 1.12


def base():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for x, y, r in STARS:
        d.ellipse((x - r, y - r, x + r, y + r), fill=(70, 80, 120))
    return im


def text(d, xy, s, size, fill=WHITE, anchor="mm", black=True, stroke=0, stroke_fill=(10, 12, 30)):
    d.text(xy, s, font=font(size, black), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)


def label(d, cx, cy, s, size, bg, fg=(15, 15, 25), pad=18, radius=16):
    f = font(size, True)
    w = d.textlength(s, font=f)
    d.rounded_rectangle((cx - w / 2 - pad, cy - size * 0.62 - pad / 2, cx + w / 2 + pad, cy + size * 0.62 + pad / 2), radius, fill=bg)
    d.text((cx, cy), s, font=f, fill=fg, anchor="mm")


# ---------- characters ----------
def person(d, cx, by, s, who, mood="neutral", arms="down"):
    """Flat person standing with feet at (cx, by), scale s (1 = ~520 px tall)."""
    shirt = {"jay": RED, "maya": YEL, "sam": GRN}[who]
    skin = SKIN_D if who == "maya" else SKIN_L
    pants = {"jay": (60, 100, 190), "maya": (70, 110, 200), "sam": (196, 170, 120)}[who]
    u = s
    # legs
    if who == "sam":
        d.rounded_rectangle((cx - 60 * u, by - 230 * u, cx + 60 * u, by - 150 * u), int(14 * u), fill=pants)
        for sx in (-1, 1):
            d.rectangle((cx + sx * 32 * u - 18 * u, by - 150 * u, cx + sx * 32 * u + 18 * u, by - 30 * u), fill=skin)
    else:
        for sx in (-1, 1):
            d.rounded_rectangle((cx + sx * 32 * u - 26 * u, by - 230 * u, cx + sx * 32 * u + 26 * u, by - 30 * u), int(12 * u), fill=pants)
    shoe = (110, 115, 125) if who == "sam" else (240, 240, 240)
    for sx in (-1, 1):
        d.rounded_rectangle((cx + sx * 34 * u - 34 * u, by - 34 * u, cx + sx * 34 * u + 34 * u, by), int(12 * u), fill=shoe)
    # torso
    d.rounded_rectangle((cx - 85 * u, by - 420 * u, cx + 85 * u, by - 210 * u), int(40 * u), fill=shirt)
    if who == "maya":  # overalls bib + straps
        d.rounded_rectangle((cx - 60 * u, by - 340 * u, cx + 60 * u, by - 215 * u), int(14 * u), fill=pants)
        for sx in (-1, 1):
            d.line((cx + sx * 50 * u, by - 340 * u, cx + sx * 66 * u, by - 412 * u), fill=pants, width=int(16 * u))
    if who == "jay":  # hoodie pocket + strings
        d.rounded_rectangle((cx - 55 * u, by - 300 * u, cx + 55 * u, by - 240 * u), int(14 * u), fill=tuple(int(c * 0.82) for c in RED))
        for sx in (-1, 1):
            d.line((cx + sx * 18 * u, by - 410 * u, cx + sx * 18 * u, by - 360 * u), fill=WHITE, width=int(5 * u))
    # arms
    for sx in (-1, 1):
        if arms == "up":
            d.line((cx + sx * 80 * u, by - 395 * u, cx + sx * 140 * u, by - 520 * u), fill=shirt, width=int(36 * u))
            d.ellipse((cx + sx * 140 * u - 22 * u, by - 545 * u, cx + sx * 140 * u + 22 * u, by - 500 * u), fill=skin)
        elif arms == "hold":
            d.line((cx + sx * 80 * u, by - 395 * u, cx + sx * 50 * u, by - 300 * u), fill=shirt, width=int(36 * u))
            d.ellipse((cx + sx * 50 * u - 22 * u, by - 322 * u, cx + sx * 50 * u + 22 * u, by - 278 * u), fill=skin)
        else:
            d.line((cx + sx * 88 * u, by - 395 * u, cx + sx * 100 * u, by - 250 * u), fill=shirt, width=int(36 * u))
            d.ellipse((cx + sx * 100 * u - 22 * u, by - 262 * u, cx + sx * 100 * u + 22 * u, by - 218 * u), fill=skin)
    if who == "maya":  # wristwatch on her left (viewer's right)
        wx, wy = (cx + 100 * u, by - 268 * u) if arms == "down" else (cx + 50 * u, by - 330 * u)
        d.rounded_rectangle((wx - 16 * u, wy - 10 * u, wx + 16 * u, wy + 10 * u), int(4 * u), fill=(20, 20, 20))
    # neck + head
    d.rectangle((cx - 22 * u, by - 450 * u, cx + 22 * u, by - 410 * u), fill=skin)
    hx, hy, r = cx, by - 520 * u, 78 * u
    # hair behind
    if who == "maya":
        for ox, oy, rr in [(-40, -95, 48), (0, -118, 54), (40, -95, 48), (-62, -55, 38), (62, -55, 38)]:
            d.ellipse((hx + ox * u - rr * u, hy + oy * u - rr * u, hx + ox * u + rr * u, hy + oy * u + rr * u), fill=(25, 22, 26))
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=skin)
    if who == "jay":
        pts = []
        for i in range(9):
            a = math.pi + i * math.pi / 8
            rr = r * (1.25 if i % 2 else 1.02)
            pts.append((hx + math.cos(a) * rr, hy + math.sin(a) * rr - 10 * u))
        d.polygon(pts, fill=(232, 70, 40))
        d.rectangle((hx - r, hy - r * 0.55, hx + r, hy - r * 0.35), fill=(232, 70, 40))
        for fx, fy in [(-30, 12), (-20, 22), (24, 14), (34, 22)]:  # freckles
            d.ellipse((hx + fx * u - 3 * u, hy + fy * u - 3 * u, hx + fx * u + 3 * u, hy + fy * u + 3 * u), fill=(200, 120, 90))
    elif who == "sam":
        d.chord((hx - r * 1.03, hy - r * 1.08, hx + r * 1.03, hy + r * 0.7), 180, 360, fill=(120, 76, 40))
        d.chord((hx - r * 1.03, hy - r * 1.0, hx + r * 1.03, hy + r * 0.25), 180, 360, fill=(120, 76, 40))
        d.chord((hx - r * 0.8, hy + r * 0.2, hx + r * 0.8, hy + r * 1.05), 0, 180, fill=(120, 76, 40))  # light beard
    else:
        d.chord((hx - r, hy - r * 1.05, hx + r, hy + r * 0.2), 180, 360, fill=(25, 22, 26))
    # face
    ey = hy - 5 * u
    for sx in (-1, 1):
        d.ellipse((hx + sx * 28 * u - 7 * u, ey - 7 * u, hx + sx * 28 * u + 7 * u, ey + 7 * u), fill=(20, 20, 25))
        if who == "sam":
            d.ellipse((hx + sx * 28 * u - 22 * u, ey - 22 * u, hx + sx * 28 * u + 22 * u, ey + 22 * u), outline=(30, 30, 30), width=int(5 * u))
    if who == "sam":
        d.line((hx - 6 * u, ey, hx + 6 * u, ey), fill=(30, 30, 30), width=int(5 * u))
    my = hy + 32 * u
    if mood == "happy":
        d.arc((hx - 26 * u, my - 22 * u, hx + 26 * u, my + 12 * u), 20, 160, fill=(40, 25, 25), width=int(6 * u))
    elif mood == "worried":
        d.arc((hx - 22 * u, my, hx + 22 * u, my + 26 * u), 200, 340, fill=(40, 25, 25), width=int(6 * u))
        for sx in (-1, 1):
            d.line((hx + sx * 14 * u, ey - 22 * u, hx + sx * 40 * u, ey - 30 * u), fill=(40, 25, 25), width=int(5 * u))
    elif mood == "smug":
        d.arc((hx - 26 * u, my - 18 * u, hx + 10 * u, my + 10 * u), 20, 150, fill=(40, 25, 25), width=int(6 * u))
    else:
        d.line((hx - 18 * u, my + 6 * u, hx + 18 * u, my + 6 * u), fill=(40, 25, 25), width=int(6 * u))
    if mood == "worried":  # sweat drop
        d.ellipse((hx + 70 * u, hy - 40 * u, hx + 86 * u, hy - 16 * u), fill=(120, 190, 255))


def envelope(d, cx, cy, s, txt="$1,000", color=WHITE):
    w, h = 210 * s, 130 * s
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(14 * s), fill=color)
    d.line((cx - w / 2, cy - h / 2, cx, cy, cx + w / 2, cy - h / 2), fill=(180, 180, 195), width=int(5 * s))
    text(d, (cx, cy + 22 * s), txt, int(46 * s), fill=(20, 110, 60))


def stack(d, cx, by, height, color, w=170):
    n = max(1, int(height // 26))
    for i in range(n):
        y = by - i * 26
        d.rounded_rectangle((cx - w / 2, y - 24, cx + w / 2, y), 6, fill=color, outline=tuple(int(c * 0.7) for c in color), width=3)


def shoebox(d, cx, by, s=1.0, lid_open=0.0):
    w, h = 260 * s, 130 * s
    d.rounded_rectangle((cx - w / 2, by - h, cx + w / 2, by), int(10 * s), fill=(176, 120, 70), outline=(110, 70, 40), width=int(5 * s))
    text(d, (cx, by - h / 2), "SHOEBOX", int(34 * s), fill=(90, 55, 30))
    ly = by - h - 18 * s - lid_open * 120 * s
    d.rounded_rectangle((cx - w / 2 - 12 * s, ly, cx + w / 2 + 12 * s, ly + 30 * s), int(8 * s), fill=(150, 98, 55), outline=(110, 70, 40), width=int(4 * s))


def basket(d, cx, cy, fill_frac, s=1.0):
    w, h = 620 * s, 360 * s
    top = cy - h / 2
    d.rounded_rectangle((cx - w / 2, top, cx + w / 2, cy + h / 2), int(40 * s), fill=(40, 52, 98), outline=(110, 130, 200), width=int(8 * s))
    cols, rows = 20, 10
    n = int(cols * rows * fill_frac)
    cw, ch = (w - 60 * s) / cols, (h - 120 * s) / rows
    for i in range(n):
        r, c = divmod(i, cols)
        x0 = cx - w / 2 + 30 * s + c * cw
        y0 = cy + h / 2 - 30 * s - (r + 1) * ch
        d.rectangle((x0 + 3, y0 + 3, x0 + cw - 3, y0 + ch - 3), fill=[RED, YEL, GRN, (110, 170, 255), (240, 140, 230)][(r * 7 + c * 3) % 5])
    label(d, cx, top - 10 * s, "S&P 500", int(70 * s), (240, 240, 245))


def chart(d, box, pts, upto, colors, crash_label=None, shake=0.0):
    x0, y0, x1, y1 = box
    ox = shake * math.sin(upto * 90) * 14
    d.line((x0 + ox, y1, x1 + ox, y1), fill=GREY, width=5)
    d.line((x0 + ox, y0, x0 + ox, y1), fill=GREY, width=5)
    for k, col in enumerate(colors):
        series = pts[k] if isinstance(pts[0], list) else pts
        m = max(2, int(len(series) * min(upto, 1.0)))
        xy = [(x0 + ox + (x1 - x0) * i / (len(series) - 1), y1 - (y1 - y0) * v) for i, v in enumerate(series[:m])]
        d.line(xy, fill=col, width=12 - k * 2, joint="curve")
    if crash_label:
        cx, s = crash_label
        label(d, x0 + (x1 - x0) * cx + ox, y0 - 10, s, 54, RED, WHITE)


# ---------- scenes ----------
def friends_row(d, t, by, s, moods=("neutral",) * 3, arms=("hold",) * 3, t0=0.0, gap=330):
    for i, who in enumerate(("jay", "maya", "sam")):
        k = pop(t, t0 + i * 0.25)
        if k <= 0:
            continue
        person(d, W / 2 + (i - 1) * gap, by, s * k, who, moods[i], arms[i])


def scene_hook(t):
    im = base(); d = ImageDraw.Draw(im)
    if t < T_ONE - 0.1:
        label(d, W / 2, 230, "2006", 90, (240, 240, 245))
        friends_row(d, t, 1520, 0.92, t0=-1.0 if t < 0.7 else -1.0)
        for i in range(3):
            k = pop(t, 0.3 + i * 0.12)
            if k > 0:
                envelope(d, W / 2 + (i - 1) * 330, 860 - 30 * k, 0.95 * k)
        k = pop(t, 1.0)
        if k > 0:
            label(d, W / 2, 400, "SAME $1,000 · SAME S&P 500", int(52 * k), YEL)
    else:
        label(d, W / 2, 230, "BY 2025", 80, (240, 240, 245))
        person(d, 190, 1560, 0.78, "jay", "worried", "down")
        person(d, 890, 1560, 0.78, "sam", "happy", "down")
        hs = 26 * 10.5 * ease((t - T_TEN + 0.6) / 0.8)
        stack(d, 390, 1500, 26, RED, 150)
        stack(d, 690, 1500, max(26, hs), GRN, 150)
        text(d, (390, 1450), "$770", 50, RED, stroke=5)
        text(d, (690, 1500 - max(26, hs) - 50), "$8,061", 56, GRN, stroke=5)
        text(d, (190, 1600), "JAY", 44, RED)
        text(d, (890, 1600), "SAM", 44, GRN)
        k = pop(t, T_TEN)
        if k > 0:
            text(d, (540, 620), "10x", int(230 * k), GOLD, stroke=10)
            text(d, (540, 790), "SAM vs JAY", int(56 * k), WHITE)
    return im


_you = None


def you_img():
    global _you
    if _you is None:
        im = Image.open(os.path.join(ROOT, "assets", "characters", "you-reference.png")).convert("RGB")
        w, h = im.size
        crop = im.crop((0, 0, int(w * 0.40), int(h * 0.82)))
        a = np.asarray(crop).astype(int)
        bgc = a[5, 5]
        m = (np.abs(a - bgc).sum(2) > 40).astype(np.uint8) * 255
        mask = Image.fromarray(m).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
        circ = Image.new("L", crop.size, 0)
        ImageDraw.Draw(circ).ellipse((0, 0, crop.size[0], crop.size[1]), fill=255)
        _you = (crop, mask)
    return _you


def scene_you(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    crop, mask = you_img()
    k = 0.9 + 0.12 * ease((t - t0) / 1.2)
    sz = (int(crop.size[0] * 1.45 * k), int(crop.size[1] * 1.45 * k))
    disc = Image.new("L", sz, 0)
    ImageDraw.Draw(disc).ellipse((0, 0, sz[0], sz[1]), fill=255)
    pic = crop.resize(sz, Image.LANCZOS)
    d.ellipse((W / 2 - sz[0] / 2 - 18, 900 - sz[1] / 2 - 18, W / 2 + sz[0] / 2 + 18, 900 + sz[1] / 2 + 18), fill=(245, 240, 232))
    im.paste(pic, (int(W / 2 - sz[0] / 2), int(900 - sz[1] / 2)), disc)
    kq = pop(t, t0 + 0.25)
    if kq > 0:
        text(d, (W / 2 + 330, 520), "?", int(260 * kq), GOLD, stroke=8)
    for i in range(3):
        bob = math.sin((t - t0) * 4 + i) * 14
        envelope(d, 220 + i * 320, 1420 + bob, 0.8)
    return im


def scene_basket(t, t0, t1):
    im = base(); d = ImageDraw.Draw(im)
    fill = ease((t - t0) / (t1 - t0 - 0.8))
    basket(d, W / 2, 760, fill)
    friends_row(d, t, 1640, 0.62, arms=("up",) * 3, gap=300)
    for i in range(3):
        u = ease((t - t0 - 0.4 - i * 0.35) / 0.7)
        x = W / 2 + (i - 1) * 300 * (1 - u)
        y = 1180 - u * 300
        if u < 0.98:
            envelope(d, x, y, 0.7 * (1 - 0.4 * u))
    k = pop(t, t0 + 1.5)
    if k > 0:
        label(d, W / 2, 300, "START OF 2006", int(64 * k), YEL)
    return im


CRASH = [0.45, 0.5, 0.56, 0.6, 0.62, 0.58, 0.3, 0.26]


def scene_crash(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    upto = ease((t - t0) / max(0.1, T_CRASH - t0 + 0.4))
    shake = 1.0 if T_CRASH <= t < T_CRASH + 0.5 else 0.0
    chart(d, (140, 260, 940, 900), CRASH, upto, [WHITE], crash_label=(0.86, "2008") if t >= T_CRASH - 0.2 else None, shake=shake)
    worried = t >= T_CRASH
    friends_row(d, t, 1640, 0.6, moods=("worried",) * 3 if worried else ("neutral",) * 3, gap=300, t0=-1)
    for i in range(3):
        txt = "$770" if t >= T_770 else "$1,000"
        sc = 0.72 if t >= T_770 else 0.82
        envelope(d, W / 2 + (i - 1) * 300, 1080, sc, txt, WHITE if t < T_770 else (255, 210, 210))
    if t >= T_770:
        text(d, (W / 2, 990), "-23%", 70, RED, stroke=6)
    return im


def scene_jay_sells(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    person(d, 360, 1560, 0.95, "jay", "worried", "hold")
    u = ease((t - t0 - 0.6) / 1.2)
    ex, ey = 360 + u * 380, 1140 + u * 240
    lid = 1.0 - ease((t - T_SHOE - 0.15) / 0.25) if t > T_SHOE else min(1.0, (t - t0) / 0.6)
    shoebox(d, 760, 1540, 1.1, lid_open=lid)
    if u < 0.95:
        envelope(d, ex, ey, 0.8 * (1 - 0.3 * u), "$770")
    label(d, W / 2, 330, "JAY SELLS", 70, RED, WHITE)
    return im


MAYA_LINE = [0.26, 0.3, 0.36, 0.42, 0.48, 0.52]


def scene_maya(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    upto = 0.2 + 0.8 * ease((t - t0) / max(0.5, T_26 - t0 + 0.3))
    chart(d, (160, 300, 940, 860), MAYA_LINE, upto, [YEL])
    if t >= T_26 - 0.2:
        label(d, 760, 360, "+26%", int(70 * pop(t, T_26 - 0.2)) or 1, GRN, WHITE)
    back = t >= T_2009 + 1.8
    mx = 540 if not back else 540
    person(d, 300 if not back else 540, 1600, 0.85, "maya", "worried" if not back else "neutral", "hold")
    if not back:
        k = math.sin((t - t0) * 6) * 8
        d.ellipse((520, 1080 + k, 600, 1160 + k), outline=WHITE, width=6)
        d.line((560, 1120 + k, 560, 1092 + k), fill=WHITE, width=5)
        d.line((560, 1120 + k, 580, 1128 + k), fill=WHITE, width=5)
        text(d, (800, 1200), "waiting...", 54, GREY)
    if t >= T_2009 - 0.2:
        label(d, W / 2, 980, "BUYS BACK: END OF 2009", 52, YEL)
    return im


def couch(d, cx, by):
    d.rounded_rectangle((cx - 300, by - 200, cx + 300, by), 40, fill=(90, 70, 120))
    d.rounded_rectangle((cx - 340, by - 300, cx - 240, by), 30, fill=(110, 86, 150))
    d.rounded_rectangle((cx + 240, by - 300, cx + 340, by), 30, fill=(110, 86, 150))


def scene_sam(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    basket(d, W / 2, 620, 1.0, 0.8)
    couch(d, W / 2, 1640)
    person(d, W / 2, 1560, 0.85, "sam", "happy", "up")
    for i in range(6):
        u = ((t - t0) * 0.9 + i / 6) % 1.0
        x = 300 + i * 95
        y = 260 + u * 380
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=GOLD, outline=(200, 140, 20), width=4)
        text(d, (x, y), "$", 30, (150, 100, 10))
    label(d, W / 2, 1000, "DIVIDENDS REINVESTED", 50, GRN, WHITE)
    return im


def scene_jay_smug(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    wob = [0.4 + 0.08 * math.sin(i * 1.3 + (t - t0) * 5) for i in range(10)]
    chart(d, (140, 260, 940, 820), wob, 1.0, [WHITE])
    person(d, 540, 1600, 0.95, "jay", "smug", "hold")
    shoebox(d, 540, 1300, 0.9)
    text(d, (540, 960), "\"SAFE\"", 70, RED, stroke=6)
    return im


def scene_results(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 250, "END OF 2025", 80, (240, 240, 245))
    data = [("jay", RED, "$770", 1, T_JAY9), ("maya", YEL, "$6,374", 26, T_MAYA9), ("sam", GRN, "$8,061", 33, T_SAM9)]
    for i, (who, col, amt, n, tw) in enumerate(data):
        cx = 220 + i * 320
        u = ease((t - tw) / 0.9)
        if t >= tw - 0.05:
            stack(d, cx, 1180, max(26, n * 22 * u), col, 200)
            k = pop(t, tw + 0.5)
            if k:
                text(d, (cx, 1180 - max(26, n * 22 * u) - 60), amt, int(62 * k), col, stroke=6)
        person(d, cx, 1660, 0.62, who, "worried" if who == "jay" and t >= tw else ("happy" if who == "sam" and t >= tw else "neutral"), "down")
    return im


def trophy(d, cx, cy, s=1.0):
    d.polygon([(cx - 90 * s, cy - 120 * s), (cx + 90 * s, cy - 120 * s), (cx + 60 * s, cy + 10 * s), (cx - 60 * s, cy + 10 * s)], fill=GOLD)
    d.rectangle((cx - 16 * s, cy + 10 * s, cx + 16 * s, cy + 70 * s), fill=GOLD)
    d.rounded_rectangle((cx - 70 * s, cy + 70 * s, cx + 70 * s, cy + 100 * s), int(8 * s), fill=(200, 150, 40))


def scene_winner(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    person(d, 330, 1600, 0.85, "jay", "worried", "hold")
    shoebox(d, 330, 1360, 0.75, lid_open=1.0)
    person(d, 760, 1600, 0.95, "sam", "happy", "up")
    k = pop(t, T_STAYED - 0.2)
    if k:
        trophy(d, 760, 840, 1.3 * k)
        label(d, W / 2, 360, "STAYED IN = WON", int(66 * k), GRN, WHITE)
    return im


def scene_mistake(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    if t < T_MAYA_COST - 0.1:
        k = pop(t, T_MISTAKE - 0.15)
        person(d, 540, 1600, 0.95, "jay", "worried", "hold")
        shoebox(d, 540, 1300, 0.9)
        if k:
            label(d, W / 2, 520, "THE SHOEBOX MISTAKE", int(74 * k), RED, WHITE)
            text(d, (W / 2, 660), "= selling in a crash", int(54 * k), WHITE)
    else:
        person(d, 540, 1600, 0.95, "maya", "worried", "hold")
        k = pop(t, T_MAYA_COST)
        if k:
            text(d, (W / 2, 560), "-$1,700", int(190 * k), RED, stroke=10)
            label(d, W / 2, 760, "MISSED ONE YEAR: 2009 +26%", int(48 * k), YEL)
    return im


def scene_question(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    signs = [("jay", "SELL", RED), ("maya", "WAIT", YEL), ("sam", "HOLD", GRN)]
    for i, (who, s, col) in enumerate(signs):
        cx = 220 + i * 320
        person(d, cx, 1640, 0.62, who, "neutral", "up")
        k = pop(t, t0 + 0.3 + i * 0.3)
        if k:
            label(d, cx, 1180, s, int(64 * k), col, (15, 15, 25) if col != RED else WHITE)
    q = 1 + 0.06 * math.sin((t - t0) * 6)
    text(d, (W / 2, 640), "?", int(380 * q), GOLD, stroke=10)
    return im


def frame_at(t):
    L = LINES
    if t < L["VO-02"][0] - 0.05:
        im = scene_hook(max(t, 0.9) if t < 0.6 else t)
    elif t < L["VO-03"][0] - 0.05:
        im = scene_you(t, L["VO-02"][0])
    elif t < L["VO-04"][0] - 0.05:
        im = scene_basket(t, L["VO-03"][0], L["VO-03"][1])
    elif t < L["VO-05"][0] - 0.05:
        im = scene_jay_sells(t, L["VO-04"][0])
    elif t < L["VO-06"][0] - 0.05:
        im = scene_maya(t, L["VO-05"][0])
    elif t < L["VO-07"][0] - 0.2:
        im = scene_sam(t, L["VO-06"][0])
    elif t < L["VO-08"][0] - 0.1:
        im = scene_jay_smug(t, L["VO-07"][0])
    elif t < L["VO-09"][0] - 0.05:
        im = scene_results(t, L["VO-08"][0])
    elif t < L["VO-10"][0] - 0.2:
        im = scene_mistake(t, L["VO-09"][0])
    else:
        im = scene_question(t, L["VO-10"][0])
    if t < 0.6:  # finished slam card on frame 1
        d = ImageDraw.Draw(im)
        d.rectangle((0, 520, W, 980), fill=(10, 12, 30))
        text(d, (W / 2, 640), "SAME $1,000", 140, WHITE, stroke=8)
        text(d, (W / 2, 830), "→ 10X DIFFERENT", 110, GRN, stroke=8)
    return im


SHIFT = 140


def shifted(im):
    out = base()
    out.paste(im.crop((0, SHIFT, W, H)), (0, 0))
    return out


def main(out):
    n = int(END * FPS)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", AUDIO, "-map", "0:v", "-map", "1:a",
                            "-shortest", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        frame = None
        for folder, a, b in [(CHART3D, LINES["VO-03"][0] - 0.05, LINES["VO-04"][0] - 0.05),
                             (STACKS3D, LINES["VO-08"][0] - 0.1, LINES["VO-09"][0] - 0.05)]:
            if folder and a <= t < b:
                f3 = os.path.join(folder, f"f{int(round((t - a) * FPS)):04d}.jpg")
                if os.path.exists(f3):
                    frame = Image.open(f3).convert("RGB").resize((W, H))
        if frame is None:
            frame = shifted(frame_at(t))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    print(out, n, "frames")


if __name__ == "__main__":
    main(sys.argv[1])
