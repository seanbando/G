"""Typed cards for the Frein edit, one per run, described by the shot's "card" entry in the plan (--arg cfg=..., --arg shot=N).
Every piece of text types on (Saylo rule). Modes:
  portrait : a real portrait as a framed print on a dark wall, the name typed big beside it        (img, name, sub, at)
  title    : the title question typed in two lines, an amber line drawn between two labelled points (l1, l2, a, b, at, at2)
  quote    : white lines with an amber bar, typed, source line under them                           (lines, who, at)
  doc      : a document page, the camera pushes in, amber highlighter sweeps over marked lines      (img, marks)
             marks = [[x0, y0, x1, y1, vo_time], ...] in fractions of the page from its top-left corner
  sources  : a heading and lines typed one after another                                           (head, lines, foot, at)
Source tags for real photos / documents are burned in by assemble.py."""
import json
import os
import sys

import bpy
import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(HERE, "..", ".."))
REPO = os.path.normpath(os.path.join(VID, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "saylo", "tools", "blender"))
import retraced as rt  # noqa: E402

a = kit.args()
N = a.frames
CFG = json.load(open(os.path.join(HERE, a.get("cfg")), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == int(a.get("shot")))
C = S["card"]
T0 = S["start"]
DUR = (N - 1) / CFG["fps"]


def f(t):
    return kit.f(t - T0)


def path(p):
    return os.path.join(VID, *p.split("/"))


def hud_text(cam, body, font, size_frac, x_frac, y_frac, color, start, cps=30, cursor=True, align="LEFT", spacing=1.05):
    """Text fixed to the camera. size and position are fractions of the half frame height / half width."""
    h, hw, hh = rt.hud(cam, 4.0)
    t = kit.text(body, font=font, size=hh * size_frac, spacing=spacing, color=color, strength=1.7, align=align,
                 loc=(hw * x_frac, hh * y_frac, 0), rot=(0, 0, 0), name="T_" + body[:10])
    kit.parent(t, h)
    rt.typed(t, start, cps=cps, cursor=cursor)
    return t, h, hw, hh


rt.setup(bloom=0.25)
mode = C["mode"]

if mode == "portrait":
    kit.backdrop(color="#0A0F1B", distance=0.4, size=40, lit=True)
    ph = kit.image_plane(path(C["img"]), width=1.75, loc=(1.55, 0, 0.1), rot=(90, 0, -3), border=0.07)
    kit.light("AREA", (-3, -5, 3), (1.5, 0, 0), power=260, color="#C9D6F2", size=4, name="Key")
    kit.light("AREA", (5.2, -1.2, 1.5), (1.6, 0.2, 0), power=160, color="#C9D6F2", size=2, name="Rim")   # no amber here: amber is Frein
    cam = kit.camera((0, -8.2, 0.1), look_at=(0.25, 0, 0.1), lens=50)
    kit.key(cam, "location", [(1, (0, -8.2, 0.1)), (N, (0.12, -7.3, 0.1))], ease="linear")
    t, h, hw, hh = hud_text(cam, C["name"], "Anton-Regular", C.get("size", 0.4), -0.9, 0.07, rt.OFF_WHITE, f(C["at"]), cps=26)
    hud_text(cam, C["sub"], "Montserrat-Bold", 0.078, -0.9, -0.23, "#C9D6F2", f(C["at"]) + 18, cps=40, cursor=False, spacing=1.15)
    bar = kit.rect(hh * 0.028, hh * 0.72, "#C9D6F2", loc=(-hw * 0.94, hh * 0.02, 0), rot=(0, 0, 0), name="Bar")
    kit.parent(bar, h)
    for i, (txt, at) in enumerate(C.get("facts", [])):            # short facts typed under the name, each at its word
        hud_text(cam, txt, "Montserrat-Bold", 0.085, -0.9, -0.42 - 0.16 * i, "#FFFFFF", f(at), cps=40, cursor=False, spacing=1.15)
    if C.get("big"):                                               # one number typed large (16 SURGERIES)
        hud_text(cam, C["big"]["text"], "Anton-Regular", 0.34, -0.9, -0.62, rt.OFF_WHITE, f(C["big"]["at"]), cps=22)

elif mode == "title":
    kit.backdrop(color="#070C18", distance=0.4, size=40, lit=False)
    cam = kit.camera((0, -8.2, 0), look_at=(0, 0, 0), lens=50)
    kit.key(cam, "location", [(1, (0, -8.2, 0)), (N, (0, -7.9, 0))], ease="linear")
    t1, h, hw, hh = hud_text(cam, C["l1"], "Montserrat-Bold", 0.2, 0, 0.42, "#FFFFFF", f(C["at"]), cps=28, cursor=False, align="CENTER")
    hud_text(cam, C["l2"], "Montserrat-Bold", 0.2, 0, 0.1, "#FFFFFF", f(C["at2"]), cps=28, align="CENTER")
    # amber line drawn between two labelled points (Retraced title card)
    x0, x1, y = -hw * 0.62, hw * 0.62, -hh * 0.36
    line = kit.rect(x1 - x0, hh * 0.012, rt.AMBER, loc=(x0, y, 0), rot=(0, 0, 0), anchor="left", name="Line")
    kit.parent(line, h)
    kit.key(line, "scale", [(f(C["at2"]) + 8, (0.001, 1, 1)), (f(C["at2"]) + 30, (1, 1, 1))], ease="in_out")
    for x, lab, fr in ((x0, C["a"], f(C["at2"]) + 6), (x1, C["b"], f(C["at2"]) + 26)):
        dot = kit.rect(hh * 0.045, hh * 0.045, rt.AMBER, loc=(x, y, 0.001), rot=(0, 0, 45), name="Dot")
        kit.parent(dot, h)
        kit.fade(dot, [(fr - 3, 0.0), (fr, 1.0)])
        tl = kit.text(lab, font="Montserrat-Bold", size=hh * 0.062, spacing=1.2, color="#C9CED8", strength=1.5,
                      align="LEFT" if x < 0 else "RIGHT", loc=(x, y - hh * 0.13, 0), rot=(0, 0, 0), name="Lab")
        kit.parent(tl, h)
        rt.typed(tl, fr, cps=60, cursor=False)

elif mode == "quote":
    kit.backdrop(color="#0A0F1B", distance=0.4, size=40, lit=False)
    cam = kit.camera((0, -8.2, 0), look_at=(0, 0, 0), lens=50)
    kit.key(cam, "location", [(1, (0, -8.2, 0)), (N, (0, -7.7, 0))], ease="linear")
    fr = f(C["at"])
    n = len(C["lines"])
    for i, ln in enumerate(C["lines"]):
        qs = C.get("size", 0.27)
        cps = max(18, int(sum(len(x) for x in C["lines"]) / max(0.8, (S["end"] - C["at"]) * 0.45)))     # done by 45% of the time left
        t, h, hw, hh = hud_text(cam, ln, "Montserrat-Bold", qs, -0.62, 0.3 - 0.36 * i * qs / 0.27, "#FFFFFF", fr, cps=cps, cursor=(i == n - 1))
        fr += int(len(ln) / cps * CFG["fps"]) + 2
    k_ = C.get("size", 0.27) / 0.27
    hud_text(cam, C["who"], "Montserrat-Bold", 0.075, -0.62, 0.3 - 0.36 * n * k_ + 0.08, rt.AMBER, fr + 4, cps=60, cursor=False, spacing=1.2)
    bar = kit.rect(hh * 0.03, hh * (0.36 * n * k_ + 0.22), rt.AMBER, loc=(-hw * 0.68, hh * (0.3 - 0.18 * (n - 1) * k_), 0), rot=(0, 0, 0), name="Bar")
    kit.parent(bar, h)
    kit.fade(bar, [(f(C["at"]) - 3, 0.0), (f(C["at"]), 1.0)])

elif mode == "doc":
    kit.backdrop(color="#0A0F1B", distance=0.6, size=60, lit=True)
    W = 5.0
    page = kit.image_plane(path(C["img"]), width=W, loc=(0, 0, 0), rot=(90, 0, 0), lit=False, strength=0.92)
    H = page["height"]
    marks = C["marks"]
    top = (0.5 - min(m[1] for m in marks)) * H
    bot = (0.5 - max(m[3] for m in marks)) * H
    zc = (top + bot) / 2
    if C.get("wide"):                                  # a short, wide clipping (a headline): keep all of it in frame
        cam = kit.camera((0.4, -9.8, zc + 0.3), look_at=(0, 0, zc), lens=50)
        kit.key(cam, "location", [(1, (0.4, -9.8, zc + 0.3)), (N, (0.0, -7.4, zc))], ease="in_out")
    else:
        cam = kit.camera((0.5, -9.5, zc + 0.6), look_at=(0, 0, zc + 0.5), lens=50)
        kit.key(cam, "location", [(1, (0.5, -9.5, zc + 0.6)), (N, (-0.25, -5.6, zc + 0.05))], ease="in_out")
        kit.key(kit.aim(cam), "location", [(1, (0, 0, zc + 0.5)), (N, (-0.3, 0, zc))], ease="in_out")
    for x0, y0, x1, y1, t in marks:                    # amber highlighter sweeps left to right
        w, hgt = (x1 - x0) * W, (y1 - y0) * H
        r = kit.rect(w, hgt, rt.AMBER, loc=((x0 - 0.5) * W, -0.01, (0.5 - (y0 + y1) / 2) * H), rot=(90, 0, 0), anchor="left", name="Mark")
        kit.fade(r, [(1, 0.42)])
        kit.key(r, "scale", [(f(t), (0.001, 1, 1)), (f(t) + 12, (1, 1, 1))], ease="out")

elif mode == "strike":
    # what investigators did not have: each word types on, then is struck through at its moment
    kit.backdrop(color="#0A0F1B", distance=0.4, size=40, lit=False)
    cam = kit.camera((0, -8.2, 0), look_at=(0, 0, 0), lens=50)
    kit.key(cam, "location", [(1, (0, -8.2, 0)), (N, (0, -7.8, 0))], ease="linear")
    n = len(C["items"])
    for i, (txt, at) in enumerate(C["items"]):
        y = 0.36 - 0.36 * i
        t, h, hw, hh = hud_text(cam, txt, "Anton-Regular", 0.3, -0.5, y, rt.OFF_WHITE, f(at) - 12, cps=30, cursor=False)
        bar = kit.rect(hw * (0.075 * len(txt) + 0.08), hh * 0.028, rt.AMBER, loc=(-hw * 0.53, hh * (y + 0.0), 0.002), rot=(0, 0, 0), anchor="left", name="Strike")
        kit.parent(bar, h)
        kit.key(bar, "scale", [(f(at), (0.001, 1, 1)), (f(at) + 6, (1, 1, 1))], ease="out")
    hud_text(cam, C["head"], "Montserrat-Bold", 0.08, -0.5, 0.36 + 0.3, rt.AMBER, f(C["at"]), cps=40, cursor=False, spacing=1.2)

elif mode == "sources":
    kit.backdrop(color="#070C18", distance=0.4, size=40, lit=False)
    cam = kit.camera((0, -8.2, 0), look_at=(0, 0, 0), lens=50)
    kit.key(cam, "location", [(1, (0, -8.2, 0)), (N, (0, -7.9, 0))], ease="linear")
    fr = f(C["at"])
    t, h, hw, hh = hud_text(cam, C["head"], "Anton-Regular", 0.2, -0.6, 0.52, rt.AMBER, fr, cps=40, cursor=False)
    # each line starts a beat after the one before and types fast, so the whole card is complete with time to read
    fr += 5
    for i, ln in enumerate(C["lines"]):
        hud_text(cam, ln, "Montserrat-Bold", 0.092, -0.6, 0.24 - 0.17 * i, "#FFFFFF", fr, cps=75, cursor=False, spacing=1.12)
        fr += 5
    hud_text(cam, C["foot"], "Montserrat-Bold", 0.07, -0.6, 0.24 - 0.17 * len(C["lines"]) - 0.1, "#C9CED8", fr + 3, cps=80, spacing=1.15)
    bar = kit.rect(hh * 0.022, hh * 1.15, rt.AMBER, loc=(-hw * 0.66, hh * 0.08, 0), rot=(0, 0, 0), name="Bar")
    kit.parent(bar, h)

rt.finish(vignette=0.5)
