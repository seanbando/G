"""The Hunt, on the same clay mountains as Who He Was.
  --arg mode=andrews : "The task force sets up in Andrews, a small town about 15 miles from Murphy."
                       MURPHY is already pinned; ANDREWS drops at `andrews` s; an amber line draws Andrews -> Murphy and
                       "~15 MILES" lands at `miles` s.
  --arg mode=grid    : "Teams walking ridgelines for weeks. ... Almost nothing."
                       amber search squares light up across the ridges west to east, then go dark at `nothing` s,
                       leaving only faint outlines.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import blender_kit as kit
import clay

a = kit.args()
end = a.frames
mode = a.get("mode", "andrews")
kit.setup(world="#050506", view="Standard", bloom=0.3)
kit.backdrop("#050506", center="#161B26", distance=60)
m = clay.mats()
gz = clay.mountains(m)
clay.night_light(moon=1.4, key=2600)
mx, my = clay.TOWNS["MURPHY"]
ax, ay = clay.TOWNS["ANDREWS"]

if mode == "andrews":
    T_AND, T_MILES = kit.f(a.get("andrews", 1.3, float)), kit.f(a.get("miles", 3.4, float))
    zm = clay.pin(m, gz, mx, my, "MURPHY", 1, side=-1)
    za = clay.pin(m, gz, ax, ay, "ANDREWS", T_AND, side=1)
    mid = ((ax + mx) / 2, (ay + my) / 2 - 0.4, max(za, zm) + 1.2)   # label between the two pins (no line)
    lab = kit.text("~15 MILES", font="Montserrat-Bold", size=0.75, spacing=1.15, color=clay.AMBER, strength=1.4,
                   loc=mid, rot=(70, 0, 0), name="Miles")
    lab.visible_shadow = False
    kit.fade(lab, [(T_MILES, 0.0), (T_MILES + 8, 1.0)])
    cam = kit.camera((-6.0, -20.0, 12.0), look_at=(-3.5, -1.0, 0.5), lens=42)
    kit.key(cam, "location", [(1, (-6.0, -20.0, 12.0)), (end, (-4.0, -17.5, 10.5))], ease="in_out")
else:
    T_OFF = kit.f(a.get("nothing", 2.74, float))
    cells = []
    for i in range(10):
        for j in range(6):
            x, y = -10.8 + i * 2.4, -6.0 + j * 2.4
            z = gz(x, y) + 0.25
            bpy.ops.mesh.primitive_plane_add(size=2.25, location=(x, y, z))
            sq = bpy.context.active_object
            kit.assign(sq, kit.emission(clay.AMBER, 0.6, f"Cell{i}_{j}"))
            t_on = 1 + i * 5 + j
            kit.fade(sq, [(t_on, 0.0), (t_on + 6, 0.35), (T_OFF, 0.35), (T_OFF + 14, 0.05)])
            sq.visible_shadow = False
    lab = kit.text("ALMOST NOTHING", font="Montserrat-Bold", size=0.9, spacing=1.2, color="#F4F1EA", strength=1.4,
                   loc=(0, -2.0, 6.0), rot=(70, 0, 0), name="Nothing")
    lab.visible_shadow = False
    kit.fade(lab, [(T_OFF + 4, 0.0), (T_OFF + 14, 1.0)])
    cam = kit.camera((-2.0, -26.0, 17.0), look_at=(0, 0.5, 0), lens=40)
    kit.key(cam, "location", [(1, (-2.0, -26.0, 17.0)), (end, (0.5, -24.0, 15.5))], ease="in_out")

kit.shake(cam, strength=0.008, speed=40)
kit.depth_of_field(cam, focus=24.0, fstop=1.4)
kit.post(bloom=0.35, vignette=0.65, grain=0.04)
