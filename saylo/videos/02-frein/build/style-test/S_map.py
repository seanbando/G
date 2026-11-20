"""Frein cold open, shot 4: "in the Pocono Mountains of Pennsylvania."
A clay road map built from OpenStreetMap data (build/osm/region.json: motorways, trunk, primary and secondary roads,
towns), amber pin on the airfield, labels typed on. Credit on screen: "© OpenStreetMap contributors" (source tag).
The pin is the Birchwood-Pocono Airpark area on Birchwood Road (OSM way 16132558); roads and towns are real positions.
1 unit = 1 km. No terrain relief: OpenStreetMap has no elevation, so the slab is flat.
"""
import json
import math
import os
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
CFG = json.load(open(os.path.join(HERE, a.get("cfg") or "shots.json"), encoding="utf-8"))
SHOT = int(a.get("shot") or 4)
S = next(s for s in CFG["shots"] if s["id"] == SHOT)
T0 = S["start"]
f = lambda t: kit.f(t - T0)
V2 = "cfg" in a._extra                              # v2 cold open: shot 7 = fast push from wide, shot 8 = close on the pin

LAT0, LON0 = 41.0624, -75.2534                   # the airfield (Birchwood Road)
KX = 111.32 * math.cos(math.radians(LAT0))


def xy(lat, lon):
    return ((lon - LON0) * KX, (lat - LAT0) * 110.57)


rt.setup(bloom=0.35)
m = rt.mats()
kit.light("SUN", (-6, -10, 20), (0, 0, 0), power=1.6, color="#9FB3E0", name="Sky")
kit.light("AREA", (-10, -14, 14), (0, 0, 0), power=9000, color="#C9D6F2", size=18, name="Key")
slab = kit.matte("#2A3140", 0.9, "Slab")
clay.box(46, 34, 0.6, (0, 0, -0.3), slab, "Slab")
road_m = {"motorway": kit.matte("#E4E2DC", 0.8, "RoadA"), "trunk": kit.matte("#D2D0CA", 0.8, "RoadB"),
          "primary": kit.matte("#B9B7B1", 0.85, "RoadC"), "secondary": kit.matte("#8D8F94", 0.9, "RoadD")}
width = {"motorway": 0.13, "trunk": 0.1, "primary": 0.075, "secondary": 0.045}

d = json.load(open(os.path.join(HERE, "..", "osm", "region.json"), encoding="utf-8"))
curves = {}
for e in d["elements"]:
    if e["type"] != "way":
        continue
    k = e["tags"]["highway"]
    cu = curves.get(k)
    if cu is None:
        cu = curves[k] = bpy.data.curves.new("Roads_" + k, "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth, cu.bevel_resolution = width[k], 2
        ob = bpy.data.objects.new("Roads_" + k, cu)
        bpy.context.scene.collection.objects.link(ob)
        kit.assign(ob, road_m[k])
    pts = [xy(g["lat"], g["lon"]) for g in e["geometry"]]
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts):
        p.co = (x, y, width[k] * 0.5, 1.0)

# towns: small clay blocks + typed labels
for name in ("Tannersville", "Stroudsburg", "Mount Pocono"):
    n = next(e for e in d["elements"] if e["type"] == "node" and e["tags"].get("name") == name)
    x, y = xy(n["lat"], n["lon"])
    for i, (dx, dy, h) in enumerate(((0, 0, 0.5), (0.35, 0.2, 0.32), (-0.3, 0.25, 0.4), (0.15, -0.35, 0.28))):
        clay.box(0.26, 0.26, h, (x + dx, y + dy, h / 2), m["clay"], "Town")
    t = kit.text(name.upper(), font="Montserrat-Bold", size=0.55, spacing=1.15, color="#DADDE3", strength=1.2,
                 align="LEFT", loc=(x + 0.7, y - 0.2, 0.9), rot=(62, 0, 0), name="T_" + name)
    t.visible_shadow = False
    rt.typed(t, (f(7.85) if not V2 else f(8.9)) + (0 if name == "Tannersville" else 8), cps=30, cursor=False)

# the airfield: amber pin dropping in, amber glow on the slab
pin_m = kit.emission(rt.AMBER, 3.0, "Pin")
post = clay.cyl(0.05, 2.0, (0, 0, 1.0), m["amber"], "PinPost", verts=12)
head = clay.sphere(0.34, (0, 0, 2.1), pin_m, "PinHead")
t0 = f(8.0) if not V2 else f(8.25)
for ob, z in ((post, 1.0), (head, 2.1)):
    kit.key(ob, "location", [(t0 - 6, (0, 0, z + 4)), (t0 + 4, (0, 0, z))], ease="expo")
glow = kit.light("POINT", (0, 0, 0.6), (0, 0, 0), power=0, color=rt.AMBER, size=1.0, name="PinGlow")
kit.key(glow.data, "energy", [(t0, 0.0), (t0 + 10, 420.0)], ease="out")

if not V2:
    cam = kit.camera((3.5, -21, 17), look_at=(-2.5, 1.2, 0), lens=34)
    kit.key(cam, "location", [(1, (3.5, -21, 17)), (N, (2.6, -17.5, 14.5))], ease="linear")
    rt.date_stamp(cam, "POCONO MOUNTAINS", "PENNSYLVANIA", start_frame=f(7.9))
elif SHOT == 7:
    cam = kit.camera((5, -30, 26), look_at=(-2.5, 1.2, 0), lens=34)
    kit.key(cam, "location", [(1, (5, -30, 26)), (N, (3.6, -22, 18))], ease="linear")
    rt.date_stamp(cam, "POCONO MOUNTAINS", "PENNSYLVANIA", start_frame=f(7.75))
else:
    cam = kit.camera((2.6, -11.5, 7.5), look_at=(-1.6, 0.2, 0.6), lens=40)
    kit.key(cam, "location", [(1, (2.6, -11.5, 7.5)), (N, (2.0, -9.2, 5.8))], ease="linear")
    rt.date_stamp(cam, "POCONO MOUNTAINS", "PENNSYLVANIA", start_frame=-300)
rt.finish()
