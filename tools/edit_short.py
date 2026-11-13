"""Add viral-style transitions and camera moves to a finished vertical short.

Usage:
    python3 tools/edit_short.py <in.mp4> <cues.txt> <out.mp4> [--audio <track>]

Cue lines ("#" starts a comment):
    <time> zoomthru            punch-zoom through the cut at <time> with blur and a flash
    <time> whip [left|right]   whip pan through the cut at <time>
    <time> flash               white flash starting at <time>
    <time> shake [seconds]     camera shake starting at <time> (default 0.25 s)
    <time> punch               quick zoom-in on a word, easing back out
    <time> push <end> <zoom>   slow push-in from <time> to <end> up to <zoom> (e.g. 1.08)
    <time> reframe <0|1|2>     jump to a slightly different framing until the next reframe
                               (0 = full frame, 1 = 7% in, upper left, 2 = 10% in, lower right),
                               like a quick cut; tools/auto_punch.py writes these
    <time> card <seconds> <red|green|black> <text>
                               full-screen number card: the frame dims and blurs, the text
                               slams in big in a marker font with a small shake, e.g.
                               "35.1 card 1.4 red $113,000,000,000"

Transitions are centred on the cut: the outgoing scene accelerates into the
cut and the incoming scene settles out of it (0.18 s each side). The video's
own audio is kept unless --audio gives a replacement track.
"""
import math
import subprocess
import sys

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "PermanentMarker-Regular.ttf")
COLORS = {"red": (196, 30, 45), "green": (34, 98, 58), "black": (20, 20, 20)}
REFRAMES = {0: (1.0, 0.0, 0.0), 1: (1.07, 0.02, 0.02), 2: (1.10, -0.02, -0.025)}

HALF = 0.18  # seconds each side of a transition


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip().split(",")
    num, den = out[2].split("/")
    return int(out[0]), int(out[1]), float(num) / float(den)


def read_cues(path):
    cues = []
    for raw in open(path):
        line = raw.split("#", 1)[0].split()
        if line:
            cues.append((float(line[0]), line[1], line[2:]))
    return cues


def ease(x):  # smooth 0..1
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def state(t, cues):
    """Zoom, x/y offset (fraction of size), blur, horizontal blur and flash at time t."""
    zoom, dx, dy, blur, hblur, flash = 1.0, 0.0, 0.0, 0.0, 0.0, 0.0
    frames = [(c, args) for c, kind, args in cues if kind == "reframe" and c <= t]
    if frames:
        rz, rx, ry = REFRAMES[int(max(frames)[1][0]) if max(frames)[1] else 0]
        zoom, dx, dy = rz, rx, ry
    for c, kind, args in cues:
        u = t - c
        if kind == "zoomthru" and -HALF <= u <= HALF:
            if u < 0:   # rush in
                k = ease((u + HALF) / HALF)
                zoom *= 1 + 0.55 * k * k
                blur = max(blur, 6 * k * k)
            else:       # settle
                k = 1 - ease(u / HALF)
                zoom *= 1 + 0.25 * k
                blur = max(blur, 4 * k)
            flash = max(flash, 0.55 * (1 - abs(u) / 0.06)) if abs(u) < 0.06 else flash
        elif kind == "whip" and -HALF <= u <= HALF:
            sign = -1 if (args[:1] or ["left"])[0] == "left" else 1
            if u < 0:
                k = ease((u + HALF) / HALF)
                dx += sign * 0.9 * k * k
                hblur = max(hblur, 40 * k)
            else:
                k = 1 - ease(u / HALF)
                dx += -sign * 0.6 * k * k
                hblur = max(hblur, 30 * k)
        elif kind == "flash" and 0 <= u < 0.2:
            flash = max(flash, 0.85 * (1 - u / 0.2))
        elif kind == "shake":
            dur = float(args[0]) if args else 0.25
            if 0 <= u < dur:
                amp = 0.018 * (1 - u / dur)
                dx += amp * math.sin(u * 95)
                dy += amp * math.cos(u * 77)
                zoom *= 1.04
        elif kind == "punch" and 0 <= u < 0.75:
            k = ease(u / 0.1) if u < 0.1 else 1 - ease((u - 0.1) / 0.65)
            zoom *= 1 + 0.12 * k
        elif kind == "push":
            end, z = float(args[0]), float(args[1])
            if c <= t <= end:
                zoom *= 1 + (z - 1) * ease((t - c) / (end - c))
    return zoom, dx, dy, blur, hblur, flash


def card_at(t, cues):
    """The number card showing at time t, as (text, colour, seconds into the card), or None."""
    for c, kind, args in cues:
        if kind == "card" and c <= t < c + float(args[0]):
            return " ".join(args[2:]), COLORS.get(args[1], COLORS["black"]), t - c
    return None


def draw_card(im, w, h, card):
    text, colour, u = card
    fade = min(u / 0.08, 1.0)
    bg = im.filter(ImageFilter.GaussianBlur(10 * fade))
    bg = Image.blend(bg, Image.new("RGB", (w, h), (246, 246, 240)), 0.55 * fade)
    size = int(w * 0.16)
    font = ImageFont.truetype(FONT, size)
    while ImageDraw.Draw(bg).textlength(text, font=font) > w * 0.9 and size > 20:
        size -= 4
        font = ImageFont.truetype(FONT, size)
    k = 1.0 + 0.6 * max(0.0, 1 - u / 0.12)          # slam: big to normal in 0.12 s
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((w / 2, h * 0.45), text, font=font, fill=colour + (255,), anchor="mm")
    if k != 1.0:
        lw, lh = int(w * k), int(h * k)
        layer = layer.resize((lw, lh), Image.BILINEAR).crop(((lw - w) // 2, (lh - h) // 2, (lw - w) // 2 + w, (lh - h) // 2 + h))
    out = bg.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")


def render(frame, w, h, s, card=None):
    zoom, dx, dy, blur, hblur, flash = s
    if card:
        im = draw_card(Image.fromarray(frame), w, h, card)
        if card[2] < 0.2:  # small shake as it lands
            a = 0.012 * (1 - card[2] / 0.2)
            dx += a * math.sin(card[2] * 90)
            dy += a * math.cos(card[2] * 70)
        frame = np.asarray(im)
    if zoom == 1 and dx == 0 and dy == 0 and blur == 0 and hblur == 0 and flash == 0:
        return frame
    im = Image.fromarray(frame)
    if zoom != 1 or dx or dy:
        cw, ch = w / zoom, h / zoom
        cx, cy = w / 2 - dx * w, h / 2 - dy * h
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        # Fill anything outside the frame with the board colour, not black.
        big = Image.new("RGB", (w * 3, h * 3), tuple(int(v) for v in frame[4, 4]))
        big.paste(im, (w, h))
        im = big.crop((box[0] + w, box[1] + h, box[2] + w, box[3] + h)).resize((w, h), Image.BILINEAR)
    if hblur > 1:
        f = max(1, int(hblur))
        im = im.resize((max(1, w // f), h), Image.BILINEAR).resize((w, h), Image.BILINEAR)
    if blur > 0.5:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    if flash > 0:
        im = Image.blend(im, Image.new("RGB", (w, h), "white"), min(flash, 1.0))
    return np.asarray(im)


def main(src, cue_file, out, audio=None):
    w, h, fps = probe(src)
    cues = read_cues(cue_file)
    dec = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc_in = ["-i", audio] if audio else ["-i", src]
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-", *enc_in,
                            "-map", "0:v", "-map", "1:a", "-shortest",
                            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
                           stdin=subprocess.PIPE)
    size, i = w * h * 3, 0
    # With a replacement track, stop at its end (the video may run longer).
    last = None
    if audio:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                    "-of", "csv=p=0", audio], capture_output=True, text=True).stdout)
        last = int(dur * fps)
    while last is None or i < last:
        buf = dec.stdout.read(size)
        if len(buf) < size:
            break
        frame = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        enc.stdin.write(np.ascontiguousarray(render(frame, w, h, state(i / fps, cues), card_at(i / fps, cues))).tobytes())
        i += 1
    enc.stdin.close()
    enc.wait()
    dec.kill()
    dec.wait()
    print(f"{out}: {i} frames, {len(cues)} cues")


if __name__ == "__main__":
    argv = sys.argv[1:]
    audio = None
    if "--audio" in argv:
        k = argv.index("--audio")
        audio = argv[k + 1]
        del argv[k:k + 2]
    if len(argv) != 3:
        sys.exit(__doc__)
    main(*argv, audio=audio)
