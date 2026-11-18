"""Hero (cold open, VO 74.68-81.59, 207 frames): "So why was he so hard to catch? There isn't one answer. There are three,
and they stack on top of each other."
The question in warm metal (0.0 s). On "There are three" (3.9 s) it lifts away and three dark slabs drop and stack on
"stack on top of each other" (5.36 s, 5.6 s, 5.85 s), numbered 1 2 3: the three chapters that follow.
"""
import blender_kit as kit

a = kit.args()
end = a.frames
AMBER = "#E0A040"
THREE, S1, S2, S3 = kit.f(3.9), kit.f(4.3), kit.f(4.9), kit.f(5.5)

kit.setup(world="#06070A")
kit.backdrop("#06070A", center="#1D1912", distance=14)

gold = kit.metal("#F2CD7E", roughness=0.24, name="Gold")
q = kit.empty((0, 0, 0.0), "Question")
l1 = kit.text("WHY WAS HE SO", font="Anton-Regular", size=2.0, extrude=0.14, bevel=0.025, material=gold, loc=(0, 0, 1.05), name="Q1")
l2 = kit.text("HARD TO CATCH?", font="Anton-Regular", size=2.0, extrude=0.14, bevel=0.025, material=gold, loc=(0, 0, -1.15), name="Q2")
for part in (l1, l2):
    kit.parent(part, q)
kit.key(q, "scale", [(1, (0.94,) * 3), (kit.f(1.2), (1.0,) * 3)], ease="out")
kit.key(q, "location", [(THREE - 4, (0, 0, 0.0)), (THREE + 10, (0, 3.0, 5.0))], ease="expo_in_out")
for part in (l1, l2):
    kit.fade(part, [(THREE - 2, 1.0), (THREE + 8, 0.0)])

# three slabs, stacking bottom to top: 1 THE WRONG MAN, 2 NO NAME, 3 BUILT FOR HIDING
slab_mat = [kit.matte("#16181D", 0.45, f"Slab{i}") for i in range(3)]
labels = ["1  ·  THE WRONG MAN", "2  ·  NO NAME", "3  ·  BUILT FOR HIDING"]
for i, (t0, lab) in enumerate(zip((S1, S2, S3), labels)):
    z = -1.4 + i * 1.05
    g = kit.empty((0, 0, z + 6.0), f"Slab{i}G")
    import bpy
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    cube = bpy.context.active_object
    cube.scale = (6.2, 1.6, 0.9)
    kit.assign(cube, slab_mat[i])
    kit.parent(cube, g)
    edge = kit.rect(0.08, 0.9, AMBER, loc=(-3.1, -0.81, 0), name=f"Edge{i}")
    kit.parent(edge, g)
    tx = kit.text(lab, font="Montserrat-Bold", size=0.42, spacing=1.15, color="#EDE8DD", strength=1.5, align="LEFT",
                  loc=(-2.8, -0.82, 0), name=f"Label{i}")
    kit.parent(tx, g)
    kit.key(g, "location", [(t0 - 9, (0, 0, z + 6.0)), (t0, (0, 0, z))], ease="bounce")
    for part in (cube, edge, tx):
        kit.fade(part, [(t0 - 9, 0.0), (t0 - 5, 1.0)])

kit.three_point(target=(0, 0, 0), power=1.5, distance=9)
kit.light("AREA", (0, -10, 1.5), (0, 0, 0), power=1800, color="#FFE7C4", size=8, name="Front")
kit.motes(count=40, center=(0, -1.0, 0.4), spread=(14, 16, 7), size=0.012, strength=1.5)

cam = kit.camera((-1.2, -15.5, 1.0), look_at=(0, 0, 0.2), lens=50)
kit.key(cam, "location", [(1, (-1.2, -15.5, 1.0)), (THREE, (-0.6, -14.2, 0.6)), (end, (0.8, -15.8, 1.6))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (0, 0, 0.3)), (THREE + 10, (0, 0, -0.3)), (end, (0, 0, -0.35))], ease="in_out")
kit.shake(cam, strength=0.013, speed=40)
kit.depth_of_field(cam, focus=15.0, fstop=2.0)
kit.post(bloom=0.3, vignette=0.4, grain=0.035)
