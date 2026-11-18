"""Generate Saylo sound effects and music beds with ElevenLabs.

Usage:
    python3 saylo/tools/generate_sound.py sfx   <out_dir>            # the SFX kit below
    python3 saylo/tools/generate_sound.py music <out_dir> A [B C D]  # music beds
Existing files are skipped. Auth comes from the environment proxy (dummy key).
"""
import json
import os
import subprocess
import sys

SFX = {  # name: (prompt, seconds)
    "typewriter-keys-short": ("Old manual typewriter, 6 quick key strikes, close mic, dry, no bell", 1.2),
    "typewriter-keys-medium": ("Old manual typewriter typing a short line, steady key strikes, close mic, dry, no bell", 2.2),
    "typewriter-keys-long": ("Old manual typewriter typing a full line, steady rhythmic key strikes, close mic, dry, no bell", 3.6),
    "typewriter-ding": ("Manual typewriter carriage return bell ding and lever slide, single", 1.2),
    "flashlight-click": ("Single metal flashlight switch click, close, quiet room", 0.6),
    "gravel-footsteps": ("Quick running footsteps on gravel at night that stop suddenly", 2.5),
    "car-idle-gravel": ("Police car rolling slowly over gravel with engine idling at night, no siren", 4.0),
    "paper-slide": ("A sheet of paper sliding across a wooden desk", 1.0),
    "helicopter-distant": ("Distant helicopter passing over a forested valley, fading in and out", 6.0),
    "riser": ("Dark cinematic tension riser building for 3 seconds, ends abruptly, no hit", 3.0),
    "boom-hit": ("Deep cinematic sub boom impact hit with short tail, documentary trailer", 2.5),
    "low-hit": ("Soft low cinematic thud hit, short, subtle", 1.5),
    "crowd-concert": ("Large outdoor night concert crowd ambience from a distance, band muffled far away", 8.0),
    "payphone-pickup": ("Old payphone handset lifted off the hook, metal cord rattle, dial tone starts", 2.0),
    "clock-tick": ("Single loud mechanical clock tick, dry", 0.5),
    "clock-ticking": ("Steady mechanical clock ticking, one tick per second, dry, close", 8.0),
    "pen-tick": ("Pen making a quick check mark on paper", 0.6),
    "stamp-thud": ("Rubber stamp slammed onto paper on a desk, heavy thud", 0.8),
    "pen-scribble": ("Ballpoint pen scribbling quickly on a small notepad", 2.0),
    "wind-gust": ("Cold wind gust through bare winter trees in the mountains", 3.0),
    "dogs-distant": ("Search dogs barking in the distance in a forest, echoing", 5.0),
    "night-forest": ("Night forest ambience with crickets and light wind, Appalachian mountains", 10.0),
    "camera-shutter": ("Single mechanical camera shutter click with flash charge whine", 1.0),
    "shovel-dirt": ("Shovel digging into wet forest dirt, two scoops", 2.5),
    "cell-door": ("Heavy steel prison cell door slamming shut with echo", 2.5),
    "whoosh": ("Soft quick cinematic whoosh transition, subtle, airy", 0.8),
}

MUSIC = {  # bed: (prompt, seconds)
    "A": ("Dark true-crime documentary underscore. Low synth drone with a slow heartbeat-like pulse at 70 bpm, sparse, tense, minor key, no melody, no vocals, no drums kit. Suitable to loop under narration.", 150),
    "B": ("Investigative documentary underscore at 90 bpm. Steady clock-like ticking rhythm, muted plucked strings, restrained low synth pads, curious and tense, no vocals, no big drums. Sits under narration.", 150),
    "C": ("Somber, respectful underscore. Sparse slow piano with soft sustained strings, minor key, quiet and emotional, no drums, no vocals. Sits under narration.", 120),
    "D": ("Lonely Appalachian night ambience score. Wind texture, low sustained cello drone, distant sparse notes, cold and isolated, no drums, no vocals. Sits under narration.", 150),
}


def post(url, body, out):
    r = subprocess.run(["curl", "-sS", "-o", out, "-w", "%{http_code}", "-X", "POST", url,
                        "-H", "xi-api-key: dummy", "-H", "Content-Type: application/json",
                        "-d", json.dumps(body)], capture_output=True, text=True)
    if r.stdout != "200":
        err = open(out, errors="ignore").read()[:300] if os.path.exists(out) else r.stderr
        if os.path.exists(out):
            os.remove(out)
        return f"FAILED {r.stdout} {err}"
    return "ok"


def main(argv):
    kind, out = argv[0], argv[1]
    os.makedirs(out, exist_ok=True)
    if kind == "sfx":
        for name, (prompt, secs) in SFX.items():
            path = os.path.join(out, f"sfx-{name}.mp3")
            if os.path.exists(path):
                continue
            print(name, post("https://api.elevenlabs.io/v1/sound-generation",
                             {"text": prompt, "duration_seconds": secs, "prompt_influence": 0.5}, path), flush=True)
    else:
        for bed in argv[2:]:
            prompt, secs = MUSIC[bed]
            path = os.path.join(out, f"bed-{bed}.mp3")
            if os.path.exists(path):
                continue
            print("bed", bed, post("https://api.elevenlabs.io/v1/music",
                                   {"prompt": prompt, "music_length_ms": secs * 1000, "force_instrumental": True}, path), flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
