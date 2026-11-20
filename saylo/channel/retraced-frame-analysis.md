# Retraced, frame by frame (Nov 19, 2026)

"Why an ER Doctor Shot 6 People in Washington DC" (https://youtu.be/Z9aLq9Ok108), the creator's 360p copy, **all 19,659 frames at 30 fps**.
Tool: `python saylo/tools/analyze_frames.py <work_dir>` (every frame diffed against the one before, cuts found as single-frame spikes, camera move per shot from tracked features). Per-shot data: `saylo/channel/reference/retraced-shots.json` (230 rows: start/end frame, length, how the shot is entered, push/pan/tilt speed). Shot sheets (first / middle / last frame of every shot) are in `saylo/videos/02-frein/media/ref/sheets/` (not in git). Every one of the 230 shots was looked at.

## 1. The numbers
| | |
|---|---|
| Length | 10:55 (655.3 s) |
| Shots | 230 detected (about 225 real ones: the gunshot flashes split a few shots) |
| Shot length | mean 2.85 s, median 2.45 s; 42 under 1 s, 88 under 2 s, 16 over 6 s, longest 11.9 s |
| First 60 s | 46 cuts, median shot **1.13 s** |
| After the first minute | 15 to 22 cuts a minute, median 2.5 to 4.0 s, steady to the end |
| Transitions | **227 of 229 are hard cuts.** 1 fade through black (1.2 s, into the next-video teaser at 10:15). 1 fade out at the very end. **No dissolves, no wipes, no whips, no zoom-through effects.** |
| Silence | 2 short ones (0.87 s at 8:46 before the police entry, and the end) |

**What is on screen (share of running time):** 3D recreation 59% (152 shots) · real footage, photos, tweets, headlines 29% (59 shots) · connection-web / title / end graphics 8% (11 shots) · clay block maps 5% (8 shots).
Real footage comes back every **5 shots** on average (longest stretch without it: 14 shots). In the first minute 14 of 47 shots are real.

## 2. The camera never sits still in 3D
Of the 152 3D shots: **126 push in, 10 pull out, 15 are locked off.** So 9 out of 10 3D shots are a forward move.
- Speed: median **7% of the frame per second**, middle half 4% to 17%. That is a visible dolly, not a drift. (My rejected test moved about 1% a second: it read as stills.)
- Short shots move faster: the 0.5 to 1 s shots in the hook push 5 to 30% a second.
- Real footage is treated more gently: 28 of 59 clips get a slow push (median 2% a second), 22 are left alone (interviews, press conferences).
- Locked-off 3D shots are the exception and are used for a reason: the door while it is being shot, a mannequin walking toward a fixed camera, a quote appearing.

**Four kinds of move, in order of how often they appear**
1. **Straight push** toward the subject or object (most shots).
2. **Push with a small sideways slide or rise** (orbit feel), usually on people and rooms.
3. **Fly-in that lands on something**: starts wide, accelerates, ends tight on a sign, a phone screen, a notepad, a document. 12 of the 16 longest shots are this move. The landing frame is where the text is.
4. **Travel through the building**: the camera goes up the outside of the block and over the roof to the figure (shot 48, 8.0 s), or from the roof down through floors and rooms to an object (shot 72, 11.9 s; shot 119, 9.4 s). One continuous move replaces what would be four cuts.

## 3. How shots are strung together
- **One place, several angles, quick.** A moment is covered by 2 to 4 short shots inside the same set before leaving it: wide of the gym with the red figure (0.97 s) → from between the treadmills (0.83 s) → same angle, muzzle flash (0.70 s). The set is built once and shot from several sides.
- **Real → 3D → real.** A real clip states the fact, the 3D shows what the camera never saw, then a real clip confirms it.
- **Object close-ups carry the story.** Phone on the desk, the intercom, a sign-in sheet, a book, a calendar, a notepad, a stamp on a court paper. About 1 in 5 3D shots is a single object, lit and pushed in on.
- **Rhythm run.** 41.0 to 43.5 s: six shots of exactly **15 frames (0.5 s) each**, back to back, on the beat, then the title card holds 4.0 s. Fast run, then a long hold.
- **Long holds are earned.** Every shot over 6 s is either a travelling camera move, a real interview, a map being explained, or the connection web building.

## 4. The "flash" is light in the scene, not an edit
Gunshots (door 704 at 16.0 s and 195.4 s, the gym at 112.8 s, the balcony at 148.4 s): a white bloom **inside the 3D shot**, full strength for 2 frames, gone by frame 5 or 6, on a locked camera. Bullet holes and wood chips appear with it. No cut, no full-screen white frame.

## 5. Chapter cards (5 of them: 0:47, 2:01, 4:27, 5:44, 8:30)
Same recipe every time, one shot of about 4.4 s:
1. establishing view of the place, slow drift, about 1.3 s;
2. a very fast move with motion blur (4 to 5 frames) onto a surface in the set;
3. the card is on that surface: a street sign, lettering on a brick wall, a mouldy wall, a court paper, a clock face;
4. it builds over about 6 frames: small "CHAPTER 01" plate, then the title lines, then a red underline draws;
5. hold about 2.5 s, hard cut out.

## 6. Text
| Kind | Look | How it arrives |
|---|---|---|
| Date / time stamp | top-left, white bold caps (Montserrat-like), tiny second line under it | on within a few frames of the shot starting, stays for the shot |
| Name tag | small white box, black bold caps; one small line under it for the role | pops on about 1 s into the shot |
| Place label | same white box, pinned to the building or map block | pops on |
| Quote | on a wall of the set, in perspective, white, red bar on the left, small source line under it | **one line at a time**, each line with the narration (3 lines over 4.3 s) |
| Interview subtitle | small white text on a dark strip, bottom centre | per phrase |
| Source credit | tiny, bottom-right, on every real clip | static |
| Counters | "6 SHOT" + six red figures over the block map; money totals inside the connection web | builds item by item |
Text is always tied to a surface or pinned to a thing. It is never a full-screen card except the title.

## 7. What the 3D actually looks like
- **Sets are finished rooms and streets**, not shapes: brick with mortar, glass that reflects, ceiling strip lights, furniture, treadmills with screens, a fireplace with flame, traffic lights, autumn trees. Colour is natural (orange walls, green turf, red brick). Only the people are colourless.
- **Lighting is strong and motivated**: daylight through big windows, rows of ceiling lights, a desk lamp, a fire. Interiors are bright with dark corners, not uniformly dim. Night scenes have pools of light.
- **Mannequins** are smooth chrome-grey or white with visible joints at shoulders, elbows, hips and knees, **dressed in simple coloured clothes** (shorts, tops, vests, hard hats), posed mid-action and often moving (running on treadmills, walking, falling, raising hands). The subject is glossy red, always, and is the only red thing in the room besides practical lights.
- **Police / tactical mannequins**: grey bodies, dark fitted vest and helmet, stacked in a line in a corridor.
- **Real people** = white clay bust with a red rim light on black (shots 24, 25, 210), or real footage.
- **Depth of field** on close-ups, clean and noise-free image, motion blur only on the fast moves.

## 8. Maps and graphics
- **Clay block map**: grey extruded city blocks, white street names on the roads, the key building white with a red outline, a red route line that draws, time top-left ("8:03 AM"), a timeline bar along the bottom with marked times, red label boxes ("ACTIVE SHOOTER", "BARRICADE"). Camera pushes in or pulls out, never static.
- **Cutaway model**: the building as shelves of rooms with one unit red; a single room lifted out as a dollhouse.
- **Connection web**: dark board, round icon nodes, thin white and red lines, the subject's photo in a red ring, a date and progress bar bottom-left; it grows by one node per fact and the camera slides to the new node.
- **Title card** (43.5 s, 4.0 s): navy, two lines of white caps typed one after the other, a red line drawn between two labelled points, sources line under it.

## 9. Structure of the 10:55
| Time | What |
|---|---|
| 0:00–0:41 | Hook: real scene footage and 3D alternating, shots of 0.5 to 2 s |
| 0:41–0:43.5 | Six 0.5 s teaser shots of what is coming |
| 0:43.5–0:47.5 | Title card |
| 0:47.5 | Chapter 01 on a street sign; then the place is established with labels and a block map |
| 2:01 / 4:27 / 5:44 / 8:30 | Chapters 02 to 05, each in the set |
| 8:46 | The only real silence, before the police go in |
| 10:15 | Fade through black |
| 10:16–10:44 | Teaser for the next video, in the same 3D language |
| 10:44–10:55 | End card |

## 10. What this means for Saylo (rules to build by)
1. **Hard cuts only.** One fade through black allowed, near the end. No transition effects at all.
2. **Every 3D shot moves forward** 4 to 17% of the frame per second; faster on shots under 1 s. Lock the camera only for an impact or a quote.
3. **Build each place once, shoot it 3 to 4 times** from different sides in quick succession.
4. **One travelling shot per chapter** that crosses the set and lands on the chapter lettering or the key object (4 to 10 s).
5. **Hook = 45+ cuts in 60 s**, median about 1.1 s, a third of them real footage; end it with a run of 0.5 s shots and then hold the title.
6. **After the hook: 15 to 22 cuts a minute**, real footage every 5 shots.
7. **Object close-ups** for facts (the thing itself, lit, pushed in on).
8. **Text lives on a surface in the set**, appears in a few frames, quotes line by line with the voice. (Saylo's own rule adds the typewriter reveal on top.)
9. **Sets need real materials, real light sources and natural colour**; the people are the only clay.
10. **Impacts are a 2-frame bloom of light in the scene.** Nobody is shown being hit (Saylo rule), the light is enough.

## 11. Where my first Frein test broke these
| Retraced | My rejected test |
|---|---|
| 9 in 10 3D shots push in at about 7% a second | every shot drifted about 1% a second |
| sets with materials, colour and practical lights | grey shapes in a flat navy wash |
| 46 cuts in the first 60 s, 0.5 to 2 s each | 22 cuts in 53 s, 1.3 to 3.4 s each |
| a moment covered from 3 to 4 angles | one angle per line |
| object close-ups | none |
| text on surfaces in the set | text stuck on the lens only |
| travelling shot onto the chapter lettering | none |
