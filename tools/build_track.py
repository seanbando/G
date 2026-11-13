"""Join per-line voice-over files into one narration track (e.g. for Golpo).

Usage: python3 tools/build_track.py <script.md> <clips_dir> <output.mp3>

Order and pauses come from the script, so the track always matches it:
- silence at the start and end of each clip is trimmed, and long pauses
  inside a clip are capped at about 0.45 s
- 0.12 s between pieces of one line (VO-13a, VO-13b), 0.3 s between lines
  from the same voice, 0.4 s when the speaker changes
- each [PAUSE: N seconds ...] in the script becomes N seconds of silence
- every clip is levelled to the same loudness, and the finished track is
  brought to YouTube's loudness (-14 LUFS, peaks under -1 dB)
- clips listed in TEMPO are gently slowed (pitch unchanged) when the voice
  model rushed them
Trimmed copies of every clip are written to <clips_dir>/trimmed/.

Add --keep-pace to skip the automatic speed-ups, for scripts whose slow
lines are slow on purpose (set with generate_voiceovers.py --speeds).
Add --tight for Shorts: pauses and quiet breaths inside a line are capped at about 0.2 s,
lines are 0.1 s apart (0.15 s when the speaker changes) and every
[PAUSE: ...] is cut to 60% of its length.
Add --punch for the creator-approved "B" sound: the whole track 15% faster
(pitch unchanged), presence EQ and two-stage compression so the voice sits
dense and upfront, levelled to -14 LUFS. Use --speed <factor> to change
the 1.15 default.
Add --tempo <sheet> to stretch chosen lines for this script only, with the
same "VO-08 1.18  # comment" format; it adds to TEMPO for this run.
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


CLIP_TARGET = -16.0   # LUFS every clip is set to
FINAL_TARGET = -14.0  # LUFS for the finished track (YouTube's level)
LIMIT = "alimiter=limit=0.89:level=false"  # keeps peaks under about -1 dB

# Lines the voice model read too fast, measured in words per minute against
# the narrator's usual ~185; the factor brings them back to ~190.
TEMPO = {}  # per-line overrides, e.g. {"VO-80": 0.9}; empty by the creator's choice

# Lines that drag are sped up automatically (pitch unchanged):
# narrator below 172 wpm -> toward 180; characters below 140 wpm -> toward 165.
AUTO_TEMPO = {"NARRATOR": (172, 180, 1.2), "OTHER": (140, 165, 1.3)}  # (below, target, max factor)
# Lines that are rushed are slowed the same way: above 215 wpm -> toward 195
# (210 for the deliberately faster opening, VO-01 to VO-06), never below 0.8x.
# Off by the creator's choice: fast, natural delivery is kept as recorded.
SLOW_DOWN_FAST_LINES = False
FAST_ABOVE, FAST_TARGET, FAST_HOOK_TARGET, FAST_MIN = 215, 195, 210, 0.8
HOOK = {f"VO-{n:02d}" for n in range(1, 7)}


def loudness(path):
    """Integrated loudness in LUFS, measured over the whole file."""
    err = subprocess.run(["ffmpeg", "-nostdin", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", path], capture_output=True, text=True).stdout)


def ff(*args):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args], check=True, stdin=subprocess.DEVNULL)


TIGHT_TRIM = (TRIM.replace("stop_duration=0.45", "stop_duration=0.25").replace("stop_silence=0.4", "stop_silence=0.2")
              .replace("stop_threshold=-45dB", "stop_threshold=-38dB"))  # also catches quiet breaths


PUNCH = ("highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=4,"
         "equalizer=f=9000:t=h:w=1:g=2,"
         "acompressor=threshold=-32dB:ratio=6:attack=3:release=50:makeup=8dB,"
         "acompressor=threshold=-18dB:ratio=3:attack=1:release=40:makeup=2dB")


def punch(path, speed):
    """Speed up the finished track and give it the dense, upfront approved sound."""
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "punch.wav")
    ff("-i", path, "-af", f"atempo={speed},{PUNCH}", "-ar", "44100", wav)
    gain = FINAL_TARGET - loudness(wav)
    ff("-i", wav, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false",
       "-c:a", "libmp3lame", "-b:a", "192k", path)


def main(script, clips, out, keep_pace=False, tight=False, speed=None):
    trim = TIGHT_TRIM if tight else TRIM
    same_gap, change_gap, pause_scale = (0.1, 0.15, 0.6) if tight else (0.3, 0.4, 1.0)
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

    parts, prev_voice, missing, sped = [], None, [], []
    for line_id, voice, text, cues in lines:
        files = sorted(glob.glob(os.path.join(clips, f"{line_id}[a-z]_*.mp3"))) or \
            sorted(glob.glob(os.path.join(clips, f"{line_id}_*.mp3")))
        if not files:
            missing.append(line_id)
            continue
        pause = sum(float(m) for c in cues if c.startswith("⏸")
                    for m in re.findall(r"([\d.]+)\s*second", c))
        if parts:
            parts.append(silence(same_gap if voice == prev_voice else change_gap))
        if pause:
            parts.append(silence(round(pause * pause_scale, 2)))
        for k, f in enumerate(files):
            name = os.path.splitext(os.path.basename(f))[0]
            wav = os.path.join(tmp, name + ".wav")
            line = name.split("_")[0]
            chain = trim + (f",atempo={TEMPO[line]}" if line in TEMPO else "")
            raw = os.path.join(tmp, name + "_raw.wav")
            # Trim first, then measure and apply an exact gain. (Running loudnorm in
            # the same chain as silenceremove can hang ffmpeg, and its automatic
            # mode is unreliable on very short clips.)
            ff("-i", f, "-af", chain, "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", raw)
            speedup = ""
            if line not in TEMPO and len(files) == 1 and not keep_pace:
                below, target, cap = AUTO_TEMPO["NARRATOR" if voice == "NARRATOR" else "OTHER"]
                wpm = len(text.split()) / duration(raw) * 60
                factor = None
                if wpm < below:
                    factor = min(target / wpm, cap)
                elif SLOW_DOWN_FAST_LINES and wpm > FAST_ABOVE:
                    goal = FAST_HOOK_TARGET if line_id in HOOK else FAST_TARGET
                    factor = max(goal / wpm, FAST_MIN)
                if factor:
                    speedup = f"atempo={factor:.3f},"
                    sped.append(f"{line_id} {wpm:.0f}->{wpm * factor:.0f} wpm")
            gain = CLIP_TARGET - loudness(raw)
            ff("-i", raw, "-af", f"{speedup}volume={gain:.2f}dB,{LIMIT}", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", wav)
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
    joined = os.path.join(tmp, "joined.wav")
    ff("-f", "concat", "-safe", "0", "-i", listing, "-c:a", "pcm_s16le", joined)
    gain = FINAL_TARGET - loudness(joined)
    ff("-i", joined, "-af", f"volume={gain:.2f}dB,{LIMIT}", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "128k", out)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    size = os.path.getsize(out) / 1e6
    print(f"{out}: {int(dur // 60)}m {dur % 60:.0f}s, {size:.1f} MB")
    if speed:
        punch(out, speed)
        print(f"punch: {speed}x faster, compressed, -14 LUFS: {duration(out):.1f} s")
    if sped:
        print(f"adjusted the pace of {len(sped)} lines: " + ", ".join(sped))


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--tempo" in argv:
        i = argv.index("--tempo")
        from generate_voiceovers import load_speeds
        TEMPO.update(load_speeds(argv[i + 1]))
        del argv[i:i + 2]
    speed = None
    if "--speed" in argv:
        i = argv.index("--speed")
        speed = float(argv[i + 1])
        del argv[i:i + 2]
    if "--punch" in argv:
        speed = speed or 1.15
    args = [a for a in argv if a not in ("--keep-pace", "--tight", "--punch")]
    main(*args[:3], keep_pace="--keep-pace" in argv, tight="--tight" in argv, speed=speed)
