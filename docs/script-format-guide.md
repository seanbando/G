# Script Format Guide (money, investing, stock market)

Adapted from the creator's "Pure Millionaires" format guide. Use the **format** for rewrites and new money explainers; the video ideas in the original are examples, not topics we have to copy. Where this guide and `docs/script-system.md` disagree, see "How this fits with the script system" at the bottom.

---

## 1. The ten rules

1. **Picture before words.** Every idea starts as something you can see (a scale, a leaky bucket, a snowball), then the narrator names it.
2. **Plain words first, then the term.** "A tiny slice of a company. That slice is called a share."
3. **Example before real numbers.** Build the main idea once with made-up round numbers on a card stamped EXAMPLE · MADE-UP NUMBERS, then switch to the real data.
4. **One fact per line.** Each line is one sentence of 8–14 words, about 4–6 s spoken, with a new picture or a big change per line.
5. **Three promises in the hook,** each closed out loud later ("Promise one, done.").
6. **Two checkpoints:** a short recap halfway through, and one right before the big reveal.
7. **Each lesson is a picture metaphor** that comes back every time the lesson is mentioned.
8. **Mascots joke, they never teach.** Buck (cocky dollar bill) and Hamlet (grumpy piggy bank) trade one-sentence gags. Hamlet's payoff lands on the saving or investing habit.
9. **One device holds the whole video together:** a scale, a ruler or a receipt wall. Show it the same way every time.
10. **Fixed ending:** a callback to the opening picture, then the next video, a comment prompt and a like line.

## 2. Voice and TTS rules

- Write full sentences only. No rhetorical questions, ellipses or fragments, because the AI voice reads them badly.
- One quiz question is allowed, and it is answered in the very next line.
- Target speed is about 180 wpm, so a 2,500-word script runs about 14 minutes.
- Voices (ElevenLabs):
  - NARRATOR: Yaboy (`eAE1ARfBOYNmMW3Ma9aS`)
  - BUCK: Larry (`fIGaHjfrR8KmMy0vGEVJ`)
  - HAMLET: Grampa Werthers (`MKlLqCItoCkvdhrxgtLv`)
- After recording, trim every silence and stutter, and check each line before using it.

## 3. Facts and money-content rules (investing videos)

- **Every number gets a source.** Write it in a fact-check table: line · claim · source URL · ✅. Unverified facts don't go in the script.
- **On-screen source tag** on every real-data shot (small grey text, bottom-left).
- **Not advice.** Explain how things work; never tell the viewer what to buy. Never say "buy X", "this will go up" or "guaranteed".
- **Returns are history, not a promise.** When showing growth, say "in the past" and show a down year too (2008, 2020 or 2022).
- **Use real, checkable data:**
  - Market history: index-provider data, Federal Reserve (FRED)
  - Inflation: Bureau of Labor Statistics (CPI)
  - Accounts and rules: SEC Investor.gov and the IRS
- **End-screen line:** "Not financial advice. For education only."

## 4. Beat map template (about 14 min)

| Time | Beat | What happens |
|---|---|---|
| 0:00 | HOOK | A strange picture, then the question, then three promises |
| 1:00 | THE DEVICE | Build the main tool from scratch using the EXAMPLE card |
| 2:30 | ACT 1 | First real case and lesson 1 |
| 4:30 | ACT 2 | Second case and lesson 2 |
| 6:30 | CHECKPOINT 1 | Three short recap lines, one per lesson so far |
| 7:00 | ACT 3 | The twist or the thing most people get wrong, then lesson 3 |
| 9:30 | ACT 4 | Today: what it looks like now |
| 11:30 | CHECKPOINT 2 + REVEAL | Recap, the quiz line and its answer, then the big number (promise one closed) |
| 12:30 | HABITS | Three habits worth stealing (promise three closed) |
| 13:30 | ENDING | Callback, next video, comment prompt, like line |

## 5. Line format (copy exactly)

**S012 · NARRATOR · ~5 s**
The spoken line goes here, one sentence, 8 to 14 words.
[DRAW: what's on screen. + an extra cut mid-line. [BUBBLE: a character: an icon or 1–3 words.]]

**S013 · BUCK · ~3 s · gag**
One short joke line.
[DRAW: Buck pops up with his clipboard.]

- Number scenes S001, S002, and so on. The tag after the time can be HOOK, PROMISE 1, CHECKPOINT 1 or gag.
- Silent [BUBBLE] cues only show an emotion or something that really happened, never invented dialogue for a real person.

## 6. Ready-made devices for investing topics

| Topic | Device (picture) | EXAMPLE numbers |
|---|---|---|
| Compound interest | A snowball rolling downhill, getting bigger each year | $1,000 at 10% a year, years 1 to 3 |
| What a stock is | A pizza cut into slices, each slice is a share | A $100 pizza in 100 slices |
| Index fund | A shopping basket holding one slice of every company | 500 slices in one basket |
| Diversification | Eggs in one basket versus eggs spread over many | One basket drops |
| Inflation | A shrinking candy bar at the same price | $1 buys less each year |
| Fees | A small leak in a water tank over 30 years | 1% versus 0.1% |
| Market crash | A roller coaster: the drop, then the climb back | A made-up dip and recovery |
| Emergency fund | An umbrella or cushion | 3 months of bills |

## 7. Hook template (example: "How the stock market actually works")

S001 NARRATOR: Every morning, millions of people buy tiny pieces of companies they will never visit.
S002 NARRATOR: Some of them get rich slowly, and some lose money fast.
S003 NARRATOR: This video builds the stock market from scratch, starting with one pizza.
S004 BUCK (gag): I was told there would be pizza.
S005 NARRATOR (PROMISE 1): By the end, you'll know what a share really is.
S006 NARRATOR (PROMISE 2): You'll see why most professionals lose to a simple basket.
S007 HAMLET (gag): Anything that keeps me full, I support.
S008 NARRATOR (PROMISE 3): And you'll get three habits that matter more than picking stocks.

(Promise 2's claim must be backed by a cited source, such as the S&P SPIVA scorecard, before it goes in a real script.)

## 8. Checklist before recording

- [ ] Every number has a ✅ source in the fact-check table
- [ ] All three promises are closed out loud
- [ ] There are two checkpoints
- [ ] No line goes over 14 words and no line is a question (apart from the quiz)
- [ ] Buck and Hamlet only joke
- [ ] The not-advice line is on the end screen
- [ ] The ending covers the callback, the next video, the comment prompt and the like line

---

## How this fits with the script system

`docs/script-system.md` (research → script → humanization) still governs **how** a script is made: research first, facts only from the research, then the humanization pass. This guide governs **what the finished script looks like** for money explainers. Clashes still to decide:

| Topic | Script system says | This guide says | Proposed |
|---|---|---|---|
| Sentence length | 10–30 words, vary the rhythm | 8–14 words, one fact per line | Use 8–14 for this format; the rhythm rules apply across lines, not inside one |
| Structure | Do/avoid: different structure every video, not one template | Fixed beat map and fixed ending | Use the beat map as a menu: keep the parts that suit the topic, reorder or drop the rest |
| Narrator | Do/avoid: own voice, avoid an AI voice on money topics | NARRATOR: Yaboy (an ElevenLabs clone) | Open: record the narrator yourself, or keep the clone |
| Mascots | Long-form video uses YOU, THE APP and other characters who move the explanation along | Buck and Hamlet only joke and never teach | New scripts use Buck and Hamlet; the existing long-form video stays as recorded unless rewritten |
| Quiz | Open conflict about rhetorical questions | One quiz question, answered in the next line | Settled: one quiz per video, answered immediately |
