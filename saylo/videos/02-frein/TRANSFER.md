# 02 Frein: moving this project to another computer

Written Nov 20, 2026. Everything needed to pick the edit up on a different PC.

## 1. What travels with git (push, then clone)
Repo: `github.com/seanbando/G`, branch `claude/inspiring-meitner-514uac`.
- All scripts, shot plans and notes: `saylo/videos/02-frein/build/style-test/` (`shots2.json` … `shots9.json`, `S_*.py`,
  `assemble.py`, `build.ps1`, `stills.py`), `saylo/tools/blender/retraced.py`, `edit-plan.md`, `sources-used.md`.
- The approved voiceover `voiceover-full.mp3` and `vo-words.json`.
- Map data: `build/osm/`.
- Music bed and sound effects: `saylo/videos/01-olympic-bomber/sound/`.

Pushed Nov 20, 2026.

## 2. What git does NOT carry: copy these folders by hand (USB drive or cloud)
| Folder (under `C:\Users\owner\G\`) | Size | What it is |
|---|---|---|
| `saylo\videos\02-frein\media\` | 0.9 GB | news videos, photos, cut-outs (also in the Google Drive folder "Frein", except the screen recordings and `cuts\`) |
| `_kit\` | 2.2 GB | Documentary Pro render runner, Poly Haven textures, trees, sky images, mannequin |
| `saylo\videos\02-frein\build\render\` | 1.8 GB+ | everything rendered so far (optional: saves hours of re-rendering) |

Keep the same folder layout under the repo. Also outside the repo:
- `C:\Users\owner\Documents\VideoHub\films\saylo-02-frein-cold-open-test\` (review copies)
- `C:\Users\owner\.claude\projects\C--Users-owner-G\memory\` (Claude's notes on how you like to work)

## 3. Programs to install on the new PC
- Blender 5.3 (default install path)
- ffmpeg 9 (full build) on PATH
- Python 3.13 on PATH
- Git, Claude desktop app, VideoHub (`C:\Users\owner\VideoHub`)

## 4. Where the edit stands (Nov 25, 2026)
**Every chapter is rendered in motion and the whole film is joined: `build/render/frein_full_v2.mp4` (12:08, one soundtrack, -14 LUFS).**
Cold open v7 is approved; the creator has given notes on the Barracks and the Swamp chapter (applied); the other chapters and the
full join are awaiting the creator's notes.

| Section | Time | Plan | Chapter file |
|---|---|---|---|
| Cold open | 0:00-0:53 | `shots2.json` | `frein_cold_open_v7.mp4` (approved) |
| Hook | 0:53-1:49 | `shots3.json` | `frein_s2_hook.mp4` |
| 01 The Barracks | 1:49-3:40 | `shots4.json` | `frein_s3_barracks.mp4` |
| 02-03 Swamp, Who | 3:40-5:27 | `shots5.json` | `frein_s4_swamp_who.mp4` |
| 04-05 Search, Left Behind | 5:27-7:23 | `shots6.json` | `frein_s5_search.mp4` |
| 06 The Hangar | 7:23-9:17 | `shots7.json` | `frein_s6_hangar.mp4` |
| 07-08 Verdict, Confession | 9:17-10:55 | `shots8.json` | `frein_s7_court.mp4` |
| 09 Handoff + outro | 10:55-12:08 | `shots9.json` | `frein_s8_handoff.mp4` |

To change a shot: edit the plan (or `make_plans.py` for shots6-9, then run it), `build.ps1 -Plan shotsN.json -Only "id"`,
`python assemble.py shotsN.json`, then `python final.py v2` for a new full film.
**Never run two build jobs at once** (the second corrupts the first's frames).

**Backup package:** folder `Frein-backup`: `1-media.zip`, `2-kit.zip`, `3-renders.zip`, `4-claude-memory.zip`. Unzip 1-3 into
the repo folder (`G`); they already contain the right sub-paths.

## 5. How to carry on
From `saylo\videos\02-frein\build\style-test\`:
- Stills for a chapter: `python stills.py shots5.json`
- Render a chapter and join it: `powershell -File build.ps1 -Plan shots5.json`
- Re-join only (no 3D render): `python assemble.py shots5.json`
- One render at a time. A render can be stopped: finished shots (`S<id>.mp4`) are kept, but `build.ps1` renders every shot
  again unless you pass `-Only "id,id"` for the missing ones.

## 6. Still open
- Creator's notes on the full film; any weak 3D shot gets replaced by a still, real footage or a card (creator's rule).
- Small cold-open items: "ABOUT 2 HOURS IN" faint on the sky, a map label under the stamp, dark wide shot at 0:33.
- Thumbnail (phone-size test at 168 px), title and upload package.
- Two photos run without a source watermark by the creator's decision (shots 413, 439).
- Rules and decisions: see `edit-plan.md`.
