"""Shared clay-diorama helpers for the Saylo look (matte white-gray clay, dark surroundings, amber accent).
Import from a scene script:  import sys, os; sys.path.insert(0, os.path.dirname(__file__)); import clay
"""
import math
import random
import bpy
import blender_kit as kit

AMBER = "#E0A040"
CLAY, CLAY_D, ASPH = "#D9D6CF", "#B9B5AD", "#6F6C68"


def mats():
    return dict(clay=kit.matte(CLAY, 0.85, "Clay"), clay_d=kit.matte(CLAY_D, 0.85, "ClayDark"),
                asph=kit.matte(ASPH, 0.95, "Asphalt"), amber=kit.matte(AMBER, 0.6, "AmberClay"),
                glow=kit.emission("#FFC978", 2.2, "Glow"), dark=kit.matte("#3A3936", 0.9, "Window"))


def box(sx, sy, sz, loc, mat, name="Box", rot=(0, 0, 0), bevel=True):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name, ob.scale, ob.rotation_euler = name, (sx, sy, sz), tuple(math.radians(r) for r in rot)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        b = ob.modifiers.new("Bevel", "BEVEL")
        b.width, b.segments = min(sx, sy, sz) * 0.08, 2
    kit.assign(ob, mat)
    return ob


def cyl(r, h, loc, mat, name="Cyl", rot=(0, 0, 0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc,
                                        rotation=tuple(math.radians(x) for x in rot))
    ob = bpy.context.active_object
    ob.name = name
    kit.assign(ob, mat)
    return ob


def sphere(r, loc, mat, name="Sphere", scale=(1, 1, 1), segs=24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=segs, ring_count=segs // 2)
    ob = bpy.context.active_object
    ob.name, ob.scale = name, scale
    kit.assign(ob, mat)
    return ob


def cone(r, h, loc, mat, name="Cone", verts=10):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, depth=h, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    kit.assign(ob, mat)
    return ob


def trees(n, xr, yr, mat, seed=7, hr=(1.0, 2.2)):
    random.seed(seed)
    for _ in range(n):
        h = random.uniform(*hr)
        cone(h * 0.32, h, (random.uniform(*xr), random.uniform(*yr), h / 2), mat)


def streetlight(x, y, m, power=700, face=1):
    cyl(0.05, 3.4, (x, y, 1.7), m["clay_d"], "Pole")
    box(0.7, 0.22, 0.1, (x + 0.3 * face, y, 3.4), m["clay"], "Arm")
    sphere(0.09, (x + 0.6 * face, y, 3.3), m["glow"], "Bulb")
    kit.light("SPOT", (x + 0.6 * face, y, 3.25), (x + 0.6 * face, y, 0), power=power, color="#FFCF8A", size=0.5, name="Lamp")


def patrol_car(loc, rot_z, m, mat_key="clay"):
    car = kit.empty(loc, "Car")
    parts = [box(2.6, 1.2, 0.5, (0, 0, 0.5), m[mat_key], "CarBody"), box(1.3, 1.05, 0.42, (-0.2, 0, 0.94), m[mat_key], "CarCabin"),
             box(0.45, 0.9, 0.09, (-0.2, 0, 1.2), m["clay_d"], "LightBar")]
    for dx in (-0.85, 0.85):
        for dy in (-0.62, 0.62):
            parts.append(cyl(0.25, 0.2, (dx, dy, 0.26), m["clay_d"], "Wheel", rot=(90, 0, 0)))
    for p in parts:
        kit.parent(p, car)
    car.rotation_euler = (0, 0, math.radians(rot_z))
    return car


def mountains(m):
    """The western-NC ridge terrain used by every mountains shot (same seed = same ridges). Returns ground_z(x, y)."""
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=220, y_subdivisions=160, size=1, location=(0, 0, 0))
    terr = bpy.context.active_object
    terr.scale = (24, 16, 1)
    bpy.ops.object.transform_apply(scale=True)
    tex = bpy.data.textures.new("Ridges", "CLOUDS")
    tex.noise_scale, tex.noise_depth, tex.noise_basis = 2.6, 3, "ORIGINAL_PERLIN"
    disp = terr.modifiers.new("Disp", "DISPLACE")
    disp.texture, disp.strength, disp.mid_level = tex, 4.2, 0.5
    sm = terr.modifiers.new("Smooth", "SMOOTH")
    sm.factor, sm.iterations = 1.0, 6
    kit.assign(terr, m["clay"])
    bpy.ops.object.shade_smooth()
    box(24.4, 16.4, 1.2, (0, 0, -1.4), m["clay_d"], "Base")

    def ground_z(x, y):
        dg = bpy.context.evaluated_depsgraph_get()
        ok, loc, *_ = bpy.context.scene.ray_cast(dg, (x, y, 30), (0, 0, -1))
        return loc.z if ok else 0.0
    return ground_z


# map positions on the mountains slab (schematic): Murphy west, Andrews ~15 mi NE, Topton beyond
TOWNS = {"MURPHY": (-6.5, -2.5), "ANDREWS": (-0.8, 0.6), "TOPTON": (4.0, 3.0)}


def pin(m, ground_z, x, y, label, t0, side=1, size=0.7):
    z = ground_z(x, y)
    post = cyl(0.04, 1.6, (x, y, z + 0.8), m["amber"], "PinPost")
    head = sphere(0.16, (x, y, z + 1.65), kit.emission(AMBER, 2.0, "PinHead"), "PinHead")
    for ob, zz in ((post, z + 0.8), (head, z + 1.65)):
        kit.key(ob, "location", [(t0 - 6, (x, y, zz + 2.5)), (t0 + 4, (x, y, zz))], ease="expo")
        kit.fade(ob, [(t0 - 6, 0.0), (t0, 1.0)])
    tx = kit.text(label, font="Montserrat-Bold", size=size, spacing=1.15, color="#F4F1EA", strength=1.4,
                  align="LEFT" if side > 0 else "RIGHT", loc=(x + 0.3 * side, y, z + 1.95), rot=(70, 0, 0), name=label)
    kit.fade(tx, [(t0 + 2, 0.0), (t0 + 10, 1.0)])
    tx.visible_shadow = False
    return z


def night_light(moon=0.55, key=1500):
    kit.light("SUN", (0, 0, 10), (2, 6, 0), power=moon, color="#B8C6E4", name="Moon")
    kit.light("AREA", (-10, -10, 12), (0, 1, 0), power=key, color="#D6DEEE", size=10, name="Key")
