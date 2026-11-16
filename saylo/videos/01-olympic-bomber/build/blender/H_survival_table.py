"""Five Years, VO 784.32-794.80 (315 frames): what he reportedly lived on, laid out on a dark table in clay.
Each item drops in on its word, with a typed label: SALAMANDERS (0.0 s), GAME (1.1, "whatever he could hunt"),
GARDENS (3.3), STOLEN GRAIN (5.26), BURIED BARRELS (6.32). On "agents later found them" (9.16) an amber light finds
the barrel. One acorn already sits on the table (the line before). Illustration, clay only; no people, no weapons.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import blender_kit as kit
import clay

a = kit.args()
end = a.frames
F = kit.f
kit.setup(world="#060606", view="Standard", bloom=0.3)
m = clay.mats()
wood = kit.matte("#5E5A55", 0.9, "Table")
dirt = kit.matte("#5C5853", 0.95, "Dirt")
clay.box(16, 6.5, 0.4, (2.5, 0.6, -0.2), wood, "Table")

def drop(objs, t0, height=2.2):
    g = kit.empty((0, 0, 0), "Drop")
    for o in objs:
        kit.parent(o, g)
    kit.key(g, "location", [(t0 - 8, (0, 0, height)), (t0 + 4, (0, 0, 0))], ease="bounce")
    for o in objs:
        kit.fade(o, [(t0 - 8, 0.0), (t0 - 4, 1.0)])
    return g

def label(text, x, t0, amber=False):
    tx = kit.text(text, font="Montserrat-Bold", size=0.32, spacing=1.15, color=clay.AMBER if amber else "#EDE8DD",
                  strength=1.4, loc=(x, -1.05, 0.02), rot=(0, 0, 0), name=text)
    tx.visible_shadow = False
    kit.fade(tx, [(t0 + 2, 0.0), (t0 + 10, 1.0)])

# acorn (already there): nut + cap
clay.sphere(0.22, (-3.6, 0.2, 0.25), m["clay"], "Acorn", scale=(0.85, 0.85, 1.15))
clay.sphere(0.24, (-3.6, 0.2, 0.47), m["clay_d"], "AcornCap", scale=(1, 1, 0.45))
clay.cyl(0.03, 0.18, (-3.6, 0.2, 0.62), m["clay_d"], "AcornStem")
label("ACORNS", -4.15, 1)

# salamander: chain of flattened spheres + tail + four legs
x0, t = -1.6, F(0.0)
parts = []
for i, (dx, r) in enumerate([(0, 0.16), (0.26, 0.18), (0.52, 0.17), (0.78, 0.14), (1.0, 0.11), (1.18, 0.08), (1.32, 0.05)]):
    parts.append(clay.sphere(r, (x0 + dx, 0.0, 0.1 + r * 0.5), m["clay"], f"Sal{i}", scale=(1.3, 1.0, 0.55)))
for dx, dy in ((0.2, 0.2), (0.2, -0.2), (0.62, 0.2), (0.62, -0.2)):
    parts.append(clay.cyl(0.03, 0.2, (x0 + dx, dy, 0.08), m["clay"], "Leg", rot=(90, 0, 0)))
drop(parts, t)
label("SALAMANDERS", x0 - 0.55, t)

# game: a rabbit (body, head, ears)
x1, t = 0.6, F(1.1)
parts = [clay.sphere(0.36, (x1, 0.0, 0.34), m["clay"], "RabBody", scale=(1.25, 0.9, 0.9)),
         clay.sphere(0.2, (x1 + 0.45, 0.0, 0.62), m["clay"], "RabHead"),
         clay.sphere(0.06, (x1 + 0.4, 0.06, 0.92), m["clay"], "Ear1", scale=(0.6, 0.6, 2.4)),
         clay.sphere(0.06, (x1 + 0.48, -0.06, 0.92), m["clay"], "Ear2", scale=(0.6, 0.6, 2.4)),
         clay.sphere(0.1, (x1 - 0.48, 0.0, 0.42), m["clay"], "Tail")]
drop(parts, t)
label("GAME", x1 - 0.3, t)

# garden: corn cob + two tomatoes
x2, t = 2.6, F(3.3)
parts = [clay.cyl(0.15, 0.9, (x2, 0.0, 0.17), m["clay"], "Corn", rot=(0, 90, 15)),
         clay.sphere(0.16, (x2 + 0.55, 0.3, 0.16), m["clay"], "Husk", scale=(1.8, 0.5, 0.4)),
         clay.sphere(0.22, (x2 + 0.2, -0.45, 0.22), m["clay_d"], "Tomato1"),
         clay.sphere(0.18, (x2 + 0.6, -0.3, 0.18), m["clay_d"], "Tomato2")]
drop(parts, t)
label("GARDENS", x2 - 0.3, t)

# grain: a squat sack + a little spill
x3, t = 4.7, F(5.26)
parts = [clay.sphere(0.5, (x3, 0.1, 0.42), m["clay"], "Sack", scale=(1.0, 0.85, 0.95)),
         clay.cyl(0.18, 0.22, (x3, 0.1, 0.9), m["clay_d"], "SackNeck")]
for i in range(14):
    parts.append(clay.sphere(0.035, (x3 + 0.55 + (i % 5) * 0.08, -0.25 + (i // 5) * 0.09, 0.03), m["clay_d"], "Grain"))
drop(parts, t)
label("STOLEN GRAIN", x3 - 0.6, t)

# buried barrel: dirt mound + barrel half in it
x4, t = 7.2, F(6.32)
mound = clay.sphere(0.9, (x4, 0.1, 0.0), dirt, "Mound", scale=(1.3, 1.1, 0.45))
barrel = clay.cyl(0.42, 1.0, (x4, 0.1, 0.38), m["clay"], "Barrel", verts=32)
lid = clay.cyl(0.44, 0.06, (x4, 0.1, 0.9), m["clay_d"], "BarrelLid", verts=32)
rings = [clay.cyl(0.43, 0.04, (x4, 0.1, z), m["clay_d"], "Ring", verts=32) for z in (0.55, 0.78)]
drop([mound, barrel, lid] + rings, t, height=1.6)
label("BURIED BARRELS", x4 - 0.75, t, amber=True)
found = kit.light("SPOT", (x4, -1.5, 4.0), (x4, 0.1, 0.5), power=0, color="#E0A040", size=0.6, name="Found")
found.data.spot_size = math.radians(30)
kit.key(found.data, "energy", [(F(9.16), 0.0), (F(9.16) + 10, 2600.0)], ease="out")

# light: low warm key from the left, soft top, dark everywhere else
kit.light("AREA", (-6, -5, 5), (2, 0, 0), power=1500, color="#FFE1BC", size=4, name="Key")
kit.light("AREA", (3, -2, 7), (3, 0, 0), power=700, color="#D6DEEE", size=8, name="Top")

# camera: low over the table edge, tracking left -> right with the items as they land
cam = kit.camera((-3.0, -6.2, 2.6), look_at=(-2.0, 0.0, 0.2), lens=45)
kit.key(cam, "location", [(1, (-3.0, -6.2, 2.6)), (F(3.3), (0.8, -6.0, 2.5)), (F(6.32), (4.4, -6.0, 2.5)), (end, (6.4, -5.8, 2.4))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (-2.0, 0, 0.2)), (F(3.3), (1.4, 0, 0.2)), (F(6.32), (5.4, 0, 0.3)), (end, (7.0, 0.1, 0.4))], ease="in_out")
kit.shake(cam, strength=0.008, speed=40)
dof = kit.depth_of_field(cam, focus=6.6, fstop=3.2)
for ob in bpy.data.objects:
    if ob.type == "MESH" and not ob.name.startswith(("Table", "Backdrop")):
        for poly in ob.data.polygons:
            poly.use_smooth = True
kit.post(bloom=0.3, vignette=0.6, grain=0.04)
