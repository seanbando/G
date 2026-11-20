"""Frein cold open (VO 0:00-0:52) in the Retraced look: the airfield near Tannersville at dusk, Oct 30, 2014.

One world, one shot per run (shots.json, cut on vo-words.json word times):
  powershell -File saylo/videos/02-frein/build/style-test/build.ps1
SCHEMATIC SET: OpenStreetMap has the roads here but not the airstrip, hangar or resort buildings, so the layout
(runway, hangar, resort block, tree line) is an illustration of "an abandoned resort with an old airstrip", not a survey.
Faceless grey mannequins = the marshals; the one glossy amber mannequin = Frein. Nobody is shown being hit.
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
CFG = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == SHOT)
T0 = S["start"]
N = a.frames
FPS = CFG["fps"]
AERIAL = SHOT in (1, 6, 14)


def f(vo_time):
    """Frame in this shot for an absolute voiceover time (seconds)."""
    return kit.f(vo_time - T0)


rt.setup()
m = rt.mats()
# dusk, a little after sunset: no direct sun, a cool sky from above and a paler band on the western horizon
kit.light("SUN", (-40, -60, 100), (0, 0, 0), power=2.6, color="#9FB3E0", name="Sky")
kit.light("SUN", (-300, -80, 75), (0, 0, 0), power=1.7, color="#B9C6E6", name="WestGlow")
kit.light("SUN", (200, 120, 90), (0, 0, 0), power=0.7, color="#6F86C0", name="EastFill")
# (no world fog here: a world volume swallows sun light in EEVEE and the ground shots go black)

# sky band: a wide ring whose emission fades from a pale dusk blue at the horizon to the navy world above
sky = bpy.data.materials.new("DuskBand")
sky.use_nodes = True
nt = sky.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
em = nt.nodes.new("ShaderNodeEmission")
tc = nt.nodes.new("ShaderNodeTexCoord")
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.0, (0.16, 0.22, 0.36, 1)
ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.55, kit.rgb(rt.NAVY)
nt.links.new(tc.outputs["Generated"], sep.inputs[0])
nt.links.new(sep.outputs["Z"], ramp.inputs[0])
nt.links.new(ramp.outputs[0], em.inputs["Color"])
nt.links.new(em.outputs[0], out.inputs[0])
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1500, depth=700, location=(0, 0, 330), end_fill_type="NOTHING")
band = bpy.context.active_object
band.name = "SkyBand"
kit.assign(band, sky)
band.visible_shadow = False

# ------------------------------------------------------------------ materials
asph = rt.pbr("asphalt_02", scale=4.0, sat=0.15)
conc = rt.pbr("concrete_wall_004", scale=3.0, sat=0.2)
metal = rt.pbr("blue_metal_plate", scale=2.5, sat=0.08, name="HangarMetal")
ground = kit.matte("#4F534C", 0.95, "Field")
strip = rt.pbr("concrete_wall_004", scale=6.0, sat=0.1, name="OldStrip")
pine_m = kit.matte("#555A60", 0.9, "Pine")
trunk_m = kit.matte("#34332F", 0.9, "Trunk")
grass_m = kit.matte("#777A70", 0.9, "Grass")
line_m = kit.matte("#B9B6AE", 0.9, "FadedPaint")
crack_m = kit.matte("#1E1E20", 0.95, "Crack")

# ------------------------------------------------------------------ ground, runway
kit.rect(3200, 3200, material=ground, loc=(0, 0, 0), rot=(0, 0, 0), name="Ground")
clay.box(18, 520, 0.05, (0, 0, 0.025), strip, "Runway", bevel=False)
clay.box(46, 14, 0.05, (-23, 30, 0.02), strip, "Apron", bevel=False)            # runway -> hangar door
for y in range(-240, 250, 30):                                                 # faded centre dashes
    clay.box(0.35, 9, 0.012, (0, y, 0.056), line_m, "Dash", bevel=False)
rnd = random.Random(11)
for _ in range(70):                                                            # cracks across the old asphalt
    x, y = rnd.uniform(-8.5, 8.5), rnd.uniform(-250, 250)
    clay.box(rnd.uniform(1.5, 7), 0.07, 0.012, (x, y, 0.057), crack_m, "Crack", rot=(0, 0, rnd.uniform(-70, 70)), bevel=False)


def collection_of(objs, name):
    col = bpy.data.collections.new(name)
    for o in objs:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
    return col


def placer(col):
    def place(loc, rot_z=0.0, scale=1.0):
        e = bpy.data.objects.new(col.name, None)
        e.instance_type, e.instance_collection = "COLLECTION", col
        e.location, e.rotation_euler, e.scale = loc, (0, 0, math.radians(rot_z)), (scale,) * 3
        bpy.context.scene.collection.objects.link(e)
        return e
    return place


# pines (3 shapes), instanced
PINES = []
for i, (h, r) in enumerate(((15, 3.1), (19, 3.7), (12, 2.7))):
    parts = [clay.cyl(0.22, h * 0.3, (0, 0, h * 0.15), trunk_m, "Trunk", verts=8)]
    for k in range(7):                           # many overlapping tiers: a spruce outline, not stacked blocks
        parts.append(clay.cone(r * (1 - 0.125 * k), h * 0.26, (0, 0, h * (0.145 + 0.118 * k)), pine_m, "Tier", verts=12))
    PINES.append(placer(collection_of(parts, f"Pine{i}")))
# weeds / tall grass tuft, instanced
tuft = []
for k in range(11):                              # thin blades, knee high
    ang = k / 11 * math.tau * 2
    rr = 0.05 + 0.012 * k
    hh = 0.32 + 0.16 * math.sin(k * 2.1)
    c = clay.cone(0.011, hh, (rr * math.cos(ang), rr * math.sin(ang), hh / 2), grass_m, "Blade", verts=4)
    c.rotation_euler = (0.3 * math.sin(ang), -0.3 * math.cos(ang), 0)
    tuft.append(c)
TUFT = placer(collection_of(tuft, "Tuft"))


def in_clearing(x, y):
    """The open ground: runway strip, the field west of it with the hangar, and the resort lot to the north."""
    if abs(x) < 42 and abs(y) < 300:
        return True
    if -92 < x < 0 and -70 < y < 74:           # hangar field; its north edge (y = 74) is the tree line Frein leaves
        return True
    if -120 < x < 0 and 135 < y < 215:         # resort lot
        return True
    return False


rnd = random.Random(5)
n_trees = 7000 if AERIAL else 3200
ext = 560 if AERIAL else 280
TS = 1.5 if SHOT == 1 else 1.0                   # the high aerial reads better with heavier trees
placed = 0
while placed < n_trees:
    x, y = rnd.uniform(-ext, ext), rnd.uniform(-ext * 0.9, ext * 0.9)
    if in_clearing(x, y):
        continue
    PINES[rnd.randrange(3)]((x, y, 0), rnd.uniform(0, 360), rnd.uniform(0.75, 1.25) * TS)
    placed += 1
# a tight, readable edge along the tree line the man walks out of (north side of the hangar field)
for i in range(60):
    x = -92 + i * 1.55 + rnd.uniform(-0.4, 0.4)
    if -50 < x < -42:
        continue                                # the gap he steps through
    PINES[rnd.randrange(3)]((x, 77 + rnd.uniform(0, 5), 0), rnd.uniform(0, 360), rnd.uniform(0.8, 1.2))

n_tufts = 1200 if AERIAL else 6500
for _ in range(n_tufts):
    x, y = rnd.uniform(-92, 42), rnd.uniform(-110, 130)
    if not in_clearing(x, y) or (abs(x) < 9 and rnd.random() < 0.93) or (-63 < x < -37 and 15 < y < 45):
        continue
    TUFT((x, y, 0), rnd.uniform(0, 360), rnd.uniform(0.5, 1.15))

# far ridges (the Poconos are a plateau: long low ridges, not peaks)
for row, (r0, n) in enumerate(((1050, 26), (1300, 30))):
    for k in range(n):
        ang = (k + 0.5 * row) / n * math.tau
        base = 300 + 80 * math.sin(k * 1.7 + row)
        hgt = 46 + 16 * math.sin(k * 2.9 + row * 2)
        pk = clay.sphere(1.0, (r0 * math.cos(ang), r0 * math.sin(ang), -8), pine_m, "Ridge", scale=(base, base, hgt), segs=24)
        bpy.ops.object.shade_smooth()

# ------------------------------------------------------------------ the hangar (door faces +X, toward the runway)
HX, HY = -50, 30
clay.box(26, 30, 0.06, (HX, HY, 0.03), conc, "HangarFloor", bevel=False)
metal = kit.matte("#AEB2B9", 0.6, "HangarClay")      # pale clay shell: the dark textured metal read as a black dome at dusk
clay.box(0.3, 30, 6, (HX - 13, HY, 3), metal, "HangarBack", bevel=False)
for sy in (-15, 15):
    clay.box(26, 0.3, 6, (HX, HY + sy, 3), metal, "HangarSide", bevel=False)
for sy in (-12.5, 12.5):
    clay.box(0.3, 5, 6, (HX + 13, HY + sy, 3), metal, "HangarFront", bevel=False)
clay.box(0.3, 30, 0.9, (HX + 13, HY, 5.55), metal, "HangarHeader", bevel=False)
# arched roof: a half-ellipse profile lofted front to back (a squashed cylinder read as a blimp)
arc = [(15.15 * math.cos(math.pi * i / 24), 6.0 + 3.6 * math.sin(math.pi * i / 24)) for i in range(25)]
roof = rt._loft("HangarRoof", [[(x, HY + y, z) for y, z in arc] for x in (HX - 13.3, HX + 13.3)], mats=[metal])
clay.box(0.2, 20, 5.1, (HX + 12.4, HY, 2.55), kit.matte("#020304", 1.0, "DoorDark"), "DoorDark", bevel=False)
clay.box(0.12, 6.5, 5.1, (HX + 13.2, HY + 6.6, 2.55), m["clay_d"], "DoorLeaf", bevel=False)   # one leaf left half shut
for ry in range(-14, 15, 2):                     # ribs on the front gable so it reads as sheet metal
    clay.box(0.08, 0.1, 6.0 if abs(ry) > 10 else 0.9, (HX + 13.2, HY + ry, 3.0 if abs(ry) > 10 else 5.55), m["clay_d"], "Rib", bevel=False)
kit.light("AREA", (HX + 30, HY - 8, 9), (HX + 13, HY, 4), power=5000, color="#AFC0E6", size=14, name="HangarFace")
# windsock pole by the runway
clay.cyl(0.07, 7, (11.5, 44, 3.5), trunk_m, "SockPole", verts=10)
sock = clay.cone(0.32, 1.6, (12.2, 44, 6.6), line_m, "Sock", verts=10)
sock.rotation_euler = (0, math.radians(108), 0)

# ------------------------------------------------------------------ the resort block (north end)
dark = m["dark"]
for (sx, sy, sz, x, y) in ((64, 18, 9, -62, 178), (18, 40, 7, -100, 168), (22, 14, 5, -22, 172)):
    clay.box(sx, sy, sz, (x, y, sz / 2), conc, "Resort")
    clay.box(sx + 0.5, sy + 0.5, 0.35, (x, y, sz + 0.17), m["clay_d"], "ResortRoof", bevel=False)
    for wz in range(2, int(sz) - 1, 3):
        nx = int(sx // 4)
        for i in range(nx):
            wx = x - sx / 2 + 2 + i * (sx - 4) / max(1, nx - 1)
            clay.box(1.5, 0.08, 1.4, (wx, y - sy / 2 - 0.01, wz + 0.3), dark, "Win", bevel=False)
clay.box(70, 26, 0.05, (-60, 152, 0.02), asph, "ResortLot", bevel=False)

# ------------------------------------------------------------------ people
def marshal(name, x, y, heading, walk=None, phase=0, gear=True):
    """White mannequin in tactical kit. walk = metres per second along heading (keys the whole shot)."""
    M = rt.real_mannequin(name, (x, y, 0), heading, m["man"])
    if gear:
        rt.tactical(M, name)
    if walk:
        d = walk * (N - 1) / FPS
        hx, hy = math.cos(math.radians(heading)), math.sin(math.radians(heading))
        kit.key(M["root"], "location", [(1, (x, y, 0)), (N, (x + d * hx, y + d * hy, 0))], ease="linear")
        rt.rwalk_cycle(M, 1, N, period=32, phase=phase)
    else:
        rt.rpose(M, "relaxed")
    return M


def subject(x, y, heading):
    M = rt.real_mannequin("Subject", (x, y, 0), heading, m["subject"])
    rt.cap(M)
    return M


def facing(frm, to):
    return math.degrees(math.atan2(to[1] - frm[1], to[0] - frm[0]))


LINE_X = (13, 19, 25, 31, 37)                    # the team in a line, working north up the east field
GROUND = (-46.0, 60.0)                           # where he ends up on the ground
STAMP = ("OCT 30, 2014", "6:07 PM  ·  NEAR TANNERSVILLE, PA")
cam = None

if SHOT == 1:
    cam = kit.camera((150, -330, 150), look_at=(-25, 40, 0), lens=30)
    kit.key(cam, "location", [(1, (150, -330, 150)), (N, (132, -296, 138))], ease="linear")
    rt.date_stamp(cam, STAMP[0], STAMP[1], start_frame=f(0.2))

elif SHOT == 2:
    cam = kit.camera((1.5, -150, 1.4), look_at=(-6, 60, 4), lens=26)
    kit.key(cam, "location", [(1, (1.5, -150, 1.4)), (N, (1.5, -128, 1.7))], ease="linear")
    rt.date_stamp(cam, STAMP[0], STAMP[1], start_frame=-300)

elif SHOT == 3:
    cam = kit.camera((-2, 2, 2.0), look_at=(HX + 4, HY, 4.2), lens=30)
    kit.key(cam, "location", [(1, (-2, 2, 2.0)), (N, (-8, 6, 2.2))], ease="linear")
    rt.date_stamp(cam, STAMP[0], STAMP[1], start_frame=-300)

elif SHOT == 5:
    for i, x in enumerate(LINE_X):
        marshal(f"M{i}", x, -62 - (i % 2) * 1.5, 90, walk=1.3, phase=i)
    cam = kit.camera((25, -48, 0.75), look_at=(25, -62, 1.35), lens=38)
    kit.key(cam, "location", [(1, (25, -48, 0.75)), (N, (25, -47.4, 0.8))], ease="linear")
    kit.depth_of_field(cam, focus=12, fstop=2.8)

elif SHOT == 6:
    for i, x in enumerate(LINE_X):
        marshal(f"M{i}", x, -58 - (i % 2) * 1.5, 90, walk=1.3, phase=i)
    cam = kit.camera((74, -84, 30), look_at=(22, -50, 0), lens=42)
    kit.key(cam, "location", [(1, (74, -84, 30)), (N, (70, -76, 28))], ease="linear")

elif SHOT == 7:
    for i, x in enumerate(LINE_X):
        marshal(f"M{i}", x, -54 - (i % 2) * 1.5, 90, walk=1.3, phase=i)
    cam = kit.camera((9.5, -51.5, 1.5), look_at=(19, -50.5, 1.35), lens=40)
    d = 1.3 * (N - 1) / FPS
    kit.key(cam, "location", [(1, (9.5, -51.5, 1.5)), (N, (9.5, -51.5 + d * 0.8, 1.5))], ease="linear")
    kit.key(kit.aim(cam), "location", [(1, (19, -50.5, 1.35)), (N, (19, -50.5 + d * 0.8, 1.35))], ease="linear")
    kit.depth_of_field(cam, focus=8.5, fstop=2.8)

elif SHOT == 8:
    cam = kit.camera((-4, 118, 2.2), look_at=(-62, 176, 4.5), lens=30)
    kit.key(cam, "location", [(1, (-4, 118, 2.2)), (N, (-9, 122, 2.4))], ease="linear")

elif SHOT == 9:
    for i, x in enumerate(LINE_X):
        marshal(f"M{i}", x, -40 - (i % 2) * 1.5, 90, walk=1.3, phase=i)
    cam = kit.camera((29, -58, 2.6), look_at=(18, 40, 2.0), lens=30)
    kit.key(cam, "location", [(1, (29, -58, 2.6)), (N, (28.4, -56.8, 2.7))], ease="linear")
    rt.date_stamp(cam, "ABOUT 2 HOURS IN", "CLEARING THE PROPERTY", start_frame=f(19.40))

elif SHOT == 11:
    # Malkowski and two of his team, walking from the runway across the apron to the hangar door
    for i, (x, y) in enumerate(((-9, 30), (-7, 32.4), (-6.5, 27.8))):
        marshal(f"M{i}", x, y, 180, walk=1.3, phase=i)
    cam = kit.camera((-2.5, 30.6, 1.7), look_at=(HX + 13, HY, 2.6), lens=34)
    kit.key(cam, "location", [(1, (-2.5, 30.6, 1.7)), (N, (-6.0, 30.6, 1.75))], ease="linear")
    kit.depth_of_field(cam, focus=6, fstop=4)

elif SHOT == 12:
    # their view north to the tree line; an amber shape moves between the trunks
    man = subject(-46, 80.5, -90)
    rt.rwalk_cycle(man, 1, N, period=34)
    kit.key(man["root"], "location", [(1, (-46, 81.5, 0)), (N, (-46, 81.5 - 1.2 * (N - 1) / FPS, 0))], ease="linear")
    cam = kit.camera((-42.5, 44, 1.7), look_at=(-46, 80, 2.6), lens=42)
    kit.key(cam, "location", [(1, (-42.5, 44, 1.7)), (N, (-43.0, 47.5, 1.7))], ease="linear")

elif SHOT == 13:
    man = subject(-46, 79, -90)
    rt.rwalk_cycle(man, 1, N, period=34)
    kit.key(man["root"], "location", [(1, (-46, 78.6, 0)), (N, (-46, 78.6 - 1.2 * (N - 1) / FPS, 0))], ease="linear")
    cam = kit.camera((-44.2, 68.5, 1.25), look_at=(-46, 77.5, 1.35), lens=45)
    kit.key(cam, "location", [(1, (-44.2, 68.5, 1.25)), (N, (-44.0, 68.0, 1.25))], ease="linear")
    kit.depth_of_field(cam, focus=9.5, fstop=2.8)

elif SHOT == 14:
    man = subject(-46, 72, -90)
    rt.rwalk_cycle(man, 1, N, period=34)
    kit.key(man["root"], "location", [(1, (-46, 72, 0)), (N, (-46, 72 - 1.2 * (N - 1) / FPS, 0))], ease="linear")
    for i, (x, y) in enumerate(((-24, 31), (-22, 33.2), (-21.5, 28.9))):
        Mx = marshal(f"M{i}", x, y, facing((x, y), (-46, 70)))
    cam = kit.camera((-6, 24, 16), look_at=(-44, 58, 0), lens=40)
    kit.key(cam, "location", [(1, (-6, 24, 16)), (N, (-7, 25, 15.6))], ease="linear")

elif SHOT == 17:
    man = subject(-46, 66, -90)
    rt.rwalk_cycle(man, 1, N, period=34)
    kit.key(man["root"], "location", [(1, (-46, 66, 0)), (N, (-46, 66 - 1.2 * (N - 1) / FPS, 0))], ease="linear")
    # behind and to one side of his head: the cap stays black, he stays amber, everything else grey
    head = kit.empty((0, 0, 1.84), "HeadAim")
    kit.parent(head, man["root"])
    rig = kit.empty((0, 0, 0), "CamRig")
    kit.parent(rig, man["root"])
    cam = kit.camera((0, 0, 0), look_at=head, lens=60)
    aim_e = kit.aim(cam)
    kit.parent(aim_e, man["root"])
    aim_e.location = (0.05, 0, 1.83)
    kit.parent(cam, man["root"])
    kit.key(cam, "location", [(1, (-1.45, 1.1, 1.98)), (N, (-1.2, 1.45, 1.95))], ease="linear")
    kit.depth_of_field(cam, focus=1.85, fstop=2.2)
    kit.light("AREA", (-44.4, 64.5, 2.6), (-46, 64.8, 1.8), power=160, color="#C9D6F2", size=1.2, name="CapKey")
    rt.quote(cam, ["“I SAW THE", "BLACK HAT.”"], "DEPUTY U.S. MARSHAL SCOTT MALKOWSKI", start_frame=f(38.62), d=1.85)       # d = the focus distance, so the words stay sharp

elif SHOT == 18:
    gx, gy = GROUND
    man = subject(gx, gy, -90)
    rt.rpose(man, "relaxed", frame=1)
    rt.rpose(man, "relaxed", frame=f(41.9))
    rt.rpose(man, "kneel", frame=f(43.3), ease="in_out")
    kit.key(man["root"], "location", [(1, (gx, gy, 0)), (f(41.9), (gx, gy, 0)), (f(43.3), (gx, gy, -rt.RDROP["kneel"]))],
            ease="in_out")
    spots = ((-42.6, 53.2), (-45.6, 53.0), (-49.4, 54.0))
    for i, (x, y) in enumerate(spots):
        marshal(f"M{i}", x, y, facing((x, y), GROUND))
    cam = kit.camera((-43.5, 50.0, 1.7), look_at=(-44.9, 60, 1.0), lens=32)
    kit.key(cam, "location", [(1, (-43.5, 50.0, 1.7)), (N, (-43.6, 50.7, 1.68))], ease="linear")

elif SHOT in (19, 20, 21):
    gx, gy = GROUND
    man = subject(gx, gy, -90)
    rt.prone(man, (gx, gy + 0.9), -90)            # face down, head to the south, arms out, hands open and empty
    ring = ((-43.3, 58.2), (-44.3, 61.6), (-47.6, 61.9), (-48.8, 58.6), (-46.2, 56.3))
    for i, (x, y) in enumerate(ring):
        marshal(f"M{i}", x, y, facing((x, y), (gx, gy)))
    if SHOT == 19:
        cam = kit.camera((-44.9, 56.4, 0.34), look_at=(gx, gy, 0.3), lens=32)
        kit.key(cam, "location", [(1, (-44.9, 56.4, 0.34)), (N, (-45.3, 56.6, 0.36))], ease="linear")
        kit.depth_of_field(cam, focus=3.4, fstop=2.8)
    elif SHOT == 20:
        # his left hand, flat on the ground, nothing in it
        hx, hy = gx + 0.83, gy - 0.5
        cam = kit.camera((hx + 0.05, hy - 0.05, 1.5), look_at=(hx, hy, 0.1), lens=50)
        kit.key(cam, "location", [(1, (hx + 0.05, hy - 0.05, 1.5)), (N, (hx + 0.05, hy - 0.05, 1.25))], ease="linear")
        kit.depth_of_field(cam, focus=1.3, fstop=4)
    else:
        cam = kit.camera((gx + 0.4, gy - 5.5, 3.2), look_at=(gx, gy - 0.1, 0.3), lens=30)
        kit.key(cam, "location", [(1, (gx + 0.4, gy - 5.5, 3.2)), (N, (gx + 0.2, gy - 3.2, 9.0))], ease="in_out")

cam.data.clip_end = 2500
kit.shake(cam, strength=0.012, speed=45)
rt.finish()
