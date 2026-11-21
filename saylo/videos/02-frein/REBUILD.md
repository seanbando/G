# 02 Frein: rebuild on a new PC WITHOUT the old PC's backup

Written Nov 21, 2026. The `Frein-backup` zips (media, kit, renders, memory) never left the old PC and it can't be reached.
Everything below rebuilds them from GitHub, Google Drive and the original download links. Do this once, then follow
`TRANSFER.md` §5 ("How to carry on").

## 0. Repo
Branch `claude/vigilant-hamilton-khjhov` (has everything from `claude/inspiring-meitner-514uac` plus `final.py`).
Repo ideally at `C:\Users\owner\G`. Check: Blender 5.3, ffmpeg, Python 3.13 on PATH.

## 1. Render kit → `_kit\docpro\`
The creator's Google Drive, folder "@watchsaylo / Downloads\working on vids":
- `Faceless-Studio-2-Documentary-Pro (3).zip` → unzip so this file exists:
  `_kit\docpro\Faceless Studio\.claude\skills\documentary-pro\scripts\render_blender.py`
- (`Faceless-Studio-3-Template-Library (2).zip` is there too; not needed by the Frein scripts.)
If a Google Drive connector is attached, download them with it; otherwise ask the creator to download them in the browser.

## 2. Assets → `_kit\assets\` (all free, CC0, re-downloadable)
From the repo root:
```
python saylo/tools/fetch_polyhaven.py textures asphalt_02 blue_metal_plate brick_wall_08 concrete_wall_004 corrugated_iron_02 cracked_concrete forest_ground_04 hangar_concrete_floor
python saylo/tools/fetch_polyhaven.py models grass_medium_01 grass_medium_02 fir_tree_01 pine_tree_01
```
- Sky: `evening_road_01_puresky` as `.hdr` (2k) from https://polyhaven.com/a/evening_road_01_puresky →
  `_kit\assets\polyhaven\hdri\evening_road_01_puresky.hdr` (fetch_polyhaven.py does not do HDRIs; download it
  from `https://api.polyhaven.com/files/evening_road_01_puresky` → `hdri` → `2k` → `hdr` → `url`).
- Trees: `blender -b --factory-startup --python saylo/tools/blender/prep_trees.py` then
  `blender -b --factory-startup --python saylo/tools/blender/prep_trees_mid.py` → `trees.blend`, `trees_mid.blend`.
- Mannequin: `_kit\assets\mannequin\male_base_mesh.glb` (`retraced.py` line ~163). Source not recorded in git. Find a
  free CC0 / CC-BY "male base mesh" GLB (e.g. Poly Haven / Sketchfab free download), save it under that name, write
  where it came from in `_kit\assets\mannequin\SOURCE.txt`, and check one still against the approved cold open look
  (grey, faceless, ~1.8 m, facing -Y). Tell the creator if it looks different.
- After that, grep the `S_*.py` scripts and `retraced.py` for any other `_kit` path and fetch what is still missing.
  Render one still per set (`stills.py`) to prove the kit works before anything long.

## 3. Footage and photos → `saylo\videos\02-frein\media\src\`
- Google Drive folder **"Frein"** (inside "Downloads\working on vids") has most news videos, photos and the screen recordings:
  copy them all into `media\src\`.
- The file names the plans expect are in each plan's `"src"` map (`build/style-test/shots*.json`) and in the footage index
  in `edit-plan.md`. Anything still missing: re-download from `download-list.md` (links + search terms),
  `sources-used.md` and `footage.md`. Cut-outs (`media\cuts\`) were made by earlier scripts; regenerate as needed.
- Photos waiting on outlet names (shots 413, 439): still open.

## 4. Renders
Gone with the old PC: `frein_cold_open_v7.mp4` (approved), the hook and Barracks motion renders. Re-render with
`build.ps1 -Plan shots2.json`, `shots3.json`, `shots4.json` (plans unchanged, so the result matches what was approved),
then carry on with `shots5.json` (re-run its stills first). One render at a time. 16 samples.

## 5. Claude's notes
The memory zip is lost. The rules that matter are in `edit-plan.md` ("Rules in force" and the Nov 20 decisions),
`saylo/CLAUDE.md` and `saylo/style-sheet.md`: read them.
