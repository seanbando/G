"""Shared by prep_trees.py / prep_trees_mid.py: shrink a huge Poly Haven tree scan ONE OBJECT AT A TIME, so a 17M-face
scan (pine_tree_01) fits in 15 GB of RAM. Each part is imported, every other part deleted, decimated, and written to a
small temp .blend; load_parts() then links the results into the current file."""
import os
import tempfile

import bpy


def _import(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before and o.type == "MESH"]


def reduce_scan(aid_dir, target_total):
    """Returns [temp .blend path, ...], one per mesh in the scan, decimated so all parts together have ~target_total faces."""
    path = next(os.path.join(aid_dir, f) for f in os.listdir(aid_dir) if f.endswith(".gltf"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    meshes = _import(path)
    names = [o.name for o in meshes]
    total = sum(len(o.data.polygons) for o in meshes)
    print("TREE", os.path.basename(aid_dir), "parts", len(names), "faces", total, flush=True)
    ratio = min(1.0, target_total / max(1, total))
    out = []
    for i, keep in enumerate(names):
        if i:                                            # fresh import for every part after the first
            bpy.ops.wm.read_factory_settings(use_empty=True)
            _import(path)
        for o in list(bpy.data.objects):
            if o.type == "MESH" and o.name != keep:
                bpy.data.objects.remove(o, do_unlink=True)
        bpy.ops.outliner.orphans_purge(do_recursive=True)
        o = bpy.data.objects[keep]
        m = o.modifiers.new("Dec", "DECIMATE")
        m.ratio = ratio
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier="Dec")
        mw = o.matrix_world.copy()                        # keep world placement without the glTF root empties
        o.parent = None
        o.matrix_world = mw
        t = os.path.join(tempfile.gettempdir(), f"tree-{os.path.basename(aid_dir)}-{i}.blend")
        bpy.data.libraries.write(t, {o}, fake_user=True)
        out.append(t)
        print("TREE part", keep, "faces", len(o.data.polygons), flush=True)
    return out


def load_parts(parts, collection_name):
    """Link the decimated parts into a new collection of the current file (after read_factory_settings)."""
    col = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(col)
    objs = []
    for t in parts:
        with bpy.data.libraries.load(t, link=False) as (src, dst):
            dst.objects = list(src.objects)
        for o in dst.objects:
            if o is not None:
                col.objects.link(o)
                o.use_fake_user = False
                objs.append(o)
    return col, objs
