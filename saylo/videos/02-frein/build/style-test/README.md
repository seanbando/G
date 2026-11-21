# Frein cold open: Retraced-look style test (Nov 18, 2026)

VO 0:00–0:52.8 of the approved voiceover (untouched), 22 shots cut on `vo-words.json` word times.
Build: `powershell -File saylo/videos/02-frein/build/style-test/build.ps1` → `build/render/frein_cold_open_style_test.mp4` (not in git).
Stills only: `build.ps1 -Stills`; some shots: `build.ps1 -Only "3,11"`.

- `shots.json`: every shot with its VO line, what it shows, and for real clips the source file, in/out seconds and watermark tag.
- `S_airfield.py`: one clay world (runway, hangar, resort block, pine woods), one shot per run. 19 of the 22 shots.
- `S_map.py`: road map from OpenStreetMap data (`build/osm/region.json`), amber pin on the airfield. Credit tag `source-openstreetmap.png`.
- `S_photo.py`: FBI photo with the name typed beside it. `O_tag.py`: name-tag overlay for real clips.
- `assemble.py`: cuts the real clips from `media/src/`, adds source tags, voice, music bed A, key clicks.
- New in `saylo/tools/blender/retraced.py`: walk cycle, kneel / prone poses, tactical kit (helmet + vest), cap, quote text.

## What is real and what is schematic
- Real: the CBS footage of Scott Malkowski (shots 10, 15, 16), the FBI photo (22), the roads and towns on the map (4).
- Schematic: the airfield set. OpenStreetMap has the roads around Birchwood Road but not the airstrip, hangar or resort
  buildings, so their layout is an illustration of "an abandoned resort with an old airstrip", not a survey.
- The hat is a plain close-fitting black cap. Malkowski only said "the black hat"; its shape is not in our sources.

## Open points for the creator
- Hat shape (cap / beanie / brimmed)?
- "6:07 PM" on the date stamp comes from `coverage.md`; the narration says "a little after six".
- Render quality is the kit's 1-sample policy; more samples only on request.
