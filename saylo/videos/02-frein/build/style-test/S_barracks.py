"""The Blooming Grove barracks at night (Frein chapters "The Barracks" and "The Handoff"), one shot per run.
  --arg cfg=shots4.json --arg shot=N
Built from the real building (WNEP photo, creator's file `wnep-b.jpg`; Morning Call sign photo): a tan block building
with a brown hipped roof, the entrance at the left end, a parking lot in front, the road, and woods across it.
SCHEMATIC: sizes and the exact lot layout are an illustration. Troopers are grey mannequins in campaign hats.
NOBODY IS SHOWN BEING HIT: the shots are a flash of light in the tree line, an empty walkway, a lit door.
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
SHOT = int(a.get("shot"))
CFG = json.load(io.open(os.path.join(HERE, a.get("cfg")), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == SHOT)
T0 = S["start"]
N = a.frames
FPS = CFG["fps"]
DUR = (N - 1) / FPS
V = S.get("view", "")                                  # which camera set-up this shot uses


def f(t):
    return kit.f(t - T0)


kit.setup(world=rt.NAVY, view="AgX", look="Medium High Contrast", bloom=0.35, motion_blur=0.3)
rt.sky("evening_road_01_puresky", strength=0.16 if V == "aerial" else 0.075, rot_z=200, sat=0.6)
kit.light("SUN", (-120, 60, 140), (0, 0, 0), power=1.1 if V == "aerial" else 0.34, color="#9FB3E0", name="Moon")

ground = rt.pbr("forest_ground_04", scale=5.0, sat=0.4)
asph = rt.pbr("asphalt_02", scale=4.0, sat=0.2)
block = rt.pbr("brick_wall_08", scale=1.6, sat=0.5, name="TanBlock")
for nd in block.node_tree.nodes:
    if nd.type == "HUE_SAT":
        nd.inputs["Value"].default_value = 1.7
roofm = kit.matte("#3A2D29", 0.85, "Roof")
steel = kit.matte("#3B3F45", 0.5, "Steel")
paint = kit.matte("#B8B5AC", 0.9, "Paint")
white = rt.gloss(rt.WHITE, 0.24, 0.7, "MannequinGloss")
amber = rt.gloss(rt.SUBJECT, 0.14, 1.0, "SubjectGloss2")
m = rt.mats()

kit.rect(1200, 1200, material=ground, loc=(0, 0, 0), rot=(0, 0, 0), name="Ground")
clay.box(76, 30, 0.06, (2, -24, 0.03), asph, "Lot", bevel=False)
clay.box(10, 16, 0.06, (30, -44, 0.03), asph, "Drive", bevel=False)
clay.box(400, 8, 0.06, (0, -52, 0.03), asph, "Road", bevel=False)
for x in range(-190, 195, 12):
    clay.box(4, 0.16, 0.012, (x, -52, 0.066), paint, "Dash", bevel=False)
for x in range(-20, 30, 3):
    clay.box(0.12, 5, 0.012, (x, -13, 0.066), paint, "Bay", bevel=False)

# ------------------------------------------------------------------ the building
BW, BD, BH = 34.0, 16.0, 4.2
clay.box(BW, BD, BH, (0, 0, BH / 2), block, "Barracks", bevel=False)
rt._loft("HipRoof", [[(-BW / 2 - 0.6, -BD / 2 - 0.6, BH), (BW / 2 + 0.6, -BD / 2 - 0.6, BH), (BW / 2 + 0.6, BD / 2 + 0.6, BH), (-BW / 2 - 0.6, BD / 2 + 0.6, BH)],
                     [(-9, 0, BH + 2.7), (9, 0, BH + 2.7), (9, 0.01, BH + 2.7), (-9, 0.01, BH + 2.7)]], mats=[roofm])
clay.box(BW + 1.3, BD + 1.3, 0.14, (0, 0, BH + 0.02), paint, "Fascia", bevel=False)
glass = kit.matte("#0A0D12", 0.15, "Glass")
for wx in (-3, 2, 7, 12, 15.5):
    clay.box(1.7, 0.1, 0.8, (wx, -BD / 2 - 0.03, 3.0), glass, "Window", bevel=False)
    clay.box(1.9, 0.06, 1.0, (wx, -BD / 2 - 0.02, 3.0), paint, "WinFrame", bevel=False)
# lobby entrance at the left end of the front: glass door with warm light behind it, a small canopy
DX, DY = -11.5, -BD / 2
door_m = kit.emission("#FFD6A0", 2.4, "LobbyGlow")
clay.box(2.0, 0.08, 2.3, (DX, DY - 0.05, 1.15), door_m, "LobbyDoor", bevel=False)
clay.box(2.3, 0.12, 2.6, (DX, DY - 0.02, 1.3), steel, "DoorFrame", bevel=False)
clay.box(5.0, 2.6, 0.2, (DX, DY - 1.3, 2.95), paint, "Canopy", bevel=False)
for sx in (-2.3, 2.3):
    clay.cyl(0.07, 2.9, (DX + sx, DY - 2.4, 1.45), steel, "CanopyPost", verts=10)
clay.box(6, 3.2, 0.12, (DX, DY - 1.6, 0.06), kit.matte("#8B8D90", 0.9, "Walk"), "Walk", bevel=False)
lobby = kit.light("AREA", (DX, DY - 0.6, 1.6), (DX, DY - 6, 0.2), power=420, color="#FFD6A0", size=2.2, name="LobbySpill")
# lot lamps: cool white pools (amber stays the accent colour)
for lx, ly in ((-20, -30), (4, -32), (26, -28)):
    clay.cyl(0.09, 7, (lx, ly, 3.5), steel, "LampPole", verts=10)
    clay.box(0.9, 0.35, 0.14, (lx, ly + 0.5, 7.0), steel, "LampHead", bevel=False)
    sp = kit.light("SPOT", (lx, ly + 0.5, 6.9), (lx, ly + 2.5, 0), power=5200, color="#DCE6FF", size=0.6, name="LotLamp")
    sp.data.spot_size = math.radians(115)
# the sign by the drive, facing the road
SX, SY = 23.0, -45.0
for dx in (-1.9, 1.9):
    clay.box(0.18, 0.18, 2.4, (SX + dx, SY, 1.2), paint, "SignPost", bevel=False)
clay.box(4.2, 0.14, 1.7, (SX, SY, 1.75), kit.matte("#15233F", 0.6, "SignBlue"), "SignBoard", bevel=False)
clay.box(4.4, 0.1, 1.9, (SX, SY + 0.03, 1.75), kit.matte("#C8A24A", 0.5, "SignEdge"), "SignEdge", bevel=False)
kit.light("AREA", (SX, SY - 3.2, 0.5), (SX, SY, 1.8), power=260 if V == "chapter" else 70, color="#DCE6FF", size=2.5, name="SignWash").data.specular_factor = 0.2


def sign_text(body, font, size, z, color, start=None, cps=22, cursor=False):
    t = kit.text(body, font=font, size=size, spacing=1.06, color=color, strength=1.6, align="CENTER",
                 loc=(SX, SY - 0.09, z), rot=(90, 0, 0), name="S_" + body[:8])
    t.visible_shadow = False
    if start is not None:
        rt.typed(t, start, cps=cps, cursor=cursor)
    return t


if V == "chapter":                                     # the chapter title is lettered on the sign (Retraced)
    sign_text(S["chapter"][0], "Montserrat-Bold", 0.2, 2.32, rt.AMBER, f(S["chapter_at"]), cps=30)
    sign_text(S["chapter"][1], "Anton-Regular", 0.72, 1.72, "#F4F1EA", f(S["chapter_at"]) + 9, cps=20, cursor=True)
    ul = kit.rect(3.2, 0.05, rt.AMBER, loc=(SX - 1.6, SY - 0.09, 1.2), rot=(90, 0, 0), anchor="left", name="Underline")
    kit.key(ul, "scale", [(f(S["chapter_at"]) + 26, (0.001, 1, 1)), (f(S["chapter_at"]) + 40, (1, 1, 1))], ease="out")
else:
    sign_text("PENNSYLVANIA STATE POLICE", "Montserrat-Bold", 0.25, 2.1, "#E9E6DE")
    sign_text("BLOOMING GROVE", "Montserrat-Bold", 0.42, 1.5, "#E9E6DE")

# ------------------------------------------------------------------ woods on every side, thickest across the road
_W = rt.autumn_woods()
WOODS, SHRUBS = _W[:-2], _W[-2:]
rnd = random.Random(9)
AERIAL = V == "aerial"
placed, want = 0, (5200 if AERIAL else 1700)
ext = 420 if AERIAL else 260
while placed < want:
    x, y = rnd.uniform(-ext, ext), rnd.uniform(-ext, ext)
    if (-44 < x < 44 and -47 < y < 13) or (-200 < x < 200 and -57.5 < y < -46.5):
        continue                                      # the lot and building; the road
    WOODS[rnd.randrange(len(WOODS))]((x, y, 0), rnd.uniform(0, 360), rnd.uniform(11, 19))
    placed += 1
for i in range(60):                                   # a dense edge right across the road from the lot
    x = -88 + i * 3.0 + rnd.uniform(-0.8, 0.8)
    WOODS[rnd.randrange(len(WOODS))]((x, -60 - rnd.uniform(0, 3), 0), rnd.uniform(0, 360), rnd.uniform(12, 18))
    SHRUBS[i % 2]((x + rnd.uniform(-1, 1), -58.2 - rnd.uniform(0, 1), 0), rnd.uniform(0, 360), rnd.uniform(11, 16))
if V in ("treeline", "treeline2", "wide", "vanish"):
    HERO = rt.tree_library("trees_mid.blend")
    for name, x, y, rz, h in (("FirMid", -6, -62, 20, 19), ("PineMid", 12, -63, 200, 21), ("FirMid", 26, -61, 110, 17),
                              ("PineMid", -22, -62.5, 70, 20), ("FirMid", -36, -61, 250, 18)):
        HERO[name]((x, y, 0), rz, h)
if not AERIAL:
    rt.haze((0, -20, 12), (300, 300, 24), density=0.004)

# ------------------------------------------------------------------ cars and people
CAR = (8.0, -16.0)                                     # Cpl. Dickson's assigned cruiser, in its bay (the planted detail)
car, CL = rt.police_car(m, (CAR[0], CAR[1], 0), 0, name="Cruiser")
CL["beam"].data.energy = 0
others = []
if V not in ("aerial",):
    for i, (x, y, r) in enumerate(((20, -16, 0), (-2, -16, 0), (-14, -16.2, 0))):
        c2, l2 = rt.police_car(m, (x, y, 0), r, name=f"Car{i}")
        l2["beam"].data.energy = 0
        others.append(c2)


def trooper(name, x, y, heading, walk=None, phase=0):
    M = rt.real_mannequin(name, (x, y, 0), heading, white, subsurf=2)
    rt.trooper_kit(M, name)
    if walk:
        d = walk * DUR
        hx, hy = math.cos(math.radians(heading)), math.sin(math.radians(heading))
        kit.key(M["root"], "location", [(1, (x, y, 0)), (N, (x + d * hx, y + d * hy, 0))], ease="linear")
        rt.rwalk_cycle(M, 1, N, period=32, phase=phase)
    else:
        rt.rpose(M, "relaxed")
    return M


def facing(frm, to):
    return math.degrees(math.atan2(to[1] - frm[1], to[0] - frm[0]))


def push(p0, aim, rate, lens=35, slide=(0.0, 0.0, 0.0), aim1=None, ease="linear"):
    k = 1.0 - 1.0 / (1.0 + rate * DUR)
    p1 = tuple(p0[i] + (aim[i] - p0[i]) * k + slide[i] for i in range(3))
    cam = kit.camera(p0, look_at=aim, lens=lens)
    kit.key(cam, "location", [(1, p0), (N, p1)], ease=ease)
    if aim1:
        kit.key(kit.aim(cam), "location", [(1, aim), (N, aim1)], ease=ease)
    return cam


def stamp(cam, line, t_line, sub=None):
    rt.date_stamp(cam, line, sub, start_frame=f(t_line) if t_line is not None else -300, cps=34, sub_cps=60)


def flash(pos, t):
    """A rifle shot as light only: a bloom in the trees, full for 2 frames, gone by frame 6 (measured from Retraced)."""
    L = kit.light("POINT", pos, (0, 0, 0), power=0, color="#FFF4DC", size=0.4, name="Flash")
    fr = f(t)
    kit.key(L.data, "energy", [(fr - 1, 0.0), (fr, 260000.0), (fr + 1, 240000.0), (fr + 5, 0.0)], ease="linear")
    em = kit.emission("#FFF4DC", 0.0, "FlashCore")
    core = clay.sphere(0.22, pos, em, "FlashCore")
    nd = next(n for n in em.node_tree.nodes if n.type == "EMISSION")
    kit.key(nd.inputs["Strength"], "default_value", [(fr - 1, 0.0), (fr, 90.0), (fr + 1, 80.0), (fr + 5, 0.0)], ease="linear")


cam = None
ST = S.get("stamp")

if V == "chapter":
    # Retraced chapter card: hold the place, a very fast move with blur, land on the lettering, hold
    p_w, a_w = (46, -70, 5.5), (2, -8, 3)
    p_s, a_s = (SX + 0.5, SY - 5.6, 1.85), (SX, SY, 1.78)
    cam = kit.camera(p_w, look_at=a_w, lens=30)
    fa = f(S["fly_at"])
    kit.key(cam, "location", [(1, p_w), (fa, (43.6, -66.8, 5.3), "linear"), (fa + 6, p_s, "in_out"), (N, (SX + 0.35, SY - 4.9, 1.83), "linear")], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, a_w), (fa, a_w, "linear"), (fa + 6, a_s, "in_out"), (N, a_s, "linear")], ease="linear")
elif V == "aerial":
    cam = push((70, -110, 85), (0, -12, 0), 0.1, lens=32)
elif V == "lot":
    cam = push((-26, -40, 1.6), (-4, -9, 2.4), 0.06, lens=28)
elif V == "leaving":
    for i, (x, y) in enumerate(((DX - 0.5, DY - 2.0), (DX + 0.9, DY - 3.6))):
        trooper(f"T{i}", x, y, -90, walk=1.25, phase=i)
    cam = push((DX + 5.5, DY - 11, 1.5), (DX, DY - 3, 1.5), 0.08, lens=35)
    kit.depth_of_field(cam, focus=9.5, fstop=2.8)
elif V == "arriving":
    c3, l3 = rt.police_car(m, (30, -40, 0), 0, name="Arriving")
    kit.key(c3, "location", [(1, (30, -42, 0)), (N, (29.2, -30, 0))], ease="out")
    kit.key(c3, "rotation_euler", [(1, (0, 0, math.radians(180))), (N, (0, 0, math.radians(172)))], ease="out")
    cam = push((16, -27, 0.8), (29, -36, 0.9), 0.06, lens=30, aim1=(29, -31, 0.9))
elif V == "to_car":
    h = facing((DX + 1.5, DY - 4), CAR)
    T = trooper("Dickson", DX + 1.5, DY - 4, h, walk=1.25)
    hx, hy = math.cos(math.radians(h)), math.sin(math.radians(h))
    d = 1.25 * DUR
    p0 = (DX + 1.5 - hx * 3.4 - hy * 0.7, DY - 4 - hy * 3.4 + hx * 0.7, 1.72)
    cam = kit.camera(p0, look_at=(CAR[0], CAR[1], 1.0), lens=32)
    kit.key(cam, "location", [(1, p0), (N, (p0[0] + hx * d * 1.12, p0[1] + hy * d * 1.12, 1.72))], ease="linear")   # follows him toward the car
    kit.depth_of_field(cam, focus=3.5, fstop=3.2)
elif V in ("cruiser", "cruiser2"):
    kit.light("AREA", (CAR[0] - 2.4, CAR[1] + 4.2, 2.6), (CAR[0], CAR[1], 0.9), power=150, color=rt.AMBER, size=2.2, name="CruiserRim").data.specular_factor = 0.8
    if V == "cruiser":
        cam = push((CAR[0] + 9, CAR[1] - 12, 1.5), (CAR[0], CAR[1], 0.9), 0.07, lens=35, slide=(-1.2, 0, 0))
    else:
        cam = push((CAR[0] - 4.6, CAR[1] - 4.4, 1.15), (CAR[0], CAR[1] - 0.4, 1.0), 0.06, lens=40, slide=(0, 0.9, 0.1))
        kit.depth_of_field(cam, focus=5.5, fstop=2.8)
elif V in ("treeline", "treeline2"):
    x0 = 0 if V == "treeline" else -18
    cam = kit.camera((x0, -14, 1.7), look_at=(x0 + 5, -62, 3.2), lens=40)       # locked off: an impact is light, not a camera move
    flash((x0 + 6, -59.6, 1.7), S["flash_at"])          # just inside the edge of the trees, where it can be seen
elif V == "front":
    cam = push((12, -32, 1.6), (-6, -9, 2.2), 0.05, lens=30)
elif V == "four":
    spots = ((19.0, -20.5, 70), (21.6, -21.6, 110), (23.6, -19.6, 200), (17.6, -22.6, 30))
    for i, (x, y, h) in enumerate(spots):
        trooper(f"T{i}", x, y, h)
    cam = push((31, -31, 1.6), (21, -20.5, 1.3), 0.07, lens=35)
    kit.depth_of_field(cam, focus=14, fstop=3.2)
elif V == "bag":
    T = trooper("Douglass", 16.5, -11.5, -90, walk=1.2)
    bag = clay.box(0.26, 0.5, 0.28, (0, -0.36, 0.86), kit.matte("#22252B", 0.8, "GymBag"), "GymBag")
    rt._on_body(T, bag, "hand.R")
    d = 1.2 * DUR
    cam = kit.camera((18.6, -14.4, 0.8), look_at=(16.35, -11.9, 0.78), lens=40)
    kit.key(cam, "location", [(1, (18.6, -14.4, 0.8)), (N, (18.3, -14.4 - d * 0.85, 0.82))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (16.35, -11.9, 0.78)), (N, (16.35, -11.9 - d, 0.78))], ease="linear")
    kit.depth_of_field(cam, focus=3.3, fstop=2.8)
    key = kit.light("AREA", (19.5, -15.5, 3.0), (16.4, -12.5, 0.8), power=320, color="#DCE6FF", size=2.5, name="BagKey")   # travels with him
    kit.key(key, "location", [(1, (19.5, -15.5, 3.0)), (N, (19.5, -15.5 - d, 3.0))], ease="linear")
elif V == "notice":
    T = trooper("Douglass", 19.2, -19.4, -90)
    rt.rpose(T, {"upper_arm.L": (4, 0, -24), "upper_arm.R": (4, 0, 24), "forearm.L": (14, 0, 0), "forearm.R": (14, 0, 0),
                 "spine.004": (0, -38, 0), "spine.005": (0, -30, 0)})          # head turned toward the building
    cam = push((21.4, -24.2, 1.7), (19.2, -19.4, 1.62), 0.09, lens=50)
    kit.depth_of_field(cam, focus=5.2, fstop=2.8)
    kit.light("AREA", (22.5, -23, 3.2), (19.2, -19.4, 1.5), power=260, color="#DCE6FF", size=2.5, name="FaceKey")
elif V == "lobby":
    cam = push((DX + 2.2, DY - 12, 1.5), (DX, DY, 1.35), 0.1, lens=35)
elif V == "doorway":
    for i, dx in enumerate((-0.55, 0.5)):                                    # two troopers in the doorway, backs to the camera
        T = trooper(f"T{i}", DX + dx, DY - 0.9, 90)
        rt.rpose(T, "kneel")
        T["root"].location = (DX + dx, DY - 0.9, -rt.RDROP["kneel"])
    cam = push((DX + 1.4, DY - 6.2, 1.15), (DX, DY - 0.6, 1.0), 0.1, lens=40)
elif V == "pages":
    # object: the torn notebook pages, on a table under a lamp (their wording is typed in the next shots, not drawn here)
    bx, by = 150.0, 150.0
    clay.box(2.4, 1.4, 0.08, (bx, by, 0.76), kit.matte("#1B1E24", 0.5, "Table"), "Table", bevel=False)
    paper = kit.matte("#D8D2C2", 0.9, "Paper")
    ink = kit.matte("#3B4254", 0.9, "Ink")
    prn = random.Random(2)
    for i, (px, py, rz) in enumerate(((-0.34, 0.03, 9), (0.02, -0.04, -6), (0.38, 0.06, 14))):
        pg = clay.box(0.3, 0.42, 0.004, (bx + px, by + py, 0.805 + i * 0.004), paper, "Page", rot=(0, 0, rz), bevel=False)
        for k in range(11):                                                # ruled handwriting as strokes: not legible on purpose
            w = prn.uniform(0.12, 0.25)
            ln = clay.box(w, 0.006, 0.001, (0, 0, 0), ink, "Line", bevel=False)
            ln.parent = pg
            ln.location = (-0.135 + w / 2, 0.17 - k * 0.032, 0.004)
    kit.light("SPOT", (bx - 0.6, by - 0.5, 1.9), (bx, by, 0.8), power=220, color="#FFE9C8", size=0.4, name="DeskLamp")
    cam = push((bx + 0.9, by - 1.25, 1.42), (bx, by, 0.8), 0.12, lens=45, slide=(-0.25, 0, 0))
    kit.depth_of_field(cam, focus=1.6, fstop=2.8)
elif V == "wide":
    cam = push((-30, -57, 2.2), (0, -6, 3), 0.05, lens=30)
elif V == "vanish":
    # whoever fired is the one amber figure, going back into the trees across the road (no weapon drawn)
    man = rt.real_mannequin("Subject", (5, -58.5, 0), -90, amber, subsurf=2)
    rt.beanie(man)
    rt.rwalk_cycle(man, 1, N, period=34)
    d = 1.3 * DUR
    kit.key(man["root"], "location", [(1, (5, -58.5, 0)), (N, (5, -58.5 - d, 0))], ease="linear")
    cam = kit.camera((6.4, -50.5, 1.6), look_at=(5, -59, 1.35), lens=40)
    kit.key(cam, "location", [(1, (6.4, -50.5, 1.6)), (N, (6.0, -51.6, 1.6))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (5, -59, 1.35)), (N, (5, -59 - d, 1.35))], ease="linear")
    kit.light("AREA", (5, -56, 6), (5, -60, 1.2), power=2600, color="#C9D6F2", size=6, name="EdgeLight").data.specular_factor = 0.0

if ST:
    stamp(cam, ST["line"], ST.get("at"), ST.get("sub"))
cam.data.clip_end = 3000
kit.shake(cam, strength=0.005, speed=50)
kit.post(bloom=0.35, vignette=0.45, grain=0.02)
