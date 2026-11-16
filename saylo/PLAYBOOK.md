# SAYLO PLAYBOOK — every rule, research step and prompt, in pipeline order

Use this to build the task manager: each **Stage** = a column/status, each **☐** = a task, each **Prompt** = a saved template.
Detailed rules live in `style-sheet.md`; this file is the map.

```
1 FIND → 2 SCORE → 3 RESEARCH → 4 SCRIPT → 5 CHECK → 6 FACT-CHECK → 7 PACKAGE → 8 VOICE → 9 EDIT → 10 PUBLISH → 11 REVIEW
```

---

## STAGE 1 — FIND CASES

**Lane rules (a case must pass all):**
- It's about *how* someone was caught or *why* it took so long — a manhunt, a wrong turn in an investigation, or the ordinary thing that broke the case.
- Mostly US, roughly 1995–2015 (audience recognizes it, never understood how it ended).
- There is a real "hidden thing": an object, a mistake, a wrong assumption that explains the case once revealed.
- There is a real answer (no unsolved mysteries).
- Enough for 18–22 minutes.

**Automatic rejects:** geopolitics/war history, famous aviation mysteries, unsolved cases, anything fern / That Chapter / Netflix / 48 Hours covered in the last ~2 years, ideas whose "hook" isn't true (e.g. "the receipt that caught the Unabomber" — false).

**Where ideas come from:**
- "How they were caught" lists: FBI Ten Most Wanted history (fbi.gov/history), FBI "famous cases" pages, DOJ press releases.
- Manhunts that involved a wrong suspect, wrong vehicle or wrong description (the white-van pattern).
- Captures by accident or by an ordinary person (rookie, store clerk, witness with a pen, tip from a TV ad).
- Competitor outliers in the niche (a small channel getting 5x+ its usual views on a case).

☐ Add 5–10 candidate cases to the idea list with a one-line angle each.

**Prompt — idea generation (Claude or GPT):**
> Paste `style-sheet.md` first. Then:
> Give me 15 real US criminal cases from roughly 1995–2015 where the most interesting part is *how the suspect was caught* or *why the manhunt took so long*. For each: the case, the year, the "hidden thing" (the object, mistake or wrong assumption that explains it), and a one-line Saylo angle. Only include cases where that hidden thing is documented — flag anything you're unsure of. Exclude unsolved cases and cases covered by fern, That Chapter or Netflix since 2024.

---

## STAGE 2 — SCORE

**Research steps per candidate (vidIQ / YouTube):**
1. YouTube search the case, sorted by view count, top 5 videos → who covered it, when, how many views. *(Demand + Competition)*
2. Look for small channels (<200k subs) with big views on it → outlier proof. *(Outlier)*
3. Check whether the big creators led with your angle or not. *(Originality)*
4. Check for government/court footage, press conferences, photos. *(Footage)*
5. Sketch the timeline — does it fill 18–22 min? *(Depth)*

**Scorecard (max 100):**
| Criteria | Weight | 5 = | 1 = |
|---|---|---|---|
| Competition (low is good) | ×5 | no big creator has a good long take | covered recently by a big channel/Netflix |
| Demand | ×4 | existing videos pull millions | nobody searches it |
| Outlier proof | ×4 | a small channel broke out with it | only big channels get views |
| Originality | ×3 | our hidden-thing angle nobody leads with | same angle as everyone |
| Footage | ×2 | gov/court footage, pressers, photos | barely any visuals |
| Depth | ×2 | easily 18–22 min | a 6-min story |

**Decision rule:** 80+ = make it next · 70–79 = queue · under 70 = only with a strong new angle · saturated = skip.
Plan in runs of 3 related videos so YouTube learns the lane.

☐ Score each candidate, record data notes (top competitor views, any outlier) in `ideas/scorecard.md`.
☐ Pick the next video and create `videos/NN-slug/`.

---

## STAGE 3 — RESEARCH

**Source priority:** court records/opinions → FBI and DOJ releases → official reviews/reports → contemporaneous reporting (AP, major papers) → later documentaries/books. Wikipedia only to find sources, never as one.

**Prompt — research (adapted from the 3-part system):**
> You are a research assistant preparing factual material for a Saylo YouTube script about [CASE].
> Compile verified information only. Do not write the script.
> Include: timeline with exact dates and times; names, ages, places; how investigators approached the case and what they believed at each stage; every wrong turn (wrong suspect, wrong vehicle, wrong theory) and what corrected it; the specific detail/person/event that broke the case; how the suspect avoided capture; the arrest sequence step by step; charges, plea, sentence (exact); victims and what happened to them; quotes with attribution; anything disputed and who disputes it; primary source links (court, FBI, DOJ) for each fact.
> Rules: only verifiable information; mark uncertain items [UNVERIFIED]; never invent details; don't compress separate events into one; note when a claim comes from a single source or from the perpetrator himself; organize by category with sources.

☐ Run research prompt → save as `videos/NN-slug/research.md`.
☐ Identify the hidden thing, the wrong answer, the break, and the ordinary-truth ending.

---

## STAGE 4 — SCRIPT

**Prompt — script (the creator's universal rules + Saylo specifics):**
> Paste `style-sheet.md` first. Then:
> Using ONLY the research above, write an [18–22] minute Saylo script for: [CASE + ANGLE + TITLE].
> TARGET AUDIENCE: Adults 25–44 (60/40 male), true crime and documentary fans who want to know how investigations actually worked. They recognize these cases but never understood how they ended. Evening/TV viewers who binge and trust calm, sourced storytelling over hype.
> UNIVERSAL RULES: natural spoken language, complete sentences (short fragments only for punch, never stacked adjective lists); specific details over generalizations; state what happened, not what it means; hook 30–45s; body chronological; let strong moments breathe, keep weak ones brief; one concrete visual every 20–30s; protective language ("reportedly", "according to") where needed; real quotes; acknowledge uncertainty; outro = specific question + related video + short subscribe ask.
> STRUCTURE: cold open on the tensest real moment + the one question → the promise → what happened → the wrong answer + a planted "hold onto that" → the break → reveal + replay → aftermath → ordinary-truth ending.
> HOOKS: a new forward hook every 2–3 minutes; if the hook promises a list, call out each item as it lands; one early plant that pays off at the end; re-hook at Part 2.
> FORBIDDEN: blocked words list; invented details; philosophical asides; superhero/game analogies; academic language; bullet lists in narration.
> FORMAT: raw script, natural paragraphs, [VISUAL: ...] only where essential, a [PART 2] split near the middle so each half is under 10,000 characters.

☐ Draft `videos/NN-slug/script.md`.

---

## STAGE 5 — CHECK (humanization + rules)

**Rules (full list in `style-sheet.md` §5):** blocked words and phrases; vary sentence length hard (1–35 words); temporal anchors (exact dates/times); real sensory details only if sourced; first-person opinions instead of hedges; break neat lists of three; no "This isn't just X, it's Y".

☐ Run `python3 saylo/tools/check_saylo.py saylo/videos/NN-slug/script.md` → zero blocked words, 2,900–3,400 words, Part 1 and Part 2 under 10,000 chars.
☐ Read-aloud pass: anything that sounds written, not spoken, gets rewritten.
☐ Hook audit: list every hook and its payoff with timestamps; no gap over ~3 minutes.

---

## STAGE 6 — FACT-CHECK

**Prompt — GPT fact-check:**
> Fact-check this YouTube script line by line. For every correction, give the corrected wording and a source link. Separately list (a) claims you could not verify either way, and (b) places where the script compresses events, invents color details, or overstates what the record shows. Do not rewrite the style — only accuracy.

**Rules learned (Olympic Bomber review):**
- Don't claim investigators looked in the wrong place unless the record says so.
- Don't skip documented steps to make a scene cleaner (the arrest sequence).
- Don't merge two events into one (the two Nordmann visits).
- Appearance or behavior isn't proof (the haircut ≠ an accomplice).
- Exact sentences/charges from court records, not summaries.
- Cut any flourish that isn't sourced.

☐ Run GPT fact-check → paste back to Claude → apply or push back with reasons.
☐ Log every change and every still-unverified item in `videos/NN-slug/factcheck.md`.
☐ Re-check any line added after the fact-check (new hooks, teasers).

---

## STAGE 7 — PACKAGE

**Title rule:** name the case clearly, reveal one surprising fact, leave the explanation for the video. Name the case by what people remember ("the Olympic Bomber"), not the person, unless the name is famous. 40–60 characters, a number when possible.

**Title formats:**
| Format | Example |
|---|---|
| Why [case] Was So Hard to Catch *(series format)* | Why the Olympic Bomber Was So Hard to Catch |
| How [unexpected person] Caught [case] | How a Rookie Cop Caught the Olympic Bomber |
| The [duration] Manhunt for [case] | The 5-Year Manhunt for the Olympic Bomber |
| He [did X]. Then [reversal]. | He Evaded the FBI for Years. Then a Rookie Found Him. |
| The [ordinary object] That [consequence] | The Car That Fooled Police for 23 Days |
| The [role] Who [unexpected outcome] | The Hero Who Became the FBI's Suspect |

**Thumbnail rules:** gray/desaturated 3D miniature diorama of the real place; ONE saturated amber-orange accent on the key detail; 2–3 words (Anton, white + one amber word); one clean arrow/circle allowed; no real faces generated; key detail large enough to read at 168px wide.

**Prompt — thumbnail (fill the brackets):**
> 3D isometric miniature diorama at night, 16:9, camera close and low at a 35-degree angle. Focus on [the real place where the key moment happened, 3–5 concrete objects]. Everything is matte white-gray clay, heavily desaturated, with dark surroundings fading to black. [The key action: who/what is found, and what reveals it]. [The key detail] is bright saturated amber-orange, the only color in the image. The key detail fills the right-center of the frame and is large and clearly readable. Top third of the frame is dark and empty for text. Clean render, high contrast, tilt-shift depth of field. No text, no logos, no faces.

☐ Pick title + a test title.
☐ Generate 2 thumbnail options → phone-size test (168px) → text in Canva.
☐ Save everything in `videos/NN-slug/package.md`.

---

## STAGE 8 — VOICE

**Rules:** calm investigator, ~150 wpm (140–165 by section), low-mid pitch, sentences land down, energy never above 4/5, darkest lines quietest, victims' names slowest and plainest. Silence added in the edit; music cut completely at 3–5 key lines per part.
**TTS text:** spell out every number/time/date; spell out uncommon abbreviations (G-B-I, nine-one-one); key lines on their own line; each file under 10,000 characters, split at a section break.
**ElevenLabs starting points:** one file per section, neighbouring text as context, stability 0.45–0.5, style 0.1–0.2, speed 0.92 (0.88 for victims/evidence sections, 0.98 for brisk sections).

☐ Write `voiceover-partN-directed.md` (energy/pace/emotion per section + beat notes + pronunciations).
☐ Build TTS files (`voiceover-partNa/b-tts.txt`).
☐ Test pronunciations, generate the cold open first, review, then generate the rest.

---

## STAGE 9 — EDIT

**Look:** case-file style — typewriter timestamp cards (`MAY 31, 2003 · 3:30 AM · MURPHY, NC`), dark maps with amber routes/pins, documents with a highlighter sweep, silence at the reveal.
**Clips/copyright:** short clips used as commentary (set up → play → break down); prefer government/court sources; no news-agency footage with logos; no music baked into clips; licensed music only.

☐ Tag every line [MAP] / [ARCHIVE] / [CLIP] / [CARD] and build an asset list.
☐ Gather assets, edit, color to the gray + amber look.
☐ Cut 2–3 Shorts from the strongest "wait, what?" moments, each ending with the full-video title.

---

## STAGE 10 — PUBLISH

☐ Upload around 2–4 PM US Eastern.
☐ Description with sources, chapters matching script sections.
☐ Test & Compare: two thumbnails (and titles if available).
☐ End screen → the most related Saylo video.
☐ Post the Shorts across the following week.

---

## STAGE 11 — REVIEW (7 and 28 days after upload)

☐ Record views, CTR, average view duration, retention dips (and what line was playing at each dip).
☐ Note which thumbnail/title won.
☐ Add one lesson to `style-sheet.md` or this playbook.
☐ Re-score the next 3 ideas if anything changed.

---

## RESEARCH ALREADY DONE (reference files)
| File | Contains |
|---|---|
| `channel/channel-audit.md` | Channel stats Nov 13 2026, why the sniper video worked, why the rest didn't |
| `channel/competitor-analysis.md` | Uncovering / fern / Nexpo script breakdown, title evidence, thumbnail patterns |
| `ideas/scorecard.md` | Ranked list: Olympic Bomber (87), Bulger (84), Dorner (83), Austin bomber (78), Frein (76)… + unscored backlog |
| `style-sheet.md` | Full rules: voice, structure, hooks, blocked words, titles, thumbnails, voiceover, workflow |
| `videos/01-olympic-bomber/` | The complete reference example of every stage |

## Prompt — competitor analysis (when adding new competitors)
> I'm providing [3–5] successful scripts from my niche. Analyze them for: average video length and word count; opening hook style; segment structure and pacing; language patterns and vocabulary level; transitions between segments; call-to-action placement; audience demographics based on content style; and the narrator's energy and emotional tone.
