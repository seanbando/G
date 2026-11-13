"""Write a tempo sheet that brings every voice-over line to one target pace.

Usage:
    python3 tools/auto_tempo.py <script.md> <clips_dir> <target_wpm> > tempo.txt

Each clip is trimmed of leading and trailing silence the same way
build_track.py trims it, its words per minute is measured, and a
pitch-safe tempo factor is written so the line plays at <target_wpm>.
Lines are only ever sped up, never slowed down (factor 1.0 to 1.35): slowing
a recorded line down makes it sound draggy and stretched (the creator heard
this on the paycheck short), so a line read faster than the target keeps
its natural pace.
Pass the sheet to build_track.py with --tempo (and use --punch --speed 1.0
for the punchy sound without a further blanket speed-up).
"""
import glob
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from build_track import TRIM, duration, ff  # noqa: E402
from make_voiceover import parse  # noqa: E402

LOW, HIGH = 1.0, 1.35


def main(script, clips, target):
    target = float(target)
    tmp = tempfile.mkdtemp()
    print(f"# Auto tempo: every line brought to about {target:.0f} words a minute.")
    for line_id, voice, text, _ in parse(script)[1]:
        files = sorted(glob.glob(os.path.join(clips, f"{line_id}_*.mp3")))
        if not files:
            continue
        wav = os.path.join(tmp, line_id + ".wav")
        ff("-i", files[0], "-af", TRIM, wav)
        wpm = len(text.split()) / duration(wav) * 60
        factor = min(max(target / wpm, LOW), HIGH)
        print(f"{line_id} {factor:.3f}  # {voice}: {wpm:.0f} wpm as recorded")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
