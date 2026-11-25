// Thumbnail options for "Follow $1", built from the same characters and props as the video.
// Usage: node video/01-follow-one-dollar/thumbnail/render.js   -> option-a.png, option-b.png, option-c.png (1280 x 720)
const path = require("path");
const { chromium } = require("playwright");
const L = require("../stills/lib.js");
const { fontCss } = require("../stills/compose.js");
const { g, W, buck, hamlet, phone, appScreen, tower, bank, pocket, appleIcon, bill, arrow, cross, INK, RED, GREEN, DGREEN, PAPER } = L;

// big thumbnail text: heavy, with a thick outline so it reads at phone size
const big = (x, y, str, size, { fill = "#fff", stroke = INK, sw = 0.16, anchor = "middle", rot = 0 } = {}) =>
  `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Nunito, sans-serif" font-weight="900" font-size="${size}" fill="${fill}" stroke="${stroke}" stroke-width="${size * sw}" stroke-linejoin="round" paint-order="stroke"${rot ? ` transform="rotate(${rot} ${x} ${y})"` : ""}>${str}</text>`;
const rays = (cx, cy, c1, c2) => Array.from({ length: 16 }, (_, i) => { const a = i / 16 * Math.PI * 2, b = (i + 0.5) / 16 * Math.PI * 2; return `<path d="M ${cx} ${cy} L ${cx + Math.cos(a) * 1600} ${cy + Math.sin(a) * 1600} L ${cx + Math.cos(b) * 1600} ${cy + Math.sin(b) * 1600} Z" fill="${c2}"/>`; }).join("");

const OPTIONS = {
  // A: the surprising fact, with Buck's shocked face
  a: `<rect width="1280" height="720" fill="#ffd84d"/>${rays(330, 420, "#ffd84d", "#ffc81f")}` +
    g(330, 430, 1.75, buck("shocked")) +
    big(900, 250, "APPLE", 150, { fill: "#fff" }) + big(900, 390, "GETS", 150, { fill: "#fff" }) + big(900, 640, "$0", 300, { fill: RED, stroke: "#fff", sw: 0.1 }),
  // B: the question and the journey, from your pocket to Wall Street
  b: `<rect width="1280" height="720" fill="${GREEN}"/>${rays(640, 800, GREEN, "#1f9150")}` +
    W(`<path d="M 210 560 C 380 430, 520 700, 700 580 S 880 470, 1000 600" fill="none" stroke="${INK}" stroke-width="34" stroke-linecap="round"/><path d="M 210 560 C 380 430, 520 700, 700 580 S 880 470, 1000 600" fill="none" stroke="#fff" stroke-width="8" stroke-dasharray="30 34" stroke-linecap="round"/>`) +
    g(150, 560, 0.85, pocket()) + g(1090, 700, 0.74, bank(" ", { w: 380 })) + `<text x="1090" y="517" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="900" font-size="46" fill="${INK}">WALL ST</text>` +
    g(590, 440, 1.05, buck("cocky")) +
    big(640, 120, "WHERE DOES", 112) + big(640, 240, "YOUR $1 GO?", 124, { fill: "#ffd84d" }),
  // C: the tap and the crossed-out arrow
  c: `<rect width="1280" height="720" fill="#2b6cb0"/>${rays(640, 360, "#2b6cb0", "#2a63a2")}` +
    big(310, 120, "YOU PAY $1", 82) + g(300, 440, 0.78, phone(appScreen())) + arrow(470, 470, 830, 470, { color: "#fff", width: 22 }) + cross(650, 470, 74, 30) +
    big(1000, 110, "APPLE GETS", 72) + big(1010, 290, "$0", 210, { fill: RED, stroke: "#fff", sw: 0.1 }) +
    g(1010, 690, 0.95, tower("APPLE", { fill: "#e6e9ee", sign: "#6b7280", w: 260, h: 300 })) + g(1010, 520, 0.6, appleIcon()),
};

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  for (const [k, body] of Object.entries(OPTIONS)) {
    await page.setContent(`<!doctype html><html><head><style>${fontCss()}body{margin:0}</style></head><body><svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><defs>${L.WOBBLE_FILTER}</defs>${body}</svg></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(__dirname, `option-${k}.png`) });
  }
  // a preview strip at the size YouTube shows on a phone, to check it still reads
  await page.setViewportSize({ width: 1020, height: 200 });
  const fs = require("fs");
  await page.setContent(`<body style="margin:0;background:#181818;display:flex;gap:15px;padding:10px">${Object.keys(OPTIONS).map((k) => `<img width="320" src="data:image/png;base64,${fs.readFileSync(path.join(__dirname, `option-${k}.png`)).toString("base64")}">`).join("")}</body>`);
  await page.evaluate(() => Promise.all([...document.images].map((i) => i.decode())));
  await page.screenshot({ path: path.join(__dirname, "preview-small.png") });
  await browser.close();
  console.log("wrote option-a/b/c.png and preview-small.png");
})();
