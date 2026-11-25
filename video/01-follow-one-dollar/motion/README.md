# Motion: Follow $1 From Your Pocket to Wall Street

Animated scenes, built from the stills and timed to the real voiceover.

- `build.js` turns a range of script lines into a HyperFrames project: `node video/01-follow-one-dollar/motion/build.js hook S001 S011`
- `hook/` (S001–S011), `pizza/` (S012–S030) and `stop1/` (S031–S039): each has `index.html` (generated, don't edit by hand), `assets/`, and the rendered `.mp4`

How timing works: each script line is one clip that starts when the narrator starts that line, and each tagged part appears on the word it belongs to (`audio/follow-one-dollar-v5/timings.json`). So when the voice speeds up the pictures speed up, and when it pauses they wait. If the voiceover is re-recorded, rebuild and everything re-times itself.

How to change motion: in `../stills/scenes-*.js`, parts are wrapped in `A(part, word, effect)`. Effects: `pop`, `fade`, `slide`, `wipe` (draws on like a pen), `stamp`, `move`; `idle: "talk"` makes a mascot hop as it speaks. Stills ignore these tags, so the still and the animation always match.

Check, then render (telemetry off):

```bash
node tools/frame_check.js video/01-follow-one-dollar/motion/hook
```

```bash
cd video/01-follow-one-dollar/motion/hook && DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1 HF_CLI_TELEMETRY_DISABLED=1 npx --yes hyperframes@0.9.92 render
```

Sound effects are added in one pass at the end, once all scenes are done.
