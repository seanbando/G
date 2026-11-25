const { chromium } = require("playwright");
const { WOBBLE_FILTER } = require("../characters/characters.js");
const P = require("./props.js");
const lab = (x, y, t) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="800" font-size="28" fill="#1f2328">${t}</text>`;
(async () => {
  const body =
    `<g transform="translate(270 330) scale(0.62)">${P.pizza({ id: "a", slices: 100, example: true, label: "Shop worth $100" })}</g>` + lab(270, 610, "S017: 100 slices, $1 each") +
    `<g transform="translate(740 330) scale(0.62)">${P.pizza({ id: "b", slices: 3, example: true, label: "Company A" })}</g>` + lab(740, 610, "S025: 3 slices × $500 = $1,500") +
    `<g transform="translate(1210 330) scale(0.62)">${P.pizza({ id: "c", slices: 8, highlight: 0, label: "Apple", note: "not to scale: about 15 billion shares" })}</g>` + lab(1210, 640, "S033: slice = 1 share") +
    `<g transform="translate(1440 140) scale(0.65)">${P.priceBoard({ price: "$250.05", change: "+$0.05", example: true })}</g>` + lab(1650, 360, "S118–S120 board");
  const html = `<!doctype html><html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="720"><defs>${WOBBLE_FILTER}</defs><rect width="1920" height="720" fill="#f6f3ea"/>${body}</svg></body></html>`;
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 720 } });
  await pg.setContent(html); await pg.screenshot({ path: process.argv[2] }); await b.close();
})();
