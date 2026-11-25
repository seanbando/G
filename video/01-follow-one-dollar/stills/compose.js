// Shared by the stills renderer and the motion builder: reads the script, and turns one
// script line + its scene layout into a full 1920 x 1080 SVG frame.
const fs = require("fs");
const path = require("path");
const L = require("./lib.js");
const SCENES = require("./scenes.js");
const ROOT = path.join(__dirname, "..", "..", "..");
const SCRIPT = path.join(ROOT, "scripts", "long-form", "01-follow-one-dollar-v2", "script.md");

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
// The label viewers see top-left. Script headings that are production words (HOOK, ENDING)
// show nothing; the others are reworded for the viewer.
function chipLabel(section) {
  if (/^(HOOK|ENDING)$/.test(section)) return null;
  if (/^CHECKPOINT/.test(section)) return "QUICK CHECK";
  return section.replace(/^THE DEVICE · /, "").replace(/^TODAY · /, "");
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
  const label = sc.chip || chipLabel(line.section);
  if (label) s += L.chip(label);
  if (sc.map !== false && (stop || sc.mapDone)) s += L.miniMap(stop || 0, sc.mapDone !== undefined ? sc.mapDone : stop - 1);

  const terms = sc.terms || (sc.term ? [sc.term] : []);
  // a plain-words card needs the bottom band, so the stage shrinks a little to make room
  const wrapAt = terms.length > 1 ? 34 : 54;   // two cards side by side are narrower
  const top = Math.min(...terms.map((tm) => L.termTop(tm[1], tm[2], wrapAt)), 9999);
  const k = terms.length && sc.fit !== false ? Math.min(0.9, (top - 24 - 236) / 614) : 1;
  // "cam" is the camera: motion can push in on it without disturbing the stage's own fit
  s += `<g class="cam"><g class="stage"${k < 1 ? ` transform="translate(${960 * (1 - k)} ${236 * (1 - k)}) scale(${k})"` : ""}>${sc.body || ""}</g></g>`;
  terms.forEach((tm, i, arr) => {
    const x = arr.length === 1 ? 960 : i === 0 ? 570 : 1350;
    s += L.termCard(tm[0], tm[1], { full: tm[2] || null, x, wrapAt });
  });
  const example = sc.example !== undefined ? sc.example : /EXAMPLE/.test(line.tag);
  if (sc.h) s += L.headline(sc.h, { ...(example ? { max: 36, width: 1220 } : {}), ...(sc.hOpts || {}) });
  if (example) s += `<g class="exbadge" data-allow-edge>${L.P.exampleBadge(1720, 150, -6)}</g>`;
  if (line.source && sc.source !== false) s += `<g class="src" data-allow-edge transform="translate(60 1040)">${L.P.sourceTag({ text: sc.sourceText || shortSource(line.source) })}</g>`;
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


module.exports = { parseScript, buildSvg, fontCss, FIT, SCENES, ROOT, shortSource };
