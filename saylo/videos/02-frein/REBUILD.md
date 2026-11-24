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

## Exact recipe (verified Nov 21, 2026 in a cloud session; use it on the PC)
Everything below was done once in a cloud session (no graphics card, so it could not render the airfield scene):
the PC only has to repeat it. Paths are from the repo root.

### Videos → `saylo/videos/02-frein/media/src/` (shared "anyone with the link": plain download works)
Download each with `https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t` and save under the name shown:
| Drive ID | save as |
|---|---|
| 1EW1P5Mj83qaqC8h7ahtohMRunXzhelxq | Authorities Identify Suspect in Pennsylvania Barracks Shooting - ABC News (720p, h264).mp4 |
| 1HXyngOoKsM5vK3paIp2hU63sqeUBQJ0_ | Eric Frein manhunt Suspect may have left letter - CBS Evening News (720p, h264).mp4 |
| 1yrLqEGsdQ54M552eZqOPpxa3vQfIZHm7 | Pa. breathes easier after capture of Eric Frein - CBS Evening News (720p, h264).mp4 |
| 10ZN86X_WXZpD6cZ4ZBcSHHPIHk1st1Ff | Police discovers journal of Pennsylvania cop killer suspect - CBS Mornings (720p, h264).mp4 |
| 1NPtg6ExSncU2-v0Wmqo8pQSFrsHf4S2j | Search for alleged cop killer instills fear in Pa. community - CBS Evening News (720p, h264).mp4 |
| 1_hCD1BpdLLhWrGthauEdHok0t247z1K7 | Slain cop's cuffs used to arrest Frein - CNN (720p, h264).mp4 |
| 1n_ELODyWhiihFwaSFR7HBGfCOM_ku2r1 | Pike County DA Ray Tonkin responds to Eric Frein's Sentence of Death - Straus News (1080p, h264).mp4 |
| 1SJM_Jn3edOxcnZrYk6Z0SDHfu3wWnbO6 | Eric Frein Notice of Execution signed for man responsible for killing PA State Trooper - WTAJ News (1080p, h264).mp4 |
| 1HHkLR8zsyf9stWyCzq5wo60kPSb90Sp3 | hangar-screen-recording-2026-11-19.mp4 |
| 12jF3JSMoZcK5bWiR87TYlADgGNYsrAiA | wnep-novak-jeep-screen-recording.mp4 |
(After they are downloaded, the creator sets these 10 back to Restricted in Drive.)

### Photos → `saylo/videos/02-frein/media/photos/` (private: Google Drive connector, or download from Drive by hand)
All in the Drive folder "Frein". Drive ID → plan name:
1pSlMASBgDxKBLqL0Y3Hyg9Qf03RqCJcB 09d-campsite-default.jpg · 1M2sumeGkE3pqeeIMg8qVgQMk_Psz4WQO 11c-phillymag-perp-walk-night.jpg ·
1xR06aVVOI2f6-omXo-1WhtdsbQAH0MoK 13b-cbs-halloween-headline.png · 1dDYQ8slkN88UGSVQadoET4qmwrBWVPiF 14-dailylocal.webp ·
1jhTiML_wlE1UpNPkgSZqBUkdraqKesJp 18b-buzzfeednews-fbi-page.png · 1-48bEvt7BaeLrlmpcEN92qjguHTpVll3 19a-court-opinion-p28.png ·
1omefhpFpViX-PH2D6tpwbZjiJNPWcs4n 19b-court-opinion-p29.png · 1AYrozZEUXUqbuAMm8uyjGv2nMCCnSpI2 19c-court-opinion-p1-caption.png ·
1qGKJbVG1V7PTaFGW_9lfh8eLkJXozPdp 20-inquirer-headline.png · 1kKEf8NA9ejVPWIC1Bj3Nij6B8Wmy_yq5 23-courthouse-milford.jpg ·
1Sul11U6kFh346-IIJBcdIWoA-TNZlKue 25-canadensis.jpg · 1islCZfc_qypq2BQEhVSgX_g2YZaC0_0u 26a-bog-forest.jpg ·
1nuRbTIi-fXx7Oe-tqsM4GmGU4tdLC4uq 26b-bog-forest.jpg · 1nWYjEsKmCiu17xu6DEiZfT37suArkIY5 27c-jeep-swamp-ap.jpg ·
1kkM6lgfbwKxGNJWZbLf_IY4oc1AM1MmT 30-troopers-rifles-6ES2.webp · 1UqT8jf4d5ovgtDEfM9L56AZG6Rkcooax 31-abc-roadblock-inset.jpg ·
1vpxpOy1g4FUt6sodawI3_ZVPYK27Lx-1 32-ap-perp-walk.jpg · 1RYYjQNgd1YUKB8BiGvwdnC3Gk6zBF69z 33-thecitizensvoice-cruisers-field.jpg ·
1Hk1qvAMKACFXiKzT19K4x1eufKpujnNt 34-armored-PPO235.jpg · 1ZKjeMNU2_8sDkh5let3CoiACrEWMSpvf 35-tactical-team-ghows.webp ·
1ljHCX6SXXJqPE-Iw-yqzRhuna8Usj5ha 36-abcnewsgo.jpg · 12hFd_2RyfxXpCetbhOcjwaeZJb_Ncl7w 41-poconorecord.webp ·
1DDwMfkmAs-oiZdKYX01JI69IX5UYMEoW 7Y7YM5UU.jpg · 1kKqUkJedNMm-DJy4RhyGqk-_HY6pIQyZ AP-manhunt-snow-hill-road.jpg ·
1vFQ5MxjgHMHpeTd_SJf0HBBhrIGCDLcR TMC-FreinManhunt-troopers-stage.webp · 1gPx29KZvHEbqhO_GFRcsDJdYebSDRUJx ca-times-brightspot.jpg ·
1xCWKjwD051-x0f3iyaSiDAgm2DTKUV1c hangar-exterior.jpg · 1-6FFZYs-hSqDjuFOmgLyq1j9OqdSwQ8s hangar-interior-reuters-abc.jpg ·
1niZM4wi_1EGnhGhis8CW7sUteu45010c mcall-b.webp (barracks sign) · 1yKUQUV270NuMagBQt8nnASvEyE5ujhZz pikecountycourier-b.webp (helicopter) ·
1TGKEzLy0e_tcIehdWCea747Nsg-qUh4j wnep-a.jpg (camera crews) · 1uhKlpK8Cd3D-SLvO6b6ma80Op1Ola_fz wnep-b.jpg (barracks, tape)
and 1ugcehj-lcT07zvpfBrCx_G-Pn3ueAaPP → `media/src/Eric_Frein ( wikimedia commons).jpg`.
(Drive has two files named mcall.webp, pikecountycourier.webp and wnep.jpg: use the IDs above, they are checked against the plan.)

### Cut-outs → `saylo/videos/02-frein/media/cuts/` (Pillow crops, pixel boxes left, top, right, bottom)
- `fbi-page-right.png`: from 18b-buzzfeednews-fbi-page.png (938x442) box (476, 0, 938, 435). Checked: the shot-325 highlights land on the Serbian/Russian line.
- `inquirer-headline-card.png`: from 20-inquirer-headline.png (2000x510) box (0, 0, 2000, 295).
- `dickson-portrait.png`: CNN "Slain cop's cuffs" frame at 112.0 s, box (402, 0, 884, 486) (PSP portrait; name tag reads DICKSON in the ABC frame).
- `douglass-portrait.png`: ABC "Authorities Identify Suspect" frame at 70.0 s, box (704, 48, 1086, 520) (the black-and-white portrait in the campaign hat).
  Not "alex douglas tpt.avif" in Drive: that is a recent personal photo, not the official portrait.

### Kit and assets
- Render kit: Drive "Faceless-Studio-2-Documentary-Pro (3).zip" (ID 1VqAyCBg86Bnp6oOfOBpAKC_LL23M2fgS) unzipped into `_kit/docpro/`.
- Poly Haven: the commands in `saylo/tools/cloud_setup.sh` step 4 (textures, grass, fir/pine scans, sky with a User-Agent header).
- Trees: `blender -b --factory-startup --python saylo/tools/blender/prep_trees.py` and `... prep_trees_mid.py`
  (on the PC leave TREES_MID_SCALE unset = full hero trees; the scripts now import the scans in slices, so RAM is no problem).
- Mannequin: `blender -b --factory-startup --python saylo/tools/blender/make_mannequin.py` → `_kit/assets/mannequin/male_base_mesh.glb`.
  The original CC0 base mesh was lost with the old PC; this rebuild uses Blender's Rigify skeleton and the same file contract.
  Show the creator one still with it (e.g. shot 315) before rendering motion: its shape differs a little from the approved cold open.

### What the cloud session already produced (not in git, so redo on the PC)
- Chapters 02-03 stills: 36 of 37 rendered and sent; shot 315 (S_open, airfield woods) crashes in Blender's EEVEE on software
  OpenGL and needs the PC's graphics card. Re-run `python stills.py shots5.json` on the PC to rebuild the sheet, then render.
