# Character kit: Buck and Hamlet

Reusable SVG characters for every video. One design, used the same way everywhere.

- `characters.js`: `buck(expression, opts)` and `hamlet(expression)` return SVG groups centred on (0, 0). Shared colours (`COLORS`), line weight and a gentle hand-drawn wobble filter (`WOBBLE_FILTER`, add it to the SVG `<defs>`).
- `character-sheet.png`: every expression, for approval and reference.
- `render_sheet.js`: re-renders the sheet with Playwright: `node kit/characters/render_sheet.js kit/characters/character-sheet.png 2`

## Buck: the cocky dollar bill (voice: Larry)

Expressions: `neutral`, `cocky`, `shocked`, `annoyed`, `happy`. Arm poses (`opts.arms`): `down`, `hip`, `up`, `crossed`, `clipboard`.
Personality: sure of himself, quick dry jokes, never explains anything.

## Hamlet: the grumpy piggy bank (voice: Grampa Werthers)

Expressions: `grumpy` (hooves crossed), `sideeye`, `shocked`, `proud` (rare), `hugging` (his coin).
Personality: old and cranky, bushy grey eyebrows and round glasses, hates spending, warms up only to saving.

## Production notes

- Motion is added scene by scene as videos are built (blinks, bobs, hops, reactions).
- Sound effects are added in one pass once a video is finished.
