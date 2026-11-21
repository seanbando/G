"""Hero (Same Hands, VO 455.29-462.55, 218 frames): "By now investigators are pretty sure it's one person. Same
construction, same habits, same kind of target."
Three real photos from the three nights land as prints on a dark table, each with its date: on "Same construction"
(3.68 s), "same habits" (4.84 s), "same kind of target" (5.84 s). A thin amber thread links them as the last lands.
  --arg photo=<park 1996> --arg photo=<sandy springs 1997> --arg photo=<otherside 1997>
"""
import bpy
import blender_kit as kit

a = kit.args()
photos = a.all("photo")
end = a.frames
AMBER = "#E0A040"
beats = [kit.f(0.5), kit.f(1.4), kit.f(2.3)]          # prints land during "By now investigators are pretty sure it's one person"
thread_at = [kit.f(3.68), kit.f(4.84)]                  # thread draws on "Same construction" -> "same habits"
dates = ["JUL 27, 1996  ·  CENTENNIAL PARK", "JAN 16, 1997  ·  SANDY SPRINGS", "FEB 21, 1997  ·  OTHERSIDE LOUNGE"]
spots = [(-4.3, 0.6, 0.2, -4), (0.0, 0.0, -0.1, 3), (4.3, 0.6, 0.15, -2)]   # x, y, z, tilt

kit.setup(world="#0A0908", look="Medium High Contrast")
kit.backdrop("#0C0B09", center="#2B261F", distance=4.5, lit=True)

pins = []
for (x, y, z, tilt), path, t0, d in zip(spots, photos, beats, dates):
    p = kit.image_plane(path, width=3.8, loc=(x, y, z), rot=(90, tilt, 0), border=0.09, strength=1.05)
    kit.key(p, "location", [(t0 - 8, (x, y - 0.8, z + 1.8)), (t0 + 6, (x, y, z))], ease="expo")
    kit.key(p, "rotation_euler", [(t0 - 8, kit.rot(90, tilt * 3, 6)), (t0 + 8, kit.rot(90, tilt, 0))], ease="out")
    kit.fade(p, [(t0 - 8, 0.0), (t0 - 3, 1.0)])
    cap = kit.text(d, font="Montserrat-Bold", size=0.3, spacing=1.12, color=AMBER, strength=1.5,
                   loc=(x, y - 0.05, z - p["height"] / 2 - 0.42), name="Date")
    kit.fade(cap, [(t0 + 2, 0.0), (t0 + 10, 1.0)])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=(x, y - 0.06, z + p["height"] / 2 - 0.12))
    pin = bpy.context.active_object
    kit.assign(pin, kit.emission("#C8402F", 2.0, "Pin"))
    kit.fade(pin, [(t0 + 4, 0.0), (t0 + 6, 1.0)])
    pins.append(pin.location.copy())

# amber thread between the pins once all three are down
for i in range(2):
    (x0, y0, z0), (x1, y1, z1) = pins[i], pins[i + 1]
    mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
    length = ((x1 - x0) ** 2 + (z1 - z0) ** 2) ** 0.5
    import math
    ang = math.degrees(math.atan2(z1 - z0, x1 - x0))
    th = kit.rect(0.001, 0.03, AMBER, loc=(mx, min(y0, y1) - 0.12, mz), rot=(90, -ang, 0), name=f"Thread{i}")
    t0 = thread_at[i]
    kit.key(th, "scale", [(t0, (1, 1, 1)), (t0 + 10, (length * 1000, 1, 1))], ease="out")

kit.light("AREA", (-6, -7, 7), (0, 1, 0), power=1500, color="#FFE1BC", size=5, name="Key")
kit.rim((0, 1, 0), "#9FB8FF", power=400, distance=8, side=1)

cam = kit.camera((-0.8, -14.6, 0.6), look_at=(0, 0.4, -0.55), lens=38)
kit.key(cam, "location", [(1, (-0.8, -14.6, 0.6)), (end, (0.4, -13.8, 0.25))], ease="in_out")
kit.shake(cam, strength=0.012, speed=45)
kit.depth_of_field(cam, focus=14.2, fstop=4.0)
kit.post(bloom=0.25, vignette=0.45, grain=0.04)
