"""One-off: hero versions of the Poly Haven fir and pine scans that KEEP their needles (about 1.6M faces per group of
three trees), for the few shots where trees are close to the camera. The light versions in trees.blend lose the
needles and read as bare trunks.
Run:  blender -b --factory-startup --python saylo/tools/blender/prep_trees_mid.py
Writes _kit/assets/trees_mid.blend with collections FirMid and PineMid."""
import os
import bpy

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PH = os.path.join(REPO, "_kit", "assets", "polyhaven")
bpy.ops.wm.read_factory_settings(use_empty=True)
for aid, name, target in (("fir_tree_01", "FirMid", 1600000), ("pine_tree_01", "PineMid", 1800000)):
    d = os.path.join(PH, aid)
    path = next(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".gltf"))
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    tris = sum(len(o.data.polygons) for o in meshes)
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    for o in meshes:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        col.objects.link(o)
        m = o.modifiers.new("Dec", "DECIMATE")
        m.decimate_type = "UNSUBDIV" if False else "COLLAPSE"
        m.ratio = min(1.0, target / max(1, tris))
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier="Dec")
    print("TREE", name, "faces", sum(len(o.data.polygons) for o in col.objects), "from", tris, flush=True)
bpy.ops.file.pack_all()
out = os.path.join(REPO, "_kit", "assets", "trees_mid.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("TREE saved", out, flush=True)
