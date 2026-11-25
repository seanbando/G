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


kit.setup(world="#05070C", view="AgX", look="Medium High Contrast", bloom=0.3, motion_blur=0.3, policy_config=rt.QUALITY)
table = rt.pbr("hangar_concrete_floor", scale=1.4, sat=0.25, name="EvidenceTable")      # worn concrete, not a flat plane
clay.box(6, 4, 0.1, (0, 0, -0.05), table, "Table", bevel=False)
LAMP = {"license": 70, "pages": 80, "notebook": 300, "casings": 160}.get(OBJ, 260)      # pale paper needs far less light than a black case
kit.light("SPOT", (-0.9, -0.8, 1.5), (0, 0, 0.02), power=LAMP, color="#E9EEFF", size=0.5, name="Lamp").data.spot_size = math.radians(70)
kit.light("AREA", (1.6, 1.2, 1.0), (0, 0, 0.05), power=30, color="#8FA6D8", size=2.0, name="Fill")
kit.light("AREA", (0.2, 1.4, 0.35), (0, 0, 0.04), power=22, color="#C9D6F2", size=0.8, name="Rim").data.specular_factor = 1.5
black = kit.matte("#101216", 0.45, "CaseBlack")
steel = kit.matte("#8A8E96", 0.3, "Steel")
paper = kit.matte("#D8D2C2", 0.9, "Paper")
ink = kit.matte("#0E1118", 0.9, "Ink")
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
    clay.box(1.26, 0.37, 0.006, (0, 0, 0.068), kit.matte("#05060A", 0.6, "Seam"), "Seam", bevel=False)      # lid seam
    for x in (-0.5, 0.5):
        clay.box(0.1, 0.02, 0.03, (x, 0.185, 0.07), steel, "Hinge", bevel=False)
    for x in (-0.56, 0.56):
        for y in (-0.15, 0.15):
            clay.cyl(0.02, 0.012, (x, y, 0.126), steel, "Corner", verts=12)
    dist, lens = 2.3, 40
elif OBJ == "casings":
    brass = kit.metal("#8D8778", 0.35, "DullBrass")
    for i, (x, y, rz) in enumerate(((-0.05, 0.0, 25), (0.07, 0.05, -40))):
        c = clay.cyl(0.006, 0.04, (x, y, 0.006), brass, "Casing", rot=(0, 90, rz), verts=24)
        cr_, sr_ = math.cos(math.radians(rz)), math.sin(math.radians(rz))
        clay.cyl(0.0042, 0.012, (x + 0.026 * cr_, y + 0.026 * sr_, 0.006), brass, "Neck", rot=(0, 90, rz), verts=20)     # bottleneck
        clay.cyl(0.0066, 0.0016, (x - 0.0205 * cr_, y - 0.0205 * sr_, 0.006), brass, "Rim", rot=(0, 90, rz), verts=24)    # rim
        clay.cyl(0.0038, 0.0005, (x + 0.0322 * cr_, y + 0.0322 * sr_, 0.006), kit.matte("#07080A", 0.9, "Mouth"), "Mouth", rot=(0, 90, rz), verts=16)
    dist, lens = 0.42, 60
elif OBJ == "license":
    card = clay.box(0.0856, 0.054, 0.001, (0, 0, 0.0006), kit.matte("#C9CCD2", 0.4, "Card"), "Card", rot=(0, 0, 12), bevel=False)
    ph = clay.box(0.024, 0.03, 0.0004, (0, 0, 0), kit.matte("#7C8088", 0.6, "Blank"), "PhotoBlank", bevel=False)
    ph.parent = card
    ph.location = (-0.026, -0.004, 0.002)
    ph.scale = (1, 1, 4)
    for k in range(4):
        ln = clay.box(0.036 - 0.006 * (k % 2), 0.0022, 0.0003, (0, 0, 0), ink, "Line", bevel=False)
        ln.parent = card
        ln.location = (0.014, 0.012 - k * 0.008, 0.002)
        ln.scale = (1, 1, 4)
    dist, lens = 0.36, 60
elif OBJ in ("pages", "notebook"):
    if OBJ == "notebook":
        clay.box(0.21, 0.28, 0.018, (0, 0, 0.009), kit.matte("#22262E", 0.6, "Cover"), "Notebook", rot=(0, 0, 8))
        for k in range(14):
            clay.cyl(0.006, 0.004, (-0.108, -0.12 + k * 0.0185, 0.019), steel, "Coil", rot=(0, 90, 8), verts=10)
    else:
        for i, (px, py, rz) in enumerate(((-0.2, 0.02, 9), (0.02, -0.03, -6), (0.24, 0.04, 14))):
            pg = clay.box(0.19, 0.27, 0.002, (px, py, 0.002 + i * 0.002), paper, "Page", rot=(0, 0, rz), bevel=False)
            cr, sr = math.cos(math.radians(rz)), math.sin(math.radians(rz))
            for k in range(11):                        # ruled handwriting as strokes, placed in world space on the page
                w = rnd.uniform(0.08, 0.16)
                lx, ly = -0.085 + w / 2, 0.11 - k * 0.021
                clay.box(w, 0.005, 0.0012, (px + lx * cr - ly * sr, py + lx * sr + ly * cr, 0.0036 + i * 0.002), ink, "Line",
                         rot=(0, 0, rz), bevel=False).visible_shadow = False
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
    # steel, not amber: the amber pair read as a toy. The amber stays in the type and the edge light.
    amber = rt.gloss("#C4C8CE", 0.2, 1.0, "CuffSteel")
    amber_d = rt.gloss("#3A3D42", 0.35, 0.9, "CuffSteelDark")
    for sx in (-1, 1):
        cx_ = sx * 0.07
        for mr, z_ in ((0.038, 0.004), (0.038, 0.012)):      # the two bars of the fixed bow
            bpy.ops.mesh.primitive_torus_add(major_radius=mr, minor_radius=0.0028, major_segments=64, location=(cx_, 0, z_))
            kit.assign(bpy.context.active_object, amber)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.034, minor_radius=0.0032, major_segments=64, location=(cx_, 0.004, 0.008))
        kit.assign(bpy.context.active_object, amber)          # the swinging ratchet arm, between them
        lock = clay.box(0.03, 0.022, 0.013, (cx_ - sx * 0.04, 0, 0.008), amber, "Lock")
        clay.cyl(0.003, 0.021, (cx_ - sx * 0.04, -0.006, 0.01), amber_d, "Keyhole", verts=12)
        for k_ in range(6):                                # ratchet teeth
            clay.box(0.002, 0.004, 0.006, (cx_ + sx * (0.02 + k_ * 0.003), 0.03 - k_ * 0.0016, 0.008), amber_d, "Tooth", bevel=False)
    for k_ in range(3):                                    # chain links between the two locks
        bpy.ops.mesh.primitive_torus_add(major_radius=0.0075, minor_radius=0.0018, location=((k_ - 1) * 0.011, 0, 0.008),
                                         rotation=(math.radians(90 if k_ % 2 else 0), 0, 0))
        bpy.context.active_object.scale = (1.35, 1, 1)
        kit.assign(bpy.context.active_object, amber)
    dist, lens = 0.52, 60
elif OBJ == "checkbook":
    cb = clay.box(0.16, 0.075, 0.008, (0, 0, 0.004), kit.matte("#22303E", 0.5, "ChequeCover"), "Checkbook", rot=(0, 0, -10))
    cr_, sr_ = math.cos(math.radians(-10)), math.sin(math.radians(-10))
    clay.box(0.158, 0.073, 0.004, (0.004 * cr_, 0.004 * sr_, 0.002), paper, "ChequePages", rot=(0, 0, -10), bevel=False)      # page edges showing
    for k_ in range(3):                                # embossed lines on the cover (no bank name: none is in the record)
        lx_, ly_ = -0.02, 0.012 - k_ * 0.012
        clay.box(0.07 - k_ * 0.012, 0.003, 0.001, (lx_ * cr_ - ly_ * sr_, lx_ * sr_ + ly_ * cr_, 0.0086), kit.matte("#8A8E96", 0.3, "Emboss"), "Emboss", rot=(0, 0, -10), bevel=False)
    dist, lens = 0.55, 55
elif OBJ == "bag":
    bag = clay.sphere(0.2, (0, 0, 0.15), kit.matte("#0C0D10", 0.25, "BagPlastic"), "Bag", scale=(1.0, 0.85, 0.75), segs=48)
    for pl in bag.data.polygons:
        pl.use_smooth = True
    sub = bag.modifiers.new("Round", "SUBSURF")
    sub.levels = sub.render_levels = 2
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
dof = kit.depth_of_field(cam, focus=dist, fstop=S.get("fstop", 11 if OBJ == "laptop" else 4))
if S.get("stamp"):
    st = S["stamp"]
    rt.date_stamp(cam, st["line"], st.get("sub"), start_frame=f(st["at"]) if st.get("at") is not None else -300, cps=34, sub_cps=60)
kit.post(bloom=0.3, vignette=0.55, grain=0.02)
