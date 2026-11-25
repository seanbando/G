"""Record a narration in natural takes and write a word-level timing map for the visuals.

Usage:
  ELEVENLABS_API_KEY=... python3 tools/record_natural.py <script.md> <out-dir> [--max-chars 900] [--only TAKE_ID,...]

Instead of one recording per short line (which makes the voice restart its tone every
sentence), consecutive narrator lines are recorded as one take, broken only at section
headings, character lines (Buck, Hamlet), [PAUSE] beats or about --max-chars characters.
Character lines are recorded on their own in their own voices.

Takes are kept whole in the final track, so the pace and pauses are exactly as spoken:
no speeding up, slowing down or re-gluing sentences. Whisper then listens to every take
and writes <out-dir>/timings.json with the start and end of each line and each word in
the final track, which the scenes use so every picture lands on its word.

Outputs in <out-dir>:
  takes/T01_NARRATOR.mp3 ...  the raw recordings (re-record one with --only T07)
  narration.mp3                 the full track (levelled, YouTube loudness)
  timings.json                  {"lines": [{"id","voice","text","start","end","words":[...]}], "pauses": [...]}
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from make_voiceover_v2 import parse  # noqa: E402
from qa_narration import norm_tokens  # noqa: E402
from build_track import loudness, LIMIT, CLIP_TARGET, FINAL_TARGET  # noqa: E402
import generate_voiceovers as gv  # noqa: E402

GAP_SAME_VOICE = 0.35   # between two takes of the narrator (a section break)
GAP_NEW_VOICE = 0.4     # when Buck or Hamlet cuts in, or hands back


def ff(*a):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *a], check=True, stdin=subprocess.DEVNULL)


def duration(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def plan_takes(script, max_chars):
    """Group script lines into takes. Returns a list of segments in order:
    {"kind": "take", "id", "voice", "lines": [(id, text)]} or {"kind": "pause", "seconds", "text"}."""
    _, items = parse(script)
    segs, cur = [], None

    def close():
        nonlocal cur
        if cur:
            segs.append(cur)
        cur = None

    for it in items:
        if it[0] == "section":
            close()
        elif it[0] == "pause":
            close()
            m = re.search(r"([\d.]+)\s*second", it[1])
            segs.append({"kind": "pause", "seconds": float(m.group(1)) if m else 2.0, "text": it[1]})
        else:
            _, lid, voice, _, text = it
            chars = sum(len(t) for _, t in cur["lines"]) if cur else 0
            if cur and voice == "NARRATOR" and cur["voice"] == "NARRATOR" and chars + len(text) <= max_chars:
                cur["lines"].append((lid, text))
            else:
                close()
                cur = {"kind": "take", "voice": voice, "lines": [(lid, text)]}
                if voice != "NARRATOR":
                    close()
    close()
    n = 0
    for s in segs:
        if s["kind"] == "take":
            n += 1
            s["id"] = f"T{n:02d}"
    return segs


def record(segs, out, only):
    from elevenlabs.client import ElevenLabs
    from elevenlabs.types import VoiceSettings
    client = ElevenLabs()
    takes = [s for s in segs if s["kind"] == "take"]
    os.makedirs(os.path.join(out, "takes"), exist_ok=True)
    for i, s in enumerate(takes):
        path = os.path.join(out, "takes", f"{s['id']}_{s['voice']}.mp3")
        s["path"] = path
        if only and s["id"] not in only and not any(l[0] in only for l in s["lines"]):
            continue
        if os.path.exists(path) and not only:
            continue
        text = " ".join(t for _, t in s["lines"])
        prev_t = " ".join(t for _, t in takes[i - 1]["lines"]) if i else None
        next_t = " ".join(t for _, t in takes[i + 1]["lines"]) if i + 1 < len(takes) else None
        audio = client.text_to_speech.convert(
            voice_id=gv.VOICES[s["voice"]], text=text, model_id=gv.MODEL, output_format=gv.FORMAT,
            voice_settings=VoiceSettings(speed=1.0, **gv.SETTINGS),
            previous_text=prev_t[-600:] if prev_t else None, next_text=next_t[:600] if next_t else None)
        with open(path, "wb") as fh:
            for chunk in audio:
                fh.write(chunk)
        print(f"recorded {s['id']} {s['voice']}: {len(s['lines'])} line(s), {len(text)} chars")
    for s in takes:
        s["path"] = os.path.join(out, "takes", f"{s['id']}_{s['voice']}.mp3")


def clean_edges(src, dst, speech_end, sr=44100):
    """Cut any click, breath or static before the first word and after the last one.
    Start: finds where speech gets loud and walks back to the last quiet moment before it.
    End: never cuts before Whisper's end of the last word (speech_end); cuts at the first
    0.1 s of real quiet after it, so trailing static is dropped but soft last words stay.
    Tiny fades so the cut itself can't click."""
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    a = np.frombuffer(pcm, dtype=np.float32).copy()
    win = int(0.01 * sr)
    n = len(a) // win
    db = 20 * np.log10(np.abs(a[:n * win]).reshape(n, win).max(axis=1) + 1e-9)
    top = db.max()
    first = int(np.argmax(db > top - 12))
    j = first
    for _ in range(30):  # up to 0.3 s back to the last quiet moment
        if j == 0 or db[j - 1] < top - 32:
            break
        j -= 1
    start = (j - 1 if j > 0 and db[j - 1] < top - 32 else max(0, j - 4)) * win
    k = min(n - 1, int(np.ceil(speech_end / 0.01)))
    end_w = None
    while k < min(n, int((speech_end + 0.8) / 0.01)):
        if k + 10 <= n and (db[k:k + 10] < top - 35).all():
            end_w = k + 2
            break
        k += 1
    end = min(len(a), (end_w if end_w else int((speech_end + 0.3) / 0.01)) * win)
    a = a[start:end]
    fi, fo = int(0.008 * sr), int(0.03 * sr)
    a[:fi] *= np.linspace(0, 1, fi)
    a[-fo:] *= np.linspace(1, 0, fo)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                    "-c:a", "pcm_s16le", dst], input=a.tobytes(), check=True)
    return start / sr, end / sr


def words_in(model, wav):
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    segs, _ = model.transcribe(np.frombuffer(pcm, dtype=np.float32), word_timestamps=True, beam_size=5,
                               condition_on_previous_text=False)
    out = []
    for seg in segs:
        for w in seg.words or []:
            for t in norm_tokens(w.word) or [w.word.strip().lower()]:
                out.append({"w": t, "start": w.start, "end": w.end})
    return out


def align_take(lines, heard, take_len):
    """Find where each line of a take starts and ends, using Whisper's words."""
    exp, owner = [], []
    for k, (_, text) in enumerate(lines):
        toks = norm_tokens(text)
        exp += toks
        owner += [k] * len(toks)
    sm = difflib.SequenceMatcher(a=exp, b=[h["w"] for h in heard], autojunk=False)
    match = {}
    for a, b, n in sm.get_matching_blocks():
        for j in range(n):
            match[a + j] = b + j
    result = []
    for k, (lid, text) in enumerate(lines):
        idx = [i for i in range(len(exp)) if owner[i] == k and i in match]
        if idx:
            s, e = heard[match[idx[0]]]["start"], heard[match[idx[-1]]]["end"]
            words = [{"word": exp[i], "start": heard[match[i]]["start"], "end": heard[match[i]]["end"]} for i in idx]
        else:
            s, e, words = None, None, []
        result.append({"id": lid, "text": text, "start": s, "end": e, "words": words,
                       "matched": len(idx), "total": owner.count(k)})
    # fill lines Whisper missed by splitting the time between their neighbours
    for k, r in enumerate(result):
        if r["start"] is None:
            prev_end = next((result[j]["end"] for j in range(k - 1, -1, -1) if result[j]["end"] is not None), 0.0)
            next_start = next((result[j]["start"] for j in range(k + 1, len(result)) if result[j]["start"] is not None), take_len)
            r["start"], r["end"], r["estimated"] = prev_end, next_start, True
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out")
    ap.add_argument("--max-chars", type=int, default=900)
    ap.add_argument("--only", help="comma-separated take or line IDs to re-record")
    ap.add_argument("--model", default="small.en")
    args = ap.parse_args()
    only = set(args.only.split(",")) if args.only else None

    segs = plan_takes(args.script, args.max_chars)
    takes = [s for s in segs if s["kind"] == "take"]
    print(f"{len(takes)} takes ({sum(1 for s in takes if s['voice'] == 'NARRATOR')} narrator) for "
          f"{sum(len(s['lines']) for s in takes)} lines")
    record(segs, args.out, only)

    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    tmp = tempfile.mkdtemp()
    parts, timeline, pauses, t, prev_voice = [], [], [], 0.0, None

    def silence(sec):
        p = os.path.join(tmp, f"sil_{sec}.wav")
        if not os.path.exists(p):
            ff("-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(sec), "-c:a", "pcm_s16le", p)
        return p

    just_paused = False
    for s in segs:
        if s["kind"] == "pause":
            parts.append(silence(s["seconds"]))
            pauses.append({"start": round(t, 3), "end": round(t + s["seconds"], 3), "text": s["text"]})
            t += s["seconds"]
            just_paused = True
            continue
        if parts and not just_paused:
            gap = GAP_SAME_VOICE if s["voice"] == prev_voice else GAP_NEW_VOICE
            parts.append(silence(gap))
            t += gap
        just_paused = False
        raw = os.path.join(tmp, s["id"] + "_raw.wav")
        wav = os.path.join(tmp, s["id"] + ".wav")
        heard_raw = words_in(model, s["path"])
        cut_in, cut_out = clean_edges(s["path"], raw, heard_raw[-1]["end"] if heard_raw else 1e9)
        if cut_in > 0.2:
            print(f"  {s['id']}: cut {cut_in:.2f} s of noise/silence before the first word")
        ff("-i", raw, "-af", f"volume={CLIP_TARGET - loudness(raw):.2f}dB,{LIMIT}", "-ac", "1", "-ar", "44100",
           "-c:a", "pcm_s16le", wav)
        length = duration(wav)
        for r in align_take(s["lines"], words_in(model, wav), length):
            r.update(voice=s["voice"], take=s["id"], start=round(t + r["start"], 3), end=round(t + r["end"], 3))
            for w in r["words"]:
                w["start"], w["end"] = round(t + w["start"], 3), round(t + w["end"], 3)
            timeline.append(r)
        parts.append(wav)
        t += length
        prev_voice = s["voice"]

    listing = os.path.join(tmp, "list.txt")
    with open(listing, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    joined = os.path.join(tmp, "joined.wav")
    ff("-f", "concat", "-safe", "0", "-i", listing, "-c:a", "pcm_s16le", joined)
    out_mp3 = os.path.join(args.out, "narration.mp3")
    ff("-i", joined, "-af", f"volume={FINAL_TARGET - loudness(joined):.2f}dB,{LIMIT}", "-ar", "44100",
       "-c:a", "libmp3lame", "-b:a", "160k", out_mp3)
    json.dump({"audio": "narration.mp3", "duration": round(duration(out_mp3), 3), "lines": timeline, "pauses": pauses},
              open(os.path.join(args.out, "timings.json"), "w"), indent=1)
    est = [r["id"] for r in timeline if r.get("estimated")]
    low = [r["id"] for r in timeline if r["total"] and r["matched"] / r["total"] < 0.6 and not r.get("estimated")]
    print(f"{out_mp3}: {duration(out_mp3) / 60:.0f}m {duration(out_mp3) % 60:.0f}s; timings for {len(timeline)} lines")
    if est:
        print("lines Whisper didn't hear (timing estimated from neighbours):", ", ".join(est))
    if low:
        print("lines with weak word matches (check these):", ", ".join(low))


if __name__ == "__main__":
    main()
