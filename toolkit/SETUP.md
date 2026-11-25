# Cashley Tools

Everything used to make Cashley Finance videos: script rules, voice-over tools, the Whisper narration check, the automatic frame check, the Buck and Hamlet character kit, and a HyperFrames scene template.

## 1. Install (once per computer)

Needs **Python 3.10+**, **Node.js 22+** and **FFmpeg** installed first.

- **Windows** (PowerShell, in this folder): `powershell -ExecutionPolicy Bypass -File setup.ps1`
- **macOS / Linux** (Terminal, in this folder): `bash setup.sh`

It installs the Python packages (faster-whisper, elevenlabs), downloads the Whisper model (about 250 MB, once), installs Playwright's Chromium, and checks HyperFrames.

**ElevenLabs key:** set it as an environment variable called `ELEVENLABS_API_KEY`. Never paste it into a file or a chat.

**HyperFrames usage tracking:** keep it off by setting `DO_NOT_TRACK=1` and `HYPERFRAMES_NO_TELEMETRY=1` before running it (the setup scripts do this for their own run).

## 2. What's inside

| Folder | What it is |
|---|---|
| `docs/` | The script system (research → script → humanization), the format guide and writing style, the video variety log, and the AI-detection notes |
| `tools/` | Voice-over, narration and frame tools (below) |
| `kit/characters/` | Buck (cocky dollar bill) and Hamlet (grumpy piggy bank): `characters.js` plus the character sheet |
| `kit/props/` | Road map, pizza, EXAMPLE card and badge, source tag, price board: `props.js` plus sheets |
| `templates/hyperframes-scene/` | A working HyperFrames scene (road map, Buck, phone, pizza with the bite) to copy for new scenes |

## 3. The tools

| Command | What it does |
|---|---|
| `python tools/check_script.py <script.md>` | Checks writing rules: banned AI phrases, sentence lengths, questions, repeated openers |
| `python tools/make_voiceover_v2.py <script.md> <voiceover.md>` | Builds the voice-only recording sheet from an S001-format script |
| `python tools/generate_voiceovers.py <script.md> <clips-dir>` | Records each line with ElevenLabs (cast and voice IDs are inside the file) |
| `python tools/build_track.py <script.md> <clips-dir> <out.mp3>` | Joins clips in order, trims silences, adds the pause beats, evens out loudness to YouTube's level |
| `python tools/qa_narration.py <script.md> <narration.mp3>` | **Whisper check:** listens to the narration and lists dead gaps, stretched words, slow or rushed sentences and wrong words, with timestamps |
| `node tools/frame_check.js <scene-dir> [--video render.mp4]` | **Frame check:** steps through a scene and flags anything past the frame edge or outside the safe area, overlaps, errors and missing files; saves snapshots with red boxes |
| `node kit/characters/render_sheet.js out.png 2` | Re-renders the character sheet |
| `node kit/props/render_props.js out.png 2` | Re-renders the props sheet |

## 4. Making a scene with HyperFrames

1. Copy `templates/hyperframes-scene/` to a new folder.
2. Put the narration for that scene at `assets/narration.mp3` (the template expects it; the frame check reports it as missing until it's there).
3. Edit `index.html`: characters and props come from `kit/` (same colours, line weight and hand-drawn wobble).
4. Use the Whisper word timings so each picture lands on its word.
5. Check it: `npx hyperframes@0.9.92 check` and `node tools/frame_check.js <scene-dir>`. Fix everything flagged.
6. Render: `npx hyperframes@0.9.92 render`, then run the frame check again with `--video`.

## 5. Rules that always apply

- Every made-up number carries the **EXAMPLE · MADE-UP NUMBERS** badge; every real number gets a **source tag** bottom-left.
- Every number, date and abbreviation in spoken text is written out in words.
- Motion is built into each scene as it's made; sound effects go in once, at the end.
- No video goes out until the Whisper check and the frame check both pass.
