"""Build the faceless grey mannequin the Retraced sets load (rt.real_mannequin) and save it as
_kit/assets/mannequin/male_base_mesh.glb.  Run:  blender -b --factory-startup --python saylo/tools/blender/make_mannequin.py

Rebuilt Nov 21, 2026 because the original CC0 base mesh stayed on the old PC. Same contract as the original:
- Rigify human metarig bone names (spine .. spine.006, thigh/shin/foot/toe, shoulder/upper_arm/forearm/hand, .L/.R)
- one body mesh parented to the armature (Armature modifier, automatic weights)
- in file space: faces +Y, soles at z = -1 (real_mannequin lifts the rig 1 m and turns it -90 deg, so it faces +X)
- head centre about z 1.85, top about 1.95 above the soles (tactical() fits the helmet to that)
The body is a smooth skin-modifier sculpt: no face, no fingers (the channel's mannequin look). Made from scratch: CC0."""
import math
import os

import addon_utils
import bmesh
import bpy

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(REPO, "_kit", "assets", "mannequin", "male_base_mesh.glb")

bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("rigify", default_set=True)
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
bpy.ops.object.mode_set(mode="OBJECT")

# ------------------------------------------------------------------ body: skin modifier over the bone chain
B = {b.name: b for b in arm.data.bones}
verts, radii, edges, index = [], [], [], {}


def pt(key, co, r):
    """One skin vertex; r = (half-width across X, half-depth along Y)."""
    if key not in index:
        index[key] = len(verts)
        verts.append(tuple(co))
        radii.append(r)
    return index[key]


def chain(names, rs, side=None):
    """Vertices at each bone's head (and the last tail), radii from rs (one more than names)."""
    ids = []
    for i, n in enumerate(names):
        b = B[n]
        ids.append(pt(n + ":h", b.head_local, rs[i]))
    last = B[names[-1]]
    ids.append(pt(names[-1] + ":t", last.tail_local, rs[-1]))
    for a, b in zip(ids, ids[1:]):
        edges.append((a, b))
    return ids


# torso and head: hips -> chest -> neck -> head (spine.004/.005 = neck, spine.006 = head)
torso = chain(["spine", "spine.001", "spine.002", "spine.003", "spine.004", "spine.005", "spine.006"],
              [(0.150, 0.105), (0.140, 0.095), (0.145, 0.100), (0.165, 0.105), (0.060, 0.058), (0.055, 0.055),
               (0.082, 0.095), (0.060, 0.070)])
# fill the skull: an extra vertex between spine.006 head and tail with the widest radius
h6 = B["spine.006"]
mid = tuple((a + b) / 2 for a, b in zip(h6.head_local, h6.tail_local))
skull = pt("skull", mid, (0.090, 0.105))
edges.remove((torso[-2], torso[-1]))
edges += [(torso[-2], skull), (skull, torso[-1])]

for s in ("L", "R"):
    # legs from the hip joint (thigh head) down to the toes
    hip = chain([f"thigh.{s}", f"shin.{s}", f"foot.{s}", f"toe.{s}"],
                [(0.088, 0.090), (0.058, 0.060), (0.043, 0.048), (0.038, 0.030), (0.030, 0.022)])
    edges.append((torso[0], hip[0]))
    # arms from the shoulder through the hand (mitten)
    sh = chain([f"shoulder.{s}", f"upper_arm.{s}", f"forearm.{s}", f"hand.{s}"],
               [(0.060, 0.055), (0.052, 0.052), (0.040, 0.040), (0.032, 0.026), (0.028, 0.018)])
    edges.append((torso[3], sh[0]))

me = bpy.data.meshes.new("MannequinBody")
me.from_pydata(verts, edges, [])
body = bpy.data.objects.new("MannequinBody", me)
bpy.context.scene.collection.objects.link(body)
skin = body.modifiers.new("Skin", "SKIN")
skin.use_smooth_shade = True
skin.branch_smoothing = 0.6
for i, r in enumerate(radii):
    body.data.skin_vertices[0].data[i].radius = r
body.data.skin_vertices[0].data[0].use_root = True
sub = body.modifiers.new("Sub", "SUBSURF")
sub.levels = sub.render_levels = 2
bpy.context.view_layer.objects.active = body
body.select_set(True)
bpy.ops.object.modifier_apply(modifier="Skin")
bpy.ops.object.modifier_apply(modifier="Sub")
for p in body.data.polygons:
    p.use_smooth = True
mat = bpy.data.materials.new("MannequinGrey")
mat.diffuse_color = (0.62, 0.62, 0.62, 1)
body.data.materials.append(mat)

# ------------------------------------------------------------------ skin it to the rig
bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type="ARMATURE_AUTO")

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
      "y", round(min(ys), 3), round(max(ys), 3), "bones", len(arm.data.bones))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_selection=True, export_animations=False,
                          export_skins=True, export_apply=False)
with open(os.path.join(os.path.dirname(OUT), "SOURCE.txt"), "w", encoding="utf-8") as fh:
    fh.write("Built by saylo/tools/blender/make_mannequin.py (Rigify metarig + skin-modifier body). Own work, CC0.\n")
print("MANNEQUIN saved", OUT)
