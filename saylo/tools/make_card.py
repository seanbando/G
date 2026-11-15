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


# Windows stand-ins for the Linux fonts above (same look: bold monospace typewriter, bold sans)
_WIN_FONTS = {"FreeMonoBold.ttf": "courbd.ttf", "LiberationSans-Bold.ttf": "arialbd.ttf"}


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        import os
        alt = _WIN_FONTS.get(os.path.basename(path))
        if not alt:
            raise
        return ImageFont.truetype(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", alt), size)


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


# ---------------------------------------------------------------------------
# Documentary Pro looks, rebuilt in 2D (the creator's Blender kit can't run in the cloud).
# Fonts: saylo/assets/fonts (Anton, Montserrat-Bold, Gelasio; OFL licensed).
import math
import os
import random

_FONTS = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
ANTON = os.path.join(_FONTS, "Anton-Regular.ttf")
MONT_B = os.path.join(_FONTS, "Montserrat-Bold.ttf")
GELASIO = os.path.join(_FONTS, "Gelasio-Variable.ttf")
ACCENT = (224, 160, 64)  # #E0A040


def _ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def _ease_expo(x):
    x = max(0.0, min(1.0, x))
    return 1.0 if x >= 1 else 1 - 2 ** (-10 * x)


def lower_third(out, name, role, seconds):
    """Transparent overlay: amber bar leads, dark panel wipes open, name types on (Montserrat Bold),
    role in amber caps underneath; everything leaves in the last 0.6 s."""
    fn, fr = _font(MONT_B, 66), _font(MONT_B, 32)
    x0, y0 = 150, 820
    tmp = Image.new("RGBA", (10, 10))
    dd = ImageDraw.Draw(tmp)
    width = max(dd.textlength(name, font=fn), dd.textlength(role.upper(), font=fr) * 1.05) + 90
    height = 150
    p = _pipe(out, alpha=True)
    n = int(seconds * FPS)
    for f in range(n):
        t = f / FPS
        leave = max(0.0, (t - (seconds - 0.6)) / 0.6)
        open_k = _ease_expo((t - 0.1) / 0.45) * (1 - _ease_expo(leave))
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        pw = int(width * open_k)
        if pw > 2:
            d.rectangle((x0, y0, x0 + pw, y0 + height), fill=(14, 17, 22, int(225 * (1 - leave))))
        bar_x = x0 - 18 + int(-60 * (1 - _ease_expo(t / 0.25)))
        d.rectangle((bar_x, y0, bar_x + 10, y0 + height), fill=ACCENT + (int(255 * (1 - leave)),))
        shown = int(max(0.0, t - 0.4) * CPS)
        a = int(255 * (1 - leave))
        d.text((x0 + 36, y0 + 18), name[:shown], font=fn, fill=(255, 255, 255, a))
        rshown = int(max(0.0, t - 0.4 - len(name) / CPS) * CPS * 1.4)
        d.text((x0 + 38, y0 + 98), role.upper()[:rshown], font=fr, fill=ACCENT + (a,))
        if shown < len(name) and a > 0:
            cx = x0 + 36 + d.textlength(name[:shown], font=fn) + 4
            d.rectangle((cx, y0 + 26, cx + 26, y0 + 84), fill=(255, 255, 255, a))
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()


def number_build(out, value, seconds, prefix="", suffix="", label="", land=2.0, seed=7):
    """Full-frame: a big gold Anton figure counts up and lands on `land` seconds, dust motes drift,
    the frame pushes in slowly; a rule and label arrive after the count lands."""
    rnd = random.Random(seed)
    motes = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.5, 7), rnd.uniform(-8, 8), rnd.uniform(-5, 3),
              rnd.uniform(40, 140)) for _ in range(70)]
    bg = Image.new("RGB", (W, H), (5, 7, 10))
    g = ImageDraw.Draw(bg)
    for r in range(900, 0, -12):  # soft centre glow
        c = int(5 + 22 * (1 - r / 900) ** 2)
        g.ellipse((W / 2 - r * 1.6, H / 2 - r, W / 2 + r * 1.6, H / 2 + r), fill=(c, c + 4, c + 12))
    fbig, flab = _font(ANTON, 230), _font(MONT_B, 40)
    p = _pipe(out)
    n = int(seconds * FPS)
    for f in range(n):
        t = f / FPS
        k = _ease_out(t / max(land, 0.1))
        val = value * k
        txt = f"{prefix}{val:,.0f}{suffix}"
        im = bg.copy().convert("RGBA")
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for (mx, my, ms, vx, vy, ma) in motes:
            x, y = (mx + vx * t) % W, (my + vy * t) % H
            d.ellipse((x - ms, y - ms, x + ms, y + ms), fill=(255, 220, 160, int(ma * 0.5)))
        layer = layer.filter(ImageFilter.GaussianBlur(2.2))
        im = Image.alpha_composite(im, layer)
        d = ImageDraw.Draw(im)
        tw = d.textlength(txt, font=fbig)
        ty = H / 2 - 190
        # gold with a soft shadow
        d.text((W / 2 - tw / 2 + 6, ty + 8), txt, font=fbig, fill=(0, 0, 0, 160))
        d.text((W / 2 - tw / 2, ty), txt, font=fbig, fill=(226, 182, 92, 255))
        if t > land:
            rk = _ease_expo((t - land) / 0.5)
            rw = 520 * rk
            d.rectangle((W / 2 - rw, H / 2 + 95, W / 2 + rw, H / 2 + 99), fill=(226, 182, 92, 255))
            if label:
                la = int(255 * _ease_out((t - land - 0.1) / 0.5))
                lw = d.textlength(label, font=flab)
                d.text((W / 2 - lw / 2, H / 2 + 125 + 12 * (1 - la / 255)), label, font=flab, fill=(217, 222, 230, la))
        # slow push-in + slight shake
        z = 1.0 + 0.06 * t / seconds
        sx = 2.5 * math.sin(t * 7.1)
        sy = 2.0 * math.cos(t * 6.3)
        zw, zh = int(W / z), int(H / z)
        cx, cy = (W - zw) / 2 + sx, (H - zh) / 2 + sy
        frame = im.crop((int(cx), int(cy), int(cx) + zw, int(cy) + zh)).resize((W, H), Image.BILINEAR)
        # vignette
        p.stdin.write(frame.tobytes())
    p.stdin.close()
    p.wait()


def photo_stack(out, photos, seconds, date, where="", beat=1.6):
    """Full-frame: real photos land one by one on a dark table (back first), then a date card
    (Montserrat Bold date, Gelasio amber place) lands on `beat` with a small overshoot; slow drift."""
    table = Image.new("RGB", (W, H), (12, 11, 9))
    g = ImageDraw.Draw(table)
    for r in range(1000, 0, -10):
        c = (int(12 + 30 * (1 - r / 1000) ** 2), int(11 + 26 * (1 - r / 1000) ** 2), int(9 + 20 * (1 - r / 1000) ** 2))
        g.ellipse((W / 2 - r * 1.5, H / 2 - r, W / 2 + r * 1.5, H / 2 + r), fill=c)
    layout = [(980, 470, -3), (620, 430, 5), (1330, 400, -6), (760, 360, 3)]  # front to back
    prints = []
    for i, path in enumerate(photos[:4]):
        ph = Image.open(path).convert("RGB")
        ph.thumbnail((760, 560))
        framed = Image.new("RGB", (ph.width + 28, ph.height + 28), (236, 232, 222))
        framed.paste(ph, (14, 14))
        prints.append(framed.convert("RGBA"))
    n_p = len(prints)
    fd, fw = _font(MONT_B, 64), _font(GELASIO, 40)
    p = _pipe(out)
    for f in range(int(seconds * FPS)):
        t = f / FPS
        im = table.copy().convert("RGBA")
        for i in range(n_p - 1, -1, -1):  # back to front
            t0 = (n_p - 1 - i) * 0.25
            k = _ease_expo((t - t0) / 0.6)
            if k <= 0:
                continue
            cx, cy, rot = layout[i] if n_p > 1 else (W / 2, 470, -2)
            pr = prints[i].rotate(rot * (1 + 1.2 * (1 - k)), expand=True, resample=Image.BICUBIC)
            sc = 1.0 + 0.25 * (1 - k)
            pr = pr.resize((int(pr.width * sc), int(pr.height * sc)))
            sh = Image.new("RGBA", pr.size, (0, 0, 0, 0))
            ImageDraw.Draw(sh).rectangle((0, 0, pr.width, pr.height), fill=(0, 0, 0, int(150 * k)))
            sh = sh.filter(ImageFilter.GaussianBlur(18))
            x, y = int(cx - pr.width / 2), int(cy - pr.height / 2 - 60 * (1 - k))
            im.alpha_composite(sh, (x + 18, y + 24)) if x + 18 >= 0 and y + 24 >= 0 else None
            pr.putalpha(Image.eval(pr.getchannel("A"), lambda v: int(v * k)))
            im.alpha_composite(pr, (max(0, x), max(0, y)))
        if t > beat - 0.15:
            k = _ease_expo((t - beat + 0.15) / 0.35)
            d = ImageDraw.Draw(im)
            tw = max(d.textlength(date, font=fd), d.textlength(where, font=fw) if where else 0) + 90
            th = 150 if where else 110
            s = 1.0 + 0.18 * (1 - k)
            x0, y0 = W / 2 - tw * s / 2, H - 120 - th * s
            d.rectangle((x0, y0, x0 + tw * s, y0 + th * s), fill=(16, 18, 21, int(235 * k)))
            d.rectangle((x0, y0, x0 + 9, y0 + th * s), fill=ACCENT + (int(255 * k),))
            d.text((x0 + 36, y0 + 18), date, font=fd, fill=(244, 241, 234, int(255 * k)))
            if where:
                d.text((x0 + 38, y0 + 96), where, font=fw, fill=ACCENT + (int(255 * k),))
        z = 1.0 + 0.05 * t / seconds
        zw, zh = int(W / z), int(H / z)
        dx = 12 * t / seconds
        frame = im.crop((int((W - zw) / 2 + dx), int((H - zh) / 2), int((W - zw) / 2 + dx) + zw, int((H - zh) / 2) + zh)).resize((W, H))
        p.stdin.write(frame.tobytes())
    p.stdin.close()
    p.wait()
