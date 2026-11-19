// Final 2K render of a cartoon short + mux with its sound mix, in one command (works on Windows, macOS, Linux).
// usage: node scripts/render-final.mjs [CompositionId] [mixFile] [outDir]
//   defaults: DollarShort, ../shorts/one-dollar/audio/mix.flac, out/dollar
// 1440x2560 (scale 4/3 of the 1080x1920 composition; "1.3333" gives an odd width that H.264 refuses), crf 16.
// Remotion writes a silent audio track, so the mix is muxed with -map 0:v:0 -map 1:a:0 (skill rule).
import path from "node:path";
import fs from "node:fs";
import { spawnSync } from "node:child_process";
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

const [id = "DollarShort", mix = "../shorts/one-dollar/audio/mix.flac", outDir = "out/dollar"] = process.argv.slice(2);
if (process.env.REMOTION_TMP) { fs.mkdirSync(process.env.REMOTION_TMP, { recursive: true }); process.env.TEMP = process.env.TMP = process.env.TMPDIR = process.env.REMOTION_TMP; }
fs.mkdirSync(outDir, { recursive: true });
const chromiumOptions = { gl: process.env.GL || "angle" };
const video = path.join(outDir, "video.mp4"), final = path.join(outDir, "final.mp4");
console.log("bundling...");
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), publicDir: path.resolve("public") });
const composition = await selectComposition({ serveUrl, id, chromiumOptions });
const t0 = Date.now();
let last = -1;
await renderMedia({
  composition, serveUrl, codec: "h264", crf: 16, scale: 4 / 3, outputLocation: video, chromiumOptions,
  timeoutInMilliseconds: 300000,
  onProgress: ({ progress }) => { const p = Math.floor(progress * 100); if (p !== last) { last = p; process.stdout.write(`\rrendering ${p}%  (${((Date.now() - t0) / 60000).toFixed(1)} min)`); } },
});
console.log(`\nrendered ${video}`);
const ff = spawnSync("npx", ["remotion", "ffmpeg", "-y", "-i", video, "-i", path.resolve(mix), "-map", "0:v:0", "-map", "1:a:0",
  "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", final], { stdio: "inherit", shell: process.platform === "win32" });
if (ff.status !== 0) { console.error("mux failed: run it yourself with ffmpeg using -map 0:v:0 -map 1:a:0"); process.exit(1); }
console.log(`done: ${final}`);
