"""Stills first (creator's review rule): one frame per shot of a plan, with the narration line under it, on one sheet.
  python stills.py shots3.json [--only 101,116]
Real clips, freeze frames and photos are cut with ffmpeg exactly as assemble.py will cut them (crop, grade, source tag);
3D shots, maps and cards are rendered as a single still through the Blender runner.
Output: build/render/<plan dir>/stills/Sxxx.png and build/render/<plan dir>_stills.jpg"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.normpath(os.path.join(HERE, "..", ".."))
REPO = os.path.normpath(os.path.join(VID, "..", "..", ".."))
TAGS = os.path.join(REPO, "saylo", "assets", "source-tags")
STUDIO = os.path.join(REPO, "_kit", "docpro", "Faceless Studio")
RUNNER = os.path.join(STUDIO, ".claude", "skills", "documentary-pro", "scripts", "render_blender.py")
plan = sys.argv[1]
only = set(int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
cfg = json.load(open(os.path.join(HERE, plan), encoding="utf-8"))
FPS = cfg["fps"]
SRC = cfg.get("src", {})
out_dir = os.path.join(VID, "build", "render", cfg["dir"], "stills")
os.makedirs(out_dir, exist_ok=True)
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-nostdin"]
GRADE = "eq=saturation=0.72:contrast=1.06:brightness=-0.03"
SCRIPT = {"open": "S_open.py", "map": "S_map.py", "map2": "S_map2.py", "photo": "S_photo.py", "card": "S_card.py",
          "3d": "S_airfield.py", "barracks": "S_barracks.py", "obj": "S_objects.py"}


def src_path(s):
    return os.path.join(VID, "media", "src", SRC.get(s["src"], s["src"]))


def fit(s):
    if s.get("crop"):
        return [f"crop={s['crop']}", "scale=1920:1080:flags=lanczos", "setsar=1"]
    if s.get("fit") == "contain":
        return ["scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos",
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0A0F1B", "setsar=1"]
    return ["scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos", "crop=1920:1080", "setsar=1"]


def overlay_png(s, n):
    """Last frame of the shot's typed overlay (name tag / stamp), with alpha, or None."""
    if not (s.get("nametag") or s.get("stamp")) or s["kind"] not in ("clip", "image", "still"):
        return None
    tmp = os.path.join(out_dir, f"O{s['id']:03d}.mov")
    r = subprocess.run([sys.executable, RUNNER, os.path.join(HERE, "O_text.py"), "--out", tmp, "--frames", str(n), "--alpha", "--stills", str(n),
                        "--arg", f"shot={s['id']}", "--arg", f"cfg={plan}", "--wait", "1500"], cwd=STUDIO, capture_output=True, text=True)
    png = os.path.join(out_dir, f"O{s['id']:03d}-still-{n:04d}.png")
    if not os.path.exists(png):
        print("   overlay FAILED", (r.stdout + r.stderr)[-400:], flush=True)
        return None
    return png


def ff_still(inputs, vf, s, dst):
    cmd = FF + inputs
    chain = ",".join(vf)
    n = round(s["end"] * FPS) - round(s["start"] * FPS)
    extra = [p for p in ((os.path.join(TAGS, s["tag"]) if s.get("tag") else None), overlay_png(s, n)) if p]
    if extra:
        fc, last = f"[0:v]{chain}[m0]", "m0"
        for i, p in enumerate(extra):
            cmd += ["-i", p]
            fc += f";[{last}][{i + 1}:v]overlay=0:0[m{i + 1}]"
            last = f"m{i + 1}"
        fc += f";[{last}]null[v]"
    else:
        fc = f"[0:v]{chain}[v]"
    subprocess.run(cmd + ["-filter_complex", fc, "-map", "[v]", "-frames:v", "1", dst], check=True, stdin=subprocess.DEVNULL)


made = []
for s in cfg["shots"]:
    dst = os.path.join(out_dir, f"S{s['id']:03d}.png")
    made.append((s, dst))
    if only and s["id"] not in only:
        continue
    n = round(s["end"] * FPS) - round(s["start"] * FPS)
    k = s["kind"]
    print("..", s["id"], k, flush=True)
    if k == "clip":
        z = []
        if s.get("zoom"):
            zz = s["zoom"]
            z = [f"crop=iw/{zz}:ih/{zz}:(iw-iw/{zz})*{s['cx']}:(ih-ih/{zz})*{s['cy']}"]
        ff_still(["-ss", str(s["out"] - 0.1 if (s.get("nametag") or s.get("stamp")) else (s["in"] + s["out"]) / 2), "-i", src_path(s)], ([f"crop={s['crop']}"] if s.get("crop") else []) + z
                 + ["scale=1920:1080:flags=lanczos", "setsar=1", GRADE], s, dst)
    elif k == "still":
        ff_still(["-ss", str(s["at"]), "-i", src_path(s)], ([f"crop={s['crop']}"] if s.get("crop") else [])
                 + ["scale=1920:1080:flags=lanczos", "setsar=1", GRADE], s, dst)
    elif k == "image":
        ff_still(["-i", os.path.join(VID, *s["img"].split("/"))], fit(s) + [GRADE], s, dst)
    elif k == "reuse":
        ff_still(["-ss", str(s.get("at", 0) + n / FPS / 2), "-i", os.path.join(VID, "build", "render", *s["from"].split("/"))],
                 ["null"], s, dst)
    else:
        frame = n if (k in ("card", "map", "map2") or s.get("last")) else max(1, int(n * s.get("still_at", 0.88)))      # typed shots: the last frame, so unfinished typing shows
        tmp = os.path.join(out_dir, f"R{s['id']:03d}.mp4")
        r = subprocess.run([sys.executable, RUNNER, os.path.join(HERE, SCRIPT[k]), "--out", tmp, "--frames", str(n), "--stills", str(frame),
                            "--arg", f"shot={s['id']}", "--arg", f"cfg={plan}", "--wait", "1500"], cwd=STUDIO, capture_output=True, text=True)
        png = os.path.join(out_dir, f"R{s['id']:03d}-still-{frame:04d}.png")
        if not os.path.exists(png):
            print("   FAILED", (r.stdout + r.stderr)[-600:], flush=True)
            continue
        ff_still(["-i", png], ["null"], s, dst)

# sheet: 4 across, the line and what it shows under each frame
TW, TH, CAP = 600, 338, 62
tiles = []
for s, dst in made:
    im = cv2.imread(dst) if os.path.exists(dst) else None
    im = cv2.resize(im, (TW, TH)) if im is not None else np.zeros((TH, TW, 3), np.uint8)
    cap = np.full((CAP, TW, 3), 18, np.uint8)
    cv2.putText(cap, f"{s['id']}  {s['start']:.1f}s  ({s['end'] - s['start']:.1f}s)  {s['kind']}", (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (120, 190, 255), 1, cv2.LINE_AA)
    cv2.putText(cap, '"' + s["line"][:62] + '"', (6, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.47, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(cap, s["what"][:74], (6, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (170, 170, 170), 1, cv2.LINE_AA)
    tiles.append(np.vstack([im, cap]))
while len(tiles) % 4:
    tiles.append(np.zeros((TH + CAP, TW, 3), np.uint8))
sheet = np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)])
out = os.path.join(VID, "build", "render", cfg["dir"] + "_stills.jpg")
cv2.imwrite(out, sheet, [cv2.IMWRITE_JPEG_QUALITY, 84])
print(out)
