"""Mix the master audio: voiceover + music + sound effects.

Usage: python3 video/01-follow-one-dollar/motion/mix_audio.py [--music-db -31] [--sfx-db 0]

- Voice: audio/follow-one-dollar-v6/narration.mp3, untouched and always on top.
- Music: audio/music/hook.mp3 under the hook, then audio/music/bed.mp3 looped with crossfades
  to the end. Kept far below the voice so every word stays clear.
- Sound effects: one per motion event (final/events.json from dump_events.js): pop, whoosh,
  stamp, pen stroke, chime for plain-words cards, ticking under the quiz pause, a ding on
  the quiz answer. Rapid runs of the same sound are thinned out, and pops vary a little
  in pitch so they don't sound like a machine.
Writes final/master-audio.wav at YouTube loudness (-14 LUFS).
"""
import argparse
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
FINAL = os.path.join(HERE, "..", "final")
SR = 44100


def load(path, ch=2):
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(pcm, dtype=np.float32).reshape(-1, ch).copy()


def lufs(x):
    p = os.path.join(FINAL, "_m.f32")
    x.astype(np.float32).tofile(p)
    out = subprocess.run(["ffmpeg", "-nostdin", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", p, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    os.remove(p)
    return float(out.split("Integrated loudness:")[-1].split("I:")[1].split("LUFS")[0])


def trim_start(x, db=-40):
    """Cut silence before the sound so it lands exactly on its event."""
    env = np.abs(x).max(axis=1)
    idx = np.argmax(env > env.max() * 10 ** (db / 20))
    return x[max(0, idx - int(0.003 * SR)):]


def repitch(x, ratio):
    n = int(len(x) / ratio)
    src = np.arange(n) * ratio
    return np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in range(x.shape[1])], axis=1).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--music-db", type=float, default=-31.0, help="music loudness in LUFS (voice is -14)")
    ap.add_argument("--hook-music-db", type=float, default=-28.0)
    ap.add_argument("--sfx-db", type=float, default=0.0, help="raise or lower all sound effects together")
    a = ap.parse_args()
    E = json.load(open(os.path.join(FINAL, "events.json")))
    voice = load(os.path.join(ROOT, "audio", "follow-one-dollar-v6", "narration.mp3"))
    n = len(voice)
    mix = np.zeros((n + SR, 2), dtype=np.float32)

    # ---- music ----
    hook_end = next(s["t0"] for s in E["sections"] if s["name"] == "pizza")
    hook = load(os.path.join(ROOT, "audio", "music", "hook.mp3"))
    bed = load(os.path.join(ROOT, "audio", "music", "bed.mp3"))
    hook *= 10 ** ((a.hook_music_db - lufs(hook)) / 20)
    bed *= 10 ** ((a.music_db - lufs(bed)) / 20)
    xf = int(2.0 * SR)
    music = np.zeros_like(mix)
    h_len = min(len(hook), int((hook_end + 1.0) * SR))
    h = hook[:h_len].copy()
    h[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))[:, None]
    h[-xf:] *= np.linspace(1, 0, xf)[:, None]
    music[:h_len] += h
    pos = h_len - xf  # the bed fades in as the hook music fades out
    while pos < n:
        seg = bed[:min(len(bed), n + SR - pos)].copy()
        seg[:xf] *= np.linspace(0, 1, xf)[:, None]
        if len(seg) == len(bed):
            seg[-xf:] *= np.linspace(1, 0, xf)[:, None]
        music[pos:pos + len(seg)] += seg
        pos += len(bed) - xf
    fade = int(3.0 * SR)
    music[n - fade:n] *= np.linspace(1, 0, fade)[:, None]
    music[n:] = 0
    mix += music

    # ---- sound effects ----
    S = {k: trim_start(load(os.path.join(ROOT, "audio", "sfx", k + ".mp3"))) for k in ["pop", "whoosh", "stamp", "pencil", "chime", "tick", "ding"]}
    for k in S:
        S[k] /= max(1e-6, np.abs(S[k]).max())   # peak 1.0, then set by PEAK below
    PEAK = {"pop": -23, "whoosh": -25, "stamp": -19, "pencil": -27, "chime": -22, "tick": -25, "ding": -19}   # dBFS; the voice peaks near -1
    MAP = {"pop": "pop", "slide": "whoosh", "stamp": "stamp", "wipe": "pencil", "term": "chime", "drain": "tick", "scalefrom": "whoosh", "move": "whoosh"}
    GAP = {"pop": 0.16, "whoosh": 0.3, "stamp": 0.25, "pencil": 0.5, "chime": 1.0, "tick": 3.0, "ding": 1.0}
    last, used, k_pop = {}, {}, 0
    for e in E["events"]:
        kind = MAP.get(e["fx"])
        if kind == "pencil" and e.get("dur", 0) and e["dur"] < 0.45:
            continue                       # short arrow wipes stay silent
        if e["fx"] == "stamp" and e["line"] == "S073":
            kind = "ding"                  # the quiz answer
        if not kind or e["t"] - last.get(kind, -9) < GAP[kind]:
            continue
        last[kind] = e["t"]
        x = S[kind]
        if kind == "pop":
            k_pop += 1
            x = repitch(x, [1.0, 1.06, 0.95, 1.03, 0.98][k_pop % 5])
        if kind == "pencil":
            L = int(min(len(x), max(0.5, min(e.get("dur") or 0.8, 1.0)) * SR))
            x = x[:L].copy(); x[-int(0.08 * SR):] *= np.linspace(1, 0, int(0.08 * SR))[:, None]
        g = 10 ** ((PEAK[kind] + a.sfx_db) / 20)
        i = int(e["t"] * SR)
        if i >= n:
            continue
        mix[i:i + len(x)] += x[:len(mix) - i] * g
        used[kind] = used.get(kind, 0) + 1

    mix[:n] += voice
    mix = mix[:n]
    peak = np.abs(mix).max()
    if peak > 0.97:
        mix *= 0.97 / peak
    mix *= 10 ** ((-14.0 - lufs(mix)) / 20)
    mix = np.clip(mix, -0.98, 0.98)
    out = os.path.join(FINAL, "master-audio.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", out], input=mix.astype(np.float32).tobytes(), check=True)
    print("sounds used:", used, "| music", a.music_db, "LUFS (hook", a.hook_music_db, ") | master", round(lufs(mix), 1), "LUFS | wrote", out)


if __name__ == "__main__":
    main()
