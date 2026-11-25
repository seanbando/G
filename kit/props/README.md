# Props kit

Reusable props that match the characters (same colours, line weight and hand-drawn wobble). Each function returns an SVG string; place it with `<g transform="translate(x y) scale(s)">` and add `WOBBLE_FILTER` from `kit/characters/characters.js` to the SVG `<defs>`. Parts have ids (prefixed with `opts.id`) so scenes can animate them.

| Prop | Function | Options |
|---|---|---|
| Road map with five stops | `roadMap()` | `stops` (names), `states` per stop: `todo`, `active`, `done` |
| Pizza | `pizza()` | `slices`, `highlight` (slice index), `bite` (scalloped bite from that slice), `label` |
| EXAMPLE card | `exampleCard()` | `title`, `lines`; always carries the "EXAMPLE · MADE-UP NUMBERS" stamp |
| Source tag | `sourceTag()` | `text`; place bottom-left (`translate(60 1040)`) on every real-data shot |
| Price board | `priceBoard()` | `label`, `price`, `change` |

`props-sheet.png` shows them all. Re-render: `node kit/props/render_props.js kit/props/props-sheet.png 2`

One-off props for a single scene (a phone, the coat check, the SIPC shield and so on) are built with the scene, in the same style.
