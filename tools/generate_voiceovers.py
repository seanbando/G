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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out_dir")
    ap.add_argument("--only", help="comma-separated line IDs, e.g. VO-01,VO-06")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
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
        # Neighbouring lines from the same voice keep intonation consistent.
        prev_text = lines[i - 1][2] if i > 0 and lines[i - 1][1] == voice else None
        next_text = lines[i + 1][2] if i + 1 < len(lines) and lines[i + 1][1] == voice else None
        audio = client.text_to_speech.convert(
            voice_id=VOICES[voice],
            text=text,
            model_id=MODEL,
            output_format=FORMAT,
            previous_text=prev_text,
            next_text=next_text,
        )
        with open(path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"wrote {name} ({os.path.getsize(path) // 1024} KB, {len(text)} chars)")


if __name__ == "__main__":
    main()
