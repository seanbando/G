"""Frame-by-frame breakdown of a short (every frame at its native fps).

Usage:
    python3 tools/analyze_frames.py <video.mp4> <out.json> [--trim-end 3]

Per frame: hard-cut detection (histogram + pixel change), camera motion inside a shot
(global zoom / pan from optical flow), on-screen change in the caption band, brightness
and saturation. Per second: cuts, motion, caption swaps. Audio: loudness (LUFS), peaks,
onsets (hits/whooshes) per second. Prints a summary and writes everything to JSON.
"""
import json
import subprocess
import sys

import cv2
import numpy as np


def audio_stats(path, end):
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", path, "-t", str(end), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    lufs = [l for l in r.splitlines() if l.strip().startswith("I:")]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-t", str(end), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float)
    hop = 160
    e = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    db = 20 * np.log10(e + 1)
    flux = np.maximum(0, np.diff(db))
    on = [i * 0.01 for i in range(1, len(flux)) if flux[i] > 8 and db[i + 1] > db.max() - 25]
    dedup = []
    for t in on:
        if not dedup or t - dedup[-1] > 0.08:
            dedup.append(round(t, 2))
    quiet = float((db < db.max() - 35).mean())
    return dict(lufs=lufs[-1].split(":")[1].strip() if lufs else None, onsets=dedup, quiet_share=round(quiet, 3))


def main(path, out, trim_end=0.0):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    end_frame = n - int(trim_end * fps)
    prev = prev_hist = prev_small = None
    frames = []
    i = 0
    while i < end_frame:
        ok, f = cap.read()
        if not ok:
            break
        small = cv2.resize(f, (180, 320))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [32, 16], [0, 180, 0, 256])
        cv2.normalize(hist, hist)
        rec = dict(t=round(i / fps, 3), bright=float(hsv[..., 2].mean()), sat=float(hsv[..., 1].mean()))
        if prev is not None:
            hd = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
            pd = float(np.abs(gray.astype(float) - prev.astype(float)).mean())
            rec.update(hist_diff=float(hd), pix_diff=pd)
            band = slice(int(320 * 0.62), int(320 * 0.86))
            rec["cap_diff"] = float(np.abs(gray[band].astype(float) - prev[band].astype(float)).mean())
            flow = cv2.calcOpticalFlowFarneback(prev, gray, None, 0.5, 2, 15, 2, 5, 1.1, 0)
            ys, xs = np.mgrid[0:320, 0:180]
            rx, ry = xs - 90, ys - 160
            radial = (flow[..., 0] * rx + flow[..., 1] * ry) / (np.sqrt(rx ** 2 + ry ** 2) + 1)
            rec.update(zoom=float(radial.mean()), pan_x=float(np.median(flow[..., 0])), pan_y=float(np.median(flow[..., 1])),
                       flow=float(np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2).mean()))
        frames.append(rec)
        prev, prev_hist = gray, hist
        i += 1
    cap.release()
    dur = len(frames) / fps
    # cuts: big histogram jump or pixel jump relative to local motion
    cuts = []
    for k, r in enumerate(frames[1:], 1):
        if r["hist_diff"] > 0.35 or (r["pix_diff"] > 28 and r["pix_diff"] > 3 * np.median([x.get("pix_diff", 0) for x in frames[max(1, k - 15):k]] or [1])):
            if not cuts or r["t"] - cuts[-1] > 0.15:
                cuts.append(r["t"])
    shots = np.diff([0.0] + cuts + [dur])
    caps = [r["t"] for r in frames[1:] if r["cap_diff"] > 6]
    cap_swaps = []
    for t in caps:
        if not cap_swaps or t - cap_swaps[-1] > 0.2:
            cap_swaps.append(t)
    moving = [r for r in frames[1:] if r["flow"] > 0.25 and r["t"] not in cuts]
    zoom_in = sum(1 for r in moving if r["zoom"] > 0.05) / max(1, len(frames))
    zoom_out = sum(1 for r in moving if r["zoom"] < -0.05) / max(1, len(frames))
    still = sum(1 for r in frames[1:] if r["flow"] < 0.05 and r["pix_diff"] < 0.5) / max(1, len(frames))
    per_sec = []
    for s in range(int(dur)):
        fr = [r for r in frames[1:] if s <= r["t"] < s + 1]
        per_sec.append(dict(s=s, cuts=sum(1 for c in cuts if s <= c < s + 1),
                            motion=round(float(np.mean([r["flow"] for r in fr])), 3) if fr else 0,
                            caps=sum(1 for c in cap_swaps if s <= c < s + 1)))
    aud = audio_stats(path, dur)
    summary = dict(file=path, fps=fps, frames=len(frames), seconds=round(dur, 2), cuts=len(cuts),
                   avg_shot=round(float(shots.mean()), 2), median_shot=round(float(np.median(shots)), 2),
                   longest_shot=round(float(shots.max()), 2), shots_over_3s=int((shots > 3).sum()),
                   first_cut=cuts[0] if cuts else None, cuts_first_5s=sum(1 for c in cuts if c < 5),
                   caption_swaps=len(cap_swaps), caption_swaps_per_s=round(len(cap_swaps) / dur, 2),
                   frames_zooming_in=round(zoom_in, 3), frames_zooming_out=round(zoom_out, 3), frames_dead_still=round(still, 3),
                   brightness=round(float(np.mean([r["bright"] for r in frames])), 1),
                   saturation=round(float(np.mean([r["sat"] for r in frames])), 1),
                   audio_lufs=aud["lufs"], audio_hits=len(aud["onsets"]), audio_hits_per_s=round(len(aud["onsets"]) / dur, 2),
                   audio_quiet_share=aud["quiet_share"])
    json.dump(dict(summary=summary, cuts=cuts, shots=[round(float(x), 2) for x in shots], caption_swaps=cap_swaps,
                   per_second=per_sec, audio_onsets=aud["onsets"], frames=frames), open(out, "w"))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    argv = sys.argv[1:]
    te = 0.0
    if "--trim-end" in argv:
        k = argv.index("--trim-end")
        te = float(argv[k + 1])
        del argv[k:k + 2]
    main(*argv, trim_end=te)
