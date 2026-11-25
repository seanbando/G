# Stills: Follow $1 From Your Pocket to Wall Street

One still per script line (S001–S164), 1920 × 1080. These are the end-state pictures for each line; motion is added when the scenes are built, timed from `audio/follow-one-dollar-v6/timings.json`.

- `png/S001.png …` the stills
- `sheets/sheet-01.png …` contact sheets (12 stills each, with the spoken line under each one) for review
- `terms.md` every "IN PLAIN WORDS" card: the term, what the letters stand for, and the plain meaning shown on screen
- `scenes-a.js … scenes-d.js` the layout of each still; `lib.js` the drawing helpers; `render.js` the renderer

Re-render everything: `node video/01-follow-one-dollar/stills/render.js`
Re-render some: `node video/01-follow-one-dollar/stills/render.js --only S090,S094`

Rules built into the renderer:
- The section chip (top-left), the EXAMPLE · MADE-UP NUMBERS badge and the source tag come straight from `script.md`, so they can't drift from the script.
- The 1–5 dots (top-right) show which stop the dollar is on.
- A term people may not know gets a yellow plain-words card in the bottom band. Acronyms are spelled out (DTCC, DTC, NYSE, IPO, SIPC).
- Long text shrinks to fit, and the renderer warns if any text leaves the safe area or a card covers the source tag.
- Mascot stills carry a 1–3 word bubble only; the joke itself is spoken.
