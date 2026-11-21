"""Hero upgrade of shot 11 ("and he spots a man crouched by the dumpsters", VO 25.60-28.45) with real assets:
the CC0 rigged mannequin and Poly Haven alley props/textures (see saylo/tools/fetch_polyhaven.py).
The patrol car sits off camera to the left; only its flashlight beam comes into frame.
Schematic: an illustration of a store's back lot, not a survey of the real Save-A-Lot.
"""
import math
import os
import sys

import bpy
import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "tools", "blender")))
import retraced as rt  # noqa: E402
import clay  # noqa: E402

T0 = 25.60
N = kit.args().frames


def f(t):
    return kit.f(t - T0)


rt.setup(bloom=0.25)
m = rt.mats()
rt.night(moon=0.9, fill=500)
rt.volume_fog(0.010)

# ground + back wall of the store (wall runs along X at y=0, lot is -Y)
asph = rt.pbr("asphalt_02", scale=3.0, sat=0.2)
kit.rect(120, 120, material=asph, loc=(0, -20, 0), rot=(0, 0, 0), name="Lot")
wall_m = rt.pbr("concrete_wall_004", scale=2.5, sat=0.25)
wall = clay.box(34, 0.6, 7.5, (0, 0.3, 3.75), wall_m, "BackWall", bevel=False)
cap = clay.box(34.4, 0.9, 0.35, (0, 0.3, 7.6), m["clay_d"], "Coping", bevel=False)
side_m = rt.pbr("brick_wall_08", scale=2.0, sat=0.2)
clay.box(0.6, 14, 7.5, (17.3, -6.7, 3.75), side_m, "SideWall", bevel=False)

rt.model("rollershutter_door", (-7.0, -0.02, 0), 0, name="LoadingDoor")
rt.model("security_light", (-7.0, -0.05, 5.0), 0, name="SecLight")
kit.light("SPOT", (-7.0, -0.6, 4.8), (-7.0, -4.0, 0), power=900, color="#E8EEFF", size=0.4, name="SecLamp")
rt.model("modular_metal_gutter", (3.6, -0.1, 0), 0, name="Gutter")
rt.model("exterior_aircon_unit", (7.5, -0.45, 2.6), 0, name="AirCon")
rt.model("utility_box_01", (11.0, -0.35, 0), 0, name="Utility")
rt.model("metal_trash_can", (5.4, -0.8, 0), 0, name="Can")
rt.model("trashbag", (4.6, -1.5, 0), 30, name="Bag1")
rt.model("trashbag", (-3.4, -1.3, 0), -40, name="Bag2")
rt.model("plastic_crate_01", (-10.5, -0.8, 0), 10, name="Crate1")
rt.model("plastic_crate_01", (-10.4, -0.8, 0.32), -5, name="Crate2")
rt.model("water_manhole_cover", (1.0, -7.0, 0.005), 0, name="Manhole")
rt.model("street_lamp_01", (13.0, -13.0, 0), 200, name="StreetLamp")
kit.light("SPOT", (12.4, -12.4, 6.0), (11, -10, 0), power=1500, color="#FFC98A", size=0.6, name="StreetLampLight")
rt.model("modular_electricity_poles", (-15.0, -12.0, 0), 0, name="Pole")

# two dumpsters (built: no CC0 dumpster on Poly Haven), painted metal, dark lids
dmp_m = rt.pbr("blue_metal_plate", scale=1.2, sat=0.25, name="DumpsterPaint")
for x in (-1.3, 1.1):
    clay.box(2.3, 1.4, 1.35, (x, -0.95, 0.78), dmp_m, "Dumpster")
    clay.box(2.4, 0.08, 0.2, (x, -1.68, 1.25), dmp_m, "Rim", bevel=False)
    clay.box(2.4, 1.55, 0.06, (x, -0.95, 1.5), m["dark"], "Lid", rot=(7, 0, 0))
    for wx in (x - 0.9, x + 0.9):
        clay.cyl(0.09, 0.08, (wx, -1.5, 0.1), m["dark"], "Caster", rot=(90, 0, 0))

# the subject: crouched at the end of the dumpsters, facing the car (-X)
man = rt.real_mannequin("Subject", (2.75, -1.1, -rt.RDROP["crouch"]), -90, m["subject"])
rt.rpose(man, "crouch")

# Postell's flashlight from the car (off camera, left): sweeps along the wall, lands on him on "man"/"crouched"
tgt = kit.empty((-6.0, -0.4, 0.8), "BeamTarget")
kit.key(tgt, "location", [(1, (-6.0, -0.4, 0.9)), (f(26.25), (-0.5, -1.0, 0.9)), (f(26.75), (2.75, -1.2, 0.75)),
                          (N, (2.75, -1.2, 0.75))], ease="in_out")
beam = rt.flashlight((-13.0, -9.5, 1.45), tgt, power=14000)
beam.data.spot_size, beam.data.spot_blend = math.radians(14), 0.45
# dim spill from the parked car's dash, and the back-door lamp
kit.light("AREA", (-11, -8.5, 1.2), (0, 0, 1), power=150, color="#7FA0FF", size=2, name="CarSpill")
# soft cool fill on him from the lot side, so the beam's hard shadows don't swallow his head
kit.light("AREA", (1.0, -4.5, 1.6), (2.75, -1.1, 0.8), power=60, color="#9FB4E8", size=2.5, name="SubjectFill")

# camera: low by the lot, pushing toward the dumpsters as the beam finds him
cam = kit.camera((-3.0, -9.0, 2.0), look_at=(-2.0, 0, 1.0), lens=32)
kit.key(cam, "location", [(1, (-3.0, -9.0, 2.0)), (N, (0.2, -5.4, 1.35))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (-2.5, -0.5, 1.2)), (f(26.75), (2.2, -1.1, 0.8)), (N, (2.6, -1.1, 0.75))],
        ease="in_out")
kit.shake(cam, strength=0.012, speed=40)
kit.depth_of_field(cam, focus=man["root"], fstop=2.8)
rt.finish(vignette=0.55, grain=0.035, bloom=0.25)
