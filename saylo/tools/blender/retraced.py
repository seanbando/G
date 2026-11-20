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


# Real mannequin (CC0 rigged base mesh, Rigify metarig). Wrapped in a root empty that stands on loc.
# FACING: at rot_z=0 it faces +X (measured), so it faces the direction at angle rot_z (degrees from +X):
# rot_z = math.degrees(math.atan2(dy, dx)) to face (dx, dy). Driver in a car whose front is local -Y: rot_z=-90.
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
    "drive": {"spine.001": (-8, 0, 0), "thigh.L": (-80, 0, 4), "thigh.R": (-80, 0, -4), "shin.L": (22, 0, 0),
              "shin.R": (22, 0, 0), "foot.L": (-10, 0, 0), "foot.R": (-10, 0, 0),
              "upper_arm.L": (62, 0, -12), "upper_arm.R": (62, 0, 12), "forearm.L": (30, 0, 0), "forearm.R": (30, 0, 0)},
    "flashlight": {"upper_arm.R": (80, 0, 0), "forearm.R": (10, 0, 0), "upper_arm.L": (10, 0, -6)},
    "hands_up": {"upper_arm.L": (150, 0, 22), "upper_arm.R": (150, 0, -22), "forearm.L": (25, 0, 0),
                 "forearm.R": (25, 0, 0)},
}
RPOSES.update({
    # one knee down (right), left foot forward, arms a little away from the body
    "kneel": {"thigh.L": (-92, 0, 0), "shin.L": (92, 0, 0), "thigh.R": (-4, 0, 0), "shin.R": (92, 0, 0),
              "foot.R": (35, 0, 0), "upper_arm.L": (12, 0, -20), "upper_arm.R": (12, 0, 20),
              "forearm.L": (10, 0, 0), "forearm.R": (10, 0, 0)},
    # lying face down, arms out to the sides with open hands (use with prone())
    "prone": {"upper_arm.L": (11, 0, 62), "upper_arm.R": (11, 0, -62), "forearm.L": (9, 0, 0), "forearm.R": (9, 0, 0),
              "hand.L": (-14, 0, 0), "hand.R": (-14, 0, 0),      # arms down onto the ground, hands flat
              "spine.004": (-12, 0, 0), "foot.L": (40, 0, 0), "foot.R": (40, 0, 0)},
})
RPOSES["relaxed"] = {"upper_arm.L": (4, 0, -24), "upper_arm.R": (4, 0, 24), "forearm.L": (14, 0, 0), "forearm.R": (14, 0, 0)}
RDROP = {"crouch": 0.5, "sit": 0.0, "kneel": 0.47}


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


def rwalk_cycle(M, f0, f1, period=32, phase=0, lean=4):
    """Walking cycle on the real mannequin between f0 and f1 (move the root yourself, about 1.3 m/s)."""
    f, i = f0 - period, phase
    while f <= f1 + period:
        s = 1 if i % 2 == 0 else -1
        rpose(M, {"spine.001": (lean, 0, 0),
                  "thigh.L": (-24 * s, 0, 0), "thigh.R": (24 * s, 0, 0),
                  "shin.L": (6 if s > 0 else 36, 0, 0), "shin.R": (36 if s > 0 else 6, 0, 0),
                  "upper_arm.L": (-16 * s, 0, -24), "upper_arm.R": (16 * s, 0, 24),
                  "forearm.L": (18, 0, 0), "forearm.R": (18, 0, 0)}, frame=f, ease="smooth")
        f += period // 2
        i += 1


def prone(M, loc, rot_z):
    """Lay the real mannequin face down at loc (feet at loc, head toward the direction rot_z, degrees from +X)."""
    rpose(M, "prone")
    M["root"].rotation_mode = "XYZ"
    M["root"].location = (loc[0], loc[1], 0.17)
    M["root"].rotation_euler = (0, math.radians(90), math.radians(rot_z))


def attach(ob, M, bone):
    """Fix a prop to one bone of the real mannequin, keeping where it is now. Call it in the rest pose, before rpose()."""
    import mathutils
    bpy.context.view_layer.update()
    arm = M["arm"]
    pb = arm.pose.bones[bone]
    ob.parent, ob.parent_type, ob.parent_bone = arm, "BONE", bone
    ob.matrix_parent_inverse = (arm.matrix_world @ pb.matrix @ mathutils.Matrix.Translation((0, pb.bone.length, 0))).inverted()
    return ob


def _on_body(M, ob, bone):
    """ob was built in the mannequin's own frame (stands at 0, faces +X): move it onto M and fix it to bone."""
    bpy.context.view_layer.update()
    ob.matrix_world = M["root"].matrix_world @ ob.matrix_world
    return attach(ob, M, bone)


def _dome(loc, radii, mat, name):
    """Upper half of an ellipsoid (rim at loc.z): a helmet shell or a close-fitting cap over the head."""
    import bmesh
    ob = clay.sphere(1.0, loc, mat, name, segs=28)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.02], context="VERTS")
    bm.to_mesh(ob.data)
    bm.free()
    ob.scale = radii
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def tactical(M, name="Gear"):
    """Tactical kit for a white mannequin: helmet and a plate-carrier vest with pouches, in dark matte grey."""
    g = kit.matte("#3C4047", 0.7, "GearGrey")
    g2 = kit.matte("#2B2E33", 0.75, "GearDark")
    # head of the base mesh: centre (0, 0, 1.85), about 0.21 deep, 0.17 wide, top at 1.95
    helmet = _dome((-0.006, 0, 1.83), (0.123, 0.102, 0.133), g, name + ".helmet")
    _on_body(M, helmet, "spine.005")
    vest = clay.box(0.31, 0.36, 0.36, (0.025, 0, 1.43), g, name + ".vest")
    _on_body(M, vest, "spine.003")
    for y in (-0.11, 0.0, 0.11):
        _on_body(M, clay.box(0.06, 0.085, 0.14, (0.2, y, 1.36), g2, name + ".pouch"), "spine.003")
    _on_body(M, clay.box(0.08, 0.26, 0.2, (-0.16, 0, 1.47), g2, name + ".pack"), "spine.003")
    return helmet


def cap(M, color="#040404", name="Cap"):
    """A plain close-fitting dark cap on the mannequin's head (no brim: the hat's shape is not in the record)."""
    c = _dome((-0.006, 0, 1.8), (0.13, 0.106, 0.192), kit.matte(color, 0.85, name), name)   # pulled down to the ears
    return _on_body(M, c, "spine.005")


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


def _loft(name, rings, mat_idx=None, mats=None):
    """Mesh through closed rings of equal length (each a list of (x, y, z)); caps both ends."""
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [[bm.verts.new(p) for p in r] for r in rings]
    n = len(rings[0])
    for a, b in zip(vs, vs[1:]):
        for i in range(n):
            bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    bm.faces.new(list(reversed(vs[0])))
    bm.faces.new(vs[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    for mt in mats or []:
        me.materials.append(mt)
    return ob


def _strut(p0, p1, r, mat, name):
    """Round bar between two points (pillars, push bar)."""
    import mathutils
    a, b = mathutils.Vector(p0), mathutils.Vector(p1)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=(b - a).length, location=(a + b) / 2)
    ob = bpy.context.active_object
    ob.name = name
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = (b - a).to_track_quat("Z", "Y")
    kit.assign(ob, mat)
    return ob


def police_car(m, loc, rot_z, name="Patrol"):
    """Detailed procedural police sedan (no CC0 model exists). Same contract as car(): front faces local -Y,
    returns (root, {"head", "beam", "seat"}). Tinted glass all round so a seated mannequin reads through it.
    Lightbar lenses are unlit (we don't show emergency lights the record doesn't mention)."""
    root = kit.empty(loc, name)
    root.rotation_euler = (0, 0, math.radians(rot_z))
    paint = kit.matte("#E3E6EA", 0.28, name + ".Paint")
    pb = next(n for n in paint.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    for k, v in (("Coat Weight", 0.6), ("Coat Roughness", 0.05), ("Metallic", 0.1)):
        if k in pb.inputs:
            pb.inputs[k].default_value = v
    black = kit.matte("#16181C", 0.3, name + ".Black")
    trim = kit.matte("#0C0D0F", 0.6, name + ".Trim")
    rubber = kit.matte("#101012", 0.85, name + ".Tyre")
    chrome = kit.matte("#B8BCC2", 0.18, name + ".Rim")
    cp = next(n for n in chrome.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    cp.inputs["Metallic"].default_value = 1.0
    glass = bpy.data.materials.new(name + ".Glass")
    glass.use_nodes = True
    gp = next(n for n in glass.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    gp.inputs["Base Color"].default_value = (0.02, 0.025, 0.035, 1)
    gp.inputs["Roughness"].default_value = 0.04
    gp.inputs["Alpha"].default_value = 0.32
    for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        if hasattr(glass, attr):
            try:
                setattr(glass, attr, val)
            except Exception:
                pass
    red = kit.matte("#5A0E10", 0.2, name + ".LensR")
    blue = kit.matte("#0E1E5A", 0.2, name + ".LensB")
    parts = []

    # lower body: side profile (y, z) lofted across the width, with wheel arches; bevelled + smoothed
    W, R_ARCH, WB = 0.93, 0.43, 1.45
    prof = [(-2.47, 0.32), (-2.5, 0.55), (-2.42, 0.74), (-2.2, 0.84), (-1.0, 0.93), (1.6, 0.96), (2.3, 0.94),
            (2.47, 0.84), (2.5, 0.58), (2.45, 0.32)]
    arches = []
    for cy in (WB, -WB):
        arc = [(cy + R_ARCH * math.cos(t), 0.36 + R_ARCH * math.sin(t))
               for t in [math.pi * i / 10 for i in range(0, 11)]]
        arches.append(arc)
    bottom = [(1.95, 0.32)] + arches[0] + [(0.95, 0.32), (-0.95, 0.32)] + arches[1] + [(-1.95, 0.32)]
    loop = prof + bottom
    rings = [[(x, y, z) for y, z in loop] for x in (-W, -W + 0.05, W - 0.05, W)]
    for i, s in ((0, 0.97), (3, 0.97)):                 # slight tumblehome at the very sides
        rings[i] = [(x, y * s + 0.0, z) for x, y, z in rings[i]]
    body = _loft(name + ".body", rings, mats=[paint])
    bv = body.modifiers.new("Bevel", "BEVEL")
    bv.width, bv.segments, bv.limit_method = 0.05, 3, "ANGLE"
    parts.append(body)
    for p in body.data.polygons:
        p.use_smooth = True
    # black-and-white door panels and dark sills
    for sx in (-1, 1):
        parts.append(clay.box(0.02, 2.0, 0.42, (sx * (W + 0.005), 0.0, 0.6), black, name + ".door"))
        parts.append(clay.box(0.03, 1.9, 0.08, (sx * (W + 0.01), 0.0, 0.36), trim, name + ".sill", bevel=False))
        parts.append(clay.box(0.015, 0.003, 0.42, (sx * (W + 0.02), 0.05, 0.6), trim, name + ".seam", bevel=False))
        parts.append(clay.box(0.03, 0.14, 0.03, (sx * (W + 0.02), -0.25, 0.78), chrome, name + ".handle", bevel=False))
        parts.append(clay.box(0.03, 0.14, 0.03, (sx * (W + 0.02), 0.75, 0.78), chrome, name + ".handle", bevel=False))
        parts.append(clay.box(0.14, 0.2, 0.1, (sx * (W + 0.07), -0.88, 1.08), black, name + ".mirror"))

    # greenhouse: tinted glass loft + painted roof + pillars
    g_bot = [(-0.86, -0.9, 0.94), (0.86, -0.9, 0.94), (0.86, 1.55, 0.97), (-0.86, 1.55, 0.97)]
    g_top = [(-0.7, -0.1, 1.47), (0.7, -0.1, 1.47), (0.7, 0.95, 1.47), (-0.7, 0.95, 1.47)]
    gl = _loft(name + ".glass", [g_bot, g_top], mats=[glass])
    parts.append(gl)
    parts.append(clay.box(1.44, 1.1, 0.05, (0, 0.42, 1.485), paint, name + ".roof"))
    for sx in (-1, 1):
        parts.append(_strut((sx * 0.86, -0.9, 0.94), (sx * 0.7, -0.1, 1.47), 0.035, black, name + ".Apillar"))
        parts.append(_strut((sx * 0.85, 0.62, 0.96), (sx * 0.71, 0.62, 1.47), 0.04, black, name + ".Bpillar"))
        parts.append(_strut((sx * 0.86, 1.55, 0.97), (sx * 0.7, 0.95, 1.47), 0.05, paint, name + ".Cpillar"))
        parts.append(_strut((sx * 0.86, -0.9, 0.95), (sx * 0.86, 1.55, 0.97), 0.02, trim, name + ".belt"))
    # interior: dash, steering wheel, seats (reads through the tinted glass)
    parts.append(clay.box(1.62, 0.5, 0.2, (0, -0.95, 0.88), trim, name + ".dash"))
    parts.append(_strut((0.4, -0.72, 0.86), (0.4, -0.56, 1.0), 0.025, trim, name + ".column"))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.018, location=(0.4, -0.55, 1.02),
                                     rotation=(math.radians(62), 0, 0))
    wheel = bpy.context.active_object
    wheel.name = name + ".steering"
    kit.assign(wheel, trim)
    parts.append(wheel)
    for sx in (0.4, -0.4):
        parts.append(clay.box(0.52, 0.5, 0.12, (sx, 0.32, 0.5), trim, name + ".seat"))
        parts.append(clay.box(0.52, 0.12, 0.62, (sx, 0.66, 0.82), trim, name + ".seatback", rot=(-12, 0, 0)))
    # lightbar (unlit)
    parts.append(clay.box(1.25, 0.3, 0.06, (0, 0.2, 1.53), trim, name + ".lb_base"))
    parts.append(clay.box(0.6, 0.26, 0.1, (-0.31, 0.2, 1.6), red, name + ".lb_r"))
    parts.append(clay.box(0.6, 0.26, 0.1, (0.31, 0.2, 1.6), blue, name + ".lb_b"))
    # front: grille, push bar, plate; rear: bumper, plate
    parts.append(clay.box(1.0, 0.04, 0.2, (0, -2.5, 0.62), trim, name + ".grille"))
    parts.append(clay.box(1.7, 0.1, 0.16, (0, -2.5, 0.38), black, name + ".bumperF"))
    parts.append(clay.box(1.7, 0.1, 0.16, (0, 2.5, 0.42), black, name + ".bumperR"))
    for sx in (-0.45, 0.45):
        parts.append(_strut((sx, -2.72, 0.32), (sx, -2.72, 0.8), 0.035, black, name + ".pushbar"))
    parts.append(_strut((-0.45, -2.72, 0.72), (0.45, -2.72, 0.72), 0.03, black, name + ".pushbar"))
    parts.append(_strut((-0.45, -2.72, 0.45), (0.45, -2.72, 0.45), 0.03, black, name + ".pushbar"))
    for sx in (-0.45, 0.45):
        parts.append(_strut((sx, -2.72, 0.6), (sx, -2.5, 0.6), 0.025, black, name + ".pushbar"))
    # wheels: tyre, rim, hub
    for sx in (-1, 1):
        for cy in (-WB, WB):
            parts.append(clay.cyl(0.34, 0.24, (sx * 0.8, cy, 0.34), rubber, name + ".wheel", rot=(0, 90, 0), verts=32))
            parts.append(clay.cyl(0.21, 0.02, (sx * 0.925, cy, 0.34), chrome, name + ".rim", rot=(0, 90, 0), verts=24))
            parts.append(clay.cyl(0.06, 0.03, (sx * 0.935, cy, 0.34), trim, name + ".hub", rot=(0, 90, 0), verts=12))
    lights = {}
    for x in (-0.66, 0.66):
        hl = clay.box(0.34, 0.05, 0.11, (x, -2.475, 0.72), m["head"], name + ".hl", bevel=False)
        tl = clay.box(0.36, 0.05, 0.12, (x, 2.475, 0.8), m["tail"], name + ".tl", bevel=False)
        parts += [hl, tl]
        lights.setdefault("head", []).append(hl)
    for p in parts:
        kit.parent(p, root)
    spot_t = kit.empty((0, -14, 0), name + ".beamtarget")
    kit.parent(spot_t, root)
    beam = kit.light("SPOT", (0, -2.6, 0.72), spot_t, power=9000, color="#FFF0D0", size=1.0, name=name + ".beam")
    beam.data.spot_size = math.radians(70)
    kit.parent(beam, root)
    lights["beam"] = beam
    lights["seat"] = (0.4, 0.3, 0.54)         # driver hip point; real_mannequin root z = seat z - 0.95, pose "drive"
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


def date_stamp(cam, line, sub=None, start_frame=1, d=4.0, cps=30, sub_cps=30):
    """Big white bold caps, top-left (Retraced), typed on. sub: a small amber line under it."""
    h, hw, hh = hud(cam, d)
    size = hh * 0.2
    x, y = -hw + hw * 0.07, hh - hh * 0.24
    t = kit.text(line, font="Montserrat-Bold", size=size, spacing=1.05, color="#FFFFFF", strength=1.7, align="LEFT",
                 loc=(x, y, 0), rot=(0, 0, 0), name="DateStamp")
    kit.parent(t, h)
    typed(t, start_frame, cps=cps)
    if sub:
        s = kit.text(sub, font="Montserrat-Bold", size=size * 0.38, spacing=1.2, color=AMBER, strength=1.6, align="LEFT",
                     loc=(x, y - size * 0.85, 0), rot=(0, 0, 0), name="DateSub")
        kit.parent(s, h)
        typed(s, start_frame + int(len(line) / cps * bpy.context.scene.render.fps) + 2, cps=sub_cps, cursor=False)
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


def quote(cam, lines, who, start_frame=1, d=4.0, y=-0.18, cps=22):
    """Retraced quote: white lines with an amber bar on the left, typed on; a small amber attribution under it."""
    h, hw, hh = hud(cam, d)
    size = hh * 0.135
    x = -hw + hw * 0.1
    y0 = hh * y
    n = len(lines)
    bar = kit.rect(size * 0.09, size * (1.25 * n + 0.75), AMBER, loc=(x - size * 0.45, y0 - size * 0.62 * (n - 1) - size * 0.2, 0),
                   rot=(0, 0, 0), name="QuoteBar")
    kit.parent(bar, h)
    kit.fade(bar, [(start_frame - 4, 0.0), (start_frame, 1.0)])
    fr = start_frame
    fps = bpy.context.scene.render.fps
    for i, ln in enumerate(lines):
        t = kit.text(ln, font="Montserrat-Bold", size=size, spacing=1.04, color="#FFFFFF", strength=1.7, align="LEFT",
                     loc=(x, y0 - i * size * 1.25, 0), rot=(0, 0, 0), name=f"Quote{i}")
        kit.parent(t, h)
        typed(t, fr, cps=cps, cursor=(i == n - 1))
        fr += int(len(ln) / cps * fps) + 1
    w = kit.text(who, font="Montserrat-Bold", size=size * 0.34, spacing=1.2, color=AMBER, strength=1.6, align="LEFT",
                 loc=(x, y0 - n * size * 1.25 + size * 0.1, 0), rot=(0, 0, 0), name="QuoteWho")
    kit.parent(w, h)
    typed(w, fr + 3, cursor=False)
    return bar


# ------------------------------------------------------------------------------------------- v2: closer to Retraced
def sky(name, strength=1.0, rot_z=0.0, sat=1.0):
    """Light the set with a real sky (Poly Haven HDRI in _kit/assets/polyhaven/hdri/<name>.hdr, CC0)."""
    w = bpy.context.scene.world
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(os.path.join(ASSETS, "polyhaven", "hdri", name + ".hdr"), check_existing=True)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(rot_z))
    hs = nt.nodes.new("ShaderNodeHueSaturation")
    hs.inputs["Saturation"].default_value = sat
    bg.inputs["Strength"].default_value = strength
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], hs.inputs["Color"])
    nt.links.new(hs.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs[0], out.inputs["Surface"])
    return bg


def gloss(color, rough=0.22, coat=0.7, name="Gloss"):
    """Shop-mannequin plastic: smooth, a clear coat on top."""
    mt = kit.matte(color, rough, name)
    pb = next(n for n in mt.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    for k, v in (("Coat Weight", coat), ("Coat Roughness", 0.06)):
        if k in pb.inputs:
            pb.inputs[k].default_value = v
    return mt


def garment(M, groups, zmin, zmax, mat, grow=0.02, name="Garment", share=0.5, exclude=False):
    """Clothing cut from the mannequin's own mesh, so it fits and bends with every pose: the faces that belong to
    the bones in `groups` and sit between zmin and zmax (metres above the feet, rest pose), pushed out by `grow`."""
    import bmesh
    bpy.context.view_layer.update()
    body = M["body"]
    g = body.copy()
    g.data = body.data.copy()
    g.name = name
    for c in body.users_collection:
        c.objects.link(g)
    idx = {vg.index for vg in g.vertex_groups if vg.name in groups}
    to_root = M["root"].matrix_world.inverted() @ body.matrix_world
    bm = bmesh.new()
    bm.from_mesh(g.data)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)   # finer mesh = a clean hem line
    bm.verts.ensure_lookup_table()
    dl = bm.verts.layers.deform.active
    drop = []
    for v in bm.verts:
        w = v[dl]
        tot = sum(w.values()) or 1.0
        z = (to_root @ v.co).z
        part = sum(val for k, val in w.items() if k in idx) / tot
        if exclude:
            part = 1.0 - part
        if part < share or not (zmin <= z <= zmax):
            drop.append(v)
    bmesh.ops.delete(bm, geom=drop, context="VERTS")
    bm.to_mesh(g.data)
    bm.free()
    g.data.materials.clear()
    g.data.materials.append(mat)
    d = g.modifiers.new("Grow", "DISPLACE")
    d.direction, d.strength, d.mid_level = "NORMAL", grow, 0.0
    return g


def marshal_kit(M, name="Kit", lettering=("POLICE", "U.S. MARSHAL")):
    """Fitted tactical kit: dark vest and trousers cut from the body, a helmet shell cut from the head."""
    dark = kit.matte("#23262B", 0.75, "KitDark")
    mid = kit.matte("#3A3E45", 0.8, "KitMid")
    arms = ("upper_arm.L", "upper_arm.R", "forearm.L", "forearm.R", "hand.L", "hand.R")
    garment(M, arms, 1.06, 1.635, dark, 0.034, name + ".vest", share=0.25, exclude=True)        # everything but the arms
    for x, w in ((0.185, 0.3), (-0.145, 0.32)):                                               # plate carrier front and back
        _on_body(M, clay.box(0.05, w, 0.34, (x, 0, 1.39), dark, name + ".plate"), "spine.003")
    for y in (-0.1, 0.0, 0.1):
        _on_body(M, clay.box(0.05, 0.08, 0.12, (0.225, y, 1.3), mid, name + ".pouch"), "spine.003")
    if lettering:                                      # what a marshal's vest carries: POLICE front, U.S. MARSHAL back
        ink = kit.matte("#E6E6E2", 0.7, "VestInk")
        fr = kit.text(lettering[0], font="Montserrat-Bold", size=0.062, spacing=1.1, material=ink, align="CENTER",
                      loc=(0.2115, 0, 1.475), rot=(90, 0, 90), name=name + ".front")
        bk = kit.text(lettering[1], font="Montserrat-Bold", size=0.043, spacing=1.08, material=ink, align="CENTER",
                      loc=(-0.1715, 0, 1.45), rot=(90, 0, -90), name=name + ".back")
        for t in (fr, bk):
            t.visible_shadow = False
            _on_body(M, t, "spine.003")
    garment(M, arms, 0.09, 1.16, mid, 0.016, name + ".trousers", share=0.55, exclude=True)
    _on_body(M, _dome((-0.006, 0, 1.835), (0.125, 0.106, 0.132), dark, name + ".helmet"), "spine.005")    # hard shell
    _on_body(M, clay.box(0.035, 0.2, 0.012, (0.105, 0, 1.842), dark, name + ".brim", bevel=False), "spine.005")


def beanie(M, color="#050505", name="Hat"):
    """The black hat as a close-fitting knit cap cut from the head mesh (shape is not in the record: kept plain)."""
    return garment(M, ("upper_arm.L", "upper_arm.R"), 1.855, 2.2, kit.matte(color, 0.9, name), 0.016, name, exclude=True)


def tree_library(blend="trees.blend"):
    """Poly Haven fir and pine scans prepared once into _kit/assets/<blend>: trees.blend = light (prep_trees.py),
    trees_mid.blend = hero trees that keep their needles (prep_trees_mid.py). Returns {name: place(loc, rot_z, height)}."""
    path = os.path.join(ASSETS, blend)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = list(src.collections)
    out = {}
    for col in dst.collections:
        zs = [(o.matrix_world @ mathutils_vec(c)).z for o in col.objects for c in o.bound_box]
        h = max(zs) - min(zs) or 1.0

        def place(loc, rot_z=0.0, height=15.0, col=col, h=h):
            e = bpy.data.objects.new(col.name, None)
            e.instance_type, e.instance_collection = "COLLECTION", col
            e.location, e.rotation_euler, e.scale = loc, (0, 0, math.radians(rot_z)), (height / h,) * 3
            bpy.context.scene.collection.objects.link(e)
            return e
        out[col.name] = place
    return out


def mathutils_vec(c):
    import mathutils
    return mathutils.Vector(c)


def haze(center, size, density=0.004, color="#9FB0CF"):
    """A box of thin haze over the set (bounded, so the sky still lights the scene)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    ob = bpy.context.active_object
    ob.name, ob.scale = "Haze", size
    mt = bpy.data.materials.new("Haze")
    mt.use_nodes = True
    nt = mt.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    vol = nt.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Density"].default_value = density
    vol.inputs["Color"].default_value = kit.rgb(color)
    nt.links.new(vol.outputs[0], out.inputs["Volume"])
    ob.data.materials.append(mt)
    ob.visible_shadow = False
    return ob


def autumn_woods(seed=3):
    """Stylised woods like the reference (blob canopies on trunks, a few dark pines), in muted late-October colours so
    amber stays the colour of the subject alone. Returns a list of place(loc, rot_z, height) functions, one per shape."""
    import random as _r
    rnd = _r.Random(seed)
    trunk = kit.matte("#2E2A27", 0.9, "TrunkBark")
    leaf = [kit.matte(c, 0.95, f"Leaf{i}") for i, c in enumerate(("#2C2320", "#2F2A20", "#272523", "#22281F", "#30251D", "#292623"))]
    pine = kit.matte("#1A231E", 0.95, "PineDark")
    tex = bpy.data.textures.new("LeafLumps", "CLOUDS")
    tex.noise_scale = 1.3
    out = []

    def collect(parts, name):
        col = bpy.data.collections.new(name)
        for o in parts:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            col.objects.link(o)

        def place(loc, rot_z=0.0, height=14.0, col=col):
            e = bpy.data.objects.new(col.name, None)
            e.instance_type, e.instance_collection = "COLLECTION", col
            e.location, e.rotation_euler, e.scale = loc, (0, 0, math.radians(rot_z)), (height / 14.0,) * 3
            bpy.context.scene.collection.objects.link(e)
            return e
        return place

    for v in range(6):                                 # broadleaf: trunk, limbs, lumpy canopy
        m = leaf[v % len(leaf)]
        parts = [clay.cyl(0.2, 6.0, (0, 0, 3.0), trunk, "Trunk", verts=8)]
        for k in range(12):                            # canopy starts low and overlaps, so it reads as a mass, not a lollipop
            ang, rad = rnd.uniform(0, math.tau), rnd.uniform(0.3, 3.0)
            z = rnd.uniform(3.6, 12.5)
            r = rnd.uniform(1.8, 3.0) * (1.0 - 0.035 * abs(z - 8.5))
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=r, location=(rad * math.cos(ang), rad * math.sin(ang), z))
            b = bpy.context.active_object
            b.scale = (1, 1, rnd.uniform(0.7, 0.95))
            sub = b.modifiers.new("Round", "SUBSURF")
            sub.levels = sub.render_levels = 1
            d = b.modifiers.new("Lumps", "DISPLACE")
            d.texture, d.strength = tex, 0.9
            for pl in b.data.polygons:
                pl.use_smooth = True
            kit.assign(b, m if k % 3 else leaf[(v + 2) % len(leaf)])
            parts.append(b)
            if k % 3 == 0:
                parts.append(_strut((0, 0, 2.8), (rad * 0.7 * math.cos(ang), rad * 0.7 * math.sin(ang), z - r * 0.5), 0.08, trunk, "Limb"))
        out.append(collect(parts, f"Broadleaf{v}"))
    for v in range(3):                                 # white pine: tall trunk, soft dark tiers
        parts = [clay.cyl(0.22, 5.0, (0, 0, 2.5), trunk, "Trunk", verts=8)]
        for k in range(10):
            c = clay.cone(3.3 * (1 - 0.088 * k) * (1 + 0.1 * rnd.uniform(-1, 1)), 3.2, (0, 0, 2.6 + 1.2 * k), pine, "Tier", verts=14)
            for pl in c.data.polygons:
                pl.use_smooth = True
            parts.append(c)
        out.append(collect(parts, f"Pine{v}"))
    for v in range(2):                                 # undergrowth: low lumps for the foot of a tree line
        parts = []
        for k in range(4):
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rnd.uniform(0.9, 1.5),
                                                  location=(rnd.uniform(-1.6, 1.6), rnd.uniform(-1.2, 1.2), rnd.uniform(0.5, 1.1)))
            b = bpy.context.active_object
            sub = b.modifiers.new("Round", "SUBSURF")
            sub.levels = sub.render_levels = 1
            d = b.modifiers.new("Lumps", "DISPLACE")
            d.texture, d.strength = tex, 0.6
            for pl in b.data.polygons:
                pl.use_smooth = True
            kit.assign(b, leaf[(v * 2 + k) % len(leaf)])
            parts.append(b)
        out.append(collect(parts, f"Shrub{v}"))
    return out


def trooper_kit(M, name="Trooper"):
    """Pennsylvania State Police uniform on a grey mannequin: grey shirt, dark trousers, black tie, campaign hat."""
    shirt = kit.matte("#8B9199", 0.75, "TrooperShirt")
    dark = kit.matte("#1E2126", 0.8, "TrooperDark")
    hat = kit.matte("#34373C", 0.8, "TrooperHat")
    garment(M, ("hand.L", "hand.R"), 1.13, 1.645, shirt, 0.022, name + ".shirt", share=0.5, exclude=True)
    garment(M, ("upper_arm.L", "upper_arm.R", "forearm.L", "forearm.R", "hand.L", "hand.R"), 0.09, 1.16, dark, 0.016,
            name + ".trousers", share=0.55, exclude=True)
    _on_body(M, clay.box(0.012, 0.05, 0.3, (0.168, 0, 1.42), dark, name + ".tie", bevel=False), "spine.003")
    brim = clay.cyl(0.2, 0.014, (-0.004, 0, 1.925), hat, name + ".brim", verts=32)
    crown = clay.cyl(0.098, 0.115, (-0.004, 0, 1.985), hat, name + ".crown", verts=24)
    for ob in (brim, crown):
        _on_body(M, ob, "spine.005")
