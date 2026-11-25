// Stills S040–S085: stop 2 (market maker), stop 3 (exchange), checkpoint 1, stop 4 (the seller).
const L = require("./lib.js");
const { map, promises } = require("./scenes-a.js");
const { A, t, lines, g, W, dim, bubble, arrow, cross, tick, stamp, card, bill, coin, slice, crumb, priceTag, person, teacher, phone, appleIcon, appScreen,
  tower, bank, booth, house, rack, signpost, calendar, clock, bell, ticket, doc, chart, buck, hamlet, P, INK, GREEN, DGREEN, RED, GREY, LGREY, BLUE, LBLUE, YEL, GOLD, PAPER, ORANGE, PURPLE } = L;

// dark two-row price board: what the booth buys at and sells at
function quoteBoard(buy, sell, { title = "APPLE SHARES", w = 620, onBuy = null, onSell = null } = {}) {
  const vb = t(w / 2 - 50, -14, buy, 52, { w: 900, fill: "#5fe08f", anchor: "end", max: w * 0.5 }), vs = t(w / 2 - 50, 100, sell, 52, { w: 900, fill: "#ffd27a", anchor: "end", max: w * 0.5 });
  return W(`<rect x="${-w / 2}" y="-160" width="${w}" height="320" rx="22" fill="#20252b" stroke="${INK}" stroke-width="8"/><rect x="${-w / 2 + 22}" y="-138" width="${w - 44}" height="276" rx="12" fill="#2c333b"/><path d="M ${-w / 2 + 40} 22 H ${w / 2 - 40}" stroke="#59636e" stroke-width="4"/>`) +
    t(0, -92, title, 30, { w: 800, fill: "#aab3bd" }) +
    t(-w / 2 + 50, -18, "WE BUY AT", 34, { w: 900, fill: "#fff", anchor: "start" }) + (onBuy ? A(vb, onBuy, "pop") : vb) +
    t(-w / 2 + 50, 96, "WE SELL AT", 34, { w: 900, fill: "#fff", anchor: "start" }) + (onSell ? A(vs, onSell, "pop") : vs);
}
const mm = (x, y, s = 1, o = {}) => g(x, y, s, booth("MARKET MAKER", { awning: GREEN, ...o }));
const shelf = (n) => W(`<rect x="-230" y="-30" width="460" height="22" fill="#c89b62" stroke="${INK}" stroke-width="5"/><path d="M -210 -8 v 60 M 210 -8 v 60" stroke="${INK}" stroke-width="8"/>`) + Array.from({ length: n }, (_, i) => g(-170 + i * 85, -110, 0.8, slice())).join("");

const S = {};

// ---------- STOP 2: THE MARKET MAKER ----------
S.S040 = { h: "Stop 2: a company most people have never heard of", map: false, anims: [{ sel: "#map-stop2", on: "stop>", fx: "pop" }],
  body: map(["done", "active"], { at: 2, who: buck("neutral"), y: 380, whoOn: "stop" }) };
S.S041 = { h: "Many everyday orders don't go straight to an exchange",
  body: A(g(360, 590, 0.62, phone(appScreen())), "start", "slide", { dir: "u" }) + A(g(1420, 560, 0.72, bank("STOCK EXCHANGE", { w: 400 })), "stock", "pop") +
    A(arrow(520, 520, 1180, 400, { dash: "18 16", color: GREY, curve: -30 }), "orders", "wipe", { dir: "r", dur: 0.6 }) + A(cross(860, 420, 42, 14), "don't", "stamp") +
    A(arrow(520, 660, 1120, 800, { color: DGREEN, curve: 40 }) + t(1240, 830, "?", 130, { w: 900, fill: DGREEN }), "exchange", "wipe", { dir: "r", dur: 0.6 }),
  term: ["RETAIL ORDER", "An order from an everyday investor like you, not from a big firm."] };
S.S042 = { h: "Brokers often send them to a market maker",
  body: g(300, 590, 0.55, phone(appScreen())) + A(arrow(430, 560, 600, 560, { color: GREY }), "start", "wipe", { dir: "r", dur: 0.3 }) + A(g(780, 760, 0.8, tower("YOUR BROKER", { w: 280, h: 330 })), "brokers", "pop") +
    A(arrow(950, 560, 1150, 560, { color: DGREEN }), "send", "wipe", { dir: "r", dur: 0.4 }) + A(mm(1420, 780, 1), "trading", "pop"),
  term: ["MARKET MAKER", "A trading firm that is always ready to buy shares from you or sell shares to you."] };
S.S043 = { h: "Picture a currency booth at the airport",
  body: A(g(640, 800, 1.15, booth("CURRENCY EXCHANGE", { awning: BLUE })) + g(640, 628, 0.5, person({ shirt: BLUE })), "currency", "pop") +
    A(W(`<path d="M 1150 330 l 230 -60 l 40 20 l -150 70 l 80 70 l -30 14 l -110 -50 l -70 30 l -20 -16 l 50 -44 Z" fill="#fff" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`), "airport", "slide", { dir: "l" }) +
    A(card(1380, 620, 600, 250, t(0, -44, "One price to BUY from you", 38, { w: 900 }) + W(`<path d="M -250 0 H 250" stroke="${LGREY}" stroke-width="4"/>`)), "price", "pop") + A(g(1380, 620, 1, t(0, 66, "A higher price to SELL to you", 38, { w: 900 })), "sell", "fade") };
S.S044 = { h: "A market maker works the same way",
  body: g(380, 800, 0.72, booth("CURRENCY EXCHANGE", { awning: BLUE })) + A(t(700, 600, "=", 130, { w: 900 }), "same", "pop") + A(mm(1020, 800, 0.72), "market", "pop") +
    A(g(1500, 560, 0.72, quoteBoard("buy price", "sell price", { onBuy: "buy", onSell: "sell" })) + t(1500, 760, "posted regularly", 36, { fill: GREY }), "posting", "pop") };
S.S045 = { h: "Say it buys at one price and sells at another",
  body: mm(480, 820, 1) + A(g(1240, 560, 1.1, quoteBoard("$350.00", "$350.02", { onBuy: "at>", onSell: "at:2>" })), "start", "slide", { dir: "r" }) };
S.S046 = { h: "That 2¢ gap is called the spread", example: true,
  body: card(520, 440, 560, 170, t(0, -18, "MARKET MAKER BUYS AT", 30, { w: 900, fill: GREY }) + t(0, 48, "$350.00", 70, { w: 900, fill: DGREEN })) +
    card(520, 700, 560, 170, t(0, -18, "MARKET MAKER SELLS AT", 30, { w: 900, fill: GREY }) + t(0, 48, "$350.02", 70, { w: 900, fill: ORANGE })) +
    A(W(`<path d="M 840 440 h 70 v 260 h -70" fill="none" stroke="${INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`) + arrow(915, 570, 1060, 570, {}), "gap", "wipe", { dir: "r", dur: 0.4 }) +
    A(card(1380, 570, 560, 230, t(0, -24, "THE SPREAD", 40, { w: 900, fill: GREY }) + t(0, 62, "2¢", 110, { w: 900, fill: RED }), { fill: YEL, sw: 9 }), "spread", "pop"),
  term: ["SPREAD", "The small gap between the buy price and the sell price. The market maker tries to earn it."] };
S.S047 = { h: "It can lose money too",
  body: mm(480, 820, 0.95) + g(780, 560, 0.9, slice()) + A(g(1000, 760, 1, chart([[0, 0.8], [0.25, 0.74], [0.4, 0.82], [0.6, 0.5], [0.8, 0.36], [1, 0.14]], { w: 640, h: 380, color: RED, xl: "a minute later" })), "price", "wipe", { dir: "r", dur: 1.4 }) +
    A(t(1320, 330, "the price moves against it", 40, { w: 900, fill: RED }), "against", "fade") };
S.S048 = { h: "One market maker handles about a third of everyday trading",
  body: A(g(640, 580, 1, W(`<circle r="250" fill="#fff" stroke="${INK}" stroke-width="8"/>`)), "start", "pop") +
    A(g(640, 580, 1, W(`<path d="M 0 0 L 0 -250 A 250 250 0 0 1 216.5 125 Z" fill="${GREEN}" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/>`) + t(96, -60, "about", 34, { w: 900, fill: "#fff" }) + t(100, 0, "1/3", 64, { w: 900, fill: "#fff" })), "third", "pop") +
    A(card(1340, 480, 680, 230, t(0, -44, "Citadel Securities says it executes", 36, { w: 800 }) + t(0, 28, "about a third", 60, { w: 900, fill: DGREEN }) + t(0, 86, "of all U.S. retail stock trading", 36, { w: 800 })), "citadel", "pop") +
    A(card(1340, 740, 680, 130, t(0, -14, "Citadel Securities = a big market maker", 32, { w: 800 }) + t(0, 36, "executes = carries out the trade", 30, { fill: GREY }), { fill: YEL }), "executes", "pop") };
S.S049 = { h: "Market makers often pay brokers for sending them orders",
  body: g(480, 800, 0.9, tower("YOUR BROKER", { w: 280, h: 330 })) + mm(1440, 820, 0.95) +
    A(arrow(660, 480, 1220, 480, { color: GREY, curve: -50, label: "your orders", ldy: -84, lsize: 36 }) + g(940, 470, 0.6, doc("ORDER", ["Buy $1"], { w: 260 })), "sending", "wipe", { dir: "r", dur: 0.6 }) +
    A(arrow(1220, 680, 660, 680, { color: DGREEN, curve: -50, label: "a small payment", ldy: 86, lsize: 36 }) + g(940, 720, 1, coin(30)) + g(1000, 730, 1, coin(30)), "pay", "wipe", { dir: "l", dur: 0.6 }),
  term: ["PAYMENT FOR ORDER FLOW", "Market makers paying your broker to send your orders to them."] };
S.S050 = { h: "That's one reason many apps charge no commission",
  body: A(g(620, 590, 0.82, phone(g(0, -150, 0.9, appleIcon()) + t(0, -46, "Apple", 46, { w: 900 }) + `<rect x="-130" y="30" width="260" height="110" rx="14" fill="${YEL}" stroke="${INK}" stroke-width="4"/>` + t(0, 70, "COMMISSION", 26, { w: 900, fill: GREY }) + t(0, 122, "$0", 50, { w: 900, fill: DGREEN }))), "apps", "slide", { dir: "u" }) +
    A(card(1300, 560, 560, 200, t(0, -20, "No fee per trade", 46, { w: 900 }) + t(0, 40, "on stock trades, at many apps", 32, { fill: GREY })), "no", "pop"),
  term: ["COMMISSION", "A fee a broker charges you each time you trade."] };
S.S051 = { h: "Your broker still has to try to get you the best available deal",
  body: A(g(440, 800, 0.9, tower("YOUR BROKER", { w: 280, h: 330 })), "broker", "pop") +
    A(g(1240, 560, 1, L.checklist(["The price", "How reliably the order gets filled"], ["done", "done"], { w: 820, title: "BEST AVAILABLE DEAL, CONSIDERING:" })), "considering", "pop"),
  term: ["BEST EXECUTION", "Your broker's duty to try to get you the best deal that is reasonably available."] };
S.S052 = { body: A(g(900, 620, 1.6, hamlet("sideeye")), "start", "fade", { idle: "talk" }) + [[420, 380], [520, 700], [1380, 720], [1480, 480]].map(([x, y], i) => A(g(x, y, 1.2, coin()), "paid", "pop", { delay: i * 0.1 })).join("") + A(bubble(1300, 330, "And the pig?", { tail: "left" }), "except", "pop") };
S.S053 = { h: "If it has the shares, it sells them from its own shelf",
  body: mm(480, 820, 0.95) + A(g(1220, 640, 1.1, shelf(5)) + t(1220, 770, "the market maker's own shares", 36, { w: 800 }), "shares", "pop") +
    A(arrow(1000, 420, 760, 420, { color: DGREEN, curve: 60 }) + g(880, 330, 0.7, slice()), "sell", "wipe", { dir: "l", dur: 0.5 }),
  term: ["INVENTORY", "Shares the market maker already owns and keeps ready to sell."] };
S.S054 = { h: "If it doesn't, your order can head to stop 3",
  body: g(520, 640, 1.1, shelf(0)) + A(t(520, 770, "shelf is empty", 36, { w: 800, fill: RED }), "doesn't", "fade") + A(arrow(860, 560, 1160, 560, { color: DGREEN, width: 12 }), "head", "wipe", { dir: "r", dur: 0.5 }) + A(g(1440, 760, 0.8, bank("STOP 3", { w: 380 })), "stop", "pop") };

// ---------- STOP 3: THE EXCHANGE ----------
S.S055 = { h: "Stop 3: the stock exchange", map: false,
  body: map(["done", "done", "active"], { at: 3, who: buck("happy"), y: 400, s: 0.9, x: 240 }),
  term: ["STOCK EXCHANGE", "An organized marketplace where buyers and sellers of shares are matched. Most people picture it when they hear \"Wall Street\"."] };
S.S056 = { h: "The opening bell rings at 9:30 a.m. Eastern time",
  body: g(620, 830, 1.1, bank("NEW YORK STOCK EXCHANGE", { w: 520 })) + g(1240, 480, 1.3, bell()) + g(1560, 500, 1.1, clock(9, 30)) + t(1560, 660, "9:30 a.m.", 48, { w: 900 }) + t(1560, 710, "Eastern time", 32, { fill: GREY }),
  term: ["NYSE", "One of the biggest U.S. stock exchanges. Its building is on Wall Street in New York City.", "New York Stock Exchange"] };
S.S057 = { h: "The computers that match its trades are in New Jersey",
  body: g(700, 800, 1.3, rack({ n: 4 })) + g(1400, 690, 1.2, signpost("Mahwah,", "New Jersey")) + t(700, 860, "NYSE data center", 38, { w: 900 }),
  term: ["DATA CENTER", "A building full of computers. This is where the trades are really matched."] };
S.S058 = { h: "Nasdaq's main computers are in New Jersey too",
  body: g(480, 760, 0.9, rack({ n: 3 })) + t(480, 820, "NYSE computers", 36, { w: 900 }) + g(480, 400, 0.8, signpost("Mahwah, NJ", null, { w: 320 })) +
    g(1440, 760, 0.9, rack({ n: 3 })) + t(1440, 820, "Nasdaq computers", 36, { w: 900 }) + g(1440, 400, 0.8, signpost("Carteret, NJ", null, { w: 320, fill: BLUE })),
  term: ["NASDAQ", "The other big U.S. stock exchange. Many tech companies, including Apple, are listed on it."] };
S.S059 = { body: g(760, 640, 1.6, buck("annoyed")) + g(1340, 700, 1.3, signpost("WELCOME TO", "NEW JERSEY", { fill: BLUE })) + bubble(1120, 320, "New Jersey?!", { tail: "left" }) };
const lists = (buy, sell, match = false) =>
  g(960, 440, 0.5, bank("STOCK EXCHANGE", { w: 1500 })) +
  g(600, 690, 1, doc("BUYERS", buy, { w: 480, size: 36, hl: match ? 0 : -1 })) + g(1320, 690, 1, doc("SELLERS", sell, { w: 480, size: 36, hl: match ? 0 : -1 }));
S.S060 = { h: "An exchange is a matchmaker that keeps two lists", body: lists(["", "", ""], ["", "", ""]) };
S.S061 = { h: "One list holds buyers, the other holds sellers",
  body: lists(["Buyer: will pay this much", "Buyer: will pay a bit less", "Buyer: will pay less still"], ["Seller: wants this much", "Seller: wants a bit more", "Seller: wants more still"]) };
S.S062 = { h: "When a buyer and a seller agree on a price, it's a match",
  body: lists(["Buyer: will pay this much", "Buyer: will pay a bit less", "Buyer: will pay less still"], ["Seller: wants this much", "Seller: wants a bit more", "Seller: wants more still"], true) +
    W(`<path d="M 846 668 H 1074" stroke="${GREEN}" stroke-width="12" stroke-linecap="round"/>`) + stamp(960, 600, "MATCH", { color: GREEN, rot: -6, size: 44 }) };
const dayBar = (ext = false) => {
  const x0 = 260, w = 1400, seg = (a, b, fill, label, sub) => W(`<rect x="${x0 + a * w}" y="430" width="${(b - a) * w}" height="120" fill="${fill}" stroke="${INK}" stroke-width="6"/>`) + t(x0 + (a + b) / 2 * w, 484, label, 36, { w: 900, max: (b - a) * w - 20 }) + (sub ? t(x0 + (a + b) / 2 * w, 526, sub, 26, { w: 800, fill: GREY, max: (b - a) * w - 20 }) : "");
  return (ext ? seg(0, 0.25, "#e6e2d6", "EARLY", "fewer traders") + seg(0.75, 1, "#e6e2d6", "LATE", "fewer traders") : "") + seg(0.25, 0.75, "#cfead7", "REGULAR TRADING", null) +
    t(x0 + 0.25 * w, 610, "9:30 a.m.", 44, { w: 900 }) + t(x0 + 0.75 * w, 610, "4:00 p.m.", 44, { w: 900 }) + t(960, 660, "Eastern time", 32, { fill: GREY });
};
const week = (y) => ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"].map((d, i) => W(`<rect x="${470 + i * 144}" y="${y}" width="120" height="96" rx="14" fill="${i < 5 ? "#cfead7" : "#e6e2d6"}" stroke="${INK}" stroke-width="5"/>`) + t(530 + i * 144, y + 60, d, 34, { w: 900, fill: i < 5 ? INK : GREY })).join("");
S.S063 = { h: "Regular trading: 9:30 to 4, Monday through Friday", hOpts: { max: 60 }, body: dayBar() + week(730) };
S.S064 = { h: "The exceptions: market holidays and a few early-close days",
  body: g(600, 560, 1.35, calendar("HOLIDAY", "CLOSED", { color: RED, w: 300 })) + g(1300, 560, 1.35, calendar("SOME DAYS", "EARLY", { sub: "closes early", color: ORANGE, w: 300 })) };
S.S065 = { h: "Some apps let you trade earlier or later",
  body: dayBar(true) + [0, 1].map((i) => g(400 + i * 60, 780, 0.34, person({ shirt: GREY }))).join("") + [0, 1, 2, 3, 4, 5, 6, 7].map((i) => g(730 + i * 66, 780, 0.34, person({ shirt: [BLUE, ORANGE, PURPLE, GREEN][i % 4], skin: i % 4 }))).join("") + [0, 1].map((i) => g(1460 + i * 60, 780, 0.34, person({ shirt: GREY }))).join(""),
  term: ["EXTENDED HOURS", "Trading before 9:30 a.m. or after 4 p.m., when far fewer people are trading."] };
S.S066 = { h: "Fewer traders can mean bigger jumps and a wider gap",
  body: card(520, 560, 680, 480, t(0, -190, "BIGGER PRICE JUMPS", 36, { w: 900, fill: RED }) + g(-270, 190, 1, chart([[0, 0.4], [0.12, 0.42], [0.2, 0.8], [0.32, 0.72], [0.45, 0.25], [0.6, 0.3], [0.72, 0.7], [0.86, 0.2], [1, 0.55]], { w: 540, h: 300, color: RED }))) +
    card(1400, 560, 680, 480, t(0, -190, "WIDER GAP (SPREAD)", 36, { w: 900, fill: RED }) + t(-150, -70, "buy price", 34, { fill: GREY }) + W(`<path d="M -260 -40 H -40" stroke="${DGREEN}" stroke-width="12" stroke-linecap="round"/><path d="M -260 150 H -40" stroke="${ORANGE}" stroke-width="12" stroke-linecap="round"/><path d="M 0 -40 h 50 v 190 h -50" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`) + t(-150, 200, "sell price", 34, { fill: GREY }) + t(170, 70, "wider", 44, { w: 900, fill: RED })) };

// ---------- CHECKPOINT 1 ----------
S.S067 = { h: "Quick check: look how far your dollar has come", mapDone: 3, stop: 0, map: false,
  body: map(["done", "done", "done"], { at: 3, who: buck("happy"), y: 400 }) };
const recap = (on) => [
  [g(0, -60, 0.28, phone(appScreen())), "STOP 1 · YOUR APP", ["Your dollar became", "an order"]],
  [g(0, 50, 0.42, booth("MARKET MAKER", { awning: GREEN })), "STOP 2 · MARKET MAKER", ["May sell to you from", "its own shelf"]],
  [g(0, 50, 0.38, bank("EXCHANGE", { w: 380 })), "STOP 3 · EXCHANGE", ["Matches buyers", "with sellers"]],
].map(([icon, title, ls], i) => { const c = card(400 + i * 560, 540, 500, 480, t(0, -190, title, 30, { w: 900, fill: DGREEN, max: 440 }) + g(0, -40, 1, icon) + t(0, 150, ls[0], 38, { w: 900 }) + t(0, 198, ls[1], 38, { w: 900 }), { fill: i === on ? YEL : "#fff", sw: i === on ? 9 : 6 }); return i === on ? c : dim(c, i < on ? 0.7 : 0.3); }).join("");
S.S068 = { h: "Quick check", mapDone: 3, stop: 0, body: recap(0) };
S.S069 = { h: "Quick check", mapDone: 3, stop: 0, body: recap(1) };
S.S070 = { h: "Quick check", mapDone: 3, stop: 0, body: recap(2) };
S.S071 = { h: "Next stop: where your dollar actually changes hands", map: false,
  body: map(["done", "done", "done", "active"], { y: 400, extra: `<circle cx="1157" cy="262" r="66" fill="none" stroke="${GREEN}" stroke-width="7" stroke-dasharray="14 12"/>` }) };

// ---------- STOP 4: THE SELLER ----------
const quiz = (answer) => [["A", "All of it", 1], ["B", "Half", 0.5], ["C", "None", 0]].map(([k, label, amt], i) => {
  const right = answer && k === "C";
  const inner = t(0, -150, k, 60, { w: 900, fill: GREY }) + (amt ? `<g><clipPath id="q${i}"><rect x="-140" y="-70" width="${280 * amt}" height="140"/></clipPath><g clip-path="url(#q${i})">${g(0, -30, 1.5, bill(170))}</g></g>` : W(`<rect x="-128" y="-96" width="256" height="132" rx="16" fill="none" stroke="${GREY}" stroke-width="6" stroke-dasharray="16 12"/>`) + t(0, -10, "$0", 60, { w: 900, fill: GREY })) + t(0, 150, label, 50, { w: 900 });
  const c = card(400 + i * 560, 560, 480, 460, inner + (right ? g(170, -170, 1, W(`<circle r="44" fill="${GREEN}" stroke="${INK}" stroke-width="6"/>`) + tick(0, 2, 20, 9, "#fff")) : ""), { fill: right ? "#cfead7" : "#fff", sw: right ? 10 : 6 });
  return answer && !right ? dim(c, 0.35) : c;
}).join("");
S.S072 = { h: "Pick: how much of your dollar does Apple get?", body: quiz(false) };
S.S073 = { h: "Usually none: Apple isn't the one selling you the share", body: quiz(true) };
const fan = (x, y, i, label) => g(x, y, 1, person({ shirt: [ORANGE, BLUE][i], skin: i + 1, hair: i ? "short" : "long", label }));
S.S074 = { h: "Think of a concert ticket that gets resold between fans",
  body: fan(520, 620, 0, "Fan 1") + fan(1400, 620, 1, "Fan 2") + g(960, 520, 1.3, ticket("CONCERT", "admit one")) + arrow(700, 400, 1220, 400, { curve: -60 }) };
const band = (x, y, s = 1) => g(x, y, s, W(`<rect x="-200" y="20" width="400" height="40" rx="8" fill="#8a5a2b" stroke="${INK}" stroke-width="6"/>`) + g(-90, -60, 0.5, person({ shirt: RED, skin: 2 })) + g(90, -60, 0.5, person({ shirt: PURPLE, skin: 0, hair: "long" })) + W(`<path d="M -20 -70 l 44 -70 l 16 10 l -44 70 Z" fill="${GOLD}" stroke="${INK}" stroke-width="5"/><circle cx="-10" cy="-50" r="26" fill="${GOLD}" stroke="${INK}" stroke-width="5"/>`) + t(0, 110, "The band", 40, { w: 900 }));
S.S075 = { h: "The band gets paid when the box office sells the ticket first",
  body: fan(340, 640, 0, "Fan 1") + g(920, 820, 0.95, booth("BOX OFFICE", { awning: PURPLE })) + band(1520, 640) +
    arrow(480, 560, 700, 560, { color: DGREEN, label: "money", ldy: -24 }) + arrow(1130, 560, 1300, 560, { color: DGREEN, label: "money", ldy: -24 }) + stamp(920, 300, "FIRST SALE", { color: GREEN, rot: -4, size: 40 }) };
S.S076 = { h: "Buy it later from another fan, and your money goes to the fan",
  body: fan(440, 640, 0, "Fan 1 (seller)") + fan(1080, 640, 1, "Fan 2 (you)") + g(760, 430, 0.8, ticket("CONCERT", "admit one")) + arrow(900, 600, 620, 600, { color: DGREEN, curve: -40, label: "money", ldy: 70 }) + g(760, 540, 1, bill(120)) +
    dim(band(1560, 640, 0.8), 0.4) + t(1560, 400, "gets nothing this time", 34, { w: 900, fill: RED, max: 380 }) };
S.S077 = { h: "Apple's box-office moment: when it first sold shares to the public",
  body: g(520, 800, 1.1, tower("APPLE", { fill: "#e6e9ee", sign: "#6b7280", w: 260, h: 360 })) + g(520, 560, 0.6, appleIcon()) +
    arrow(700, 500, 1100, 500, { color: DGREEN, curve: -40, label: "new shares", ldy: -40 }) + arrow(1100, 660, 700, 660, { color: GREY, curve: -40, label: "money to Apple", ldy: 80 }) +
    [0, 1, 2].map((i) => g(1280 + i * 150, 620, 0.6, person({ shirt: [BLUE, ORANGE, PURPLE][i], skin: i, hair: i === 1 ? "long" : "short" }))).join("") + t(1430, 760, "the public", 38, { w: 900 }),
  term: ["IPO", "The first time a company sells its shares to the public.", "Initial Public Offering"] };
S.S078 = { h: "December 12, 1980, at $22 a share",
  body: g(620, 560, 1.5, calendar("DECEMBER 1980", "12", { w: 300 })) + g(1300, 520, 1.9, priceTag("$22")) + t(1320, 680, "a share", 44, { w: 900 }) };
S.S079 = { h: "Today, your dollar goes to whoever sold you the share",
  body: g(480, 560, 1.6, bill(170)) + arrow(680, 560, 1100, 560, { color: DGREEN, width: 12 }) + g(1360, 600, 1.3, person({ shirt: GREY, hair: "none", skin: 3, mouth: "flat" })) + t(1360, 500, "?", 80, { w: 900, fill: "#fff" }) + t(1360, 830, "the seller", 44, { w: 900 }) };
S.S080 = { h: "The seller could be…",
  body: [[g(0, 90, 0.5, tower("BROKER", { w: 240, h: 300 })), "your own broker"], [g(0, 90, 0.44, booth("MARKET MAKER", { awning: GREEN })), "a market maker"], [g(0, 90, 0.5, tower("BIG FUND", { w: 300, h: 340, sign: PURPLE })), "a big fund"], [g(0, 20, 0.7, teacher(null)), "a retired teacher"]]
    .map(([icon, label], i) => card(300 + i * 440, 540, 400, 440, g(0, -30, 1, icon) + t(0, 180, label, 36, { w: 900, max: 360 }))).join(""),
  term: ["FUND", "A big pool of many people's money, invested together by a manager."] };
S.S081 = { h: "Say a retired teacher sells a little stock to help pay for a new roof",
  body: g(560, 620, 1.2, teacher()) + g(760, 520, 0.8, slice()) + g(1340, 800, 1.3, house({ roof: "old" })) + t(1340, 860, "needs a new roof", 36, { w: 800, fill: GREY }) };
S.S082 = { body: g(700, 640, 1.5, buck("cocky")) + g(1420, 820, 1.1, house({ roof: "old" })) + bubble(1080, 300, "I'll pay for it!", { tail: "left" }) };
S.S083 = { h: "Your dollar ends up helping pay for that roof",
  body: g(300, 600, 0.5, phone(appScreen())) + t(300, 830, "You", 40, { w: 900 }) + g(960, 620, 1, teacher()) + g(1600, 780, 0.9, house({ roof: "old" })) +
    arrow(440, 520, 800, 520, { color: DGREEN, curve: -50, label: "your $1", ldy: -44 }) + g(620, 430, 0.8, bill(130)) +
    arrow(800, 720, 440, 720, { color: GREY, curve: -50, label: "a crumb of her stock", ldy: 84 }) + g(620, 730, 1.2, crumb()) +
    arrow(1100, 560, 1400, 560, { color: DGREEN, label: "toward the roof", ldy: -24 }) };
S.S084 = { h: "Promise one, done", body: promises(1, [1], [1]) + card(960, 830, 900, 96, t(0, 14, "Your dollar went to the SELLER, not to Apple.", 36, { w: 900 }), { fill: "#cfead7" }) };
S.S085 = { h: "Apple still cares about its share price",
  body: g(480, 800, 1.1, tower("APPLE", { fill: "#e6e9ee", sign: "#6b7280", w: 260, h: 360 })) + g(480, 560, 0.6, appleIcon()) +
    g(1080, 620, 1.1, person({ shirt: "#3a4756", skin: 3, label: "Executive" })) + g(1260, 540, 0.9, slice()) + card(1500, 720, 400, 110, t(0, 14, "often paid in stock", 34, { w: 900 }), { fill: YEL }),
  term: ["EXECUTIVES", "The top bosses who run a company."] };

module.exports = { S, quoteBoard, mm };
