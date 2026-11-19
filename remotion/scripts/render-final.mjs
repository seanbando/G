// Final 2K render of a cartoon short + mux with its sound mix, in one command (works on Windows, macOS, Linux).
// usage: node scripts/render-final.mjs [CompositionId] [mixFile] [outDir]
//   defaults: DollarShort, ../shorts/one-dollar/audio/mix.flac, out/dollar
// - 1440x2560 (scale 4/3 of the 1080x1920 composition; "1.3333" gives an odd width that H.264 refuses), crf 16.
// - Renders in chunks of CHUNK frames (default 150) into out/<name>/parts/. If the PC or the render stops, run the same
//   command again: finished chunks are kept and it carries on from the first missing one.
// - CONCURRENCY browser tabs at once (default 2). Every tab holds the whole 3D town at 2K in graphics memory, so the
//   Remotion default (half the CPU threads) can exhaust the GPU and crash the driver. Use 1 if it still struggles.
// - Remotion writes a silent audio track, so the mix is muxed with -map 0:v:0 -map 1:a:0 (skill rule).
import path from "node:path";
import fs from "node:fs";
import { spawnSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

const [id = "DollarShort", mix = "../shorts/one-dollar/audio/mix.flac", outDir = "out/dollar"] = process.argv.slice(2);
const CHUNK = Number(process.env.CHUNK || 150), CONC = Number(process.env.CONCURRENCY || 2);
if (process.env.REMOTION_TMP) { fs.mkdirSync(process.env.REMOTION_TMP, { recursive: true }); process.env.TEMP = process.env.TMP = process.env.TMPDIR = process.env.REMOTION_TMP; }
const parts = path.join(outDir, "parts");
fs.mkdirSync(parts, { recursive: true });
const chromiumOptions = { gl: process.env.GL || "angle" };
const ffmpeg = (args) => spawnSync("npx", ["remotion", "ffmpeg", ...args], { stdio: "inherit", shell: process.platform === "win32" }).status === 0;

console.log(`bundling... (${CONC} tab${CONC > 1 ? "s" : ""}, chunks of ${CHUNK} frames)`);
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), publicDir: path.resolve("public") });
const composition = await selectComposition({ serveUrl, id, chromiumOptions });
const total = composition.durationInFrames, n = Math.ceil(total / CHUNK), t0 = Date.now();
const list = [];
for (let k = 0; k < n; k++) {
  const a = k * CHUNK, b = Math.min(total - 1, a + CHUNK - 1);
  const file = path.join(parts, `part_${String(k).padStart(3, "0")}.mp4`);
  list.push(file);
  if (fs.existsSync(file) && fs.statSync(file).size > 0) { console.log(`chunk ${k + 1}/${n} (frames ${a}-${b}) already done, skipping`); continue; }
  const tmp = file.replace(/\.mp4$/, ".tmp.mp4");
  let last = -1;
  await renderMedia({
    composition, serveUrl, codec: "h264", crf: 16, scale: 4 / 3, outputLocation: tmp, chromiumOptions, frameRange: [a, b],
    concurrency: CONC, timeoutInMilliseconds: 300000,
    onProgress: ({ progress }) => {
      const p = Math.floor(((k + progress) / n) * 100);
      if (p !== last) { last = p; process.stdout.write(`\rrendering ${p}%  chunk ${k + 1}/${n}  (${((Date.now() - t0) / 60000).toFixed(1)} min)   `); }
    },
  });
  fs.renameSync(tmp, file); // only a finished chunk gets its final name, so a crash never leaves a broken one behind
}
console.log("\njoining chunks...");
const listFile = path.join(parts, "list.txt");
fs.writeFileSync(listFile, list.map((f) => `file '${path.resolve(f).replace(/\\/g, "/")}'`).join("\n"));
const video = path.join(outDir, "video.mp4"), final = path.join(outDir, "final.mp4");
if (!ffmpeg(["-y", "-f", "concat", "-safe", "0", "-i", listFile, "-map", "0:v:0", "-c", "copy", video])) { console.error("joining failed"); process.exit(1); }
if (!ffmpeg(["-y", "-i", video, "-i", path.resolve(mix), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
  "-movflags", "+faststart", "-t", String(total / composition.fps), final])) { console.error("mux failed: the picture is in " + video); process.exit(1); }
console.log(`done: ${final}`);
