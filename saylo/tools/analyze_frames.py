"""Frame-by-frame edit analysis of a reference video (every frame, 30 fps): every cut, what kind of transition it is,
and how the camera moves inside each shot.

  python saylo/tools/analyze_frames.py <work_dir>

<work_dir> holds  frames/00001.jpg ... (every frame, 320x180:  ffmpeg -i ref.mp4 -vf scale=320:180 -q:v 5 frames/%05d.jpg)
and scene_all.txt (ffmpeg per-frame scene score:  -vf "select='gte(scene,0)',metadata=print:file=scene_all.txt").
Writes shots.json (one row per shot) and sheets/shots-NN.jpg (first / middle / last frame of every shot, numbered).

Per shot: start/end frame and time, length, how it was entered (hard cut / dissolve / fade from black / flash),
camera motion from tracked features (zoom % per second = push in or pull out, pan and tilt in % of the frame per
second, rotation), how much of the picture changes besides the camera (subject motion), brightness, colourfulness.
"""
import json
import os
import re
import sys

import cv2
import numpy as np

W = sys.argv[1]
FPS = 30.0
FR = os.path.join(W, "frames")
names = sorted(os.listdir(FR))
n = len(names)

score = np.zeros(n)
txt = open(os.path.join(W, "scene_all.txt"), encoding="utf-8").read()
for i, m in enumerate(re.finditer(r"scene_score=([0-9.]+)", txt)):
    if i + 1 < n:
        score[i + 1] = float(m.group(1))        # score of frame i+1 against frame i (first frame has none)

gray, luma, sat = [], np.zeros(n), np.zeros(n)
for i, nm in enumerate(names):
    im = cv2.imread(os.path.join(FR, nm))
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray.append(g)
    luma[i] = g.mean()
    sat[i] = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[..., 1].mean()
diff = np.zeros(n)
for i in range(1, n):
    diff[i] = np.abs(gray[i].astype(np.int16) - gray[i - 1].astype(np.int16)).mean()

# ---- cuts: a frame whose change is a spike against its neighbours (a camera move changes every frame a little)
cuts = [0]
for i in range(2, n - 1):
    local = np.median(diff[max(1, i - 6):i].tolist() + diff[i + 1:i + 7].tolist())
    if (score[i] > 0.14 and diff[i] > 3.2 * max(local, 0.6)) or (diff[i] > 22 and diff[i] > 4 * max(local, 0.6)):
        if i - cuts[-1] >= 3:
            cuts.append(i)
        elif diff[i] > diff[cuts[-1]]:
            cuts[-1] = i
cuts.append(n)


def motion(a, b):
    """Camera move between two frames from tracked corners: (zoom factor, dx, dy, rotation deg, inlier share)."""
    p0 = cv2.goodFeaturesToTrack(gray[a], 300, 0.01, 6)
    if p0 is None or len(p0) < 12:
        return None
    p1, st, _ = cv2.calcOpticalFlowPyrLK(gray[a], gray[b], p0, None, winSize=(21, 21), maxLevel=3)
    ok = st.ravel() == 1
    if ok.sum() < 12:
        return None
    M, inl = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
    if M is None:
        return None
    s = float(np.hypot(M[0, 0], M[1, 0]))
    cx, cy = 160, 90
    dx = M[0, 0] * cx + M[0, 1] * cy + M[0, 2] - cx      # shift of the frame centre
    dy = M[1, 0] * cx + M[1, 1] * cy + M[1, 2] - cy
    return s, dx, dy, float(np.degrees(np.arctan2(M[1, 0], M[0, 0]))), float(inl.mean())


shots = []
for k in range(len(cuts) - 1):
    a, b = cuts[k], cuts[k + 1] - 1
    L = b - a + 1
    # how the shot starts
    kind = "hard cut"
    if a == 0:
        kind = "start"
    else:
        pre = luma[max(0, a - 3):a].mean()
        if pre < 12:
            kind = "from black"
        elif luma[a:a + 2].max() > 200 and luma[a:a + 2].max() > 1.7 * np.median(luma[a:b + 1]):
            kind = "white flash"
    # dissolve: change stays high for many frames with no single spike at the cut (checked on the frames before it)
    if a > 12 and kind == "hard cut":
        ramp = diff[a - 10:a]
        if np.median(ramp) > 4.5 and diff[a] < 2.2 * np.median(ramp):
            kind = "dissolve?"
    flash = [int(i) for i in range(a + 1, b) if luma[i] > 205 and luma[i] > 1.6 * np.median(luma[a:b + 1])]
    # camera move, accumulated over steps of 3 frames
    zoom, tx, ty, rot, used, inl = 1.0, 0.0, 0.0, 0.0, 0, []
    step = 3
    for i in range(a + 1, b - step, step):
        mv = motion(i, i + step)
        if mv is None:
            continue
        zoom *= mv[0]
        tx += mv[1]
        ty += mv[2]
        rot += mv[3]
        inl.append(mv[4])
        used += 1
    dur = L / FPS
    cover = used * step / max(1, L)
    body = diff[a + 1:b + 1] if L > 1 else np.array([0.0])
    shots.append(dict(
        id=k + 1, f0=a + 1, f1=b + 1, t0=round(a / FPS, 3), t1=round((b + 1) / FPS, 3), frames=L, sec=round(dur, 2),
        enter=kind, flash_frames=flash[:6],
        zoom_pct_s=round((zoom - 1) * 100 / max(dur, 0.1), 2), pan_pct_s=round(tx / 320 * 100 / max(dur, 0.1), 2),
        tilt_pct_s=round(ty / 180 * 100 / max(dur, 0.1), 2), rot_deg_s=round(rot / max(dur, 0.1), 2),
        track_cover=round(cover, 2), track_inliers=round(float(np.mean(inl)) if inl else 0.0, 2),
        change=round(float(body.mean()), 2), still=bool(body.mean() < 0.35),
        luma=round(float(luma[a:b + 1].mean()), 1), sat=round(float(sat[a:b + 1].mean()), 1)))

for s in shots:
    z, p, t = s["zoom_pct_s"], s["pan_pct_s"], s["tilt_pct_s"]
    parts = []
    if s["still"]:
        parts.append("frozen")
    if abs(z) >= 1.0:
        parts.append(("push in" if z > 0 else "pull out") + f" {abs(z):.1f}%/s")
    if abs(p) >= 1.5:
        parts.append(("picture moves right (camera left)" if p > 0 else "picture moves left (camera right)") + f" {abs(p):.1f}%/s")
    if abs(t) >= 1.5:
        parts.append(("picture moves down (camera up)" if t > 0 else "picture moves up (camera down)") + f" {abs(t):.1f}%/s")
    if abs(s["rot_deg_s"]) >= 0.6:
        parts.append(f"roll {s['rot_deg_s']:.1f} deg/s")
    s["camera"] = ", ".join(parts) or "locked off / drift under 1%/s"

json.dump(dict(fps=FPS, frames=n, shots=shots), open(os.path.join(W, "shots.json"), "w"), indent=1)

# ---- sheets: first / middle / last frame of every shot, 12 shots a sheet
os.makedirs(os.path.join(W, "sheets"), exist_ok=True)
PER = 12
for page in range(0, len(shots), PER):
    rows = []
    for s in shots[page:page + PER]:
        a, b = s["f0"] - 1, s["f1"] - 1
        tiles = []
        for i in (a, (a + b) // 2, b):
            im = cv2.imread(os.path.join(FR, names[i]))
            tiles.append(im)
        row = np.hstack(tiles)
        label = f"#{s['id']}  {s['t0']:.2f}s  {s['sec']}s ({s['frames']}f)  {s['enter']}  |  {s['camera'][:70]}"
        bar = np.zeros((22, row.shape[1], 3), np.uint8)
        cv2.putText(bar, label, (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        rows.append(np.vstack([bar, row]))
    # two columns of 6
    half = (len(rows) + 1) // 2
    cols = []
    for part in (rows[:half], rows[half:]):
        while len(part) < half:
            part.append(np.zeros_like(rows[0]))
        cols.append(np.vstack(part))
    cv2.imwrite(os.path.join(W, "sheets", f"shots-{page // PER + 1:02d}.jpg"), np.hstack(cols), [cv2.IMWRITE_JPEG_QUALITY, 82])

L = np.array([s["frames"] for s in shots]) / FPS
print("shots", len(shots), "mean", round(L.mean(), 2), "median", round(float(np.median(L)), 2), "under1s", int((L < 1).sum()),
      "under2s", int((L < 2).sum()), "over6s", int((L > 6).sum()), "longest", round(L.max(), 1))
print("cuts first 60s", sum(1 for s in shots if 0 < s["t0"] < 60), "first 120s", sum(1 for s in shots if 0 < s["t0"] < 120))
from collections import Counter
print(Counter(s["enter"] for s in shots))
