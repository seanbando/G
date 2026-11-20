# Money Mystery: the channel's short format (chosen 2026-11-13)

Built for money explainers with maximum retention. It keeps Ricks Clips' retention mechanics (mystery up front, answer late, mid-video fake-out) but the payoff is a money concept the viewer can use, not a weird fact.

## Length and pace

Length follows the story, not a 60-second target: never pad a script to reach a minute, and cut any line that drags. The goal is viewers staying to the end. Pace stays high the whole way: every line at about 195 words a minute (`tools/auto_tempo.py`), like Ricks Clips.

## First-frame rule (from the Elon short's retention graph, 2026-11-14)

About 28% of viewers left in the first 3 seconds while the first board was still being drawn. So:
- **Frame 1 is finished and loud:** the hook scene itself, already composed and readable, with the shock number on a prop in the scene (see the visual hook rule; plain text slam cards are retired as openers, Nov 20 2026).
- **The hook line lands within 4 to 5 seconds.** Cut lists from the opening line.

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

## Idea checklist (run before scripting any idea)
1. Safe for YouTube? (no "get rich" promises, no specific buy/sell advice, finance facts sourced)
2. Is our audience (18-35 beginners) interested? Proof, not a feeling: search demand, competitor outliers, our own analytics.
3. Something they don't see every day? (skip overdone: latte factor, "rule of 72", "pay yourself first")
4. Does the viewer learn something new?
5. Strong hook? (a paradox that fits a frame-1 slam card and lands in 5 s)
6. Real payoff? (the reveal plus something they can do or check today)
7. Picked with confidence or guessing? If guessing, validate first (outlier search when vidIQ credits return, free web/forum demand checks meanwhile).

## Simple first (creator rule)
Viewers are beginners scrolling fast. Nerd-proof means never say anything false; it does NOT mean adding detail.
- Feeling first, number second: the relatable moment ("car breaks down, you're back to zero") before any math.
- At most one number per line, and only as a dollar story ("borrow $400, owe $460 two weeks later"), never a rate a beginner can't picture (skip "400% APR" in the voice; it can go on screen small).
- Everyday words only: no APR, credit mix, utilization, liquidity in the voice-over.
- If a nerd detail makes the line harder, cut the detail rather than add it; put it in the description.
- Test: could a 15-year-old repeat the line to a friend after one listen?

## Pick the hook type from the idea (the body stays the same)
The idea decides the opening; beats after the hook (YOU question, mechanism, re-hook/fake-out, payoff, question ending) stay.
| The idea is... | Hook type | Template |
|---|---|---|
| A myth people believe | Common belief -> contradict -> why | "Broke people aren't bad with money, being broke just costs more." |
| A habit that fails without one fix | Won't work -> unless | "Paying the minimum won't get you out of debt, unless..." |
| A deal or choice with a smarter option | Better way -> best way -> re-hook | "0% sounds like the best deal, but there's a better one." |
| A result YOU (or a real person) got | Results first -> what they did -> steps | "YOU paid off $5,000 in 10 months without a raise. Here's how." |
| A journey from start to goal | A -> B -> how | "From $0 saved to $1,000 in 90 days." |
| News / famous name drama (Afterhour) | Contradiction + real name + stakes | "Nvidia didn't lose a war or a customer. It lost $300B over one man." |
Track "viewed vs. swiped away" per hook type to learn which opening this audience stays for.

## RULE: one structure per video (creator rule, Nov 15 2026)
Never mix structures. Pick the ONE that fits the idea best and follow its beats only:
| Structure | Fits when the idea is... | Beats |
|---|---|---|
| Money Mystery (ours) | a money paradox about the viewer's own life (minimum payment, broke, paycheck) | paradox hook -> YOU question -> setup -> escalation -> mechanism -> fake-out -> callback lesson + question |
| Ricks Clips | a strange real story, place or system (weird things behind money, history) | strange act + stake -> "You see" -> doubters -> fake-out -> time jumps -> outcome -> mechanism last / one-line truth (no CTA) |
| Afterhour Theory | current drama with a famous name or company | contrarian hook + real name -> "But how?" -> you play the company (need -> asset) -> fast list -> twist that pulls the viewer in |
Hook types (common belief, won't work unless, better way, results first, A to B) are openings inside the chosen structure, not extra structures.
The recurring character YOU can appear in the drawings of any structure; YOU only speaks a line in Money Mystery.

## Running image must be said early (creator feedback, Nov 17 2026)
A metaphor that only appears in the drawings and then shows up in the last line feels random ("the seed that got stepped on" came out of nowhere).
- Introduce the image in the voice-over by line 3 or 4 ("Picture your paycheck as a pizza", "It's like an escalator moving down").
- Use it at least once in the middle, then flip it at the end.
- If it can't be set up naturally, drop it and end on the plain payoff.

## 14-point script check (from topicfinder.ai carousel, Nov 2026)
Already strong: 02 open loops (YOU question + fake-out), 04 progression, 05 contrarian, 08 illustrate (one running image), 09 non-obvious insights, 10 shift a belief, 12 pattern interrupt (slam card, punches), 14 pay off the promise.
Add to every script:
- 01 Clear promise: the hook says exactly what they'll get ("one had over 10x as much", not "here's a crazy story").
- 06 Call out the viewer in line 1 or 2 when it fits ("If you've ever paid the minimum...", "If you're 22 with $1,000...").
- 07 Name the mechanism: give the lesson a short repeatable name ("the shoebox mistake", "key person risk", "escape velocity").
- 11 Stack proof: one on-screen proof tag ("Real S&P 500 returns 2006-2025", "Source: Federal Reserve") so viewers trust the numbers.
- 13 Shared enemy (fair, nerd-proof): fees, the minimum-payment trap, panic selling. Never a named company or person without facts.
- 14+ Overdeliver: one bonus the viewer didn't expect (the statement warning box, "even coming back late cost Maya $1,700").
- Roadmap (03) only for list videos ("3 things..."); stories use the cast/setup as the roadmap.

## RULE: visual hook + verbal hook (creator rule, Nov 18 2026)
The first 5 seconds need a VISUAL hook as strong as the spoken one. Never hold one frame in the hook.
- Something new appears on screen on every key word of the hook line (about every 0.5-1 s): a new object, a number slam, a scene swap.
- Each beat illustrates the exact word being said (e.g. "tomorrow" -> calendar NOV 19, "millions" -> crowd floods the screen, "buy the game" -> controller + money, "own" -> building rises + OWN stamp).
- Add a cut, punch or whoosh on each beat.
- Frame 1 is the hook SCENE itself, not a text card (creator rule, Nov 20 2026): the first frame is a finished, readable 3D shot already acting out the hook line (the character, the object, the stakes), with at most a small number on a prop. The visuals then act out the hook word by word. A plain full-screen text slam card is no longer the opener.
- After the hook: no still frame longer than about 1.5 s anywhere in the video.

## RULE: measure every word's timing (creator rule, Nov 18 2026)
Estimated word times drift by up to ~1 s (the "Millions" visual landed a full second early on the GTA short).
- After the final voiceover is built, run `tools/stt_words.py <script.md> <track.mp3> <words.json>` (ElevenLabs speech-to-text, word timestamps; small credit cost, reused from cache on reruns).
- Every visual beat, punch, sound effect and caption is cued from those measured times. Captions snap to the real start of the matching spoken word (`tools/make_captions.py`).
- tools/word_times.py is only a free fallback for previews.

## RULE: the camera never sits still (from the 30 fps reference analysis, Nov 19 2026)
Reference shorts have under 1% still frames; ours had 39-55%. Every edit now runs `tools/auto_camera.py`:
- a new framing on every caption phrase (wide / medium / close, aimed at the content so nothing is cropped),
- a slow push-in or pull-back on every shot,
- `--calm` ranges keep 3D scenes and number reveals at full frame (still drifting).
Check with `tools/analyze_frames.py`: dead-still frames under 5%. Master at -13 LUFS.
