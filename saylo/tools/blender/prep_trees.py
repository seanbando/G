"""One-off: turn the huge Poly Haven tree scans (10M triangles) into light versions the Retraced sets can instance.
Run:  blender -b --factory-startup --python saylo/tools/blender/prep_trees.py
Writes _kit/assets/trees.blend with collections <Name>Hi (hero, near the camera) and <Name>Lo (forest)."""
import os
import bpy

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PH = os.path.join(REPO, "_kit", "assets", "polyhaven")
bpy.ops.wm.read_factory_settings(use_empty=True)
for aid, name in (("fir_tree_01", "Fir"), ("pine_tree_01", "Pine")):
    d = os.path.join(PH, aid)
    path = next(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".gltf"))
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    tris = sum(len(o.data.polygons) for o in meshes)
    print("TREE", aid, "objects", len(meshes), "faces", tris, "dims", [tuple(round(v, 1) for v in o.dimensions) for o in meshes][:6])
    # Memory-light (the pine scan is 17M faces; a full copy of it ran a 15 GB machine out of memory):
    # shrink the scan in place to the Hi level first, then copy that small Hi mesh and shrink it again for Lo.
    src = meshes
    for level, target in (("Hi", 260000), ("Lo", 28000)):
        col = bpy.data.collections.new(name + level)
        bpy.context.scene.collection.children.link(col)
        have = sum(len(o.data.polygons) for o in src)
        out_objs = []
        for o in src:
            if level == "Hi":
                c = o
                for uc in list(c.users_collection):
                    uc.objects.unlink(c)
            else:
                c = o.copy()
                c.data = o.data.copy()
            col.objects.link(c)
            m = c.modifiers.new("Dec", "DECIMATE")
            m.ratio = min(1.0, target / max(1, have))
            bpy.context.view_layer.objects.active = c
            bpy.ops.object.modifier_apply(modifier="Dec")
            out_objs.append(c)
        src = out_objs
        print("TREE", name + level, "faces", sum(len(o.data.polygons) for o in col.objects), flush=True)
    bpy.ops.outliner.orphans_purge(do_recursive=True)
bpy.ops.file.pack_all()
out = os.path.join(REPO, "_kit", "assets", "trees.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("TREE saved", out)
