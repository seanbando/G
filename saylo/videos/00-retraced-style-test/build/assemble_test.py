"""Join the rendered shots (render/shots/S01..S13.mp4) with the real cold-open narration, a music bed and the
typewriter clicks for every typed text. Output: render/retraced_style_test.mp4 (1080p30, -14 LUFS)."""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(HERE)
REPO = os.path.normpath(os.path.join(VID, "..", "..", ".."))
OB = os.path.join(REPO, "saylo", "videos", "01-olympic-bomber")
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf-8"))
shots_dir = os.path.join(VID, "render", "shots")
out = os.path.join(VID, "render", "retraced_style_test.mp4")
END = cfg["end"]

lst = os.path.join(shots_dir, "list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for s in cfg["shots"]:
        fh.write(f"file 'S{s['id']:02d}.mp4'\n")

# typed text moments (VO seconds) -> keystroke length
TYPES = [(0.25, "short"), (4.55, "short"), (7.38, "short"), (17.6, "medium"), (23.02, "short")]
sfx = os.path.join(OB, "sound", "sfx")
inputs = ["-f", "concat", "-safe", "0", "-i", lst,
          "-t", str(END), "-i", os.path.join(OB, "voiceover-full.mp3"),
          "-stream_loop", "-1", "-i", os.path.join(OB, "sound", "music", "bed-A.mp3")]
filt = ["[1:a]volume=1.0[vo]", f"[2:a]atrim=0:{END},volume=0.16,afade=t=out:st={END - 1.2}:d=1.2[bed]"]
mix = ["[vo]", "[bed]"]
for i, (t, kind) in enumerate(TYPES):
    inputs += ["-i", os.path.join(sfx, f"sfx-typewriter-keys-{kind}.mp3")]
    k = 3 + i
    filt.append(f"[{k}:a]atrim=0:0.9,afade=t=out:st=0.6:d=0.3,volume=0.35,adelay={int(t * 1000)}|{int(t * 1000)}[k{i}]")
    mix.append(f"[k{i}]")
filt.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[a]")

cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filt),
       "-map", "0:v", "-map", "[a]", "-t", str(END), "-c:v", "libx264", "-crf", "17", "-preset", "slow",
       "-pix_fmt", "yuv420p", "-r", str(cfg["fps"]), "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print(out)
