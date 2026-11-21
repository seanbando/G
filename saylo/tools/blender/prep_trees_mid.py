"""One-off: hero versions of the Poly Haven fir and pine scans that KEEP their needles (about 1.6M faces per group of
three trees), for the few shots where trees are close to the camera. The light versions in trees.blend lose the
needles and read as bare trunks.
Run:  blender -b --factory-startup --python saylo/tools/blender/prep_trees_mid.py
Writes _kit/assets/trees_mid.blend with collections FirMid and PineMid.
Memory-light (Nov 21, 2026): each scan is shrunk one object at a time (tree_parts.py), so it fits in 15 GB of RAM."""
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tree_parts  # noqa: E402

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PH = os.path.join(REPO, "_kit", "assets", "polyhaven")

parts = {name: tree_parts.reduce_scan(os.path.join(PH, aid), target)
         for aid, name, target in (("fir_tree_01", "FirMid", 1600000), ("pine_tree_01", "PineMid", 1800000))}
bpy.ops.wm.read_factory_settings(use_empty=True)
for name, files in parts.items():
    col, objs = tree_parts.load_parts(files, name)
    print("TREE", name, "faces", sum(len(o.data.polygons) for o in objs), flush=True)
tree_parts.dedupe_materials()
bpy.ops.file.pack_all()
out = os.path.join(REPO, "_kit", "assets", "trees_mid.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("TREE saved", out, flush=True)
