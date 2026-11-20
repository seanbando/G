"""Frein cold open v2 (VO 0:00-0:52.8), built to the measured Retraced rules (saylo/channel/retraced-frame-analysis.md):
hard cuts only, every 3D shot pushes in 4-17% of the frame per second, each place is shot from several sides,
object close-ups, text on a surface of the set, one travelling move. 39 shots in shots2.json, cut on vo-words.json.
  powershell -File saylo/videos/02-frein/build/style-test/build.ps1 -Cfg shots2.json
SCHEMATIC SET: OpenStreetMap has the roads here but not the airstrip, hangar or resort, so their layout is an
illustration. Grey mannequins = marshals, the amber one = Frein. Nobody is shown being hit. No weapons are drawn.
"""
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
SHOT = int(a.get("shot") or 1)
CFG = json.load(open(os.path.join(HERE, a.get("cfg") or "shots2.json"), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == SHOT)
T0 = S["start"]
SHOT = int(S.get("as", SHOT))                          # a later chapter can reuse a camera set-up by number
N = a.frames
FPS = CFG["fps"]
DUR = (N - 1) / FPS
AERIAL = SHOT in (1, 2, 11, 26)
WOODS_SHOT = SHOT in (119, 120)                       # he is alone in the woods


def f(vo_time):
    return kit.f(vo_time - T0)


kit.setup(world=rt.NAVY, view="AgX", look="Medium High Contrast", bloom=0.25, motion_blur=0.3)
rt.sky("evening_road_01_puresky", strength=0.3, rot_z=200, sat=0.8)
kit.light("SUN", (-200, 40, 120), (0, 0, 0), power=0.45, color="#B9C8EC", name="SkyKey")

# ------------------------------------------------------------------ materials (CC0 scans, pulled toward grey)
ground = rt.pbr("forest_ground_04", scale=5.0, sat=0.45)
conc = rt.pbr("cracked_concrete", scale=5.0, sat=0.35)
floor = rt.pbr("hangar_concrete_floor", scale=4.0, sat=0.35)
iron = rt.pbr("corrugated_iron_02", scale=2.2, sat=0.3)
asph = rt.pbr("asphalt_02", scale=4.0, sat=0.2)


def brighten(mat, value):
    for nd in mat.node_tree.nodes:
        if nd.type == "HUE_SAT":
            nd.inputs["Value"].default_value = value
    return mat


# the real hangar (Reuters photo, WNEP aerial): white corrugated metal, pale grey roof, dark green trim
wall_w = brighten(rt.pbr("corrugated_iron_02", scale=2.2, sat=0.06, name="WhiteIron"), 2.3)
roof_g = brighten(rt.pbr("corrugated_iron_02", scale=2.2, sat=0.06, name="RoofIron"), 1.6)
green = kit.matte("#34513F", 0.7, "GreenTrim")
brick = rt.pbr("brick_wall_08", scale=2.0, sat=0.45)
steel = kit.matte("#3B3F45", 0.5, "Steel")
paint = kit.matte("#B8B5AC", 0.9, "FadedPaint")
white = rt.gloss(rt.WHITE, 0.24, 0.7, "MannequinGloss")
amber = rt.gloss(rt.SUBJECT, 0.14, 1.0, "SubjectGloss2")

kit.rect(1600, 1600, material=ground, loc=(0, 0, 0), rot=(0, 0, 0), name="Ground")
clay.box(18, 520, 0.06, (0, 0, 0.03), asph, "Runway", bevel=False)
clay.box(52, 44, 0.06, (-13, 30, 0.025), asph, "Apron", bevel=False)      # the cracked asphalt lot in front of the doors
for y in range(-240, 250, 30):
    clay.box(0.4, 9, 0.012, (0, y, 0.066), paint, "Dash", bevel=False)
for sx in (-8.2, 8.2):
    clay.box(0.25, 500, 0.012, (sx, 0, 0.066), paint, "Edge", bevel=False)

# ------------------------------------------------------------------ hangar, rebuilt from the real one
# (Reuters exterior photo + WNEP aerial, creator files of Nov 19): a white corrugated shed with a low pitched roof,
# the big doors in the gable end (here facing +X, toward the strip), small windows down the long sides, green trim.
# No windsock: nothing in the record shows one here, and the real aerial now covers that line.
HX, HY, HW, HD, HH, RIDGE = -50, 30, 30, 26, 6.0, 2.3
FX = HX + HD / 2
clay.box(HD, HW, 0.08, (HX, HY, 0.04), floor, "HangarFloor", bevel=False)
clay.box(0.25, HW, HH, (HX - HD / 2, HY, HH / 2), wall_w, "Back", bevel=False)
for sy in (-1, 1):
    clay.box(HD, 0.25, HH, (HX, HY + sy * HW / 2, HH / 2), wall_w, "Side", bevel=False)
    clay.box(0.25, 4.6, HH, (FX, HY + sy * (HW / 2 - 2.3), HH / 2), wall_w, "Front", bevel=False)
    clay.box(HD + 1.2, 0.18, 0.22, (HX + 0.1, HY + sy * (HW / 2 + 0.2), HH - 0.02), green, "EaveTrim", bevel=False)
    clay.box(0.2, 0.3, HH, (FX + 0.05, HY + sy * (HW / 2 - 0.02), HH / 2), green, "CornerTrim", bevel=False)
    rt._strut((FX + 0.2, HY + sy * (HW / 2 + 0.25), HH + 0.02), (FX + 0.2, HY, HH + RIDGE + 0.05), 0.13, green, "Rake")
slab = [(-HW / 2 - 0.45, HH), (0, HH + RIDGE), (HW / 2 + 0.45, HH), (HW / 2 + 0.45, HH - 0.14), (0, HH + RIDGE - 0.14), (-HW / 2 - 0.45, HH - 0.14)]
rt._loft("Roof", [[(x, HY + y, z) for y, z in slab] for x in (HX - HD / 2 - 0.5, FX + 0.6)], mats=[roof_g])
tri = [(-HW / 2, HH - 0.05), (0, HH + RIDGE - 0.1), (HW / 2, HH - 0.05)]
for gx in (FX, HX - HD / 2):
    rt._loft("Gable", [[(x, HY + y, z) for y, z in tri] for x in (gx - 0.12, gx + 0.12)], mats=[wall_w])
clay.box(0.3, HW - 9.2, 0.5, (FX, HY, HH - 0.25), wall_w, "Lintel", bevel=False)
clay.box(0.05, 3.0, 0.9, (FX + 0.16, HY - 9.5, HH + 0.35), green, "GableSign", bevel=False)
clay.box(0.12, HW, 0.14, (FX + 0.25, HY, HH - 0.6), green, "DoorRail", bevel=False)
for y0, w in ((HY - 7.9, 5.0), (HY + 2.6, 5.0), (HY + 7.9, 5.0)):      # four leaves, one slid aside
    clay.box(0.1, w, HH - 0.7, (FX + 0.25, y0, (HH - 0.7) / 2), wall_w, "DoorLeaf", bevel=False)
    for dy in (-w / 2 + 0.05, w / 2 - 0.05):
        clay.box(0.14, 0.12, HH - 0.7, (FX + 0.25, y0 + dy, (HH - 0.7) / 2), green, "DoorFrame", bevel=False)
for fx in range(-10, 11, 5):                                            # steel frame inside, so the dark interior has depth
    for sy in (-1, 1):
        clay.box(0.18, 0.18, HH, (HX + fx, HY + sy * (HW / 2 - 0.25), HH / 2), steel, "Post", bevel=False)
        rt._strut((HX + fx, HY + sy * (HW / 2 - 0.25), HH), (HX + fx, HY, HH + RIDGE - 0.3), 0.09, steel, "Rafter")
# windows and a door along the long sides (the north wall keeps a clear stretch where the quote is typed)
glass = kit.matte("#0A0D12", 0.15, "WinGlass")
for sy in (-1, 1):
    xs = [HX - 11 + 3.1 * i for i in range(8)] if sy < 0 else [HX - 11, HX - 7.9]
    for wx in xs:
        clay.box(1.25, 0.1, 1.05, (wx, HY + sy * (HW / 2 + 0.1), 1.95), glass, "Window", bevel=False)
        clay.box(1.45, 0.06, 1.25, (wx, HY + sy * (HW / 2 + 0.08), 1.95), green, "WinFrame", bevel=False)
    clay.box(1.0, 0.1, 2.1, (HX - 12.3 if sy > 0 else HX + 11.6, HY + sy * (HW / 2 + 0.1), 1.05), green, "SideDoor", bevel=False)
kit.light("AREA", (HX + 4, HY, 5.6), (HX + 2, HY, 0), power=40, color="#8FA6D8", size=9, name="HangarSpill")
kit.light("AREA", (FX + 32, HY - 20, 14), (FX, HY, 4), power=9000, color="#AFC0E6", size=25, name="HangarFace").data.specular_factor = 0.3

# the resort block, north end (only where it is seen)
if SHOT in (1, 2, 14):
    dark = kit.matte("#07090C", 0.3, "WinDark")
    for (sx, sy, sz, x, y) in ((64, 18, 9.5, -62, 178), (18, 40, 7, -100, 168), (22, 14, 5, -22, 172)):
        clay.box(sx, sy, sz, (x, y, sz / 2), brick, "Resort", bevel=False)
        clay.box(sx + 0.8, sy + 0.8, 0.35, (x, y, sz + 0.17), steel, "ResortRoof", bevel=False)
        for wz in range(1, int(sz) - 1, 3):
            nx = int(sx // 3.2)
            for i in range(nx):
                wx = x - sx / 2 + 1.8 + i * (sx - 3.6) / max(1, nx - 1)
                clay.box(1.5, 0.12, 1.7, (wx, y - sy / 2 - 0.02, wz + 1.0), dark, "Win", bevel=False)
                clay.box(1.7, 0.16, 0.1, (wx, y - sy / 2 - 0.03, wz + 0.1), paint, "Sill", bevel=False)
    clay.box(70, 26, 0.05, (-60, 152, 0.02), conc, "ResortLot", bevel=False)

# ------------------------------------------------------------------ woods and grass
_W = rt.autumn_woods()
WOODS, SHRUBS = _W[:-2], _W[-2:]                      # trees, and low undergrowth for the foot of a tree line
rnd = random.Random(4)


def clearing(x, y):
    return (abs(x) < 34 and abs(y) < 320) or (-92 < x < 0 and -60 < y < 73) or (-120 < x < 0 and 135 < y < 215)


placed, want, ext = 0, (8500 if SHOT in (1, 2) else 2600), (520 if SHOT in (1, 2) else 300)
KEEP_OUT = 30.0 if SHOT in (22, 23, 24, 25, 119, 120) else 6.5   # simple trees stay away from the scanned ones
while placed < want:
    x, y = rnd.uniform(-ext, ext * 0.9), rnd.uniform(-ext * 0.9, ext)
    if clearing(x, y) or (x + 46) ** 2 + (y - 80) ** 2 < KEEP_OUT ** 2:
        continue                                      # the gap he walks out of stays open
    WOODS[rnd.randrange(len(WOODS))]((x, y, 0), rnd.uniform(0, 360), rnd.uniform(11, 19))
    placed += 1
CLOSE_TREES = SHOT in (22, 23, 24, 25, 119, 120)                # the camera is near the tree line: scanned trees there
for i in range(34):                                   # a full tree line along the north edge of the hangar field
    x = -94 + i * 2.9 + rnd.uniform(-0.8, 0.8)
    if -50.5 < x < -41.5 or (CLOSE_TREES and -66 < x < -26):
        continue
    WOODS[rnd.randrange(len(WOODS))]((x, 76 + rnd.uniform(0, 3.5), 0), rnd.uniform(0, 360), rnd.uniform(12, 18))
    SHRUBS[i % 2]((x + rnd.uniform(-1, 1), 74.2 + rnd.uniform(0, 1.2), 0), rnd.uniform(0, 360), rnd.uniform(11, 17))

if CLOSE_TREES:
    # real scanned firs and pines with their needles (CC0, Poly Haven) around the gap he walks out of
    HERO = rt.tree_library("trees_mid.blend")
    for name, x, y, rz, h in (("FirMid", -56.5, 79.0, 20, 19), ("PineMid", -36.5, 80.5, 200, 21), ("FirMid", -30.0, 78.0, 110, 17),
                              ("PineMid", -64.0, 81.0, 70, 20), ("FirMid", -46.5, 92.0, 250, 18), ("PineMid", -40.0, 96.0, 320, 20)):
        HERO[name]((x, y, 0), rz, h)

GX, GY = -46.0, 54.0                                  # where he ends up on the ground
ZONES = {3: (-9, 9, -80, -30), 4: (-40, 8, 8, 44), 5: (6, 22, 38, 56), 6: (-38, -26, 20, 40),
         9: (4, 32, -66, -44), 10: (2, 32, -62, -48), 13: (18.8, 30, -56, -40), 15: (-9, 9, -64, 0),
         16: (10, 26, -46, -30), 17: (4, 32, -56, -20), 18: (-20, -4, 24, 36), 20: (-40, 4, 18, 42),
         21: (-30, -8, 22, 40), 22: (-34, -12, 26, 60), 23: (-56, -34, 44, 80), 24: (-54, -38, 58, 80),
         25: (-56, -46.9, 62, 76), 29: (-52, -40, 46, 68), 30: (-54, -40, 45, 64), 31: (-54, -40, 45, 62),
         32: (-53, -39, 46, 60), 33: (-53, -38, 48, 60), 34: (-53, -39, 48, 60), 35: (-54, -39, 48, 61),
         36: (-60, -32, 40, 68), 119: (-56, -36, 62, 92), 120: (-56, -46.9, 62, 80), 37: (-52, -40, 46, 58), 38: (-53, -39, 47, 61)}
if SHOT in ZONES:
    grass = rt.instancer("grass_medium_01", sat=0.4)
    grass2 = rt.instancer("grass_medium_02", sat=0.4)
    z = ZONES[SHOT]
    PRONE = SHOT >= 34
    for _ in range(1500):
        x, y = rnd.uniform(z[0], z[1]), rnd.uniform(z[2], z[3])
        on_concrete = (abs(x) < 9) or (-46 < x < 0 and 22 < y < 38)
        if on_concrete and rnd.random() < 0.88:
            continue                                   # a few weeds through the cracks only
        if -63.2 < x < -36.8 and 14.8 < y < 45.2:
            continue                                   # not inside the hangar
        if PRONE and (x - GX) ** 2 + (y - GY) ** 2 < (9.0 if SHOT == 36 else 3.6) ** 2:      # the grass model is a spread of clumps metres wide: keep it well away from the hand close-up
            continue                                   # flattened where he lies
        (grass if rnd.random() < 0.6 else grass2)((x, y, 0.02), rnd.uniform(0, 360), rnd.uniform(0.9, 2.2))
if not AERIAL:
    rt.haze((-30, 40, 14), (340, 340, 28), density=0.0048)


# ------------------------------------------------------------------ people
def facing(frm, to):
    return math.degrees(math.atan2(to[1] - frm[1], to[0] - frm[0]))


def marshal(name, x, y, heading, walk=None, phase=0):
    M = rt.real_mannequin(name, (x, y, 0), heading, white, subsurf=2)
    rt.marshal_kit(M, name)
    if walk:
        d = walk * DUR
        hx, hy = math.cos(math.radians(heading)), math.sin(math.radians(heading))
        kit.key(M["root"], "location", [(1, (x, y, 0)), (N, (x + d * hx, y + d * hy, 0))], ease="linear")
        rt.rwalk_cycle(M, 1, N, period=32, phase=phase)
    else:
        rt.rpose(M, "relaxed")
    return M


def subject(y0, walk=1.25):
    """Frein, walking south from the tree line toward the hangar (x = -46). y0 = where he is when the shot starts."""
    M = rt.real_mannequin("Subject", (GX, y0, 0), -90, amber, subsurf=2)
    rt.beanie(M)
    if walk:
        rt.rwalk_cycle(M, 1, N, period=34)
        kit.key(M["root"], "location", [(1, (GX, y0, 0)), (N, (GX, y0 - walk * DUR, 0))], ease="linear")
    else:
        rt.rpose(M, "relaxed")
    return M


def push(p0, aim, rate, lens=35, slide=(0.0, 0.0, 0.0), aim1=None, ease="linear"):
    """Camera that dollies toward `aim` so the picture grows by `rate` (0.07 = 7%) per second, plus a slide."""
    k = 1.0 - 1.0 / (1.0 + rate * DUR)
    p1 = tuple(p0[i] + (aim[i] - p0[i]) * k + slide[i] for i in range(3))
    cam = kit.camera(p0, look_at=aim, lens=lens)
    kit.key(cam, "location", [(1, p0), (N, p1)], ease=ease)
    if aim1:
        kit.key(kit.aim(cam), "location", [(1, aim), (N, aim1)], ease=ease)
    return cam


def stamp(cam, line, t_line, sub=None, t_sub=None):
    """Date stamp top-left, typed on at the voiceover times (a time before the shot = already there)."""
    h, hw, hh = rt.hud(cam, 4.0)
    size = hh * 0.2
    x, y = -hw + hw * 0.07, hh - hh * 0.24
    t = kit.text(line, font="Montserrat-Bold", size=size, spacing=1.05, color="#FFFFFF", strength=1.7, align="LEFT",
                 loc=(x, y, 0), rot=(0, 0, 0), name="Stamp")
    kit.parent(t, h)
    rt.typed(t, f(t_line))
    sh = kit.text(line, font="Montserrat-Bold", size=size, spacing=1.05, color="#000000", strength=0.0, align="LEFT",
                  loc=(x + size * 0.035, y - size * 0.035, -0.004), rot=(0, 0, 0), name="StampShadow")
    kit.parent(sh, h)
    rt.typed(sh, f(t_line), cursor=False)
    if sub:
        s = kit.text(sub, font="Montserrat-Bold", size=size * 0.38, spacing=1.2, color=rt.AMBER, strength=1.6, align="LEFT",
                     loc=(x, y - size * 0.85, 0), rot=(0, 0, 0), name="StampSub")
        kit.parent(s, h)
        rt.typed(s, f(t_sub), cursor=False)
        s2 = kit.text(sub, font="Montserrat-Bold", size=size * 0.38, spacing=1.2, color="#000000", strength=0.0, align="LEFT",
                      loc=(x + size * 0.02, y - size * 0.85 - size * 0.02, -0.004), rot=(0, 0, 0), name="StampSubShadow")
        kit.parent(s2, h)
        rt.typed(s2, f(t_sub), cursor=False)


LINE_X = (8, 13, 18, 23, 28)                           # the team in a line, working north up the field east of the runway
LINE_T0, LINE_Y0 = 10.10, -62.0                        # where the line is at VO 10.10 s (1.3 m/s north)
TRIO = ((0.0, 0.0), (2.4, 2.5), (2.8, -2.4))           # Malkowski + two, offsets behind him; they walk west along the apron
TRIO_T0, TRIO_X0 = 25.0, -13.0
DATE = ("OCT 30, 2014", "6:07 PM  ·  NEAR TANNERSVILLE, PA")


def team_line():
    y = LINE_Y0 + 1.3 * (T0 - LINE_T0)
    return [marshal(f"M{i}", x, y - (i % 2) * 1.5, 90, walk=1.3, phase=i) for i, x in enumerate(LINE_X)], y


def trio(walk=True):
    x = TRIO_X0 - 1.3 * (T0 - TRIO_T0)
    return [marshal(f"M{i}", x + dx, 30 + dy, 180, walk=1.3 if walk else None, phase=i) for i, (dx, dy) in enumerate(TRIO)], x


def sub_y(t):
    """His y at VO time t: leaves the trees (y = 78) at about 31.4 s, walks 1.25 m/s, stops at GY."""
    return max(GY, 78.0 - 1.25 * (t - 31.4))


cam = None
dof = None

if SHOT == 1:
    cam = push((200, -440, 210), (-25, 40, 0), 0.14, lens=30)
    stamp(cam, DATE[0], 0.15)
elif SHOT == 2:
    cam = push((46, -280, 52), (-28, 30, 4), 0.16, lens=30)
    stamp(cam, DATE[0], 0.15)
elif SHOT == 3:
    cam = push((0.9, -79, 0.32), (0.2, -40, 0.25), 0.22, lens=24, aim1=(0.2, -30, 0.6))
    kit.depth_of_field(cam, focus=6, fstop=4)
    stamp(cam, DATE[0], 0.15)
elif SHOT == 4:
    cam = push((5, 10, 1.3), (FX, HY, 4.2), 0.09, lens=28, slide=(0, 0, 0.5))
    stamp(cam, DATE[0], -9, DATE[1], 3.5)
elif SHOT == 6:
    cam = push((-30.5, 25.5, 1.5), (FX + 0.25, HY + 3.2, 3.2), 0.14, lens=35, slide=(0, 0.6, 0.15))
    kit.depth_of_field(cam, focus=8.5, fstop=2.8)
    kit.light("AREA", (-33, 28, 3.5), (FX, HY + 4, 3), power=260, color="#B9C8EC", size=4, name="DoorKey").data.specular_factor = 0.4

elif SHOT == 9:
    Ms, y = team_line()
    cam = push((18.6, y + 7.5, 0.9), (18, y + 1, 1.35), 0.05, lens=22, slide=(0.3, 0, 0.05))
    kit.depth_of_field(cam, focus=6.5, fstop=2.8)
    kit.key(cam.data.dof, "focus_distance", [(1, 6.6), (N, 4.4)], ease="linear")
elif SHOT == 10:
    Ms, y = team_line()
    d = 1.3 * DUR
    cam = kit.camera((3.6, y + 1.0, 1.4), look_at=(13, y + 0.4, 1.35), lens=40)
    kit.key(cam, "location", [(1, (3.6, y + 1.0, 1.4)), (N, (4.6, y + 1.0 + d, 1.42))], ease="linear")      # tracks with them, creeping in
    kit.key(kit.aim(cam), "location", [(1, (13, y + 0.4, 1.35)), (N, (13, y + 0.4 + d, 1.35))], ease="linear")
    kit.depth_of_field(cam, focus=9.0, fstop=2.8)
elif SHOT == 11:
    Ms, y = team_line()
    cam = push((-7, y - 15, 12), (18, y + 3, 0.5), 0.11, lens=40)             # from over the strip: no trees between camera and team
elif SHOT == 13:
    Ms, y = team_line()
    d = 1.3 * DUR
    cam = kit.camera((16.6, y + 1.9, 0.42), look_at=(18.1, y + 0.6, 0.5), lens=35)
    kit.key(cam, "location", [(1, (16.6, y + 1.9, 0.42)), (N, (16.8, y + 1.9 + d * 0.8, 0.44))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (18.1, y + 0.6, 0.5)), (N, (18.1, y + 0.6 + d, 0.5))], ease="linear")
    kit.depth_of_field(cam, focus=1.9, fstop=2.8)
elif SHOT == 14:
    cam = push((-4, 118, 2.0), (-62, 170, 5.5), 0.11, lens=30, slide=(0, 0, 0.4))
elif SHOT == 15:
    cam = kit.camera((0.5, -62, 0.3), look_at=(0, 200, 1.5), lens=20)
    kit.key(cam, "location", [(1, (0.5, -62, 0.3)), (N, (0.5, -32, 0.45))], ease="linear")                 # fast and low down the strip
elif SHOT == 16:
    Ms, y = team_line()
    d = 1.3 * DUR
    cam = kit.camera((17.5, y - 1.9, 1.7), look_at=(18.05, y + 0.1, 1.56), lens=50)                     # helmet, shoulders and the back of the vest
    kit.key(cam, "location", [(1, (17.5, y - 1.9, 1.7)), (N, (17.55, y - 1.6 + d, 1.7))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (18.05, y + 0.1, 1.56)), (N, (18.05, y + 0.1 + d, 1.56))], ease="linear")
    kit.depth_of_field(cam, focus=2.0, fstop=2.8)
elif SHOT == 17:
    Ms, y = team_line()
    cam = push((19, y - 13, 2.3), (6, y + 60, 2.6), 0.06, lens=28, slide=(0, 0, 0.3))
    stamp(cam, "ABOUT 2 HOURS IN", 20.1, "CLEARING THE PROPERTY", 20.75)
elif SHOT == 18:
    Ms, x = trio()
    d = 1.3 * DUR
    cam = kit.camera((x - 3.6, 31.3, 1.62), look_at=(x, 30, 1.72), lens=60)
    kit.key(cam, "location", [(1, (x - 3.6, 31.3, 1.62)), (N, (x - 3.1 - d, 31.2, 1.64))], ease="linear")   # backs away slower than he walks: he grows
    kit.key(kit.aim(cam), "location", [(1, (x, 30, 1.72)), (N, (x - d, 30, 1.72))], ease="linear")
    kit.depth_of_field(cam, focus=3.6, fstop=2.2)
    kit.key(cam.data.dof, "focus_distance", [(1, 3.8), (N, 3.3)], ease="linear")

elif SHOT == 20:
    Ms, x = trio()
    d = 1.3 * DUR
    cam = kit.camera((x + 9.5, 31.2, 0.7), look_at=(FX, HY, 3.0), lens=26)
    kit.key(cam, "location", [(1, (x + 9.5, 31.2, 0.7)), (N, (x + 9.5 - d * 1.9, 30.6, 1.35))], ease="linear")
    kit.depth_of_field(cam, focus=8.5, fstop=2.8)
elif SHOT == 21:
    Ms, x = trio()
    d = 1.3 * DUR
    cam = push((x - 9.5, 34.6, 1.25), (x - d * 0.5, 30, 1.45), 0.07, lens=40, aim1=(x - d, 30, 1.45))
    kit.depth_of_field(cam, focus=9.5, fstop=2.8)
    kit.key(cam.data.dof, "focus_distance", [(1, 10.2), (N, 7.2)], ease="linear")
elif SHOT == 22:
    Ms, x = trio(walk=False)                           # they have stopped
    for M in Ms:
        M["root"].rotation_euler = (0, 0, math.radians(facing((x, 30), (GX, 78))))
    hx_, hy_ = x, 30.0
    cam = push((hx_ + 0.75, hy_ - 2.3, 1.84), (hx_ - 5.5, hy_ + 20, 2.3), 0.035, lens=50, slide=(0.12, 0, 0))
    kit.depth_of_field(cam, focus=2.45, fstop=2.0)
    kit.key(cam.data.dof, "focus_distance", [(1, 2.45), (N, 30.0)], ease="in_out")                         # rack from the helmet to the trees
elif SHOT == 23:
    man = subject(sub_y(T0))                           # still inside the trees
    cam = push((-40.5, 46, 1.7), (GX, 80, 2.2), 0.09, lens=45, slide=(-0.6, 0, 0))
    kit.light("AREA", (GX, 72, 7), (GX, 80, 1.2), power=420, color="#C9D6F2", size=6, name="GapLight").data.specular_factor = 0.0
elif SHOT == 24:
    man = subject(sub_y(T0))
    cam = kit.camera((-44.6, 62.5, 0.55), look_at=(GX, 79, 1.5), lens=40)
    kit.key(cam, "location", [(1, (-44.6, 62.5, 0.55)), (N, (-45.1, 66.3, 1.05))], ease="linear")
    kit.depth_of_field(cam, focus=14, fstop=2.0)
    kit.key(cam.data.dof, "focus_distance", [(1, 17.0), (N, 11.5)], ease="linear")
    kit.light("AREA", (GX, 70, 7), (GX, 78, 1.2), power=420, color="#C9D6F2", size=6, name="GapLight").data.specular_factor = 0.0
elif SHOT == 25:
    y0 = 72.5                                          # clear of the trunks at the gap
    man = subject(y0)
    d = 1.25 * DUR
    cam = kit.camera((-43.4, y0 - 1.5, 0.5), look_at=(GX, y0 - 0.3, 0.55), lens=35)
    kit.key(cam, "location", [(1, (-43.4, y0 - 1.5, 0.5)), (N, (-43.9, y0 - 1.5 - d * 0.7, 0.52))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (GX, y0 - 0.3, 0.55)), (N, (GX, y0 - 0.3 - d, 0.55))], ease="linear")
    kit.depth_of_field(cam, focus=2.9, fstop=2.8)
elif SHOT == 26:
    y0 = sub_y(T0)
    man = subject(y0)
    for i, (dx, dy) in enumerate(TRIO):
        marshal(f"M{i}", -27 + dx, 47 + dy * 0.8, facing((-27, 47), (GX, y0)))
    cam = push((-21, 43.5, 4.6), (-44, 64, 1.0), 0.1, lens=45, slide=(0, 0.8, 0))

elif SHOT == 29:
    y0 = 62.0                                          # (the walk is shortened between cuts: 29-31 are close to the hangar)
    man = subject(y0)
    d = 1.25 * DUR
    cam = kit.camera((GX + 0.5, y0 + 4.2, 1.8), look_at=(GX, y0, 1.72), lens=45)
    kit.key(cam, "location", [(1, (GX + 0.5, y0 + 4.2, 1.8)), (N, (GX + 0.35, y0 + 2.9 - d, 1.82))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (GX, y0, 1.72)), (N, (GX, y0 - d, 1.78))], ease="linear")
    kit.depth_of_field(cam, focus=4.0, fstop=2.5)
    kit.key(cam.data.dof, "focus_distance", [(1, 4.2), (N, 2.9)], ease="linear")
elif SHOT in (30, 31):
    y0 = 60.5 if SHOT == 30 else 58.6
    man = subject(y0)
    d = 1.25 * DUR
    # the quote, typed on the hangar's north wall ahead of him (Retraced: quotes sit on a wall of the set)
    WY = HY + HW / 2 + 0.16
    qx = GX - 1.2
    bar = kit.rect(0.14, 2.9, rt.AMBER, loc=(qx + 4.9, WY, 3.1), rot=(90, 0, 180), name="QuoteBar")
    q1 = kit.text("“I SAW", font="Montserrat-Bold", size=1.15, spacing=1.04, color="#FFFFFF", strength=1.7, align="LEFT",
                  loc=(qx + 4.4, WY, 3.75), rot=(90, 0, 180), name="Q1")
    q2 = kit.text("THE BLACK HAT.”", font="Montserrat-Bold", size=1.15, spacing=1.04, color="#FFFFFF", strength=1.7,
                  align="LEFT", loc=(qx + 4.4, WY, 2.35), rot=(90, 0, 180), name="Q2")
    q3 = kit.text("DEPUTY U.S. MARSHAL SCOTT MALKOWSKI", font="Montserrat-Bold", size=0.3, spacing=1.2, color=rt.AMBER,
                  strength=1.6, align="LEFT", loc=(qx + 4.4, WY, 1.55), rot=(90, 0, 180), name="Q3")
    for t in (bar, q1, q2, q3):
        t.visible_shadow = False
    rt.typed(q1, f(38.6), cps=18, cursor=False)
    rt.typed(q2, f(39.66), cps=20)
    rt.typed(q3, f(40.45), cps=45, cursor=False)
    kit.fade(bar, [(f(38.5), 0.0), (f(38.62), 1.0)])
    kit.light("AREA", (GX, WY + 9, 6), (GX, WY, 3), power=1500, color="#AFC0E6", size=10, name="WallWash").data.specular_factor = 0.2
    if SHOT == 30:
        cam = kit.camera((GX + 1.7, y0 + 3.3, 1.95), look_at=(qx + 0.6, WY, 3.0), lens=32)
        kit.key(cam, "location", [(1, (GX + 1.7, y0 + 3.3, 1.95)), (N, (GX + 1.45, y0 + 2.5 - d, 1.95))], ease="linear")
    else:
        cam = kit.camera((GX + 0.95, y0 + 1.75, 1.93), look_at=(GX - 0.9, WY, 2.75), lens=40)
        kit.key(cam, "location", [(1, (GX + 0.95, y0 + 1.75, 1.93)), (N, (GX + 0.8, y0 + 1.35 - d, 1.93))], ease="linear")
        kit.light("AREA", (GX + 1.8, y0 - 0.5, 2.8), (GX, y0 - 1, 1.85), power=90, color="#C9D6F2", size=1.5, name="CapRim").data.specular_factor = 0.3

elif SHOT in (32, 33):
    man = subject(GY, walk=None)
    spots = ((GX + 3.2, GY - 3.8), (GX + 0.8, GY - 5.0), (GX - 2.6, GY - 4.4))
    for i, (x, y) in enumerate(spots):
        marshal(f"M{i}", x, y, facing((x, y), (GX, GY)))
    if SHOT == 32:
        cam = push((GX + 2.0, GY - 6.9, 1.66), (GX, GY, 1.15), 0.11, lens=30)
        kit.depth_of_field(cam, focus=7.0, fstop=3.2)
    else:
        rt.rpose(man, "relaxed", frame=1)
        rt.rpose(man, "relaxed", frame=f(42.45))
        rt.rpose(man, "kneel", frame=f(43.45), ease="in_out")
        kit.key(man["root"], "location", [(1, (GX, GY, 0)), (f(42.45), (GX, GY, 0)), (f(43.45), (GX, GY, -rt.RDROP["kneel"]))],
                ease="in_out")
        cam = push((GX + 5.6, GY + 0.9, 1.05), (GX, GY - 0.2, 0.95), 0.1, lens=40, slide=(0, -0.4, 0))
        kit.depth_of_field(cam, focus=5.5, fstop=2.8)

elif SHOT in (34, 35, 36, 37, 38):   # he is face down, head to the south, arms out, hands open and empty; marshals around him
    man = rt.real_mannequin("Subject", (GX, GY, 0), -90, amber, subsurf=2)
    rt.beanie(man)
    rt.prone(man, (GX, GY + 0.9), -90)
    ring = ((2.8, -1.7), (1.8, 1.8), (-1.7, 2.0), (-2.9, -1.4), (-0.3, -3.8))
    for i, (dx, dy) in enumerate(ring):
        marshal(f"M{i}", GX + dx, GY + dy, facing((dx, dy), (0, 0)))
    if SHOT == 34:
        cam = push((GX + 1.2, GY - 3.4, 0.55), (GX, GY - 0.6, 0.22), 0.13, lens=32)
        kit.depth_of_field(cam, focus=3.6, fstop=2.8)
    elif SHOT == 35:
        cam = push((GX - 4.6, GY + 2.6, 1.0), (GX, GY, 0.35), 0.1, lens=35, slide=(0.5, 0, 0.1))
        kit.depth_of_field(cam, focus=5.0, fstop=3.2)
    elif SHOT == 36:
        # "He isn't carrying a gun": his open, empty hand, low and close, the other arm and the marshals' boots behind
        # (the first version pushed straight down and the hand slid out of frame: creator note)
        bpy.context.view_layer.update()
        pb = man["arm"].pose.bones["hand.L"]
        hand = man["arm"].matrix_world @ ((pb.head + pb.tail) / 2)
        hx_, hy_ = hand.x, hand.y
        side = 1.0 if hx_ > GX else -1.0
        p0 = (hx_ + side * 0.7, hy_ - 0.95, hand.z + 0.42)
        cam = push(p0, (hx_ - side * 0.12, hy_, hand.z - 0.02), 0.09, lens=45, slide=(-side * 0.08, 0, -0.03))
        kit.depth_of_field(cam, focus=1.15, fstop=2.8)
        kit.key(cam.data.dof, "focus_distance", [(1, 1.18), (N, 1.0)], ease="linear")
        kit.light("AREA", (hx_ + side * 0.9, hy_ - 0.2, 1.4), (hx_, hy_, 0.2), power=45, color="#C9D6F2", size=1.2, name="HandKey").data.specular_factor = 0.5
    elif SHOT == 37:
        cam = push((GX + 1.1, GY - 0.5, 0.3), (GX - 0.3, GY - 3.8, 1.5), 0.1, lens=28, slide=(0, 0, 0.12))
        kit.depth_of_field(cam, focus=3.4, fstop=3.2)
    else:
        cam = kit.camera((GX + 1.6, GY - 4.6, 0.5), look_at=(GX, GY - 0.1, 0.35), lens=28)
        kit.key(cam, "location", [(1, (GX + 1.6, GY - 4.6, 0.5)), (N, (GX + 0.3, GY - 2.4, 8.5))], ease="in_out")   # crane up and over
        kit.depth_of_field(cam, focus=5, fstop=4)
        kit.key(cam.data.dof, "focus_distance", [(1, 4.8), (N, 8.6)], ease="in_out")

if SHOT in (119, 120):
    # the hook question: one man, alone, going back into the woods (heading north, away from the hangar)
    y0 = 70.0 if SHOT == 119 else 74.0
    man = rt.real_mannequin("Subject", (GX, y0, 0), 90, amber, subsurf=2)
    rt.beanie(man)
    rt.rwalk_cycle(man, 1, N, period=34)
    d = 1.25 * DUR
    kit.key(man["root"], "location", [(1, (GX, y0, 0)), (N, (GX, y0 + d, 0))], ease="linear")
    if SHOT == 119:
        cam = kit.camera((GX + 0.9, y0 - 7.5, 1.5), look_at=(GX, y0 + 1, 1.3), lens=40)
        kit.key(cam, "location", [(1, (GX + 0.9, y0 - 7.5, 1.5)), (N, (GX + 0.6, y0 - 5.6 + d, 1.55))], ease="linear")
        kit.key(kit.aim(cam), "location", [(1, (GX, y0 + 1, 1.3)), (N, (GX, y0 + 1 + d, 1.3))], ease="linear")
        kit.depth_of_field(cam, focus=7.5, fstop=2.8)
        kit.key(cam.data.dof, "focus_distance", [(1, 7.6), (N, 5.8)], ease="linear")
    else:
        cam = kit.camera((GX + 2.6, y0 + 1.5, 0.5), look_at=(GX, y0 + 0.3, 0.55), lens=35)
        kit.key(cam, "location", [(1, (GX + 2.6, y0 + 1.5, 0.5)), (N, (GX + 2.1, y0 + 1.5 + d * 0.7, 0.52))], ease="linear")
        kit.key(kit.aim(cam), "location", [(1, (GX, y0 + 0.3, 0.55)), (N, (GX, y0 + 0.3 + d, 0.55))], ease="linear")
        kit.depth_of_field(cam, focus=2.9, fstop=2.8)
        stamp(cam, "7 WEEKS", 83.7, "SEPT 12 \u2013 OCT 30, 2014", 84.1)
    kit.light("AREA", (GX, y0 + 2, 7), (GX, y0 + 6, 1.2), power=420, color="#C9D6F2", size=6, name="GapLight").data.specular_factor = 0.0

cam.data.clip_end = 3000
kit.shake(cam, strength=0.006, speed=50)
kit.post(bloom=0.25, vignette=0.4, grain=0.02)
