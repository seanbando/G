# Retraced look: 30-second style test (Nov 16, 2026)

The Olympic Bomber cold open (VO 0:00–0:33, real narration, cut on `vo-words.json`) rebuilt in the Retraced look, all in Blender by script.
Build: `powershell -File saylo/videos/00-retraced-style-test/build/build.ps1` → `render/retraced_style_test.mp4` (not in git).
Stills only: `build.ps1 -Stills`; some shots: `build.ps1 -Only "3,11"`.

- `build/shots.json`: 13 shots, each with its VO line and what it shows.
- `build/S_cold_open.py`: one clay world (Murphy main street + Save-A-Lot back lot, schematic), one shot per run.
- `saylo/tools/blender/retraced.py`: the reusable Retraced layer on top of `clay.py` (mannequins + poses + run cycle, open-cabin patrol car with lights, glowing route line, flashlight, typed date stamp / name tag / in-set lettering).

## Checklist against the Retraced look
| Element | Status in this test |
|---|---|
| Faceless mannequins, subject the one glossy amber mannequin | Built (procedural, posable: sit, crouch, run, hands up). Looks like an artist's wooden mannequin, not Retraced's smooth realistic figure. |
| Clean 3D sets of real places, dark navy light | Built (street, store, back lot, dumpsters, patrol car). Simple boxes; no furniture or interior props yet. |
| White clay city-block map with a glowing route line | Built (top-down store block, amber line draws behind the store, store lit amber). |
| White clay busts of real people | **Missing.** Needs a head model per person (photo → 3D), and a rule call: Saylo never fakes real faces. |
| Chapter titles built into the scene | Built (MURPHY / NORTH CAROLINA typed onto a building wall). |
| Date stamps | Built (big white caps top-left, typed on with cursor + key clicks). |
| Quote walls | Helper not built yet (no quote in these 33 s). Same text code as the stamps; quick to add. |

## What's missing to match Retraced fully
1. **A real mannequin model** (smooth body, rigged). Free CC0 options exist (e.g. a base mesh + Rigify); the procedural one works but reads toy-like.
2. **Clay busts** for real people (see rule above).
3. **Props library**: furniture, gym/office/apartment pieces, cars that look like cars. Today everything is boxes.
4. **Render quality**: the kit renders at 1 sample by policy (grain at night). Only the creator can ask for more samples.
5. **Mountains**: low-poly cones; a displaced terrain (like `clay.mountains`) would look better around the town.
6. Flashlight does not follow the man when he runs in shot 13 (he still reads in the dark).
