"""Burn captions into a finished vertical video, as the very last step.

Usage:
    python3 tools/burn_captions.py <in.mp4> <captions.srt> <out.mp4> [--y 0.74] [--size 0.075]

Reference-short style: 2 to 3 words at a time, bold white text with a thick
black outline, a quick pop as each caption appears. Placed low (centre at
--y of the height, default 74%) so it stays off the drawings and above the
app buttons at the bottom; --size is the text height as a share of the
frame width. Audio is copied unchanged.
"""
import os
import re
import subprocess
import sys
import tempfile


def probe(path):
    w, h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                           "stream=width,height", "-of", "csv=p=0", path],
                          capture_output=True, text=True).stdout.strip().split(",")
    return int(w), int(h)


def srt_to_ass(srt, ass, w, h, y, size):
    font_px = int(w * size)
    margin_v = int(h * (1 - y) - font_px / 2)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter ExtraBold,{font_px},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,{max(3, font_px // 9)},2,2,{int(w * 0.08)},{int(w * 0.08)},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def t(x):
        hh, mm, rest = x.split(":")
        ss, ms = rest.split(",")
        return f"{int(hh)}:{mm}:{ss}.{ms[:2]}"

    events = []
    for block in re.split(r"\n\s*\n", open(srt).read().strip()):
        rows = block.splitlines()
        if len(rows) < 3:
            continue
        start, end = [s.strip() for s in rows[1].split("-->")]
        text = " ".join(rows[2:]).replace("{", "(").replace("}", ")")
        pop = r"{\fscx82\fscy82\t(0,90,\fscx100\fscy100)}"
        events.append(f"Dialogue: 0,{t(start)},{t(end)},Cap,,0,0,0,,{pop}{text}")
    open(ass, "w").write(head + "\n".join(events) + "\n")


def main(src, srt, out, y=0.74, size=0.075):
    w, h = probe(src)
    tmp = tempfile.mkdtemp()
    ass = os.path.join(tmp, "captions.ass")
    srt_to_ass(srt, ass, w, h, y, size)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vf", f"ass={ass}",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    print(f"{out}: captions burned at {y:.0%} height")


if __name__ == "__main__":
    argv = sys.argv[1:]
    opts = {"--y": 0.74, "--size": 0.075}
    for k in list(opts):
        if k in argv:
            i = argv.index(k)
            opts[k] = float(argv[i + 1])
            del argv[i:i + 2]
    if len(argv) != 3:
        sys.exit(__doc__)
    main(*argv, y=opts["--y"], size=opts["--size"])
