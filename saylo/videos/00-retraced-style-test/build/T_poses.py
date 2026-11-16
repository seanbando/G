"""Pose check for the real mannequin: stand, crouch (amber), sit, flashlight, hands up, mid-run. Stills only."""
import os
import sys

import bpy
import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "tools", "blender")))
import retraced as rt  # noqa: E402

rt.setup()
m = rt.mats()
kit.rect(60, 60, material=m["ground"], loc=(0, 0, 0), rot=(0, 0, 0), name="Ground")
kit.light("AREA", (-4, -8, 7), (0, 0, 1), power=3000, color="#DDE4F5", size=6, name="Key")
kit.light("AREA", (5, 6, 4), (0, 0, 1), power=1500, color="#8FA8E8", size=4, name="Rim")
names = ["stand", "crouch", "sit", "flashlight", "hands_up", "run"]
for i, p in enumerate(names):
    x = (i - 2.5) * 1.6
    mat = m["subject"] if p in ("crouch", "hands_up", "run") else m["man"]
    M = rt.real_mannequin(p, (x, 0, -rt.RDROP.get(p, 0.0)), 25, mat)
    if p == "run":
        rt.rrun_cycle(M, 1, 30)
        bpy.context.scene.frame_set(1)
    else:
        rt.rpose(M, p)
cam = kit.camera((0, -11, 2.2), look_at=(0, 0, 0.9), lens=40)
rt.finish()
