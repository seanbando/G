"""Render Saylo typewriter graphics as video: full cards and transparent overlays.

Every piece of on-screen text types on letter by letter with a blinking cursor (style sheet §8).

Python use:
    from make_card import card, overlay
    card(out_mp4, lines, seconds, bg=None)            # full-screen card (black or darkened image bg)
    overlay(out_mov, text, seconds, kind="tag")        # transparent overlay: "tag" (lower-left name), "stamp" (top-left timestamp)

lines: list of (text, style) where style is "type" (typewriter), "big" (large condensed caps) or "amber" (typewriter, amber).
Needs ffmpeg + Pillow. 1920x1080, 30 fps.
"""
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
CPS = 30  # characters per second while typing
TYPE_FONT = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"
BIG_FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
OFF_WHITE = (236, 232, 222)
AMBER = (255, 170, 40)


def _font(path, size):
    return ImageFont.truetype(path, size)


def _pipe(out, alpha=False):
    if alpha:
        args = ["-c:v", "qtrle", "-pix_fmt", "argb"]
    else:
        args = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p"]
    return subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
                             "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *args, out],
                            stdin=subprocess.PIPE)


def _background(bg):
    if not bg:
        return Image.new("RGBA", (W, H), (8, 9, 11, 255))
    im = Image.open(bg).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    im = im.filter(ImageFilter.GaussianBlur(6))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.blend(im, dark, 0.72).convert("RGBA")


def _styles():
    return {"type": (_font(TYPE_FONT, 64), OFF_WHITE), "amber": (_font(TYPE_FONT, 64), AMBER),
            "big": (_font(BIG_FONT, 120), OFF_WHITE), "small": (_font(TYPE_FONT, 44), (190, 186, 176))}


def card(out, lines, seconds, bg=None):
    """Full-screen card. Lines type on one after another, centred, then the cursor blinks."""
    st = _styles()
    base = _background(bg)
    total_chars = sum(len(t) for t, _ in lines)
    # layout
    d0 = ImageDraw.Draw(base)
    heights = [d0.textbbox((0, 0), t or " ", font=st[s][0])[3] + 28 for t, s in lines]
    y0 = (H - sum(heights)) // 2
    p = _pipe(out)
    frames = int(seconds * FPS)
    for f in range(frames):
        shown = int(f / FPS * CPS)
        im = base.copy()
        d = ImageDraw.Draw(im)
        y, left = y0, shown
        cursor_xy = None
        for (text, style), hgt in zip(lines, heights):
            font, color = st[style]
            part = text[:max(0, min(len(text), left))]
            full_w = d.textlength(text, font=font)
            x = (W - full_w) / 2
            d.text((x, y), part, font=font, fill=color)
            if 0 <= left <= len(text) or (left > len(text) and cursor_xy is None and text is lines[-1][0]):
                cursor_xy = (x + d.textlength(part, font=font) + 6, y, font)
            left -= len(text)
            y += hgt
        done = shown >= total_chars
        blink_on = (not done) or (int(f / FPS * 2) % 2 == 0 and (f / FPS) < total_chars / CPS + 1.6)
        if cursor_xy and blink_on:
            cx, cy, font = cursor_xy
            hh = font.size
            d.rectangle((cx, cy + 6, cx + hh * 0.45, cy + hh + 4), fill=OFF_WHITE)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()


def overlay(out, text, seconds, kind="tag", sub=None):
    """Transparent overlay that types on: a lower-left name tag or a top-left timestamp stamp."""
    if kind == "tag":
        font, color, pos = _font(BIG_FONT, 72), OFF_WHITE, (110, 860)
    else:
        font, color, pos = _font(TYPE_FONT, 46), OFF_WHITE, (90, 70)
    sfont = _font(TYPE_FONT, 36)
    p = _pipe(out, alpha=True)
    n = len(text) + (len(sub) if sub else 0)
    for f in range(int(seconds * FPS)):
        shown = int(f / FPS * CPS)
        fade = min(1.0, max(0.0, (seconds - f / FPS) / 0.4))  # fade out in the last 0.4 s
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        part = text[:shown]
        x, y = pos
        if part:
            tw = d.textlength(text, font=font)
            box = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(box).rectangle((x - 24, y - 14, x + tw + 34, y + font.size + 20 + (50 if sub else 0)),
                                          fill=(0, 0, 0, int(150 * fade)))
            im = Image.alpha_composite(im, box)
            d = ImageDraw.Draw(im)
            d.rectangle((x - 24, y - 14, x - 16, y + font.size + 20 + (50 if sub else 0)), fill=AMBER + (int(255 * fade),))
            d.text((x, y), part, font=font, fill=color + (int(255 * fade),))
        if sub and shown > len(text):
            d.text((x + 2, y + font.size + 18), sub[:shown - len(text)], font=sfont, fill=(200, 196, 186, int(255 * fade)))
        if shown < n or int(f / FPS * 2) % 2 == 0:
            cur_text = part if shown <= len(text) else None
            if cur_text is not None and fade > 0.5:
                cx = x + d.textlength(cur_text, font=font) + 6
                d.rectangle((cx, y + 8, cx + font.size * 0.4, y + font.size + 6), fill=OFF_WHITE + (int(255 * fade),))
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()
