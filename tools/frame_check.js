// Automatic frame check for a HyperFrames scene, run before anyone looks at it.
//
// Usage: node tools/frame_check.js <project-dir> [--video renders/x.mp4] [--step 0.25] [--out report-dir]
//
// Steps through the composition's timeline and, at every step, measures each visible
// text and object. Flags:
//   - EDGE:     anything outside the frame, touching it, or outside the 90% action-safe box
//               (text: outside the 80% title-safe box)
//   - OVERLAP:  text overlapping other text, or text covered by an object painted on top
//   - ERROR:    page errors, console errors, failed images or a missing timeline
// With --video, also scans the rendered frames' borders for anything that isn't background.
// Each problem moment gets a snapshot with red boxes in <out>/, plus report.md.
//
// Mark deliberate cases in the HTML: data-allow-edge (enters from off screen, full-bleed art)
// or data-allow-overlap (a label meant to sit on something).
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const args = process.argv.slice(2);
const dir = path.resolve(args[0] || ".");
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const STEP = parseFloat(opt("--step", "0.25"));
const OUT = path.resolve(opt("--out", path.join(dir, "frame-check")));
const VIDEO = opt("--video", null);
const W = 1920, H = 1080;
const ACTION = { x: W * 0.05, y: H * 0.05, w: W * 0.9, h: H * 0.9 };
const TITLE = { x: W * 0.1, y: H * 0.1, w: W * 0.8, h: H * 0.8 };

function inter(a, b) {
  const x = Math.max(a.x, b.x), y = Math.max(a.y, b.y);
  const r = Math.min(a.x + a.w, b.x + b.w), btm = Math.min(a.y + a.h, b.y + b.h);
  return r > x && btm > y ? (r - x) * (btm - y) : 0;
}
const inside = (a, box) => a.x >= box.x && a.y >= box.y && a.x + a.w <= box.x + box.w && a.y + a.h <= box.y + box.h;
const ts = s => `${Math.floor(s / 60)}:${(s % 60).toFixed(2).padStart(5, "0")}`;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const errors = [];
  page.on("pageerror", e => errors.push(`page error: ${e.message}`));
  page.on("console", m => { if (m.type() === "error") errors.push(`console error: ${m.text()}`); });
  page.on("requestfailed", r => {
    const u = r.url();
    if (u.startsWith("file://") && fs.existsSync(decodeURIComponent(u.slice(7)))) return; // exists; preview just can't play it
    errors.push(`failed to load: ${u}`);
  });
  await page.addInitScript(() => { window.__timelines = window.__timelines || {}; });
  await page.goto("file://" + path.join(dir, "index.html"));
  await page.waitForTimeout(800);
  const meta = await page.evaluate(() => {
    const root = document.querySelector("[data-composition-id]");
    const id = root && root.getAttribute("data-composition-id");
    const tl = id && window.__timelines[id];
    return { id, hasTimeline: !!tl, duration: root ? parseFloat(root.getAttribute("data-duration")) : 0 };
  });
  if (!meta.hasTimeline) errors.push(`no timeline registered for composition "${meta.id}"`);

  const issues = new Map(); // key -> {kind, msg, times:[], boxes}
  const add = (kind, key, msg, t, boxes) => {
    const k = kind + "|" + key;
    if (!issues.has(k)) issues.set(k, { kind, msg, times: [], boxes, first: t });
    issues.get(k).times.push(t);
  };

  for (let t = 0; t <= meta.duration + 1e-6 && meta.hasTimeline; t += STEP) {
    const items = await page.evaluate(({ t, id }) => {
      window.__timelines[id].seek(t, false);
      // clip visibility follows data-start / data-duration
      document.querySelectorAll(".clip").forEach(c => {
        const s = parseFloat(c.dataset.start || 0), d = parseFloat(c.dataset.duration || 1e9);
        c.style.visibility = t >= s && t < s + d ? "visible" : "hidden";
      });
      const visible = el => {
        for (let e = el; e && e.nodeType === 1; e = e.parentElement || e.parentNode) {
          const cs = getComputedStyle(e);
          if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) < 0.05) return false;
          if (e.getAttribute && e.getAttribute("opacity") !== null && parseFloat(e.getAttribute("opacity")) < 0.05) return false;
        }
        return true;
      };
      const flag = (el, attr) => { for (let e = el; e && e.nodeType === 1; e = e.parentElement || e.parentNode) if (e.hasAttribute && e.hasAttribute(attr)) return true; return false; };
      const name = el => {
        let p = el, idp = "";
        for (; p && p.nodeType === 1; p = p.parentElement || p.parentNode) if (p.id) { idp = "#" + p.id; break; }
        return el.tagName.toLowerCase() === "text" || el.tagName.toLowerCase() === "div" ? `"${(el.textContent || "").trim().slice(0, 40)}" (${idp || el.tagName})` : idp || el.tagName;
      };
      const out = [];
      let order = 0;
      const all = document.querySelectorAll("text, [id]");
      all.forEach(el => {
        order++;
        if (el.closest("defs, clipPath") || ["root", "AUDIO"].includes(el.id) || el.tagName === "AUDIO") return;
        if (el.matches(".clip, .layer, svg, [data-composition-id]")) return;
        const INLINE = ["B", "STRONG", "I", "EM", "SPAN", "SMALL", "BR", "TSPAN", "tspan"];
        const isText = el.tagName.toLowerCase() === "text" ||
          (!(el instanceof SVGElement) && (el.textContent || "").trim() && [...el.children].every(c => INLINE.includes(c.tagName)));
        if (!isText && !el.id) return;
        if (!visible(el)) return;
        let r = el.getBoundingClientRect();
        if (isText && !(el instanceof SVGElement)) {
          const range = document.createRange(); range.selectNodeContents(el);
          const rr = range.getBoundingClientRect(); if (rr.width > 0) r = rr;
        }
        if (r.width < 2 || r.height < 2) return;
        if (!isText && r.width * r.height > 0.6 * 1920 * 1080) return; // full-frame containers
        out.push({ name: name(el), text: isText, x: r.x, y: r.y, w: r.width, h: r.height, order,
                   allowEdge: flag(el, "data-allow-edge"), allowOverlap: flag(el, "data-allow-overlap"),
                   el: el.id || null, parentIds: (() => { const ids = []; for (let p = el.parentElement || el.parentNode; p && p.nodeType === 1; p = p.parentElement || p.parentNode) if (p.id) ids.push(p.id); return ids; })() });
      });
      return out;
    }, { t, id: meta.id });

    const objIds = new Set(items.filter(i => !i.text && i.el).map(i => i.el));
    for (const a of items) {
      if (a.parentIds.some(p => objIds.has(p))) continue;  // report the whole character/prop once, not each part
      if (!a.allowEdge) {
        if (a.x < 0 || a.y < 0 || a.x + a.w > W || a.y + a.h > H)
          add("EDGE", a.name, `${a.name} goes past the frame edge`, t, [a]);
        else if (a.x < 2 || a.y < 2 || a.x + a.w > W - 2 || a.y + a.h > H - 2)
          add("EDGE", a.name, `${a.name} touches the frame edge`, t, [a]);
        else if (a.text && !inside(a, TITLE))
          add("EDGE", a.name, `text ${a.name} is outside the title-safe area (inner 80%)`, t, [a]);
        else if (!a.text && !inside(a, ACTION))
          add("EDGE", a.name, `${a.name} is outside the action-safe area (inner 90%)`, t, [a]);
      }
    }
    const texts = items.filter(i => i.text);
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], b = texts[j];
      if (a.allowOverlap || b.allowOverlap) continue;
      const o = inter(a, b);
      if (o > 0.05 * Math.min(a.w * a.h, b.w * b.h)) add("OVERLAP", a.name + "~" + b.name, `text ${a.name} overlaps text ${b.name}`, t, [a, b]);
    }
    for (const tx of texts) for (const ob of items.filter(i => !i.text)) {
      if (tx.allowOverlap || ob.allowOverlap || ob.order < tx.order) continue;       // only objects painted on top
      if (tx.parentIds.includes(ob.el) || (ob.parentIds || []).some(p => tx.parentIds.includes(p) && p === ob.parentIds[0] && false)) continue;
      if (ob.parentIds.includes(tx.el)) continue;
      const o = inter(tx, ob);
      if (o > 0.15 * tx.w * tx.h) add("OVERLAP", tx.name + "^" + ob.name, `${ob.name} covers text ${tx.name}`, t, [tx, ob]);
    }
  }

  // Snapshots with red boxes for the first moment of each issue.
  let n = 0;
  const shots = new Map();
  for (const [, is] of issues) {
    n++;
    const file = `issue-${String(n).padStart(2, "0")}.png`;
    await page.evaluate(({ t, id, boxes }) => {
      window.__timelines[id].seek(t, false);
      document.querySelectorAll(".clip").forEach(c => {
        const s = parseFloat(c.dataset.start || 0), d = parseFloat(c.dataset.duration || 1e9);
        c.style.visibility = t >= s && t < s + d ? "visible" : "hidden";
      });
      document.querySelectorAll(".__fc").forEach(e => e.remove());
      boxes.forEach(b => {
        const d = document.createElement("div");
        d.className = "__fc";
        Object.assign(d.style, { position: "fixed", left: b.x + "px", top: b.y + "px", width: b.w + "px", height: b.h + "px",
          border: "5px solid #ff0033", boxSizing: "border-box", zIndex: 99999, pointerEvents: "none" });
        document.body.appendChild(d);
      });
    }, { t: is.first, id: meta.id, boxes: is.boxes });
    await page.screenshot({ path: path.join(OUT, file) });
    shots.set(is, file);
  }
  await browser.close();

  // Rendered video: anything non-background in a 3-pixel border.
  const videoIssues = [];
  if (VIDEO) {
    const dur = parseFloat(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VIDEO]).toString());
    const bg = execFileSync("ffmpeg", ["-nostdin", "-v", "error", "-ss", "0.05", "-i", VIDEO, "-frames:v", "1", "-vf", "crop=2:2:960:2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]);
    for (let t = 0.1; t < dur; t += 0.5) {
      const raw = execFileSync("ffmpeg", ["-nostdin", "-v", "error", "-ss", t.toFixed(2), "-i", VIDEO, "-frames:v", "1", "-vf", "scale=480:270", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]);
      const px = (x, y) => raw.subarray((y * 480 + x) * 3, (y * 480 + x) * 3 + 3);
      const off = p => Math.abs(p[0] - bg[0]) + Math.abs(p[1] - bg[1]) + Math.abs(p[2] - bg[2]) > 60;
      let hits = 0;
      for (let x = 0; x < 480; x++) for (const y of [0, 1, 268, 269]) if (off(px(x, y))) hits++;
      for (let y = 0; y < 270; y++) for (const x of [0, 1, 478, 479]) if (off(px(x, y))) hits++;
      if (hits > 6) videoIssues.push(t);
    }
  }

  const groups = { ERROR: [...new Set(errors)].map(e => `- ${e}`), EDGE: [], OVERLAP: [], BRIEF: [] };
  for (const [, is] of issues) {
    const span = `${ts(is.times[0])}–${ts(is.times[is.times.length - 1])}`;
    const brief = is.kind !== "ERROR" && is.times.length * STEP < 0.5;
    groups[brief ? "BRIEF" : is.kind].push(`- **${span}** · ${is.msg} · [snapshot](${shots.get(is)})`);
  }
  const lines = [`# Frame check: ${path.basename(dir)}`, "",
    `Checked every ${STEP} s over ${meta.duration} s.` + (VIDEO ? ` Rendered video border scanned every 0.5 s.` : ""), "",
    `## Errors (${groups.ERROR.length})`, ...(groups.ERROR.length ? groups.ERROR : ["- none"]), "",
    `## Edges and safe area (${groups.EDGE.length})`, ...(groups.EDGE.length ? groups.EDGE : ["- none"]), "",
    `## Overlaps (${groups.OVERLAP.length})`, ...(groups.OVERLAP.length ? groups.OVERLAP : ["- none"]), "",
    `## Brief moments under 0.5 s, usually transitions (${groups.BRIEF.length}, review but not counted)`,
    ...(groups.BRIEF.length ? groups.BRIEF : ["- none"]), ""];
  if (VIDEO) lines.push(`## Rendered video: something at the frame border (${videoIssues.length})`,
    ...(videoIssues.length ? videoIssues.map(t => `- ${ts(t)}`) : ["- none"]), "");
  const total = groups.ERROR.length + groups.EDGE.length + groups.OVERLAP.length + videoIssues.length;
  lines.push(total ? `**${total} issue(s) to fix.**` : "**All clear.**");
  fs.writeFileSync(path.join(OUT, "report.md"), lines.join("\n") + "\n");
  console.log(lines.join("\n"));
  process.exitCode = total ? 1 : 0;
})();
