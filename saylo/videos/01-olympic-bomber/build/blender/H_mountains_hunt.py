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
elif mode == "arrest":
    # "where was this? Murphy. Near where they'd found his abandoned truck back in 1998. Five years, and he hadn't gone far."
    T_AR, T_TR, T_FAR = kit.f(a.get("arrest", 1.34, float)), kit.f(a.get("truck", 2.26, float)), kit.f(a.get("far", 6.76, float))
    ax2, ay2 = mx + 0.3, my + 0.2          # the arrest, in town
    tx2, ty2 = mx + 1.5, my + 1.3          # the truck, a few miles out (schematic)
    za = clay.pin(m, gz, ax2, ay2, "ARREST · 2003", T_AR, side=-1, size=0.5)
    zt = clay.pin(m, gz, tx2, ty2, "TRUCK · 1998", T_TR, side=1, size=0.5)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.03, major_segments=96, minor_segments=8,
                                     location=((ax2 + tx2) / 2, (ay2 + ty2) / 2, max(za, zt) + 0.3))
    ring = bpy.context.active_object
    kit.assign(ring, kit.emission(clay.AMBER, 2.0, "Ring"))
    kit.key(ring, "scale", [(T_FAR, (0.2, 0.2, 1)), (T_FAR + 12, (1.35, 1.35, 1))], ease="out")
    kit.fade(ring, [(T_FAR - 1, 0.0), (T_FAR + 3, 1.0)])
    ring.visible_shadow = False
    far = kit.text("HE HADN'T GONE FAR", font="Montserrat-Bold", size=0.42, spacing=1.15, color=clay.AMBER, strength=1.4,
                   loc=((ax2 + tx2) / 2, (ay2 + ty2) / 2 - 1.7, max(za, zt) + 0.4), rot=(70, 0, 0), name="Far")
    far.visible_shadow = False
    kit.fade(far, [(T_FAR + 4, 0.0), (T_FAR + 14, 1.0)])
    cx, cy = (ax2 + tx2) / 2, (ay2 + ty2) / 2
    cam = kit.camera((cx - 3.0, cy - 15.0, 11.0), look_at=(cx, cy, 0.6), lens=45)
    kit.key(cam, "location", [(1, (cx - 3.0, cy - 15.0, 11.0)), (end, (cx - 1.0, cy - 10.5, 7.4))], ease="in_out")
elif mode == "campsite":
    # "They were searching the right mountains. But knowing the region… and finding his campsite are two very different things."
    T_CAMP = kit.f(a.get("camp", 4.3, float))
    wl = kit.light("SPOT", (0.0, 0.0, 16.0), (0.0, 0.0, 0.0), power=9000, color="#E0A040", size=3.0, name="Region")
    wl.data.spot_size, wl.data.spot_blend = math.radians(70), 0.5
    kit.key(wl.data, "energy", [(1, 0.0), (12, 9000.0), (T_CAMP, 9000.0), (T_CAMP + 30, 600.0)], ease="in_out")
    sa = kit.text("THE RIGHT MOUNTAINS", font="Montserrat-Bold", size=0.9, spacing=1.2, color=clay.AMBER, strength=1.4,
                  loc=(0, -3.0, 6.0), rot=(70, 0, 0), name="SearchArea")
    sa.visible_shadow = False
    kit.fade(sa, [(8, 0.0), (18, 1.0), (T_CAMP, 1.0), (T_CAMP + 12, 0.0)])
    cpx, cpy = mx + 1.6, my + 1.8
    cz = gz(cpx, cpy)
    dot = clay.sphere(0.06, (cpx, cpy, cz + 0.08), kit.emission(clay.AMBER, 4.0, "CampDot"), "CampDot")
    kit.fade(dot, [(T_CAMP + 6, 0.0), (T_CAMP + 12, 1.0)])
    hc = kit.text("HIS CAMP", font="Montserrat-Bold", size=0.12, spacing=1.15, color="#F4F1EA", strength=1.4,
                  loc=(cpx + 0.12, cpy, cz + 0.28), rot=(70, 0, 0), align="LEFT", name="HisCamp")
    hc.visible_shadow = False
    kit.fade(hc, [(T_CAMP + 14, 0.0), (T_CAMP + 24, 1.0)])
    cam = kit.camera((-2.0, -26.0, 17.0), look_at=(0, 0.5, 0), lens=40)
    kit.key(cam, "location", [(1, (-2.0, -26.0, 17.0)), (T_CAMP, (-1.0, -24.0, 15.5)), (end, (cpx - 0.6, cpy - 3.2, cz + 2.0))], ease="in_out")
    kit.key(kit.aim(cam), "location", [(1, (0, 0.5, 0)), (T_CAMP, (0, 0.5, 0)), (end, (cpx, cpy, cz + 0.1))], ease="in_out")
elif mode == "camps":
    # "he moved between hidden camps on the slopes": small amber tent markers drop onto the slopes around Murphy
    T_C = kit.f(a.get("camps", 2.5, float))
    zm = clay.pin(m, gz, mx, my, "MURPHY", 1, side=-1)
    import random
    random.seed(4)
    spots = [(mx + 1.6, my + 1.8), (mx - 1.4, my + 2.4), (mx + 2.8, my + 0.2), (mx + 0.6, my + 3.4), (mx - 2.6, my + 0.9), (mx + 3.4, my + 2.6)]
    for k, (x, y) in enumerate(spots):
        z = gz(x, y)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.32, depth=0.4, location=(x, y, z + 0.2), rotation=(0, 0, math.radians(45)))
        tent = bpy.context.active_object
        kit.assign(tent, kit.emission(clay.AMBER, 1.6, f"Camp{k}"))
        t0 = T_C + k * 4
        kit.key(tent, "location", [(t0 - 6, (x, y, z + 2.2)), (t0 + 3, (x, y, z + 0.2))], ease="expo")
        kit.fade(tent, [(t0 - 6, 0.0), (t0, 1.0)])
    lab = kit.text("HIDDEN CAMPS", font="Montserrat-Bold", size=0.6, spacing=1.15, color=clay.AMBER, strength=1.4,
                   loc=(mx + 1.2, my + 1.0, zm + 2.3), rot=(70, 0, 0), name="Camps")
    lab.visible_shadow = False
    kit.fade(lab, [(T_C + 6, 0.0), (T_C + 16, 1.0)])
    cam = kit.camera((mx - 2.0, my - 13.0, 9.0), look_at=(mx + 0.6, my + 1.4, 0.8), lens=45)
    kit.key(cam, "location", [(1, (mx - 2.0, my - 13.0, 9.0)), (end, (mx - 1.0, my - 11.0, 7.6))], ease="in_out")
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
