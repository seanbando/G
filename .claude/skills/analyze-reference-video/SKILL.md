---
name: analyze-reference-video
description: Measure the editing style (cuts, pacing, zooms, transitions, maps, music gaps) of competitor/reference YouTube videos the creator uploads, and turn it into Saylo editing rules or a shot list. Use when the creator shares reference videos (Google Drive folder/link or files) and asks how they're edited, or wants a video edited "like" a competitor.
---

# Analyze a reference video's editing

## 1. Get the files
- The creator uploads compressed copies (360p–480p, audio kept, full length) to Google Drive.
- Find them with the Google Drive connector (`search_files`, e.g. `title contains 'compressed'`). Note each file `id`.
- The connector can't download files over 10 MB. Download directly instead:
  ```bash
  curl -sSL -o NAME.mp4 "https://drive.usercontent.google.com/download?id=FILE_ID&export=download&confirm=t"
  ```
  - Needs `drive.usercontent.google.com` on the environment allowlist (added Nov 2026).
  - Needs the file/folder shared "Anyone with the link · Viewer". If `file NAME.mp4` says HTML, it's still private — ask the creator to change sharing.
- Save videos to the scratchpad, never into the repo (size + copyright).

## 2. Measure
```bash
python3 saylo/tools/analyze_edit.py A.mp4 B.mp4 --sheets <scratchpad>/sheets
```
Gives shots, mean/median shot length, % under 2s / over 10s, cuts/min per third, hook cuts (first 60s), fades to black, full silences.

## 3. Look
Read the contact sheets (`*.hook.jpg` = first 60s every 2s, `*.overview-N.jpg` = every 20s). Note: map style, document treatment, name tags, archival framing, recreations, host shots, chapter cards, color grade.

## 4. Save
- Add results to `saylo/channel/edit-style-analysis.md` (table + observations).
- If the rules change, update `saylo/style-sheet.md` §8 (source of truth).
- For a specific video, write/refresh `saylo/videos/NN-slug/edit-plan.md` (shot budget per chapter), then `shot-list.md`.
- Tell the creator they can delete the Drive copies and set the folder back to Restricted once results are committed.
