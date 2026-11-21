"""Hero shot (The Wrong Man, VO 370.81-380.33): could Jewell have been the 911 caller?

The real Centennial Olympic Park map lies flat on a dark table. On "point out the bag" (0.0 s) an amber pin drops on
the blast site the map itself marks. On "a payphone several blocks away" (1.8 s) an amber ring spreads past the edge
of the park: the record only says "several blocks away", so the ring shows the distance without inventing a spot or a
direction. On "in about sixty seconds" (5.3 s) the ~60 SECONDS timer lands.

  python <docpro>/scripts/render_blender.py build/blender/H_park_bench_to_payphone.py --out render/blender/H_park.mp4 \
      --frames 286 --stills 1,60,160,240 --arg map=media/Centennial Park Bomb Map.jpg
"""
import math
import bpy
import blender_kit as kit

a = kit.args()
MAP = a.get("map")
end = a.frames
AMBER = "#E0A040"
PIN, RING, SIXTY = kit.f(0.15), kit.f(1.85), kit.f(5.3)

kit.setup(world="#08090B", view="Standard", bloom=0.2)
kit.floor("#0B0C0E", z=-0.02)

# The map, flat on the table (+Y = top of the map). 10 m wide, 881x1200 px.
W = 10.0
H = W * 1200 / 881
mp = kit.image_plane(MAP, width=W, loc=(0, 0, 0), rot=(0, 0, 0), lit=True, name="ParkMap")

def map_xy(px, py):
    """Map pixel (881x1200 image) -> world XY on the flat map."""
    return ((px / 881 - 0.5) * W, (0.5 - py / 1200) * H)

bx, by = map_xy(656, 428)          # the map's own "Blast Site" marker: the bench by the NBC tower

# Pin: amber disc on the map + a thin glowing post, dropping in on the word.
disc = bpy.ops.mesh.primitive_circle_add(vertices=48, radius=0.32, fill_type="NGON", location=(bx, by, 0.01))
disc = bpy.context.active_object
kit.assign(disc, kit.emission(AMBER, 1.6, "PinDisc"))
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.035, depth=1.6, location=(bx, by, 0.8))
post = bpy.context.active_object
kit.assign(post, kit.emission(AMBER, 1.8, "PinPost"))
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(bx, by, 1.62))
head = bpy.context.active_object
kit.assign(head, kit.emission(AMBER, 2.2, "PinHead"))
for ob in (post, head):
    kit.key(ob, "location", [(PIN - 6, (bx, by, ob.location.z + 3.0)), (PIN + 4, (bx, by, ob.location.z))], ease="expo")
    kit.fade(ob, [(PIN - 6, 0.0), (PIN, 1.0)])
kit.key(disc, "scale", [(PIN, (0.01,) * 3), (PIN + 8, (1.0,) * 3)], ease="back")
lab = kit.text("THE BENCH  \u00b7  12:57 AM", font="Montserrat-Bold", size=0.42, spacing=1.12, color="#F4F1EA", strength=1.3,
               align="LEFT", loc=(bx + 0.45, by + 0.1, 0.9), rot=(62, 0, 0), name="PinLabel")
kit.fade(lab, [(PIN + 4, 0.0), (PIN + 12, 1.0)])

# Ring: "several blocks away", spreading past the park edge (no direction claimed).
bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.025, major_segments=128, minor_segments=8,
                                 location=(bx, by, 0.03))
ring = bpy.context.active_object
kit.assign(ring, kit.emission(AMBER, 2.0, "Ring"))
R = 7.5
kit.key(ring, "scale", [(RING, (0.3, 0.3, 1.0)), (RING + kit.f(1.6), (R, R, 1.0)), (end, (R * 1.04, R * 1.04, 1.0))], ease="out")
kit.fade(ring, [(RING - 1, 0.0), (RING + 2, 1.0)])
# a soft amber wash inside the ring
wash = bpy.ops.mesh.primitive_circle_add(vertices=96, radius=1.0, fill_type="NGON", location=(bx, by, 0.015))
wash = bpy.context.active_object
kit.assign(wash, kit.emission(AMBER, 0.35, "Wash"))
kit.key(wash, "scale", [(RING, (0.3, 0.3, 1.0)), (RING + kit.f(1.6), (R, R, 1.0)), (end, (R * 1.04, R * 1.04, 1.0))], ease="out")
kit.fade(wash, [(RING - 1, 0.0), (RING + 6, 0.18)])
rlg = kit.empty((bx + 3.0, by - 5.2, 1.4), "RingLabelGroup")
rl = kit.text("PAYPHONE  \u00b7  SEVERAL BLOCKS AWAY", font="Montserrat-Bold", size=0.5, spacing=1.12, color=AMBER,
              strength=1.3, loc=(0, -0.02, 0), rot=(62, 0, 0), name="RingLabel")
rlp = kit.rect(7.6, 0.95, material=kit.matte("#0E0F12", 0.6, "RingPlate"), loc=(0, 0.03, 0), rot=(62, 0, 0), name="RingPlate")
for part in (rl, rlp):
    kit.parent(part, rlg)
    kit.fade(part, [(RING + kit.f(0.9), 0.0), (RING + kit.f(1.4), 1.0)])

# ~60 SECONDS: lands on "in about sixty seconds", floating above the map toward the camera.
# Light: warm key from the top left, cool rim; the map takes it (lit=True) so it reads like paper on a table.
kit.light("AREA", (-7, -8, 11), (0, 0, 0), power=1500, color="#FFE1BC", size=7, name="Key")
kit.light("AREA", (6, 9, 6), (0, 0, 0), power=250, color="#9FB8FF", size=6, name="Rim")
kit.motes(60, center=(bx, by - 3, 2.5), spread=(14, 10, 4), size=0.012)

# Camera: starts close and low on the blast site, pulls up and back as the ring spreads, settles for the timer.
cam = kit.camera((bx - 1.0, by - 7.0, 6.0), look_at=(bx, by, 0), lens=40)
kit.key(cam, "location", [(1, (bx - 1.0, by - 7.0, 6.0)), (RING, (bx - 1.2, by - 8.5, 7.5)),
                          (RING + kit.f(2.0), (bx - 2.0, by - 15.5, 15.0)), (end, (bx - 2.2, by - 16.5, 15.6))], ease="in_out")
kit.key(kit.aim(cam), "location", [(1, (bx, by, 0)), (RING + kit.f(2.0), (bx - 0.6, by - 1.2, 0)), (end, (bx - 0.7, by - 1.4, 0))], ease="in_out")
kit.shake(cam, strength=0.012, speed=45)

# ~60 SECONDS: a plate fixed to the camera (lower left of the frame), landing on "in about sixty seconds".
sixty = kit.empty((-1.38, -0.68, -5.0), "Sixty")
kit.parent(sixty, cam)
plate = kit.rect(1.55, 0.72, material=kit.emission("#0E0F12", 1.0, "SixtyPlate"), loc=(0.62, 0, -0.01), rot=(0, 0, 0), name="SixtyPlate")
bar = kit.rect(0.035, 0.72, AMBER, loc=(-0.15, 0, 0), rot=(0, 0, 0), name="SixtyBar")
num = kit.text("~60", font="Anton-Regular", size=0.62, color="#F4F1EA", strength=1.3, align="LEFT", loc=(-0.02, 0.08, 0.01),
               rot=(0, 0, 0), name="SixtyNum")
sec = kit.text("SECONDS", font="Montserrat-Bold", size=0.16, spacing=1.15, color=AMBER, strength=1.3, align="LEFT",
               loc=(0.0, -0.24, 0.01), rot=(0, 0, 0), name="SixtySec")
for part in (plate, bar, num, sec):
    kit.parent(part, sixty)
    kit.fade(part, [(SIXTY - 3, 0.0), (SIXTY + 2, 1.0)])
kit.key(sixty, "scale", [(SIXTY - 3, (1.15,) * 3), (SIXTY + 7, (1.0,) * 3)], ease="back")
dof = kit.depth_of_field(cam, focus=9.0, fstop=4.0)
kit.key(dof, "focus_distance", [(1, 9.0), (RING + kit.f(2.0), 20.0), (end, 21.0)], ease="in_out")

kit.post(bloom=0.3, vignette=0.45, grain=0.035)
