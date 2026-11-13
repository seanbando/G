# Saylo — Channel Workspace

Everything for @watchsaylo lives here. Start every new chat (with Claude or GPT) by pasting `style-sheet.md`.

| File | What it is |
|---|---|
| `style-sheet.md` | The rules: channel, audience, voice, structure, blocked words, titles, thumbnails, workflow, GPT fact-check prompt |
| `channel/channel-audit.md` | Where the channel stood on Nov 13, 2026 and why the sniper video worked |
| `channel/competitor-analysis.md` | Uncovering / fern / Nexpo scripts, competitor thumbnails, title formats that work |
| `ideas/scorecard.md` | How ideas are scored, plus the ranked list of next videos |
| `videos/01-olympic-bomber/` | Script, package (title + thumbnail), fact-check log, thumbnail images |
| `tools/check_saylo.py` | Scans a script for blocked words, length and sentence rhythm |
| `CLAUDE.md` | Instructions Claude reads automatically when working in this folder |

## Video pipeline
| # | Video | Status |
|---|---|---|
| 01 | Why the Olympic Bomber Was So Hard to Catch | Script fact-checked once. Re-check new hook (18 months), then record. Thumbnail approved — finish text in Canva. |
| 02 | Whitey Bulger (scorecard #2) | Not started |
| 03 | Christopher Dorner (scorecard #3) | Not started |

## Check a script
```bash
python3 saylo/tools/check_saylo.py saylo/videos/01-olympic-bomber/script.md
```
