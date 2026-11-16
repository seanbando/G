"""Thumbnail B still: "hard to catch". Night clay mountains with pine forest, a helicopter searchlight sweeping
the ridges (right), one tiny amber campsite in a ravine OUTSIDE the beam (lower left-centre). Top-left sky kept
dark and empty for the overlay text ("200 AGENTS" + arrow to the camp, added by make_thumbnail.py).
    powershell -File build/blender/render.ps1 T_thumb_hunt.py thumb_hunt 1 1 --size 2560x1440
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import blender_kit as kit
import clay

a = kit.args()
kit.setup(world="#030304", view="Standard", bloom=0.3)
kit.backdrop("#030304", center="#0C1018", distance=70)
m = clay.mats()
gz = clay.mountains(m)

# Night: a low cold moon from behind-left (rim on the ridges), very little fill, so the scene reads dark gray
kit.light("SUN", (0, 0, 10), (-3, 8, 0), power=0.5, color="#AFC0E0", name="Moon")
kit.light("AREA", (-12, -14, 10), (0, 2, 0), power=220, color="#C9D3E6", size=12, name="Fill")

# Pine forest: small dark-clay cones on the slopes (skip the ravine floor where the camp sits)
pine = kit.matte("#6E6B66", 0.9, "Pine")
random.seed(11)
CAMP = (-2.0, -1.5)
for _ in range(1400):
    x, y = random.uniform(-11.5, 11.5), random.uniform(-7.5, 7.5)
    if math.hypot(x - CAMP[0], y - CAMP[1]) < 1.0 or (abs(x - CAMP[0]) < 0.6 and y < CAMP[1]):   # clearing + sightline
        continue
    z = gz(x, y)
    h = random.uniform(0.35, 0.7)
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=h * 0.3, depth=h, location=(x, y, z + h / 2 - 0.05))
    kit.assign(bpy.context.active_object, pine)

# The campsite: a tiny amber tent + ember glow, the only warm colour
cx, cy = CAMP
cz = gz(cx, cy)
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.3, depth=0.34, location=(cx, cy, cz + 0.17), rotation=(0, 0, math.radians(30)))
kit.assign(bpy.context.active_object, kit.emission(clay.AMBER, 2.6, "Tent"))
clay.sphere(0.03, (cx + 0.3, cy - 0.12, cz + 0.04), kit.emission("#FFB347", 5.0, "Ember"), "Ember")
kit.light("POINT", (cx + 0.3, cy - 0.2, cz + 0.4), (cx, cy, cz), power=22, color="#F39A2B", size=0.2, name="CampGlow")

# Helicopter (upper right, in frame) + searchlight on the ridges away from the camp
hx, hy, hz = 3.8, -5.0, 5.0
S, YAW = 0.8, math.radians(205)       # built straight in world space (parenting distorted the parts)
def W(lx, ly, lz):
    c, s = math.cos(YAW), math.sin(YAW)
    return (hx + S * (lx * c - ly * s), hy + S * (lx * s + ly * c), hz + S * lz)
heli_mat = kit.matte("#CFCBC3", 0.7, "HeliClay")
parts = [clay.sphere(0.55 * S, W(0, 0, 0), heli_mat, "Body", scale=(1.5, 0.95, 0.85)),
         clay.cyl(0.11 * S, 2.3 * S, W(1.85, 0, 0.12), heli_mat, "Tail", rot=(0, 90, math.degrees(YAW))),
         clay.box(0.07 * S, 0.45 * S, 0.55 * S, W(2.95, 0, 0.35), heli_mat, "Fin", rot=(0, 0, math.degrees(YAW))),
         clay.cyl(0.07 * S, 0.25 * S, W(0, 0, 0.62), m["clay_d"], "Mast"),
         clay.box(3.6 * S, 0.12 * S, 0.03 * S, W(0, 0, 0.76), m["clay_d"], "BladeA", rot=(0, 0, 20)),
         clay.box(3.6 * S, 0.12 * S, 0.03 * S, W(0, 0, 0.76), m["clay_d"], "BladeB", rot=(0, 0, 110)),
         clay.box(1.7 * S, 0.06 * S, 0.06 * S, W(0, 0.48, -0.62), m["clay_d"], "SkidL", rot=(0, 0, math.degrees(YAW))),
         clay.box(1.7 * S, 0.06 * S, 0.06 * S, W(0, -0.48, -0.62), m["clay_d"], "SkidR", rot=(0, 0, math.degrees(YAW)))]
parts[0].rotation_euler = (0, 0, YAW)
for p in parts:
    p.visible_shadow = False
tx, ty = 3.0, 1.2                    # beam target: a ridge well away from the camp
tz = gz(tx, ty)
kit.light("POINT", (hx - 1.5, hy - 1.5, hz + 1.0), (hx, hy, hz), power=120, color="#C9D3E6", size=1.0, name="HeliRim")
sp = kit.light("SPOT", (hx, hy, hz - 0.45), (tx, ty, tz), power=14000, color="#EEF2FF", size=0.15, name="Search")
sp.data.spot_size, sp.data.spot_blend = math.radians(16), 0.25
# visible beam: a soft emissive cone from the helicopter to the ground
hz -= 0.45                             # beam starts under the helicopter body
L = math.dist((hx, hy, hz), (tx, ty, tz))
bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=L * math.tan(math.radians(8)), radius2=0.08, depth=L,
                                location=((hx + tx) / 2, (hy + ty) / 2, (hz + tz) / 2))
beam = bpy.context.active_object
d = (hx - tx, hy - ty, hz - tz)
beam.rotation_euler = (0, math.acos(d[2] / L), math.atan2(d[1], d[0]))
kit.assign(beam, kit.emission("#DDE6FF", 0.7, "Beam"))
kit.fade(beam, [(1, 0.10)])
beam.visible_shadow = False

CAM = (-3.0, -17.0, 7.2)
cam = kit.camera(CAM, look_at=(0.6, 0.0, 2.4), lens=40)
kit.depth_of_field(cam, focus=math.dist(CAM, (cx, cy, cz)), fstop=4.0)
kit.post(bloom=0.45, vignette=0.7, grain=0.02)
