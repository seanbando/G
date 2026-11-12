# Golpo Brief: One Man's Secret Just Cost Nvidia $300 Billion (60-second cut)

Golpo builds the visuals around the finished narration. Voice, words and pauses come from the audio; these settings steer the look and the motion.

## Narration

`audio/nvidia-300-billion-60s-TIGHT.mp3` (55 s), built with `tools/build_track.py --tight`. Golpo fetches it from the public raw GitHub link:

`https://raw.githubusercontent.com/seanbando/G/claude/festive-euler-fir0ml/audio/nvidia-300-billion-60s-TIGHT.mp3`

## Settings

| Field | Value | Why |
|---|---|---|
| `audio_clip` | the TIGHT mp3 link above | Creator's voice, Eric (YOU) and Andrew (NEWS ANCHOR) |
| `video_type` | `short` | 9:16 for Shorts |
| `timing` | `auto` | Length follows the narration |
| `visual_style` | **Sharpie** (Canvas) | Golpo's match for StrokeVideo's "Marker, colorful" |
| `pen_style` | `marker` | A marker draws each board |
| `pacing` | `fast` | One sentence per scene |
| `enable_camera_follow` | **true** | Motion: the camera zooms and pans to whatever is being drawn |
| `visual_animation_style` | `auto` | Motion: a mix of stroke-drawn and fade-in elements |
| `bg_music` | `dramatic` | Tension for reveals. Music drops are done in the editor |
| `onscreen_text_from_script_only` | `true` | No on-screen words that weren't spoken |
| `language` | `en` | |
| `is_public` | `false` | |

**Motion by default:** every future short should send `enable_camera_follow: true` and `visual_animation_style: auto`, plus the editor cues below.

## `prompt`

```
A 55-second news short for 18 to 35 year-olds new to investing. Nvidia, the chipmaker every AI runs on, lost about $300 billion in market value in one week in November 2026 after reports about CEO Jensen Huang: an alleged Chinese intelligence operation targeting him, an affair he admitted to staff, and a second relationship with someone who reports to him. The board is reportedly preparing to remove him and the stock fell about 9% in one night. The lesson is key-person risk: Huang has said he doesn't believe in succession planning. The twist: Nvidia is one of the biggest holdings in S&P 500 index funds, so ordinary investors lost money too. Allegations are unproven and no charges have been filed.
```

## `video_instructions`

```
Dark newsroom mood: black, white, Nvidia-style green and alarm red. Big readable numbers: $300 billion, 9%. Keep every scene moving: build each board in layers, use arrows, motion lines and falling or rising elements, and frame key objects large so the camera can push in on them. Recurring CEO: simple cartoon man with grey-black hair, glasses and a black leather jacket, never a realistic face. News anchor boards: TV anchor behind a desk with a red BREAKING banner. "Wait, how is that even possible?": a young guy staring at his phone, shocked. Chips: a glowing computer chip with simple AI icons, no real company logos. Scandal beats: newspaper headlines, a spy silhouette, a cracked heart, a boardroom table with an empty CEO chair. Stock drop: a red chart crashing down. "No plan B": an empty chair under a spotlight. Index fund: a basket of stocks with the green chip as one of the biggest pieces. Last line: the young guy looks at his own phone showing a red number. Draw only what the narration describes at that moment.
```

## Version 2: build-up boards (rendered 2026-11-12)

Learned from a nurse explainer that reads better: one board that keeps growing beats a new scene every sentence. Changes from version 1:

- `pacing`: `normal` (boards stay up to about 15 s and build) instead of `fast`.
- Three boards: 1 the empire (chip, viewer, CEO holding it up, "one man"), 2 the cracks (same board; each scandal beat adds a tagged icon and a crack: "alleged", "unfaithful", "board", "nine percent"), 3 you (empty spot, "no plan B", then pull back into an "index fund" basket on the viewer's phone).
- Every item: icon + rounded pill label + small effect icon. Pill words must be spoken words, because on-screen text is limited to the narration.
- Big icons that fill the vertical frame; little text.

Job: `30ec2366-1531-4025-b1b8-ceb97ec80740`. Version 1 (fast pacing, a scene per sentence): `f573bc12-ab2a-43e6-8979-f32c78109ac6`.

## Editor motion cues (times from the TIGHT track)

Golpo can't time zooms or shakes to a word, so add these in the editor.

| Time | Line | Motion |
|---|---|---|
| 0:00 | "Nvidia didn't lose a war…" | Start at 105% and drift in slowly |
| 0:05 | "three hundred billion dollars" | Quick punch-in to 115% on the number |
| 0:08.2 | YOU: "Wait, how is that even possible?" | Hard cut, small pop-in on the shocked guy |
| 0:16 | "They were buying one man." | Slow push-in on the CEO, music drops out |
| 0:18.4 | ANCHOR: "Breaking tonight…" | 2-frame white flash, light shake, music back |
| 0:25.2 to 0:35.5 | Escalation | Slow continuous zoom-in (100% to 112%) to build tension |
| 0:38 | "nine percent in a single night" | Screen shake, red flash, music drops out |
| 0:44.5 | "There's no plan B." | Snap zoom-out to the empty chair, silence |
| 0:46.6 | "Oh, and if you own…" | Reset to 100%, music back quietly |
| 0:53.3 | "You just lost money too." | Slow push-in on the phone's red number |
| 0:55.1 | End | Hard cut, no fade, so the loop restarts cleanly |

## Before posting

- Recheck the Nvidia board decision. If he has been removed, VO-06 needs a new line.
- Add the "KEY-PERSON RISK" label in the editor at about 0:41 to 0:46 (blocked in Golpo by the spoken-words-only setting).
- Description disclaimer: "Not financial advice. Based on news reports as of November 2026; allegations are unproven and no charges have been filed."
