"""Join the rendered sections into the full video, with the complete voiceover on top.

Usage: python3 video/01-follow-one-dollar/motion/assemble.py

Each section was rendered with a little overlap at its end, so every section is trimmed to
the exact frame where the next one starts. The frame counts come from the voiceover timings,
so the pictures stay locked to the voice from the first second to the last.
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
AUDIO = os.path.join(ROOT, "audio", "follow-one-dollar-v6")
SECTIONS = [("hook", "S001"), ("pizza", "S012"), ("stop1", "S031"), ("stop2", "S040"), ("stop3", "S055"), ("stop4", "S067"),
            ("stop5", "S086"), ("money", "S102"), ("basket", "S127"), ("checks", "S142"), ("ending", "S154")]
FPS = 30

T = json.load(open(os.path.join(AUDIO, "timings.json")))
start = {l["id"]: l["start"] for l in T["lines"]}
t0 = [0.0 if i == 0 else start[first] - 0.2 for i, (_, first) in enumerate(SECTIONS)] + [T["duration"]]
frames = [round(t0[i + 1] * FPS) - round(t0[i] * FPS) for i in range(len(SECTIONS))]

inputs, filt = [], ""
for i, (name, _) in enumerate(SECTIONS):
    inputs += ["-i", os.path.join(HERE, name, name + ".mp4")]
    # hold the last frame if a section is a frame short, then cut to the exact length
    filt += f"[{i}:v]fps={FPS},tpad=stop_mode=clone:stop_duration=1,trim=end_frame={frames[i]},setpts=PTS-STARTPTS[v{i}];"
filt += "".join(f"[v{i}]" for i in range(len(SECTIONS))) + f"concat=n={len(SECTIONS)}:v=1:a=0[v]"
out_dir = os.path.join(HERE, "..", "final")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "follow-one-dollar.mp4")
# master audio (voice + music + sound effects from mix_audio.py) if it exists, else the voice alone
master = os.path.join(out_dir, "master-audio.wav")
sound = master if os.path.exists(master) else os.path.join(AUDIO, "narration.mp3")
print("audio:", os.path.relpath(sound, ROOT))
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-i", sound, "-filter_complex", filt,
                "-map", "[v]", "-map", f"{len(SECTIONS)}:a", "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], check=True)
for (name, first), f, t in zip(SECTIONS, frames, t0):
    print(f"{name:7s} starts {int(t // 60)}:{t % 60:04.1f}  {f / FPS:6.1f} s")
print("wrote", out)
