// Stills S086–S126: stop 5 (making it official), checkpoint 2, how a share makes money.
const L = require("./lib.js");
const { map, promises } = require("./scenes-a.js");
const { A, t, lines, g, W, dim, bubble, arrow, cross, tick, stamp, card, bill, coin, slice, crumb, priceTag, person, phone, appleIcon, appScreen,
  tower, bank, booth, calendar, clock, ticket, doc, shield, chart, newspaper, scaleIcon, ballotBox, buck, hamlet, P, INK, GREEN, DGREEN, RED, GREY, LGREY, BLUE, LBLUE, YEL, GOLD, PAPER, ORANGE, PURPLE } = L;

const coat = (color = "#6b7fa8") => W(`<path d="M 0 -150 q 0 -30 22 -30 q 22 0 22 20 q 0 16 -22 22 L 0 -128" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/><path d="M 0 -128 L -120 -70 L -100 150 H 100 L 120 -70 Z" fill="${color}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><path d="M 0 -128 V 150 M -40 -108 L 0 -40 L 40 -108" fill="none" stroke="${INK}" stroke-width="5"/>`);
const tag = (str, { fill = "#fff", w = 170 } = {}) => W(`<path d="M ${-w / 2} -50 H ${w / 2 - 30} L ${w / 2} 0 L ${w / 2 - 30} 50 H ${-w / 2} Z" fill="${fill}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><circle cx="${w / 2 - 36}" cy="0" r="9" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>`) + t(-18, 18, str, 50, { w: 900, max: w - 80 });
const stopwatch = (s = 1) => g(0, 0, s, W(`<rect x="-16" y="-124" width="32" height="30" rx="6" fill="${INK}"/><circle r="96" fill="#fff" stroke="${INK}" stroke-width="8"/><path d="M 0 0 L 40 -52" stroke="${RED}" stroke-width="8" stroke-linecap="round"/><circle r="8" fill="${INK}"/><path d="M 0 -80 v 14 M 80 0 h -14 M 0 80 v -14 M -80 0 h 14" stroke="${INK}" stroke-width="5"/>`));
const dtcc = (x, y, s = 1, label = "DTCC") => g(x, y, s, bank(label, { w: 360, fill: "#e4ecf5" }));

const S = {};

// ---------- STOP 5: MAKING IT OFFICIAL ----------
// "Cede" is not in the word timings (Whisper hears "and company"), so Cede cues use the word before it.
const WHOSE = "STOP 5 · WHOSE NAME IS ON YOUR STOCK";
S.S086 = { h: "Stop 5: where your trade becomes official", map: false, anims: [{ sel: "#map-stop5", on: "stop>", fx: "pop" }],
  body: map(["done", "done", "done", "done", "active"], { at: 5, who: buck("neutral"), y: 400, whoOn: "stop" }) };
S.S087 = { h: "Your trade is matched, but the paperwork isn't finished",
  body: A(card(520, 560, 520, 300, t(0, -30, "YOUR TRADE", 36, { w: 900, fill: GREY }) + t(0, 50, "MATCHED", 76, { w: 900, fill: DGREEN }) + g(190, -110, 1, W(`<circle r="40" fill="${GREEN}" stroke="${INK}" stroke-width="6"/>`) + tick(0, 2, 18, 9, "#fff")), { fill: "#cfead7" }), "matched", "pop") +
    A(arrow(820, 560, 1020, 560, {}), "but", "wipe", { dir: "r", dur: 0.3 }) + [0, 1, 2, 3].map((i) => A(g(1340 + i * 8, 640 - i * 46, 1, doc("PAPERWORK", ["", ""], { w: 440 }), (i % 2 ? 3 : -3)), "paperwork", "slide", { dir: "d", delay: i * 0.1 })).join("") + A(stamp(1500, 720, "NOT FINISHED", { rot: -8, size: 40 }), "finished", "stamp") };
S.S088 = { h: "Since May 28, 2024: most U.S. stock trades settle one business day later",
  body: A(g(480, 580, 1.4, calendar("MAY 2024", "28", { w: 280 })), "may", "pop") + A(card(1260, 480, 760, 190, t(-200, 22, "Trade day", 44, { w: 900 }) + t(20, 26, "+", 70, { w: 900, fill: DGREEN }) + t(210, 22, "1 business day", 44, { w: 900 })), "one", "pop") +
    A(card(1260, 720, 760, 130, t(0, 16, "= the trade is final", 46, { w: 900, fill: DGREEN }), { fill: YEL }), "later", "pop"),
  terms: [["SETTLE", "The trade is finished: the buyer has the shares and the seller has the money."], ["T+1", "Trade day plus 1 business day. That is when the trade settles."]] };
S.S089 = { h: "Your Tuesday trade is usually final on Wednesday",
  body: A(g(540, 540, 1.4, calendar("YOU TAP BUY", "TUE", { w: 280 })), "tuesday", "pop") + A(arrow(790, 540, 1130, 540, { color: DGREEN, width: 12, label: "1 business day", ldy: -30, lsize: 36 }), "usually", "wipe", { dir: "r", dur: 0.6 }) +
    A(g(1380, 540, 1.4, calendar("TRADE IS FINAL", "WED", { color: GREEN, w: 280 })), "wednesday", "pop") + A(g(1600, 380, 1, W(`<circle r="48" fill="${GREEN}" stroke="${INK}" stroke-width="6"/>`) + tick(0, 2, 22, 10, "#fff")), "wednesday", "stamp", { delay: 0.35 }) };
S.S090 = { h: "Behind the scenes, a group called the DTCC finishes the trade",
  body: g(340, 780, 0.8, tower("BUYER'S FIRM", { w: 260, h: 300 })) + g(1580, 780, 0.8, tower("SELLER'S FIRM", { w: 260, h: 300, sign: ORANGE })) + A(dtcc(960, 800, 1.05), "dtcc", "pop") +
    A(arrow(480, 560, 740, 560, { color: GREY, label: "money", ldy: -24 }) + arrow(1180, 560, 1440, 560, { color: GREY }), "clear", "wipe", { dir: "r", dur: 0.7 }) +
    A(arrow(1440, 660, 1180, 660, { color: DGREEN, label: "shares", ldy: 60 }) + arrow(740, 660, 480, 660, { color: DGREEN }), "settle", "wipe", { dir: "l", dur: 0.7 }),
  term: ["DTCC", "The behind-the-scenes group of companies that clears and settles stock trades in the U.S.", "Depository Trust & Clearing Corporation"] };
S.S091 = { h: "The DTCC companies do three jobs",
  body: [[g(0, -30, 0.62, shield("OK", { fill: GREEN })), ["Guarantee", "eligible trades"], "guarantee"], [W(`<rect x="-80" y="-130" width="160" height="200" rx="14" fill="#fff" stroke="${INK}" stroke-width="6"/><rect x="-60" y="-110" width="120" height="50" rx="6" fill="${LBLUE}" stroke="${INK}" stroke-width="4"/>`) + [0, 1, 2, 3, 4, 5].map((i) => `<rect x="${-58 + (i % 3) * 42}" y="${-44 + Math.floor(i / 3) * 46}" width="32" height="34" rx="6" fill="${LGREY}" stroke="${INK}" stroke-width="3"/>`).join(""), ["Work out what", "each firm owes"], "work"],
    [W(`<rect x="-100" y="-130" width="200" height="200" rx="16" fill="#8a8f98" stroke="${INK}" stroke-width="7"/><circle cx="0" cy="-30" r="56" fill="#cfd4da" stroke="${INK}" stroke-width="6"/><path d="M 0 -86 V 26 M -56 -30 H 56" stroke="${INK}" stroke-width="6"/><circle cx="0" cy="-30" r="12" fill="${INK}"/>`), ["Hold the", "shares"], "hold"]]
    .map(([icon, ls, on], i) => A(card(400 + i * 560, 550, 480, 450, t(0, -180, String(i + 1), 44, { w: 900, fill: GREY }) + g(0, 0, 1, icon) + t(0, 140, ls[0], 42, { w: 900 }) + t(0, 196, ls[1], 42, { w: 900 })), on, "pop")).join(""),
  terms: [["CLEAR", "Check the trade and work out who owes what."], ["SETTLE", "Swap the money and the shares. The trade is done."]] };
S.S092 = { body: A(g(860, 620, 1.6, hamlet("proud")), "start", "fade", { idle: "talk" }) + A(g(1240, 640, 1, W(`<rect x="-60" y="-34" width="120" height="68" rx="30" fill="${GOLD}" stroke="${INK}" stroke-width="6"/><rect x="50" y="-16" width="70" height="32" rx="8" fill="${GOLD}" stroke="${INK}" stroke-width="6"/><circle cx="-14" cy="0" r="14" fill="${INK}"/>`)), "referee", "pop") + A(bubble(1300, 340, "A money referee!", { tail: "left" }), "money", "pop") };
S.S093 = { h: "Now for the paperwork question from the start", chip: WHOSE,
  body: A(g(960, 580, 1.5, doc("YOUR STOCK", ["Registered name:", "? ? ? ? ?"], { w: 520, size: 40, hl: 1 })), "paperwork", "pop") };
S.S094 = { h: "Many shares are registered under one name: Cede & Co.", chip: WHOSE,
  body: g(960, 600, 1.4, doc("OFFICIAL RECORD", ["Registered name:", ""], { w: 560, size: 44, hl: 1 })) + `<g data-allow-overlap>${A(g(960, 600, 1.4, doc("OFFICIAL RECORD", ["Registered name:", "CEDE & CO."], { w: 560, size: 44, hl: 1 })), "name>", "fade", { dur: 0.25 })}</g>` +
    A(g(1560, 560, 0.5, phone(appScreen())) + t(1560, 760, "held through", 30, { fill: GREY }) + t(1560, 800, "a brokerage", 30, { fill: GREY }), "brokerages", "pop"),
  term: ["CEDE & CO.", "The name written on the official record for many shares that are held through brokerages. \"Cede\" is said like \"seed\"."] };
S.S095 = { h: "Cede & Co. is the name the Depository Trust Company uses", chip: WHOSE,
  body: g(1400, 520, 1.3, doc("OFFICIAL RECORD", ["CEDE & CO."], { w: 420, size: 44, hl: 0 })) + A(g(560, 820, 1.1, bank("DEPOSITORY TRUST CO.", { w: 480, fill: "#e4ecf5" })), "depository", "pop") + A(arrow(860, 520, 1100, 520, { label: "signs as", ldy: -24 }), "uses", "wipe", { dir: "r", dur: 0.5 }),
  term: ["DTC", "The DTCC company that holds the shares. On the official record it uses the name Cede & Co.", "Depository Trust Company"] };
S.S096 = { h: "It's a bit like a coat check at a restaurant", chip: WHOSE,
  body: A(W(`<path d="M 300 330 H 1620" stroke="${INK}" stroke-width="10" stroke-linecap="round"/><rect x="340" y="700" width="1240" height="40" fill="#c89b62" stroke="${INK}" stroke-width="6"/><rect x="380" y="740" width="1160" height="110" fill="#e8d2b0" stroke="${INK}" stroke-width="6"/>`) + t(960, 815, "COAT CHECK", 46, { w: 900 }), "start", "fade") +
    ["#6b7fa8", "#b5564c", "#5a8f6a", "#8e6bbf"].map((c, i) => A(g(520 + i * 290, 500, 0.9, coat(c)) + g(590 + i * 290, 470, 0.5, tag("#" + (25 + i))), "coat", "slide", { dir: "d", delay: i * 0.1 })).join("") };
S.S097 = { h: "The hanger tag doesn't have your name, but your ticket proves the coat is yours", chip: WHOSE,
  body: g(520, 600, 1.3, coat()) + A(g(700, 520, 1.1, tag("#27", { fill: YEL })), "tag", "pop") + A(t(520, 850, "hanger tag: a number, no name", 34, { w: 800, fill: GREY }), "name", "fade") +
    A(g(1380, 520, 1.3, ticket("#27", "your ticket", { color: YEL })) + g(1380, 740, 0.5, person({ shirt: BLUE, label: null })) + t(1500, 760, "You", 40, { w: 900, anchor: "start" }), "ticket", "pop") +
    A(W(`<path d="M 850 520 H 1130" stroke="${GREEN}" stroke-width="10" stroke-dasharray="20 14" stroke-linecap="round"/>`) + t(990, 490, "same number", 34, { w: 900, fill: DGREEN }), "proves", "wipe", { dir: "r", dur: 0.5 }) };
S.S098 = { h: "Your brokerage's records are that ticket", chip: WHOSE,
  body: A(g(1320, 570, 1.25, doc("YOUR BROKERAGE'S RECORDS", ["Owner of these shares:", "YOU"], { w: 600, size: 42, hl: 1 })), "records", "pop") + A(t(800, 590, "=", 120, { w: 900 }), "are", "pop") + A(g(480, 560, 1.1, ticket("#27", "your ticket", { color: YEL })), "ticket", "pop"),
  term: ["BENEFICIAL OWNER", "The real owner. You get the gains and the losses, even though another name is on the official record."] };
S.S099 = { h: "Promise two, done", chip: WHOSE, body: promises(2, [1, 2], [1, 2], null, "done") + A(card(960, 830, 1040, 96, t(0, 14, "The name on the record isn't yours, but the shares are.", 36, { w: 900 }), { fill: "#cfead7" }), "shares", "pop") };
S.S100 = { h: "The gains are yours, and so are the losses", chip: WHOSE,
  body: A(card(520, 560, 600, 420, arrow(0, 80, 0, -130, { color: GREEN, width: 26 }) + t(0, 170, "GAINS: yours", 50, { w: 900, fill: DGREEN }), { fill: "#e6f4ea" }), "gains", "pop") +
    A(card(1400, 560, 600, 420, arrow(0, -130, 0, 80, { color: RED, width: 26 }) + t(0, 170, "LOSSES: yours too", 50, { w: 900, fill: RED }), { fill: "#fbe9e6" }), "losses", "pop") };
S.S101 = { h: "Voting with a fractional share depends on your broker's rules", chip: WHOSE,
  body: A(g(620, 620, 1.5, ballotBox()), "voting", "pop") + A(g(1000, 440, 1.6, crumb()) + t(1000, 560, "?", 90, { w: 900, fill: GREY }), "fractional", "pop") + A(g(1420, 780, 0.9, tower("YOUR BROKER", { w: 280, h: 330 })) + t(1420, 380, "its rules decide", 38, { w: 900 }), "broker's", "pop"),
  term: ["SHAREHOLDER VOTE", "People who own shares can vote on some big company decisions."] };

// ---------- CHECKPOINT 2 ----------
S.S102 = { h: "Quick check: the whole route is on the map now", map: false,
  body: map(["done", "done", "done", "done", "done"], { at: 5, who: buck("happy"), y: 400 }) };
const steps3 = (items) => items.map(([icon, ls], i) => card(400 + i * 560, 560, 460, 420, g(0, -60, 1, icon) + t(0, 110, ls[0], 38, { w: 900, max: 420 }) + t(0, 158, ls[1], 38, { w: 900, max: 420 }))).join("") + arrow(650, 560, 710, 560, { width: 10 }) + arrow(1210, 560, 1270, 560, { width: 10 });
S.S103 = { h: "Your dollar became an order, took one possible route, and reached a seller", mapDone: 5, stop: 0,
  body: steps3([[g(0, 0, 0.6, doc("ORDER", ["Buy $1 of Apple"], { w: 380 })), ["Became", "an order"]], [g(-180, -70, 0.24, P.roadMap({ id: "m2", states: ["done", "done", "done", "done", "done"] })), ["Took one", "possible route"]], [g(0, 10, 0.6, L.teacher(null)), ["Reached", "a seller"]]]) };
S.S104 = { h: "It settled a business day later, with Cede & Co. on the record", mapDone: 5, stop: 0,
  body: g(560, 560, 1.3, calendar("TRADE DAY", "+1", { sub: "business day", color: GREEN, w: 300 })) + g(1340, 560, 1.3, doc("OFFICIAL RECORD", ["Registered name:", "CEDE & CO."], { w: 520, size: 40, hl: 1 })) };
S.S105 = { h: "The order: a fraction of a second. Settlement: a business day later.", mapDone: 5, stop: 0,
  body: card(520, 570, 640, 440, g(0, -50, 1, stopwatch()) + t(0, 110, "THE ORDER", 34, { w: 900, fill: GREY }) + t(0, 166, "a fraction of a second", 44, { w: 900 })) +
    card(1400, 570, 640, 440, g(0, -70, 0.85, calendar("TRADE DAY", "+1", { color: GREEN, w: 260 })) + t(0, 110, "SETTLEMENT", 34, { w: 900, fill: GREY }) + t(0, 166, "one business day later", 44, { w: 900 })) };
S.S106 = { h: "The part that matters most: how one dollar turns into more dollars", mapDone: 5, stop: 0, map: false,
  body: g(520, 580, 1.8, bill(170)) + arrow(760, 580, 1060, 580, { color: DGREEN, width: 14 }) + [0, 1, 2, 3].map((i) => g(1360 + i * 14, 640 - i * 44, 1.8, bill(170))).join("") + t(1680, 500, "?", 130, { w: 900, fill: DGREEN }) };

// ---------- HOW A SHARE MAKES MONEY ----------
const ways = (on) => [["1", ["Sell for more", "than you paid"], g(0, -40, 1, arrow(-90, 40, 90, -60, { color: GREEN, width: 18 }))], ["2", ["Dividends"], g(-40, -40, 1.3, coin()) + g(40, -20, 1.3, coin())]]
  .map(([n, ls, icon], i) => { const c = card(520 + i * 880, 560, 680, 460, t(0, -170, "WAY " + n, 40, { w: 900, fill: DGREEN }) + icon + ls.map((l, k) => t(0, 120 + k * 56 - (ls.length - 1) * 20, l, 48, { w: 900 })).join(""), { fill: on === i ? YEL : "#fff", sw: on === i ? 9 : 6 }); return on === null || on === i ? c : dim(c, 0.35); }).join("");
S.S107 = { h: "Two main ways to make money from owning a stock", body: ways(null) };
S.S108 = { h: "Way 1: sell for more than you paid", body: ways(0) };
S.S109 = { h: "A made-up example to show how that works", example: false, body: g(560, 330, 1.25, P.exampleCard({ title: "MAYA AND JORDAN", lines: ["Maya buys shares.", "Later, Jordan wants them.", ""] })) };
const maya = (x = 400) => g(x, 600, 1.2, person({ shirt: PURPLE, skin: 1, hair: "long", label: "Maya" }));
const jordan = (x = 1520) => g(x, 600, 1.2, person({ shirt: ORANGE, skin: 2, label: "Jordan" }));
const sum = (x, y, rows, total, tf = DGREEN, w = 640) => card(x, y, w, 120 + rows.length * 62 + 110, rows.map((r, i) => t(0, -((rows.length * 62 + 110) / 2) + 40 + i * 62, r, 44, { w: 800, max: w - 60 })).join("") + W(`<path d="M ${-w / 2 + 40} ${((rows.length * 62 + 110) / 2) - 96 - 14} H ${w / 2 - 40}" stroke="${INK}" stroke-width="5"/>`) + t(0, ((rows.length * 62 + 110) / 2) - 18, total, 66, { w: 900, fill: tf, max: w - 60 }));
const tenSlices = (x, y) => [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => g(x + (i % 5) * 62, y + Math.floor(i / 5) * 86, 0.45, slice())).join("");
S.S110 = { h: "Maya buys 10 shares at $200 each", body: maya() + tenSlices(620, 420) + sum(1300, 560, ["10 shares × $200"], "= $2,000") };
S.S111 = { h: "A year later, Jordan offers $250 a share for all ten",
  body: maya() + tenSlices(620, 420) + jordan() + card(1180, 500, 400, 240, t(0, -60, "1 YEAR LATER", 30, { w: 900, fill: GREY }) + t(0, 0, "10 × $250", 50, { w: 900 }) + t(0, 70, "= $2,500", 60, { w: 900, fill: DGREEN })) + arrow(1380, 700, 900, 700, { color: DGREEN, curve: -40, label: "offer", ldy: 70 }) };
S.S112 = { h: "Maya sells and makes $500",
  body: maya() + sum(1040, 520, ["Sold for   $2,500", "Paid         $2,000"], "+$500") + jordan() + t(1040, 780, "before taxes and any fees", 36, { w: 800, fill: GREY }) };
S.S113 = { h: "At $150 a share, Maya would have lost $500",
  body: maya() + sum(1040, 520, ["Sold for   $1,500", "Paid         $2,000"], "−$500", RED) + jordan() + t(1040, 780, "10 × $150 = $1,500", 36, { w: 800, fill: GREY }) };
const owners = (x, y) => [0, 1, 2].map((i) => g(x + i * 170, y, 0.7, person({ shirt: [BLUE, ORANGE, PURPLE][i], skin: i, hair: i === 1 ? "long" : "short" }))).join("");
S.S114 = { h: "Way 2: dividends. The company shares part of its profits with its owners.",
  body: g(480, 800, 1, tower("COMPANY", { w: 280, h: 360 })) + [0, 1, 2].map((i) => arrow(660, 520, 1150 + i * 170, 480, { color: DGREEN, curve: -60 - i * 20, width: 6 }) + g(900 + i * 110, 400 - i * 16, 1, coin(30))).join("") + owners(1180, 660) + t(1350, 810, "its owners (shareholders)", 36, { w: 900 }),
  term: ["DIVIDEND", "A payment a company makes to the people who own its shares, out of its profits."] };
S.S115 = { h: "Not every company pays dividends, and they can be cut",
  body: card(400, 560, 480, 420, g(0, 90, 0.5, tower("COMPANY A", { w: 260, h: 300 })) + g(-60, -150, 1, coin(30)) + g(10, -160, 1, coin(30)) + g(80, -150, 1, coin(30)) + t(0, 170, "pays dividends", 38, { w: 900, fill: DGREEN })) +
    card(960, 560, 480, 420, g(0, 90, 0.5, tower("COMPANY B", { w: 260, h: 300, sign: ORANGE })) + t(0, -130, "$0", 60, { w: 900, fill: GREY }) + t(0, 170, "pays none", 38, { w: 900, fill: GREY })) +
    card(1520, 560, 480, 420, g(0, 90, 0.5, tower("COMPANY C", { w: 260, h: 300, sign: PURPLE })) + g(-30, -150, 1, coin(30)) + dim(g(50, -150, 1, coin(30)), 0.3) + cross(50, -150, 30, 9) + t(0, 170, "cut its dividend", 38, { w: 900, fill: RED })) };
S.S116 = { body: g(860, 640, 1.6, hamlet("proud")) + [[760, 300], [860, 250], [960, 310]].map(([x, y]) => g(x, y, 1.1, coin())).join("") + bubble(1320, 380, "Rent for my savings!", { tail: "left" }) };
const board = (price, change, ex) => g(640, 400, 1, P.priceBoard({ price, change, example: false }));
S.S117 = { h: "The price you usually see is the last-traded price",
  body: g(260, 420, 1, P.priceBoard({ price: "$ ? ? ?", label: "APPLE · LAST TRADE" })) + arrow(1200, 570, 940, 570, { color: DGREEN }) + card(1500, 570, 560, 220, t(0, -30, "the last price", 46, { w: 900 }) + t(0, 36, "someone actually paid", 46, { w: 900 }), { fill: YEL }),
  term: ["LAST-TRADED PRICE", "The price of the most recent sale: what a buyer just paid a seller."] };
S.S118 = { h: "Say Apple's last trade was $350.00", body: g(640, 420, 1, P.priceBoard({ price: "$350.00" })) };
S.S119 = { h: "The cheapest seller wants $350.05, and a buyer pays it",
  body: g(200, 300, 0.8, P.priceBoard({ price: "$350.00" })) + g(1180, 680, 0.9, person({ shirt: ORANGE, skin: 2, label: "Cheapest seller" })) + g(1180, 400, 1.3, priceTag("$350.05", { w: 280, color: YEL })) +
    g(1640, 680, 0.9, person({ shirt: BLUE, label: "Buyer" })) + arrow(1540, 600, 1300, 600, { color: DGREEN, label: "pays it", ldy: -24 }) + stamp(1420, 480, "DEAL", { color: GREEN, rot: -8 }) };
S.S120 = { h: "The last-trade price now becomes $350.05", body: g(640, 420, 1, P.priceBoard({ price: "$350.05", change: "+$0.05" })) };
const jag = (n, seed, trend = 0.5) => { const pts = []; let v = 0.2, r = seed; const rnd = () => ((r = (r * 9301 + 49297) % 233280) / 233280); for (let i = 0; i <= n; i++) { pts.push([i / n, Math.max(0.05, Math.min(0.95, v))]); v += (rnd() - 0.5 + trend * 0.12) * 0.16; } return pts; };
S.S121 = { h: "Millions of small deals like that, every day, make a stock chart move",
  body: g(420, 820, 1, chart(jag(60, 11, 0.8), { w: 1080, h: 480, color: GREEN, sw: 7, xl: "time", yl: "price" })) + [0.2, 0.45, 0.7].map((x, i) => g(420 + x * 1080, 330 + i * 30, 0.8, stamp(0, 0, "DEAL", { color: GREEN, rot: -6 + i * 5, size: 30 }))).join("") };
S.S122 = { h: "Prices mostly move on what people expect a company to earn later",
  body: g(420, 640, 1, person({ shirt: BLUE, label: "Buyers" })) + g(640, 640, 1, person({ shirt: ORANGE, skin: 2, label: "Sellers" })) +
    W(`<path d="M 760 470 L 1040 400 L 1050 440 L 770 520 Z" fill="#cfd4da" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><circle cx="1066" cy="418" r="34" fill="${LBLUE}" stroke="${INK}" stroke-width="6"/>`) +
    card(1460, 520, 520, 380, t(0, -140, "LATER", 34, { w: 900, fill: GREY }) + g(-190, 130, 1, chart([[0, 0.2], [0.3, 0.35], [0.6, 0.55], [1, 0.9]], { w: 380, h: 200, color: GREEN })) + t(0, 172, "future profits?", 36, { w: 900 }), { fill: YEL }),
  term: ["EARNINGS", "A company's profit: the money left after it pays its costs."] };
S.S123 = { h: "Good news can lift a price in minutes, and bad news can sink it",
  body: g(480, 600, 1.4, newspaper("GOOD NEWS")) + arrow(760, 720, 760, 420, { color: GREEN, width: 22 }) + g(1280, 600, 1.4, newspaper("BAD NEWS", { good: false })) + arrow(1560, 420, 1560, 720, { color: RED, width: 22 }) };
S.S124 = { h: "A lesson Warren Buffett passed on from his teacher, Benjamin Graham",
  body: g(480, 600, 1.3, doc("1987 LETTER", ["To the shareholders of", "Berkshire Hathaway", "", "Warren Buffett"], { w: 500, size: 34 })) +
    g(1160, 620, 1, person({ shirt: "#3a4756", hair: "none", skin: 3, glasses: true, label: "Warren Buffett" })) + arrow(1500, 500, 1300, 500, { curve: 40, label: "taught him", ldy: -46 }) + g(1640, 620, 1, person({ shirt: "#6b5a4a", hair: "none", skin: 3, glasses: true, label: "Benjamin Graham" })) };
S.S125 = { h: "Short run: a voting machine. Long run: a weighing machine.",
  body: card(520, 570, 640, 460, t(0, -180, "IN THE SHORT RUN", 36, { w: 900, fill: GREY }) + g(0, 20, 1.1, ballotBox()) + t(0, 190, "a voting machine", 46, { w: 900 })) +
    card(1400, 570, 640, 460, t(0, -180, "IN THE LONG RUN", 36, { w: 900, fill: GREY }) + g(0, 10, 1, scaleIcon()) + t(0, 190, "a weighing machine", 46, { w: 900 }), { fill: YEL }) };
S.S126 = { h: "Day to day, prices follow moods. Over many years, they tend to follow profits.",
  body: card(520, 570, 640, 440, t(0, -170, "DAY TO DAY: MOODS", 36, { w: 900, fill: RED }) + g(-250, 150, 1, chart(jag(26, 5, 0), { w: 500, h: 240, color: RED, sw: 7 }))) +
    card(1400, 570, 640, 440, t(0, -170, "MANY YEARS: PROFITS", 36, { w: 900, fill: DGREEN }) + g(-250, 150, 1, chart([[0, 0.1], [0.2, 0.22], [0.35, 0.2], [0.5, 0.42], [0.65, 0.5], [0.8, 0.72], [1, 0.95]], { w: 500, h: 240, color: GREEN, sw: 9 })), { fill: "#e6f4ea" }) };

module.exports = { S, jag, steps3 };
