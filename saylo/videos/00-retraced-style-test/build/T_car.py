"""Look-dev for rt.police_car(): front three-quarter and side views (--arg view=front|side), officer seated. Stills only."""
import os
import sys

import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "tools", "blender")))
import retraced as rt  # noqa: E402

view = kit.args().get("view") or "front"
rt.setup()
m = rt.mats()
rt.night(moon=0.9, fill=500)
asph = rt.pbr("asphalt_02", scale=3.0, sat=0.2)
kit.rect(60, 60, material=asph, loc=(0, 0, 0), rot=(0, 0, 0), name="Lot")
car, CL = rt.police_car(m, (0, 0, 0), 0)
off = rt.real_mannequin("Officer", (CL["seat"][0], CL["seat"][1], CL["seat"][2] - 0.95), -90, m["man"])
kit.parent(off["root"], car)
rt.rpose(off, "drive")
kit.light("AREA", (-5, -6, 6), (0, 0, 0.8), power=2500, color="#DDE4F5", size=5, name="Key")
kit.light("AREA", (5, 5, 3), (0, 0, 0.8), power=1200, color="#7F98D8", size=4, name="Rim")
kit.light("SPOT", (3, -3, 4), (0, 0, 0.6), power=1500, color="#FFCF8A", size=0.5, name="Lamp")
if view == "pose":                                    # the driver alone, side on
    for ob in car.children_recursive:
        if not ob.name.startswith("Officer"):
            ob.hide_render = True
    cam = kit.camera((4.6, 0.0, 0.8), look_at=(0, 0.0, 0.6), lens=32)
elif view == "side":
    cam = kit.camera((4.6, 0.2, 1.4), look_at=(0, 0.2, 0.9), lens=32)
else:
    cam = kit.camera((3.6, -5.6, 1.6), look_at=(0, 0, 0.75), lens=35)
rt.finish()
