"""Build a section of the video from its shot plans (build/plan_*.py).

    python saylo/videos/01-olympic-bomber/build/build_part1.py                       -> render/part1.mp4 (cold open + The Park)
    python saylo/videos/01-olympic-bomber/build/build_part1.py <name> <plan.py> [...] -> render/<name>.mp4

Plans are written on the voiceover's clock (vo-words.json). A plan may also list news BITES: moments where the
narration pauses and a real clip plays with its own sound, e.g.
    BITES = [dict(at=194.54, src="bite ap witness smoke.mp4", dur=4.6)]
`at` must be a cut point (between two narration lines). Bites from ALL plans are applied to every build, so every
shot, music bed, SFX and cue after a bite moves later by its length, and the voiceover gets the bite's audio in the
gap (so the music ducks under it too).

Source files are read from ../media (the creator's clips, not in git). A missing file becomes a typed "MISSING" card.
Needs SAYLO_EFFECTS for the Template Library effects (defaults to the kit unpacked in <repo>/_kit).
"""
import glob, hashlib, json, os, runpy, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(VID, "..", "..", ".."))
TOOLS = os.path.join(REPO, "saylo", "tools")
MEDIA = os.path.join(VID, "media")
OUT = os.path.join(VID, "render")
VO = os.path.join(VID, "voiceover-full.mp3")
os.environ.setdefault("SAYLO_EFFECTS", os.path.join(REPO, "_kit", "Faceless Studio", ".claude", "effects"))

NAME = sys.argv[1] if len(sys.argv) > 2 else "part1"
PLANS = sys.argv[2:] if len(sys.argv) > 2 else ["plan_cold_open.py", "plan_park.py"]

# ---- bites from every plan (they shift the whole timeline)
BITES = []
for f in sorted(glob.glob(os.path.join(HERE, "plan_*.py"))):
    BITES += runpy.run_path(f).get("BITES", [])
BITES.sort(key=lambda b: b["at"])

def shift(t, include_at=True):
    """VO-clock time -> output time. A shot starting exactly at a bite goes after it (include_at)."""
    return t + sum(b["dur"] for b in BITES if (b["at"] <= t if include_at else b["at"] < t))

segs, music, sfx, cues, silence = [], [], [], [], []
for name in PLANS:
    p = runpy.run_path(os.path.join(HERE, name))
    for s in p["S"]:
        for b in BITES:
            assert not (s["start"] < b["at"] < s["end"]), f"bite at {b['at']} falls inside shot {s['start']}-{s['end']}"
        s["start"], s["end"] = round(shift(s["start"]), 3), round(shift(s["end"], include_at=False), 3)
        segs.append(s)
    for b in p.get("BITES", []):
        a = round(shift(b["at"], include_at=False), 3)
        segs.append(dict(start=a, end=round(a + b["dur"], 3), src=b["src"], **{"in": b.get("in", 0.0)}))
    for m in p["MUSIC"]:
        music.append(dict(m, start=round(shift(m["start"]), 3), end=round(shift(m["end"], include_at=False), 3)))
    sfx += [dict(at=round(shift(a), 3), file=f, gain=g) for a, f, g in p["SFX"]]
    silence += [[round(shift(x), 3), round(shift(y, include_at=False), 3)] for x, y in p.get("SILENCE", [])]  # music fully out
    cues += [f"{shift(float(l.split()[0])):.2f} " + " ".join(l.split()[1:]) for l in p.get("CUES", "").splitlines() if l.strip()]
segs.sort(key=lambda s: s["start"])

missing = []
def have(f):
    ok = os.path.exists(os.path.join(MEDIA, f))
    if not ok and f not in missing:
        missing.append(f)
    return ok

for s in segs:
    need = [s[k] for k in ("src", "bg") if s.get(k)]
    ov = s.get("ov", {})
    need += ov.get("images", []) + ([ov["backgroundImage"]] if ov.get("backgroundImage") else [])
    gone = [f for f in need if not have(f)]
    if gone:
        label = os.path.splitext(gone[0])[0].upper()
        for k in ("src", "effect", "ov", "tag", "in", "crop", "motion", "fx", "bg"):
            s.pop(k, None)
        s["card"] = [["MISSING CLIP", "amber"], [label[:40], "small"]]

os.makedirs(OUT, exist_ok=True)

# ---- voiceover with the bites' own audio in the gaps (cached by the bite list)
vo = VO
if BITES:
    sig = hashlib.sha1(json.dumps(BITES, sort_keys=True).encode()).hexdigest()[:10]
    vo = os.path.join(OUT, f"_vo_bites_{sig}.wav")
    if not os.path.exists(vo):
        ins, parts, prev = ["-i", VO], [], 0.0
        for k, b in enumerate(BITES, start=1):
            ins += ["-i", os.path.join(MEDIA, b["src"])]
            parts.append(f"[0:a]atrim={prev:.3f}:{b['at']:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[v{k}]")
            parts.append(f"[{k}:a]atrim=0:{b['dur']:.3f},asetpts=PTS-STARTPTS,volume={b.get('gain', 0)}dB,"
                         f"apad=whole_dur={b['dur']:.3f},afade=t=in:d=0.08,afade=t=out:st={b['dur'] - 0.15:.3f}:d=0.15,"
                         f"aformat=sample_rates=48000:channel_layouts=stereo[b{k}]")
            prev = b["at"]
        parts.append(f"[0:a]atrim=start={prev:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[vend]")
        order = "".join(f"[v{k}][b{k}]" for k in range(1, len(BITES) + 1)) + "[vend]"
        graph = ";".join(parts) + f";{order}concat=n={2 * len(BITES) + 1}:v=0:a=1[out]"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *ins, "-filter_complex", graph,
                        "-map", "[out]", "-ar", "48000", vo], check=True)

plan = dict(assets=MEDIA, voiceover=vo,
            music_dir=os.path.join(VID, "sound", "music"), sfx_dir=os.path.join(VID, "sound", "sfx"),
            segments=segs, music=music, sfx=sfx, silence=silence)
pj = os.path.join(OUT, NAME + ".plan.json")
json.dump(plan, open(pj, "w"), indent=1)
# cue times are on the full-video clock; the render starts at the first segment
T0 = min(s["start"] for s in segs)
cues = [f"{float(c.split()[0]) - T0:.2f} " + " ".join(c.split()[1:]) for c in cues]
open(os.path.join(OUT, NAME + ".cues.txt"), "w").write("\n".join(cues) + "\n")

raw = os.path.join(OUT, NAME + "_raw.mp4")
subprocess.run([sys.executable, os.path.join(TOOLS, "assemble.py"), pj, raw], check=True)
subprocess.run([sys.executable, os.path.join(TOOLS, "edit_video.py"), raw, os.path.join(OUT, NAME + ".cues.txt"),
                os.path.join(OUT, NAME + ".mp4")], check=True)
print("wrote", os.path.join(OUT, NAME + ".mp4"), f"(starts at {T0:.2f} on the final timeline)")
print("MISSING (placeholder cards):", missing or "none")
