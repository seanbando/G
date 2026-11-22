"""Build the grey mannequin the Retraced sets load (rt.real_mannequin) from Blender's official CC0 "Human Base Meshes"
bundle, and save it as _kit/assets/mannequin/male_base_mesh.glb (replaces the thin skin-modifier body of make_mannequin.py).

Get the bundle once (CC0, blender.org):
  https://download.blender.org/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.4.1.zip
  unzip into _kit/assets/mannequin/hbm-download/
Run:  blender -b --factory-startup --python saylo/tools/blender/make_mannequin_hbm.py

Same contract as make_mannequin.py: Rigify human metarig bone names, one body mesh on the armature (automatic weights),
faces +Y with soles at z = -1 in file space, top of the head about 1.95 above the soles. Eyes are dropped and the face is
smoothed away (the channel's mannequin is faceless)."""
import glob
import math
import os

import addon_utils
import bmesh
import bpy

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
MAN = os.path.join(REPO, "_kit", "assets", "mannequin")
OUT = os.path.join(MAN, "male_base_mesh.glb")
BUNDLE = sorted(glob.glob(os.path.join(MAN, "hbm-download", "*", "human_base_meshes_bundle.blend")))[-1]
BODY = "GEO-body_male_realistic"

bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("rigify", default_set=True)

# ------------------------------------------------------------------ body from the bundle
with bpy.data.libraries.load(BUNDLE, link=False) as (src, dst):
    dst.objects = [BODY]
body = dst.objects[0]
bpy.context.scene.collection.objects.link(body)
body.parent = None
body.name = body.data.name = "MannequinBody"
bpy.context.view_layer.objects.active = body
body.select_set(True)
for m in list(body.modifiers):                      # bake subdivision / mirror etc. into the mesh
    if m.type in ("MULTIRES",):
        body.modifiers.remove(m)
        continue
    try:
        bpy.ops.object.modifier_apply(modifier=m.name)
    except RuntimeError:
        body.modifiers.remove(m)
body.data.shape_keys and bpy.ops.object.shape_key_remove(all=True, apply_mix=True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# soles at 0, centred, top of head at 1.95
zs = [v.co.z for v in body.data.vertices]
xs = [v.co.x for v in body.data.vertices]
ys = [v.co.y for v in body.data.vertices]
k = 1.95 / (max(zs) - min(zs))
cx, cy, z0 = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, min(zs)
for v in body.data.vertices:
    v.co.x, v.co.y, v.co.z = (v.co.x - cx) * k, (v.co.y - cy) * k, (v.co.z - z0) * k
H = 1.95

# faceless: smooth the front of the head hard (nose, lips, eye sockets), keep the skull shape
bm = bmesh.new()
bm.from_mesh(body.data)
face = [v for v in bm.verts if v.co.z > H * 0.875]          # the whole head above the jaw line
for _ in range(80):
    bmesh.ops.smooth_vert(bm, verts=face, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
# smoothing shrinks the head: grow it back (from the jaw line up) so the top is at H again and the cap still fits
z_jaw = H * 0.875
cxh = sum(v.co.x for v in face) / len(face)
cyh = sum(v.co.y for v in face) / len(face)
g = (H - z_jaw) / (max(v.co.z for v in face) - z_jaw)
for v in face:
    w = min(1.0, (v.co.z - z_jaw) / (H * 0.03))               # blend in over the first 6 cm so the neck stays joined
    f = 1 + (g - 1) * w
    v.co.x, v.co.y, v.co.z = cxh + (v.co.x - cxh) * f, cyh + (v.co.y - cyh) * f, z_jaw + (v.co.z - z_jaw) * f
bm.to_mesh(body.data)
bm.free()
for p in body.data.polygons:
    p.use_smooth = True
body.data.materials.clear()
mat = bpy.data.materials.new("MannequinGrey")
mat.diffuse_color = (0.62, 0.62, 0.62, 1)
body.data.materials.append(mat)

# ------------------------------------------------------------------ rig: Rigify human metarig, fitted to the body height
bpy.ops.object.armature_human_metarig_add()
arm = bpy.context.object
arm.name = arm.data.name = "Mannequin"
KEEP = ["spine", "spine.001", "spine.002", "spine.003", "spine.004", "spine.005", "spine.006"]
for s in ("L", "R"):
    KEEP += [f"{b}.{s}" for b in ("pelvis", "thigh", "shin", "foot", "toe", "heel.02", "shoulder", "upper_arm",
                                  "forearm", "hand")]
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones
for b in list(eb):
    if b.name not in KEEP:
        eb.remove(b)
top = max(max(b.head.z, b.tail.z) for b in eb)
s_ = H / top
for b in eb:
    b.head *= s_
    b.tail *= s_
# the metarig's arms stick out sideways, the body's arms hang down (A-pose): lay each arm chain along the body's arm,
# shoulder joint -> fingertip, or the arm gets weighted to the hip and does not move
from mathutils import Vector  # noqa: E402
vs = [v.co for v in body.data.vertices]
for side, sgn in (("L", 1), ("R", -1)):
    tip = max(vs, key=lambda v: sgn * v.x).copy()
    root = eb[f"upper_arm.{side}"].head.copy()
    d = tip - root
    elbow = root + d * 0.43 + Vector((0, 0.035, 0))          # slight bend backwards so the elbow folds the right way
    wrist = root + d * 0.78
    eb[f"upper_arm.{side}"].tail = elbow
    eb[f"forearm.{side}"].head, eb[f"forearm.{side}"].tail = elbow, wrist
    eb[f"hand.{side}"].head, eb[f"hand.{side}"].tail = wrist, tip
    # same twist as the thigh on that side, so a +X turn swings the arm the way the walk/run poses expect
    zt = -eb[f"thigh.{side}"].z_axis                  # half a turn from the thigh: retraced's arm angles expect this
    for n in ("upper_arm", "forearm", "hand"):
        eb[f"{n}.{side}"].align_roll(zt)
    print("MANNEQUIN arm", side, [round(c, 3) for c in root], [round(c, 3) for c in elbow], [round(c, 3) for c in tip])
bpy.ops.object.mode_set(mode="OBJECT")
print("MANNEQUIN rig scale", round(s_, 3))

bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type="ARMATURE_AUTO")

# retraced.py's poses were written for a base mesh whose arms rest held OUT (they bring the upper arm DOWN about 24 deg
# with a Z turn). This body's arms hang down, so raise them 24 deg and make that the rest pose.
bpy.ops.object.mode_set(mode="POSE")
for side in ("L", "R"):
    pb = arm.pose.bones[f"upper_arm.{side}"]
    pb.rotation_mode = "XYZ"
    hand = arm.pose.bones[f"hand.{side}"]
    x0 = abs((arm.matrix_world @ hand.tail).x)
    pb.rotation_euler = (0, 0, math.radians(24))
    bpy.context.view_layer.update()
    if abs((arm.matrix_world @ hand.tail).x) < x0:            # this side turns the other way: raise with -24 instead
        pb.rotation_euler = (0, 0, math.radians(-24))
        bpy.context.view_layer.update()
    print("MANNEQUIN raise", side, round(math.degrees(pb.rotation_euler.z)), round(x0, 3),
          round(abs((arm.matrix_world @ hand.tail).x), 3))
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.objects.active = body
mod = next(m for m in body.modifiers if m.type == "ARMATURE")
bpy.ops.object.modifier_apply(modifier=mod.name)              # bake the raised arms into the mesh
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
bpy.ops.pose.armature_apply(selected=False)                   # and make that pose the rest pose
bpy.ops.object.mode_set(mode="OBJECT")
mod = body.modifiers.new("Armature", "ARMATURE")
mod.object = arm

# ------------------------------------------------------------------ file-space contract: face +Y, soles at z = -1
arm.rotation_euler = (0, 0, math.radians(180))
arm.location = (0, 0, -1.0)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
bpy.context.view_layer.update()
bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)

zs = [(body.matrix_world @ v.co).z for v in body.data.vertices]
ys = [(body.matrix_world @ v.co).y for v in body.data.vertices]
print("MANNEQUIN verts", len(body.data.vertices), "z", round(min(zs), 3), round(max(zs), 3),
      "y", round(min(ys), 3), round(max(ys), 3), "groups", len(body.vertex_groups))

bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
arm.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_selection=True, export_animations=False,
                          export_skins=True, export_apply=False)
with open(os.path.join(MAN, "SOURCE.txt"), "w", encoding="utf-8") as fh:
    fh.write("Body: GEO-body_male_realistic from Blender's Human Base Meshes bundle v1.4.1 (CC0, blender.org), face "
             "smoothed, on a Rigify metarig. Built by saylo/tools/blender/make_mannequin_hbm.py.\n")
print("MANNEQUIN saved", OUT)
