// Builds an animated HyperFrames scene from the stills, timed to the real voiceover.
//
// Usage: node video/01-follow-one-dollar/motion/build.js <name> <first-line> <last-line>
//   e.g. node video/01-follow-one-dollar/motion/build.js hook S001 S011
// Writes motion/<name>/ (index.html, assets/, hyperframes.json, package.json).
//
// Every script line is one clip that starts when the narrator starts that line
// (audio/follow-one-dollar-v6/timings.json). Parts tagged with A(...) in the scene files
// appear on the exact word they are tied to, so fast lines move fast and pauses wait.
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const C = require("../stills/compose.js");

const [name, first, last, audioDir] = process.argv.slice(2); // audioDir: optional, default the v6 voiceover
if (!name || !first || !last) { console.error("usage: build.js <name> <first-line> <last-line>"); process.exit(1); }
const AUDIO_DIR = audioDir ? path.resolve(audioDir) : path.join(C.ROOT, "audio", "follow-one-dollar-v6");
const T = JSON.parse(fs.readFileSync(path.join(AUDIO_DIR, "timings.json"), "utf8"));
const OUT = path.join(__dirname, name);
fs.mkdirSync(path.join(OUT, "assets"), { recursive: true });

const script = C.parseScript();
const ids = script.map((l) => l.id);
const i0 = ids.indexOf(first), i1 = ids.indexOf(last);
const tl = T.lines;
const t0 = i0 === 0 ? 0 : tl[i0].start - 0.2;                       // where this part starts in the full track
const tEnd = i1 + 1 < tl.length ? tl[i1 + 1].start - 0.15 : T.duration;   // 0.05 s overlap with the next part; assemble.py trims it
const total = +(tEnd - t0).toFixed(3);

// cut this part's audio out of the full narration
execFileSync("ffmpeg", ["-nostdin", "-v", "error", "-y", "-ss", String(t0), "-t", String(total), "-i", path.join(AUDIO_DIR, "narration.mp3"),
  "-c:a", "libmp3lame", "-b:a", "160k", path.join(OUT, "assets", "narration.mp3")]);
const gsapSrc = path.join(C.ROOT, "experiments", "hyperframes-test", "assets", "gsap.min.js");
fs.copyFileSync(gsapSrc, path.join(OUT, "assets", "gsap.min.js"));

const scenes = [];
let clips = "";
for (let i = i0; i <= i1; i++) {
  const line = script[i], sc = C.SCENES[line.id], tm = tl[i];
  const start = i === i0 ? 0 : +(tm.start - t0 - 0.12).toFixed(3);   // picture leads the voice slightly
  const end = i === i1 ? total : +(tl[i + 1].start - t0 - 0.12).toFixed(3);
  const prev = i > i0 ? C.SCENES[script[i - 1].id] : null;
  scenes.push({ id: line.id, start, dur: +(end - start).toFixed(3), lineStart: +(tm.start - t0).toFixed(3), lineEnd: +(tm.end - t0).toFixed(3),
    words: tm.words.map((w) => ({ w: w.word, t: +(w.start - t0).toFixed(3), e: +(w.end - t0).toFixed(3) })), enter: sc.enter || "fade",
    sameHeadline: !!(prev && prev.h && prev.h === sc.h), anims: sc.anims || [] });
  const svg = C.buildSvg(line).replace(/^<svg[^>]*>/, `<svg viewBox="0 0 1920 1080">`).replace(/<rect width="1920" height="1080"[^>]*\/>/, "");
  clips += `      <div id="sc-${line.id}" class="clip layer scene" data-start="${start}" data-duration="${(end - start).toFixed(3)}" data-track-index="${(i - i0) % 2}">\n        ${svg}\n      </div>\n`;
}

const RUNTIME = function (SCENES, FIT) {
  FIT();
  const NS = "http://www.w3.org/2000/svg";
  const tl = gsap.timeline({ paused: true });
  const LEAD = 0.1; // start a touch early so the move lands on the word
  let clipN = 0;
  const when = (sc, on) => {
    if (!on || on === "start") return sc.start + 0.05;
    if (on === "end") return sc.lineEnd + 0.1;            // right after the line is spoken (e.g. the quiz pause)
    if (on[0] === "+") return sc.lineStart + parseFloat(on);
    const after = on.endsWith(">");                      // "word>" = right after the word (for numbers)
    const [w, n] = on.replace(">", "").toLowerCase().split(":");
    const hits = sc.words.filter((x) => x.w === w);
    const hit = hits[(parseInt(n || "1", 10) || 1) - 1];
    if (!hit) { console.error(`motion: word "${on}" is not in line ${sc.id}`); return sc.start + 0.05; }
    return Math.max(sc.start + 0.02, after ? hit.e + 0.02 : hit.t - LEAD);
  };
  const apply = (sc, svg, el, a) => {
    const at = when(sc, a.on) + parseFloat(a.delay || 0);
    const dir = a.dir || "u", dur = parseFloat(a.dur || 0);
    if (a.fx === "pop") tl.fromTo(el, { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: dur || 0.4, ease: "back.out(1.9)" }, at);
    else if (a.fx === "fade") tl.fromTo(el, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: dur || 0.4, ease: "power2.out" }, at);
    else if (a.fx === "slide") {
      const d = { u: { y: 260 }, d: { y: -260 }, l: { x: -420 }, r: { x: 420 } }[dir];
      tl.fromTo(el, { opacity: 0, ...d }, { opacity: 1, x: 0, y: 0, duration: dur || 0.55, ease: "back.out(1.3)" }, at);
    } else if (a.fx === "stamp") {
      tl.fromTo(el, { scale: 2.6, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: dur || 0.22, ease: "power4.in" }, at);
      tl.fromTo(el, { rotation: -5 }, { rotation: 0, duration: 0.3, ease: "elastic.out(1.2, 0.4)" }, at + 0.22);
    } else if (a.fx === "pulse") {
      tl.fromTo(el, { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.07, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut" }, at);
    } else if (a.fx === "drain") {
      tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.15 }, at);
      tl.fromTo(el, { scaleX: 1, transformOrigin: "0% 50%" }, { scaleX: 0, duration: dur || 3, ease: "none" }, at + 0.1);
    } else if (a.fx === "scalefrom") {
      tl.fromTo(el, { scale: parseFloat(a.from || 1), transformOrigin: "50% 50%" }, { scale: 1, duration: dur || 0.8, ease: "power2.inOut" }, at);
    } else if (a.fx === "move") {
      tl.to(el, { x: parseFloat(a.dx || 0), y: parseFloat(a.dy || 0), duration: dur || 1, ease: "power1.inOut" }, at);
    } else if (a.fx === "wipe") {
      // reveal along a direction, like a pen drawing the line
      const b = el.getBBox(), pad = 24, id = "wipe" + clipN++;
      const cp = document.createElementNS(NS, "clipPath"); cp.setAttribute("id", id);
      const r = document.createElementNS(NS, "rect");
      const full = { x: b.x - pad, y: b.y - pad, width: b.width + pad * 2, height: b.height + pad * 2 };
      Object.entries(full).forEach(([k, v]) => r.setAttribute(k, v));
      cp.appendChild(r); svg.querySelector("defs").appendChild(cp);
      el.setAttribute("clip-path", `url(#${id})`);
      const from = dir === "r" ? { width: 0 } : dir === "l" ? { x: full.x + full.width, width: 0 } : dir === "d" ? { height: 0 } : { y: full.y + full.height, height: 0 };
      tl.fromTo(r, { attr: { ...full, ...from } }, { attr: full, duration: dur || 0.8, ease: "power1.inOut" }, at);
    }
  };
  SCENES.forEach((sc) => {
    const box = document.getElementById("sc-" + sc.id), svg = box.querySelector("svg");
    // scene arrives: a quick soft fade of the stage, unless it continues the last picture
    if (sc.enter !== "cut" && sc.start > 0) tl.fromTo(svg.querySelector(".stage"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power1.out" }, sc.start);
    const h = svg.querySelector(".headline");
    if (h && !sc.sameHeadline) tl.fromTo(h, { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, sc.start + 0.02);
    svg.querySelectorAll(".anim").forEach((el) => apply(sc, svg, el, el.dataset));
    sc.anims.forEach((a) => svg.querySelectorAll(a.sel).forEach((el) => apply(sc, svg, el, a)));
    svg.querySelectorAll(".idle").forEach((el) => {
      if (el.dataset.idle === "bob") tl.to(el, { y: -10, duration: 0.7, yoyo: true, repeat: Math.max(1, Math.floor(sc.dur / 0.7)), ease: "sine.inOut" }, sc.start);
      else if (el.dataset.idle === "talk") {
        // a small hop on each spoken word, plus a slight lean, so the character looks like it is talking
        sc.words.forEach((w, k) => { if (k % 2 === 0) tl.to(el, { y: -14, rotation: k % 4 ? 1.5 : -1.5, transformOrigin: "50% 100%", duration: 0.11, yoyo: true, repeat: 1, ease: "sine.out" }, Math.max(sc.start, w.t - 0.02)); });
      }
    });
    // plain-words cards rise in when the term is said (or halfway through the line)
    svg.querySelectorAll(".term").forEach((el) => {
      const first = (el.querySelector(":scope > text").textContent || "").toLowerCase().split(/[^a-z0-9&+']+/).filter(Boolean)[0];
      const hits = sc.words.filter((x) => x.w === first);
      const at = hits.length ? hits[hits.length - 1].t - LEAD : sc.lineStart + (sc.lineEnd - sc.lineStart) * 0.5;
      tl.fromTo(el, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.4)" }, Math.max(sc.start + 0.05, at));
    });
    svg.querySelectorAll(".src, .exbadge").forEach((el) => tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.3 }, sc.start + 0.3));
  });
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
  tl.seek(0);
};

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      ${C.fontCss()}
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #f6f3ea; }
      #root { position: relative; width: 100%; height: 100%; font-family: "Nunito"; }
      .layer { position: absolute; inset: 0; }
      svg { position: absolute; inset: 0; width: 1920px; height: 1080px; overflow: visible; }
    </style>
  </head>
  <body>
    <!-- Built by motion/build.js from stills ${first}–${last}. Do not edit by hand: change the scene files and rebuild. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="${total}" data-width="1920" data-height="1080">
      <audio id="vo" class="clip" data-start="0" data-duration="${total}" data-track-index="9" src="assets/narration.mp3"></audio>
${clips}    </div>
    <script>
      (${RUNTIME.toString()})(${JSON.stringify(scenes)}, ${C.FIT.toString()});
    </script>
  </body>
</html>
`;
fs.writeFileSync(path.join(OUT, "index.html"), html);
fs.writeFileSync(path.join(OUT, "hyperframes.json"), JSON.stringify({ $schema: "https://hyperframes.heygen.com/schema/hyperframes.json", registry: "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry", paths: { blocks: "compositions", components: "compositions/components", assets: "assets" }, media: { autoProxy: true } }, null, 2) + "\n");
fs.writeFileSync(path.join(OUT, "package.json"), JSON.stringify({ name: "follow-one-dollar-" + name, private: true, type: "module", scripts: { render: "npx --yes hyperframes@0.9.92 render" } }, null, 2) + "\n");
console.log(`built ${OUT}: ${scenes.length} scenes, ${total} s (track ${t0.toFixed(2)}–${tEnd.toFixed(2)} s)`);
