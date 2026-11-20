"""Name tag overlay (alpha) for a real clip: rendered with --alpha to a ProRes 4444 .mov, laid over the footage in the
assembly. --arg name=... --arg role=... --arg at=<seconds into the overlay when typing starts>"""
import os
import sys

import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "saylo", "tools", "blender"))
import retraced as rt  # noqa: E402

a = kit.args()
kit.setup(view="Standard", look=None, bloom=0, motion_blur=0, world="#000000")
cam = kit.camera((0, -10, 0), look_at=(0, 0, 0), lens=50)
rt.name_tag(cam, a.get("name"), a.get("role"), start_frame=kit.f(float(a.get("at") or 0.2)))
