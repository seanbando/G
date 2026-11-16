"""Retraced-look style test: the Olympic Bomber cold open, VO 0:00-0:33, as 13 Blender shots.

One world (Murphy main street + the Save-A-Lot back lot, schematic clay), one shot per run:
  powershell -File saylo/videos/00-retraced-style-test/build/build.ps1          (renders all, then assembles)
Shot timings live in shots.json (cut on vo-words.json word times).
Schematic only: the street layout, store shape and lot are illustrations, not a survey of the real place.
"""
import json
import math
import os
import sys

import bpy
import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "saylo", "tools", "blender"))
import retraced as rt  # noqa: E402
import clay  # noqa: E402

a = kit.args()
SHOT = int(a.get("shot") or 1)
CFG = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == SHOT)
T0 = S["start"]
N = a.frames


def f(vo_time):
    """Frame in this shot for an absolute voiceover time (seconds)."""
    return kit.f(vo_time - T0)


rt.setup()
m = rt.mats()
rt.night()

# ------------------------------------------------------------------ the town (main street runs along +Y)
kit.rect(900, 900, material=m["ground"], loc=(0, 0, 0), rot=(0, 0, 0), name="Ground")
clay.box(8, 140, 0.04, (0, 0, 0.02), m["road"], "MainRoad", bevel=False)
clay.box(66, 8, 0.04, (37, 60, 0.02), m["road"], "SideRoad", bevel=False)
for x in (-5, 5):
    clay.box(2, 128, 0.16, (x, -4, 0.08), m["clay_d"], "Sidewalk", bevel=False)
for i, y in enumerate(range(-52, 50, 12)):
    for side in (-1, 1):
        h = 5 + ((i * 7 + (side + 1) * 3) % 6)
        if side == -1 and y == -4:
            h = 9                                     # the lettered building
        clay.box(10, 10, h, (side * 11, y, h / 2), m["wall"], "Block")
        # dark windows on the street face (none on the lettered wall)
        for wz in ([] if (side == -1 and y == -4) else range(2, int(h) - 1, 2)):
            for wy in (-3, 0, 3):
                clay.box(0.06, 1.4, 0.9, (side * 5.99, y + wy, wz + 0.4), m["dark"], "Window", bevel=False)
    clay.streetlight(-5.2, y + 6, m, power=900, face=1)
    clay.streetlight(5.2, y + 6, m, power=900, face=-1)

# ring of clay mountain ridges (two rows of smooth peaks)
for row, (r0, n) in enumerate(((150, 34), (205, 40))):
    for k in range(n):
        ang = (k + 0.5 * row) / n * math.tau
        r = r0 + 18 * math.sin(k * 2.3 + row)
        base = 38 + 14 * math.sin(k * 1.7 + 1 + row)
        hgt = base * (0.75 + 0.25 * math.sin(k * 3.1 + row * 2))
        pk = clay.cone(base, hgt * (1.3 if row else 1.0), (r * math.cos(ang), 40 + r * math.sin(ang), hgt * 0.45),
                       m["clay_d"], "Peak", verts=48)
        bpy.ops.object.shade_smooth()

# in-set title on the lettered building's street wall (faces +X)
LET = []
LET.append(kit.text("MURPHY", font="Anton-Regular", size=2.6, extrude=0.06, color="#F2EFE8", align="CENTER",
                    loc=(-5.9, -4, 5.4), rot=(90, 0, 90), name="WallMurphy"))
LET.append(kit.text("NORTH CAROLINA", font="Montserrat-Bold", size=0.62, extrude=0.03, color=rt.AMBER, align="CENTER",
                    loc=(-5.9, -4, 3.7), rot=(90, 0, 90), spacing=1.25, name="WallNC"))
wash = kit.light("AREA", (-1.5, -4, 1.0), (-6, -4, 5), power=300, color="#E9DCC6", size=4, name="WallWash")

# ------------------------------------------------------------------ the store and its back lot
clay.box(24, 16, 6, (30, 76, 3), m["wall"], "Store")
clay.box(24.6, 16.6, 0.5, (30, 76, 6.2), m["clay_d"], "StoreParapet")
clay.box(36, 14, 0.04, (30, 91, 0.02), m["road"], "BackLot", bevel=False)
clay.box(6, 34, 0.04, (15, 79, 0.02), m["road"], "SideDrive", bevel=False)
for i, x in enumerate((28.0, 30.4, 32.8)):
    clay.box(2.2, 1.4, 1.4, (x, 85.3, 0.72), m["dumpster"], "Dumpster")
    clay.box(2.3, 1.5, 0.08, (x, 85.3, 1.46), m["clay_d"], "Lid", rot=(8, 0, 0))
kit.light("AREA", (30, 84.4, 5.0), (30, 88, 0), power=180, color="#C9D6FF", size=1.2, name="BackDoorLamp")
roof_lbl = kit.text("SAVE-A-LOT", font="Montserrat-Bold", size=2.0, color="#FFFFFF", strength=1.6, align="CENTER",
                    loc=(30, 76, 6.5), rot=(0, 0, 0), spacing=1.15, name="RoofLabel")

# ------------------------------------------------------------------ characters
car, CL = rt.car(m, (2, -38, 0), 180, name="Patrol")
officer = rt.mannequin("Officer", (CL["seat"][0], CL["seat"][1], CL["seat"][2] + 0.08 - 0.93), 0, m["man"])
kit.parent(officer["root"], car)
rt.pose(officer, "sit")

man = rt.mannequin("Subject", (34.9, 86.2, -rt.DROP["crouch"]), -90, m["subject"])
rt.pose(man, "crouch")

ROUTE = [(2, 30, 0.2), (2, 60, 0.2), (15, 60, 0.2), (15, 90, 0.2), (23, 90, 0.2)]


def car_along(frames_pts):
    """Key the car root through [(frame, (x, y), heading_deg), ...]."""
    kit.key(car, "location", [(fr, (x, y, 0)) for fr, (x, y), _ in frames_pts], ease="in_out")
    kit.key(car, "rotation_euler", [(fr, (0, 0, math.radians(h))) for fr, _, h in frames_pts], ease="in_out")


# ------------------------------------------------------------------ shots
if SHOT == 1:
    cam = kit.camera((-70, -84, 70), look_at=(6, 18, 0), lens=30)
    kit.key(cam, "location", [(1, (-70, -84, 70)), (N, (-62, -74, 64))], ease="linear")
    rt.date_stamp(cam, "MAY 31, 2003  ·  3:30 AM", start_frame=f(0.25))

elif SHOT == 2:
    cam = kit.camera((0, -78, 24), look_at=(0, 10, 0), lens=30)
    kit.key(cam, "location", [(1, (0, -78, 24)), (N, (0, -58, 18))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (0, 10, 0)), (N, (0, 22, 0))], ease="linear")
    rt.date_stamp(cam, "MAY 31, 2003  ·  3:30 AM", start_frame=-200)

elif SHOT == 3:
    rt.typed(LET[0], f(4.55), cps=14)
    rt.typed(LET[1], f(5.08), cps=26, cursor=False)
    cam = kit.camera((2.5, -13.5, 3.0), look_at=(-6, -4, 4.6), lens=28)
    kit.key(cam, "location", [(1, (2.5, -13.5, 3.0)), (N, (2.0, -9.5, 3.3))], ease="linear")

elif SHOT == 4:
    cam = kit.camera((80, -190, 110), look_at=(0, 12, 0), lens=30)
    kit.key(cam, "location", [(1, (80, -190, 110)), (N, (58, -200, 106))], ease="linear")
    h, hw, hh = rt.hud(cam)
    pop = kit.text("POP. ABOUT 1,600", font="Montserrat-Bold", size=hh * 0.075, spacing=1.15, color="#FFFFFF",
                   strength=1.7, align="LEFT", loc=(-hw * 0.93, -hh * 0.8, 0), rot=(0, 0, 0), name="Pop")
    kit.parent(pop, h)
    rt.typed(pop, f(7.38))

elif SHOT == 5:
    cam = kit.camera((1.5, -44, 1.6), look_at=(0, 30, 2.4), lens=30)
    kit.key(cam, "location", [(1, (1.5, -44, 1.6)), (N, (1.4, -37, 1.7))], ease="linear")

elif SHOT == 6:
    car_along([(1, (2, -40), 180), (N, (2, -22), 180)])
    cam = kit.camera((0.8, -50, 1.3), look_at=(2, -34, 0.9), lens=32)
    kit.key(cam, "location", [(1, (0.8, -50, 1.3)), (N, (0.9, -31, 1.4))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (2, -34, 0.9)), (N, (2, -16, 0.9))], ease="linear")

elif SHOT in (7, 8):
    y0, y1 = (-20, -10) if SHOT == 7 else (-10, 4)
    car_along([(1, (2, y0), 180), (N, (2, y1), 180)])
    head = (CL["seat"][0], CL["seat"][1], 1.42)
    if SHOT == 7:
        cam = kit.camera((1.7, -4.4, 2.1), look_at=(head[0], head[1], 1.15), lens=30)
        kit.key(cam, "location", [(1, (1.7, -4.4, 2.1)), (N, (1.0, -3.0, 1.9))], ease="in_out")
    else:
        cam = kit.camera((2.4, -1.4, 1.45), look_at=head, lens=38)
        kit.key(cam, "location", [(1, (2.4, -1.4, 1.45)), (N, (2.0, -0.4, 1.5))], ease="in_out")
        rt.name_tag(cam, "JEFF POSTELL", "MURPHY POLICE OFFICER", start_frame=f(17.6))
    kit.parent(cam, car)
    kit.parent(kit.aim(cam), car)
    dash = kit.light("AREA", (CL["seat"][0], -0.6, 1.1), head, power=40, color="#7FA6FF", size=0.4, name="DashGlow")
    kit.parent(dash, car)
    dof = kit.depth_of_field(cam, focus=officer["neck"], fstop=2.2)

elif SHOT == 9:
    route = rt.route_line(ROUTE, m["route"], f(21.75), f(24.0), depth=0.35)
    car_along([(f(21.7), (2, 44), 180), (f(22.6), (2, 58), 180), (f(22.95), (8, 60), 90), (f(23.2), (15, 63), 180),
               (f(23.8), (15, 86), 180), (N, (17, 90), 90)])
    cam = kit.camera((24, 58, 70), look_at=(20, 76, 0), lens=30)
    kit.key(cam, "location", [(1, (24, 58, 70)), (N, (24, 62, 62))], ease="linear")
    roof_lbl.data.body = "SAVE-A-LOT"
    rt.typed(roof_lbl, f(23.02))
    kit.light("AREA", (30, 76, 14), (30, 76, 6), power=2500, color="#FFC070", size=8, name="StoreKey")

elif SHOT == 10:
    car_along([(1, (16.5, 90), 90), (N, (22.5, 90), 90)])
    rt.lights_off(CL, f(24.62), dur=3)
    cam = kit.camera((31, 88.6, 1.1), look_at=(19, 90, 0.8), lens=35)
    kit.key(cam, "location", [(1, (31, 88.6, 1.1)), (N, (30, 88.8, 1.1))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (18, 90, 0.8)), (N, (22, 90, 0.8))], ease="linear")

if SHOT != 9:
    roof_lbl.hide_render = True
if SHOT in (11, 12, 13):
    car.location, car.rotation_euler = (23, 90, 0), (0, 0, math.radians(90))
    CL["beam"].data.energy = 0.0
    tgt = kit.empty((36, 84.2, 0.3), "FlashTarget")
    beam_from = (24.6, 91.6, 1.45)
    flash = rt.flashlight(beam_from, tgt, power=5200)
    flash.data.spot_size, flash.data.spot_blend = math.radians(18), 0.35

if SHOT == 11:
    officer["root"].hide_render = True
    for ob in officer["root"].children_recursive:
        ob.hide_render = True
    kit.key(tgt, "location", [(1, (26.5, 84.4, 0.3)), (f(26.3), (31.5, 85.0, 0.6)), (f(26.8), (34.9, 86.2, 0.7)),
                              (N, (34.9, 86.2, 0.7))], ease="in_out")
    cam = kit.camera((30.2, 93.5, 2.1), look_at=(33.5, 86.0, 0.7), lens=32)
    kit.key(cam, "location", [(1, (30.2, 93.5, 2.1)), (N, (32.0, 90.2, 1.3))], ease="in_out")
    kit.key(kit.aim(cam), "location", [(1, (31.0, 85.5, 0.8)), (f(26.8), (34.6, 86.2, 0.7)), (N, (34.9, 86.2, 0.6))],
            ease="in_out")

elif SHOT in (12, 13):
    # officer out of the car, standing by the driver door, flashlight raised
    officer["root"].parent = None
    officer["root"].location = (24.6, 92.0, 0)
    officer["root"].rotation_euler = (0, 0, math.radians(-110))
    rt.pose(officer, "flashlight")
    if SHOT == 12:
        tgt.location = (34.9, 86.2, 0.7)
        cam = kit.camera((22.6, 94.4, 2.0), look_at=(34.9, 86.2, 0.8), lens=34)
        kit.key(cam, "location", [(1, (22.6, 94.4, 2.0)), (N, (23.4, 93.9, 1.9))], ease="linear")
        kit.depth_of_field(cam, focus=12.3, fstop=3.2)
    else:
        bolt, stop, up = f(31.10), f(31.85), f(32.05)
        rt.pose(man, "crouch", frame=1)
        rt.pose(man, "crouch", frame=bolt - 3)
        kit.key(man["root"], "location", [(1, (34.9, 86.2, -rt.DROP["crouch"])), (bolt - 3, (34.9, 86.2, -rt.DROP["crouch"])),
                                          (bolt + 4, (35.6, 86.5, 0.0)), (stop, (39.6, 88.0, 0.0)), (N, (39.9, 88.1, 0.0))],
                ease="in_out")
        rt.run_cycle(man, bolt + 2, stop - 2, period=12)
        rt.pose(man, "stand", frame=stop)
        rt.pose(man, "hands_up", frame=up + 9)
        kit.key(tgt, "location", [(1, (34.9, 86.2, 0.7)), (bolt + 4, (35.6, 86.5, 1.0)), (stop, (39.6, 88.0, 1.1)),
                                  (N, (39.9, 88.1, 1.2))], ease="in_out")
        flash.data.energy = 9000
        cam = kit.camera((35.2, 94.6, 1.9), look_at=(36.0, 87.0, 0.9), lens=32)
        kit.key(cam, "location", [(1, (35.2, 94.6, 1.9)), (N, (36.6, 94.0, 1.8))], ease="linear")
        kit.key(kit.aim(cam), "location", [(1, (35.5, 86.6, 0.9)), (stop, (38.8, 87.8, 1.1)), (N, (39.4, 88.0, 1.2))],
                ease="in_out")

kit.shake(cam, strength=0.015, speed=40)
rt.finish()
