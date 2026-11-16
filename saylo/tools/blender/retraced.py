"""Retraced look for Saylo Blender shots, on top of the shared clay setup (style-sheet §8 "Retraced look").

- Faceless mannequins: everyone matte white-gray, the subject one glossy amber-orange mannequin.
- Clean clay sets lit dark navy with practical lights (streetlights, headlights, flashlights).
- Glowing amber route lines that draw themselves across clay blocks.
- Typed-on text (typewriter rule): date stamps top-left, name tags lower-left, lettering built into the set.

Import from a scene script (run through the Documentary Pro runner, which puts blender_kit on the path):
    import sys, os
    sys.path.insert(0, r"<repo>/saylo/tools/blender")
    import retraced as rt
"""
import math
import os
import sys

import bpy
import blender_kit as kit

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLAY = os.path.normpath(os.path.join(_HERE, "..", "..", "videos", "01-olympic-bomber", "build", "blender"))
if _CLAY not in sys.path:
    sys.path.insert(0, _CLAY)
import clay  # noqa: E402  (shared clay look: box/cyl/sphere, streetlight, AMBER)

AMBER = clay.AMBER                 # route lines, labels, the lit key place
SUBJECT = "#E2852B"                # glossy amber-orange subject mannequin
WHITE = "#D9DCE1"                  # everyone else
NAVY = "#070B14"                   # world / sky
OFF_WHITE = "#F4F1EA"


# ------------------------------------------------------------------------------------------- look
def setup(bloom=0.3):
    """Start a Retraced shot: dark navy world, AgX, light bloom."""
    sc = kit.setup(world=NAVY, view="AgX", look="Medium High Contrast", bloom=bloom, motion_blur=0.3)
    return sc


def finish(vignette=0.5, grain=0.03, bloom=0.3):
    kit.post(bloom=bloom, vignette=vignette, grain=grain)


def night(moon=1.2, fill=900):
    """Cool navy moonlight + a soft navy sky fill. Practical lights do the rest."""
    kit.light("SUN", (0, 0, 30), (8, 20, 0), power=moon, color="#9FB3E0", name="Moon")
    kit.light("AREA", (-30, -40, 40), (0, 20, 0), power=fill * 40, color="#5D74B0", size=40, name="SkyFill")


def mats():
    m = clay.mats()
    m.update(
        ground=kit.matte("#8E8C88", 0.9, "Ground"),
        road=kit.matte("#4B4B4E", 0.95, "Road"),
        wall=kit.matte("#CFCCC5", 0.85, "Wall"),
        dumpster=kit.matte("#5E6660", 0.6, "Dumpster"),
        man=kit.matte(WHITE, 0.45, "Mannequin"),
        subject=kit.matte(SUBJECT, 0.16, "SubjectGloss"),
        tail=kit.emission("#FF2A1E", 3.0, "Taillight"),
        head=kit.emission("#FFF3D6", 4.0, "Headlight"),
        route=kit.emission(AMBER, 4.0, "Route"),
    )
    return m


# ------------------------------------------------------------------------------------------- mannequin
def _limb(parent, length, radius, mat, name, z0=0.0):
    """A smooth ellipsoid hanging down from a joint (joint at parent origin)."""
    ob = clay.sphere(1.0, (0, 0, z0 - length / 2), mat, name, scale=(radius, radius, length / 2 * 1.04), segs=20)
    bpy.ops.object.shade_smooth()
    kit.parent(ob, parent)
    return ob


def _joint(parent, loc, name):
    j = kit.empty(loc, name)
    j.rotation_mode = "XYZ"
    kit.parent(j, parent)
    return j


def mannequin(name, loc=(0, 0, 0), rot_z=0.0, mat=None):
    """Faceless mannequin, ~1.8 m, standing on loc, facing -Y rotated by rot_z degrees. Returns dict of joints.
    Joints (rotation_euler in degrees via pose()): root, spine, neck, sh_l, sh_r, el_l, el_r, hip_l, hip_r, kn_l, kn_r.
    Swing forward = negative X on shoulders/hips; knees bend with positive X; elbows bend with negative X."""
    root = kit.empty(loc, name)
    root.rotation_euler = (0, 0, math.radians(rot_z))
    J = {"root": root}
    spine = J["spine"] = _joint(root, (0, 0, 0.95), name + ".spine")
    # pelvis, belly, chest
    for z, s in ((0.0, (0.16, 0.11, 0.10)), (0.15, (0.135, 0.095, 0.13)), (0.33, (0.18, 0.115, 0.19))):
        p = clay.sphere(1.0, (0, 0, z), mat, name + ".torso", scale=s, segs=24)
        bpy.ops.object.shade_smooth()
        kit.parent(p, spine)
    neck = J["neck"] = _joint(spine, (0, 0, 0.5), name + ".neck")
    n = clay.cyl(0.045, 0.1, (0, 0, 0.04), mat, name + ".neckmesh", verts=16)
    kit.parent(n, neck)
    h = clay.sphere(1.0, (0, -0.01, 0.17), mat, name + ".head", scale=(0.092, 0.108, 0.125), segs=28)
    bpy.ops.object.shade_smooth()
    kit.parent(h, neck)
    for side, sx in (("l", 1), ("r", -1)):
        sh = J["sh_" + side] = _joint(spine, (0.2 * sx, 0, 0.46), f"{name}.sh_{side}")
        clay.sphere(0.055, (0, 0, 0), mat, name + ".shoulder").parent = sh
        _limb(sh, 0.29, 0.046, mat, name + ".uarm")
        el = J["el_" + side] = _joint(sh, (0, 0, -0.29), f"{name}.el_{side}")
        _limb(el, 0.26, 0.038, mat, name + ".farm")
        clay.sphere(1.0, (0, 0, -0.3), mat, name + ".hand", scale=(0.035, 0.05, 0.06)).parent = el
        hp = J["hip_" + side] = _joint(root, (0.09 * sx, 0, 0.93), f"{name}.hip_{side}")
        _limb(hp, 0.44, 0.072, mat, name + ".thigh")
        kn = J["kn_" + side] = _joint(hp, (0, 0, -0.44), f"{name}.kn_{side}")
        _limb(kn, 0.43, 0.05, mat, name + ".shin")
        clay.sphere(1.0, (0, -0.06, -0.45), mat, name + ".foot", scale=(0.045, 0.11, 0.035)).parent = kn
    return J


POSES = {
    "stand": {},
    "sit": {"hip_l": (-88, 0, 0), "hip_r": (-88, 0, 0), "kn_l": (88, 0, 0), "kn_r": (88, 0, 0),
            "sh_l": (-55, 0, 0), "sh_r": (-55, 0, 0), "el_l": (-35, 0, 0), "el_r": (-35, 0, 0)},
    "crouch": {"spine": (28, 0, 0), "hip_l": (-85, 0, 4), "hip_r": (-75, 0, -4), "kn_l": (125, 0, 0),
               "kn_r": (115, 0, 0), "sh_l": (-35, 0, 8), "sh_r": (-45, 0, -8), "el_l": (-70, 0, 0),
               "el_r": (-60, 0, 0), "neck": (-18, 0, 0)},
    "flashlight": {"sh_r": (-80, 0, 0), "el_r": (-10, 0, 0), "sh_l": (-10, 0, 0)},
    "hands_up": {"sh_l": (-165, 0, 12), "sh_r": (-165, 0, -12), "el_l": (-25, 0, 0), "el_r": (-25, 0, 0)},
}
# root height drop per pose so the feet stay on the ground
DROP = {"sit": 0.42, "crouch": 0.46}


def pose(J, name_or_dict, frame=None, ease="in_out"):
    """Set (and key at frame) a pose. Joints not named go back to 0."""
    p = POSES[name_or_dict] if isinstance(name_or_dict, str) else name_or_dict
    for j, ob in J.items():
        if j == "root":
            continue
        ob.rotation_euler = tuple(math.radians(v) for v in p.get(j, (0, 0, 0)))
        if frame is not None:
            kit.key(ob, "rotation_euler", [(frame, tuple(ob.rotation_euler))], ease=ease)


def run_cycle(J, f0, f1, period=18, lean=14):
    """Key a running cycle on the limbs between f0 and f1 (move the root yourself)."""
    f = f0
    i = 0
    while f <= f1:
        s = 1 if i % 2 == 0 else -1
        pose(J, {"spine": (lean, 0, 0), "neck": (-lean * 0.6, 0, 0),
                 "hip_l": (-40 * s, 0, 0), "hip_r": (40 * s, 0, 0),
                 "kn_l": (25 if s > 0 else 95, 0, 0), "kn_r": (95 if s > 0 else 25, 0, 0),
                 "sh_l": (45 * s, 0, 0), "sh_r": (-45 * s, 0, 0),
                 "el_l": (-85, 0, 0), "el_r": (-85, 0, 0)}, frame=f, ease="smooth")
        f += period // 2
        i += 1


# ------------------------------------------------------------------------------------------- real assets (CC0)
# Downloaded by saylo/tools/fetch_polyhaven.py and the mannequin zip (see _kit/assets/*/SOURCE.txt); not in git.
REPO = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
ASSETS = os.path.join(REPO, "_kit", "assets")
MANNEQUIN_GLB = os.path.join(ASSETS, "mannequin", "male_base_mesh.glb")


def _desaturate(mat, sat=0.35):
    """Retraced sets are near-monochrome: pull the colour out of a textured material (keeps its detail)."""
    if not mat or not mat.use_nodes:
        return
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if not bsdf or not bsdf.inputs["Base Color"].is_linked:
        return
    link = bsdf.inputs["Base Color"].links[0]
    hs = nt.nodes.new("ShaderNodeHueSaturation")
    hs.inputs["Saturation"].default_value = sat
    nt.links.new(link.from_socket, hs.inputs["Color"])
    nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])


def _import_gltf(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def model(aid, loc=(0, 0, 0), rot_z=0.0, scale=1.0, sat=0.35, name=None):
    """A Poly Haven model (_kit/assets/polyhaven/<aid>/*.gltf) under one empty at loc, turned rot_z degrees."""
    d = os.path.join(ASSETS, "polyhaven", aid)
    path = next(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".gltf"))
    objs = _import_gltf(path)
    root = kit.empty(loc, name or aid)
    for o in objs:
        if o.parent is None:
            o.parent = root
        if o.type == "MESH":
            for s in o.material_slots:
                if s.material and not s.material.get("_desat"):
                    _desaturate(s.material, sat)
                    s.material["_desat"] = 1
    root.rotation_euler = (0, 0, math.radians(rot_z))
    root.scale = (scale,) * 3
    return root


def instancer(aid, sat=0.35):
    """Import a Poly Haven model once into a hidden collection; returns place(loc, rot_z=0, scale=1) that drops
    cheap collection instances of it (streetlights along a whole street, rows of bins)."""
    d = os.path.join(ASSETS, "polyhaven", aid)
    path = next(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".gltf"))
    objs = _import_gltf(path)
    col = bpy.data.collections.new("INST_" + aid)
    for o in objs:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
        if o.type == "MESH":
            for s in o.material_slots:
                if s.material and not s.material.get("_desat"):
                    _desaturate(s.material, sat)
                    s.material["_desat"] = 1

    def place(loc, rot_z=0.0, scale=1.0, name=None):
        e = bpy.data.objects.new(name or aid, None)
        e.instance_type, e.instance_collection = "COLLECTION", col
        e.location, e.rotation_euler, e.scale = loc, (0, 0, math.radians(rot_z)), (scale,) * 3
        bpy.context.scene.collection.objects.link(e)
        return e
    return place


def pbr(aid, scale=1.0, sat=0.35, name=None):
    """Tiling PBR material from a Poly Haven texture folder, box-projected on object coordinates (no UVs needed)."""
    d = os.path.join(ASSETS, "polyhaven", aid)
    files = os.listdir(d)
    pick = lambda key: next((os.path.join(d, f) for f in files if key in f.lower()), None)
    mat = bpy.data.materials.new(name or aid)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1 / scale,) * 3
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])

    def tex(path, non_color=False):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(path, check_existing=True)
        t.projection, t.projection_blend = "BOX", 0.25
        if non_color:
            t.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
        return t
    diff = pick("diff")
    if diff:
        hs = nt.nodes.new("ShaderNodeHueSaturation")
        hs.inputs["Saturation"].default_value = sat
        nt.links.new(tex(diff).outputs["Color"], hs.inputs["Color"])
        nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])
    rough = pick("rough")
    if rough:
        nt.links.new(tex(rough, True).outputs["Color"], bsdf.inputs["Roughness"])
    nor = pick("nor_gl")
    if nor:
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(tex(nor, True).outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


# Real mannequin (CC0 rigged base mesh, Rigify metarig). Imported facing +X, soles at z=-1; wrapped in a root empty
# that stands on loc and faces -Y turned by rot_z (same convention as mannequin()).
# Bone rotations are in each bone's own axes (degrees): thigh/shin X- = forward / X+ = knee bend;
# upper_arm/forearm X+ = forward / elbow bend; upper_arm.L Z+ / upper_arm.R Z- = out to the side; spine X+ = lean in.
RPOSES = {
    "stand": {"upper_arm.L": (0, 0, -8), "upper_arm.R": (0, 0, 8)},
    "sit": {"thigh.L": (-90, 0, 0), "thigh.R": (-90, 0, 0), "shin.L": (90, 0, 0), "shin.R": (90, 0, 0),
            "upper_arm.L": (55, 0, -10), "upper_arm.R": (55, 0, 10), "forearm.L": (35, 0, 0), "forearm.R": (35, 0, 0)},
    "crouch": {"spine.001": (22, 0, 0), "spine.002": (12, 0, 0), "spine.004": (-15, 0, 0),
               "thigh.L": (-105, 0, 6), "thigh.R": (-92, 0, -6), "shin.L": (135, 0, 0), "shin.R": (125, 0, 0),
               "foot.L": (-25, 0, 0), "foot.R": (-25, 0, 0),
               "upper_arm.L": (40, 0, -5), "upper_arm.R": (50, 0, 5), "forearm.L": (70, 0, 0), "forearm.R": (60, 0, 0)},
    "flashlight": {"upper_arm.R": (80, 0, 0), "forearm.R": (10, 0, 0), "upper_arm.L": (10, 0, -6)},
    "hands_up": {"upper_arm.L": (150, 0, 22), "upper_arm.R": (150, 0, -22), "forearm.L": (25, 0, 0),
                 "forearm.R": (25, 0, 0)},
}
RDROP = {"crouch": 0.5, "sit": 0.0}


def real_mannequin(name, loc=(0, 0, 0), rot_z=0.0, mat=None, subsurf=1):
    objs = _import_gltf(MANNEQUIN_GLB)
    arm = next(o for o in objs if o.type == "ARMATURE")
    for o in objs:
        if o.type == "MESH" and o.name.startswith("Icosphere"):
            bpy.data.objects.remove(o, do_unlink=True)
    body = next(o for o in bpy.data.objects if o.parent == arm and o.type == "MESH")
    body.name, arm.name = name + ".body", name + ".rig"
    if mat:
        kit.assign(body, mat)
    for p in body.data.polygons:
        p.use_smooth = True
    if subsurf:
        sm = body.modifiers.new("Smooth", "SUBSURF")
        sm.levels = sm.render_levels = subsurf          # after the Armature modifier the import made
    root = kit.empty(loc, name)
    arm.parent = root
    arm.location = (0, 0, 1.0)
    arm.rotation_euler = (0, 0, math.radians(-90))
    root.rotation_euler = (0, 0, math.radians(rot_z))
    for pb in arm.pose.bones:
        pb.rotation_mode = "XYZ"
    return {"root": root, "arm": arm, "body": body}


def rpose(M, p, frame=None, ease="in_out"):
    """Pose the real mannequin from a dict (or RPOSES name); bones not named go back to rest."""
    p = RPOSES[p] if isinstance(p, str) else p
    for pb in M["arm"].pose.bones:
        if pb.name.startswith(("f_", "thumb")):
            continue
        pb.rotation_euler = tuple(math.radians(v) for v in p.get(pb.name, (0, 0, 0)))
        if frame is not None:
            pb.keyframe_insert("rotation_euler", frame=frame)
    if frame is not None:
        for fc in kit._fcurves(M["arm"]):
            for kp in fc.keyframe_points:
                if round(kp.co[0]) == round(frame):
                    kp.interpolation, kp.easing = kit.EASES[ease]


def rrun_cycle(M, f0, f1, period=12, lean=14):
    f, i = f0, 0
    while f <= f1:
        s = 1 if i % 2 == 0 else -1
        rpose(M, {"spine.001": (lean, 0, 0), "spine.004": (-lean * 0.5, 0, 0),
                  "thigh.L": (-45 * s, 0, 0), "thigh.R": (45 * s, 0, 0),
                  "shin.L": (20 if s > 0 else 100, 0, 0), "shin.R": (100 if s > 0 else 20, 0, 0),
                  "upper_arm.L": (-40 * s, 0, -8), "upper_arm.R": (40 * s, 0, 8),
                  "forearm.L": (85, 0, 0), "forearm.R": (85, 0, 0)}, frame=f, ease="smooth")
        f += period // 2
        i += 1


def volume_fog(density=0.012, color="#8FA3CC"):
    """Thin atmosphere so light beams read (world volume)."""
    w = bpy.context.scene.world
    nt = w.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
    vol = nt.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Density"].default_value = density
    vol.inputs["Color"].default_value = kit.rgb(color)
    nt.links.new(vol.outputs[0], out.inputs["Volume"])
    ee = bpy.context.scene.eevee
    for attr, val in (("volumetric_end", 60.0), ("volumetric_tile_size", "4"), ("use_volumetric_shadows", True)):
        if hasattr(ee, attr):
            try:
                setattr(ee, attr, val)
            except Exception:
                pass


# ------------------------------------------------------------------------------------------- props
def car(m, loc, rot_z, body="clay", name="Car"):
    """Clay patrol car with an open cabin (a mannequin can sit inside and be seen). Front faces local -Y.
    Returns (root, dict of head/tail light objects and the seat position)."""
    root = kit.empty(loc, name)
    root.rotation_euler = (0, 0, math.radians(rot_z))
    parts = [clay.box(1.8, 4.6, 0.62, (0, 0, 0.58), m[body], name + ".body"),
             clay.box(1.7, 2.1, 0.07, (0, 0.25, 1.6), m[body], name + ".roof"),
             clay.box(0.9, 0.35, 0.1, (0, 0.25, 1.68), m["clay_d"], name + ".lightbar"),
             clay.box(1.5, 0.5, 0.16, (0, -0.85, 0.95), m["clay_d"], name + ".dash")]
    for x in (-0.82, 0.82):
        for y in (-0.8, 1.3):
            parts.append(clay.box(0.07, 0.07, 0.76, (x, y, 1.2), m[body], name + ".pillar", bevel=False))
        for y in (-1.45, 1.45):
            parts.append(clay.cyl(0.33, 0.24, (x * 1.0, y, 0.33), m["dark"], name + ".wheel", rot=(0, 90, 0)))
    lights = {}
    for x in (-0.62, 0.62):
        hl = clay.sphere(0.09, (x, -2.3, 0.72), m["head"], name + ".hl")
        tl = clay.box(0.3, 0.05, 0.12, (x, 2.31, 0.75), m["tail"], name + ".tl", bevel=False)
        parts += [hl, tl]
        lights.setdefault("head", []).append(hl)
    for p in parts:
        kit.parent(p, root)
    spot_t = kit.empty((0, -14, 0), name + ".beamtarget")
    kit.parent(spot_t, root)
    beam = kit.light("SPOT", (0, -2.4, 0.75), spot_t, power=9000, color="#FFF0D0", size=1.0, name=name + ".beam")
    beam.data.spot_size = math.radians(70)
    kit.parent(beam, root)
    lights["beam"] = beam
    lights["seat"] = (0.4, 0.15, 0.55)     # driver seat, local to the car
    return root, lights


def lights_off(lights, frame, dur=4):
    """Headlights off at frame."""
    kit.key(lights["beam"].data, "energy", [(frame, lights["beam"].data.energy), (frame + dur, 0.0)], ease="linear")
    mat = lights["head"][0].active_material
    node = next((n for n in mat.node_tree.nodes if n.type == "EMISSION"), None)
    if node:
        kit.key(node.inputs["Strength"], "default_value", [(frame, node.inputs["Strength"].default_value),
                                                          (frame + dur, 0.0)], ease="linear")


def route_line(points, mat, f0, f1, depth=0.18, name="Route"):
    """Glowing route line through points [(x, y, z), ...] that draws itself from f0 to f1."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution = depth, 4
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points):
        p.co = (co[0], co[1], co[2], 1.0)
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    kit.assign(ob, mat)
    kit.key(cu, "bevel_factor_end", [(f0, 0.0), (f1, 1.0)], ease="in_out")
    return ob


def flashlight(holder_loc, target, power=6000, name="Flash"):
    return kit.light("SPOT", holder_loc, target, power=power, color="#F4F7FF", size=0.3, name=name)


# ------------------------------------------------------------------------------------------- typed text
_TYPED = []


def _type_handler(scene, *_):
    fr = round(scene.frame_current + scene.frame_subframe)
    fps = scene.render.fps
    for t in _TYPED:
        ob = bpy.data.objects.get(t["obj"])
        if ob is None:
            continue
        el = (fr - t["f0"]) / fps
        if el < 0:
            ob.data.body = " "
            continue
        n = min(len(t["full"]), int(el * t["cps"]) + 1)
        body = t["full"][:n]
        done_at = len(t["full"]) / t["cps"]
        blink = t["blinks"] * 0.5
        if el < done_at + blink and t["cursor"]:
            on = el < done_at or int((el - done_at) / 0.25) % 2 == 0
            body += "|" if on else " "
        ob.data.body = body


def typed(text_obj, start_frame, cps=30, blinks=3, cursor=True):
    """Typewriter reveal (style-sheet rule): letters type on at cps, a blinking cursor for `blinks` blinks, then gone."""
    _TYPED.append(dict(obj=text_obj.name, full=text_obj.data.body, f0=start_frame, cps=cps, blinks=blinks, cursor=cursor))
    if _type_handler not in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.append(_type_handler)
    _type_handler(bpy.context.scene)
    return text_obj


def hud(cam, d=4.0):
    """An empty fixed to the camera d metres ahead, plus the half width/height of the frame there (16:9)."""
    h = kit.empty((0, 0, -d), cam.name + ".hud")
    kit.parent(h, cam)
    half_w = d * 18.0 / cam.data.lens
    return h, half_w, half_w * 9 / 16


def date_stamp(cam, line, sub=None, start_frame=1, d=4.0):
    """Big white bold caps, top-left (Retraced), typed on. sub: a small amber line under it."""
    h, hw, hh = hud(cam, d)
    size = hh * 0.2
    x, y = -hw + hw * 0.07, hh - hh * 0.24
    t = kit.text(line, font="Montserrat-Bold", size=size, spacing=1.05, color="#FFFFFF", strength=1.7, align="LEFT",
                 loc=(x, y, 0), rot=(0, 0, 0), name="DateStamp")
    kit.parent(t, h)
    typed(t, start_frame)
    if sub:
        s = kit.text(sub, font="Montserrat-Bold", size=size * 0.38, spacing=1.2, color=AMBER, strength=1.6, align="LEFT",
                     loc=(x, y - size * 0.85, 0), rot=(0, 0, 0), name="DateSub")
        kit.parent(s, h)
        typed(s, start_frame + int(len(line) / 30 * bpy.context.scene.render.fps) + 2, cursor=False)
    return t


def name_tag(cam, name, role, start_frame=1, d=4.0):
    """Name tag lower-left: Anton caps off-white name, small amber role line, on a dark plate (typed on)."""
    h, hw, hh = hud(cam, d)
    size = hh * 0.11
    x, y = -hw + hw * 0.07, -hh + hh * 0.3
    plate = kit.rect(size * (0.62 * len(name) + 0.9), size * 1.75, material=kit.emission("#0B0D12", 1.0, "TagPlate"),
                     loc=(x - size * 0.3, y - size * 0.25, -0.01), rot=(0, 0, 0), anchor="left", name="TagPlate")
    bar = kit.rect(size * 0.07, size * 1.75, AMBER, loc=(x - size * 0.3, y - size * 0.25, -0.005), rot=(0, 0, 0),
                   anchor="left", name="TagBar")
    nm = kit.text(name, font="Anton-Regular", size=size, spacing=1.05, color=OFF_WHITE, strength=1.6, align="LEFT",
                  loc=(x, y + size * 0.12, 0), rot=(0, 0, 0), name="TagName")
    rl = kit.text(role, font="Montserrat-Bold", size=size * 0.36, spacing=1.2, color=AMBER, strength=1.6, align="LEFT",
                  loc=(x, y - size * 0.62, 0), rot=(0, 0, 0), name="TagRole")
    for ob in (plate, bar, nm, rl):
        kit.parent(ob, h)
    kit.fade(plate, [(start_frame - 4, 0.0), (start_frame, 0.92)])
    kit.fade(bar, [(start_frame - 4, 0.0), (start_frame, 1.0)])
    typed(nm, start_frame)
    typed(rl, start_frame + int(len(name) / 30 * bpy.context.scene.render.fps) + 3, cursor=False)
    return nm
