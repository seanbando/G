"""Clay road maps for the Frein edit, described by the shot's "map" entry in the plan (--arg cfg=..., --arg shot=N).
Roads and place positions are OpenStreetMap data (build/osm/*.json), credit "(c) OpenStreetMap contributors" via the
source tag. 1 unit = 1 km, flat slab (OpenStreetMap has no elevation).
  "map": {"center": [lat, lon],            where the camera looks
          "span": 30,                      kilometres across the frame at the start
          "move": "push" | "pull",         the camera always moves (Retraced rule)
          "pins": [{"lat":, "lon":, "label": "BARRACKS", "amber": true, "at": 117.9}, ...],   label types on at `at`
          "route": [[lat, lon], ...], "route_at": [t0, t1],                                   amber line that draws itself
          "stamp": "PIKE COUNTY, PA", "sub": "...", "at": 118.0}                              typed top-left
Positions the plan gives are plotted exactly; anything approximate must be said in its label."""
import io
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
CFG = json.load(io.open(os.path.join(HERE, a.get("cfg")), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == int(a.get("shot")))
MP = S["map"]
T0 = S["start"]
LAT0, LON0 = MP["center"]
KX = 111.32 * math.cos(math.radians(LAT0))


def f(t):
    return kit.f(t - T0)


def xy(lat, lon):
    return ((lon - LON0) * KX, (lat - LAT0) * 110.57)


rt.setup(bloom=0.35)
m = rt.mats()
kit.light("SUN", (-6, -10, 20), (0, 0, 0), power=1.6, color="#9FB3E0", name="Sky")
kit.light("AREA", (-10, -14, 14), (0, 0, 0), power=9000, color="#C9D6F2", size=18, name="Key")
clay.box(160, 120, 0.6, (0, 0, -0.3), kit.matte("#2A3140", 0.9, "Slab"), "Slab", bevel=False)
span = float(MP.get("span", 30))
k = span / 30.0                                       # line widths and label sizes follow the scale of the view
road_m = {"motorway": kit.matte("#E4E2DC", 0.8, "RoadA"), "trunk": kit.matte("#D2D0CA", 0.8, "RoadB"),
          "primary": kit.matte("#B9B7B1", 0.85, "RoadC"), "secondary": kit.matte("#8D8F94", 0.9, "RoadD")}
width = {"motorway": 0.13 * k, "trunk": 0.1 * k, "primary": 0.075 * k, "secondary": 0.045 * k}
curves = {}
for fn in ("region_wide.json", "region.json"):
    d = json.load(io.open(os.path.join(HERE, "..", "osm", fn), encoding="utf-8"))
    for e in d["elements"]:
        if e["type"] != "way" or "geometry" not in e:
            continue
        kind = e["tags"].get("highway")
        if kind not in width or (fn == "region.json" and kind != "secondary"):
            continue
        pts = [xy(g["lat"], g["lon"]) for g in e["geometry"]]
        if all(abs(x) > span * 1.6 or abs(y) > span * 1.2 for x, y in pts):
            continue
        cu = curves.get(kind)
        if cu is None:
            cu = curves[kind] = bpy.data.curves.new("Roads_" + kind, "CURVE")
            cu.dimensions = "3D"
            cu.bevel_depth, cu.bevel_resolution = width[kind], 2
            ob = bpy.data.objects.new("Roads_" + kind, cu)
            bpy.context.scene.collection.objects.link(ob)
            kit.assign(ob, road_m[kind])
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for p, (x, y) in zip(sp.points, pts):
            p.co = (x, y, width[kind] * 0.5, 1.0)

pin_m = kit.emission(rt.AMBER, 3.0, "Pin")
for i, p in enumerate(MP.get("pins", [])):
    x, y = xy(p["lat"], p["lon"])
    t0 = f(p["at"]) if p.get("at") is not None else -300
    amber = p.get("amber", False)
    h = 2.0 * k
    post = clay.cyl(0.05 * k, h, (x, y, h / 2), m["amber"] if amber else m["clay"], "PinPost", verts=12)
    head = clay.sphere((0.32 if amber else 0.22) * k, (x, y, h + 0.1 * k), pin_m if amber else kit.emission("#E8E8E2", 1.6, "PinW"), "PinHead")
    for ob, z in ((post, h / 2), (head, h + 0.1 * k)):
        kit.key(ob, "location", [(t0 - 6, (x, y, z + 4 * k)), (t0 + 4, (x, y, z))], ease="expo")
    if amber:
        glow = kit.light("POINT", (x, y, 0.6 * k), (x, y, 0), power=0, color=rt.AMBER, size=1.0, name="PinGlow")
        kit.key(glow.data, "energy", [(t0, 0.0), (t0 + 10, 420.0 * k * k)], ease="out")
    side = p.get("side", 1)
    t = kit.text(p["label"], font="Montserrat-Bold", size=0.62 * k, spacing=1.15, color="#F4F1EA" if amber else "#C9CED8",
                 strength=1.5 if amber else 1.2, align="LEFT" if side > 0 else "RIGHT", loc=(x + 0.55 * k * side, y - 0.2 * k, h + 0.25 * k),
                 rot=(62, 0, 0), name="L_" + p["label"][:8])
    t.visible_shadow = False
    rt.typed(t, t0 + 4, cps=34, cursor=False)

if MP.get("route"):
    pts = [(*xy(la, lo), 0.25 * k) for la, lo in MP["route"]]
    r0, r1 = MP.get("route_at", [T0 + 0.3, S["end"] - 0.3])
    rt.route_line(pts, m["route"], f(r0), f(r1), depth=0.09 * k, name="Route")

cx, cy = MP.get("look", [0.0, 0.0])
d0 = span * 0.95
p_far = (cx + span * 0.12, cy - d0 * 0.78, d0 * 0.6)
p_near = (cx + span * 0.085, cy - d0 * 0.6, d0 * 0.46)
a_, b_ = (p_far, p_near) if MP.get("move", "push") == "push" else (p_near, p_far)
cam = kit.camera(a_, look_at=(cx, cy, 0), lens=36)
kit.key(cam, "location", [(1, a_), (N, b_)], ease="linear")
cam.data.clip_end = 2000
if MP.get("stamp"):
    rt.date_stamp(cam, MP["stamp"], MP.get("sub"), start_frame=f(MP["at"]) if MP.get("at") is not None else -300, cps=40, sub_cps=70)
rt.finish()
