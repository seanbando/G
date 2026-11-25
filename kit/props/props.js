// Reusable props for the channel's videos. Same colours and line weight as the
// characters (kit/characters/characters.js), so everything matches on screen.
// Each function returns an SVG string; place it with <g transform="translate(x y) scale(s)">.
// Element ids are prefixed (opts.id) so scenes can animate parts with GSAP.

const { COLORS } = require("../characters/characters.js");
const INK = COLORS.ink;
const FONT = "Nunito, sans-serif";
const PAPER = "#f6f3ea";
const ACCENT = "#23a05a";
const STAMP = "#c0392b";
const GREY = "#7a7f87";

function text(x, y, str, size, { weight = 800, fill = INK, anchor = "middle", extra = "" } = {}) {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${FONT}" font-weight="${weight}" font-size="${size}" fill="${fill}" ${extra}>${str}</text>`;
}

// Small red "EXAMPLE · MADE-UP NUMBERS" badge for any prop showing made-up numbers.
function exampleBadge(x, y, rot = -8) {
  return `<g transform="translate(${x} ${y}) rotate(${rot})">` +
    `<rect x="-120" y="-30" width="240" height="60" rx="9" fill="#fffaf0" stroke="${STAMP}" stroke-width="5"/>` +
    text(0, -4, "EXAMPLE", 24, { weight: 900, fill: STAMP }) +
    text(0, 20, "MADE-UP NUMBERS", 17, { weight: 900, fill: STAMP }) + `</g>`;
}

// ---------- ROAD MAP ----------
// Five stops along a hand-drawn road. state per stop: "todo" | "active" | "done".
// Drawn in a 1600 x 360 box with its top-left at (0, 0).
const ROAD_PATH = "M 20 220 C 230 60, 340 330, 560 210 S 900 70, 1050 210 S 1380 330, 1580 150";
function roadMap({ id = "map", stops = ["Your App", "Market Maker", "Exchange", "Seller", "Clearinghouse"],
                   states = [], positions = [[100, 158], [452, 245], [800, 128], [1157, 262], [1500, 183]],
                   labelAbove = [false, false, false, false, true] } = {}) {
  let s = `<g id="${id}" filter="url(#wobble)">`;
  s += `<path id="${id}-road" d="${ROAD_PATH}" fill="none" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>`;
  s += `<path d="${ROAD_PATH}" fill="none" stroke="${PAPER}" stroke-width="3" stroke-dasharray="18 22" stroke-linecap="round"/>`;
  stops.forEach((name, i) => {
    const [x, y] = positions[i];
    const st = states[i] || "todo";
    const fill = st === "active" ? ACCENT : st === "done" ? "#cfead7" : "#fff";
    s += `<g id="${id}-stop${i + 1}">`;
    s += `<circle cx="${x}" cy="${y}" r="40" fill="${fill}" stroke="${INK}" stroke-width="8"/>`;
    s += st === "done"
      ? `<path d="M ${x - 16} ${y} L ${x - 4} ${y + 13} L ${x + 18} ${y - 14}" fill="none" stroke="${COLORS.billDark}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>`
      : text(x, y + 15, i + 1, 42, { weight: 900, fill: st === "active" ? "#fff" : INK });
    s += text(x, labelAbove[i] ? y - 62 : y + 98, name, 36);
    s += `</g>`;
  });
  return s + `</g>`;
}

// ---------- PIZZA ----------
// A pizza centred on (0, 0), radius 300. highlight = slice index (0 = right, going counter-clockwise).
// bite = true cuts a scalloped bite from the highlighted slice's crust.
function pizza({ id = "pizza", slices = 8, highlight = null, bite = false, label = null, note = null, example = false } = {}) {
  const R = 300;
  let s = `<g id="${id}" filter="url(#wobble)">`;
  s += `<circle r="${R}" fill="#f3c26b" stroke="${INK}" stroke-width="10"/>`;
  s += `<circle r="${R - 45}" fill="#e8573f" stroke="${INK}" stroke-width="6"/>`;
  // pepperoni, fixed positions
  [[-120, -90], [60, -160], [-40, 60], [140, 40], [-150, 120], [40, 180], [180, -90], [-60, -190]]
    .forEach(([x, y]) => (s += `<circle cx="${x}" cy="${y}" r="26" fill="#b8352a" stroke="${INK}" stroke-width="4"/>`));
  for (let k = 0; k < slices; k++) {
    const a = (-k / slices) * Math.PI * 2;
    const w = slices > 40 ? 1.5 : slices > 16 ? 3 : 6;
    const r0 = slices > 16 ? R * 0.16 : 0;  // many slices: start the cuts away from the centre
    s += `<line x1="${(Math.cos(a) * r0).toFixed(1)}" y1="${(Math.sin(a) * r0).toFixed(1)}" x2="${(Math.cos(a) * R).toFixed(1)}" y2="${(Math.sin(a) * R).toFixed(1)}" stroke="${INK}" stroke-width="${w}"/>`;
  }
  if (highlight !== null) {
    const a1 = (-highlight / slices) * Math.PI * 2, a2 = (-(highlight + 1) / slices) * Math.PI * 2;
    const p1 = [Math.cos(a1) * R, Math.sin(a1) * R], p2 = [Math.cos(a2) * R, Math.sin(a2) * R];
    const wedge = `M 0 0 L ${p1[0].toFixed(1)} ${p1[1].toFixed(1)} A ${R} ${R} 0 0 0 ${p2[0].toFixed(1)} ${p2[1].toFixed(1)} Z`;
    s += `<g id="${id}-slice"><defs><clipPath id="${id}-clip"><path d="${wedge}"/></clipPath></defs>`;
    s += `<path d="${wedge}" fill="#ffd27a" stroke="${COLORS.billDark}" stroke-width="10" stroke-linejoin="round"/>`;
    if (bite) {
      const mid = (a1 + a2) / 2, spread = (a1 - a2) * 0.32;
      s += `<g id="${id}-bite" clip-path="url(#${id}-clip)">`;
      [[mid - spread, 44], [mid, 50], [mid + spread, 44]].forEach(([a, r]) => {
        s += `<circle cx="${(Math.cos(a) * 285).toFixed(1)}" cy="${(Math.sin(a) * 285).toFixed(1)}" r="${r}" fill="${PAPER}" stroke="${COLORS.billDark}" stroke-width="8"/>`;
      });
      s += `</g>`;
    }
    s += `</g>`;
  }
  if (label) s += text(0, -R - 50, label, 52);
  if (note) s += text(0, R + 62, note, 34, { weight: 700, fill: GREY });
  if (example) s += exampleBadge(R - 40, R - 10);
  return s + `</g>`;
}

// ---------- EXAMPLE CARD ----------
// A cream index card with a red "EXAMPLE · MADE-UP NUMBERS" stamp. Top-left at (0, 0), 640 x 360.
function exampleCard({ id = "example", title = "EXAMPLE", lines = [] } = {}) {
  let s = `<g id="${id}" filter="url(#wobble)">`;
  s += `<rect x="8" y="10" width="640" height="360" rx="14" fill="#d9d3c4"/>`;
  s += `<rect width="640" height="360" rx="14" fill="#fffaf0" stroke="${INK}" stroke-width="7"/>`;
  [120, 180, 240, 300].forEach(y => (s += `<line x1="36" y1="${y}" x2="604" y2="${y}" stroke="#b9d3e8" stroke-width="3"/>`));
  s += `<line x1="36" y1="78" x2="604" y2="78" stroke="#e8a3a3" stroke-width="3"/>`;
  s += text(40, 62, title, 44, { weight: 900, anchor: "start" });
  lines.forEach((l, i) => (s += text(40, 166 + i * 60, l, 38, { weight: 700, anchor: "start" })));
  s += `<g id="${id}-stamp" transform="translate(470 300) rotate(-12)">` +
       `<rect x="-150" y="-36" width="300" height="72" rx="10" fill="none" stroke="${STAMP}" stroke-width="7"/>` +
       text(0, -4, "EXAMPLE", 30, { weight: 900, fill: STAMP }) +
       text(0, 26, "MADE-UP NUMBERS", 22, { weight: 900, fill: STAMP }) + `</g>`;
  return s + `</g>`;
}

// ---------- SOURCE TAG ----------
// Small grey caption for every real-data shot. Place at bottom-left: translate(60 1040).
function sourceTag({ id = "source", text: str = "Source: SEC Investor.gov" } = {}) {
  return `<g id="${id}">` +
    `<rect x="-14" y="-34" width="${Math.max(220, str.length * 15.5)}" height="48" rx="10" fill="#ffffff" opacity="0.82"/>` +
    text(0, 0, str, 28, { weight: 700, fill: GREY, anchor: "start" }) + `</g>`;
}

// ---------- PRICE BOARD ----------
// A ticker-style board showing the last-trade price. Top-left at (0, 0), 640 x 300.
function priceBoard({ id = "board", label = "APPLE · LAST TRADE", price = "$250.00", change = null, example = false } = {}) {
  let s = `<g id="${id}" filter="url(#wobble)">`;
  s += `<rect x="0" y="0" width="640" height="300" rx="22" fill="#20252b" stroke="${INK}" stroke-width="8"/>`;
  s += `<rect x="24" y="24" width="592" height="252" rx="12" fill="#2c333b"/>`;
  s += text(320, 82, label, 32, { weight: 800, fill: "#aab3bd" });
  s += `<g id="${id}-price">` + text(320, 196, price, 104, { weight: 900, fill: "#5fe08f" }) + `</g>`;
  if (change) s += text(320, 252, change, 34, { weight: 800, fill: "#5fe08f" });
  [70, 570].forEach(x => (s += `<circle cx="${x}" cy="50" r="8" fill="#5fe08f"/>`));
  if (example) s += exampleBadge(540, 4, 6);
  return s + `</g>`;
}

module.exports = { roadMap, pizza, exampleCard, sourceTag, priceBoard, exampleBadge, ROAD_PATH };
