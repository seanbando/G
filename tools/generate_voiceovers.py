"""Generate one ElevenLabs audio file per voice-over line.

Usage:
    python3 tools/generate_voiceovers.py <script.md> <output_dir> [--only VO-01,VO-02] [--force]
        [--speeds speeds.txt]

--speeds reads a per-line speed sheet ("VO-06 0.85  # comment" per line) and
replaces the default speeds below, so each short can set its own pacing.

Reads the script with the same parser as make_voiceover.py, so file names
(VO-01_NARRATOR.mp3, ...) match the voice-over sheet. Existing files are
skipped unless --force is given. The ElevenLabs SDK reads ELEVENLABS_API_KEY
from the environment.
"""
import argparse
import os
import re
import string
import sys

from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings

sys.path.insert(0, os.path.dirname(__file__))
from make_voiceover import parse  # noqa: E402

VOICES = {
    "NARRATOR": "eAE1ARfBOYNmMW3Ma9aS",      # Yaboy (creator's cloned voice)
    "YOU": "cjVigY5qzO86Huf0OWal",           # Eric - Smooth, Trustworthy
    "THE APP": "iCVkdoGNYLTCRiLXC3Iu",       # Wayne - Robotic and Clear
    "THE EXCHANGE": "L1xUIshtTbSBoOSqBFaP",  # Andrew - Crisp Announcer
    # Newer characters (confirmed by the creator):
    "THE MARKET MAKER": "CwhRBWXzGAHq8TQ4Fs17",   # Roger - Laid-Back, Casual, Resonant
    "THE SELLER": "FGY2WhTYpPnrIDTdsKH5",         # Laura - Enthusiast, Quirky Attitude
    "THE CLEARINGHOUSE": "pqHfZKP75CvOlQylNhV4",  # Bill - Wise, Mature, Balanced
    "MAYA": "cgSgspJ2msm6clMCkdW9",               # Jessica - Playful, Bright, Warm
    "JORDAN": "bIHbv24MWmeRgasZH58o",             # Will - Relaxed Optimist
}
MODEL = "eleven_v4"  # narrator style D, chosen by the creator
FORMAT = "mp3_44100_128"

# Delivery: lower stability = more natural variation; a little style = more expressive.
SETTINGS = dict(stability=0.4, similarity_boost=0.8, style=0.2, use_speaker_boost=True)
DEFAULT_SPEED = 1.0
# Faster read for the hook (roughly the first 30 seconds).
SPEED = {f"VO-{n:02d}": 1.12 for n in range(1, 7)}  # VO-01 to VO-06

# --split: long lines are cut into pieces of a few sentences (VO-13a, VO-13b, ...).
SPLIT_TARGET = 220  # aim for pieces of about this many characters
SPLIT_MIN = 120     # a line shorter than this is never split


def sentences(text):
    """Split into sentences without breaking on abbreviations like 'U.S.'."""
    parts, start = [], 0
    for m in re.finditer(r"[.?!]['\"]?\s+(?=[A-Z\"'])", text):
        before = text[start:m.end()].rstrip()
        if re.search(r"\b(?:[A-Z]\.){2,}$", before):  # U.S. followed by a capital
            continue
        parts.append(before)
        start = m.end()
    parts.append(text[start:].strip())
    return [p for p in parts if p]


def split_line(text):
    if len(text) < SPLIT_MIN:
        return [text]
    pieces, cur = [], ""
    for sent in sentences(text):
        if cur and len(cur) + 1 + len(sent) > SPLIT_TARGET:
            pieces.append(cur)
            cur = sent
        else:
            cur = f"{cur} {sent}".strip()
    if cur:
        # Fold a very short tail into the previous piece.
        if pieces and len(cur) < 60:
            pieces[-1] += " " + cur
        else:
            pieces.append(cur)
    return pieces


def load_speeds(path):
    """Read 'VO-06 0.85  # comment' lines into {line_id: speed}."""
    speeds = {}
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if line:
            line_id, value = line.split()
            speeds[line_id] = float(value)
    return speeds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out_dir")
    ap.add_argument("--only", help="comma-separated line IDs, e.g. VO-01,VO-06")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--model", default=MODEL, help="ElevenLabs model ID")
    ap.add_argument("--split", action="store_true", help="cut long lines into smaller pieces")
    ap.add_argument("--speeds", help="per-line speed sheet; replaces the default speeds")
    args = ap.parse_args()
    speed_map = load_speeds(args.speeds) if args.speeds else SPEED

    _, lines = parse(args.script)
    only = set(args.only.split(",")) if args.only else None
    os.makedirs(args.out_dir, exist_ok=True)
    client = ElevenLabs()  # reads ELEVENLABS_API_KEY

    # Expand lines into (file_id, line_id, voice, text) units.
    units = []
    for line_id, voice, text, _ in lines:
        pieces = split_line(text) if args.split else [text]
        for k, piece in enumerate(pieces):
            suffix = string.ascii_lowercase[k] if len(pieces) > 1 else ""
            units.append((line_id + suffix, line_id, voice, piece))

    for i, (file_id, line_id, voice, text) in enumerate(units):
        if only and line_id not in only and file_id not in only:
            continue
        name = f"{file_id}_{voice.replace(' ', '_')}.mp3"
        path = os.path.join(args.out_dir, name)
        if os.path.exists(path) and not args.force:
            print(f"skip  {name} (exists)")
            continue
        # Surrounding text gives the model context, so delivery flows between files.
        prev_text = units[i - 1][3] if i > 0 else None
        next_text = units[i + 1][3] if i + 1 < len(units) else None
        speed = speed_map.get(line_id, DEFAULT_SPEED)
        audio = client.text_to_speech.convert(
            voice_id=VOICES[voice],
            text=text,
            model_id=args.model,
            output_format=FORMAT,
            voice_settings=VoiceSettings(speed=speed, **SETTINGS),
            previous_text=prev_text,
            next_text=next_text,
        )
        with open(path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"wrote {name} ({os.path.getsize(path) // 1024} KB, {len(text)} chars, speed {speed})")

if __name__ == "__main__":
    main()
