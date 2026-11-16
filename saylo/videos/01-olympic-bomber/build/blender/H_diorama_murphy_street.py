"""Clay diorama: Murphy's main street at 3:30 AM (an illustration of the place, not a replica).
Empty road, low storefronts on both sides with dark windows, warm streetlamps, the domed Cherokee County Courthouse
at the end of the street (Murphy's landmark), wooded mountains behind. Nothing moving. Camera drifts down the street.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import blender_kit as kit
import clay

a = kit.args()
end = a.frames
kit.setup(world="#050506", view="Standard", bloom=0.3)
kit.backdrop("#050506", center="#1A2030", distance=46)
m = clay.mats()

# base slab, road along +Y, sidewalks
clay.box(12, 26, 0.6, (0, 4, -0.3), m["clay_d"], "Base")
clay.box(4.2, 25.6, 0.04, (0, 4, 0.02), m["asph"], "Road")
for i in range(12):
    clay.box(0.08, 0.9, 0.01, (0, -7.5 + i * 2.0, 0.05), m["clay"], f"Dash{i}")
for x in (-2.8, 2.8):
    clay.box(1.4, 25.6, 0.16, (x, 4, 0.08), m["clay"], "Sidewalk")

# storefronts: varied low blocks with a dark display window and a door, both sides
import random
random.seed(3)
y = -7.0
while y < 12.5:
    w = random.uniform(2.2, 3.4)
    for side in (-1, 1):
        h = random.uniform(1.8, 3.4)
        x = side * 4.6
        clay.box(2.4, w - 0.12, h, (x, y + w / 2, h / 2 + 0.16), m["clay"], "Shop")
        clay.box(2.45, w - 0.1, 0.18, (x, y + w / 2, h + 0.25), m["clay_d"], "Cornice")
        clay.box(0.06, (w - 0.12) * 0.62, 0.9, (x - side * 1.21, y + w / 2 - 0.25, 0.85), m["dark"], "Window", bevel=False)
        clay.box(0.06, 0.45, 1.1, (x - side * 1.21, y + w / 2 + (w - 0.12) * 0.36, 0.72), m["clay_d"], "Door", bevel=False)
    y += w

# the courthouse at the end of the street: block, columns, drum, dome
cx, cy = 0, 15.6
clay.box(6.0, 4.0, 3.0, (cx, cy, 1.66), m["clay"], "Courthouse")
for i in range(6):
    clay.cyl(0.14, 2.4, (cx - 2.0 + i * 0.8, cy - 2.15, 1.36), m["clay"], "Column")
clay.box(4.6, 0.6, 0.35, (cx, cy - 2.15, 2.75), m["clay_d"], "Pediment")
clay.cyl(1.25, 1.2, (cx, cy, 3.75), m["clay"], "Drum", verts=32)
clay.sphere(1.25, (cx, cy, 4.35), m["clay"], "Dome", scale=(1, 1, 1.1), segs=32)
clay.cyl(0.08, 0.7, (cx, cy, 5.95), m["clay_d"], "Spire")

# streetlamps along the sidewalks (warm pools on the empty road)
for i, yy in enumerate((-5.5, -0.5, 4.5, 9.5)):
    clay.streetlight(-2.4, yy, m, power=1600, face=1)
    clay.streetlight(2.4, yy + 2.5, m, power=1600, face=-1)

# wooded mountains behind
clay.trees(60, (-7.5, 7.5), (18.5, 21.5), m["clay_d"], seed=11, hr=(1.2, 2.6))
for i, (x, s) in enumerate(((-9, 9), (0, 12), (10, 9))):
    clay.sphere(1.0, (x, 30, -1.5), kit.matte("#34332F", 1.0, f"Ridge{i}"), f"Ridge{i}", scale=(s, 4.0, 8.5))

clay.night_light(moon=0.8, key=2000)

# camera: high above the near end of the street, drifting down it toward the courthouse
cam = kit.camera((-2.6, -15.0, 5.2), look_at=(0, 10.0, 1.8), lens=35)
kit.key(cam, "location", [(1, (-2.6, -15.0, 5.2)), (end, (-1.6, -10.5, 4.2))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (0, 10.0, 1.8)), (end, (0, 12.0, 2.2))], ease="in_out")
kit.shake(cam, strength=0.008, speed=40)
dof = kit.depth_of_field(cam, focus=26.0, fstop=0.7)
kit.key(dof, "focus_distance", [(1, 26.0), (end, 23.0)], ease="in_out")
kit.post(bloom=0.35, vignette=0.7, grain=0.045)
