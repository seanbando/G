"""Make a sound-effect track that lines up with a narration track.

Usage:
    python3 tools/build_sfx.py <cues.txt> <narration.mp3> <out_dir> [--force]

Cue lines: "time name loudness seconds prompt  # note". A name used again
reuses the first sound, so later lines only need time and name. Each new
sound is generated once with ElevenLabs (skipped if the file exists, unless
--force), levelled to its loudness in LUFS, and placed at its time.

Writes to <out_dir>:
    <name>.mp3          one file per sound
    sfx-track.mp3       effects only, same length as the narration; drop it
                        on the timeline at 0:00 under the video
    preview-mix.mp3     narration plus effects, for listening
The ElevenLabs SDK reads ELEVENLABS_API_KEY from the environment.
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from build_track import duration, ff, loudness  # noqa: E402


def read_cues(path):
    cues, sounds = [], {}
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split(None, 4)
        time, name = float(parts[0]), parts[1]
        if len(parts) == 5 and name not in sounds:
            sounds[name] = dict(lufs=float(parts[2]), seconds=float(parts[3]), prompt=parts[4])
        if name not in sounds:
            sys.exit(f"{name} at {time}s has no loudness, length or prompt")
        cues.append((time, name))
    return cues, sounds


def generate(sounds, out_dir, force):
    from elevenlabs.client import ElevenLabs
    client = ElevenLabs()
    for name, s in sounds.items():
        path = os.path.join(out_dir, f"{name}.mp3")
        if os.path.exists(path) and not force:
            print(f"skip  {name}.mp3 (exists)")
            continue
        audio = client.text_to_sound_effects.convert(
            text=s["prompt"], duration_seconds=s["seconds"], prompt_influence=0.6)
        with open(path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"wrote {name}.mp3 ({s['seconds']} s): {s['prompt']}")


def main(cue_file, narration, out_dir, force=False):
    cues, sounds = read_cues(cue_file)
    os.makedirs(out_dir, exist_ok=True)
    generate(sounds, out_dir, force)

    tmp = tempfile.mkdtemp()
    levelled = {}
    for name, s in sounds.items():
        wav = os.path.join(tmp, name + ".wav")
        ff("-i", os.path.join(out_dir, f"{name}.mp3"), "-ac", "2", "-ar", "44100", wav)
        gain = s["lufs"] - loudness(wav)
        out = os.path.join(tmp, name + "_lev.wav")
        ff("-i", wav, "-af", f"volume={gain:.2f}dB", "-ac", "2", "-ar", "44100", out)
        levelled[name] = out

    total = duration(narration)
    inputs, chains = [], []
    for i, (time, name) in enumerate(cues):
        inputs += ["-i", levelled[name]]
        ms = int(round(time * 1000))
        chains.append(f"[{i}]adelay={ms}|{ms}[c{i}]")
    mix = "".join(f"[c{i}]" for i in range(len(cues)))
    graph = ";".join(chains) + f";{mix}amix=inputs={len(cues)}:normalize=0,apad,atrim=0:{total:.3f}," \
        "alimiter=limit=0.89:level=false[out]"
    sfx = os.path.join(out_dir, "sfx-track.mp3")
    ff(*inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", sfx)

    preview = os.path.join(out_dir, "preview-mix.mp3")
    ff("-i", narration, "-i", sfx, "-filter_complex",
       "[0]aformat=channel_layouts=stereo[v];[v][1]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false[out]",
       "-map", "[out]", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", preview)
    print(f"{sfx}: {duration(sfx):.1f} s, {len(cues)} cues, {len(sounds)} sounds")
    print(f"{preview}: {duration(preview):.1f} s")


if __name__ == "__main__":
    argv = [a for a in sys.argv[1:] if a != "--force"]
    if len(argv) != 3:
        sys.exit(__doc__)
    main(*argv, force="--force" in sys.argv)
