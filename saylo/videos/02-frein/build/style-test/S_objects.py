"""Evidence close-ups for the Frein edit (Retraced: about one 3D shot in five is a single object, lit and pushed in on).
  --arg cfg=<plan>.json --arg shot=N        the shot's "obj" names the object; "stamp" / "label" add typed text
Objects are plain models of the KIND of thing the record names, not copies of the real exhibits:
  case      a black rifle case                         casings   two spent cartridge casings
  license   a blank licence-sized card (no face)       pages     three torn notebook pages (writing not legible)
  notebook  a closed notebook                          laptop    a screen; "lines" type on it one at a time
  cuffs     a pair of handcuffs (amber: the object the whole video is about)
  checkbook a chequebook                               bag       a tied rubbish bag
"""
import io
import json
import math
import os
import random
import sys

import bpy
import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "saylo", "tools", "blender"))
import retraced as rt  # noqa: E402
import clay  # noqa: E402

a = kit.args()
N = a.frames
CFG = json.load(io.open(os.path.join(HERE, a.get("cfg")), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == int(a.get("shot")))
T0 = S["start"]
DUR = (N - 1) / CFG["fps"]
OBJ = S["obj"]


def f(t):
    return kit.f(t - T0)


kit.setup(world="#05070C", view="AgX", look="Medium High Contrast", bloom=0.3, motion_blur=0.3)
table = kit.matte("#1A1D23", 0.45, "Table")
clay.box(6, 4, 0.1, (0, 0, -0.05), table, "Table", bevel=False)
LAMP = {"license": 40, "pages": 45, "notebook": 120, "casings": 160}.get(OBJ, 260)      # pale paper needs far less light than a black case
kit.light("SPOT", (-0.9, -0.8, 1.5), (0, 0, 0.02), power=LAMP, color="#E9EEFF", size=0.5, name="Lamp").data.spot_size = math.radians(70)
kit.light("AREA", (1.6, 1.2, 1.0), (0, 0, 0.05), power=18, color="#8FA6D8", size=2.0, name="Fill")
black = kit.matte("#101216", 0.45, "CaseBlack")
steel = kit.matte("#8A8E96", 0.3, "Steel")
paper = kit.matte("#D8D2C2", 0.9, "Paper")
ink = kit.matte("#3B4254", 0.9, "Ink")
rnd = random.Random(2)
focus = (0, 0, 0.05)
dist = 1.6
lens = 45

if OBJ == "case":
    body = clay.box(1.25, 0.36, 0.12, (0, 0, 0.06), black, "Case")
    for x in (-0.4, 0.4):
        clay.box(0.07, 0.03, 0.03, (x, -0.185, 0.075), steel, "Latch", bevel=False)
    clay.box(0.2, 0.05, 0.035, (0, -0.2, 0.06), black, "Handle")
    for y in (-0.1, 0.0, 0.1):
        clay.box(1.2, 0.012, 0.004, (0, y, 0.122), kit.matte("#1B1E24", 0.4, "Rib"), "Rib", bevel=False)
    dist, lens = 2.3, 40
elif OBJ == "casings":
    brass = kit.metal("#8D8778", 0.35, "DullBrass")
    for i, (x, y, rz) in enumerate(((-0.05, 0.0, 25), (0.07, 0.05, -40))):
        c = clay.cyl(0.006, 0.051, (x, y, 0.006), brass, "Casing", rot=(0, 90, rz), verts=20)
    dist, lens = 0.42, 60
elif OBJ == "license":
    card = clay.box(0.0856, 0.054, 0.001, (0, 0, 0.0006), kit.matte("#C9CCD2", 0.4, "Card"), "Card", rot=(0, 0, 12), bevel=False)
    ph = clay.box(0.024, 0.03, 0.0004, (0, 0, 0), kit.matte("#7C8088", 0.6, "Blank"), "PhotoBlank", bevel=False)
    ph.parent = card
    ph.location = (-0.026, -0.004, 0.0008)
    for k in range(4):
        ln = clay.box(0.036 - 0.006 * (k % 2), 0.0022, 0.0003, (0, 0, 0), ink, "Line", bevel=False)
        ln.parent = card
        ln.location = (0.014, 0.012 - k * 0.008, 0.0008)
    dist, lens = 0.36, 60
elif OBJ in ("pages", "notebook"):
    if OBJ == "notebook":
        clay.box(0.21, 0.28, 0.018, (0, 0, 0.009), kit.matte("#22262E", 0.6, "Cover"), "Notebook", rot=(0, 0, 8))
        for k in range(14):
            clay.cyl(0.006, 0.004, (-0.108, -0.12 + k * 0.0185, 0.019), steel, "Coil", rot=(0, 90, 8), verts=10)
    else:
        for i, (px, py, rz) in enumerate(((-0.2, 0.02, 9), (0.02, -0.03, -6), (0.24, 0.04, 14))):
            pg = clay.box(0.19, 0.27, 0.002, (px, py, 0.002 + i * 0.002), paper, "Page", rot=(0, 0, rz), bevel=False)
            for k in range(11):
                w = rnd.uniform(0.08, 0.16)
                ln = clay.box(w, 0.004, 0.0006, (0, 0, 0), ink, "Line", bevel=False)
                ln.parent = pg
                ln.location = (-0.085 + w / 2, 0.11 - k * 0.021, 0.0015)
    dist, lens = 1.05, 45
elif OBJ == "laptop":
    clay.box(0.34, 0.24, 0.016, (0, 0, 0.008), kit.matte("#2A2D33", 0.4, "Base"), "Base")
    scr = clay.box(0.34, 0.012, 0.22, (0, 0.13, 0.115), kit.matte("#2A2D33", 0.4, "Lid"), "Lid", rot=(-14, 0, 0))
    glass = kit.emission("#0B1422", 1.0, "Screen")
    sc = kit.rect(0.31, 0.19, material=glass, loc=(0, 0.1225, 0.117), rot=(76, 0, 0), name="ScreenGlow")
    head = kit.text(S.get("head", ""), font="Montserrat-Bold", size=0.011, spacing=1.2, color=rt.AMBER, strength=1.8, align="LEFT",
                    loc=(-0.14, 0.121, 0.185), rot=(76, 0, 0), name="Head")
    rt.typed(head, f(S.get("head_at", T0)), cps=40, cursor=False)
    for i, (txt, at) in enumerate(S.get("lines", [])):
        t = kit.text(txt, font="Montserrat-Bold", size=0.0125, spacing=1.08, color="#FFFFFF", strength=1.8, align="LEFT",
                     loc=(-0.14, 0.1215 - 0.0068 * (i + 1), 0.158 - i * 0.03), rot=(76, 0, 0), name=f"L{i}")
        rt.typed(t, f(at), cps=30, cursor=(i == len(S["lines"]) - 1))
    kit.light("AREA", (0, -0.05, 0.3), (0, 0.12, 0.12), power=2, color="#8FB0FF", size=0.3, name="ScreenSpill")
    focus, dist, lens = (0, 0.12, 0.118), 0.86, 50
elif OBJ == "cuffs":
    amber = rt.gloss(rt.SUBJECT, 0.14, 1.0, "CuffAmber")
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.037, minor_radius=0.0045, location=(sx * 0.062, 0, 0.0045))
        kit.assign(bpy.context.active_object, amber)
        clay.box(0.03, 0.022, 0.01, (sx * 0.062 - sx * 0.037, 0, 0.005), amber, "Lock")
    for k in range(3):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.008, minor_radius=0.002, location=((k - 1) * 0.012, 0, 0.004),
                                         rotation=(math.radians(90 if k % 2 else 0), 0, 0))
        kit.assign(bpy.context.active_object, amber)
    dist, lens = 0.5, 60
elif OBJ == "checkbook":
    clay.box(0.16, 0.075, 0.008, (0, 0, 0.004), kit.matte("#2B3A4A", 0.6, "Cheque"), "Checkbook", rot=(0, 0, -10))
    dist, lens = 0.55, 55
elif OBJ == "bag":
    bag = clay.sphere(0.2, (0, 0, 0.15), kit.matte("#0C0D10", 0.25, "BagPlastic"), "Bag", scale=(1.0, 0.85, 0.75), segs=24)
    d = bag.modifiers.new("Crumple", "DISPLACE")
    tex = bpy.data.textures.new("Crumple", "CLOUDS")
    tex.noise_scale = 0.08
    d.texture, d.strength = tex, 0.06
    clay.cone(0.05, 0.1, (0, 0, 0.33), kit.matte("#0C0D10", 0.25, "BagTie"), "Tie", verts=10)
    focus, dist, lens = (0, 0, 0.15), 1.3, 45

ang = math.radians(S.get("angle", 35))
elev = math.radians(S.get("elev", 38))
rate = S.get("rate", 0.1)
p0 = (focus[0] + dist * math.cos(elev) * math.sin(ang), focus[1] - dist * math.cos(elev) * math.cos(ang), focus[2] + dist * math.sin(elev))
if S.get("fly"):                                       # Retraced "fly-in that lands on the thing": start wide, arrive tight
    far = tuple(focus[i] + (p0[i] - focus[i]) * 3.2 for i in range(3))
    cam = kit.camera(far, look_at=focus, lens=lens)
    kit.key(cam, "location", [(1, far), (f(S["fly"]), p0, "in_out"), (N, tuple(focus[i] + (p0[i] - focus[i]) * 0.9 for i in range(3)), "linear")], ease="in_out")
else:
    k = 1.0 - 1.0 / (1.0 + rate * DUR)
    p1 = tuple(p0[i] + (focus[i] - p0[i]) * k for i in range(3))
    cam = kit.camera(p0, look_at=focus, lens=lens)
    kit.key(cam, "location", [(1, p0), (N, (p1[0] - 0.06 * dist, p1[1], p1[2]))], ease="linear")
dof = kit.depth_of_field(cam, focus=dist, fstop=S.get("fstop", 4))
if S.get("stamp"):
    st = S["stamp"]
    rt.date_stamp(cam, st["line"], st.get("sub"), start_frame=f(st["at"]) if st.get("at") is not None else -300, cps=34, sub_cps=60)
kit.post(bloom=0.3, vignette=0.55, grain=0.02)
