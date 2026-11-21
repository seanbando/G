"""One-off: turn the huge Poly Haven tree scans (7M-17M faces) into light versions the Retraced sets can instance.
Run:  blender -b --factory-startup --python saylo/tools/blender/prep_trees.py
Writes _kit/assets/trees.blend with collections <Name>Hi (hero, near the camera) and <Name>Lo (forest).
Memory-light (Nov 21, 2026): each scan is shrunk one object at a time (tree_parts.py), so it fits in 15 GB of RAM."""
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tree_parts  # noqa: E402

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PH = os.path.join(REPO, "_kit", "assets", "polyhaven")
HI, LO = 260000, 28000

parts = {name: tree_parts.reduce_scan(os.path.join(PH, aid), HI)
         for aid, name in (("fir_tree_01", "Fir"), ("pine_tree_01", "Pine"))}
bpy.ops.wm.read_factory_settings(use_empty=True)
for name, files in parts.items():
    hi_col, hi = tree_parts.load_parts(files, name + "Hi")
    print("TREE", name + "Hi", "faces", sum(len(o.data.polygons) for o in hi), flush=True)
    lo_col = bpy.data.collections.new(name + "Lo")
    bpy.context.scene.collection.children.link(lo_col)
    for o in hi:
        c = o.copy()
        c.data = o.data.copy()
        lo_col.objects.link(c)
        m = c.modifiers.new("Dec", "DECIMATE")
        m.ratio = LO / HI
        bpy.context.view_layer.objects.active = c
        bpy.ops.object.modifier_apply(modifier="Dec")
    print("TREE", name + "Lo", "faces", sum(len(o.data.polygons) for o in lo_col.objects), flush=True)
bpy.ops.file.pack_all()
out = os.path.join(REPO, "_kit", "assets", "trees.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("TREE saved", out, flush=True)
