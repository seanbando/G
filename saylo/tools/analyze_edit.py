"""Measure the editing style of a reference video (cuts, pacing, fades, silence).

Usage:
    python3 saylo/tools/analyze_edit.py <video.mp4> [more.mp4 ...] [--sheets OUT_DIR]

Needs ffmpeg/ffprobe. A compressed copy (360p-480p, audio kept, full length) is enough.

Prints, per video:
  - duration, shot count, mean/median shot length
  - share of shots under 2s and over 10s, longest shot
  - cuts per minute in each third of the video, and cuts in the first 60s (the hook)
  - fades to black and moments of full silence

With --sheets, also writes contact sheets you can look at:
  <name>.overview-N.jpg  one frame every 20s (6x5 grid per image)
  <name>.hook.jpg        one frame every 2s for the first 60s
Look at those to read the visual grammar (maps, documents, name tags, push-ins).

Cut detection uses ffmpeg's scene score > 0.3. It catches hard cuts; slow
dissolves and continuous camera moves inside one shot are not counted as cuts.
"""
import os
import re
import statistics as st
import subprocess
import sys


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout
    return float(out.strip())


def ffmpeg_log(args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args, "-f", "null", "-"],
                          capture_output=True, text=True).stderr


def cuts(path):
    log = ffmpeg_log(["-i", path, "-an", "-vf", "scale=320:-2,select='gt(scene,0.3)',showinfo"])
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", log)]


def blacks(path):
    log = ffmpeg_log(["-i", path, "-an", "-vf", "scale=160:-2,blackdetect=d=0.3:pix_th=0.08"])
    return log.count("black_start")


def silences(path):
    log = ffmpeg_log(["-i", path, "-vn", "-af", "silencedetect=n=-40dB:d=0.6"])
    return log.count("silence_start")


def sheets(path, out_dir):
    name = os.path.splitext(os.path.basename(path))[0]
    os.makedirs(out_dir, exist_ok=True)
    base = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", path]
    subprocess.run(base + ["-vf", "fps=1/20,scale=320:-2,tile=6x5",
                           os.path.join(out_dir, f"{name}.overview-%d.jpg")])
    subprocess.run(base + ["-t", "60", "-vf", "fps=1/2,scale=320:-2,tile=6x5", "-frames:v", "1",
                           os.path.join(out_dir, f"{name}.hook.jpg")])


def report(path):
    d = duration(path)
    c = cuts(path)
    edges = [0.0, *c, d]
    shots = [b - a for a, b in zip(edges, edges[1:])]
    thirds = [sum(1 for x in c if i * d / 3 <= x < (i + 1) * d / 3) / (d / 3 / 60) for i in range(3)]
    print(f"\n== {os.path.basename(path)}  ({d / 60:.1f} min)")
    print(f"shots: {len(shots)}   mean {st.mean(shots):.1f}s   median {st.median(shots):.1f}s   longest {max(shots):.0f}s")
    print(f"under 2s: {sum(s < 2 for s in shots) / len(shots):.0%}   over 10s: {sum(s > 10 for s in shots) / len(shots):.0%}")
    print(f"cuts/min by third: {' / '.join(f'{t:.1f}' for t in thirds)}   cuts in first 60s: {sum(1 for x in c if x < 60)}")
    print(f"fades to black: {blacks(path)}   full silences (>0.6s): {silences(path)}")


def main(argv):
    out_dir = None
    if "--sheets" in argv:
        i = argv.index("--sheets")
        out_dir = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        sys.exit(__doc__)
    for path in argv:
        report(path)
        if out_dir:
            sheets(path, out_dir)
    if out_dir:
        print(f"\ncontact sheets in {out_dir}")


if __name__ == "__main__":
    main(sys.argv[1:])
