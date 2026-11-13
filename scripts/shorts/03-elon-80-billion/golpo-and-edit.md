# Elon short: Golpo render and edit

- Golpo job `1351e55d-e421-4d57-98a1-352d499357c8` (Editorial, marker, fast pacing, camera follow, dramatic music), narration `audio/elon-80-billion-FAST.mp3` (the punched "B" voice, 50.0 s). Cost 0.75 credits.
- Checked frame by frame: all 10 scenes drawn as mapped; narration at 0:00 with no drift; a 2 s still tail after the last word.
- Edit (`transitions.txt`, `tools/edit_short.py`): 13 transitions on Golpo's scene changes (zoom-throughs on the big beats, whips between), punches on key words, shakes on impacts, slow pushes over the moments where Golpo held a finished drawing. Quietest second went from 0 to 11 on the motion scan.
- Audio: Golpo's track (-20.4 LUFS) raised to the narration's level, plus the 20 word-timed sound effects (`sfx-fast.txt`) and 13 whooshes (`transition-sfx.txt`), cut at 50.1 s, -14 LUFS, peaks -1.7 dB.
- Output: `video/elon-80-billion-final.mp4`, captions `video/elon-80-billion-captions.srt` (51), cover `video/elon-80-billion-cover.png`.
