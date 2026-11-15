# 01 Olympic Bomber: PROGRESS (handoff, Nov 15, 2026)

Start a new chat with: **"Continue the Olympic Bomber video. Read saylo/videos/01-olympic-bomber/PROGRESS.md and saylo/style-sheet.md first."**
Branch: `claude/inspiring-meitner-514uac` (repo seanbando/G).

## Hard rules (creator)
1. **100% rule:** the picture always shows what the narration says at that exact moment. Cut on word timestamps from `vo-words.json` (find a phrase: `python3 saylo/tools/words.py vo-words.json "the man bolts"`). Never put a clip under a line it wasn't made for.
2. Use every scene/clip the creator made, on the line it was made for (`make-these-clips.md` says which line each is for).
3. Real news footage first; real photos of real people are never animated or AI-faked; AI recreations are faceless.
4. The look the creator approved = the 36 s "style test": Template Library effects (case board, press stack, film window, photo timeline, clock badge, maps, archive profiles) carry stills; plain photo push-ins only as quick cutaways. Every text types on (typewriter + clicks).

## Done
- Script (`script.md`), voiceover "Saylo new" voice, clean continuous 18:04 (`voiceover-full.mp3`), word timings (`vo-words.json`).
- Music beds A–D + 26 SFX (`sound/`), mixed via `saylo/tools/assemble.py` (ducking, -14 LUFS).
- Tools: `assemble.py` (plan → video; segment types: src clip/photo, card, number, stack, effect, tag), `make_card.py` (typewriter cards, lower thirds, number build, photo stack), `edit_video.py` (whip/zoomthru/flash/shake/punch), `build_cues.py`, `words.py`.
- Template Library effects engine works in the cloud: set `SAYLO_EFFECTS` to the extracted kit's `.claude/effects` (zip `Faceless-Studio-3-Template-Library (2).zip` in the creator's clips Drive folder `1Fy8dWKIESHpuzA-0k2UOienNl1jLchVN`; run `npm install` there). Blender (Documentary Pro) can't run in the cloud.
- Real footage cut and cleaned: AP Oct 28 1996 press conference (36b, 36c, 37b, 30b) and Retro Report (23e, 26c, 27b, 27c, 29b, 30j, 36d): see `research/clip-cuts.md`. AJC archive photo pack (24 photos) + Commons photos: `assets/SOURCES*.md`.
- Part 1 render (cold open + The Park, 0:00–4:00) reviewed by the creator.

## Fix before continuing (creator feedback on part 1)
- **Re-cut the cold open and The Park on word timings.** Key word times (cold open): "a mountain town" 6.54 · "the occasional patrol car" 12.36 → `K clip` · "His name is Jeff Postell" 17.38 → `04 postell clip` + lower third · "swings around behind" 21.92 → `05 save a lot clip` · "with his lights off" 24.28 → `L02 savealot backlot` · "he spots a man crouched" 25.66 → `A clip` (flashlight on crouched man) · "The man bolts" 30.68 / "then gives up" 31.80 → **L clip** (running, slips, hands up), NOT the I (dumpster raid) clip · "He says his name" 35.74 → Jerry Wilson card · "It's a lie" 41.98 · "the man standing in that parking lot" 47.02 → A clip · "Ten Most Wanted" 50.10 → poster · "Helicopters with heat cameras" 53.86 → J clip · "At one point… 200 federal agents" 58.28 → number build **200+ FEDERAL AGENTS** (not $1,000,000) · "His real name was Eric Rudolph" 63.62 → rudolph clip + lower third · "after a bomb went off" 67.54 → 23e live TV · "the FBI had spent… 88 days chasing someone else" 70.14 → 30b media scrum · "So why was he" 74.68 → title card · "the guard who'd helped save" 86.20 → 26c Jewell CNN · "Then for a year and a half" 92.06 → "2 · NO NAME" card · "built for hiding" 99.10 → "3" card over L05/Nantahala · "I'm working from court records" 100.62 → sources card.
- **I clip (dumpster raid)** goes ONLY under "at night, when the town was asleep, he'd come down and go through the trash" (Five Years chapter).
- Use the creator's animated location clips wherever their line comes up (L02, L03, L07–L10 uploaded; K, M uploaded).
- M clip: only first ~2.5 s (later frames look like an explosion). L10: only first ~3 s (smoke).

## Creator's location/scene clips: Drive file IDs (clips folder; generator names → our names)
Download: `curl -sSL -o NAME "https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t"`
| Our name | Drive title | ID | Use on |
|---|---|---|---|
| L clip | Man_stops_and_raises_hands… | 1zbnGqG5OuHQRTm2QhmDtuY6mu9jmvRK9 | "The man bolts… then gives up" (runs, slips, stands, hands up) |
| K2 police car | Police_car_driving_down_street… | 17h3oBZ7IWIFpeJGiTApBmxn8v-ox8WW- | drives forward, red/blue lights ON: use after the arrest / "second car" beats, not "lights off" |
| L05 nantahala | Fog_rolling_over_mountain_ridges… | 1qn9IGWXDzJODqkmANNM0jIL_gfaZCZH- | "half a million acres of mountain", "built for hiding" |
| L06 hidden camp | Tarp_shelter_overlooking_town_li… | 1K-XCBhiVgB1dFrS53A4L3O37odnxDgLR | "hidden camps… close enough to look down on Murphy" |
| L11 andrews | Flag_moves_on_street… (gas station + task-force trailers) | 1SovibaL4CjjABRACxuEi-KaxjMQTslsl | "The task force sets up in Andrews" |
| K clip | k clip.mp4 | 1mp6oK3ZJg3Dk3U6pGFM87aUlBVrmCQ4J | "the occasional patrol car" |
| M clip | m clip.mp4 | 1Rfk5txP_idyyZKH1k0ewbo3hHUDlZvj0 | park crowd (first 2.5 s only) |
| L02 savealot | Rain_falling_near_dumpsters… | 126U2U5JDdDYvzeI-Kg2Dh8Y6oVmZq_FW | "behind the Save-A-Lot" |
| L03 olympic park | Crowd_swaying_at_summer_concert… | 1rcUfHv7i0rCv8ayBEXFfdfPtE0LkO7Q3 | "Centennial Olympic Park was where you went" |
| L07 apartment media | TV_vans_and_satellite_dishes… | 15i0VGp2wfHwC-_WcLKJbUvhAlU1d7crs | "reporters camped outside his mother's apartment" |
| L08 sandy springs | Approaching_building_entrance_wi… | 14fAclV-9FZ_oYG5HTcD1hSNATW2PJs2b | Sandy Springs, Jan 16 1997 |
| L09 otherside | Police_lights_pulse_on_wall… | 1hlEDhMojCPzYYW_htJw5iR52S1bISteZ | Otherside Lounge |
| L10 birmingham | Approaching_clinic_door… | 1o_Kzjm76jm-eIfe3s6lOMdMPHw5tEh0I | Birmingham clinic (first 3 s only) |

Still no clip (don't ask again; use the AI still with push-in + fog/flicker): `L01 murphy street` (loc-murphy-street), `L04 payphone` (loc-payphone-1996). `N clip` → real Jewell photo in a film window (no animation). Clips 16–30 (O…AD) not made yet (Google credits ran out; Higgsfield trial doesn't cover video; Kling free daily credits are the option). Ready batch: `build/higgsfield_batch_16_30.json`.

## Next after the fixes
Build The Wrong Man → Same Hands → Birmingham → Who He Was → The Hunt → Five Years → The Stop → The Deal → What It Actually Was → Outro, chapter by chapter, sending each for review. Plans live in `build/plan_*.py`; render with `assemble.py` then `edit_video.py`.
