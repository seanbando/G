// Renders the character sheet to PNG with the pre-installed Playwright Chromium.
// Usage: node kit/characters/render_sheet.js <out.png> [scale]
const { chromium } = require("playwright");
const { buck, hamlet, WOBBLE_FILTER } = require("./characters.js");
(async () => {
  const out = process.argv[2] || "sheet.png";
  const scale = parseFloat(process.argv[3] || "1");
  const buckPoses = [["neutral", "Neutral"], ["cocky", "Cocky"], ["shocked", "Shocked"], ["annoyed", "Annoyed"], ["happy", "Happy"], ["neutral", "Clipboard", { arms: "clipboard" }]];
  const hamPoses = [["grumpy", "Grumpy"], ["sideeye", "Side-eye"], ["shocked", "Shocked"], ["proud", "Proud (rare)"], ["hugging", "Hugging his coin"]];
  const cell = (svg, label, x, y) =>
    `<g transform="translate(${x} ${y})">${svg}</g><text x="${x}" y="${y + 175}" text-anchor="middle" font-family="Nunito, sans-serif" font-weight="800" font-size="30" fill="#1f2328">${label}</text>`;
  let body = "";
  buckPoses.forEach(([e, l, o], i) => (body += cell(`<g transform="scale(0.85)">${buck(e, o)}</g>`, l, 175 + i * 300, 300)));
  hamPoses.forEach(([e, l], i) => (body += cell(hamlet(e), l, 220 + i * 370, 770)));
  const html = `<!doctype html><html><head><style>body{margin:0;background:#f6f3ea}</style></head><body>
  <svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
    <defs>${WOBBLE_FILTER}</defs>
    <rect width="1920" height="1080" fill="#f6f3ea"/>
    <text x="60" y="90" font-family="Nunito, sans-serif" font-weight="900" font-size="54" fill="#1f2328">BUCK <tspan font-weight="700" font-size="34" fill="#1f7a45">the cocky dollar bill · voice: Larry</tspan></text>
    <text x="60" y="560" font-family="Nunito, sans-serif" font-weight="900" font-size="54" fill="#1f2328">HAMLET <tspan font-weight="700" font-size="34" fill="#c9677f">the grumpy piggy bank · voice: Grampa Werthers</tspan></text>
    ${body}
  </svg></body></html>`;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale });
  await page.setContent(html);
  await page.screenshot({ path: out });
  await browser.close();
  console.log("wrote", out);
})();
