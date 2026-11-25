# Motion: Follow $1 From Your Pocket to Wall Street

Animated scenes, built from the stills and timed to the real voiceover.

- `build.js` turns a range of script lines into a HyperFrames project: `node video/01-follow-one-dollar/motion/build.js hook S001 S011`
- One folder per section, each with `index.html` (generated, don't edit by hand), `assets/`, and the rendered `.mp4`:
  `hook/` (S001–S011), `pizza/` (S012–S030), `stop1/` (S031–S039), `stop2/` (S040–S054), `stop3/` (S055–S066), `stop4/` (S067–S085, with checkpoint 1 and the quiz), `stop5/` (S086–S101), `money/` (S102–S126, with checkpoint 2), `basket/` (S127–S141), `checks/` (S142–S153), `ending/` (S154–S164)
- `assemble.py` joins the sections into `../final/follow-one-dollar.mp4` with the complete voiceover: `python3 video/01-follow-one-dollar/motion/assemble.py`

How timing works: each script line is one clip that starts when the narrator starts that line, and each tagged part appears on the word it belongs to (`audio/follow-one-dollar-v6/timings.json`). So when the voice speeds up the pictures speed up, and when it pauses they wait. If the voiceover is re-recorded, rebuild and everything re-times itself.

How to change motion: in `../stills/scenes-*.js`, parts are wrapped in `A(part, word, effect)`. Effects: `pop`, `fade`, `slide`, `wipe` (draws on like a pen), `stamp`, `move`; `idle: "talk"` makes a mascot hop as it speaks. Stills ignore these tags, so the still and the animation always match.

Check, then render (telemetry off):

```bash
node tools/frame_check.js video/01-follow-one-dollar/motion/hook
```

```bash
cd video/01-follow-one-dollar/motion/hook && DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1 HF_CLI_TELEMETRY_DISABLED=1 npx --yes hyperframes@0.9.92 render
```

## The master

```bash
node video/01-follow-one-dollar/motion/dump_events.js
```

```bash
python3 video/01-follow-one-dollar/motion/mix_audio.py
```

```bash
python3 video/01-follow-one-dollar/motion/assemble.py
```

```bash
python3 video/01-follow-one-dollar/motion/make_extras.py
```

- `dump_events.js` lists every motion event with its time in the full video (`../final/events.json`).
- `mix_audio.py` mixes voice + music + sound effects (`audio/music/`, `audio/sfx/`) to YouTube loudness. `--music-db -31` sets the music level, `--sfx-db 0` raises or lowers all sound effects.
- `assemble.py` joins the sections and puts the master audio on top (`../final/follow-one-dollar.mp4`).
- `make_extras.py` writes captions (`captions.srt`) and YouTube chapters (`youtube-chapters.txt`).

Also built in: mascots sway and blink; ten key reveals get a slow camera push-in (`zoom: [word, x, y, scale]` on a scene).
