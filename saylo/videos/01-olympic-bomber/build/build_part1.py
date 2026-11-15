"""Build part 1 (cold open + The Park, 0:00-4:00) from plan_cold_open.py + plan_park.py.

    python saylo/videos/01-olympic-bomber/build/build_part1.py

Source files are read from ../media (the creator's Drive clips folder, not in git). Any file that is missing is
replaced by a typed "MISSING" card so the cut can still be reviewed; the missing names are printed at the end.
Writes render/part1.mp4 (after assemble.py + edit_video.py). Needs SAYLO_EFFECTS for the Template Library effects
(defaults to the kit unpacked in <repo>/_kit).
"""
import json, os, runpy, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(VID, "..", "..", ".."))
TOOLS = os.path.join(REPO, "saylo", "tools")
MEDIA = os.path.join(VID, "media")
OUT = os.path.join(VID, "render")
os.environ.setdefault("SAYLO_EFFECTS", os.path.join(REPO, "_kit", "Faceless Studio", ".claude", "effects"))

segs, music, sfx, cues = [], [], [], []
for name in ("plan_cold_open.py", "plan_park.py"):
    p = runpy.run_path(os.path.join(HERE, name))
    segs += p["S"]
    music += p["MUSIC"]
    sfx += [dict(at=a, file=f, gain=g) for a, f, g in p["SFX"]]
    cues += [l for l in p.get("CUES", "").splitlines() if l.strip()]

missing = []
def have(f):
    ok = os.path.exists(os.path.join(MEDIA, f))
    if not ok and f not in missing:
        missing.append(f)
    return ok

for s in segs:
    need = [s[k] for k in ("src", "bg") if s.get(k)]
    ov = s.get("ov", {})
    need += ov.get("images", []) + ([ov["backgroundImage"]] if ov.get("backgroundImage") else [])
    gone = [f for f in need if not have(f)]
    if gone:
        label = os.path.splitext(gone[0])[0].upper()
        for k in ("src", "effect", "ov", "tag", "in", "crop", "motion", "fx", "bg"):
            s.pop(k, None)
        s["card"] = [["MISSING CLIP", "amber"], [label[:40], "small"]]

os.makedirs(OUT, exist_ok=True)
plan = dict(assets=MEDIA, voiceover=os.path.join(VID, "voiceover-full.mp3"),
            music_dir=os.path.join(VID, "sound", "music"), sfx_dir=os.path.join(VID, "sound", "sfx"),
            segments=segs, music=music, sfx=sfx)
pj = os.path.join(OUT, "part1.plan.json")
json.dump(plan, open(pj, "w"), indent=1)
open(os.path.join(OUT, "part1.cues.txt"), "w").write("\n".join(cues) + "\n")

raw = os.path.join(OUT, "part1_raw.mp4")
subprocess.run([sys.executable, os.path.join(TOOLS, "assemble.py"), pj, raw], check=True)
subprocess.run([sys.executable, os.path.join(TOOLS, "edit_video.py"), raw, os.path.join(OUT, "part1.cues.txt"),
                os.path.join(OUT, "part1.mp4")], check=True)
print("wrote", os.path.join(OUT, "part1.mp4"))
print("MISSING (placeholder cards):", missing or "none")
