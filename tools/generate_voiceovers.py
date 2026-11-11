"""Generate one ElevenLabs audio file per voice-over line.

Usage:
    python3 tools/generate_voiceovers.py <script.md> <output_dir> [--only VO-01,VO-02] [--force]

Reads the script with the same parser as make_voiceover.py, so file names
(VO-01_NARRATOR.mp3, ...) match the voice-over sheet. Existing files are
skipped unless --force is given. The ElevenLabs SDK reads ELEVENLABS_API_KEY
from the environment.
"""
import argparse
import os
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
}
MODEL = "eleven_multilingual_v2"
FORMAT = "mp3_44100_128"

# Delivery: lower stability = more natural variation; a little style = more expressive.
SETTINGS = dict(stability=0.35, similarity_boost=0.8, style=0.25, use_speaker_boost=True)
DEFAULT_SPEED = 1.0
# Faster read for the hook (roughly the first 30 seconds).
SPEED = {"VO-01": 1.12, "VO-02": 1.12, "VO-03": 1.12}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out_dir")
    ap.add_argument("--only", help="comma-separated line IDs, e.g. VO-01,VO-06")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--model", default=MODEL, help="ElevenLabs model ID")
    args = ap.parse_args()

    _, lines = parse(args.script)
    only = set(args.only.split(",")) if args.only else None
    os.makedirs(args.out_dir, exist_ok=True)
    client = ElevenLabs()  # reads ELEVENLABS_API_KEY

    for i, (line_id, voice, text, _) in enumerate(lines):
        if only and line_id not in only:
            continue
        name = f"{line_id}_{voice.replace(' ', '_')}.mp3"
        path = os.path.join(args.out_dir, name)
        if os.path.exists(path) and not args.force:
            print(f"skip  {name} (exists)")
            continue
        # Surrounding lines give the model context, so delivery flows between files.
        prev_text = lines[i - 1][2] if i > 0 else None
        next_text = lines[i + 1][2] if i + 1 < len(lines) else None
        speed = SPEED.get(line_id, DEFAULT_SPEED)
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
