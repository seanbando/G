# SAYLO STYLE SHEET
Paste this at the start of every script, title, or fact-check request.

---

## 1. CHANNEL
**Saylo (@watchsaylo)** — How they actually got caught, and why it took so long.
Investigative documentary with a suspense-driven, educational edge. Every video is built around one hidden thing (an object, a mistake, a wrong assumption) that explains the whole case once it's revealed.

**In lane:** manhunts, investigations that went wrong, the clue or person that finally broke a case. Mostly US cases, roughly 1995–2015.
**Out of lane:** geopolitics, unsolved mysteries with no answer, famous aviation mysteries, cases Netflix/fern/That Chapter covered in the last ~2 years.

## 2. AUDIENCE
Adults 25–44 (about 60/40 male). True crime and documentary fans who want to know *how* investigations actually worked. They recognize these cases — some from the news at the time, more from later documentaries — but never understood how the suspect was caught. They watch 18–30 minute videos in the evening, often on TV or while multitasking, binge related videos, and trust calm, sourced storytelling over hype. They read comments and will catch factual errors.

The click: **"I know what happened, but I never understood how they caught him."**

## 3. VOICE
- Calm investigator, not hype narrator. Present tense for scenes.
- Plain spoken words. Talk like you're telling a friend.
- First-person opinions are allowed and encouraged ("this part still gets me", "I'm not sure").
- Cite sources out loud: trial records, court opinions, FBI files, DOJ reviews, contemporary reporting.
- Say when something is disputed. Use "reportedly" / "according to" for single-source claims.
- Victims are named and treated with respect. Never sensationalized.
- Signature ending: the truth is smaller and more ordinary than what people imagined.

**VOICEOVER GATE: flawless or it doesn't ship (creator, Nov 17, 2026; hard rule, learned after video 01 went up with flaws).** The voiceover must play straight through perfectly: no stutters, no repeated or cut-off words, no wrong or missing words, no hesitations or delays mid-sentence, no dead air, no glued sentences with no breath, no line that suddenly rushes or drags, no volume jumps between chunks. Before ANY editing starts:
1. Generate the voiceover, then transcribe the **final mixed file** with word timestamps (ElevenLabs scribe → `vo-words.json`).
2. Run `python3 saylo/tools/check_vo.py vo-words.json voiceover-part1-tts.txt voiceover-part2-tts.txt --audio voiceover-full.mp3 --timings vo-timings.tsv --config vo-config.json --out vo-gate.md`. Gaps are measured from the real audio; chapter breaks (≤2.3 s) and the beats listed in `vo-config.json` are allowed; names the transcriber spells differently but that sound the same go in `vo-config.json` "aliases" (e.g. Dixon=Dickson). Pace = syllables per second of speech, normal 3.3–6.3. It must say **0 problems**. Every flagged line gets regenerated (same voice and settings, a new seed in `vo-config.json` "chunk_settings", with previous/next text), or slowed with `"tempo": 0.88` if it keeps reading rushed, or its gap trimmed; then re-transcribe and re-run. Intentional holds must be written as `[PAUSE]` in the script, or they get flagged.
3. Run the per-chunk loudness/pace check (`vo-check.md`) and fix outliers.
4. The creator listens once, start to finish, and approves. Only then does the edit begin. If a flaw is found after editing has started, fix the voiceover first, then re-time the edit (word timings change).
Pauses written in the voice direction (★ beats, the final hold) are added in the edit **after** the gate passes, so the raw voiceover shouldn't contain them.

## 4. STRUCTURE (18–22 min, ~2,900–3,400 words at ~160 wpm)
| Time | Beat |
|---|---|
| 0:00–0:45 | Cold open on the most tense real moment + the one question the video answers |
| 0:45–1:15 | Why this case is different + one line on sources |
| 1:15–6:00 | What happened, and what investigators had |
| 6:00–12:00 | The wrong answer everyone believed + a planted detail ("hold onto that") |
| 12:00–16:00 | The ordinary thing that broke it |
| 16:00–18:00 | The reveal, then a replay of the case with that fact in hand |
| 18:00–end | Aftermath, the ordinary truth, a closing line |
| Outro (~30s) | One specific question for comments + one related Saylo video + short subscribe ask |

**Hooks & payoffs (retention):**
- Open a new forward hook at least every 2–3 minutes. No stretch over ~3 minutes without one (biography and "the search" sections are where gaps happen).
- If the hook promises a list ("three reasons"), call out each one when it lands ("That's reason number two").
- At least one "hold onto that" plant in the first third that pays off near the end.
- Re-hook at the start of Part 2 with a teaser about the ending.
- Use only facts for teasers — a hook can't promise something the script doesn't deliver.

Mark a split point `[PART 2]` near the middle so each half fits under 10,000 characters for voice tools.

## 5. WRITING RULES
**Rhythm:** mix very short sentences with long ones. Fragments are fine for punch ("One minute."), but never stacked adjective lists ("Smart. Calculated. Ruthless.").
**Specifics:** real dates, times, places, names, numbers. One concrete visual every 20–30 seconds.
**No invented details.** Sensory or "color" details must be sourced. If it can't be sourced, cut it. Don't compress separate events into one, and don't turn a complicated investigation into a single-clue solution.
**Interpretation is labeled as interpretation.** State what happened; keep "what it means" to the ending, in first person.

**Blocked words and phrases:**
in conclusion, it is important to note, furthermore, moreover, consequently, in summary, to wrap things up, let's dive in/into, without further ado, it is worth noting, conversely, notably, additionally, subsequently, unlocking the secrets, embark on a journey, game-changer, the ultimate guide, master the art of, in the vast landscape of, in the realm of, a rich tapestry, a testament to, beacon of hope, unleash the power of, elevate, navigating the complex world of, it depends on various factors, on one hand/on the other hand, it remains to be seen, ideally, typically, generally speaking, while it may seem, remember to always, it is crucial to ensure, by following these steps, foster a sense of, it is paramount that, have you ever wondered, in today's fast-paced world, in this digital age, in the modern world, welcome back to the channel, delve, landscape, testament, tapestry, realm, foster, underscore, nuanced, crucial, paramount, unlock, unleash, elevate, optimization, leverage, holistic, synergy, robust, streamline, revolutionize.
Also avoid: "This isn't just X, it's Y", "carefully orchestrated", "multifaceted", superhero/video game analogies.

**Source watermark (every piece of real footage, photo or document):** the **source's name only**, nothing else — e.g. `WNEP`, `FBI`, `Pa. Supreme Court`. Small text, bottom-right, no box: JetBrains Mono Medium 22px, off-white at ~67% opacity, 70px from the right edge, 60px from the bottom. On screen for the whole clip. Creative Commons images are the one exception: their license requires the author and license, so they read `SounderBruce · CC BY-SA 4.0`. Make one with `python3 saylo/tools/make_source_tag.py "WNEP"`; ready-made ones are in `assets/source-tags/`.

**Clips (copyright):** **Real news footage first, always, whenever it exists:** over stock footage or AI recreations (creator's rule, Nov 14, 2026). Use recreations only where no real footage exists. Keep each clip short (under ~10s) and always as commentary: set it up, play it, break it down. Crop network logos out of the frame where you can, but don't paint over or blur them (removing a broadcaster's mark can cause its own copyright problem); our source watermark credits them. No clips with music baked in. Only licensed music.

## 5b. VOICEOVER
- Calm investigator, ~150 wpm baseline (range 140–165). Low-mid pitch, sentences land down. Energy never above 4/5; the darkest lines are the quietest.
- Silence is the main effect: pauses are added in the edit. Cut music entirely at 3–5 key lines per part.
- Victims' names: slowest pace, plain delivery, no dramatic emphasis.
- TTS files: spell out every number, time and date ("twelve fifty-eight", "nineteen ninety-six"); spell out uncommon abbreviations (G-B-I, A-T-and-T, nine-one-one, U-S). Keep each file under 10,000 characters; split at a section break.
- Each video gets a `voiceover-partN-directed.md` (energy/pace/emotion per section + beat notes) alongside the TTS text. Example: `videos/01-olympic-bomber/`.

## 6. TITLES
**Rule:** name the case clearly, reveal one surprising fact, leave the explanation for the video.
Name the case by what people remember ("the Olympic Bomber", "the D.C. Sniper"), not the person's name — unless the name itself is famous (Bulger, Escobar). 40–60 characters. Include a number when possible.

| Format | Example |
|---|---|
| Why [case] Was So Hard to Catch *(recurring series format)* | Why the Olympic Bomber Was So Hard to Catch |
| How [unexpected person] Caught [case] | How a Rookie Cop Caught the Olympic Bomber |
| The [duration] Manhunt for [case] | The 5-Year Manhunt for the Olympic Bomber |
| He [did X]. Then [reversal]. | He Evaded the FBI for Years. Then a Rookie Found Him. |
| The [ordinary object] That [consequence] | The Car That Fooled Police for 23 Days |
| The [role] Who [unexpected outcome] | The Hero Who Became the FBI's Suspect |

Never: claims the video can't back up, vague "the mystery of" titles, "Full Documentary".

## 7. THUMBNAILS
- Gray/desaturated base with ONE fully saturated accent: amber-orange (the niche uses red, so orange stands out in the sidebar). Used on every video.
- Preferred look: 3D isometric miniature diorama of the real place (matte white-gray clay), with the key detail, route or figure in amber. Proven by Uncovering's top outliers (escape route, North Tower, Pizza Hut).
- **The thumbnail must show the title's key object or action** (not just the mood). Viewers should get the title's story from the image alone. Titles built around a physical object beat abstract titles because they can be drawn.
- One object or scene. 2–3 words max, heavy condensed font (Anton), white with one amber word. Text adds to the title, never repeats it.
- One clean white hand-drawn arrow or circle pointing at the key detail is fine. No cluttered arrows, no shocked faces.
- Must read on a phone and on a TV. Squint test before upload.
- Never generate a real person's face. Recreate scenes with AI/3D renders; avoid news-agency photos.
- Test 2 options with YouTube Studio's Test & Compare.

**Thumbnail prompt template** (swap the bracketed parts, keep the rest):
```
3D isometric miniature diorama at night, 16:9, camera close and low at a 35-degree angle. Focus on [the real place where the key moment happened, 3–5 concrete objects]. Everything is matte white-gray clay, heavily desaturated, with dark surroundings fading to black. [The key action: who/what is found, and what reveals it]. [The key detail] is bright saturated amber-orange, the only color in the image. The key detail fills the right-center of the frame and is large and clearly readable. Top third of the frame is dark and empty for text. Clean render, high contrast, tilt-shift depth of field. No text, no logos, no faces.
```
Text goes on in Canva afterward (AI tools mangle lettering). Approved example: `videos/01-olympic-bomber/`.

**Narrator voice:** **Saylo new** — the creator's own Yaboy clone remixed deeper and steadier (ElevenLabs `MB346AXfvAnxXiEMXWHX`), `eleven_v4`, stability 0.4 / similarity 0.8 / style 0.2. Matches the Boston-bombers reference narrator (~95–100 Hz, steady pitch). Use the same voice on every video. Extra energy in the hook comes from music/SFX and dense visuals, not speed. Keep the original Yaboy for CashleyFinance.

## 8. VISUAL STYLE
Case-file look: timestamp cards in a typewriter font (`MAY 31, 2003 · 3:30 AM · MURPHY, NC`), dark maps with the accent color for routes and scenes, documents with a highlighter sweep on the key line, silence at the reveal.

**Editing rules** (measured from Uncovering + fern, see `channel/edit-style-analysis.md`):
| Rule | Target |
|---|---|
| Overall pace | ~13 cuts/min, median shot ~3–3.5s, average ~4.5s. A 20-min video ≈ 270 shots. |
| Hook (first 60s) | 25–35 cuts — one every ~2s. Fastest part of the video. |
| Short vs long | ~1/3 of shots under 2s; ~1 in 10 held 10s+ (maps being explained, emotional beats). |
| Chapter breaks | Fade to black + chapter card. Only at chapters (~8–10 per video). Nowhere else. |
| Music | Never stops, except 1–2 deliberate silent holds at the biggest emotional beat. |
| Maps | Dark teal/near-black terrain or street map, route line draws itself in amber, pin icons, timestamp card in the corner, camera flies between pins. |
| Documents | Slow push-in + amber highlighter sweep on the key line. |
| People | Name tag (Anton, caps, off-white) the first time anyone appears. Real photos get a slow push-in or parallax. |
| **All on-screen text** | **Typewriter effect on every piece of text, no exceptions:** timestamp cards, name tags, labels, counters, quotes, chapter cards, map labels, evidence-board text. Letters type on one by one (~25–35 characters/sec, fast enough to finish before the line it supports ends) with a blinking cursor at the end for 2–3 blinks, then the cursor disappears. Each type-on gets **typewriter keystroke SFX** matched to its length, plus a carriage-return "ding" only on chapter cards. Fonts stay as set (typewriter font for cards/labels, Anton for name tags); only the reveal is typed. |
| Archival clips | Set up → play (short) → break down. Framed or with a lower third, never dropped in raw. |
| Missing footage | AI/3D recreations (no real faces), maps, documents — never invent a scene the record doesn't support. |
| Color grade | Dark, desaturated, cool shadows; amber is the only warm accent. |

**Transitions** (same effects as the shorts, tuned calmer for long-form; tool: `saylo/tools/edit_video.py`):
| Effect | Use it for | Limit |
|---|---|---|
| Hard cut | Default for everything | — |
| `zoomthru` (punch-zoom + blur + flash through the cut) | Big reveals: "His real name was Eric Rudolph", "Eric Robert Rudolph" name reveal, booking photo | 3–5 per video |
| `whip left/right` | Jumps between places or years: map pin → next pin, 1996 → 1998, back to the parking lot | ~1 per chapter |
| `flash` | Only the blast cut and the camera-shutter on the booking photo | 2 per video |
| `shake 0.2–0.3` | Lands with a boom SFX (name reveals, "That second one was for them", cell door) | with booms only |
| `punch` | A number as it's spoken: $1,000,000, 88 days, 200 agents, 250 lbs, 6 life sentences | max ~1 per 20s |
| `push` | Photos, documents, maps (100→115% over ~6s) | most stills |
| `reframe` jump cuts | Hook only (first 60s), for energy | not after 1:00 |
Never use a transition inside the silent Jewell hold or on archival news clips.

**The Saylo look (locked Nov 15, 2026, after the style test):** the creator's Template Library effects carry the stills: case board / evidence wall (connections), press stack and article zoom (headlines, documents), film window (archival photos), photo timeline (sequences of dated photos), clock badge and territory/date maps (times and places), archive profiles (people). Plain photos with a push-in are only quick 2–3 s cutaways between them. Moving AI recreations (faceless, 5 s, same look as scenes A–J) cover beats with no real footage; real news footage always wins when it exists. Engine: `node .claude/effects/render_effect.mjs` from the Template Library (see `saylo/tools` notes).

**100% rule (creator, Nov 15, 2026): the picture always shows what the narration is saying at that exact moment.** Shots are cut on word-level timestamps (`vo-words.json`), never on sentence or chunk timing. A clip made for one line is never reused under a different line it doesn't match (e.g. the dumpster-raid scene only plays under "go through the trash", never under "the man bolts"). If no matching visual exists for a line, use a typed card or a matching effect, and list the gap for the creator. Every asset the creator made (scenes A–J and later, animated location clips) gets used on the line it was made for.

**Retraced look (creator, Nov 16, 2026: "copy his visuals + transitions"; supersedes the Template Library look where they conflict):**
- Recreations are **3D mannequin scenes**: clean 3D sets of the real places, dark navy/gray light, everyone a faceless matte white/gray mannequin, **the subject (Rudolph) one glossy amber-orange mannequin** in every scene. Real people = real footage/photos or a white 3D clay bust with an amber rim light. Prompts: `videos/01-olympic-bomber/retraced-style-prompts.md`.
- Maps = 3D white clay block/terrain models, key place lit amber, route line glows across, time stamp + timeline bar.
- Chapter cards live inside the scene (street sign, wall lettering). Date stamps big white bold caps top-left. Quotes on a wall with an amber bar. Counters as icons ("6 SHOT" style).
- Pace: ~25 cuts/min in the first third, ~15 after; median shot 2.6 s; 40+ cuts in the first 60 s.
- Transitions: hard cuts; motion comes from the camera inside the clip (dolly, orbit, push through a door/window). White flash only on the blast. Fade to black only at the 2 biggest beats. Whips/zoom-throughs dropped.
- Typewriter rule for text still applies (creator rule).

Every script gets a shot list (`videos/NN-slug/shot-list.md`) before editing: one row per beat with visual, source, motion, transition and music cue.

## 9. WORKFLOW
1. Pick and score the topic (scorecard: Competition ×5, Demand ×4, Outlier proof ×4, Originality ×3, Footage ×2, Depth ×2 = /100).
2. Claude writes the script using this sheet.
3. GPT fact-checks it (prompt below).
4. Paste the review back to Claude; Claude applies fixes or pushes back with reasons.
5. Titles + thumbnails, then [MAP]/[ARCHIVE]/[CLIP] tagging, then record.

**Fact-check prompt for GPT:**
> Fact-check this YouTube script line by line. For every correction, give the corrected wording and a source link. Separately list (a) claims you could not verify either way, and (b) places where the script compresses events, invents color details, or overstates what the record shows. Do not rewrite the style — only accuracy.
