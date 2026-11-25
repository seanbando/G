// Stills S127–S164: the basket (index funds), history and drops, the three checks, the ending.
const L = require("./lib.js");
const { map, promises, formula, ticketScreen } = require("./scenes-a.js");
const { jag } = require("./scenes-c.js");
const { A, t, lines, g, W, dim, bubble, arrow, cross, tick, stamp, card, bill, coin, slice, crumb, priceTag, person, teacher, phone, appleIcon, appScreen,
  tower, bank, house, pocket, calendar, doc, basket, shield, chart, candles, checklist, thumbsUp, buck, hamlet, P, INK, GREEN, DGREEN, RED, GREY, LGREY, BLUE, LBLUE, YEL, GOLD, PAPER, ORANGE, PURPLE } = L;

// a basket with slices poking out; sizes = relative slice sizes
const fullBasket = (sizes = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]) => sizes.map((s, i) => g(-150 + i * (300 / (sizes.length - 1)), -110 - s * 30, s, slice(), (i - (sizes.length - 1) / 2) * 7)).join("") + basket();
const CHECKS = ["How big is the company?", "How does your order work?", "Is your brokerage a SIPC member?"];
const checks = (states) => g(960, 560, 1, checklist(CHECKS, states, { w: 980, size: 44, title: "3 CHECKS BEFORE YOU TAP BUY" }));
const growth = (() => { const pts = []; for (let y = 0; y <= 40; y += 2) pts.push([y / 40, (Math.pow(1.1, y)) / 48]); return pts; })();
// S&P-style line with two drops (shape only, not to scale)
const HIST = [[0, 0.3], [0.1, 0.38], [0.2, 0.46], [0.26, 0.5], [0.34, 0.24], [0.42, 0.36], [0.55, 0.52], [0.68, 0.66], [0.74, 0.72], [0.78, 0.5], [0.84, 0.74], [0.92, 0.86], [1, 0.95]];

const S = {};

// ---------- TODAY: THE BASKET ----------
// Numbers are not in the word timings, so number cues use "word>" (right after that word).
S.S127 = { h: "Picking single companies isn't the only way to own stocks",
  body: A(card(520, 570, 560, 420, g(0, -30, 1.6, slice()) + t(0, 170, "one company", 44, { w: 900 })), "single", "pop") + A(t(960, 590, "or", 70, { w: 900, fill: GREY }), "only", "pop") +
    A(card(1400, 570, 560, 420, t(0, 40, "?", 190, { w: 900, fill: DGREEN }) + t(0, 170, "another way", 44, { w: 900 }), { fill: YEL }), "way", "pop") };
S.S128 = { h: "An S&P 500 index fund: a basket holding slices of about 500 companies",
  body: A(g(640, 680, 1.3, fullBasket()), "basket", "pop") + A(card(1380, 560, 600, 240, t(0, -30, "about 500", 76, { w: 900, fill: DGREEN }) + t(0, 50, "companies in one basket", 40, { w: 900 })), "about>", "pop"),
  terms: [["S&P 500", "A list of about 500 of the biggest U.S. companies."], ["INDEX FUND", "A fund that simply buys everything on a list."]] };
S.S129 = { h: "You buy a slice of the fund, and the fund owns the companies for you",
  body: A(g(320, 620, 1, person({ shirt: BLUE, label: "You" })), "you", "pop") + A(arrow(460, 560, 700, 560, { color: DGREEN, label: "buy a slice of the fund", ldy: -30, lsize: 28 }), "buy", "wipe", { dir: "r", dur: 0.5 }) +
    A(g(960, 680, 1, fullBasket()) + t(960, 850, "THE FUND", 40, { w: 900 }), "fund", "pop") + A(arrow(1200, 560, 1340, 560, { color: GREY, label: "owns", ldy: -24 }), "owns", "wipe", { dir: "r", dur: 0.4 }) +
    A([0, 1, 2].map((i) => g(1420 + i * 120, 700, 0.42, tower(["A", "B", "C"][i], { w: 200, h: 300 + (i % 2) * 60, sign: [BLUE, ORANGE, PURPLE][i] }))).join("") + t(1540, 760, "the companies", 36, { w: 900 }), "companies", "pop") };
S.S130 = { h: "The biggest companies get the biggest weight in the basket",
  body: `<g transform="translate(-60 -50) scale(1.12)">` + A(g(820, 700, 1.05, fullBasket([1.5, 1.15, 0.9, 0.7, 0.55, 0.42, 0.34])), "start", "pop") + A(arrow(500, 450, 610, 520, { color: DGREEN }) + t(410, 430, "biggest company", 34, { w: 900, fill: DGREEN }), "biggest:2", "fade") +
    A(arrow(1240, 560, 1080, 580, { color: GREY }) + t(1420, 572, "smaller companies", 34, { w: 900, fill: GREY }), "basket", "fade") + `</g>` };
S.S131 = { body: A(`<g transform="translate(900 640) scale(2.9 0.75)">${buck("shocked")}</g>`, "start", "fade", { idle: "talk" }) + A(bubble(1320, 340, "So thin…", { tail: "left" }), "thin", "pop") };
S.S132 = { body: A(g(900, 520, 1.3, hamlet("proud")), "start", "slide", { dir: "d", idle: "talk" }) + g(900, 720, 1.5, basket({ w: 420 })) + A(bubble(1340, 300, "I'd sit in this.", { tail: "left" }), "sit", "pop") };
S.S133 = { h: "Over long periods, the S&P 500 has returned roughly 10% a year",
  body: A(g(300, 820, 1, chart(HIST, { w: 800, h: 460, color: GREEN, xl: "many years", area: true })), "long", "wipe", { dir: "r", dur: 2.2 }) +
    A(card(1460, 520, 560, 300, t(0, -70, "historically, roughly", 36, { w: 800, fill: GREY }) + t(0, 40, "10%", 130, { w: 900, fill: DGREEN }) + t(0, 114, "a year", 44, { w: 900 })), "roughly>", "pop"),
  term: ["RETURN", "How much an investment gained or lost over a period, shown as a percent."] };
S.S134 = { h: "That's history, not a promise",
  body: A(card(520, 480, 640, 180, t(0, -14, "with dividends reinvested", 42, { w: 900 }) + t(0, 44, "dividends used to buy more shares", 30, { fill: GREY })), "dividends", "pop") + A(card(520, 710, 640, 180, t(0, -14, "before inflation", 42, { w: 900 }) + t(0, 44, "not adjusted for rising prices", 30, { fill: GREY })), "inflation", "pop") +
    A(stamp(1300, 580, "HISTORY, NOT A PROMISE", { size: 48, rot: -6 }), "history", "stamp"),
  terms: [["REINVESTED", "Dividends used to buy more shares instead of being spent."], ["INFLATION", "Everyday prices rising over time, so a dollar buys less."]] };
// growth chart: the axes stay put; the curve draws on a word
const gchart = (full, on = null) => g(420, 820, 1, chart(growth.slice(0, 2), { w: 900, h: 460, color: GREEN }) + [0, 10, 20, 30, 40].map((y) => t(y / 40 * 900, 36, y, 28, { w: 800, fill: GREY })).join("") + t(450, 76, "years", 28, { w: 800, fill: GREY }) + g(0, -1 / 48 * 460 - 44, 1, t(10, 0, "$1", 40, { w: 900, anchor: "start" })) +
  (full ? (on ? A(chart(growth, { w: 900, h: 460, color: GREEN, area: true, axes: false }), on, "wipe", { dir: "r", dur: 2.4 }) : chart(growth, { w: 900, h: 460, color: GREEN, area: true, axes: false })) : ""));
S.S135 = { h: "What a steady 10% a year would do to one dollar", body: A(gchart(false), "start", "fade") + A(g(1520, 520, 1.6, bill(170)), "to>", "pop") + A(t(1520, 660, "10% a year, every year", 36, { w: 900 }), "steady>", "fade") };
S.S136 = { zoom: ["about>", 1150, 450, 1.07], h: "After 40 years of steady 10% growth, $1 becomes about $45", enter: "cut",
  body: gchart(true, "after") + A(card(1000, 400, 400, 200, t(0, -30, "after 40 years", 34, { w: 800, fill: GREY }) + t(0, 50, "about $45", 64, { w: 900, fill: DGREEN }), { fill: YEL }) + arrow(1210, 390, 1300, 392, { color: DGREEN }), "about>", "pop") };
S.S137 = { h: "Real markets don't move in a straight line, and the drops can be brutal",
  body: A(card(520, 570, 640, 440, t(0, -170, "STEADY (THE EXAMPLE)", 34, { w: 900, fill: GREY }) + g(-250, 150, 1, chart([[0, 0.1], [1, 0.9]], { w: 500, h: 240, color: GREY }))), "straight", "pop") +
    A(card(1400, 570, 640, 440, t(0, -170, "REAL MARKETS", 34, { w: 900, fill: RED }), { fill: "#fbe9e6" }), "real", "pop") + A(g(1150, 720, 1, chart(HIST, { w: 500, h: 240, color: RED })), "drops", "wipe", { dir: "r", dur: 1.0 }) };
const drop = (title, big, sub, pts, ons) => A(g(300, 820, 1, chart(pts, { w: 760, h: 460, color: RED, area: true })), ons[0], "wipe", { dir: "r", dur: 1.6 }) +
  A(card(1400, 520, 620, 340, t(0, -100, title, 38, { w: 900, fill: GREY, max: 560 }) + t(0, 20, big, 90, { w: 900, fill: RED, max: 560 }) + t(0, 104, sub, 36, { w: 900, max: 560 })), ons[1], "pop");
S.S138 = { h: "Late 2007 to early 2009: the S&P 500 lost more than half its value",
  body: drop("LATE 2007 TO EARLY 2009", "more than half", "of its value, gone", [[0, 0.9], [0.15, 0.84], [0.3, 0.74], [0.45, 0.66], [0.6, 0.5], [0.75, 0.36], [0.9, 0.3], [1, 0.34]], ["from", "lost"]) };
S.S139 = { h: "In 2020, it fell almost 34% in about a month",
  body: drop("FEB 19 TO MAR 23, 2020", "almost −34%", "in about a month", [[0, 0.8], [0.2, 0.84], [0.4, 0.9], [0.55, 0.7], [0.7, 0.52], [0.85, 0.36], [1, 0.3]], ["fell", "almost>"]) };
S.S140 = { h: "The broad index came back both times. A single company doesn't always.",
  body: A(card(520, 570, 640, 440, t(0, -170, "THE BROAD INDEX", 34, { w: 900, fill: DGREEN }) + g(-250, 150, 1, chart(HIST, { w: 500, h: 240, color: GREEN })) + A(stamp(170, 60, "CAME BACK", { color: GREEN, rot: -6, size: 34 }), "back", "stamp"), { fill: "#e6f4ea" }), "broad", "pop") +
    A(card(1400, 570, 640, 440, t(0, -170, "A SINGLE COMPANY", 34, { w: 900, fill: RED }) + g(-250, 150, 1, chart([[0, 0.6], [0.2, 0.7], [0.4, 0.5], [0.55, 0.2], [0.75, 0.1], [1, 0.06]], { w: 500, h: 240, color: RED })) + A(stamp(150, -40, "NOT ALWAYS", { rot: -6, size: 34 }), "always", "stamp"), { fill: "#fbe9e6" }), "single", "pop") };
S.S141 = { body: A(g(900, 640, 1.6, hamlet("sleeping")), "start", "fade", { idle: "bob" }) + A(bubble(1340, 380, "One eye open.", { tail: "left" }), "eye", "pop") };

// ---------- THREE CHECKS ----------
S.S142 = { h: "Three checks worth doing before you ever tap BUY", body: A(checks(["todo", "todo", "todo"]), "three", "pop") };
S.S143 = { h: "Check 1: the size of the company, not just the price of one share",
  body: A(g(520, 600, 0.8, P.pizza({ id: "c1", slices: 12 })), "size", "pop") + A(g(520, 600, 1, W(`<circle r="270" fill="none" stroke="${GREEN}" stroke-width="10" stroke-dasharray="20 14"/>`)) + t(520, 930, "the whole company", 40, { w: 900, fill: DGREEN }), "company", "pop") +
    A(g(1380, 560, 1.7, priceTag("1 share")), "not", "pop") + A(cross(1380, 560, 110, 16), "price", "stamp") + A(t(1380, 780, "not just this", 40, { w: 900, fill: RED }), "share", "fade") };
S.S144 = { h: "Price × shares tells you how big the pizza really is",
  body: formula(["Price of", "1 share"], ["Number of", "shares"], ["How big the", "pizza is"], YEL, ["price", "times", "shares", "tells", "big"]),
  term: ["MARKET CAP", "Price × number of shares. What the whole company is worth."] };
S.S145 = { h: "Check 2: how your order works",
  body: A(g(560, 590, 0.8, ticketScreen([["STOCK", "Apple"], ["AMOUNT", "$1"], ["ORDER TYPE", "MARKET"]], 2, "market")), "start", "slide", { dir: "u" }) + A(arrow(800, 560, 1020, 560, { color: DGREEN }), "market", "wipe", { dir: "r", dur: 0.4 }) +
    A(card(1380, 560, 640, 220, t(0, -30, "A market order takes", 46, { w: 900 }) + t(0, 36, "the available price", 46, { w: 900 })), "takes", "pop") };
S.S146 = { h: "Your app should explain its order types and how it routes your orders",
  body: A(g(560, 590, 0.8, phone(t(0, -210, "HELP", 34, { w: 900, fill: GREY }) + [["Order types", -110], ["How we route", 10], ["your orders", 56]].map(([l, y]) => t(0, y, l, 34, { w: 900 })).join("") + `<rect x="-130" y="-160" width="260" height="80" rx="12" fill="none" stroke="${INK}" stroke-width="4"/><rect x="-130" y="-40" width="260" height="120" rx="12" fill="none" stroke="${INK}" stroke-width="4"/>`)), "start", "slide", { dir: "u" }) +
    A(card(1360, 560, 640, 220, t(0, -30, "Read both before", 46, { w: 900 }) + t(0, 36, "you tap BUY", 46, { w: 900 })), "explain", "pop"),
  term: ["ORDER ROUTING", "Where your broker sends your order to get it filled."] };
S.S147 = { h: "Check 3: is your brokerage a SIPC member, and what does that cover?",
  body: A(g(1340, 800, 1, tower("YOUR BROKERAGE", { w: 320, h: 360 })), "brokerage", "pop") + A(g(620, 600, 1.6, shield("SIPC")), "sipc", "stamp") + A(t(1340, 380, "member?", 50, { w: 900, fill: DGREEN }), "member", "pop"),
  term: ["SIPC", "It protects customers if a brokerage firm fails. It does not protect against a stock falling.", "Securities Investor Protection Corporation"] };
S.S148 = { h: "If a member firm fails with customer assets missing, SIPC can help recover them",
  body: A(g(520, 820, 1.1, tower("BROKERAGE", { w: 320, h: 360, fill: "#d9d5cb", sign: GREY })), "firm", "pop") + A(W(`<path d="M 470 420 l 40 90 l -50 60 l 60 100 l -30 80" fill="none" stroke="${INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>`), "fails", "wipe", { dir: "d", dur: 0.3 }) + A(stamp(520, 330, "FAILED", { rot: -6 }), "fails", "stamp", { delay: 0.2 }) +
    A(g(1560, 600, 0.9, person({ shirt: BLUE, label: "Customer" })), "customer", "pop") + A(g(1040, 600, 1.2, shield("SIPC")), "sipc", "stamp") +
    A(arrow(1200, 560, 1420, 560, { color: DGREEN, width: 12 }) + g(1300, 470, 0.7, slice()) + g(1310, 660, 0.9, bill(120)), "recover", "wipe", { dir: "r", dur: 0.5 }),
  term: ["CUSTOMER ASSETS", "The shares and cash a brokerage holds for you."] };
S.S149 = { zoom: ["to>", 1200, 520, 1.06], h: "Protection goes up to $500,000 per customer",
  body: A(g(420, 600, 1.2, shield("SIPC")), "start", "pop") + A(W(`<rect x="700" y="420" width="1000" height="130" rx="14" fill="#cfead7" stroke="${INK}" stroke-width="6"/>`), "to>", "wipe", { dir: "r", dur: 0.8 }) + A(t(1200, 640, "up to $500,000 per customer, in total", 46, { w: 900 }), "to>", "fade", { delay: 0.2 }) +
    A(W(`<rect x="700" y="420" width="500" height="130" rx="14" fill="${GREEN}" stroke="${INK}" stroke-width="6"/>`) + t(950, 500, "up to $250,000 in cash", 36, { w: 900, fill: "#fff", max: 460 }), "including>", "wipe", { dir: "r", dur: 0.6 }) + A(t(1200, 710, "(the cash limit is part of it)", 34, { fill: GREY }), "cash", "fade") };
S.S150 = { h: "That protection is for a failed brokerage, not for a stock that falls",
  body: A(card(520, 570, 640, 420, g(0, -40, 0.44, tower("BROKERAGE", { w: 300, h: 320, sign: GREY })) + t(0, 110, "Your brokerage fails", 44, { w: 900 }) + t(0, 174, "COVERED", 46, { w: 900, fill: DGREEN }) + g(240, -150, 1, W(`<circle r="44" fill="${GREEN}" stroke="${INK}" stroke-width="6"/>`) + tick(0, 2, 20, 9, "#fff")), { fill: "#e6f4ea" }), "failed", "pop") +
    A(card(1400, 570, 640, 420, g(-200, 20, 1, chart([[0, 0.9], [0.3, 0.7], [0.6, 0.4], [1, 0.1]], { w: 400, h: 160, color: RED })) + t(0, 110, "Your stock falls", 44, { w: 900 }) + t(0, 174, "NOT COVERED", 46, { w: 900, fill: RED }) + g(240, -150, 1, W(`<circle r="44" fill="${RED}" stroke="${INK}" stroke-width="6"/>`) + `<path d="M -18 -18 L 18 18 M 18 -18 L -18 18" stroke="#fff" stroke-width="9" stroke-linecap="round"/>`), { fill: "#fbe9e6" }), "not", "pop") };
S.S151 = { body: A(g(860, 620, 1.7, buck("annoyed")) + W(`<rect x="650" y="520" width="110" height="36" rx="10" fill="#f3d9b0" stroke="${INK}" stroke-width="5" transform="rotate(-20 705 538)"/>`), "start", "slide", { dir: "l", idle: "talk" }) + A(bubble(1300, 320, "My feelings?", { tail: "left" }), "feelings", "pop") };
S.S152 = { body: A(g(700, 640, 1.5, hamlet("proud")), "start", "fade", { idle: "talk" }) + A(g(1400, 620, 0.62, checklist(CHECKS, ["done", "done", "done"], { w: 940, size: 44 })), "checks", "pop") + A(bubble(1160, 300, "A list I trust.", { tail: "left" }), "trust", "pop") };
S.S153 = { h: "Promise three, done", body: promises(3, [1, 2, 3], [1, 2, 3], null, "promise>") + A(card(960, 830, 980, 96, t(0, 14, "None of these checks tells you what to buy.", 36, { w: 900 }), { fill: "#cfead7" }), "none", "pop") };

// ---------- ENDING ----------
S.S154 = { h: "The whole trip: from your pocket to a retired teacher's new roof", mapDone: 5, stop: 0, map: false,
  body: map(["done", "done", "done", "done", "done"], { x: 440, y: 380, s: 0.66 }) + A(g(310, 520, 0.5, pocket()) + g(310, 440, 0.6, bill(170)) + t(310, 660, "Your pocket", 32, { w: 900 }), "pocket", "pop") + A(g(1620, 640, 0.62, house({ roof: "new" })) + t(1620, 690, "New roof", 32, { w: 900 }), "roof", "pop") };
S.S155 = { zoom: ["tiny", 1400, 600, 1.07], h: "Apple never got your dollar, but you now own a tiny piece of Apple",
  body: A(g(480, 800, 1.05, tower("APPLE", { fill: "#e6e9ee", sign: "#6b7280", w: 260, h: 360 })) + g(480, 570, 0.6, appleIcon()), "apple", "pop") + A(card(480, 330, 420, 110, t(0, 14, "got $0 from your dollar", 32, { w: 900, fill: RED }), {}), "never", "pop") +
    A(g(1240, 640, 1.2, person({ shirt: BLUE, label: "You" })), "you", "pop") + A(g(1460, 520, 2.2, crumb()) + t(1540, 660, "a tiny piece", 40, { w: 900, fill: DGREEN }) + t(1540, 714, "of Apple", 40, { w: 900, fill: DGREEN }), "tiny", "pop") };
const me = (x, y, s = 1.1) => g(x, y, s, person({ shirt: GREEN, skin: 1, label: null }));
S.S156 = { h: "Before I ask you something, I'll go first with my own story", body: A(me(620, 620, 1.3), "start", "pop") + A(g(1260, 580, 1.3, doc("MY STORY", ["", "", ""], { w: 460 })), "story", "pop") };
const chipIcon = W(`<rect x="-110" y="-110" width="220" height="220" rx="20" fill="#2c333b" stroke="${INK}" stroke-width="7"/><rect x="-66" y="-66" width="132" height="132" rx="10" fill="#76b900" stroke="${INK}" stroke-width="5"/>` + [-70, -24, 24, 70].map((p) => `<path d="M ${p} -110 v -34 M ${p} 110 v 34 M -110 ${p} h -34 M 110 ${p} h 34" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>`).join(""));
S.S157 = { h: "The first stock I ever bought was Nvidia",
  body: me(480, 640) + A(g(1000, 540, 1.1, chipIcon) + t(1000, 780, "NVIDIA", 56, { w: 900 }), "nvidia", "pop") + A(card(1460, 540, 480, 200, t(0, -24, "one of the biggest", 38, { w: 900 }) + t(0, 34, "companies in the market", 38, { w: 900 })), "biggest", "pop"),
  term: ["NVIDIA", "A company that designs computer chips, including chips used for AI."] };
S.S158 = { h: "I think it's tied to where the world is heading", enter: "cut",
  body: me(480, 640) + g(980, 560, 0.9, chipIcon) + A(stamp(1380, 500, "MY REASON, NOT ADVICE", { size: 44, rot: -6 }), "reason", "stamp") + A(t(1380, 700, "This is not a tip to buy anything.", 36, { w: 800, fill: GREY }), "advice", "fade") };
S.S159 = { h: "The first time I opened a candlestick chart, I was completely lost",
  body: A(g(380, 640, 1.1, person({ shirt: GREEN, skin: 1, mouth: "sad" })), "start", "pop") + A(g(820, 800, 1.4, candles(11, { w: 620, h: 300 })), "candlestick", "wipe", { dir: "r", dur: 1.2 }) + A(t(380, 410, "? ? ?", 70, { w: 900, fill: RED }), "lost", "pop"),
  term: ["CANDLESTICK CHART", "A price chart made of bars. Each bar shows where the price started, ended, and its high and low."] };
S.S160 = { h: "I started learning about money because I want to be financially free",
  body: me(620, 640, 1.3) + A(W(`<circle cx="1320" cy="560" r="150" fill="${GOLD}" stroke="${INK}" stroke-width="7"/>` + [0, 1, 2, 3, 4, 5, 6].map((i) => { const a = Math.PI + i * Math.PI / 6; return `<path d="M ${1320 + Math.cos(a) * 180} ${560 + Math.sin(a) * 180} L ${1320 + Math.cos(a) * 230} ${560 + Math.sin(a) * 230}" stroke="${INK}" stroke-width="8" stroke-linecap="round"/>`; }).join("")), "financially", "slide", { dir: "u", dur: 1.0 }) +
    `<rect x="1040" y="714" width="560" height="170" fill="${PAPER}"/>` + W(`<path d="M 1060 710 H 1580" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>`),
  term: ["FINANCIALLY FREE", "Having enough money that you don't have to work just to pay the bills."] };
S.S161 = { body: g(900, 900, 1.6, house({ roof: "new" })) + A(g(900, 500, 0.85, buck("shocked")), "ended", "pop", { idle: "talk" }) + A(bubble(1380, 300, "I'm in the roof.", { tail: "left" }), "inside", "pop") };
S.S162 = { h: "Next time: how to read a candlestick chart without getting lost",
  body: A(card(960, 640, 900, 520, t(0, -200, "NEXT VIDEO", 36, { w: 900, fill: GREY }), { sw: 9 }), "start", "pop") + A(g(630, 840, 1.15, candles(12, { w: 580, h: 300, seed: 8 })), "candlestick", "wipe", { dir: "r", dur: 1.2 }) };
const cbubble = (x, y, ls, fill = "#fff") => g(x, y, 1, W(`<path d="M -330 -110 H 330 Q 360 -110 360 -80 V 60 Q 360 90 330 90 H -180 L -250 150 L -240 90 H -330 Q -360 90 -360 60 V -80 Q -360 -110 -330 -110 Z" fill="${fill}" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>`) + ls.map((l, i) => t(0, -30 + i * 60 + (ls.length === 1 ? 30 : 0), l, 44, { w: 900 })).join(""));
S.S163 = { h: "Tell me in the comments", body: A(cbubble(560, 520, ["Which stop", "surprised you most?"]), "which", "pop") + A(cbubble(1360, 620, ["What was your", "first stock?"], YEL), "what", "pop") };
S.S164 = { h: "If this made the stock market make more sense, a like really helps",
  body: A(g(960, 520, 1.7, thumbsUp()), "like", "stamp") + A(card(960, 850, 1000, 100, t(0, 14, "Not financial advice. For education only.", 38, { w: 900, fill: GREY }), {}), "start", "fade") };

module.exports = { S };
