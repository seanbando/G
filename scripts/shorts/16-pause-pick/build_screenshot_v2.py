"""Stock screenshot game, laid out like the reference: a full stock "map" on top with one tile lit red
(changing 5x a second), a small result box bottom-left (like the flag box), 3-line white text, YOU below.

Usage: python3 build_screenshot_v2.py <out.mp4>
"""
import math
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import build_screenshot as base

HERE = __file__.rsplit("/", 1)[0] or "."

W, H, FPS, SECS, STEP = 1080, 1920, 30, 7.2, 4  # 7.5 changes a second
F = base.font
PANEL = 960
# a market-map style layout (x, y, w, h) inside the top panel, our own design
TILES = {
    "NVDA": (40, 120, 330, 260), "META": (370, 120, 240, 140), "TSLA": (610, 120, 230, 140), "AMD": (840, 120, 200, 130),
    "PLTR": (840, 250, 200, 130), "SPY": (370, 260, 240, 180), "QQQ": (610, 260, 230, 180),
    "NFLX": (40, 380, 170, 140), "JPM": (210, 380, 160, 140), "XOM": (840, 380, 200, 140),
    "SPCX": (370, 440, 240, 120), "GLD": (610, 440, 230, 120),
    "DIS": (40, 520, 170, 120), "PFE": (210, 520, 160, 120), "KO": (840, 520, 200, 120), "PTON": (370, 560, 470, 80),
}
INFO = {s[0]: s for s in base.STOCKS + [("PTON", "Peloton", 41, "")]}


def board(lit):
    im = Image.new("RGB", (W, PANEL), (243, 244, 246))
    d = ImageDraw.Draw(im)
    for t, (x, y, w, h) in TILES.items():
        on = t == lit
        d.rectangle([x, y, x + w, y + h], fill=(225, 29, 46) if on else (214, 217, 222), outline=(160, 165, 172), width=3)
        f = F("Inter-ExtraBold.otf", max(30, min(64, int(min(w, h) * 0.32))))
        tw = d.textlength(t, font=f)
        d.text((x + (w - tw) / 2, y + h / 2 - f.size * 0.62), t, font=f, fill=(255, 255, 255) if on else (120, 126, 136))
    return im


def result_box(t):
    tick, name, val, emo = INFO[t]
    im = Image.new("RGBA", (300, 250), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((4, 0), "Congratulations!", font=F("Inter-SemiBold.otf", 22), fill=(40, 40, 40))
    d.text((4, 26), "Your $1,000 became:" if tick != "SPCX" else "Your $1,000 (IPO) became:", font=F("Inter-SemiBold.otf", 22), fill=(40, 40, 40))
    d.text((4, 54), name, font=F("Inter-Bold.otf", 22), fill=(20, 20, 20))
    col = (22, 163, 74) if val >= 1000 else (220, 38, 38)
    d.rectangle([0, 88, 280, 240], fill=col)
    vt = ("≈" if tick == "SPCX" else "") + f"${val:,}"
    f = F("Inter-ExtraBold.otf", 64 if len(vt) <= 7 else 56)
    tw = d.textlength(vt, font=f)
    d.text(((280 - tw) / 2, 120), vt, font=f, fill=(255, 255, 255))
    return im


def main(out):
    rnd = random.Random(11)
    n = int(SECS * FPS)
    order, keys = [], list(TILES)
    while len(order) < n // STEP:
        b = keys[:]
        rnd.shuffle(b)
        if order and b[0] == order[-1]:
            b.append(b.pop(0))
        order += b
    order = order[: n // STEP]
    if order[-1] == order[0]:
        order[-1], order[-2] = order[-2], order[-1]
    boards = {t: board(t) for t in TILES}
    boxes = {t: result_box(t) for t in TILES}
    bb = base.bottom_bg()
    you = Image.open(HERE + "/../../../assets/characters/you-front-cutout.png").convert("RGBA")
    sc = 1.75
    you = you.resize((int(you.width * sc), int(you.height * sc)), Image.LANCZOS)
    ftxt = F("Inter-ExtraBold.otf", 64)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out + ".v.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        ph = 2 * math.pi * t / SECS
        lit = order[i // STEP]
        fr = Image.new("RGB", (W, H))
        fr.paste(boards[lit], (0, 0))
        fr.paste(boxes[lit], (24, PANEL - 262), boxes[lit])
        dd = ImageDraw.Draw(fr)
        fs = F("Inter-Medium.otf", 22)
        for j, ln in enumerate(["Historical: end of 2020 to end of 2025,", "dividends reinvested. SpaceX since", "June 2026 IPO. Not financial advice."]):
            dd.text((640, 790 + j * 28), ln, font=fs, fill=(120, 126, 136))
        fr.paste(bb, (0, PANEL))
        bob, sway = 10 * math.sin(ph * 3), 6 * math.sin(ph * 2)
        yx, yy = int((W - you.width) / 2 + sway), int(1960 - you.height + 260 + bob)
        cut = max(0, PANEL - yy)  # keep YOU inside the bottom half, like the reference
        part = you.crop((0, cut, you.width, you.height))
        fr.paste(part, (yx, yy + cut), part)
        d = ImageDraw.Draw(fr)
        for j, ln in enumerate(["The stock you screenshot", "is what your $1,000", "turned into"]):
            base.centered(d, 975 + j * 80, ln, ftxt, (255, 255, 255), 7, (0, 0, 0))
        enc.stdin.write(fr.tobytes())
    enc.stdin.close()
    enc.wait()
    sr = 44100
    N = int(SECS * sr)
    a = np.zeros(N, np.float32)
    beat = SECS / 16

    def put(sig, t0, g):
        s0 = int(t0 * sr)
        e = min(N, s0 + len(sig))
        a[s0:e] += g * sig[: e - s0]

    tk = np.arange(int(0.35 * sr)) / sr
    kick = np.sin(2 * np.pi * (45 + 110 * np.exp(-tk * 28)) * tk) * np.exp(-tk * 9)
    rng = np.random.default_rng(1)
    tn = np.arange(int(0.18 * sr)) / sr
    snare = (rng.standard_normal(len(tn)) * 0.7 + np.sin(2 * np.pi * 190 * tn)) * np.exp(-tn * 22)
    th = np.arange(int(0.05 * sr)) / sr
    hat = rng.standard_normal(len(th)) * np.exp(-th * 90)
    hat = np.diff(hat, prepend=0)
    notes = [55.0, 55.0, 65.41, 49.0]  # A1 A1 C2 G1, one per bar
    for b in range(16):
        t0 = b * beat
        put(kick, t0, 0.9)
        if b % 2 == 1:
            put(snare, t0, 0.45)
        for h in (0, 0.5):
            put(hat, t0 + h * beat, 0.25)
        f = notes[b // 4]
        tb = np.arange(int(beat * 0.9 * sr)) / sr
        bass = np.tanh(2.5 * np.sin(2 * np.pi * f * tb)) * np.exp(-tb * 3)
        put(bass, t0, 0.35)
    m = int(0.02 * sr)
    clk = (np.sin(2 * np.pi * 2200 * np.arange(m) / sr) * np.exp(-np.arange(m) / (0.003 * sr))).astype(np.float32)
    for j in range(len(order)):
        put(clk, j * STEP / FPS, 0.18)
    a = (a / np.abs(a).max() * 0.85).astype(np.float32)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".v.mp4", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out], input=a.tobytes(), check=True)
    subprocess.run(["rm", "-f", out + ".v.mp4"])
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1])
