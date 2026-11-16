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

## Narrator voice: "Police Found Both Boston Bombers. One Still Escaped." (Nov 14, 2026)
Measured with a numpy prosody script (syllable-rate proxy, level, pitch via autocorrelation). Rough numbers; the music bed adds noise.

| Span | Syllables/s | Level | Pitch (median) | Pitch variation |
|---|---|---|---|---|
| 0–30s | 4.33 | −24.4 dB | 91 Hz | 3.4 st |
| 30–60s | 4.37 | −23.3 dB | 101 Hz | 3.7 st |
| 60–150s | ~4.0 | −23 dB | ~103 Hz | 3.5 st |
| 150–780s | ~4.4 | −23.6 dB | ~100 Hz | 3.5–4.0 st |

**Finding:** this narrator does **not** speed up or get louder in the hook. Pace and level are flat for the whole video and match our Mike track (~4.3 syll/s). The energy comes from:
1. **A deeper, heavier voice:** ~100 Hz median pitch vs. Mike ~124 Hz. Lower and steadier, with less pitch movement (3.6 st vs. Mike 4.1 st).
2. **Wall-to-wall visuals in the hook:** CCTV with a yellow frame, location label in the corner (`MASSACHUSETTS AVENUE, CAMBRIDGE`), name tag (`SEAN COLLIER`), a recreation of the police car, a flashlight reveal of an evidence board, then a jump back to the marathon start with a date card (`15TH APRIL, MONDAY`).
3. **Music and SFX** under every line.

Closest of our 9 tested voices by pitch and steadiness: **Philip – Quiet Authority** (113 Hz, 3.2 st). All 9 are higher than this narrator.

## Retraced: "Why an ER Doctor Shot 6 People in Washington DC" (Nov 16, 2026, creator's pick: "the exact look + transitions I want")
Measured (360p copy, 10.9 min): **209 shots · mean 3.1 s · median 2.6 s · 35% under 2 s · 2% over 10 s · cuts/min 25.8 / 17.0 / 14.3 by third · 43 cuts in the first 60 s · 2 fades to black · 2 full silences.** Faster than Uncovering/fern (~13/min).

What it looks like:
- **~70% is 3D recreation** (Unreal/Blender look): real places rebuilt as clean 3D sets (street corner, gym, apartment, hallway, office), lit dark navy/gray with practical lights.
- **People are faceless mannequins.** Everyone is white/gray matte; **the subject is one glossy colored mannequin** (red) so you always know who he is. Real people are shown as **3D clay busts** (white bust, red rim light) or in real interview/press footage.
- **City/maps = 3D clay block models**: white-gray buildings, the key building lit in the accent color, a glowing route line draws across the blocks; top-down block map with a time stamp ("8:03 AM") and a timeline bar along the bottom.
- **Chapter cards are built into the 3D scene**: "CHAPTER 01 / FIFTEENTH AND P" as a green street sign on the building; "SEVEN-OH-FOUR" in big letters on the wall.
- **Date stamps**: big white bold caps top-left ("AUGUST 2024", "ABOUT 9:00 AM") over the 3D shot.
- **Quotes**: projected on a 3D wall next to the mannequin, white text with a red vertical bar on the left.
- **Connection web**: dark board, round icons (house, building, gavel, person) joined by thin white/red lines, labels, small timeline in the corner.
- **Title card**: navy background, two-line title, a red line between two points ("THE WHITE HOUSE" ─── "15TH & P STREET NW"), sources line under it.
- **Real footage**: interviews, press conferences, bodycam/news, a tweet card; always with a lower third (name + role) and burned-in subtitle line on interviews; news clips sometimes framed on a 3D wall/TV.
- **Counters as icons**: "6 SHOT" + six red person icons over the block map.

Transitions: **almost all hard cuts.** Motion comes from the 3D camera (slow dolly, orbit, crane, push through a window/door into the next room), not from editing effects. A white light flash on gunshots/impacts. Fades to black only at the 2 biggest beats. No whips, no zoom-throughs.

What Saylo can do in the cloud: every 2D piece (date stamps, quote walls, connection web, title card with route line, icon counters, lower thirds, timeline bar) plus 3D-look clips generated from text/image prompts (mannequin style) by the creator in Kling/Higgsfield. Real Blender/Unreal renders need the creator's PC.
