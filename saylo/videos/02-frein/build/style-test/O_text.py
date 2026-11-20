"""Typed text over a real clip or photo, rendered with --alpha and laid over the footage by assemble.py / stills.py.
Reads the shot from the plan (--arg cfg=..., --arg shot=N):
  "nametag": {"name": "GEORGE BIVENS", "role": "LT. COL., PENNSYLVANIA STATE POLICE", "at": 282.1}
  "stamp":   {"line": "48 DAYS", "sub": "SEPT 12 - OCT 30, 2014", "at": 52.9}     (big caps top-left)
Times are voiceover seconds; the text must finish typing before the shot ends."""
import io
import json
import os
import sys

import blender_kit as kit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "saylo", "tools", "blender"))
import retraced as rt  # noqa: E402

a = kit.args()
CFG = json.load(io.open(os.path.join(HERE, a.get("cfg")), encoding="utf-8"))
S = next(s for s in CFG["shots"] if s["id"] == int(a.get("shot")))
T0 = S["start"]
kit.setup(view="Standard", look=None, bloom=0, motion_blur=0, world="#000000")
cam = kit.camera((0, -10, 0), look_at=(0, 0, 0), lens=50)
if S.get("nametag"):
    nt = S["nametag"]
    rt.name_tag(cam, nt["name"], nt["role"], start_frame=kit.f(nt["at"] - T0))
if S.get("stamp"):
    st = S["stamp"]
    rt.date_stamp(cam, st["line"], st.get("sub"), start_frame=kit.f(st["at"] - T0), cps=34, sub_cps=60)
