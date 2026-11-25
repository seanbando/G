// Drawing helpers and one-off props for the stills of "Follow $1".
// Same colours, line weight and wobble as the kit (kit/characters, kit/props).
// Everything returns SVG strings. Stage is 1920 x 1080.
const path = require("path");
const KIT = path.join(__dirname, "..", "..", "..", "kit");
const { buck, hamlet, COLORS, WOBBLE_FILTER } = require(path.join(KIT, "characters", "characters.js"));
const P = require(path.join(KIT, "props", "props.js"));

const INK = COLORS.ink, PAPER = "#f6f3ea", GREEN = "#23a05a", DGREEN = COLORS.billDark, RED = "#c0392b",
  GREY = "#7a7f87", LGREY = "#d5d2c8", BLUE = "#3b82c4", LBLUE = "#cfe3f5", YEL = "#fff1a8", GOLD = COLORS.gold,
  CREAM = "#fffaf0", ORANGE = "#e8843f", PURPLE = "#8e6bbf", SKIN = ["#f1c9a5", "#c98d5e", "#8a5a3c", "#e6b48c"];
const FONT = "Nunito, sans-serif";
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

// text; opts.max = shrink to fit this width (done in the browser at render time)
function t(x, y, str, size = 40, { w = 800, fill = INK, anchor = "middle", max = null, extra = "" } = {}) {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${FONT}" font-weight="${w}" font-size="${size}" fill="${fill}"${max ? ` data-max="${max}"` : ""} ${extra}>${esc(str)}</text>`;
}
function wrap(str, max) {
  const out = []; let cur = "";
  for (const word of String(str).split(" ")) {
    if (cur && (cur + " " + word).length > max) { out.push(cur); cur = word; } else cur = cur ? cur + " " + word : word;
  }
  if (cur) out.push(cur);
  return out;
}
// multi-line text block, centred on x, first baseline at y
function lines(x, y, str, size = 40, { max = 30, lh = 1.22, ...o } = {}) {
  return (Array.isArray(str) ? str : wrap(str, max)).map((l, i) => t(x, y + i * size * lh, l, size, o)).join("");
}
const g = (x, y, s, inner, rot = 0) => `<g transform="translate(${x} ${y})${rot ? ` rotate(${rot})` : ""}${s !== 1 ? ` scale(${s})` : ""}">${inner}</g>`;
const W = (inner, id) => `<g filter="url(#wobble)"${id ? ` id="${id}"` : ""}>${inner}</g>`;
// Motion tag. In a still this is just a group; the motion builder animates it when the
// narrator reaches the word `on` ("start", a word, "word:2" for its 2nd use, or "+1.5" seconds
// into the line). fx: pop, fade, slide (dir l/r/u/d), wipe (dir), stamp, move (dx, dy, dur).
// idle: "bob" (gentle float) or "talk" (hops on each spoken word).
function A(inner, on = "start", fx = "pop", o = {}) {
  const at = Object.entries({ dir: o.dir, dx: o.dx, dy: o.dy, dur: o.dur, delay: o.delay }).filter(([, v]) => v !== undefined).map(([k, v]) => ` data-${k}="${v}"`).join("");
  return `<g class="anim" data-on="${on}" data-fx="${fx}"${at}>${o.idle ? `<g class="idle" data-idle="${o.idle}">${inner}</g>` : inner}</g>`;
}
const dim = (inner, o = 0.3) => `<g opacity="${o}">${inner}</g>`;

// ---------- frame furniture ----------
// headline: one line if it fits, otherwise two balanced lines (no single word left alone)
function headline(str, { size = 62, max = 44, fill = INK, width = 1500 } = {}) {
  let ls = [str];
  if (str.length > max) {
    const words = str.split(" "); let best = null;
    for (let i = 1; i < words.length; i++) {
      const a = words.slice(0, i).join(" "), b = words.slice(i).join(" "), d = Math.abs(a.length - b.length);
      if (!best || d < best.d) best = { d, ls: [a, b] };
    }
    ls = best.ls;
  }
  const ys = ls.length === 1 ? [184] : [172, 172 + size * 1.12];
  return `<g class="headline">` + ls.map((l, i) => t(960, ys[i], l, size, { w: 900, fill, max: width })).join("") + `</g>`;
}
function chip(label) {
  return `<g class="chip fitbox" data-allow-edge data-pad="22" data-anchor="start"><rect x="50" y="34" width="300" height="52" rx="26" fill="#fff" stroke="${INK}" stroke-width="4"/>` +
    t(74, 71, label, 26, { w: 900, anchor: "start", fill: GREY }) + `</g>`;
}
// five dots, top-right: where we are on the trip
function miniMap(active, doneUpTo = active - 1) {
  let s = `<g class="minimap" data-allow-edge><path d="M 1560 62 H 1840" stroke="${INK}" stroke-width="5" stroke-dasharray="10 9"/>`;
  for (let i = 1; i <= 5; i++) {
    const x = 1560 + (i - 1) * 70, st = i === active ? "a" : i <= doneUpTo ? "d" : "t";
    s += `<circle cx="${x}" cy="62" r="23" fill="${st === "a" ? GREEN : st === "d" ? "#cfead7" : "#fff"}" stroke="${INK}" stroke-width="5"/>` +
      t(x, 72, i, 26, { w: 900, fill: st === "a" ? "#fff" : INK });
  }
  return s + `</g>`;
}
// Plain-words card for a term people may not know. Sits in the bottom band.
// term: the word; full: what the letters stand for (optional); meaning: plain words (string or 2 lines)
function termCard(term, meaning, { full = null, x = 960, bottom = 992 } = {}) {
  const ms = Array.isArray(meaning) ? meaning : wrap(meaning, 54);
  const h = 84 + ms.length * 44 + (full ? 40 : 0) + 14, y = bottom - h;
  let s = `<g class="fitbox term" data-pad="36" data-minw="520" data-anchor="middle">`;
  s += `<rect x="${x - 300}" y="${y}" width="600" height="${h}" rx="16" fill="${YEL}" stroke="${INK}" stroke-width="5"/>`;
  s += t(x, y + 62, term, 42, { w: 900 });
  let yy = y + 62;
  if (full) { yy += 40; s += t(x, yy, "= " + full, 30, { w: 800, fill: DGREEN }); }
  ms.forEach((l) => { yy += 44; s += t(x, yy, l, 34, { w: 700 }); });
  s += `<g transform="translate(${x} ${y})"><rect x="-112" y="-18" width="224" height="36" rx="18" fill="${INK}"/>` + t(0, 8, "IN PLAIN WORDS", 21, { w: 900, fill: "#fff" }) + `</g>`;
  return s + `</g>`;
}
function bubble(x, y, str, { tail = "left", size = 44 } = {}) {
  const tx = tail === "left" ? -60 : 60;
  return `<g class="fitbox bubble" data-pad="30" data-anchor="middle"><rect x="${x - 150}" y="${y - 52}" width="300" height="84" rx="36" fill="#fff" stroke="${INK}" stroke-width="6"/>` +
    t(x, y + 5, str, size, { w: 900 }) + `</g>` +
    `<path d="M ${x + tx - 20} ${y + 29} L ${x + tx * 1.9} ${y + 84} L ${x + tx + 22} ${y + 29}" fill="#fff" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>` +
    `<path d="M ${x + tx - 16} ${y + 27} H ${x + tx + 18}" stroke="#fff" stroke-width="9"/>`;
}
function arrow(x1, y1, x2, y2, { color = INK, width = 8, label = null, dash = null, curve = 0, lsize = 30, lfill = null, ldy = -18 } = {}) {
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
  const cx = mx - (dy / len) * curve, cy = my + (dx / len) * curve;
  const ang = Math.atan2(y2 - cy, x2 - cx), a = 0.5, hl = 26;
  const head = `M ${x2 - hl * Math.cos(ang - a)} ${y2 - hl * Math.sin(ang - a)} L ${x2} ${y2} L ${x2 - hl * Math.cos(ang + a)} ${y2 - hl * Math.sin(ang + a)}`;
  return `<path d="M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round"${dash ? ` stroke-dasharray="${dash}"` : ""}/>` +
    `<path d="${head}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>` +
    (label ? t(cx * 0.5 + mx * 0.5, cy * 0.5 + my * 0.5 + ldy, label, lsize, { w: 800, fill: lfill || color }) : "");
}
const cross = (x, y, r = 40, w = 12) => `<path d="M ${x - r} ${y - r} L ${x + r} ${y + r} M ${x + r} ${y - r} L ${x - r} ${y + r}" stroke="${RED}" stroke-width="${w}" stroke-linecap="round"/>`;
const tick = (x, y, r = 40, w = 12, c = GREEN) => `<path d="M ${x - r} ${y} L ${x - r * 0.3} ${y + r * 0.7} L ${x + r} ${y - r * 0.8}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
function stamp(x, y, str, { color = RED, rot = -8, size = 40 } = {}) {
  return `<g transform="translate(${x} ${y}) rotate(${rot})"><g class="fitbox" data-pad="22" data-anchor="middle"><rect x="-100" y="${-size * 0.95}" width="200" height="${size * 1.5}" rx="10" fill="${CREAM}" stroke="${color}" stroke-width="7"/>` +
    t(0, size * 0.22, str, size, { w: 900, fill: color }) + `</g></g>`;
}
// labelled card (white panel) centred on x,y
function card(x, y, w, h, inner = "", { fill = "#fff", stroke = INK, sw = 6, rx = 20 } = {}) {
  return `<g transform="translate(${x} ${y})"><rect x="${-w / 2 + 7}" y="${-h / 2 + 9}" width="${w}" height="${h}" rx="${rx}" fill="${LGREY}"/>` +
    `<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>${inner}</g>`;
}

// ---------- small objects (centred on 0,0) ----------
const bill = (w = 150) => { const h = w * 0.52; return W(`<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="${w * 0.07}" fill="${COLORS.bill}" stroke="${INK}" stroke-width="5"/><ellipse rx="${w * 0.2}" ry="${h * 0.32}" fill="${COLORS.billLight}" stroke="${DGREEN}" stroke-width="3"/>` + t(0, h * 0.17, "$1", h * 0.42, { w: 900, fill: DGREEN })); };
const coin = (r = 34, sym = "$") => W(`<circle r="${r}" fill="${GOLD}" stroke="${INK}" stroke-width="5"/><circle r="${r * 0.72}" fill="none" stroke="${COLORS.goldDark}" stroke-width="3"/>` + t(0, r * 0.36, sym, r, { w: 900, fill: COLORS.goldDark }));
// a pizza slice (a share); tip at the bottom
const slice = (s = 1, { fill = "#ffd27a", crumb = false } = {}) => g(0, 0, s, W(`<path d="M 0 90 L -62 -70 Q 0 -100 62 -70 Z" fill="${fill}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><path d="M -56 -54 Q 0 -82 56 -54" fill="none" stroke="#e8573f" stroke-width="14"/><circle cx="-8" cy="-14" r="12" fill="#b8352a" stroke="${INK}" stroke-width="3"/><circle cx="14" cy="24" r="9" fill="#b8352a" stroke="${INK}" stroke-width="3"/>` +
  (crumb ? `<path d="M 0 90 L -14 54 L 14 54 Z" fill="${GREEN}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>` : "")));
const crumb = (s = 1) => g(0, 0, s, W(`<path d="M 0 26 L -20 -18 Q 0 -28 20 -18 Z" fill="#ffd27a" stroke="${DGREEN}" stroke-width="6" stroke-linejoin="round"/>`));
function priceTag(str, { color = "#fff", size = 44, w = 230 } = {}) {
  return W(`<path d="M ${-w / 2} 0 L ${-w / 2 + 46} -50 H ${w / 2} V 50 H ${-w / 2 + 46} Z" fill="${color}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><circle cx="${-w / 2 + 44}" cy="0" r="10" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>`) + t(24, size * 0.34, str, size, { w: 900, max: w - 90 });
}
function person({ shirt = BLUE, skin = 0, hair = "short", hairColor = "#3a2a1c", glasses = false, label = null, mouth = "smile", s = 1 } = {}) {
  let o = `<path d="M -74 100 Q -80 -52 0 -58 Q 80 -52 74 100 Z" fill="${shirt}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`;
  if (hair === "long") o += `<path d="M -54 -120 Q -64 -40 -50 -30 L 50 -30 Q 64 -40 54 -120 Z" fill="${hairColor}" stroke="${INK}" stroke-width="5"/>`;
  o += `<circle cx="0" cy="-116" r="48" fill="${SKIN[skin]}" stroke="${INK}" stroke-width="6"/>`;
  if (hair === "bun") o += `<circle cx="0" cy="-176" r="20" fill="${hairColor}" stroke="${INK}" stroke-width="5"/>`;
  if (hair !== "none") o += `<path d="M -48 -118 Q -52 -172 0 -168 Q 52 -172 48 -118 Q 22 -148 -48 -118 Z" fill="${hairColor}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>`;
  o += `<circle cx="-17" cy="-112" r="5" fill="${INK}"/><circle cx="17" cy="-112" r="5" fill="${INK}"/>`;
  if (glasses) o += `<circle cx="-17" cy="-112" r="14" fill="none" stroke="${INK}" stroke-width="4"/><circle cx="17" cy="-112" r="14" fill="none" stroke="${INK}" stroke-width="4"/><path d="M -3 -112 H 3" stroke="${INK}" stroke-width="4"/>`;
  o += mouth === "smile" ? `<path d="M -14 -92 Q 0 -80 14 -92" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`
    : mouth === "flat" ? `<path d="M -12 -88 H 12" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`
    : `<path d="M -14 -84 Q 0 -96 14 -84" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
  return g(0, 0, s, W(o) + (label ? t(0, 146, label, 34, { w: 800 }) : ""));
}
const teacher = (label = "Retired teacher", s = 1) => person({ shirt: PURPLE, skin: 0, hair: "bun", hairColor: "#b9bcc2", glasses: true, label, s });
function phone(inner = "", { s = 1 } = {}) {
  return g(0, 0, s, W(`<rect x="-170" y="-310" width="340" height="620" rx="46" fill="${INK}"/><rect x="-150" y="-286" width="300" height="572" rx="28" fill="#fff"/><rect x="-44" y="-300" width="88" height="14" rx="7" fill="#444"/>`) + inner);
}
const appleIcon = (s = 1, fill = "#9aa0a8") => g(0, 0, s, W(`<path d="M 0 -30 C -40 -52 -62 -12 -50 22 C -40 52 -16 58 0 46 C 16 58 40 52 50 22 C 62 -12 40 -52 0 -30 Z" fill="${fill}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><path d="M 2 -34 Q 6 -62 30 -66 Q 28 -40 2 -34 Z" fill="${GREEN}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>`));
const buyBtn = (label = "BUY $1", w = 230) => `<rect x="${-w / 2}" y="-40" width="${w}" height="80" rx="40" fill="${GREEN}" stroke="${INK}" stroke-width="5"/>` + t(0, 15, label, 40, { w: 900, fill: "#fff" });
// app screen: Apple + buy button
const appScreen = (extra = "") => g(0, -150, 0.9, appleIcon()) + t(0, -46, "Apple", 46, { w: 900 }) + g(0, 150, 1, buyBtn()) + extra;

// ---------- buildings (base line at y = 0, centred on x = 0) ----------
function tower(label, { w = 220, h = 330, fill = "#dfe6ee", sign = BLUE, sub = null } = {}) {
  let o = `<rect x="${-w / 2}" y="${-h}" width="${w}" height="${h}" fill="${fill}" stroke="${INK}" stroke-width="6"/>`;
  const cols = Math.max(2, Math.floor(w / 60)), rows = Math.floor((h - 110) / 56);
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) o += `<rect x="${-w / 2 + 24 + c * ((w - 48) / cols) + 4}" y="${-h + 78 + r * 56}" width="${(w - 48) / cols - 12}" height="34" fill="#fff" stroke="${INK}" stroke-width="3"/>`;
  o += `<rect x="-22" y="-58" width="44" height="58" fill="${INK}"/>`;
  o += `<rect x="${-w / 2 - 12}" y="${-h - 4}" width="${w + 24}" height="58" rx="8" fill="${sign}" stroke="${INK}" stroke-width="5"/>`;
  return W(o) + t(0, -h + 38, label, 32, { w: 900, fill: "#fff", max: w - 6 }) + (sub ? t(0, 44, sub, 30, { w: 800 }) : "");
}
function bank(label, { w = 420, sub = null, fill = "#eef0f2" } = {}) {
  let o = `<rect x="${-w / 2 - 20}" y="-24" width="${w + 40}" height="24" fill="#cfd4da" stroke="${INK}" stroke-width="5"/>`;
  o += `<rect x="${-w / 2}" y="-230" width="${w}" height="206" fill="${fill}" stroke="${INK}" stroke-width="6"/>`;
  const n = Math.max(4, Math.round(w / 90));
  for (let i = 0; i < n; i++) o += `<rect x="${-w / 2 + 26 + i * ((w - 52 - 34) / (n - 1))}" y="-218" width="34" height="194" rx="6" fill="#fff" stroke="${INK}" stroke-width="5"/>`;
  o += `<rect x="${-w / 2 - 14}" y="-296" width="${w + 28}" height="66" fill="#fff" stroke="${INK}" stroke-width="6"/>`;
  o += `<path d="M ${-w / 2 - 30} -296 L 0 -392 L ${w / 2 + 30} -296 Z" fill="${fill}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`;
  return W(o) + t(0, -250, label, 36, { w: 900, max: w - 10 }) + (sub ? t(0, 44, sub, 30, { w: 800 }) : "");
}
function booth(label, { w = 380, awning = RED, board = null, sub = null } = {}) {
  let o = `<rect x="${-w / 2}" y="-250" width="${w}" height="250" fill="#fff" stroke="${INK}" stroke-width="6"/>`;
  o += `<rect x="${-w / 2 + 24}" y="-200" width="${w - 48}" height="96" fill="${LBLUE}" stroke="${INK}" stroke-width="5"/>`;
  o += `<rect x="${-w / 2 - 14}" y="-104" width="${w + 28}" height="26" fill="#c89b62" stroke="${INK}" stroke-width="5"/>`;
  const n = 6;
  for (let i = 0; i < n; i++) o += `<path d="M ${-w / 2 - 20 + i * ((w + 40) / n)} -306 h ${(w + 40) / n} l 0 44 q ${-(w + 40) / n / 2} 26 ${-(w + 40) / n} 0 Z" fill="${i % 2 ? "#fff" : awning}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>`;
  o += `<rect x="${-w / 2 + 10}" y="-372" width="${w - 20}" height="62" rx="8" fill="${INK}"/>`;
  return W(o) + t(0, -328, label, 34, { w: 900, fill: "#fff", max: w - 40 }) + (board || "") + (sub ? t(0, 44, sub, 30, { w: 800 }) : "");
}
function house({ roof = "old", w = 320 } = {}) {
  let o = `<rect x="${-w / 2}" y="-190" width="${w}" height="190" fill="#fbe9c6" stroke="${INK}" stroke-width="6"/>`;
  o += `<rect x="-34" y="-110" width="68" height="110" fill="#9c6b3f" stroke="${INK}" stroke-width="5"/><circle cx="18" cy="-54" r="6" fill="${GOLD}"/>`;
  o += `<rect x="${-w / 2 + 30}" y="-140" width="64" height="60" fill="${LBLUE}" stroke="${INK}" stroke-width="5"/><rect x="${w / 2 - 94}" y="-140" width="64" height="60" fill="${LBLUE}" stroke="${INK}" stroke-width="5"/>`;
  const rf = roof === "new" ? RED : "#9a8f85";
  o += `<path d="M ${-w / 2 - 40} -190 L 0 -340 L ${w / 2 + 40} -190 Z" fill="${rf}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`;
  if (roof === "old") o += `<path d="M -60 -250 l 34 -8 l 10 30 l -30 14 Z" fill="${INK}"/><path d="M 40 -232 l 40 4 l -6 26 l -36 -4 Z" fill="#6f665e" stroke="${INK}" stroke-width="4"/><path d="M -110 -214 h 44 M 84 -206 h 40 M -10 -290 h 34" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
  else o += `<path d="M -120 -214 h 240 M -84 -250 h 168 M -46 -290 h 92" stroke="#8f2a1f" stroke-width="5" stroke-linecap="round"/>` + sparkle(150, -300) + sparkle(-170, -250, 0.7);
  return W(o);
}
const sparkle = (x, y, s = 1) => `<path transform="translate(${x} ${y}) scale(${s})" d="M 0 -30 L 8 -8 L 30 0 L 8 8 L 0 30 L -8 8 L -30 0 L -8 -8 Z" fill="${GOLD}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`;
function rack({ n = 3 } = {}) {
  let o = "";
  for (let k = 0; k < n; k++) {
    const x = (k - (n - 1) / 2) * 150;
    o += `<rect x="${x - 62}" y="-270" width="124" height="270" rx="8" fill="#2c333b" stroke="${INK}" stroke-width="6"/>`;
    for (let r = 0; r < 6; r++) o += `<rect x="${x - 48}" y="${-252 + r * 40}" width="96" height="26" rx="4" fill="#20252b"/><circle cx="${x - 34}" cy="${-239 + r * 40}" r="5" fill="${(r + k) % 3 ? "#5fe08f" : GOLD}"/><path d="M ${x - 14} ${-239 + r * 40} h 50" stroke="#59636e" stroke-width="4"/>`;
  }
  return W(o);
}
function signpost(text1, text2 = null, { fill = GREEN, w = 420 } = {}) {
  return W(`<rect x="-9" y="-40" width="18" height="170" fill="#8a8f98" stroke="${INK}" stroke-width="4"/><rect x="${-w / 2}" y="${text2 ? -170 : -140}" width="${w}" height="${text2 ? 140 : 100}" rx="14" fill="${fill}" stroke="${INK}" stroke-width="6"/>`) +
    t(0, text2 ? -112 : -76, text1, 36, { w: 900, fill: "#fff", max: w - 30 }) + (text2 ? t(0, -64, text2, 36, { w: 900, fill: "#fff", max: w - 30 }) : "");
}
function calendar(top, big, { sub = null, color = RED, w = 250 } = {}) {
  return W(`<rect x="${-w / 2}" y="-130" width="${w}" height="260" rx="16" fill="#fff" stroke="${INK}" stroke-width="6"/><path d="M ${-w / 2} -62 V -114 Q ${-w / 2} -130 ${-w / 2 + 16} -130 H ${w / 2 - 16} Q ${w / 2} -130 ${w / 2} -114 V -62 Z" fill="${color}" stroke="${INK}" stroke-width="6"/><rect x="${-w / 4 - 8}" y="-150" width="16" height="40" rx="8" fill="${INK}"/><rect x="${w / 4 - 8}" y="-150" width="16" height="40" rx="8" fill="${INK}"/>`) +
    t(0, -80, top, 34, { w: 900, fill: "#fff", max: w - 24 }) + t(0, sub ? 36 : 54, big, sub ? 76 : 84, { w: 900, max: w - 30 }) + (sub ? t(0, 96, sub, 34, { w: 800, fill: GREY, max: w - 24 }) : "");
}
function clock(h, m, { r = 90 } = {}) {
  const ha = ((h % 12) + m / 60) / 12 * Math.PI * 2 - Math.PI / 2, ma = m / 60 * Math.PI * 2 - Math.PI / 2;
  let o = `<circle r="${r}" fill="#fff" stroke="${INK}" stroke-width="7"/>`;
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; o += `<path d="M ${Math.cos(a) * r * 0.8} ${Math.sin(a) * r * 0.8} L ${Math.cos(a) * r * 0.9} ${Math.sin(a) * r * 0.9}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`; }
  o += `<path d="M 0 0 L ${Math.cos(ha) * r * 0.5} ${Math.sin(ha) * r * 0.5}" stroke="${INK}" stroke-width="9" stroke-linecap="round"/><path d="M 0 0 L ${Math.cos(ma) * r * 0.74} ${Math.sin(ma) * r * 0.74}" stroke="${INK}" stroke-width="6" stroke-linecap="round"/><circle r="7" fill="${RED}"/>`;
  return W(o);
}
const bell = (s = 1) => g(0, 0, s, W(`<path d="M -60 40 Q -52 -70 0 -76 Q 52 -70 60 40 Z" fill="${GOLD}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><rect x="-74" y="36" width="148" height="20" rx="10" fill="${GOLD}" stroke="${INK}" stroke-width="6"/><circle cx="0" cy="68" r="14" fill="${COLORS.goldDark}" stroke="${INK}" stroke-width="5"/><rect x="-10" y="-96" width="20" height="24" rx="6" fill="${INK}"/><path d="M 92 -40 q 20 26 0 56 M 116 -58 q 30 44 0 92 M -92 -40 q -20 26 0 56 M -116 -58 q -30 44 0 92" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`));
function ticket(l1, l2 = null, { color = "#ffd9a0", w = 300 } = {}) {
  return W(`<path d="M ${-w / 2} -70 H ${w / 2} V -22 a 22 22 0 0 0 0 44 V 70 H ${-w / 2} V 22 a 22 22 0 0 0 0 -44 Z" fill="${color}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><path d="M ${w / 2 - 70} -62 V 62" stroke="${INK}" stroke-width="4" stroke-dasharray="9 9"/>`) +
    t(-30, l2 ? -8 : 14, l1, 36, { w: 900, max: w - 120 }) + (l2 ? t(-30, 36, l2, 28, { w: 800, fill: GREY, max: w - 120 }) : "");
}
function doc(title, rows = [], { w = 440, h = null, fill = "#fff", titleFill = INK, size = 32, hl = -1 } = {}) {
  h = h || 110 + rows.length * (size * 1.55);
  let o = W(`<rect x="${-w / 2 + 8}" y="${-h / 2 + 10}" width="${w}" height="${h}" rx="12" fill="${LGREY}"/><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="12" fill="${fill}" stroke="${INK}" stroke-width="6"/><path d="M ${-w / 2 + 26} ${-h / 2 + 76} H ${w / 2 - 26}" stroke="${INK}" stroke-width="4"/>`);
  o += t(0, -h / 2 + 54, title, 34, { w: 900, fill: titleFill, max: w - 40 });
  rows.forEach((r, i) => {
    const y = -h / 2 + 76 + (i + 0.72) * (size * 1.55);
    if (i === hl) o += `<rect x="${-w / 2 + 14}" y="${y - size * 1.02}" width="${w - 28}" height="${size * 1.45}" rx="8" fill="${YEL}"/>`;
    o += t(-w / 2 + 34, y, r, size, { w: 700, anchor: "start", max: w - 60 });
  });
  return o;
}
function basket({ w = 360 } = {}) {
  let o = `<path d="M ${-w / 2 + 30} -60 Q 0 -300 ${w / 2 - 30} -60" fill="none" stroke="#8a5a2b" stroke-width="16" stroke-linecap="round"/><path d="M ${-w / 2 + 30} -60 Q 0 -300 ${w / 2 - 30} -60" fill="none" stroke="${INK}" stroke-width="3" transform="translate(0 -9)"/>`;
  o += `<path d="M ${-w / 2} -70 H ${w / 2} L ${w / 2 - 44} 110 H ${-w / 2 + 44} Z" fill="#d9a560" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`;
  for (let i = 1; i < 4; i++) o += `<path d="M ${-w / 2 + i * 11} ${-70 + i * 45} H ${w / 2 - i * 11}" stroke="#8a5a2b" stroke-width="5"/>`;
  for (let i = 1; i < 8; i++) o += `<path d="M ${-w / 2 + i * (w / 8)} -70 L ${-w / 2 + 44 + i * ((w - 88) / 8)} 110" stroke="#8a5a2b" stroke-width="4"/>`;
  o += `<rect x="${-w / 2 - 12}" y="-86" width="${w + 24}" height="28" rx="12" fill="#c08a45" stroke="${INK}" stroke-width="6"/>`;
  return W(o);
}
function shield(label, { s = 1, fill = BLUE } = {}) {
  return g(0, 0, s, W(`<path d="M 0 -130 L 110 -92 V 0 Q 110 96 0 140 Q -110 96 -110 0 V -92 Z" fill="${fill}" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/><path d="M 0 -104 L 86 -74 V 0 Q 86 78 0 112 Q -86 78 -86 0 V -74 Z" fill="none" stroke="#fff" stroke-width="4" opacity="0.7"/>`) + t(0, 20, label, 52, { w: 900, fill: "#fff", max: 170 }));
}
// simple chart: pts in 0..1 space, drawn into w x h with origin bottom-left at (0,0)
function chart(pts, { w = 700, h = 360, color = GREEN, sw = 9, axes = true, area = false, xl = null, yl = null } = {}) {
  const d = pts.map(([x, y], i) => `${i ? "L" : "M"} ${(x * w).toFixed(1)} ${(-y * h).toFixed(1)}`).join(" ");
  let o = "";
  if (area) o += `<path d="${d} L ${w} 0 L 0 0 Z" fill="${color}" opacity="0.15"/>`;
  if (axes) o += `<path d="M 0 ${-h - 10} V 0 H ${w + 10}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`;
  o += `<path d="${d}" fill="none" stroke="${color}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round"/>`;
  return W(o) + (xl ? t(w / 2, 48, xl, 28, { w: 800, fill: GREY }) : "") + (yl ? t(-18, -h - 26, yl, 28, { w: 800, fill: GREY, anchor: "start" }) : "");
}
function candles(n = 9, { w = 520, h = 280, seed = 3 } = {}) {
  let o = `<path d="M 0 ${-h - 10} V 0 H ${w + 10}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`, v = 0.35, r = seed;
  const rnd = () => ((r = (r * 9301 + 49297) % 233280) / 233280);
  for (let i = 0; i < n; i++) {
    const up = rnd() > 0.42, body = 0.08 + rnd() * 0.14, o1 = v, c1 = Math.max(0.08, Math.min(0.9, v + (up ? body : -body))), hi = Math.max(o1, c1) + 0.05 + rnd() * 0.06, lo = Math.min(o1, c1) - 0.04 - rnd() * 0.05;
    const x = (i + 0.7) * (w / (n + 0.4));
    o += `<path d="M ${x} ${-hi * h} V ${-Math.max(0.02, lo) * h}" stroke="${INK}" stroke-width="5"/><rect x="${x - 17}" y="${-Math.max(o1, c1) * h}" width="34" height="${Math.abs(c1 - o1) * h}" fill="${up ? GREEN : RED}" stroke="${INK}" stroke-width="4"/>`;
    v = c1;
  }
  return W(o);
}
function newspaper(head, { good = true } = {}) {
  return W(`<rect x="-150" y="-110" width="300" height="220" rx="8" fill="#fff" stroke="${INK}" stroke-width="6"/><rect x="-126" y="-88" width="252" height="50" fill="${good ? "#cfead7" : "#f6cfc9"}" stroke="${INK}" stroke-width="3"/><path d="M -126 -14 H 126 M -126 14 H 126 M -126 42 H 40 M -126 70 H 90" stroke="${LGREY}" stroke-width="9" stroke-linecap="round"/>`) + t(0, -52, head, 30, { w: 900, fill: good ? DGREEN : RED, max: 240 });
}
function checklist(items, states = [], { w = 760, size = 40, title = null } = {}) {
  const rh = size * 2.1, h = items.length * rh + (title ? 110 : 50);
  let o = W(`<rect x="${-w / 2 + 8}" y="${-h / 2 + 10}" width="${w}" height="${h}" rx="16" fill="${LGREY}"/><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="16" fill="#fff" stroke="${INK}" stroke-width="6"/><rect x="-70" y="${-h / 2 - 26}" width="140" height="46" rx="10" fill="#8a8f98" stroke="${INK}" stroke-width="5"/>`);
  if (title) o += t(0, -h / 2 + 70, title, 40, { w: 900, max: w - 60 });
  items.forEach((it, i) => {
    const y = -h / 2 + (title ? 110 : 50) + (i + 0.5) * rh, st = states[i] || "todo";
    o += W(`<rect x="${-w / 2 + 34}" y="${y - 28}" width="56" height="56" rx="10" fill="${st === "done" ? "#cfead7" : st === "active" ? YEL : "#fff"}" stroke="${INK}" stroke-width="5"/>`) + (st === "done" ? tick(-w / 2 + 62, y, 18, 8, DGREEN) : "");
    o += t(-w / 2 + 116, y + size * 0.35, it, size, { w: st === "todo" ? 700 : 900, anchor: "start", fill: st === "dim" ? LGREY : INK, max: w - 150 });
  });
  return o;
}
const thumbsUp = (s = 1) => g(0, 0, s, W(`<rect x="-90" y="-10" width="50" height="110" rx="10" fill="${BLUE}" stroke="${INK}" stroke-width="6"/><path d="M -40 0 Q 0 -30 0 -90 Q 40 -100 40 -30 H 96 Q 124 -24 112 6 Q 126 30 106 46 Q 112 72 88 80 Q 84 100 56 100 H -40 Z" fill="${SKIN[0]}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`));
const scaleIcon = (s = 1) => g(0, 0, s, W(`<rect x="-130" y="40" width="260" height="70" rx="14" fill="#cfd4da" stroke="${INK}" stroke-width="6"/><rect x="-150" y="6" width="300" height="34" rx="10" fill="#fff" stroke="${INK}" stroke-width="6"/><circle cx="0" cy="-70" r="70" fill="#fff" stroke="${INK}" stroke-width="6"/><path d="M 0 -70 L 34 -112" stroke="${RED}" stroke-width="7" stroke-linecap="round"/><circle cx="0" cy="-70" r="8" fill="${INK}"/><path d="M -48 -70 h 12 M 36 -70 h 12 M 0 -118 v 12" stroke="${INK}" stroke-width="5"/>`));
const ballotBox = (s = 1) => g(0, 0, s, W(`<rect x="-120" y="-30" width="240" height="140" rx="10" fill="${LBLUE}" stroke="${INK}" stroke-width="6"/><rect x="-136" y="-52" width="272" height="34" rx="8" fill="#fff" stroke="${INK}" stroke-width="6"/><rect x="-50" y="-42" width="100" height="12" rx="6" fill="${INK}"/><rect x="-40" y="-150" width="80" height="104" fill="#fff" stroke="${INK}" stroke-width="5" transform="rotate(8 0 -100)"/><path d="M -14 -104 l 12 14 l 26 -32" fill="none" stroke="${GREEN}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" transform="rotate(8 0 -100)"/>`));
const pocket = (s = 1) => g(0, 0, s, W(`<path d="M -150 -120 H 150 V 40 Q 150 150 0 160 Q -150 150 -150 40 Z" fill="#5b7fb5" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/><path d="M -126 -96 H 126 V 36 Q 126 126 0 136 Q -126 126 -126 36 Z" fill="none" stroke="#f0d9a0" stroke-width="5" stroke-dasharray="14 10"/>`));

const termTop = (meaning, full) => 992 - (84 + (Array.isArray(meaning) ? meaning : wrap(meaning, 54)).length * 44 + (full ? 40 : 0) + 14);
module.exports = { A, termTop, buck, hamlet, COLORS, WOBBLE_FILTER, P, INK, PAPER, GREEN, DGREEN, RED, GREY, LGREY, BLUE, LBLUE, YEL, GOLD, CREAM, ORANGE, PURPLE, SKIN,
  t, wrap, lines, g, W, dim, headline, chip, miniMap, termCard, bubble, arrow, cross, tick, stamp, card, bill, coin, slice, crumb, priceTag, person, teacher, phone, appleIcon, buyBtn, appScreen,
  tower, bank, booth, house, sparkle, rack, signpost, calendar, clock, bell, ticket, doc, basket, shield, chart, candles, newspaper, checklist, thumbsUp, scaleIcon, ballotBox, pocket };
