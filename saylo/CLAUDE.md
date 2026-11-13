# Saylo (@watchsaylo) — working instructions

This folder is the production home for the Saylo YouTube channel. Claude acts as the channel's writer and editor.
(The rest of this repo — `scripts/`, `docs/`, `tools/`, `audio/` — belongs to a different channel, CashleyFinance. Don't mix the two.)

## Before any Saylo work
1. Read `style-sheet.md`. It is the source of truth for voice, structure, blocked words, titles and thumbnails.
2. For a new topic, check `ideas/scorecard.md` first and score the idea before writing.
3. Look at the latest finished video folder in `videos/` as the reference for format.

## Workflow (every video)
1. Score the topic (`ideas/scorecard.md`).
2. Write `videos/NN-slug/script.md` following the style sheet.
3. Run `python3 saylo/tools/check_saylo.py <script.md>` — zero blocked words, ~2,900–3,400 words, wide sentence-length spread.
4. The creator runs the script through GPT for a fact-check and pastes the review back. Apply corrections, push back with reasons where the review is wrong, and log everything in `videos/NN-slug/factcheck.md`.
5. Write `videos/NN-slug/package.md`: chosen title, test title, thumbnail prompt(s), overlay text.
6. Thumbnail review: crop/phone-size test (168px wide) before approving.
7. Edit plan: `videos/NN-slug/edit-plan.md` (shot budget per chapter, holds, silences, name tags) using style-sheet §8, then `shot-list.md` (one row per beat: visual, source, motion, transition, music).
8. Commit and push.

New reference videos from competitors → use the `analyze-reference-video` skill (`.claude/skills/`) and `tools/analyze_edit.py`.

## Hard rules learned so far
- Never invent details (sensory "color", quotes, times, places). If it isn't sourced, cut it or mark it "reportedly".
- Don't compress separate events into one. Don't turn a complicated investigation into a single-clue solution.
- Don't claim investigators "looked in the wrong place" unless the record says so (the Rudolph fact-check caught this).
- Opinions and interpretation go in first person, mostly in the ending.
- Name the case by what people remember ("the Olympic Bomber"), not the person's name, unless the name itself is famous.
- Never generate a real person's face in thumbnails.
