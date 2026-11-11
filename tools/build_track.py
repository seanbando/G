"""Join per-line voice-over files into one narration track (e.g. for Golpo).

Usage: python3 tools/build_track.py <script.md> <clips_dir> <output.mp3>

Order and pauses come from the script, so the track always matches it:
- silence at the start and end of each clip is trimmed, and long pauses
  inside a clip are capped at about 0.45 s
- 0.12 s between pieces of one line (VO-13a, VO-13b), 0.3 s between lines
  from the same voice, 0.4 s when the speaker changes
- each [PAUSE: N seconds ...] in the script becomes N seconds of silence
Trimmed copies of every clip are written to <clips_dir>/trimmed/.
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from make_voiceover import parse  # noqa: E402

TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,"
        "areverse,silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-45dB:stop_silence=0.4")


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def main(script, clips, out):
    _, lines = parse(script)
    tmp = tempfile.mkdtemp()
    os.makedirs(os.path.join(clips, "trimmed"), exist_ok=True)
    silences = {}

    def silence(sec):
        if sec not in silences:
            path = os.path.join(tmp, f"silence_{sec}.wav")
            ff("-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(sec), "-c:a", "pcm_s16le", path)
            silences[sec] = path
        return silences[sec]

    parts, prev_voice, missing = [], None, []
    for line_id, voice, _, cues in lines:
        files = sorted(glob.glob(os.path.join(clips, f"{line_id}[a-z]_*.mp3"))) or \
            sorted(glob.glob(os.path.join(clips, f"{line_id}_*.mp3")))
        if not files:
            missing.append(line_id)
            continue
        pause = sum(float(m) for c in cues if c.startswith("⏸")
                    for m in re.findall(r"([\d.]+)\s*second", c))
        if parts:
            parts.append(silence(0.3 if voice == prev_voice else 0.4))
        if pause:
            parts.append(silence(pause))
        for k, f in enumerate(files):
            name = os.path.splitext(os.path.basename(f))[0]
            wav = os.path.join(tmp, name + ".wav")
            ff("-i", f, "-af", TRIM, "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", wav)
            ff("-i", wav, "-c:a", "libmp3lame", "-b:a", "128k", os.path.join(clips, "trimmed", name + ".mp3"))
            if k:
                parts.append(silence(0.12))
            parts.append(wav)
        prev_voice = voice

    if missing:
        sys.exit(f"Missing audio for: {', '.join(missing)}")
    listing = os.path.join(tmp, "list.txt")
    with open(listing, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    ff("-f", "concat", "-safe", "0", "-i", listing, "-c:a", "libmp3lame", "-b:a", "128k", out)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    size = os.path.getsize(out) / 1e6
    print(f"{out}: {int(dur // 60)}m {dur % 60:.0f}s, {size:.1f} MB")


if __name__ == "__main__":
    main(*sys.argv[1:4])
