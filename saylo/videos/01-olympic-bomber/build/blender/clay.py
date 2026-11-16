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


def night_light(moon=0.55, key=1500):
    kit.light("SUN", (0, 0, 10), (2, 6, 0), power=moon, color="#B8C6E4", name="Moon")
    kit.light("AREA", (-10, -10, 12), (0, 1, 0), power=key, color="#D6DEEE", size=10, name="Key")
