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


def split_gltf(path, max_faces=1200000):
    """Cut a scan into small standalone .gltf files Blender can import one at a time: one per primitive of every tree,
    and primitives bigger than max_faces (the needle cards: 4-7M faces) sliced into index ranges. Each part keeps the
    original accessors and reads the ORIGINAL .bin (absolute path), only its index accessor is narrowed, so nothing
    is copied. Returns [(part name, part .gltf path, face count)]."""
    import copy
    import json
    src_dir = os.path.dirname(os.path.abspath(path))
    g = json.load(open(path, encoding="utf-8"))
    out_dir = os.path.join(tempfile.gettempdir(), "tree-split-" + os.path.splitext(os.path.basename(path))[0])
    os.makedirs(out_dir, exist_ok=True)
    base = copy.deepcopy(g)
    base["buffers"] = [dict(b, uri=os.path.join(src_dir, b["uri"]).replace("\\", "/")) for b in g["buffers"]]
    base["images"] = [dict(im, uri=os.path.join(src_dir, im["uri"]).replace("\\", "/")) if "uri" in im else im
                      for im in g.get("images", [])]
    size = {5121: 1, 5123: 2, 5125: 4}
    parts = []
    for node in g["nodes"]:
        if "mesh" not in node:
            continue
        mesh = g["meshes"][node["mesh"]]
        for pi, prim in enumerate(mesh["primitives"]):
            acc = g["accessors"][prim["indices"]]
            faces = acc["count"] // 3
            step = max_faces
            for k, f0 in enumerate(range(0, faces, step)):
                f1 = min(faces, f0 + step)
                part = copy.deepcopy(base)
                ia = dict(acc)
                ia["byteOffset"] = acc.get("byteOffset", 0) + f0 * 3 * size[acc["componentType"]]
                ia["count"] = (f1 - f0) * 3
                ia.pop("min", None)
                ia.pop("max", None)
                part["accessors"].append(ia)
                q = dict(prim, indices=len(part["accessors"]) - 1)
                name = f"{node.get('name', 'tree')}_p{pi}_{k}"
                part["meshes"] = [dict(mesh, name=name, primitives=[q])]
                part["nodes"] = [dict(node, name=name, mesh=0)]
                part["scenes"] = [{"name": "Scene", "nodes": [0]}]
                part["scene"] = 0
                gp = os.path.join(out_dir, name + ".gltf")
                with open(gp, "w", encoding="utf-8") as fo:
                    json.dump(part, fo)
                parts.append((name, gp, f1 - f0))
    return parts


def reduce_scan(aid_dir, target_total):
    """Returns [temp .blend path, ...], one per mesh in the scan, decimated so all parts together have ~target_total faces."""
    path = next(os.path.join(aid_dir, f) for f in os.listdir(aid_dir) if f.endswith(".gltf"))
    split = split_gltf(path)
    total = sum(f for _, _, f in split)
    print("TREE", os.path.basename(aid_dir), "parts", len(split), "faces", total, flush=True)
    ratio = min(1.0, target_total / max(1, total))
    out = []
    for i, (keep, part_path, _) in enumerate(split):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        meshes = _import(part_path)
        o = meshes[0]
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
