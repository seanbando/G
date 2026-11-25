// Stills S001–S039: hook, the pizza device, stop 1 (your app).
const L = require("./lib.js");
const { A, t, lines, g, W, dim, bubble, arrow, cross, tick, stamp, card, bill, coin, slice, crumb, priceTag, person, phone, appleIcon, buyBtn, appScreen,
  tower, bank, booth, calendar, doc, checklist, pocket, buck, hamlet, P, INK, GREEN, DGREEN, RED, GREY, LGREY, BLUE, LBLUE, YEL, GOLD, PAPER } = L;

const POS = [[100, 158], [452, 245], [800, 128], [1157, 262], [1500, 183]];
// the road map, placed on the stage. states per stop; who = character svg standing on a stop
function map(states, { x = 200, y = 330, s = 0.95, at = null, who = null, extra = "" } = {}) {
  let o = g(x, y, s, P.roadMap({ states }) + extra);
  if (at && who) { const [px, py] = POS[at - 1]; o += g(x + px * s, y + (py - (at === 5 ? 190 : 118)) * s, 0.5, who); }
  return o;
}
const stopXY = (i, { x = 200, y = 330, s = 0.95 } = {}) => [x + POS[i - 1][0] * s, y + POS[i - 1][1] * s];

// three promise cards; active = highlighted one, done = list of finished ones
const PROMISES = [["Who ends up", "holding your dollar"], ["Whose name is", "on your stock"], ["3 checks before", "you tap BUY"]];
function promises(active, done = [], show = [1, 2, 3], word = null) {
  let o = "";
  PROMISES.forEach((p, i) => {
    const n = i + 1, x = 400 + i * 560, on = n === active, isDone = done.includes(n), shown = show.includes(n) || isDone;
    const icon = n === 1 ? g(0, -70, 0.9, bill(170)) + W(`<path d="M -110 -20 Q -60 30 0 30 Q 60 30 110 -20" fill="none" stroke="${INK}" stroke-width="8" stroke-linecap="round"/>`)
      : n === 2 ? g(0, -66, 0.62, doc("STOCK", ["Name: ? ? ?"], { w: 380 }))
      : g(0, -64, 0.5, checklist(["", "", ""], ["done", "done", "done"], { w: 300, size: 34 }));
    let inner = t(0, -170, "PROMISE " + n, 34, { w: 900, fill: on || isDone ? DGREEN : GREY }) + (shown ? icon + t(0, 90, p[0], 40, { w: 900 }) + t(0, 150, p[1], 40, { w: 900 }) : t(0, 40, "?", 150, { w: 900, fill: LGREY }));
    if (isDone) inner += stamp(170, -214, "DONE", { color: GREEN, rot: 8, size: 44 });
    const c = card(x, 520, 480, 440, inner, { fill: on ? YEL : "#fff", sw: on ? 9 : 6 });
    o += on && word ? A(c, word, "pop") : on || isDone ? c : dim(c, shown ? 0.55 : 0.5);
  });
  return o;
}

const S = {};

// ---------- HOOK ----------
// A(...) tags say which spoken word each part appears on (see lib.js); stills ignore them.
S.S001 = { h: "You tap BUY on $1 of Apple stock…",
  body: A(g(520, 590, 0.82, phone(appScreen())), "start", "slide", { dir: "u" }) +
    A(W(`<circle cx="520" cy="712" r="74" fill="none" stroke="${GREEN}" stroke-width="7" stroke-dasharray="14 12"/>`), "buy", "pop") +
    A(g(1400, 760, 1, tower("APPLE", { fill: "#e6e9ee", sign: "#6b7280" })) + g(1400, 580, 0.5, appleIcon()), "apple", "pop") +
    A(arrow(730, 560, 1150, 560, { dash: "18 16", color: GREY }), "apple:2", "wipe", { dir: "r", dur: 0.5 }) + A(cross(940, 560, 46, 14), "none", "stamp") +
    A(card(1400, 310, 420, 150, t(0, -22, "Apple usually gets", 34) + t(0, 48, "$0", 54, { w: 900, fill: RED }), { fill: "#fff" }), "none", "pop", { delay: 0.2 }) };
S.S002 = { h: "Your dollar goes somewhere else",
  body: g(300, 600, 0.6, phone(appScreen())) +
    A(arrow(660, 440, 1540, 440, { dash: "18 16", curve: -40, color: GREY }), "goes", "wipe", { dir: "r", dur: 3 }) +
    [820, 1120, 1420].map((x, i) => A(g(x, 820, 0.8, tower("?", { fill: "#e3e0d6", sign: GREY, w: 200, h: 280 + (i % 2) * 50 })), "passes", "pop", { delay: i * 0.3 })).join("") +
    A(A(g(560, 440, 1, bill(150)), "dollar", "pop"), "goes", "move", { dx: 880, dy: 0, dur: 3 }) +
    A(t(1650, 500, "?", 150, { w: 900, fill: RED }), "way", "pop") + A(t(1120, 900, "…passing through several companies on the way", 36, { fill: GREY }), "several", "fade") };
S.S003 = { h: "Follow $1 from your pocket to Wall Street",
  body: A(g(320, 560, 0.9, pocket()) + t(320, 780, "Your pocket", 40, { w: 900 }), "start", "slide", { dir: "u" }) + A(g(320, 420, 1, bill(170)), "dollar", "pop", { idle: "bob" }) +
    A(W(`<path d="M 500 600 C 700 440, 820 760, 1040 620 S 1260 480, 1360 600" fill="none" stroke="${INK}" stroke-width="12" stroke-linecap="round"/><path d="M 500 600 C 700 440, 820 760, 1040 620 S 1260 480, 1360 600" fill="none" stroke="${PAPER}" stroke-width="4" stroke-dasharray="18 22"/>`), "pocket", "wipe", { dir: "r", dur: 1.2 }) +
    A(g(1540, 740, 0.9, bank("WALL STREET", { w: 380 })), "wall", "pop") };
S.S004 = { body: A(g(900, 600, 1.7, buck("annoyed")), "start", "slide", { dir: "l", idle: "talk" }) +
    A(W(`<rect x="1180" y="640" width="150" height="110" rx="14" fill="#c89b62" stroke="${INK}" stroke-width="7"/><path d="M 1225 640 v -30 h 60 v 30" fill="none" stroke="${INK}" stroke-width="7"/><path d="M 1180 690 h 150" stroke="${INK}" stroke-width="5"/>`), "travel", "pop") +
    A(bubble(1250, 330, "Nobody asked me.", { tail: "left" }), "nobody", "pop") };
S.S005 = { h: "By the end, you'll know…", body: promises(1, [], [1], "know") };
S.S006 = { h: "By the end, you'll know…", enter: "cut", body: promises(2, [], [1, 2], "whose") };
S.S007 = { body: W(`<path d="M 380 800 H 1540" stroke="${INK}" stroke-width="12" stroke-linecap="round"/><path d="M 470 800 v 60 M 1450 800 v 60" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>`) +
    A(g(820, 610, 1.5, hamlet("grumpy")), "start", "fade", { idle: "talk" }) +
    A(W(`<rect x="1150" y="640" width="250" height="134" rx="16" fill="none" stroke="${GREY}" stroke-width="6" stroke-dasharray="16 12"/>`) + t(1275, 720, "empty", 34, { fill: GREY }), "here", "fade") +
    A(bubble(1220, 400, "He was safe here.", { tail: "left" }), "perfectly", "pop") };
S.S008 = { h: "By the end, you'll know…", body: promises(3, [], [1, 2, 3], "three") };
S.S009 = { h: "The BUY button isn't as simple as it looks",
  body: A(g(420, 590, 0.82, phone(appScreen())), "start", "slide", { dir: "u" }) +
    A(W(`<path d="M 520 712 C 700 712, 640 420, 800 420 S 860 760, 1010 720 S 1080 380, 1230 440 S 1300 760, 1440 700 S 1560 470, 1640 520" fill="none" stroke="${INK}" stroke-width="9" stroke-linecap="round" stroke-dasharray="4 20"/>`), "route", "wipe", { dir: "r", dur: 1.6 }) +
    [[800, 420], [1010, 720], [1230, 440], [1440, 700], [1640, 520]].map(([x, y], i) => A(W(`<circle cx="${x}" cy="${y}" r="36" fill="#fff" stroke="${INK}" stroke-width="7"/>`) + t(x, y + 14, i + 1, 38, { w: 900 }), "route", "pop", { delay: 0.3 + i * 0.3 })).join("") +
    A(W(`<circle cx="420" cy="712" r="74" fill="none" stroke="${GREEN}" stroke-width="7" stroke-dasharray="14 12"/>`), "buy", "pop") };
S.S010 = { h: "This trip has 5 stops",
  anims: [{ sel: "#map", on: "trip", fx: "wipe", dir: "r", dur: 1.0 }, ...[1, 2, 3, 4, 5].map((i) => ({ sel: `#map-stop${i}`, on: "five", fx: "pop", delay: (i - 1) * 0.16 }))],
  body: map([]) + A(W(`<path d="M 630 520 Q 960 860 1290 560" fill="none" stroke="${GREY}" stroke-width="6" stroke-dasharray="14 14"/>`), "skip", "wipe", { dir: "r", dur: 0.6 }) +
    A(card(960, 800, 900, 96, t(0, 14, "One common route. Real orders can skip some stops.", 34), {}), "common", "pop") };
S.S011 = { enter: "cut", body: map([]) + A(g(300, 290, 0.9, buck("annoyed")), "start", "slide", { dir: "u", idle: "talk" }) +
    A(W(`<path d="M 440 200 q 14 22 0 36 q -14 -14 0 -36 Z" fill="${LBLUE}" stroke="${INK}" stroke-width="4"/>`), "walking", "pop") + A(bubble(760, 210, "That's a lot of walking.", { tail: "left" }), "lot", "pop") };

// ---------- THE DEVICE: WHAT YOUR DOLLAR BUYS ----------
// Numbers are not in the word timings (Whisper writes them as digits), so number cues use
// "word>" = right after that word ends, which is where the number is spoken.
S.S012 = { h: "First: what is your dollar actually buying?",
  body: A(g(620, 600, 1.4, buck("neutral")), "start", "slide", { dir: "l", idle: "bob" }) +
    A(W(`<rect x="1090" y="440" width="300" height="300" rx="20" fill="#fff" stroke="${INK}" stroke-width="8" stroke-dasharray="22 14"/>`) + t(1240, 650, "?", 190, { w: 900, fill: GREY }), "what", "pop") };
S.S013 = { h: "Picture a company as a pizza, cut into slices",
  body: A(g(480, 800, 1.1, tower("A COMPANY", { w: 260, h: 380 })), "company", "pop") + A(t(880, 620, "=", 150, { w: 900 }), "as", "pop") + A(g(1300, 570, 0.9, P.pizza({})), "pizza", "pop") };
S.S014 = { h: "One slice = one share",
  body: g(760, 560, 0.9, P.pizza({ highlight: 0 })) + A(arrow(1090, 470, 1240, 470, { color: DGREEN }), "slice:2", "wipe", { dir: "r", dur: 0.4 }) +
    A(g(1380, 470, 1.5, slice()), "slice:2", "pop", { delay: 0.25 }) + A(t(1380, 680, "1 share", 54, { w: 900, fill: DGREEN }), "share", "pop"),
  term: ["SHARE", "One small piece of ownership in a company."] };
S.S015 = { h: "The stock market is where people trade those slices",
  body: A(g(960, 760, 1, W(`<rect x="-560" y="-430" width="1120" height="60" rx="10" fill="${INK}"/><path d="M -520 -370 V 0 M 520 -370 V 0" stroke="${INK}" stroke-width="12"/>`) + t(0, -386, "STOCK MARKET", 40, { w: 900, fill: "#fff" })), "stock", "fade") +
    A(g(560, 640, 1, person({ shirt: BLUE })), "people", "pop") + A(g(1360, 640, 1, person({ shirt: L.ORANGE, skin: 1, hair: "long" })), "people", "pop", { delay: 0.15 }) +
    A(g(820, 500, 0.9, slice()) + arrow(700, 470, 1220, 470, { color: DGREEN, curve: -70, label: "slice", ldy: 62 }), "trade", "wipe", { dir: "r", dur: 0.6 }) +
    A(g(1100, 700, 1, bill(130)) + arrow(1220, 700, 700, 700, { color: GREY, curve: -70, label: "money", ldy: 84 }), "slices", "wipe", { dir: "l", dur: 0.6 }),
  term: ["STOCK MARKET", "The place where people buy and sell shares."] };
S.S016 = { h: "A simple example, with made-up numbers", example: false, anims: [{ sel: "#example-stamp", on: "made", fx: "stamp" }],
  body: A(g(560, 330, 1.25, P.exampleCard({ title: "EXAMPLE: A PIZZA SHOP", lines: ["How do slices work?", "", ""] })), "example", "pop") };
// the pizza shop: m = which word each part appears on
const shop = (value, per, { s = 0.78, hl = true, arrowDir = 0, note2 = null, m = {} } = {}) => {
  const T = (inner, key, fx = "pop", o = {}) => (m[key] ? A(inner, m[key], fx, o) : inner);
  const pie = g(660, 560, s, P.pizza({ slices: 100, highlight: hl ? 0 : null }));
  return (m.grow ? A(pie, m.grow, "scalefrom", { from: (0.78 / s).toFixed(3), dur: 0.9 }) : T(pie, "pizza")) +
    T(card(1340, 420, 560, 170, t(0, -18, "PIZZA SHOP", 32, { w: 900, fill: GREY }) + t(0, 44, "worth " + value, 60, { w: 900 })), "worth") +
    (per ? T(card(1340, 660, 560, 190, t(0, -26, "1 slice", 32, { w: 900, fill: GREY }) + t(0, 44, per, 64, { w: 900, fill: arrowDir < 0 ? RED : DGREEN }), { fill: YEL }), "per") +
      (hl ? T(arrow(660 + 300 * s + 14, 548, 1050, 640, { color: DGREEN, curve: 30 }), "arrow", "wipe", { dir: "r", dur: 0.4 }) : "") : "") +
    (note2 ? T(t(1340, 800, note2, 36, { w: 800 }), "note", "fade") : "") +
    (arrowDir ? T(arrow(1690, arrowDir > 0 ? 500 : 340, 1690, arrowDir > 0 ? 340 : 500, { color: arrowDir > 0 ? GREEN : RED, width: 16 }), "dir", "wipe", { dir: arrowDir > 0 ? "u" : "d", dur: 0.5 }) : "");
};
S.S017 = { h: "A pizza shop worth $100, cut into 100 slices", body: shop("$100", null, { hl: false, m: { pizza: "pizza", worth: "worth>" } }) + A(card(1340, 660, 560, 150, t(0, 18, "cut into 100 slices", 46, { w: 900 })), "cut", "pop") };
S.S018 = { h: "Each slice is worth $1", enter: "cut", body: shop("$100", "= $1", { note2: "1 slice of 100 = you own 1%", m: { arrow: "slice", per: "worth>", note: "owning:2" } }) };
S.S019 = { h: "The shop grows, and so does your slice", enter: "cut", body: shop("$200", "= $2", { s: 0.92, arrowDir: 1, m: { grow: "grows", dir: "grows", worth: "to>", per: "worth>" } }) };
S.S020 = { h: "The shop shrinks, and so does your slice", enter: "cut", body: shop("$50", "= 50¢", { s: 0.56, arrowDir: -1, m: { grow: "shrinks", dir: "shrinks", worth: "to>", per: "worth>" } }) };
S.S021 = { body: A(g(860, 600, 1.6, hamlet("hugging")), "start", "fade", { idle: "talk" }) + A(bubble(1300, 360, "Coins stay home.", { tail: "left" }), "coins", "pop") };
S.S022 = { h: "A price tag can fool you",
  body: A(g(620, 540, 1.6, priceTag("$500")), "price", "pop") + A(g(1300, 540, 1.6, priceTag("$5")), "tag", "pop") + A(t(960, 760, "Which company is bigger?", 50, { w: 900, fill: GREY }), "fool", "fade") };
const AB = (o = {}) => {
  const a = g(520, 560, 1, card(0, 0, 620, 520, t(0, -200, "COMPANY A", 40, { w: 900, fill: BLUE }) + (o.a || ""), { fill: o.hlA ? YEL : "#fff" }));
  const b = g(1400, 560, 1, card(0, 0, 620, 520, t(0, -200, "COMPANY B", 40, { w: 900, fill: L.ORANGE }) + (o.b || ""), { fill: o.hlB ? YEL : "#fff" }));
  const a2 = o.dimA ? dim(a, 0.4) : a, b2 = o.dimB ? dim(b, 0.4) : b;
  return (o.onA ? A(a2, o.onA, "slide", { dir: "l" }) : a2) + (o.onB ? A(b2, o.onB, "slide", { dir: "r" }) : b2) + (o.mid || "");
};
const shareTag = (p, on = null) => g(-110, -20, 1.3, slice()) + (on ? A(g(130, -30, 1.1, priceTag(p)), on, "pop") : g(130, -30, 1.1, priceTag(p))) + t(0, 190, "price of 1 share", 34, { fill: GREY });
S.S023 = { h: "Two companies, two share prices", body: AB({ a: shareTag("$500", "costs>"), b: shareTag("$5", "costs:2>"), onA: "company", onB: "company:2" }) };
S.S024 = { h: "The $500 share looks like the bigger company", enter: "cut",
  body: AB({ a: shareTag("$500"), b: shareTag("$5"), hlA: true, dimB: true }) + A(stamp(960, 880, "THAT'S THE TRAP", { size: 56, rot: -4 }), "trap", "stamp") };
const totalA = (on) => { const p = g(0, -40, 0.42, P.pizza({ id: "pa", slices: 3 })), l1 = t(0, 140, "3 slices × $500", 44, { w: 900 }), l2 = t(0, 208, "= $1,500", 56, { w: 900, fill: DGREEN });
  return on ? A(p, "three", "pop") + A(l1, "slices", "fade") + A(l2, "worth>", "pop") : p + l1 + l2; };
S.S025 = { h: "Company A is cut into only 3 slices", body: AB({ hlA: true, dimB: true, a: totalA(true), b: shareTag("$5") }) };
S.S026 = { h: "Company B is cut into a million slices", enter: "cut",
  body: AB({ hlB: true, dimA: true, a: totalA(false),
    b: A(g(0, -40, 0.5, P.pizza({ id: "pb", slices: 90 })), "million", "pop") + A(t(0, 140, "1,000,000 slices × $5", 40, { w: 900 }), "slices", "fade") + A(t(0, 208, "= $5,000,000", 56, { w: 900, fill: DGREEN }), "worth>", "pop") }) };
S.S027 = { h: "The cheap slice came from the far bigger pizza",
  body: A(g(480, 600, 0.3, P.pizza({ id: "pa", slices: 3 })) + t(480, 400, "COMPANY A", 38, { w: 900, fill: BLUE }) + t(480, 760, "$500 a slice", 36, { fill: GREY }) + t(480, 824, "whole pizza: $1,500", 44, { w: 900 }), "start", "fade") +
    A(g(1180, 540, 0.82, P.pizza({ id: "pb", slices: 90 })), "bigger", "pop") +
    A(t(1590, 330, "COMPANY B", 38, { w: 900, fill: L.ORANGE, max: 270 }) + t(1590, 400, "$5 a slice", 36, { fill: GREY }) + t(1590, 480, "whole pizza:", 40, { w: 900, max: 270 }) + t(1590, 550, "$5,000,000", 50, { w: 900, fill: DGREEN, max: 270 }), "cheap", "fade") };
// formula cards; ons = words for [card 1, ×, card 2, =, result]
const formula = (a, b, c, cFill = YEL, ons = null) => {
  const T = (inner, i) => (ons ? A(inner, ons[i], "pop") : inner);
  return T(card(400, 520, 440, 240, lines(0, a.length > 1 ? -14 : 16, a, 46, { w: 900, lh: 1.4 })), 0) + T(t(680, 550, "×", 110, { w: 900 }), 1) +
    T(card(960, 520, 440, 240, lines(0, b.length > 1 ? -14 : 16, b, 46, { w: 900, lh: 1.4 })), 2) + T(t(1240, 550, "=", 110, { w: 900 }), 3) +
    T(card(1520, 520, 440, 240, lines(0, c.length > 1 ? -14 : 16, c, 50, { w: 900, fill: DGREEN, lh: 1.4 }), { fill: cFill, sw: 9 }), 4);
};
S.S028 = { h: "Price × number of shares = market cap",
  body: formula(["Price of", "1 share"], ["Number of", "shares"], ["MARKET CAP"], YEL, ["price", "times", "number", "called", "market"]),
  term: ["MARKET CAP", "What the whole company is worth. Short for market capitalization."] };
S.S029 = { h: "Apple is cut into about 14.5 billion shares",
  body: A(g(560, 570, 0.8, P.pizza({ id: "apl", slices: 120 })) + g(560, 570, 1.5, appleIcon(1, "#f6f3ea")), "apple", "pop") +
    A(card(1340, 400, 640, 160, t(0, -18, "about 14.5 billion shares", 46, { w: 900 }) + t(0, 44, "each worth a few hundred dollars", 32, { fill: GREY })), "about>", "pop") +
    A(t(1340, 570, "=", 90, { w: 900 }), "value", "pop") + A(card(1340, 700, 640, 160, t(0, -14, "worth TRILLIONS", 56, { w: 900, fill: DGREEN }) + t(0, 48, "of dollars", 34, { fill: GREY }), { fill: YEL, sw: 9 }), "trillions", "pop") };
S.S030 = { body: A(g(860, 620, 1.7, buck("happy")), "start", "slide", { dir: "l", idle: "talk" }) + A(g(1130, 420, 1.6, crumb()), "crumb", "pop") + A(bubble(1330, 300, "My crumb!", { tail: "left" }), "proud", "pop") };

// ---------- STOP 1: YOUR APP ----------
S.S031 = { h: "Stop 1: the investing app on your phone", map: false,
  body: map(["active"], { at: 1, who: buck("neutral"), y: 380 }) + g(1700, 800, 0.36, phone(appScreen())) };
S.S032 = { h: "Tuesday morning: you buy $1 of Apple",
  body: g(560, 560, 1.4, calendar("MORNING", "TUE", {})) + g(1280, 590, 0.82, phone(appScreen())) + W(`<circle cx="1280" cy="712" r="74" fill="none" stroke="${GREEN}" stroke-width="7" stroke-dasharray="14 12"/>`) };
S.S033 = { h: "One share costs a few hundred dollars, so $1 buys a crumb",
  body: g(620, 540, 2.6, slice(1, { crumb: true })) + t(620, 830, "1 Apple share: a few hundred dollars", 36, { w: 800, max: 700 }) +
    arrow(700, 740, 1180, 600, { color: DGREEN, curve: 60 }) + g(1320, 540, 2.4, crumb()) + g(1320, 700, 1, bill(150)) + t(1560, 560, "your $1", 46, { w: 900, fill: DGREEN }) };
S.S034 = { h: "These crumbs are called fractional shares",
  body: g(520, 530, 1.9, slice()) + W(`<path d="M 520 420 v 250 M 440 500 h 160 M 468 580 h 104" stroke="${INK}" stroke-width="6" stroke-dasharray="12 10"/>`) +
    arrow(700, 530, 900, 530, {}) + [0, 1, 2, 3, 4, 5].map((i) => g(1040 + (i % 3) * 150, 460 + Math.floor(i / 3) * 150, 1.5, crumb())).join("") +
    t(1190, 730, "pieces of one share", 38, { w: 800 }) + g(1640, 540, 0.36, phone(appScreen())) + t(1640, 730, "sold by many big apps", 30, { fill: GREY, max: 300 }),
  term: ["FRACTIONAL SHARE", "A piece of one share, for when you buy less than a whole one."] };
const ticketScreen = (rows, hl) => phone(t(0, -210, "YOUR ORDER", 30, { w: 900, fill: GREY }) + rows.map((r, i) => (i === hl ? `<rect x="-136" y="${-166 + i * 92}" width="272" height="80" rx="12" fill="${YEL}" stroke="${INK}" stroke-width="4"/>` : "") + t(0, -134 + i * 92, r[0], 22, { w: 800, fill: GREY }) + t(0, -100 + i * 92, r[1], 34, { w: 900, max: 250 })).join("") + g(0, 210, 0.9, buyBtn("BUY")));
S.S035 = { h: "You place a market order",
  body: g(560, 570, 0.8, ticketScreen([["STOCK", "Apple"], ["AMOUNT", "$1"], ["ORDER TYPE", "MARKET"]], 2)) +
    arrow(800, 560, 1020, 560, { color: DGREEN }) + card(1380, 560, 640, 220, t(0, -30, "Buy right away,", 48, { w: 900 }) + t(0, 36, "at the available price", 48, { w: 900 })),
  term: ["MARKET ORDER", "An order to buy (or sell) right now, at whatever price is available."] };
S.S036 = { h: "The price can change before your order goes through",
  body: card(480, 520, 480, 250, t(0, -50, "Price you SAW", 36, { fill: GREY }) + g(0, 40, 1.2, priceTag("$ ? ? ?", { w: 260 }))) +
    g(960, 520, 0.9, L.clock(10, 10)) + arrow(760, 400, 1160, 400, { curve: -50, label: "a moment later", ldy: -40 }) +
    card(1440, 520, 480, 250, t(0, -50, "Price you GET", 36, { fill: GREY }) + g(0, 40, 1.2, priceTag("$ ? ? ?", { w: 260, color: YEL })), {}) +
    t(960, 760, "may not be exactly the same", 44, { w: 900, fill: RED }) };
S.S037 = { h: "Your broker may bundle your crumb with other orders",
  body: [0, 1, 2].map((i) => g(300, 380 + i * 170, 0.5, person({ shirt: [BLUE, L.ORANGE, L.PURPLE][i], skin: i, hair: i === 1 ? "long" : "short", label: i === 0 ? "You" : null })) + g(430, 370 + i * 170, 1, crumb()) + arrow(490, 370 + i * 170, 780, 520, { color: GREY, width: 6 })).join("") +
    g(960, 720, 1, tower("YOUR BROKER", { w: 280, h: 330 })) + arrow(1130, 540, 1380, 540, { color: DGREEN }) +
    W(`<rect x="1410" y="450" width="250" height="180" rx="16" fill="#fff" stroke="${INK}" stroke-width="7"/>`) + [0, 1, 2].map((i) => g(1470 + i * 65, 540, 1.1, crumb())).join("") + t(1535, 690, "one bigger order", 34, { w: 800 }),
  term: ["BROKER", "The company behind your investing app. It places your orders for you."] };
S.S038 = { h: "Your broker picks where the order goes",
  body: g(420, 760, 1, tower("YOUR BROKER", { w: 280, h: 330 })) +
    arrow(590, 500, 1050, 340, { color: DGREEN, curve: -30 }) + g(1280, 420, 0.5, bank("EXCHANGE", { w: 360 })) + t(1560, 360, "an exchange", 36, { w: 900, anchor: "start", max: 300 }) +
    arrow(600, 580, 1050, 580, { color: DGREEN }) + g(1280, 690, 0.5, booth("MARKET MAKER")) + t(1560, 610, "a market maker", 36, { w: 900, anchor: "start", max: 300 }) +
    arrow(560, 760, 760, 830, { color: DGREEN, curve: -160 }) + t(900, 842, "or fill it itself", 36, { w: 900, anchor: "start" }) };
S.S039 = { body: g(760, 600, 1, doc("ORDER #0001", ["Buy: $1 of Apple", "Type: market order", ""], { w: 560, size: 40 })) + g(760, 690, 0.62, buck("annoyed")) + stamp(1010, 440, "PAPERWORK", { rot: 10 }) + bubble(1330, 360, "No thank-you?", { tail: "left" }) };

module.exports = { S, map, stopXY, promises, formula, ticketScreen, POS };
