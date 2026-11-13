# Saylo — Channel Workspace

Everything for @watchsaylo lives here. Start every new chat (with Claude or GPT) by pasting `style-sheet.md`.

| File | What it is |
|---|---|
| `style-sheet.md` | The rules: channel, audience, voice, structure, blocked words, titles, thumbnails, workflow, GPT fact-check prompt |
| `channel/channel-audit.md` | Where the channel stood on Nov 13, 2026 and why the sniper video worked |
| `channel/competitor-analysis.md` | Uncovering / fern / Nexpo scripts, competitor thumbnails, title formats that work |
| `channel/edit-style-analysis.md` | Measured editing of Uncovering + fern videos: cuts/min, shot lengths, maps, documents, holds, silences |
| `ideas/scorecard.md` | How ideas are scored, plus the ranked list of next videos |
| `videos/01-olympic-bomber/` | Script, package (title + thumbnail), fact-check log, thumbnail images |
| `tools/check_saylo.py` | Scans a script for blocked words, length and sentence rhythm |
| `tools/analyze_edit.py` | Measures a reference video's editing (cuts, pacing, fades, silences) + contact sheets |
| `videos/01-olympic-bomber/edit-plan.md` | Shot budget per chapter, holds, silent moment, name tags, timestamp cards |
| `CLAUDE.md` | Instructions Claude reads automatically when working in this folder |

## Video pipeline
| # | Video | Status |
|---|---|---|
| 01 | Why the Olympic Bomber Was So Hard to Catch | Script fact-checked once. Re-check new hook (18 months), then record. Thumbnail approved — finish text in Canva. Edit plan done; shot list next. |
| 02 | Whitey Bulger (scorecard #2) | Not started |
| 03 | Christopher Dorner (scorecard #3) | Not started |

## Check a script
```bash
python3 saylo/tools/check_saylo.py saylo/videos/01-olympic-bomber/script.md
```

## Analyze a reference video
```bash
python3 saylo/tools/analyze_edit.py video.mp4 --sheets out/
```
