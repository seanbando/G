"""Generate a Saylo voiceover in small chunks, check consistency, and join it into one track.

Usage:
    python3 saylo/tools/generate_vo.py saylo/videos/NN-slug            # generate missing chunks + build
    python3 saylo/tools/generate_vo.py saylo/videos/NN-slug --redo 012,047   # regenerate only these chunks
    python3 saylo/tools/generate_vo.py saylo/videos/NN-slug --build-only     # just re-join

Reads <video>/script.md. Writes:
    <video>/vo/VO-001.mp3 …          one file per chunk (1–3 sentences)
    <video>/vo/chunks.tsv            id, chapter, text
    <video>/voiceover-full.mp3       joined track
    <video>/vo-timings.tsv           id, chapter, start, end, text (real timestamps for the shot list)
    <video>/vo-check.md              pace/loudness outliers to listen to

Consistency: same voice, model, settings and seed for every chunk, plus the text before and
after each chunk as context (previous_text / next_text), so the read flows across files.
Needs ffmpeg. ElevenLabs auth comes from the environment's proxy (dummy key in the header).
"""
import concurrent.futures as cf
import json
import os
import re
import statistics as st
import subprocess
import sys

VOICE_ID = "MB346AXfvAnxXiEMXWHX"  # "Saylo new" — creator's Yaboy remix, deeper/steadier (style sheet)
MODEL = "eleven_v4"
SETTINGS = dict(stability=0.4, similarity_boost=0.8, style=0.2, use_speaker_boost=True, speed=1.0)
SEED = 1996
API = "https://api.elevenlabs.io/v1/text-to-speech/{}?output_format=mp3_44100_128"

# Spoken forms the voice tends to misread. Applied to the audio text only.
SPOKEN = {
    "3:30": "three thirty",
    "12:57": "twelve fifty-seven",
    "12:58": "twelve fifty-eight",
    "about 1:20": "about one twenty",
    "7:30 a.m.": "seven thirty a.m.",
    "1 a.m.": "one a.m.",
    "101st Airborne": "one-oh-first Airborne",
}

# Pauses (seconds) inserted when joining.
GAP_SENTENCE = 0.28   # between chunks of the same paragraph
GAP_PARAGRAPH = 0.55  # between paragraphs
GAP_CHAPTER = 1.4     # at chapter headings
BEATS = {              # extra hold after a chunk ending with this text
    "a pretty good one.": 0.9,
    "Almost nothing.": 1.0,
    "He was 44.": 4.0,          # silent Jewell photo hold
    "a rookie was.": 1.5,
}

# Approved takes: a chunk whose text matches uses this recorded file instead of a new
# generation, plus an extra pause before it. Paths are relative to the video folder.
LOCKED = {
    "It's a lie, and a pretty good one.": dict(
        file="voice-samples/lie-takes/take3-line.mp3", pre=0.8),  # take 3, chosen Nov 14, 2026
}


def chunks_from_script(path):
    text = open(path).read().split("\n---\n", 1)[1]
    chapter, out = "Cold open", []
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para or para == "---" or para.startswith("[VISUAL") or para == "[PART 2]":
            continue
        if para.startswith("## "):
            chapter = para[3:].strip()
            out.append(("CHAPTER", chapter))
            continue
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'—])", para)
        buf = []
        for s in sentences:
            if buf and (len(buf) == 3 or len(" ".join(buf + [s])) > 260):
                out.append((chapter, " ".join(buf)))
                buf = []
            buf.append(s)
        if buf:
            out.append((chapter, " ".join(buf)))
        out.append(("PARA", None))
    units, kind = [], None
    for chap, t in out:
        if chap == "CHAPTER":
            kind = "chapter"
        elif chap == "PARA":
            kind = kind or "paragraph"
        else:
            units.append({"id": f"{len(units) + 1:03d}", "chapter": chap, "text": t,
                          "gap_before": kind or "sentence"})
            kind = None
    units[0]["gap_before"] = "none"
    return units


def spoken(t):
    for a, b in SPOKEN.items():
        t = t.replace(a, b)
    return t


def generate(unit, prev_text, next_text, out_path):
    body = {"text": spoken(unit["text"]), "model_id": MODEL, "voice_settings": SETTINGS, "seed": SEED}
    if prev_text:
        body["previous_text"] = spoken(prev_text)
    if next_text:
        body["next_text"] = spoken(next_text)
    for attempt in range(4):
        r = subprocess.run(["curl", "-sS", "-o", out_path, "-w", "%{http_code}", "-X", "POST", API.format(VOICE_ID),
                            "-H", "xi-api-key: dummy", "-H", "Content-Type: application/json",
                            "-d", json.dumps(body)], capture_output=True, text=True)
        if r.stdout == "200":
            return unit["id"], "ok"
        err = open(out_path, errors="ignore").read()[:200] if os.path.exists(out_path) else r.stderr
        if os.path.exists(out_path):
            os.remove(out_path)
        if attempt == 3:
            return unit["id"], f"FAILED {r.stdout} {err}"
        subprocess.run(["sleep", str(2 ** (attempt + 1))])


def ff(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], capture_output=True, text=True)


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)


def loudness(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[0-9.]+)", log)
    return float(m.group(1)) if m else 0.0


def build(video, units):
    vo, tmp = os.path.join(video, "vo"), os.path.join(video, "vo", "_tmp")
    os.makedirs(tmp, exist_ok=True)
    trim = "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse"
    gaps = {"none": 0, "sentence": GAP_SENTENCE, "paragraph": GAP_PARAGRAPH, "chapter": GAP_CHAPTER}
    listing, t, rows, stats = [], 0.0, [], []
    for u in units:
        wav = os.path.join(tmp, f"{u['id']}.wav")
        ff("-i", os.path.join(vo, f"VO-{u['id']}.mp3"), "-af", trim, "-ar", "44100", "-ac", "1", wav)
        gap = gaps[u["gap_before"]] + (rows and BEATS_after(rows[-1][4]) or 0) + LOCKED.get(u["text"], {}).get("pre", 0)
        if gap:
            sil = os.path.join(tmp, f"gap-{u['id']}.wav")
            ff("-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", f"{gap:.2f}", sil)
            listing.append(sil)
            t += gap
        d = dur(wav)
        listing.append(wav)
        rows.append((u["id"], u["chapter"], t, t + d, u["text"]))
        stats.append((u["id"], len(u["text"].split()) / d * 60 if d else 0, loudness(wav), d, u["text"]))
        t += d
    with open(os.path.join(tmp, "list.txt"), "w") as f:
        f.writelines(f"file '{os.path.abspath(p)}'\n" for p in listing)
    out = os.path.join(video, "voiceover-full.mp3")
    ff("-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-c:a", "libmp3lame", "-b:a", "192k", out)
    with open(os.path.join(video, "vo-timings.tsv"), "w") as f:
        f.write("id\tchapter\tstart\tend\ttext\n")
        for i, c, a, b, txt in rows:
            f.write(f"{i}\t{c}\t{mmss(a)}\t{mmss(b)}\t{txt}\n")
    report(video, stats, t)
    subprocess.run(["rm", "-rf", tmp])
    return out, t


def BEATS_after(text):
    return next((v for k, v in BEATS.items() if text.endswith(k)), 0)


def mmss(s):
    return f"{int(s // 60)}:{s % 60:05.2f}"


def report(video, stats, total):
    long = [s for s in stats if len(s[4].split()) >= 6]  # pace is noisy on tiny chunks
    pm, ps = st.mean(x[1] for x in long), st.pstdev(x[1] for x in long)
    lm, ls = st.mean(x[2] for x in stats), st.pstdev(x[2] for x in stats)
    flags = []
    for i, wpm, loud, d, txt in stats:
        why = []
        if len(txt.split()) >= 6 and abs(wpm - pm) > 2 * ps:
            why.append(f"pace {wpm:.0f} wpm (avg {pm:.0f})")
        if abs(loud - lm) > 2 * ls:
            why.append(f"loudness {loud:.1f} dB (avg {lm:.1f})")
        if why:
            flags.append(f"| VO-{i} | {'; '.join(why)} | {txt[:80]} |")
    lines = [f"# Voiceover check\n", f"Total length: **{mmss(total)}** · {len(stats)} chunks · average pace {pm:.0f} wpm · average loudness {lm:.1f} dB\n",
             "Chunks more than 2 standard deviations from the average. Listen to these; redo with `--redo ID,ID`.\n",
             "| Chunk | Why | Text |", "|---|---|---|", *(flags or ["| — | none flagged | |"])]
    open(os.path.join(video, "vo-check.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def main(argv):
    video = argv[0].rstrip("/")
    redo = set()
    if "--redo" in argv:
        redo = {x.strip().zfill(3) for x in argv[argv.index("--redo") + 1].split(",")}
    units = chunks_from_script(os.path.join(video, "script.md"))
    vo = os.path.join(video, "vo")
    os.makedirs(vo, exist_ok=True)
    with open(os.path.join(vo, "chunks.tsv"), "w") as f:
        f.write("id\tchapter\tgap_before\ttext\n")
        f.writelines(f"{u['id']}\t{u['chapter']}\t{u['gap_before']}\t{u['text']}\n" for u in units)
    if "--build-only" not in argv:
        jobs = []
        for i, u in enumerate(units):
            path = os.path.join(vo, f"VO-{u['id']}.mp3")
            lock = LOCKED.get(u["text"])
            if lock:
                subprocess.run(["cp", os.path.join(video, lock["file"]), path])
                continue
            if os.path.exists(path) and u["id"] not in redo:
                continue
            prev_t = units[i - 1]["text"] if i else None
            next_t = units[i + 1]["text"] if i + 1 < len(units) else None
            jobs.append((u, prev_t, next_t, path))
        print(f"{len(units)} chunks, generating {len(jobs)} ({sum(len(spoken(j[0]['text'])) for j in jobs)} chars)")
        with cf.ThreadPoolExecutor(4) as ex:
            for uid, status in ex.map(lambda j: generate(*j), jobs):
                if status != "ok":
                    print(uid, status)
        missing = [u["id"] for u in units if not os.path.exists(os.path.join(vo, f"VO-{u['id']}.mp3"))]
        if missing:
            sys.exit(f"missing chunks: {','.join(missing)} — rerun to retry")
    out, total = build(video, units)
    print(f"\nwrote {out} ({mmss(total)})")


if __name__ == "__main__":
    main(sys.argv[1:])
