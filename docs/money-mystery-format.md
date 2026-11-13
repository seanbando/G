# Money Mystery: the channel's short format (chosen 2026-11-13)

Built for money explainers with maximum retention. It keeps Ricks Clips' retention mechanics (mystery up front, answer late, mid-video fake-out) but the payoff is a money concept the viewer can use, not a weird fact.

## Length and pace

Length follows the story, not a 60-second target: never pad a script to reach a minute, and cut any line that drags. The goal is viewers staying to the end. Pace stays high the whole way: every line at about 195 words a minute (`tools/auto_tempo.py`), like Ricks Clips.

## Beats (typically 45 to 60 s, B voice)

| Time | Beat |
|---|---|
| 0 to 3 s | **The paradox:** a money fact that seems impossible. Don't give away how. |
| 3 to 8 s | **The viewer's question** in the YOU voice, answered by the video. |
| 8 to 18 s | **Concrete setup:** one real person or worked example, drawn. |
| 18 to 28 s | **Escalation and re-hook:** numbers climbing or falling, or a news bulletin. |
| 28 to 35 s | **The mechanism, shown before it is named.** |
| 35 to 42 s | **Fake-out:** a moment where the opposite seems true. |
| 42 to 55 s | **Callback to the opening drawings, then the lesson turned on the viewer;** end so the video loops. |

Re-hook every 8 to 10 seconds. One concept per short. Every line names one drawable thing and one motion.

## Three versions

1. **News Mystery:** big names, this week (Nvidia, Elon). Spikes fast, fades fast.
2. **Evergreen Mystery:** timeless money weirdness (scams, lottery and gambling mechanisms, market history). Gets views for months.
3. **Money Ladder:** the same amount, 3 or 4 levels, each bigger, with the fake-out on the last level. Under 60 s, every level drawn, no stereotypes.

## Workflow

1. Script, approved by the creator.
2. Voiceover with the B recipe (`docs/voiceover-recipe.md`), which gives exact word timings.
3. Storyboard, board by board, timed to the voiceover (layout, draw order, motion, on-screen text, camera, transition in and out, sound, hook or payoff). Approved before any Golpo credits.
4. Golpo render from the storyboard.
5. Edit with `tools/edit_short.py`, sound effects with `tools/build_sfx.py`, frozen-spot check, captions and cover.

After each short has been up 24 to 48 hours, compare its YouTube retention graph against these beats and adjust.

## On-screen numbers rule (creator, 2026-11-13; all videos, long and short)

Every amount of money or percentage that appears on screen (drawings, labels, captions, covers) is written with digits and its symbol:

- Money always has **$ in front**: $300, $12,000, $406,000, $80 billion, $113 billion. Large round amounts may use a word for the unit ("$80 billion"), never "eighty billion dollars".
- Percentages always end in **%**: 9%, 4%, 10%, 11%.
- Never spell numbers out on screen. (The voice-over script still writes numbers in words so the voice reads them correctly; this rule is only for what viewers see.)

How it is applied:
- **Golpo:** every `video_instructions` includes: "Write every amount on screen with digits: money with $ in front (e.g. $406,000) and percentages with % (e.g. 10%); never spell numbers out." Scene descriptions quote amounts in that form.
- **Captions:** after the word timestamps, spelled-out numbers are converted to digits with $ or % before the .srt is written.
- **Frame check:** the frame-by-frame review of each render also checks that every drawn amount follows this rule; a wrong one is patched or flagged.

## Golpo lessons (2026-11-13, friend-who-quit render)

- **`onscreen_text_from_script_only` blocks the numbers rule.** With it on, Golpo only writes words from the narration transcript, so "$48,000" and "4%" were not drawn. For future renders set it to **false** and list the exact labels in `video_instructions` ("Only these words may appear: ..."), each amount with $ or %.
- **Golpo does not keep characters identical across scenes**, even with detailed descriptions. When a callback needs the same characters, reuse the opening board's frames in the edit (as with the Nvidia RESIGNED patch), or use Golpo's character reference features only with the creator's green light.
- Any missing or wrong on-screen number can be added or covered in the edit with a marker-style overlay at the word's timestamp, at no credit cost.

## Editing tools added 2026-11-13 (from the Jensen and Google reference shorts)

- `tools/word_times.py`: free word timings from the clips (`--tight --fit <track>`); use ElevenLabs speech-to-text only with the creator's green light.
- `tools/auto_punch.py`: punch-ins on every money amount and percentage, plus a reframe (jump-cut feel) about every 1.6 s; merge with the hand-placed transitions and drop any that land inside a transition or card.
- `tools/edit_short.py` new cues: `reframe <0|1|2>` and `card <seconds> <red|green|black> <text>` (full-screen number card in the Permanent Marker font, `assets/fonts/`, Apache 2.0). Use a card for the single biggest number, written in full ($113,000,000,000).
- `tools/make_captions.py`: captions from a `display.txt` with on-screen numbers ($, %), 2 to 3 words each.
- `tools/burn_captions.py`: **the very last step**, after every edit, so captions never interfere with drawings or effects. Low on the frame (74% height), white with a black outline, a quick pop.
- StrokeVideo: one board per paragraph of the exact-words text, so the storyboard's boards are set by how the paragraphs are split (see `scripts/shorts/05-first-paycheck/strokevideo-kit.md`).
