"""Frein cold open, look v2 (after the creator rejected v1): three hero shots built to sit next to the Retraced
reference frames (saylo/channel/reference/). What changed against S_airfield.py:
  real sky lighting (HDRI) instead of a flat navy wash, textured ground / concrete / corrugated metal, scanned fir and
  pine trees and grass instead of cones, glossy shop-mannequin bodies with fitted kit cut from the body mesh,
  haze for depth, and one real camera move per shot (dolly, push, crane) instead of a drift.
  --arg shot=A  three marshals walk to the hangar (VO 25.00-28.14), low dolly in behind them
  --arg shot=B  the amber figure steps out of the trees (VO 30.76-32.66), push in through the grass
  --arg shot=C  he is on the ground, marshals around him (VO 47.86-51.26), crane up and over
SCHEMATIC SET: the airstrip, hangar and tree line are an illustration (OpenStreetMap has only the roads here).
"""
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
SHOT = (a.get("shot") or "A").upper()
N = a.frames
FPS = 30

kit.setup(world=rt.NAVY, view="AgX", look="Medium High Contrast", bloom=0.25, motion_blur=0.3)
rt.sky("evening_road_01_puresky", strength=float(a.get("sky_s") or 0.3), rot_z=float(a.get("sky") or 200), sat=0.8)
kit.light("SUN", (-200, 40, 120), (0, 0, 0), power=0.45, color="#B9C8EC", name="SkyKey")      # soft top light, cool

# ------------------------------------------------------------------ materials (real CC0 scans, pulled toward grey)
ground = rt.pbr("forest_ground_04", scale=5.0, sat=0.45)
conc = rt.pbr("cracked_concrete", scale=5.0, sat=0.35)
floor = rt.pbr("hangar_concrete_floor", scale=4.0, sat=0.35)
iron = rt.pbr("corrugated_iron_02", scale=2.2, sat=0.3)
steel = kit.matte("#3B3F45", 0.5, "Steel")
white = rt.gloss(rt.WHITE, 0.24, 0.7, "MannequinGloss")
amber = rt.gloss(rt.SUBJECT, 0.14, 1.0, "SubjectGloss2")

kit.rect(1400, 1400, material=ground, loc=(0, 0, 0), rot=(0, 0, 0), name="Ground")
clay.box(18, 520, 0.06, (0, 0, 0.03), conc, "Runway", bevel=False)
clay.box(46, 16, 0.06, (-23, 30, 0.025), conc, "Apron", bevel=False)

# ------------------------------------------------------------------ hangar (door faces +X)
HX, HY, HW, HD, HH = -50, 30, 30, 26, 6.0
clay.box(HD, HW, 0.08, (HX, HY, 0.04), floor, "HangarFloor", bevel=False)
clay.box(0.25, HW, HH, (HX - HD / 2, HY, HH / 2), iron, "Back", bevel=False)
for sy in (-1, 1):
    clay.box(HD, 0.25, HH, (HX, HY + sy * HW / 2, HH / 2), iron, "Side", bevel=False)
    clay.box(0.25, 4.6, HH, (HX + HD / 2, HY + sy * (HW / 2 - 2.3), HH / 2), iron, "Front", bevel=False)
arc = [(HW / 2 * 1.005 * math.cos(math.pi * i / 28), HH + 3.4 * math.sin(math.pi * i / 28)) for i in range(29)]
roof = rt._loft("Roof", [[(x, HY + y, z) for y, z in arc] for x in (HX - HD / 2 - 0.3, HX + HD / 2 + 0.5)], mats=[iron])
gable = rt._loft("Gable", [[(x, HY + y, z) for y, z in arc] for x in (HX + HD / 2 - 0.1, HX + HD / 2 + 0.12)], mats=[iron])
clay.box(0.3, HW - 9.2, 0.5, (HX + HD / 2, HY, HH - 0.25), steel, "Lintel", bevel=False)
# sliding doors on a rail, one pushed half open; steel frames inside so the dark interior has depth
clay.box(0.12, HW, 0.14, (HX + HD / 2 + 0.25, HY, HH - 0.6), steel, "DoorRail", bevel=False)
for y0, w in ((HY - 7.6, 5.4), (HY + 6.4, 7.8)):
    clay.box(0.1, w, HH - 0.7, (HX + HD / 2 + 0.25, y0, (HH - 0.7) / 2), iron, "DoorLeaf", bevel=False)
    for dy in (-w / 2 + 0.05, w / 2 - 0.05):
        clay.box(0.14, 0.1, HH - 0.7, (HX + HD / 2 + 0.25, y0 + dy, (HH - 0.7) / 2), steel, "DoorFrame", bevel=False)
for fx in range(-10, 11, 5):
    rib = rt._loft("Rib", [[(x, HY + y * 0.985, z - 0.12) for y, z in arc] for x in (HX + fx - 0.08, HX + fx + 0.08)], mats=[steel])
    for sy in (-1, 1):
        clay.box(0.18, 0.18, HH, (HX + fx, HY + sy * (HW / 2 - 0.25), HH / 2), steel, "Post", bevel=False)
kit.light("AREA", (HX + 4, HY, 5.6), (HX + 2, HY, 0), power=40, color="#8FA6D8", size=9, name="HangarSpill")
kit.light("AREA", (HX + 45, HY - 20, 14), (HX + 13, HY, 4), power=9000, color="#AFC0E6", size=25, name="HangarFace").data.specular_factor = 0.3   # sky spill in the doorway

# ------------------------------------------------------------------ woods and grass (scanned, CC0)
T = rt.tree_library()
rnd = random.Random(4)


def clearing(x, y):
    return (abs(x) < 34 and abs(y) < 320) or (-92 < x < 0 and -60 < y < 73)


placed = 0
while placed < 300:
    x, y = rnd.uniform(-230, 190), rnd.uniform(-190, 250)
    if clearing(x, y) or (x - (-46)) ** 2 + (y - 77) ** 2 < 15 ** 2:
        continue
    T[rnd.choice(("FirLo", "PineLo", "FirLo"))]((x, y, 0), rnd.uniform(0, 360), rnd.uniform(14, 23))
    placed += 1
for i in range(26):                                   # the tree line north of the hangar field
    x = -94 + i * 3.8 + rnd.uniform(-0.8, 0.8)
    if -51.5 < x < -40.5:
        continue                                      # the gap he walks out of
    T["FirHi" if i % 2 else "PineHi"]((x, 78 + rnd.uniform(0, 4), 0), rnd.uniform(0, 360), rnd.uniform(15, 21))
if SHOT == "B":
    T["FirHi"]((-54.5, 77.5, 0), 40, 18)              # hero trees either side of the gap
    T["PineHi"]((-37.5, 78.5, 0), 200, 19)

grass = rt.instancer("grass_medium_01", sat=0.4)
grass2 = rt.instancer("grass_medium_02", sat=0.4)
ZONE = {"A": (-40, 4, 18, 42), "B": (-54, -38, 58, 80), "C": (-53, -39, 53, 67)}[SHOT]
for _ in range(1500):
    x, y = rnd.uniform(ZONE[0], ZONE[1]), rnd.uniform(ZONE[2], ZONE[3])
    if SHOT == "A" and 23.5 < y < 36.5 and rnd.random() < 0.9:
        continue                                      # the apron: only a few weeds through the cracks
    if SHOT == "C" and abs(x + 46) < 1.3 and 58.6 < y < 61.2:
        continue                                      # flattened where he lies (no blades through the body)
    (grass if rnd.random() < 0.6 else grass2)((x, y, 0.02), rnd.uniform(0, 360), rnd.uniform(0.9, 2.2))
rt.haze((-30, 40, 14), (320, 320, 28), density=0.0035)


# ------------------------------------------------------------------ people
def facing(frm, to):
    return math.degrees(math.atan2(to[1] - frm[1], to[0] - frm[0]))


def marshal(name, x, y, heading, walk=None, phase=0):
    M = rt.real_mannequin(name, (x, y, 0), heading, white, subsurf=2)
    rt.marshal_kit(M, name)
    if walk:
        d = walk * (N - 1) / FPS
        hx, hy = math.cos(math.radians(heading)), math.sin(math.radians(heading))
        kit.key(M["root"], "location", [(1, (x, y, 0)), (N, (x + d * hx, y + d * hy, 0))], ease="linear")
        rt.rwalk_cycle(M, 1, N, period=32, phase=phase)
    else:
        rt.rpose(M, "relaxed")
    return M


def subject(x, y, heading):
    M = rt.real_mannequin("Subject", (x, y, 0), heading, amber, subsurf=2)
    rt.beanie(M)
    return M


if SHOT == "A":
    for i, (x, y) in enumerate(((-13, 30), (-10.6, 32.5), (-10.2, 27.6))):
        marshal(f"M{i}", x, y, 180, walk=1.3, phase=i)
    cam = kit.camera((-3.5, 31.2, 0.7), look_at=(HX + HD / 2, HY, 3.0), lens=26)
    d = 1.3 * (N - 1) / FPS
    kit.key(cam, "location", [(1, (-3.5, 31.2, 0.7)), (N, (-3.5 - d * 1.5, 30.6, 1.55))], ease="in_out")   # dolly in + rise
    kit.depth_of_field(cam, focus=8.5, fstop=2.8)
    rt.date_stamp(cam, "OCT 30, 2014", "6:07 PM  ·  NEAR TANNERSVILLE, PA", start_frame=-300)

elif SHOT == "B":
    man = subject(-46, 81, -90)
    rt.rwalk_cycle(man, 1, N, period=34)
    kit.key(man["root"], "location", [(1, (-46, 81, 0)), (N, (-46, 81 - 1.25 * (N - 1) / FPS, 0))], ease="linear")
    cam = kit.camera((-44.6, 62.5, 0.55), look_at=(-46, 79, 1.5), lens=40)
    kit.key(cam, "location", [(1, (-44.6, 62.5, 0.55)), (N, (-45.2, 67.5, 1.15))], ease="in_out")          # push in through the grass
    kit.depth_of_field(cam, focus=14, fstop=2.0)
    kit.key(cam.data.dof, "focus_distance", [(1, 17.5), (N, 10.5)], ease="linear")
    kit.light("AREA", (-46, 70, 7), (-46, 78, 1.2), power=900, color="#C9D6F2", size=5, name="GapLight").data.specular_factor = 0.0   # sky through the gap (no mirror patch on the gloss)

else:
    gx, gy = -46.0, 60.0
    man = subject(gx, gy, -90)
    rt.prone(man, (gx, gy + 0.9), -90)
    for i, (x, y) in enumerate(((-43.2, 58.3), (-44.2, 61.8), (-47.7, 62.0), (-48.9, 58.6), (-46.3, 56.2))):
        marshal(f"M{i}", x, y, facing((x, y), (gx, gy)))
    cam = kit.camera((gx + 1.6, gy - 4.6, 0.5), look_at=(gx, gy - 0.1, 0.35), lens=28)
    kit.key(cam, "location", [(1, (gx + 1.6, gy - 4.6, 0.5)), (N, (gx + 0.3, gy - 2.4, 8.5))], ease="in_out")   # crane up and over
    kit.depth_of_field(cam, focus=5, fstop=4)
    kit.key(cam.data.dof, "focus_distance", [(1, 4.8), (N, 8.6)], ease="in_out")

cam.data.clip_end = 3000
kit.shake(cam, strength=0.008, speed=50)
kit.post(bloom=0.25, vignette=0.4, grain=0.02)
