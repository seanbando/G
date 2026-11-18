"""Motion graphics for "Buy the Game or the Company?" (GTA 6 / Take-Two).

Usage: python3 scripts/shorts/11-gta6-take-two/animate.py <out.mp4>
Reuses the drawing helpers from the three-friends short (same dark navy style).
"""
import json
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "shorts", "10-three-kids"))
import animate_v4 as A  # noqa: E402

W, H, FPS = A.W, A.H, A.FPS
WHITE, RED, YEL, GRN, GOLD, GREY = A.WHITE, A.RED, A.YEL, A.GRN, A.GOLD, A.GREY
PURPLE = (150, 110, 255)
AUDIO = os.path.join(ROOT, "audio", "gta6-FULL.mp3")
WORDS = json.load(open(os.path.join(HERE, "words.json")))
LINES = {l["id"]: (l["start"], l["end"]) for l in WORDS["lines"]}
END = WORDS["lines"][-1]["end"] + 0.35
ease, pop, text, label = A.ease, A.pop, A.text, A.label


def wt(line, word, n=0):
    return [w["start"] for w in WORDS["words"] if w["line"] == line and w["text"].lower().strip(".,?!:") == word][n]


def base():
    return A.base()


def controller(d, cx, cy, s=1.0):
    d.rounded_rectangle((cx - 170 * s, cy - 80 * s, cx + 170 * s, cy + 80 * s), int(70 * s), fill=(60, 66, 100))
    d.rectangle((cx - 115 * s, cy - 12 * s, cx - 55 * s, cy + 12 * s), fill=WHITE)
    d.rectangle((cx - 97 * s, cy - 30 * s, cx - 73 * s, cy + 30 * s), fill=WHITE)
    for ox, oy, c in [(85, -25, GRN), (115, 5, RED), (55, 5, YEL), (85, 35, (110, 170, 255))]:
        d.ellipse((cx + ox * s - 16 * s, cy + oy * s - 16 * s, cx + ox * s + 16 * s, cy + oy * s + 16 * s), fill=c)


def building(d, cx, by, s=1.0, sign="THE COMPANY", col=PURPLE):
    w, h = 300 * s, 520 * s
    d.rectangle((cx - w / 2, by - h, cx + w / 2, by), fill=(48, 56, 100))
    for r in range(8):
        for c in range(4):
            x0 = cx - w / 2 + 30 * s + c * 64 * s
            y0 = by - h + 30 * s + r * 58 * s
            d.rectangle((x0, y0, x0 + 34 * s, y0 + 32 * s), fill=(250, 220, 120) if (r * 3 + c) % 4 else (90, 100, 150))
    label(d, cx, by - h - 50 * s, sign, int(54 * s), col, WHITE)


def bar(d, cx, by, h, w, col, top_text=None, bot_text=None, size=60):
    d.rounded_rectangle((cx - w / 2, by - h, cx + w / 2, by), 14, fill=col)
    if top_text:
        text(d, (cx, by - h - 55), top_text, size, col, stroke=6)
    if bot_text:
        text(d, (cx, by + 55), bot_text, 46, WHITE)


def scene_hook(t, t0, t1):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 230, "GTA 6 · NOV 19", 84, (240, 240, 245))
    k1 = pop(t, t0 + 0.6)
    if k1:
        controller(d, 280, 900, 0.85 * k1)
        text(d, (280, 1100), "THE GAME", int(60 * k1), WHITE)
        text(d, (280, 1180), "millions buy it", int(40 * k1), GREY)
    k2 = pop(t, wt("VO-01", "own") - 0.1)
    if k2:
        building(d, 800, 1260, 0.95 * k2)
        text(d, (800, 1330), "a few OWN it", int(46 * k2), GRN)
    text(d, (540, 900), "vs", 80, GOLD)
    return im


def scene_you(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    crop, _ = A.you_img()
    k = 0.9 + 0.12 * ease((t - t0) / 1.2)
    sz = (int(crop.size[0] * 1.45 * k), int(crop.size[1] * 1.45 * k))
    disc = Image.new("L", sz, 0)
    ImageDraw.Draw(disc).ellipse((0, 0, sz[0], sz[1]), fill=255)
    d.ellipse((W / 2 - sz[0] / 2 - 18, 900 - sz[1] / 2 - 18, W / 2 + sz[0] / 2 + 18, 900 + sz[1] / 2 + 18), fill=(245, 240, 232))
    im.paste(crop.resize(sz), (int(W / 2 - sz[0] / 2), int(900 - sz[1] / 2)), disc)
    kq = pop(t, t0 + 0.25)
    if kq:
        text(d, (W / 2 + 330, 520), "?", int(260 * kq), GOLD, stroke=8)
    controller(d, W / 2, 1500, 0.8)
    return im


def scene_owner(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    k = pop(t, t0 + 0.1)
    building(d, W / 2, 1150, 1.1 * max(k, 0.01), "TAKE-TWO", PURPLE)
    k2 = pop(t, t0 + 0.9)
    if k2:
        d.polygon([(W / 2 - 30, 1200), (W / 2 + 30, 1200), (W / 2, 1260)], fill=WHITE)
        label(d, W / 2, 1330, "owns ROCKSTAR GAMES", int(56 * k2), (240, 240, 245))
    return im


def scene_13k(t, t0, t1):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 320, "$1,000 ON GTA 5 LAUNCH DAY", 56, YEL)
    text(d, (W / 2, 410), "Sept 17, 2013 · about $17 a share", 40, GREY)
    tk = wt("VO-04", "thirteen")
    u = ease((t - (tk - 2.0)) / 2.2)
    val = 1000 + (13000 - 1000) * u if u < 0.999 else 13000
    h = 60 + 740 * u
    bar(d, 330, 1450, 60, 200, GREY, "$1,000", "2013")
    bar(d, 750, 1450, h, 200, GRN, f"${val:,.0f}".replace("$13,000", "≈$13,000"), "TODAY")
    if t >= tk:
        text(d, (330, 1150), "≈13x", int(130 * pop(t, tk)), GOLD, stroke=8)
    return im


def scene_vs_sp(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 230, "SAME YEARS, 2013 → TODAY", 56, (240, 240, 245))
    u = ease((t - t0) / 1.0)
    bar(d, 330, 1450, 800, 220, GRN, "TAKE-TWO", "≈13x")
    bar(d, 750, 1450, 260 * u + 20, 220, (110, 170, 255), "S&P 500", "far less")
    return im


def scene_revenue(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 230, "TAKE-TWO REVENUE", 64, (240, 240, 245))
    u = ease((t - wt("VO-06", "double") + 0.6) / 0.8)
    bar(d, 330, 1450, 360, 220, GREY, "$1.21B", "FY2013")
    bar(d, 750, 1450, 360 + 340 * u, 220, GRN, "$2.35B" if u > 0.5 else "", "FY2014")
    if u > 0.6:
        text(d, (W / 2, 470), "NEARLY 2x", int(110 * pop(t, wt("VO-06", "double"))), GOLD, stroke=8)
    text(d, (W / 2, 1640), "after GTA 5 (Sept 2013)", 40, GREY)
    return im


def scene_runup(t, t0, t1):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 230, "BEFORE GTA 5 EVEN LAUNCHED", 56, YEL)
    pts = [(160, 1250), (330, 1210), (500, 1150), (660, 1060), (800, 960), (920, 880)]
    u = ease((t - t0 - 0.8) / 3.0)
    m = max(2, int(len(pts) * u) + 1)
    d.line([(140, 1350), (960, 1350)], fill=GREY, width=5)
    d.line(pts[:m], fill=GRN, width=16, joint="curve")
    text(d, (160, 1310), "JAN 2013", 38, GREY)
    text(d, (900, 1310), "SEPT 2013", 38, GREY)
    if t > wt("VO-07", "eleven") - 0.1:
        label(d, 200, 1170, "$11", 60, (240, 240, 245))
    if t > wt("VO-07", "eighteen") - 0.1:
        label(d, 900, 800, "$18", 60, GRN, WHITE)
        text(d, (W / 2, 560), "$11 → $18", int(130 * pop(t, wt("VO-07", "eighteen"))), GOLD, stroke=8)
    return im


def scene_today(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 230, "TODAY · DAY BEFORE GTA 6", 56, (240, 240, 245))
    k = pop(t, wt("VO-08", "seven") - 0.1)
    if k:
        text(d, (W / 2, 700), "+7%", int(260 * k), GRN, stroke=10)
        d.polygon([(W / 2 - 70, 470), (W / 2 + 70, 470), (W / 2, 360)], fill=GRN)
    k2 = pop(t, wt("VO-08", "hype") - 0.1)
    if k2:
        r = 190 * k2
        d.ellipse((W / 2 - r, 1150 - r, W / 2 + r, 1150 + r), fill=(240, 90, 160))
        d.line((W / 2, 1150 + r, W / 2, 1150 + r + 160), fill=WHITE, width=5)
        text(d, (W / 2, 1150), "HYPE", int(80 * k2), WHITE)
        text(d, (W / 2, 1560), "already priced in?", int(56 * k2), YEL)
    return im


def scene_targets(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    label(d, W / 2, 230, "ANALYST PRICE TARGETS", 60, (240, 240, 245))
    x0, x1, y = 140, 940, 950
    px = lambda p: x0 + (p - 150) / (350 - 150) * (x1 - x0)
    u = ease((t - t0) / 0.8)
    d.rounded_rectangle((px(170), y - 22, px(170) + (px(330) - px(170)) * u, y + 22), 20, fill=(70, 80, 130))
    k1 = pop(t, wt("VO-09", "three") - 0.1)
    if k1:
        d.ellipse((px(330) - 30, y - 30, px(330) + 30, y + 30), fill=GRN)
        text(d, (px(330), y - 110), "$330", int(70 * k1), GRN, stroke=6)
        text(d, (px(330) - 60, y + 100), "Bank of America", int(40 * k1), WHITE)
    k2 = pop(t, wt("VO-09", "lowest") - 0.1)
    if k2:
        d.ellipse((px(170) - 30, y - 30, px(170) + 30, y + 30), fill=RED)
        text(d, (px(170), y - 110), "$170", int(70 * k2), RED, stroke=6)
        text(d, (px(170) + 30, y + 100), "lowest target", int(40 * k2), WHITE)
    d.line((px(220), y - 60, px(220), y + 60), fill=YEL, width=6)
    text(d, (px(220), y + 180), "today ≈$220", 40, YEL)
    text(d, (W / 2, 1450), "Nobody knows.", 70, WHITE)
    return im


def scene_question(t, t0):
    im = base(); d = ImageDraw.Draw(im)
    for i, (s, col) in enumerate([("GAME", (110, 170, 255)), ("STOCK", GRN), ("BOTH", GOLD)]):
        k = pop(t, t0 + 0.4 + i * 0.35)
        if k:
            label(d, W / 2, 900 + i * 220, s, int(110 * k), col, (15, 15, 25))
    q = 1 + 0.06 * math.sin((t - t0) * 6)
    text(d, (W / 2, 560), "?", int(300 * q), GOLD, stroke=10)
    return im


def frame_at(t):
    L = LINES
    if t < L["VO-02"][0] - 0.05:
        im = scene_hook(max(t, 2.6) if t < 0.6 else t, 0, L["VO-01"][1])
    elif t < L["VO-03"][0] - 0.05:
        im = scene_you(t, L["VO-02"][0])
    elif t < L["VO-04"][0] - 0.05:
        im = scene_owner(t, L["VO-03"][0])
    elif t < L["VO-05"][0] - 0.05:
        im = scene_13k(t, L["VO-04"][0], L["VO-04"][1])
    elif t < L["VO-06"][0] - 0.05:
        im = scene_vs_sp(t, L["VO-05"][0])
    elif t < L["VO-07"][0] - 0.2:
        im = scene_revenue(t, L["VO-06"][0])
    elif t < L["VO-08"][0] - 0.05:
        im = scene_runup(t, L["VO-07"][0], L["VO-07"][1])
    elif t < L["VO-09"][0] - 0.05:
        im = scene_today(t, L["VO-08"][0])
    elif t < L["VO-10"][0] - 0.2:
        im = scene_targets(t, L["VO-09"][0])
    else:
        im = scene_question(t, L["VO-10"][0])
    if t < 0.6:
        d = ImageDraw.Draw(im)
        d.rectangle((0, 520, W, 1000), fill=(10, 12, 30))
        text(d, (W / 2, 610), "GTA 6:", 150, WHITE, stroke=8)
        text(d, (W / 2, 770), "BUY THE GAME", 92, (110, 170, 255), stroke=6)
        text(d, (W / 2, 900), "OR THE COMPANY?", 92, GOLD, stroke=6)
    return im


def main(out):
    n = int(END * FPS)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", AUDIO, "-map", "0:v", "-map", "1:a",
                            "-shortest", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(n):
        enc.stdin.write(A.shifted(frame_at(i / FPS)).tobytes())
    enc.stdin.close()
    enc.wait()
    print(out, n, "frames")


if __name__ == "__main__":
    main(sys.argv[1])
