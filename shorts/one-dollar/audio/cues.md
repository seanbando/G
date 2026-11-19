# How Many Days Until $1 Owns the World - soundtrack cue sheet

All sound is original: synthesized in numpy/scipy by `sfx_gen.py` / `instruments.py`, placed by `sfx.py` / `music.py`, mixed by `mix.py`.
Voice = `voice/voice.wav`, gain only (no EQ, no compression, no pitch).

## Files
| file | content |
|---|---|
| `mix.wav` | final mix, 48 kHz, stereo, 24-bit, 3,312,000 samples = 69.000 s |
| `stem_voice.wav` / `stem_music.wav` / `stem_sfx.wav` | stems at mix gain (they sum to the mix before the master limiter) |

## Master loudness (own BS.1770-4 meter)
- Integrated **-15.0 LUFS**, true peak **-1.2 dBTP**, LRA 2.4 LU, max momentary -9.2 LUFS, max short-term -12.9 LUFS
- Stems: voice -14.9 LUFS, music -24.7 LUFS, sfx -37.4 LUFS (voice gain +5.93 dB, same gain on every stem)
- Master limiter (4x oversampled look-ahead, ceiling -1.2 dBTP): max gain reduction 2.38 dB, active (>0.1 dB) on 5.94 % of samples, >0.5 dB on 2.20 %

ffmpeg ebur128 cross-check:
```
Summary:
  Integrated loudness:
    I:         -15.0 LUFS
    Threshold: -25.2 LUFS
  Loudness range:
    LRA:         2.4 LU
    Threshold: -35.3 LUFS
    LRA low:   -16.4 LUFS
    LRA high:  -14.0 LUFS
  True peak:
    Peak:       -1.2 dBFS
```

## Voice on top: per-section loudness (LUFS, integrated per stem, at mix gain)
bed = music + sfx. margin = voice - bed (integrated over the section). speech median / p10 = median and 10th percentile of the 400 ms momentary margin (voice - bed) over windows centred on spoken words.

| section (shots) | time s | voice | music | sfx | bed | margin LU | speech median LU | speech p10 LU |
|---|---|---|---|---|---|---|---|---|
| hook | 0.00-6.83 | -14.3 | -23.8 | -28.9 | -23.2 | 8.9 | 10.8 | 6.0 |
| story | 6.83-23.90 | -14.9 | -24.9 | -38.4 | -24.7 | 9.8 | 10.2 | 4.8 |
| climb | 23.90-37.90 | -15.4 | -24.9 | -41.6 | -24.8 | 9.4 | 9.4 | 5.6 |
| tension | 37.90-39.67 | -13.7 | -23.9 | -37.2 | -23.8 | 10.1 | 9.4 | 3.2 |
| hit | 39.67-45.35 | -15.3 | -24.3 | -36.8 | -24.0 | 8.7 | 8.0 | 4.1 |
| dropout | 45.35-50.92 | -14.2 | - | -45.0 | -45.0 | 30.8 | 30.8 | 27.3 |
| snowball | 50.92-57.00 | -14.8 | -24.3 | -39.3 | -24.1 | 9.4 | 9.3 | 2.7 |
| slow | 57.00-63.25 | -15.9 | -26.8 | -40.3 | -26.6 | 10.8 | 10.0 | 7.6 |
| end | 63.25-69.00 | -14.8 | -24.3 | -43.4 | -24.3 | 9.5 | 12.4 | 5.7 |

## Music map (original score, F major, 120 bpm)
Music target per section, LU under the voice (after a -3 dB speech duck keyed from words.json): hook -9.5, story -10.0, climb -9.5, tension -10.0, hit -9.0, dropout -10.0, snowball -9.5, slow -11.0, end -9.5. Applied section gains (dB): hook -6.1, story -5.6, climb -11.1, tension -1.8, hit -7.4, dropout -7.4, snowball -6.3, slow -10.3, end -6.1.

Rides (music only, dB):  - so quiet sentence-final words stay on top and the band blooms in the gaps after them. The hook's last two footfalls (3.5, 4.0) are also 3 dB lower in the SFX for '...walking across it.'

| time s | frame | music |
|---|---|---|
| 0.00 | 0 | hook motif + doubling arpeggio, cut on the white flash |
| 7.00 | 210 | theme on glock; oompah from day 10, horns + snare from day 20, triangle from day 30 |
| 23.90 | 717 | climb: fife + horn theme, march snare, roll -> stab, dead stop on "Then," |
| 39.67 | 1190 | tutti hit on "Day forty-nine", golden pad + vibes; dead stop at "Luckily" |
| 50.92 | 1528 | snowball ostinato: arpeggio rate doubles every 3 beats |
| 57.00 | 1710 | 350 years: the theme half-speed on a music box |
| 63.25 | 1898 | golden reprise on vibes, final F chord rings out |

## SFX events
Level convention: every EVENT has a naive level (LU vs the voice stem, as the event's max momentary loudness); applied = naive - 6 dB (standard mix rule) + distance/intensity offsets. BEDS are integrated loudness, not reduced. 'mix LUFS' = the event's max momentary loudness in the final mix (voice stem = -14.9 LUFS integrated). Column sounds also get the camera-distance low-pass and more valley reverb.

| # | time s | frame | cue | what | naive LU | applied LU | mix LUFS | pan |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.000 | 0.0 | amb_street (bed, integrated) | street air: breeze, sparrows (hook table) | -30 | -30.0 | -44.9 | +0.00 |
| 2 | 0.100 | 3.0 | bill_set | a crisp bill laid on the table ("One dollar") | -14 | -20.0 | -34.9 | +0.00 |
| 3 | 1.000 | 30.0 | double | the stack doubles (2 bills) | -15 | -21.0 | -35.9 | -0.10 |
| 4 | 1.167 | 35.0 | double | the stack doubles (4 bills) | -14 | -19.8 | -34.7 | +0.00 |
| 5 | 1.333 | 40.0 | double | the stack doubles (8 bills) | -13 | -18.6 | -33.5 | +0.10 |
| 6 | 1.500 | 45.0 | double | the stack doubles (16 bills) | -11 | -17.4 | -32.3 | -0.10 |
| 7 | 1.667 | 50.0 | double | the stack doubles (32 bills) | -10 | -16.2 | -31.1 | +0.00 |
| 8 | 1.833 | 55.0 | double | the stack doubles (64 bills) | -9 | -15.0 | -29.9 | +0.10 |
| 9 | 2.000 | 60.0 | double | the stack doubles (128 bills) | -8 | -13.8 | -28.7 | -0.10 |
| 10 | 2.167 | 65.0 | double | the stack doubles (256 bills) | -7 | -12.6 | -27.5 | +0.00 |
| 11 | 2.333 | 70.0 | double | the stack doubles (512 bills) | -5 | -11.4 | -26.3 | +0.10 |
| 12 | 2.500 | 75.0 | amb_high (bed, integrated) | high wind over the money mountains (aerial, summit) | -31 | -31.0 | -45.9 | +0.00 |
| 13 | 2.500 | 75.0 | whoosh_aerial | whoosh up to the aerial over both mountains | -14 | -20.0 | -34.9 | +0.00 |
| 14 | 2.567 | 77.0 | kaching | money sting on "outgrows" | -11 | -17.0 | -31.9 | +0.00 |
| 15 | 6.833 | 205.0 | amb_street2 (bed, integrated) | street air (day 0 .. day 40) | -30 | -30.0 | -44.9 | +0.00 |
| 16 | 6.833 | 205.0 | flash | white flash whoosh + soft boom into "Day zero" | -10 | -16.0 | -30.9 | +0.00 |
| 17 | 8.167 | 245.0 | bill_close | paper crinkle on the bill close-up | -18 | -24.0 | -38.9 | +0.00 |
| 18 | 11.933 | 358.0 | wallet_stuff | wallet stuffed fat: paper riffle | -15 | -21.0 | -35.9 | +0.20 |
| 19 | 14.133 | 424.0 | wallet_pop | bills popping out of the wallet | -16 | -22.0 | -36.9 | +0.20 |
| 20 | 15.267 | 458.0 | house_pour | bills pouring out of every window (continuous) | -14 | -20.0 | -34.9 | -0.30 |
| 21 | 17.867 | 536.0 | house_whoa | the owner: "whoa" (needs the whole house) | -18 | -24.0 | -38.9 | -0.10 |
| 22 | 19.533 | 586.0 | street_crowd | neighbours wading in money: laughs, hoorays, murmur | -19 | -25.0 | -39.9 | +0.00 |
| 23 | 19.533 | 586.0 | street_rain | bills raining on the street | -18 | -24.0 | -38.9 | +0.00 |
| 24 | 21.900 | 657.0 | whoosh_up | whoosh up over the street | -17 | -23.0 | -37.9 | +0.00 |
| 25 | 23.900 | 717.0 | hill_boom | impact on the kick | -12 | -18.0 | -32.9 | +0.00 |
| 26 | 23.900 | 717.0 | hill_rise | the money hill heaves up over the rooftops | -10 | -16.0 | -30.9 | +0.00 |
| 27 | 27.733 | 832.0 | rich_gasp | the richest person's gasp | -15 | -21.0 | -35.9 | +0.15 |
| 28 | 29.400 | 882.0 | amb_high2 (bed, integrated) | high wind over the buried town (day 48/49, summit) | -30 | -30.0 | -44.9 | +0.00 |
| 29 | 29.400 | 882.0 | whoosh_half | whoosh up to the aerial (day 48) | -15 | -21.0 | -35.9 | +0.00 |
| 30 | 38.400 | 1152.0 | far_rise | the far bank fills with money (one more doubling) | -8 | -14.0 | -28.9 | +0.00 |
| 31 | 39.667 | 1190.0 | far_boom | the big impact on "Day forty-nine" | -9 | -15.0 | -29.9 | +0.00 |
| 32 | 40.933 | 1228.0 | kaching2 | money sting on "five hundred sixty-three trillion" | -13 | -19.0 | -33.9 | +0.00 |
| 33 | 45.267 | 1358.0 | amb_table (bed, integrated) | quiet street at the table again (luckily / unluckily) | -31 | -31.0 | -45.9 | +0.00 |
| 34 | 48.567 | 1457.0 | deadpan | a single paper flick on the cut to "Unluckily" | -20 | -26.0 | -40.9 | +0.00 |
| 35 | 50.900 | 1527.0 | amb_high3 (bed, integrated) | wind on the mountain (snowball, halves) | -31 | -31.0 | -45.9 | +0.00 |
| 36 | 50.967 | 1529.0 | snow_roll | the money snowball rolling and growing down the mountain | -12 | -18.0 | -32.9 | +0.00 |
| 37 | 53.333 | 1600.0 | whoosh_halves | whoosh to the two halves | -16 | -22.0 | -36.9 | +0.00 |
| 38 | 56.833 | 1705.0 | amb_years (bed, integrated) | 350 years: birds, crickets, wind, the town passing | -30 | -30.0 | -44.9 | +0.00 |
| 39 | 57.400 | 1722.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 40 | 57.400 | 1722.0 | tree_grow | the tree creaking up from a sapling | -22 | -28.0 | -42.9 | -0.30 |
| 41 | 57.900 | 1737.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 42 | 58.400 | 1752.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 43 | 58.900 | 1767.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 44 | 59.400 | 1782.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 45 | 59.900 | 1797.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 46 | 60.400 | 1812.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 47 | 60.900 | 1827.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 48 | 61.400 | 1842.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 49 | 61.900 | 1857.0 | tick | clock tick (time passing at 10 % a year) | -22 | -28.0 | -42.9 | +0.30 |
| 50 | 63.100 | 1893.0 | amb_golden (bed, integrated) | golden evening: soft breeze, blackbirds, crickets | -31 | -31.0 | -45.9 | +0.00 |
| 51 | 63.233 | 1897.0 | whoosh_gold | soft whoosh into the golden aerial | -18 | -24.0 | -38.9 | +0.00 |
| 52 | 66.067 | 1982.0 | bill_keep | the bill tucked away ("keep the dollar") | -18 | -24.0 | -38.9 | +0.00 |
| 53 | 67.333 | 2020.0 | whoosh_crane | slow whoosh on the crane out | -20 | -26.0 | -40.9 | +0.00 |
