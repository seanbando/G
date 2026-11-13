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
