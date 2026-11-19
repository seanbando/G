# Rendering the cartoon shorts on your own PC

The 3D renderer needs a graphics card, so the final video is rendered on your computer rather than in the cloud
session. Everything else (scenes, timing, the sound mix) is already in this repository.

## One-time setup

1. Install **Node.js 20 or newer** from nodejs.org (the LTS installer is fine) and **Git** from git-scm.com.
2. Open a terminal (Windows: PowerShell; Mac: Terminal) and get the project:

```bash
git clone https://github.com/seanbando/G.git
```

```bash
cd G/remotion
```

```bash
npm install
```

## Render the $1 short

From the `G/remotion` folder:

```bash
node scripts/render-final.mjs
```

- The first run downloads a headless Chrome for Remotion (a minute or two).
- On a PC with a graphics card it takes roughly 10-20 minutes for the 69 s video.
- It writes `out/dollar/video.mp4` (picture only) and then `out/dollar/final.mp4`: **1440x2560, 30 fps, with the
  finished sound mix** (voice + score + effects from `shorts/one-dollar/audio/mix.flac`).

If you already cloned before, update first:

```bash
git pull
```

## If something goes wrong

- *Out of disk space*: every render bundle copies the project to the temp folder. Point it at a big drive, e.g.
  PowerShell `$env:REMOTION_TMP="D:\remotion-tmp"`, then render again. Delete old `remotion-webpack-bundle-*`
  folders there when you are done.
- *Black or blank frames / WebGL errors*: try `$env:GL="vulkan"` (PowerShell) or `GL=vulkan` (Mac/Linux) before the
  command; the default is `angle`.
- *The mux step fails*: the picture is still in `out/dollar/video.mp4`; mux it yourself with ffmpeg using
  `-map 0:v:0 -map 1:a:0` (Remotion writes a silent audio track).

## Quality check (optional, needs Python 3 + ffmpeg)

```bash
python scripts/short_qa.py out/dollar/final.mp4 out/dollar/qa shots.json
```

It checks every frame for black, white, frozen and popping frames plus loudness, and writes contact sheets.
