// Renders every still (one per script line) and contact sheets for review.
// Usage: node video/01-follow-one-dollar/stills/render.js [--only S001,S002] [--sheets-only]
// Output: stills/png/S001.png ... and stills/sheets/sheet-01.png ...
// Section chips, EXAMPLE badges and source tags come from the script itself, so they can't drift.
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { parseScript, buildSvg, fontCss, FIT, SCENES } = require("./compose.js");

const OUT = path.join(__dirname, "png"), SHEETS = path.join(__dirname, "sheets");

(async () => {
  const args = process.argv.slice(2);
  const only = args.includes("--only") ? new Set(args[args.indexOf("--only") + 1].split(",")) : null;
  const lines = parseScript();
  const missing = lines.filter((l) => !SCENES[l.id]).map((l) => l.id);
  if (missing.length) console.log("no scene yet for:", missing.join(", "));
  fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(SHEETS, { recursive: true });
  const css = fontCss();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  let problems = 0;
  if (!args.includes("--sheets-only")) {
    for (const line of lines) {
      if (!SCENES[line.id] || (only && !only.has(line.id))) continue;
      await page.setContent(`<!doctype html><html><head><style>${css}body{margin:0}</style></head><body>${buildSvg(line)}</body></html>`);
      await page.evaluate(() => document.fonts.ready);
      const bad = await page.evaluate(FIT);
      if (bad.length) { problems++; console.log(line.id, "text outside the safe area or overlapping:", bad.join(" | ")); }
      await page.screenshot({ path: path.join(OUT, line.id + ".png") });
    }
  }
  // contact sheets: 12 stills each, with the spoken line under every still
  const done = lines.filter((l) => fs.existsSync(path.join(OUT, l.id + ".png")));
  const per = 12;
  await page.setViewportSize({ width: 1920, height: 1310 });
  for (let i = 0, n = 1; i < done.length; i += per, n++) {
    const cells = done.slice(i, i + per).map((l) =>
      `<div class="c"><img src="data:image/png;base64,${fs.readFileSync(path.join(OUT, l.id + ".png")).toString("base64")}"><p><b>${l.id} · ${l.voice[0] + l.voice.slice(1).toLowerCase()}</b> ${l.text.replace(/</g, "&lt;")}</p></div>`).join("");
    await page.setContent(`<!doctype html><html><head><style>${css}body{margin:0;background:#2b2f36;font-family:Nunito,sans-serif}.g{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:14px}.c{background:#fff;border-radius:8px;overflow:hidden}img{width:100%;display:block}p{margin:0;padding:6px 10px 8px;font-size:14.5px;font-weight:700;line-height:1.25;height:54px;color:#1f2328}b{color:#23a05a;font-weight:900}</style></head><body><div class="g">${cells}</div></body></html>`);
    await page.evaluate(() => Promise.all([...document.images].map((im) => im.decode())));
    await page.screenshot({ path: path.join(SHEETS, `sheet-${String(n).padStart(2, "0")}.png`), fullPage: true });
  }
  await browser.close();
  console.log(`rendered ${done.length} of ${lines.length} stills; ${problems} with layout warnings`);
})();
