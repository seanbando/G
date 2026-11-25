// Buck and Hamlet: reusable SVG characters for the channel.
// Each function returns an SVG <g> string centred on (0, 0), about 300 x 260 units.
// Usage: buck("cocky"), hamlet("grumpy"). Wrap in <g transform="translate(x y) scale(s)">.
// Colours and line weight live in COLORS / LINE so every scene matches.

const COLORS = {
  ink: "#1f2328",
  bill: "#a9dfb2",
  billLight: "#d8f1dc",
  billDark: "#1f7a45",
  pig: "#f3a8ba",
  pigLight: "#f9cdd8",
  pigDark: "#c9677f",
  brow: "#8a8f98",
  gold: "#f2c14e",
  goldDark: "#b8860b",
  white: "#ffffff",
};
const LINE = 6;

// A gentle hand-drawn wobble applied to whole characters (deterministic seed).
const WOBBLE_FILTER = `
  <filter id="wobble" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/>
  </filter>`;

// ---------- BUCK ----------
const BUCK_FACES = {
  neutral: { browL: "M -38 -26 L -12 -28", browR: "M 12 -28 L 38 -26", pupil: 5.5, look: 0,
             mouth: "M -18 18 Q 0 30 18 18" },
  cocky:   { browL: "M -38 -34 Q -25 -44 -12 -36", browR: "M 12 -27 L 38 -25", pupil: 5.5, look: 3,
             mouth: "M -20 18 Q 4 26 22 12", lids: true },
  shocked: { browL: "M -40 -36 Q -26 -48 -12 -38", browR: "M 12 -38 Q 26 -48 40 -36", pupil: 3, look: 0,
             mouth: "O" },
  annoyed: { browL: "M -38 -34 L -12 -24", browR: "M 12 -24 L 38 -34", pupil: 5.5, look: -5,
             mouth: "M -16 22 L 16 20" },
  happy:   { browL: "M -38 -30 Q -25 -36 -12 -30", browR: "M 12 -30 Q 25 -36 38 -30", closed: true,
             mouth: "M -22 14 Q 0 36 22 14 Z" },
};

const BUCK_ARMS = {
  down:     ["M -122 10 Q -142 40 -146 72", "M 122 10 Q 142 40 146 72"],
  hip:      ["M -122 10 Q -150 30 -128 52", "M 122 10 Q 142 40 146 72"],
  up:       ["M -122 0 Q -150 -40 -156 -86", "M 122 0 Q 150 -40 156 -86"],
  crossed:  ["M -122 26 Q -64 62 34 50", "M 122 26 Q 64 66 -34 54"],
  clipboard:["M -122 10 Q -142 40 -146 72", "M 122 10 Q 150 20 168 0"],
};

function glove(x, y, r = 14) {
  return `<circle cx="${x}" cy="${y}" r="${r}" fill="${COLORS.white}" stroke="${COLORS.ink}" stroke-width="${LINE - 1}"/>`;
}

function armEnd(d) {
  const m = d.match(/(-?[\d.]+) (-?[\d.]+)$/);
  return [parseFloat(m[1]), parseFloat(m[2])];
}

function buck(expr = "neutral", opts = {}) {
  const f = BUCK_FACES[expr] || BUCK_FACES.neutral;
  const armKey = opts.arms || { neutral: "down", cocky: "hip", shocked: "up", annoyed: "crossed", happy: "up" }[expr] || "down";
  const arms = BUCK_ARMS[armKey];
  const ink = COLORS.ink;
  let s = `<g filter="url(#wobble)">`;
  // legs and sneakers
  s += `<path d="M -36 62 L -42 118" stroke="${ink}" stroke-width="${LINE + 1}" stroke-linecap="round" fill="none"/>`;
  s += `<path d="M 36 62 L 42 118" stroke="${ink}" stroke-width="${LINE + 1}" stroke-linecap="round" fill="none"/>`;
  s += `<path d="M -66 124 Q -60 108 -40 114 L -34 126 Z" fill="${ink}"/><path d="M 66 124 Q 60 108 40 114 L 34 126 Z" fill="${ink}"/>`;
  // arms behind the bill when crossed is drawn after the body
  const drawArms = () => arms.map(d => `<path d="${d}" stroke="${ink}" stroke-width="${LINE}" stroke-linecap="round" fill="none"/>` + glove(...armEnd(d))).join("");
  if (armKey !== "crossed") s += drawArms();
  // the bill
  s += `<rect x="-122" y="-66" width="244" height="132" rx="16" fill="${COLORS.bill}" stroke="${ink}" stroke-width="${LINE}"/>`;
  s += `<rect x="-106" y="-51" width="212" height="102" rx="10" fill="none" stroke="${COLORS.billDark}" stroke-width="3"/>`;
  [[-90, -28], [90, -28], [-90, 44], [90, 44]].forEach(([x, y]) => {
    s += `<text x="${x}" y="${y}" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="900" font-size="22" fill="${COLORS.billDark}">1</text>`;
  });
  s += `<ellipse cx="0" cy="0" rx="62" ry="46" fill="${COLORS.billLight}" stroke="${COLORS.billDark}" stroke-width="3"/>`;
  // face
  const eye = (x) => f.closed
    ? `<path d="M ${x - 11} -4 Q ${x} -16 ${x + 11} -4" stroke="${ink}" stroke-width="${LINE - 1}" fill="none" stroke-linecap="round"/>`
    : `<circle cx="${x}" cy="-6" r="12" fill="${COLORS.white}" stroke="${ink}" stroke-width="3"/>` +
      `<circle cx="${x + (f.look || 0)}" cy="-5" r="${f.pupil}" fill="${ink}"/>` +
      (f.lids ? `<path d="M ${x - 12} -10 L ${x + 12} -10" stroke="${ink}" stroke-width="4"/>` : "");
  s += eye(-24) + eye(24);
  s += `<path d="${f.browL}" stroke="${ink}" stroke-width="5" stroke-linecap="round" fill="none"/>`;
  s += `<path d="${f.browR}" stroke="${ink}" stroke-width="5" stroke-linecap="round" fill="none"/>`;
  if (f.mouth === "O") s += `<ellipse cx="0" cy="22" rx="9" ry="12" fill="${ink}"/>`;
  else if (f.mouth.endsWith("Z")) s += `<path d="${f.mouth}" fill="${ink}" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
  else s += `<path d="${f.mouth}" stroke="${ink}" stroke-width="5" stroke-linecap="round" fill="none"/>`;
  if (armKey === "crossed") s += drawArms();
  if (armKey === "clipboard") {
    s += `<g transform="translate(186 -10) rotate(8)"><rect x="-34" y="-46" width="68" height="92" rx="6" fill="#c89b62" stroke="${ink}" stroke-width="${LINE - 1}"/>` +
         `<rect x="-26" y="-34" width="52" height="72" fill="${COLORS.white}" stroke="${ink}" stroke-width="2"/>` +
         `<rect x="-12" y="-52" width="24" height="12" rx="3" fill="#888" stroke="${ink}" stroke-width="2"/>` +
         `<path d="M -18 -18 H 18 M -18 -4 H 18 M -18 10 H 8" stroke="${ink}" stroke-width="3"/></g>` + glove(168, 0);
  }
  return s + `</g>`;
}

// ---------- HAMLET ----------
const HAMLET_FACES = {
  grumpy:  { browL: "M -62 -46 Q -42 -36 -22 -40", browR: "M 22 -40 Q 42 -36 62 -46", pupil: 4, look: 0,
             mouth: "M -16 52 Q 0 42 16 52" },
  sideeye: { browL: "M -62 -42 L -22 -36", browR: "M 22 -46 L 62 -40", pupil: 4, look: 6,
             mouth: "M -14 50 L 14 48", lids: true },
  shocked: { browL: "M -62 -54 Q -42 -66 -22 -54", browR: "M 22 -54 Q 42 -66 62 -54", pupil: 2.5, look: 0,
             mouth: "O", tilt: true },
  proud:   { browL: "M -62 -48 Q -42 -54 -22 -48", browR: "M 22 -48 Q 42 -54 62 -48", closed: true,
             mouth: "M -18 46 Q 0 60 18 46" },
  hugging: { browL: "M -62 -46 L -22 -38", browR: "M 22 -38 L 62 -46", pupil: 4, look: -3,
             mouth: "M -14 52 Q 0 46 14 52" },
};

function hamlet(expr = "grumpy") {
  const f = HAMLET_FACES[expr] || HAMLET_FACES.grumpy;
  const ink = COLORS.ink;
  let s = `<g filter="url(#wobble)">`;
  // tail and legs
  s += `<path d="M 118 6 q 22 -10 18 -26 q -4 -14 -16 -6 q -8 8 6 14" stroke="${ink}" stroke-width="${LINE - 1}" fill="none" stroke-linecap="round"/>`;
  [[-78, 62], [-36, 74], [36, 74], [78, 62]].forEach(([x, y]) => {
    s += `<rect x="${x - 14}" y="${y}" width="28" height="40" rx="8" fill="${COLORS.pig}" stroke="${ink}" stroke-width="${LINE - 1}"/>` +
         `<path d="M ${x - 14} ${y + 32} H ${x + 14}" stroke="${ink}" stroke-width="3"/>`;
  });
  // ears
  s += `<path d="M -78 -66 L -62 -112 L -34 -82 Z" fill="${COLORS.pig}" stroke="${ink}" stroke-width="${LINE - 1}" stroke-linejoin="round"/>`;
  s += `<path d="M 78 -66 L 62 -112 L 34 -82 Z" fill="${COLORS.pig}" stroke="${ink}" stroke-width="${LINE - 1}" stroke-linejoin="round"/>`;
  // body
  s += `<ellipse cx="0" cy="0" rx="124" ry="92" fill="${COLORS.pig}" stroke="${ink}" stroke-width="${LINE}"/>`;
  s += `<ellipse cx="-40" cy="-46" rx="34" ry="14" fill="${COLORS.pigLight}" opacity="0.8"/>`;
  // coin slot
  s += `<rect x="-30" y="-98" width="60" height="12" rx="6" fill="${ink}"/>`;
  // glasses and eyes
  const eyeX = [-42, 42];
  const tilt = f.tilt ? 6 : 0;
  eyeX.forEach((x, i) => {
    const y = -26 + (i ? tilt : -tilt);
    s += f.closed
      ? `<path d="M ${x - 9} ${y + 2} Q ${x} ${y - 8} ${x + 9} ${y + 2}" stroke="${ink}" stroke-width="4" fill="none" stroke-linecap="round"/>`
      : `<circle cx="${x + (f.look || 0)}" cy="${y}" r="${f.pupil}" fill="${ink}"/>` +
        (f.lids ? `<path d="M ${x - 12} ${y - 4} H ${x + 12}" stroke="${ink}" stroke-width="4"/>` : "");
    s += `<circle cx="${x}" cy="${y}" r="19" fill="none" stroke="${ink}" stroke-width="4"/>`;
  });
  s += `<path d="M -23 ${-28 - tilt} Q 0 ${-36} 23 ${-28 + tilt}" stroke="${ink}" stroke-width="4" fill="none"/>`;
  // bushy grey eyebrows
  s += `<path d="${f.browL}" stroke="${COLORS.brow}" stroke-width="11" stroke-linecap="round" fill="none"/>`;
  s += `<path d="${f.browR}" stroke="${COLORS.brow}" stroke-width="11" stroke-linecap="round" fill="none"/>`;
  // snout and mouth
  s += `<ellipse cx="0" cy="14" rx="36" ry="25" fill="${COLORS.pigLight}" stroke="${ink}" stroke-width="${LINE - 1}"/>`;
  s += `<ellipse cx="-11" cy="14" rx="5" ry="8" fill="${COLORS.pigDark}"/><ellipse cx="11" cy="14" rx="5" ry="8" fill="${COLORS.pigDark}"/>`;
  if (f.mouth === "O") s += `<ellipse cx="0" cy="54" rx="9" ry="11" fill="${ink}"/>`;
  else s += `<path d="${f.mouth}" stroke="${ink}" stroke-width="5" stroke-linecap="round" fill="none"/>`;
  // front hooves
  if (expr === "sideeye" || expr === "grumpy") {
    s += `<path d="M -100 44 Q -24 86 44 76" stroke="${ink}" stroke-width="22" stroke-linecap="round" fill="none"/>` +
         `<path d="M -100 44 Q -24 86 44 76" stroke="${COLORS.pig}" stroke-width="13" stroke-linecap="round" fill="none"/>` +
         `<path d="M 100 44 Q 24 90 -44 80" stroke="${ink}" stroke-width="22" stroke-linecap="round" fill="none"/>` +
         `<path d="M 100 44 Q 24 90 -44 80" stroke="${COLORS.pig}" stroke-width="13" stroke-linecap="round" fill="none"/>`;
  } else if (expr === "hugging") {
    s += `<circle cx="0" cy="64" r="34" fill="${COLORS.gold}" stroke="${ink}" stroke-width="${LINE - 1}"/>` +
         `<text x="0" y="76" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="900" font-size="34" fill="${COLORS.goldDark}">$</text>` +
         `<path d="M -100 22 Q -60 70 -24 70" stroke="${ink}" stroke-width="22" stroke-linecap="round" fill="none"/>` +
         `<path d="M -100 22 Q -60 70 -24 70" stroke="${COLORS.pig}" stroke-width="13" stroke-linecap="round" fill="none"/>` +
         `<path d="M 100 22 Q 60 70 24 70" stroke="${ink}" stroke-width="22" stroke-linecap="round" fill="none"/>` +
         `<path d="M 100 22 Q 60 70 24 70" stroke="${COLORS.pig}" stroke-width="13" stroke-linecap="round" fill="none"/>`;
  } else if (expr === "shocked") {
    s += `<path d="M -112 -6 Q -150 -40 -150 -80" stroke="${ink}" stroke-width="22" stroke-linecap="round" fill="none"/>` +
         `<path d="M -112 -6 Q -150 -40 -150 -80" stroke="${COLORS.pig}" stroke-width="13" stroke-linecap="round" fill="none"/>` +
         `<path d="M 112 -6 Q 150 -40 150 -80" stroke="${ink}" stroke-width="22" stroke-linecap="round" fill="none"/>` +
         `<path d="M 112 -6 Q 150 -40 150 -80" stroke="${COLORS.pig}" stroke-width="13" stroke-linecap="round" fill="none"/>`;
  }
  return s + `</g>`;
}

if (typeof module !== "undefined") module.exports = { buck, hamlet, COLORS, WOBBLE_FILTER, BUCK_FACES, HAMLET_FACES };
