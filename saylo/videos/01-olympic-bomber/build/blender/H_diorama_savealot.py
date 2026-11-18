"""Clay diorama: the back lot of a small-town grocery store at 3:30 AM (an illustration of the place, not a replica).

Matte white-gray clay, dark surroundings, amber the only colour (the approved thumbnail look). What's in it is only
what the record supports: the store's back wall and loading door, dumpsters, a security light, a parking lot, a patrol
car with its lights off, wooded mountains behind, and one crouched figure by the dumpsters (amber, faceless).
Camera: a slow, low orbit toward the figure with tilt-shift depth of field.
  --arg focus=figure|car   (what the shot ends on)
"""
import math
import bpy
import blender_kit as kit

a = kit.args()
end = a.frames
AMBER = "#E0A040"
CLAY, CLAY_D, ASPH = "#D9D6CF", "#B9B5AD", "#6F6C68"

kit.setup(world="#050506", view="Standard", bloom=0.25)
clay = kit.matte(CLAY, 0.85, "Clay")
clay_d = kit.matte(CLAY_D, 0.85, "ClayDark")
asph = kit.matte(ASPH, 0.95, "Asphalt")
amber_m = kit.matte(AMBER, 0.6, "AmberClay")

def box(sx, sy, sz, loc, mat, name, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name, ob.scale, ob.rotation_euler = name, (sx, sy, sz), tuple(math.radians(r) for r in rot)
    bpy.ops.object.transform_apply(scale=True)
    bev = ob.modifiers.new("Bevel", "BEVEL")
    bev.width, bev.segments = min(sx, sy, sz) * 0.08, 2
    kit.assign(ob, mat)
    return ob

def cyl(r, h, loc, mat, name, rot=(0, 0, 0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc,
                                        rotation=tuple(math.radians(x) for x in rot))
    ob = bpy.context.active_object
    ob.name = name
    kit.assign(ob, mat)
    return ob

def sphere(r, loc, mat, name, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=12)
    ob = bpy.context.active_object
    ob.name, ob.scale = name, scale
    kit.assign(ob, mat)
    return ob

# --- the diorama base: a thick clay slab that ends in the dark (so it reads as a miniature)
box(16, 12, 0.6, (0, 0, -0.3), clay_d, "Base")
box(15.6, 8.2, 0.04, (0, -1.6, 0.02), asph, "Lot")
for i in range(7):                                   # faded parking lines
    box(0.06, 1.5, 0.01, (-5.4 + i * 1.6, -4.4, 0.05), clay, f"Line{i}")

# --- the store: long low box, flat roof with a parapet, loading door + dock, back door, security light
store = box(11, 4.2, 3.0, (0, 4.0, 1.5), clay, "Store")
box(11.2, 4.4, 0.25, (0, 4.0, 3.12), clay_d, "Parapet")
box(2.6, 0.12, 2.2, (2.8, 1.86, 1.1), clay_d, "LoadingDoor")
box(3.2, 1.0, 0.7, (2.8, 1.4, 0.35), clay_d, "Dock")
box(0.9, 0.1, 1.9, (-3.2, 1.86, 0.95), clay_d, "BackDoor")
for x in (-4.6, -1.0, 4.6):                           # roof units
    box(0.9, 0.9, 0.5, (x, 4.6, 3.5), clay_d, f"RoofUnit{x}")
lamp = box(0.35, 0.25, 0.18, (-1.2, 1.78, 2.55), clay, "WallLamp")
kit.light("SPOT", (-1.2, 1.5, 2.45), (-1.6, -1.2, 0), power=1400, color="#FFCF8A", size=0.3, name="SecurityLight")

# --- dumpsters (two), lids slightly open
for i, x in enumerate((-5.6, -4.0)):
    box(1.4, 1.0, 1.0, (x, 1.0, 0.55), clay_d, f"Dumpster{i}")
    box(1.45, 1.05, 0.08, (x, 0.95, 1.1), clay, f"Lid{i}", rot=(-8, 0, 0))

# --- light pole in the lot
cyl(0.06, 4.2, (5.8, -3.0, 2.1), clay_d, "Pole")
box(0.9, 0.3, 0.12, (5.45, -3.0, 4.2), clay, "PoleHead")
kit.light("SPOT", (5.3, -3.0, 4.05), (5.0, -2.6, 0), power=900, color="#FFCF8A", size=0.4, name="PoleLight")

# --- patrol car, lights off: body, cabin, light bar, wheels (clay, no markings)
car = kit.empty((4.6, -2.6, 0), "Car")
parts = [box(2.6, 1.2, 0.55, (0, 0, 0.55), clay, "CarBody"), box(1.4, 1.05, 0.45, (-0.15, 0, 1.02), clay, "CarCabin"),
         box(0.5, 0.9, 0.1, (-0.15, 0, 1.3), clay_d, "LightBar")]
for dx in (-0.85, 0.85):
    for dy in (-0.62, 0.62):
        parts.append(cyl(0.26, 0.2, (dx, dy, 0.28), clay_d, "Wheel", rot=(90, 0, 0)))
for p in parts:
    kit.parent(p, car)
car.rotation_euler = (0, 0, math.radians(165))

# --- the man standing in the lot by the dumpsters (amber, faceless): hood up, hands in pockets
fig = kit.empty((-2.6, -0.2, 0), "Figure")
fparts = [sphere(0.13, (0.0, 0.0, 1.66), amber_m, "Head", scale=(1.0, 1.05, 1.12)),
          cyl(0.19, 0.72, (0.0, 0.0, 1.16), amber_m, "Torso"),
          cyl(0.075, 0.82, (-0.09, 0.0, 0.41), amber_m, "LegL"),
          cyl(0.075, 0.82, (0.09, 0.0, 0.41), amber_m, "LegR"),
          cyl(0.055, 0.6, (-0.24, 0.02, 1.12), amber_m, "ArmL", rot=(0, 8, 0)),
          cyl(0.055, 0.6, (0.24, 0.02, 1.12), amber_m, "ArmR", rot=(0, -8, 0))]
for p_ in fparts:
    kit.parent(p_, fig)
fig.rotation_euler = (0, 0, math.radians(-20))
fig.scale = (1.0, 1.0, 1.0)

# --- wooded mountains behind: clay cones on the base, then dark ridges
import random
random.seed(7)
for i in range(46):
    x, y = random.uniform(-7.6, 7.6), random.uniform(6.6, 9.6)
    h = random.uniform(1.0, 2.2)
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=h * 0.32, depth=h, location=(x, y, h / 2))
    kit.assign(bpy.context.active_object, clay_d)
for i, (x, s) in enumerate(((-6, 9), (2, 11), (9, 8))):
    sphere(1.0, (x, 22, -2.0), kit.matte("#2A2927", 1.0, f"Ridge{i}"), f"Ridge{i}", scale=(s, 3.0, 5.5))

# --- light: dim cool moonlight + the warm practicals; dark surroundings
kit.light("SUN", (0, 0, 10), (2, 6, 0), power=0.55, color="#B8C6E4", name="Moon")
kit.light("AREA", (-10, -10, 12), (0, 1, 0), power=1500, color="#D6DEEE", size=10, name="Key")

# --- camera: low, slow orbit toward the figure (or the car), tilt-shift DOF
target = fig if a.get("focus", "figure") == "figure" else car
tx, ty = target.location.x, target.location.y
cam = kit.camera((tx - 15.0, ty - 21.0, 15.0), look_at=(0.5, 1.5, 0.5), lens=50)
kit.key(cam, "location", [(1, (tx - 15.0, ty - 21.0, 15.0)), (end, (tx - 8.5, ty - 13.5, 9.0))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (0.5, 1.5, 0.5)), (end, (tx + 0.3, ty + 0.3, 0.5))], ease="in_out")
kit.shake(cam, strength=0.008, speed=40)
dof = kit.depth_of_field(cam, focus=28.0, fstop=0.45)
kit.key(dof, "focus_distance", [(1, 28.5), (end, 17.6)], ease="in_out")
kit.post(bloom=0.35, vignette=0.7, grain=0.045)
