"""Shot-by-shot deep breakdown (uses tools/analyze_frames.py JSON for cuts and motion).

Usage:
    python3 tools/deep_shots.py <video.mp4> <frames.json> <out_dir>

For every shot: length, camera move (push / pull / pan / tilt / shake / static, from optical
flow), lighting and grade at the middle frame (brightness, contrast, saturation, warm/cool,
vignette = how much darker the corners are, highlight/shadow share, 5 dominant colours),
and a mid-frame crop for looking at faces and expressions. Writes shots.json, a palette strip
and a contact sheet of every shot's middle frame.
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw


def classify(frames):
    if not frames:
        return "static"
    z = np.array([f.get("zoom", 0) for f in frames])
    px = np.array([f.get("pan_x", 0) for f in frames])
    py = np.array([f.get("pan_y", 0) for f in frames])
    fl = np.array([f.get("flow", 0) for f in frames])
    if fl.mean() < 0.06:
        return "static"
    jitter = np.std(np.diff(px)) + np.std(np.diff(py))
    if jitter > 0.6:
        return "shake"
    if abs(z.mean()) > 0.04 and abs(z.mean()) > 0.6 * max(abs(px.mean()), abs(py.mean())):
        return "push-in" if z.mean() > 0 else "pull-back"
    if abs(px.mean()) >= abs(py.mean()):
        return "pan-left" if px.mean() > 0 else "pan-right"
    return "tilt-down" if py.mean() < 0 else "tilt-up"


def grade(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[..., 2].astype(float)
    h, w = v.shape
    corners = np.concatenate([v[:h // 6, :w // 6].ravel(), v[:h // 6, -w // 6:].ravel(), v[-h // 6:, :w // 6].ravel(), v[-h // 6:, -w // 6:].ravel()])
    centre = v[h // 3:2 * h // 3, w // 3:2 * w // 3]
    b, g, r = [img[..., i].astype(float).mean() for i in range(3)]
    px = img.reshape(-1, 3).astype(np.float32)
    _, labels, centers = cv2.kmeans(px, 5, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 2, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.ravel(), minlength=5)
    order = np.argsort(-counts)
    pal = [("#%02x%02x%02x" % tuple(int(c) for c in centers[i][::-1]), round(float(counts[i] / counts.sum()), 2)) for i in order]
    return dict(brightness=round(float(v.mean()), 1), contrast=round(float(v.std()), 1),
                saturation=round(float(hsv[..., 1].mean()), 1), warmth=round(r - b, 1),
                vignette=round(float(centre.mean() - corners.mean()), 1),
                highlights=round(float((v > 220).mean()), 3), shadows=round(float((v < 40).mean()), 3), palette=pal)


def main(video, frames_json, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    data = json.load(open(frames_json))
    frames = data["frames"]
    dur = data["summary"]["seconds"]
    bounds = [0.0] + data["cuts"] + [dur]
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    shots, thumbs = [], []
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        fr = [f for f in frames[1:] if a + 0.05 < f["t"] < b - 0.05]
        cap.set(cv2.CAP_PROP_POS_FRAMES, int((a + b) / 2 * fps))
        ok, img = cap.read()
        if not ok:
            continue
        g = grade(cv2.resize(img, (216, 384)))
        shots.append(dict(i=i, start=round(a, 2), length=round(b - a, 2), move=classify(fr),
                          move_speed=round(float(np.mean([f.get("flow", 0) for f in fr])) if fr else 0, 3), **g))
        thumbs.append(cv2.cvtColor(cv2.resize(img, (135, 240)), cv2.COLOR_BGR2RGB))
    cap.release()
    json.dump(shots, open(os.path.join(out_dir, "shots.json"), "w"), indent=1)
    cols = 12
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 135, rows * 262), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for k, (t, s) in enumerate(zip(thumbs, shots)):
        x, y = (k % cols) * 135, (k // cols) * 262
        sheet.paste(Image.fromarray(t), (x, y))
        d.text((x + 3, y + 242), f"{s['start']:.1f}s {s['move'][:8]}", fill=(255, 255, 0))
    sheet.save(os.path.join(out_dir, "shots-sheet.jpg"), quality=85)
    moves = {}
    for s in shots:
        moves[s["move"]] = moves.get(s["move"], 0) + 1
    avg = {k: round(float(np.mean([s[k] for s in shots])), 1) for k in ("brightness", "contrast", "saturation", "warmth", "vignette")}
    avg["highlights"] = round(float(np.mean([s["highlights"] for s in shots])), 3)
    avg["shadows"] = round(float(np.mean([s["shadows"] for s in shots])), 3)
    summary = dict(shots=len(shots), moves=moves, **avg)
    json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
