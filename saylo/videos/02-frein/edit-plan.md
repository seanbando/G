# 02 Frein: edit plan (working document, Nov 19–20, 2026)

How the edit is being built, what is approved, and the shot plan chapter by chapter. Plans are JSON files in
`build/style-test/` (one row per shot, cut on `vo-words.json` word times); stills sheets go to the creator before any
chapter is rendered in motion.

## Rules in force (creator-approved)
- **Pace and transitions approved** ("it makes me wanna keep watching"): hard cuts only, every 3D shot pushes in
  4–17% of frame per second, 40+ cuts in the first minute, 15–22 a minute after. Source: `saylo/channel/retraced-frame-analysis.md`.
- **Stills first, chapter by chapter.** `python stills.py <plan>.json` → `build/render/<dir>_stills.jpg`.
- **Every shot shows the thing being named and keeps it in frame** for the whole line.
- **Typed text finishes before the cut** (cards and maps are checked on their last frame).
- **Real footage and photos win** over 3D wherever they exist; every one carries its source tag.
- Marshals' vests read POLICE / U.S. MARSHAL (not FBI). Troopers: grey shirt, campaign hat.
- Victims: full formal name (Bryon K. Dickson II), no amber on their cards, slow shots, no effects.
- Never shown: anyone being hit, pipe-bomb close-ups, Dickson's family. Frein's scraped face: brief, wide, no zoom.
- Amber = Frein, the key object of a scene, route lines and pins. Nothing else.

## Status
| Section | Time | Plan | Stills | Motion |
|---|---|---|---|---|
| Cold open | 0:00–0:52.8 | `shots2.json` (40 shots) | approved | **v5 approved** (`frein_cold_open_v5.mp4`) |
| Hook | 0:52.8–1:48.9 | `shots3.json` (32 shots) | sent, text fixes applied | not rendered |
| 01 The Barracks | 1:48.9–3:40.1 | `shots4.json` (30 shots) | in progress | – |
| 02 The Swamp | 3:40.1–4:22.3 | to write (`shots5.json`) | – | – |
| 03 Who They Were Looking For | 4:22.3–5:26.6 | to write (`shots5.json`) | – | – |
| 04 The Search | 5:26.6–6:34 | to write | – | – |
| 05 What He Left Behind | 6:34–7:19 | to write | – | – |
| 06 The Hangar | 7:19–9:16 | to write | – | – |
| 07 The Verdict | 9:16–10:00 | to write | – | – |
| 08 The Confession | 10:00–10:55 | to write | – | – |
| 09 The Handoff + outro | 10:55–12:08 | to write | – | – |

## Sets and scripts
- `S_open.py`: the airfield (hangar rebuilt from the Reuters photo and WNEP aerial, autumn woods, scanned pines up close).
- `S_barracks.py`: Blooming Grove barracks at night, from the WNEP photo (tan block, brown hipped roof, lot, road, tree line).
- `S_map.py` (cold open) / `S_map2.py` (general): clay road maps from OpenStreetMap data in `build/osm/`. Barracks pin = OSM
  "Pennsylvania State Police - Troop R - Blooming Grove" (41.3871, -75.1310). Canadensis 41.192, -75.2513. Airfield 41.0624, -75.2534.
- `S_card.py`: typed cards (portrait, title, quote, doc with highlighter, sources, strike list).
- To build: `S_objects.py` (evidence close-ups: rifle case, casings, blank licence, notebook, laptop, handcuffs), hangar interior.

## Footage index (seconds in the source files, `media/src/`)
- **CBS capture** ("Pa. breathes easier"): 80.4–83.9 Malkowski at the map · 84.0–88.6 Malkowski with his team · perp walk after 89 (face scrapes).
- **CBS search** ("Search for alleged cop killer"), crop 1102:620:0:0: 20–24 cars racing through town · 26–28 helicopter through branches ·
  30–32 trooper stops a car · 40–41 camouflaged searchers in a field · 42–43 searcher in woods · 44–48 resident interview.
- **CBS letter** ("Suspect may have left letter"), same crop: 18–24 cruisers on a road at dusk/night · 26 re-enactor photo (PSP release) ·
  28–30 troopers in a creek · 32–34 Bivens at the microphones · 55 campsite items photo · **60.6+ pipe-bomb close-up: never use**.
- **ABC** ("Authorities Identify Suspect"), crop 896:504:192:0: 47–53 Noonan at the podium · 56–62 emergency lights at night (the night of the shooting) ·
  65–71 troopers' portraits · 74 Bivens at the podium · 77–80 police cars on a wooded road · 83–98 ABC's own dossier graphic (skip).
- **CNN** ("Slain cop's cuffs"), crop 853:480:213:0: 0.6–13 Corbett · 17.8–26 Tonkin · 44–48 arrest night, blue lights (WNEP footage) ·
  50–52 perp walk · 54–58 Noonan · 60–62 tactical team on a vehicle, woods · 92–119 reporter + Noonan on the handcuffs · 112 Dickson portrait.
- **CBS journal** ("Police discovers journal"), crop 996:560:142:0: 40.3–46.9 and 59.5–66.4 Bivens reads the journal · 105–116, 141–148 Bivens.
- **WNEP Jeep** (screen recording, crop 1840:1035:40:0; banner on screen 32–44 s): 48–56 Novak and reporter walk through the woods ·
  60–68 Novak points across the pond site · 72–76, 92–96 the track and ruts · 80–88, 100, 120–136 Novak interview · 106–109 water and reeds · 144–156 the pond field.
- **WNEP hangar** (screen recording): 16.8–44.9 helicopter views of the real hangar. Ground shots of tan hangars = a different airport: never use as the site.
- **Straus News**: 126–142 Tonkin "this verdict is for…" · 270.8–279.7 "full justice". **WTAJ**: 8.6–38.3 execution date.

## Planned, not yet written as JSON
### 02 The Swamp (220.1–262.3)
map with CHAPTER 02 lettering + SEPT 14 stamp → Novak and the reporter walking (real) → AP photo of the Jeep in the water →
Novak pointing at the pond (real) → Jeep photo with "REGISTERED TO HIS PARENTS" typed → Novak (real) → three object close-ups
(rifle case, two casings, blank licence card) → notebook pages → the ruts and the water (real) → quote card "DISASTER." →
amber figure's legs into the woods at night → Noonan at the podium (real) → Frein's FBI photo with his name typed →
map pin on Canadensis → empty woods, held, for "What they didn't have was Eric Frein."
### 03 Who They Were Looking For (262.3–326.6)
map with CHAPTER 03 lettering, pin on Canadensis → Canadensis photo (CC0) → re-enactor photo (PSP) wide, then detail →
FBI page, highlighter on the Serbian/Russian line → Bivens with name tag → quote card "ASSUMED THAT ROLE IN REAL LIFE" →
Noonan at the podium, two angles, name tag → amber figure standing in the woods → campsite items photo (PSP via CBS) →
laptop screen, three research topics typed one at a time → barracks seen straight down, "RECORDED STATEMENT · OCT 30, 2014" →
map: Canadensis and the barracks, line between → barracks from above with the tree line lit amber →
card "RECORDED STATEMENT" → court opinion p. 28 with the highlighter (tease).

## Where this stopped (Nov 20, 2026: usage limit reached mid-pass)
- Plans written: `shots2` (cold open, approved), `shots3` (hook), `shots4` (Barracks), `shots5` (Swamp + Who), `shots6` (Search + What He Left Behind, generated by `make_plans.py`).
- Still to write: The Hangar (443.07–556.55), The Verdict + The Confession (556.55–655.47), The Handoff + outro (655.47–727.8). Shot-by-shot notes for these are not saved anywhere yet; footage index above covers them.
- Stills sheets: `build/render/shots3_stills*.jpg` (sent), `shots4_stills.jpg`, `shots5_stills.jpg`, `shots6_stills.jpg`.
- `stills.py` must run ONE job at a time (the Blender runner allows one render; it now waits with `--wait 1500`). A re-run of shots5 fixes + all of shots6 was in progress when this stopped: check the sheets, re-run if any tile is black.
- Known mistakes still open on the Barracks sheet (`shots4`): 215 first flash not visible · 219 gym bag not in frame (legs only) · 228 pages show no writing · 232 figure leaving into the trees is black.
- Open on `shots5`: 306 used the station's own caption (moved to 122.0 s), 310/311 paper blown out (lamp lowered), 332 laptop text cut off (resized): all re-rendering in the run above, not yet checked.
- Not yet done for any chapter after the cold open: rendering in motion.

## Nov 20, 2026: creator decisions and look pass
- **Pavement:** asphalt pad added along the hangar's north side; he is stopped, kneels and lies on it (matches the marshals' account). Affects cold-open shots 29-38.
- **Card wording:** creator is fine with the summary cards as written.
- **Unconfirmed photos:** creator says use them where they fit. Placed: `ca-times-brightspot.jpg` (shot 403, credited Los Angeles Times),
  `34-armored-PPO235.jpg` (439) and `7Y7YM5UU.jpg` (413). **The last two still need an outlet name for their watermark before the final render** (`credit_needed` in the plan).
- **Render quality:** raised from 1 to 16 samples at the creator's request (`rt.QUALITY`); roughly 3x slower per frame.
- **Look:** barracks lit to read at night; evidence close-ups on a concrete surface with more detail; scanned pines along the tree lines in every ground-level shot.
- **Cold open credit:** the Malkowski credit on the quote wall now finishes before the cut.
- All stills sheets predate this look pass except the test tiles in `build/render/stills/look_fix.jpg`; re-run `stills.py` per chapter before rendering it.

## Nov 20, 2026 (later): motion renders
- Cold open **v7 approved**. Hook (`frein_s2_hook.mp4`) and The Barracks (`frein_s3_barracks.mp4`) rendered in motion and sent;
  joined review file `frein_0000_0340.mp4`. Awaiting the creator's notes on both.
- Barracks set renders about 4 s/frame at 16 samples; the airfield set about 8 s/frame.
- Creator is moving to another PC: see `TRANSFER.md`.

## Nov 25, 2026: uncredited photos
- Creator's decision: `7Y7YM5UU.jpg` (shot 413) and `34-armored-PPO235.jpg` (shot 439) stay in, without a source watermark
  (outlet unknown). The only two real images in the film with no tag. Logged in `sources-used.md` rows 46–47.
