# Script Template — Story-Driven Finance Explainer (Whiteboard)

Based on Paper Billions' structure, with Stick Finance's recurring example character for concepts.

**Targets:** 2,000–3,000 words · 12–18 min · ~160 wpm · 7–9 chapters · avg sentence ≤ 10 words

## Script format conventions

```
## Chapter N: <Story-beat title>          ← a moment, not a topic label

Narration line. One idea per line.          ← narrator (main VO)
[DRAW: what appears on the whiteboard]      ← one cue per scene, 3–6 sec
**ROLE:** "Character line."                 ← a different voice; draw them with a speech bubble
```

Character roles to use: real people (quote only what they actually said), imagined people (traders, a neighbour, "you"), and personified things (the stock, the app, the chart).

---

## Chapter 1 — Cold Open (0:00–0:45, ~120 words)

1. **Shocking fact or scene in the first sentence.** A specific number, person, or place.
   - "On <day>, <who> <did/lost/made> <huge specific thing>…"
2. **A denial that deepens the mystery.** "No <expected cause>. No <other cause>."
3. **Voice burst** (2–3 short lines from characters reacting).
4. **Central question:** "So why did <thing> happen?"
5. **Short answer teaser:** "The short answer is <A>, <B>, and <C>."
6. **Rewind:** "The long answer starts <time earlier>, in <place>."

## Chapter 2 — The Setup / The Hero (1.5–3 min)

- Introduce the main character(s) with one humanising detail.
- Define the core concept with an **everyday analogy** (cake, concert tickets, sneakers, restaurant).
- Introduce a **recurring example character** if the concept needs a worked example (Stick Finance's "Maya").
- Plant the **callback line** for the first time.

## Chapters 3–4 — The Build (2–3 min each)

- Raise the stakes with **numbered items** ("Crack one… Crack two…").
- Every big number gets a **human-scale translation** ("about the price of a used couch").
- A character-voice exchange every 20–40 seconds.
- Plant one **open loop**: "Hold that thought."
- Optional soft CTA at ~40%, at a natural pause.

## Chapter 5 — The Turn (2–3 min)

- The event that tips everything. Use **time jumps** ("Tuesday, the third of November.").
- Close the open loop from Chapter 3–4.

## Chapter 6 — The Climax (2–3 min)

- **Ticking clock:** "Nine thirty. … Ten thirty-five. … Four o'clock."
- Fast lines, more voices, the biggest numbers.

## Chapter 7 — Who Gets Hurt / Your Wallet (1–2 min)

- "It's easy to think this only hurts <rich people>. It doesn't."
- Speak to the viewer directly: "If you're twenty-five… If you're sixty-two…"

## Chapter 8 — What It Means (1.5–2 min)

- "So who do you get angry at?" — answer honestly, without a cartoon villain.
- A historical parallel (one paragraph).
- The plain-English answer to the opening question.
- **2–3 takeaways for ordinary investors** (not financial advice).

## Ending (30 sec)

- Return to the opening scene or the callback line.
- One specific comment prompt (e.g. "Would you have sold? Tell me in the comments.").
- No hard sell. Disclaimer as an on-screen note.

---

## Pre-flight checklist

- [ ] First sentence contains a specific number, person, or place
- [ ] Central question asked within 30 seconds
- [ ] Every chapter title is a story beat
- [ ] A new analogy or example at least every 60 seconds
- [ ] A character voice at least every 40 seconds
- [ ] Every number over $1 million has a human-scale comparison
- [ ] Each chapter ends mid-sentence or on a question that carries into the next
- [ ] At least one open loop and one callback line
- [ ] Viewer's wallet is addressed directly
- [ ] Every fact, quote, and number checked against a source
- [ ] Read-aloud test: no sentence needs a second breath

---

## Human-sounding writing (apply to every new script)

Taken from the "Gemini content classification" notes, keeping the solid writing advice and dropping the unverified claims about YouTube.

**Do**
- Use specific details: real dates, names, places and numbers instead of general statements.
- Vary sentence length a lot. Mix very short lines with long ones; avoid a run of similar-length sentences.
- Say things plainly and take a position where the facts support one. Hedge only where something is genuinely uncertain, and say why.
- Use the words people in the niche actually use, explained the first time.
- Use real personal moments from the creator's own experience when they help.

**Don't**
- Use filler and stock AI phrasing: "delve", "furthermore", "moreover", "crucial", "leverage", "robust", "comprehensive", "in today's world", "it's important to note", "at the end of the day", "without further ado", "in the world of".
- Lean on tidy lists of three or perfectly balanced sentences.
- Repeat the same opener ("Here's…", "So here's…") more than twice in a script.
- Invent personal stories or experiences. A made-up anecdote in a finance video misleads viewers.

**Open question for each script:** whether a few short fragments are allowed in character lines. The original rules ban fragments; decide per script.

**Check before recording:**

```bash
python3 tools/check_script.py scripts/<script>.md
```
