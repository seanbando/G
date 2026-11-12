# Voiceover Recipe (approved by the creator)

The creator called the Nvidia final voiceover (`audio/nvidia-300-billion-final-sfx/preview-mix.mp3`, 59.5 s) "perfect". Make every short's voiceover this way unless the creator asks otherwise. Its files are in `scripts/shorts/02-nvidia-300-billion/` (`script-final.md`, `speeds-final.txt`, `tempo-final.txt`, `sfx-final.txt`).

## Voices

| Role | Voice | Use |
|---|---|---|
| NARRATOR | Yaboy, the creator's cloned voice | Everything except the two roles below |
| YOU | Eric (Smooth, Trustworthy) | One short viewer question right after the hook, answered right away |
| NEWS ANCHOR | Andrew (Crisp Announcer) | Headlines in news shorts ("Breaking tonight…", "This just in…") |

At most two extra voices in a short, each with one job. Never voice a real person.

## Delivery settings (narrator style D)

- Model `eleven_v4`, stability 0.4, similarity 0.8, style 0.2, speaker boost on (the defaults in `tools/generate_voiceovers.py`).
- Generate at speed 1.0 (pass a speeds sheet so the long video's 1.12 hook speed isn't applied). The model mostly ignores its speed setting, so pace is fixed when joining instead.
- Each line is generated with the lines around it as context, so delivery flows between files.

## Script shape

- About 150 to 160 words for a 60-second short; this voice reads about 160 to 165 words a minute.
- One spoken line per drawing; every line names one drawable thing and one motion (see `docs/script-system.md`).
- Numbers and abbreviations written out for the voice ("three hundred billion", "A-I", "C-E-O", "S and P five hundred").
- Hooks about every 5 to 8 seconds; end with a callback to the opening, then a twist that lands on the viewer.
- `[PAUSE: N seconds]` only where a beat should land: after the first payoff, after the peak, after a big reveal, before the callback.

## Editing instead of regenerating

- When the script changes, re-record only the changed lines (`--only VO-07,VO-08`) and copy the unchanged recordings in under their new line numbers. Never regenerate the whole narration for a small change.

## Joining the track (this is what removed the dead space)

```bash
python3 tools/build_track.py <script.md> <clips_dir> <out.mp3> --keep-pace --tight --tempo <tempo.txt>
```

- `--tight`: pauses and quiet breaths inside a line capped at about 0.2 s, lines 0.1 s apart (0.15 s when the speaker changes), script pauses cut to 60%.
- `--keep-pace`: no automatic speed changes, so deliberate slow beats stay slow.
- `--tempo`: pitch-safe speed-ups only for lines the voice model read too slowly. In the approved version: anchor headline 1.25, escalation line 1.08, anchor "This just in" 1.15, one slow narrator line 1.05. Target: anchor around 145 to 165 words a minute, escalation 185 to 195, slow emphasis lines left alone.
- Check the length and the gaps afterwards (silencedetect at -40 dB, 0.3 s); remaining 0.3 to 0.6 s gaps should only be intended beats.
- Loudness: narration at -15 to -14 LUFS, peaks under -1 dB (done by the builder).

## Sound effects

```bash
python3 tools/build_sfx.py <sfx.txt> <narration.mp3> <out_dir>
```

- Get word timestamps with ElevenLabs speech-to-text (`scribe_v1`, word granularity) and place each effect on the exact word.
- One effect per beat, never two at once; leave the silence after the peak empty.
- Effects levelled around -18 to -26 LUFS, about 6 dB under the voice; the mix stays as loud as the voice alone.
- Reuse existing sounds across versions; generate only new ones.
- Deliver `sfx-track.mp3` (drop at 0:00 in CapCut) and `preview-mix.mp3` (voice plus effects).
- Golpo gets the voice-only track; effects are added in the editor.
