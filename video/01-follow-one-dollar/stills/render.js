// Renders every still (one per script line) and contact sheets for review.
// Usage: node video/01-follow-one-dollar/stills/render.js [--only S001,S002] [--sheets-only]
// Output: stills/png/S001.png ... and stills/sheets/sheet-01.png ...
// Section chips, EXAMPLE badges and source tags come from the script itself, so they can't drift.
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const L = require("./lib.js");
const SCENES = require("./scenes.js");

const ROOT = path.join(__dirname, "..", "..", "..");
const SCRIPT = path.join(ROOT, "scripts", "long-form", "01-follow-one-dollar-v2", "script.md");
const OUT = path.join(__dirname, "png"), SHEETS = path.join(__dirname, "sheets");

function parseScript() {
  const text = fs.readFileSync(SCRIPT, "utf8").split("\n");
  const out = []; let section = "", cur = null;
  for (const ln of text) {
    let m;
    if ((m = ln.match(/^## (.+)$/))) section = m[1];
    else if ((m = ln.match(/^\*\*(S\d+) · (\w+) · ~\d+ s(?: · ([^*]+))?\*\*/))) { cur = { id: m[1], voice: m[2], tag: (m[3] || "").trim(), section, text: "", source: null }; out.push(cur); }
    else if (cur && (m = ln.match(/^\[SOURCE: (.+)\]$/))) cur.source = m[1];
    else if (cur && !cur.text && ln.trim() && !ln.startsWith("[")) cur.text = ln.trim();
  }
  return out;
}
// short on-screen version of a source note
function shortSource(s) {
  s = s.split(";")[0].replace(/\s*\([^)]*\)/g, "").trim();
  return "Source: " + (s.length > 64 ? s.slice(0, 61).trim() + "…" : s);
}
const stopOf = (section) => { const m = section.match(/^STOP (\d)/); return m ? +m[1] : null; };

function fontCss() {
  const dir = path.join(ROOT, "kit", "fonts");
  return [700, 800, 900].map((w) => `@font-face{font-family:"Nunito";font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(path.join(dir, `nunito-latin-${w}-normal.woff2`)).toString("base64")}) format("woff2");}`).join("");
}

function buildSvg(line) {
  const sc = SCENES[line.id];
  if (!sc) throw new Error("no scene for " + line.id);
  const stop = sc.stop !== undefined ? sc.stop : stopOf(line.section);
  let s = `<rect width="1920" height="1080" fill="${L.PAPER}"/>`;
  s += L.chip(sc.chip || line.section);
  if (sc.map !== false && (stop || sc.mapDone)) s += L.miniMap(stop || 0, sc.mapDone !== undefined ? sc.mapDone : stop - 1);

  const terms = sc.terms || (sc.term ? [sc.term] : []);
  // a plain-words card needs the bottom band, so the stage shrinks a little to make room
  const top = Math.min(...terms.map((tm) => L.termTop(tm[1], tm[2])), 9999);
  const k = terms.length && sc.fit !== false ? Math.min(0.9, (top - 24 - 236) / 614) : 1;
  s += `<g id="stage"${k < 1 ? ` transform="translate(${960 * (1 - k)} ${236 * (1 - k)}) scale(${k})"` : ""}>${sc.body || ""}</g>`;
  terms.forEach((tm, i, arr) => {
    const x = arr.length === 1 ? 960 : i === 0 ? 500 : 1420;
    s += L.termCard(tm[0], tm[1], { full: tm[2] || null, x });
  });
  const example = sc.example !== undefined ? sc.example : /EXAMPLE/.test(line.tag);
  if (sc.h) s += L.headline(sc.h, { ...(example ? { max: 36, width: 1220 } : {}), ...(sc.hOpts || {}) });
  if (example) s += L.P.exampleBadge(1720, 150, -6);
  if (line.source && sc.source !== false) s += `<g transform="translate(60 1040)">${L.P.sourceTag({ text: sc.sourceText || shortSource(line.source) })}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs>${L.WOBBLE_FILTER}</defs>${s}</svg>`;
}

// runs in the page: shrink long text, size boxes to their text, report text outside the safe area
const FIT = () => {
  document.querySelectorAll("text[data-max]").forEach((el) => {
    const m = +el.dataset.max, w = el.getComputedTextLength();
    if (w > m) el.setAttribute("font-size", (parseFloat(el.getAttribute("font-size")) * m / w).toFixed(1));
  });
  document.querySelectorAll(".fitbox").forEach((gp) => {
    const rect = gp.querySelector(":scope > rect"), texts = [...gp.querySelectorAll(":scope > text")];
    if (!rect || !texts.length) return;
    const pad = +(gp.dataset.pad || 24), minw = +(gp.dataset.minw || 0);
    const w = Math.max(minw, Math.max(...texts.map((x) => x.getComputedTextLength())) + pad * 2);
    const x0 = +rect.getAttribute("x"), w0 = +rect.getAttribute("width");
    if (gp.dataset.anchor === "start") rect.setAttribute("width", w);
    else { rect.setAttribute("x", x0 + w0 / 2 - w / 2); rect.setAttribute("width", w); }
  });
  const bad = [];
  document.querySelectorAll("text").forEach((el) => {
    const b = el.getBoundingClientRect();
    if (b.width && (b.left < 36 || b.right > 1884 || b.top < 20 || b.bottom > 1064)) bad.push(el.textContent.slice(0, 40));
  });
  const src = document.querySelector("#source rect"), terms = [...document.querySelectorAll(".term > rect")];
  if (src) terms.forEach((r) => { const a = r.getBoundingClientRect(), b = src.getBoundingClientRect(); if (a.left < b.right && a.right > b.left && a.bottom > b.top) bad.push("term card overlaps source tag"); });
  return bad;
};

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
