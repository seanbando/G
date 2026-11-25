// Renders the props sheet. Usage: node kit/props/render_props.js <out.png> [scale]
const { chromium } = require("playwright");
const { WOBBLE_FILTER, buck } = require("../characters/characters.js");
const P = require("./props.js");
(async () => {
  const out = process.argv[2] || "props-sheet.png";
  const scale = parseFloat(process.argv[3] || "1");
  const label = (x, y, t) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="800" font-size="30" fill="#1f2328">${t}</text>`;
  const body =
    `<g transform="translate(160 40) scale(0.8)">${P.roadMap({ states: ["done", "active"] })}</g>` +
    `<g transform="translate(500 120) scale(0.5)">${buck("cocky")}</g>` +
    label(960, 400, "ROAD MAP · stop 1 done, stop 2 active") +
    `<g transform="translate(250 690) scale(0.6)">${P.pizza({})}</g>` + label(250, 1000, "PIZZA") +
    `<g transform="translate(640 690) scale(0.6)">${P.pizza({ id: "p2", highlight: 0, bite: true })}</g>` + label(640, 1000, "SLICE + BITE") +
    `<g transform="translate(900 470) scale(0.72)">${P.exampleCard({ title: "EXAMPLE: A PIZZA SHOP", lines: ["Shop worth $100", "Cut into 100 slices", "1 slice = $1"] })}</g>` +
    label(1130, 760, "EXAMPLE CARD") +
    `<g transform="translate(1400 470) scale(0.72)">${P.priceBoard({ price: "$250.05", change: "+$0.05" })}</g>` +
    label(1630, 730, "PRICE BOARD") +
    `<g transform="translate(940 860)">${P.sourceTag({ text: "Source: Apple Investor Relations" })}</g>` +
    label(1180, 930, "SOURCE TAG (bottom-left on real-data shots)");
  const html = `<!doctype html><html><body style="margin:0;background:#f6f3ea">
  <svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
    <defs>${WOBBLE_FILTER}</defs><rect width="1920" height="1080" fill="#f6f3ea"/>${body}</svg></body></html>`;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale });
  await page.setContent(html);
  await page.screenshot({ path: out });
  await browser.close();
  console.log("wrote", out);
})();
