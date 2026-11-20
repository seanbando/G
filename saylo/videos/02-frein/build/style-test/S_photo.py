"""Frein cold open, shot 22: "Eric Frein." The FBI wanted photo (public domain) on a dark wall, slow push, name typed on.
The photo is small (393x444), so it sits framed as a print, not full screen. Source tag (FBI) is added in the assembly."""
import json
import os
import sys

import bpy
import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "saylo", "tools", "blender"))
import retraced as rt  # noqa: E402

a = kit.args()
N = a.frames
PHOTO = os.path.join(HERE, "..", "..", "media", "src", "Eric_Frein ( wikimedia commons).jpg")

rt.setup(bloom=0.25)
kit.backdrop(color="#0A0F1B", distance=0.4, size=40, lit=True)
ph = kit.image_plane(PHOTO, width=1.9, loc=(1.6, 0, 0.1), rot=(90, 0, -3), border=0.07)
kit.light("AREA", (-3, -5, 3), (0.9, 0, 0), power=260, color="#C9D6F2", size=4, name="Key")
kit.light("AREA", (5.2, -1.2, 1.5), (1.6, 0.2, 0), power=220, color=rt.AMBER, size=2, name="AmberRim")
cam = kit.camera((0, -8.2, 0.1), look_at=(0.25, 0, 0.1), lens=50)
kit.key(cam, "location", [(1, (0, -8.2, 0.1)), (N, (0.1, -7.5, 0.1))], ease="linear")
# the name, big, left of the photo (a normal name tag is too small for the reveal); camera-fixed, typed on
h, hw, hh = rt.hud(cam, 4.0)
size = hh * 0.42
x, y = -hw * 0.9, hh * 0.02
bar = kit.rect(size * 0.07, size * 1.75, rt.AMBER, loc=(x - size * 0.3, y - size * 0.25, 0), rot=(0, 0, 0), anchor="left", name="NameBar")
nm = kit.text("ERIC FREIN", font="Anton-Regular", size=size, spacing=1.05, color=rt.OFF_WHITE, strength=1.6, align="LEFT",
              loc=(x, y + size * 0.12, 0), rot=(0, 0, 0), name="Name")
sub = kit.text("AGE 31  ·  CANADENSIS, PA", font="Montserrat-Bold", size=size * 0.3, spacing=1.25, color=rt.AMBER,
               strength=1.6, align="LEFT", loc=(x, y - size * 0.62, 0), rot=(0, 0, 0), name="NameSub")
for ob in (bar, nm, sub):
    kit.parent(ob, h)
rt.typed(nm, kit.f(0.05), cps=30)
rt.typed(sub, kit.f(0.45), cps=40, cursor=False)
rt.finish(vignette=0.6)
