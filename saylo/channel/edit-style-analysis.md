# Edit Style Analysis — reference videos (Nov 13, 2026)

Measured with `saylo/tools/analyze_edit.py` (ffmpeg cut detection, fade/silence detection) plus frame-by-frame contact sheets.
Source files were compressed copies the creator uploaded to Google Drive (`vids` folder). The videos themselves are not stored in this repo.

## The four references
| File | Channel / video | Length |
|---|---|---|
| `compressed_luis man.mp4` | Uncovering — The 5-Day Manhunt for Luigi Mangione | 18.3 min |
| `compressed_hackers'.mp4` | Uncovering — The 9/11 Hijackers' Secret Lives in America | 32.3 min |
| `compressed_fern.mp4` | fern — Gaza journalists / media blackout investigation | 27.7 min |
| `compressed_fern religon.mp4` | fern — NAR / religion & power | 51.5 min |

Uncovering is the closest match to Saylo (same lane, same length). fern is the polish benchmark.

## Measured pacing
| | Luigi | Hijackers | fern | fern religion |
|---|---|---|---|---|
| Shots | 249 | 319 | 346 | 649 |
| Mean shot | 4.4s | 6.1s | 4.8s | 4.8s |
| Median shot | 3.5s | 3.8s | 2.7s | 2.8s |
| Cuts per minute (1st / 2nd / 3rd third) | 13.3 / 13.8 / 13.6 | 12.2 / 8.3 / 9.1 | 16.1 / 9.8 / 11.4 | 14.1 / 12.9 / 10.7 |
| Shots under 2s | 27% | 25% | 38% | 38% |
| Shots over 10s | 6% | 14% | 12% | 12% |
| Longest shot | 72s | 78s | 46s | 43s |
| Cuts in first 60s | 26 | 36 | 19 | 13 |
| Fades to black | 4 | 5 | 3 | 10 |
| Full silences (>0.6s) | 4 | 2 | 1 | 0 |

## What they all do
1. **Fastest at the hook.** Uncovering cuts every ~2s for the first minute (26–36 cuts), then settles to one cut every 4–5s. Pace often eases in the middle third and stays steady after.
2. **Mostly short shots, a few long holds.** About a third of shots are under 2s. Roughly 1 in 10 holds 10s+: emotional beats, a map being explained, or host-to-camera.
3. **Maps carry the investigation (Uncovering).** Dark teal 3D city/terrain maps, glowing streets, a route line that draws itself (red → orange → yellow), pin icons, small timestamp card in the corner ("6:44 AM", "6:54 AM"). Camera flies/tilts over the map between pins.
4. **Documents get a push-in + highlight (fern).** Slow zoom into an article, letter or court document; an orange/red bar sweeps across the key line. Also used for full-screen quoted text.
5. **Name tag on first appearance.** Bold condensed caps at the bottom of the frame ("LUIGI MANGIONE", "MOHAMED ATTA", "AL-HAZMI" with hand-drawn arrows).
6. **Archival is framed, not dropped in.** News clips get a frame, a title card, or a "BREAKING NEWS" style lower third; deposition/interview clips keep their timecode; multi-clip grids for "the media went wild" moments.
7. **Recreations instead of missing footage.** Uncovering and fern use 3D animated recreations (labeled "all our animations are made by humans"). Saylo substitute: AI/3D stills with a slow push or parallax, maps, documents and real photos.
8. **Fades to black are rare** (3–10 per video) — chapter breaks only.
9. **Music almost never stops** (0–4 full silences per video). A silent hold is the strongest tool you have; use it once or twice.
10. **Uncovering's host** appears on location (handheld walk-and-talk at the real spots) and at a mic in a dark room. fern uses expert interviews as a second voice every few minutes. Saylo is voice-only, so the second voice = real 911 audio, press conferences, court/news clips.
11. **Chapter cards** — title-style text over a dark scene (fern: "Roots"; Uncovering: newspaper-style title "The 9/11 Hijackers' Secret Lives in America").
12. **Color:** dark, desaturated, teal/blue shadows; one warm accent (orange/red) for routes, highlights and key details. Matches Saylo's amber accent.

## Saylo editing rules (derived)
Copied into `style-sheet.md` §8 — that file is the source of truth.
