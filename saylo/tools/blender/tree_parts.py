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


def split_gltf(path):
    """Write one standalone .gltf + .bin per scene node (one tree each), so Blender never loads the whole scan.
    Returns [(node name, part .gltf path, face count)]."""
    import json
    src_dir = os.path.dirname(os.path.abspath(path))
    g = json.load(open(path, encoding="utf-8"))
    assert len(g["buffers"]) == 1, "expects one buffer"
    binpath = os.path.join(src_dir, g["buffers"][0]["uri"])
    out_dir = os.path.join(tempfile.gettempdir(), "tree-split-" + os.path.splitext(os.path.basename(path))[0])
    os.makedirs(out_dir, exist_ok=True)
    parts = []
    with open(binpath, "rb") as fb:
        for ni, node in enumerate(g["nodes"]):
            if "mesh" not in node:
                continue
            mesh = g["meshes"][node["mesh"]]
            acc_ids = set()
            for p in mesh["primitives"]:
                acc_ids.update(p["attributes"].values())
                if "indices" in p:
                    acc_ids.add(p["indices"])
            acc_ids = sorted(acc_ids)
            bv_ids = sorted({g["accessors"][a]["bufferView"] for a in acc_ids})
            blob, new_bv, bv_map = bytearray(), [], {}
            for b in bv_ids:
                bv = dict(g["bufferViews"][b])
                fb.seek(bv.get("byteOffset", 0))
                data = fb.read(bv["byteLength"])
                while len(blob) % 4:
                    blob += b"\0"
                bv["byteOffset"], bv["buffer"] = len(blob), 0
                blob += data
                bv_map[b] = len(new_bv)
                new_bv.append(bv)
            acc_map, new_acc = {}, []
            for a in acc_ids:
                acc = dict(g["accessors"][a])
                acc["bufferView"] = bv_map[acc["bufferView"]]
                acc_map[a] = len(new_acc)
                new_acc.append(acc)
            prims, faces = [], 0
            for p in mesh["primitives"]:
                q = dict(p)
                q["attributes"] = {k: acc_map[v] for k, v in p["attributes"].items()}
                if "indices" in p:
                    q["indices"] = acc_map[p["indices"]]
                    faces += g["accessors"][p["indices"]]["count"] // 3
                prims.append(q)
            part = dict(g)
            part["nodes"] = [dict(node, mesh=0)]
            part["meshes"] = [dict(mesh, primitives=prims)]
            part["scenes"] = [{"name": "Scene", "nodes": [0]}]
            part["scene"] = 0
            part["accessors"], part["bufferViews"] = new_acc, new_bv
            name = node.get("name", f"part{ni}")
            bname = f"{name}.bin"
            part["buffers"] = [{"byteLength": len(blob), "uri": bname}]
            # textures stay where they are: point image URIs at the original folder
            part["images"] = [dict(im, uri=os.path.join(src_dir, im["uri"]).replace("\\", "/")) if "uri" in im else im
                              for im in g.get("images", [])]
            with open(os.path.join(out_dir, bname), "wb") as fo:
                fo.write(blob)
            gp = os.path.join(out_dir, f"{name}.gltf")
            with open(gp, "w", encoding="utf-8") as fo:
                json.dump(part, fo)
            parts.append((name, gp, faces))
            del blob
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
