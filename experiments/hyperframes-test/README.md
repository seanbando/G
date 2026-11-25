# HyperFrames look test

A 19.5-second hand-built test of the custom 2D look for the $1 journey video, rendered with HyperFrames 0.9.92 (HTML + GSAP rendered to MP4). Narration is three lines from the v1 recording.

- `index.html`: the whole scene (road map, Buck, phone, pizza) as SVG animated with GSAP
- `hyperframes-test.mp4`: the render (1920×1080, 30 fps)

Re-render (telemetry off):

```bash
DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1 npx --yes hyperframes@0.9.92 render
```
