# Frame-by-frame analysis: reference shorts vs ours (Nov 19, 2026)

Tool: `tools/analyze_frames.py` (every frame at 30 fps: hard cuts, optical-flow camera motion, caption-band changes, color; audio loudness and hit density). Raw per-frame data in the JSON files here.
Ricks Clips not included yet (no video files in the session; YouTube downloads are blocked here). Need the creator's mp4s.

| Metric | Jensen (Afterhour-style) | Google (Afterhour-style) | Our GTA 6 | Our 3 friends | Our paycheck (Golpo) |
|---|---|---|---|---|---|
| Frames analysed | 4,484 | 3,399 | 1,463 | 1,530 | 1,993 |
| Hard cuts | 138 | 37 | 8 | 6 | 24 |
| Median shot | **0.9 s** | 1.9 s | 3.6 s | 5.5 s | 1.4 s |
| Cuts in first 5 s | **7** | 2 | 2 | 0 | 1 |
| Frames dead still | **0.4%** | **0.6%** | 55% | 39% | 31% |
| Frames camera pushing in | **39%** | **43%** | 8% | 9% | 15% |
| Caption swaps per second | 2.2 | 1.5 | (ours sit lower; not measured) | | 2.3 |
| Loudness | -12.9 LUFS | -12.1 LUFS | -14.2 | -14.2 | -14.0 |
| Audio hits per second | 1.9 | 2.6 | 2.1 | 2.1 | 2.0 |

## What they do that we don't
1. The camera NEVER stops. Under 1% of their frames are still; about 40% of frames are a slow push-in, the rest drift, pan or zoom out. Ours are still 30-55% of the time (animated objects move, but the camera sits).
2. Re-angle cuts on every phrase. Jensen keeps one set (the throne) but cuts wide -> medium -> close-up -> low angle -> back to wide on each caption phrase (7 cuts in the first 5 s). New angle = new visual without a new scene.
3. The opening shot is a wide establishing shot with the hook words already on screen ("You are Jensen"), then a cut closer at 0.5 s.
4. Props that literally show the words: newspapers "IS GOOGLE FINISHED?", a real tweet card, the logo sign. Credibility props, not text cards.
5. A bit louder: -12 to -13 LUFS (YouTube turns both down to about -14, Instagram less so).
6. Sound hits about 2 per second: we already match this.

## New targets for our edits
- Dead-still frames under 5%: every shot gets a continuous slow push (1.00 -> 1.08 over the shot), alternating with slow pull-backs.
- Re-angle cut on every caption phrase (about every 0.8-1.5 s): alternate framings wide / medium (1.3x) / close (1.6x) on the subject, not just the 7-10% reframes we use now.
- 4+ cuts or re-angles in the first 5 s (on top of the visual-hook beats).
- Master at -13 LUFS, peaks under -1 dB.
