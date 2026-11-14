# Part 1 — Voice Direction

Use with `voiceover-part1a-tts.txt` (cold open → end of The Wrong Man) and `voiceover-part1b-tts.txt` (Same Hands → end of Part 1). Numbers are spelled out for the voice; the wording is otherwise identical to the approved script, except "1 a.m." now reads "one in the morning" — this sheet says *how* each section should sound.

## Saylo baseline
- **Who:** a calm investigator telling a friend something that still bothers him. Not an announcer, not a horror narrator.
- **Pace:** ~150 wpm baseline (slower than Uncovering/fern at ~165, faster than Nexpo at ~125). Range 140–165 by section.
- **Pitch:** low-mid, relaxed. Sentences land *down* at the end. No upward "YouTube voice" lilt.
- **Energy scale (1–5):** never above 4. The scariest lines are delivered the quietest.
- **Silence is the main effect.** Pauses below are added in the edit (most reliable), not by the voice tool.
- **Music:** low bed under scenes; cut it completely at the four ★ moments.

## Pronunciations to test first
Nantahala = nan-tuh-HAY-luh · Uzunyol = oo-ZOON-yol · Bobi = BOB-ee · Piedmont = PEED-mont · Postell = poh-STELL (verify) · Murphy, Topton, Merritt Island as written.
If the voice gets one wrong, respell it phonetically in the TTS file for that line only.

## Section map
| Section | Energy | Pace | Emotion |
|---|---|---|---|
| Cold open (Murphy, 2003) | 2 | slow, 140 | hushed, close-mic, curious |
| The promise (three reasons) | 3 | normal, 150 | direct to viewer, a little intrigue |
| Sources line | 2 | quick, 160 | matter-of-fact, almost an aside |
| The Park — setup | 3 | normal, 155 | warm, summer-night nostalgia |
| The Park — backpack → blast | 3→4 | builds to 165 | tension, then flat and still |
| The Park — victims | 1 | slowest, 135 | quiet respect, no drama |
| The Park — hero → headline | 3 | 150 | dry irony on the last line |
| The Wrong Man | 3 | 150 | controlled frustration, never angry |
| Phone records | 3 | deliberate, 140 | precise, like laying out evidence |
| Same Hands | 3 | brisk, 160 | reportorial, cold |
| Birmingham | 2→3 | 145 | grave, then lean-in curiosity |
| Who He Was | 2 | 150 | neutral documentary, softening at the end |

## Beat-by-beat
**Cold open**
- "Three thirty in the morning." → pause 0.8s after each of the first three sentences (time, date, place). Match the timestamp card.
- "Thin, clean-shaven, polite." → light, even, like reading a description.
- "It's a lie, and a pretty good one." → small dry smile in the voice. Pause 1s after.
- "His real name was Eric Rudolph." → slower, lower. Pause 1.2s.
- Three reasons → count them with the voice: slight lift on "first", "Then", "And once he finally did".

**The Park**
- Open warmer than anything else in Part 1 — this is the last normal moment.
- "you try telling a crowd at one in the morning to leave a concert because of a bag" → a touch of humor; it humanizes Jewell.
- "He said thirty minutes. It went off at about one twenty." → ★ two flat sentences, 1.2s pause between them. Music out.
- "There's a detail hiding in that phone call…" → drop to a near-aside, conspiratorial. This is a hook; don't oversell it.
- Victims paragraph → slowest pace of the video. Pause 0.8s after "Alice Hawthorne, forty-four, from Albany, Georgia." No emphasis on "killed" — let it sit plain.
- "For three days, Richard Jewell was a hero." → warm. Then "the headline said…" → dry, a little disbelief. Pause 1.5s at the section end.

**The Wrong Man**
- "Suspicion isn't evidence, though." → firm, slower, slight emphasis on *evidence*.
- "Didn't matter." → clipped, flat. 0.6s pause after.
- Bobi Jewell paragraph → softer, empathetic. "Picture that" is a real invitation, not a slogan.
- "one detail from it still gets me" → genuinely personal, slightly lower.
- "And the thing that should've cleared him was sitting there the whole time." → ★ lean in, slow. Music out. Pause 1s.
- "Twelve fifty-seven… twelve fifty-eight" → space the numbers out; each timestamp gets its own breath.
- "One minute." → ★ alone, quiet. 1.2s pause after.
- "It needed a clock and a map." → land it down. Pause 1s.
- "That's the first reason he was so hard to catch." → conversational check-in, a little lighter.
- "And the real bomber wasn't finished." → low, ominous, slow. Pause 1.5s, section break.

**Same Hands**
- Brisk and factual — this section moves fast by design.
- "That second one was for them." → ★ cold, slow, quiet. Pause 1s.
- "the same trick" → slight bitterness.

**Birmingham**
- Sanderson and Lyons → grave, unhurried. No dramatic pause after "He's killed." — just a normal sentence break; the plainness is the point.
- "And then something happens that hadn't happened at any of the other scenes." → lean in, slower. Pause 0.8s.
- "He was walking away from it. Not fast." → curious, almost puzzled. "Just strolling off like he'd finished an errand" → the strangeness should be audible.
- "and grabbed a pen" → tiny smile; it's the human-scale win.
- "Eric. Robert. Rudolph." → say the full name deliberately (the TTS file keeps it as one line; add 0.3s gaps in the edit if needed).
- "That's reason number two" → conversational check-in.

**Who He Was**
- Neutral, quicker documentary read.
- "Then he went home. Back to the woods." → softer, lower.
- "Hold onto the name of that town." → direct to the viewer, slight smile — a promise.
- "And he was just gone." → quiet. Final line of Part 1 trails into 2s of music/ambience.

## If using ElevenLabs
Generate **one file per section** (like the CashleyFinance pipeline) so each can get its own speed, and pass the neighbouring text as context so delivery flows between files.
Starting points to test, not final values: stability 0.45–0.5 (steady but not robotic), style 0.1–0.2 (Saylo is restrained), speed 0.92 baseline, 0.88 for the victims and phone-records sections, 0.98 for Same Hands. Listen to the cold open first — if it sounds like an announcer, lower style before changing anything else.

## If recording yourself
Sit back from the mic about a hand's width, speak at the volume you'd use with someone across a small table, and record each section as its own take. Read the ★ lines twice and keep the quieter take.
