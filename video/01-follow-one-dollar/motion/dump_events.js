// Lists every motion event in the built sections with its time in the full video, for the sound pass.
// Usage: node video/01-follow-one-dollar/motion/dump_events.js  -> writes ../final/events.json
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const SECTIONS = [["hook", "S001"], ["pizza", "S012"], ["stop1", "S031"], ["stop2", "S040"], ["stop3", "S055"], ["stop4", "S067"], ["stop5", "S086"], ["money", "S102"], ["basket", "S127"], ["checks", "S142"], ["ending", "S154"]];
const T = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "..", "audio", "follow-one-dollar-v6", "timings.json"), "utf8"));
const start = Object.fromEntries(T.lines.map((l) => [l.id, l.start]));
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const all = [], sections = [];
  for (const [name, first] of SECTIONS) {
    const t0 = first === "S001" ? 0 : start[first] - 0.2;
    await page.goto("file://" + path.join(__dirname, name, "index.html"));
    await page.waitForTimeout(500);
    const ev = await page.evaluate(() => window.__sfx || null);
    if (!ev) throw new Error(name + " was built before events were recorded: rebuild it");
    ev.forEach((e) => all.push({ ...e, t: +(e.t + t0).toFixed(3), section: name }));
    sections.push({ name, first, t0: +t0.toFixed(3) });
  }
  await browser.close();
  all.sort((a, b) => a.t - b.t);
  fs.mkdirSync(path.join(__dirname, "..", "final"), { recursive: true });
  fs.writeFileSync(path.join(__dirname, "..", "final", "events.json"), JSON.stringify({ duration: T.duration, sections, events: all }, null, 1));
  console.log(all.length, "events");
})();
