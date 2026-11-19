# Original score for the $1 short, composed and synthesized here (F major, 120 bpm, quarter = 0.5 s). The band and
# render engine are the bridge short's (instruments.py, Band, per-track balance, hall reverb); the tune and the form
# are this story's: the music grows the way the dollar does.
#   hook: a glockenspiel motif, a rising arpeggio that doubles its notes with every doubling of the stack; cut on the flash
#   story: the theme on glock over pizzicato bass; each new "Day" adds players (day 10 oompah, day 20 snare, day 30 tutti)
#   climb (day 40 -> 48): the theme on fife + brass, marching snare, a roll into a dead stop on "Then,"
#   one more doubling: a timpani roll crescendo -> a tutti hit on "Day forty-nine" -> a golden pad (bigger than everyone)
#   "Luckily": the music stops dead (the deadpan joke plays dry)
#   snowball: a bass ostinato whose glock arpeggio doubles its note rate every beat
#   350 years: the theme half-speed on a music box
#   end: warm golden reprise on vibes and pad, a last chord that rings out
import numpy as np
from dsp import SR, ns, rng, pan, place, fades, dbg, make_ir, convolve_st, integrated, lp, hp
import instruments as I
import timeline as T

N = ns(T.DUR)
Q = 0.5
F = I.m2f

# theme: (bar, beat, quarters, midi)
THEME = [
    (1, 0, 1, 72), (1, 1, .5, 69), (1, 1.5, .5, 72), (1, 2, 1, 77), (1, 3, 1, 72),
    (2, 0, .5, 74), (2, .5, .5, 72), (2, 1, .5, 69), (2, 1.5, .5, 65), (2, 2, 2, 67),
    (3, 0, 1, 69), (3, 1, .5, 67), (3, 1.5, .5, 69), (3, 2, 1, 70), (3, 3, 1, 74),
    (4, 0, 3, 72),
    (5, 0, 1, 72), (5, 1, .5, 69), (5, 1.5, .5, 72), (5, 2, 1, 77), (5, 3, 1, 79),
    (6, 0, .5, 81), (6, .5, .5, 79), (6, 1, .5, 77), (6, 1.5, .5, 74), (6, 2, 2, 72),
    (7, 0, .5, 70), (7, .5, .5, 69), (7, 1, .5, 67), (7, 1.5, .5, 69), (7, 2, 1, 70), (7, 3, 1, 76),
    (8, 0, 2, 77), (8, 2, 1, 72), (8, 3, 1, 65),
]
CHB = {1: ["F"] * 4, 2: ["Bb", "Bb", "C", "C"], 3: ["F", "F", "Bb", "Bb"], 4: ["C7"] * 4, 5: ["F"] * 4,
       6: ["Bb", "Bb", "F", "F"], 7: ["Gm", "Gm", "C7", "C7"], 8: ["F"] * 4}
CH = {
    "F": dict(oom=(41, 36), pah=[53, 57, 60]), "Bb": dict(oom=(34, 41), pah=[53, 58, 62]),
    "C": dict(oom=(36, 43), pah=[52, 55, 60]), "C7": dict(oom=(36, 43), pah=[52, 58, 60]),
    "Gm": dict(oom=(43, 38), pah=[55, 58, 62]), "Dm": dict(oom=(38, 45), pah=[53, 57, 62]),
}

STORY0 = 7.0                 # "Day zero" at 7.08
CLIMB0 = 23.9                # "Day forty" at 23.98
STOP = 37.9                  # dead stop on "Then," (37.94)
HIT = T.fr(T.FAR_RISE1)      # "Day forty-nine" (39.67)
DRY0 = 45.35                 # "Luckily," at 45.46: silence
SNOW0, SNOW1 = T.fr(T.SNOW0) - 0.05, 56.95
SLOW0 = 57.0
END0 = 63.25

SECTIONS = [("hook", 0.0, T.FLASH), ("story", T.FLASH, CLIMB0), ("climb", CLIMB0, STOP), ("tension", STOP, HIT),
            ("hit", HIT, DRY0), ("dropout", DRY0, SNOW0), ("snowball", SNOW0, SLOW0), ("slow", SLOW0, END0), ("end", END0, T.DUR)]


def theme(t_bar1, bars=range(1, 9), transpose=0, q=Q):
    return sorted((t_bar1 + (b - 1) * 4 * q + beat * q, d * q, m + transpose) for (b, beat, d, m) in THEME if b in bars)


class Band:
    def __init__(self):
        self.tr, self.send, self.cues = {}, {}, []

    def track(self, name, send):
        if name not in self.tr:
            self.tr[name] = np.zeros((2, N)); self.send[name] = send
        return self.tr[name]

    def add(self, name, x, t, p=0.0, g=1.0, send=0.15):
        if t >= T.DUR:
            return
        buf = self.track(name, send)
        place(buf, pan(x, p) if np.ndim(x) == 1 else x, t, g)


R = rng(2026)
_r = lambda: rng(int(R.integers(1 << 30)))


def oompah(b, t_bar, chords, vel=0.6, pah_vel=0.4, pah=True, q=Q):
    for beat in range(4):
        c = CH[chords[beat]]
        t = t_bar + beat * q
        b.add("tuba", I.brass(F(c["oom"][beat % 2]), 0.3, vel * (1.0 if beat in (0, 2) else 0.88), _r(), "tuba"), t, -0.1)
        if pah:
            for k, m in enumerate(c["pah"]):
                b.add("pah", I.brass(F(m), 0.15, pah_vel, _r(), "horn", scoop=-12), t + q / 2 + 0.004 * k, 0.32 - 0.12 * k)


def pizz(b, t_bar, chords, vel=0.6, q=Q):
    for beat in range(4):
        c = CH[chords[beat]]
        b.add("pluck", I.pluck(F(c["oom"][beat % 2] + 12), vel, _r(), 0.6), t_bar + beat * q, -0.15)


def snare_bar(b, t_bar, vel, pat=(3, 0, 1, 1, 2, 0, 1, 0, 3, 0, 1, 1, 2, 0, 1, 0)):
    for s, v in enumerate(pat):
        if v:
            b.add("snare", I.snare(vel * {1: 0.5, 2: 0.9, 3: 0.95}[v] * R.uniform(0.93, 1.05), _r()), t_bar + s * Q / 4, 0.05)


def roll(b, t0, t1, v0, v1):
    for t, v in I.snare_roll(t0, t1, v0, v1, _r()):
        b.add("snare", I.snare(v, _r(), dur=0.14, buzz=True), t, 0.05)


def mel(b, name, notes, vel, fn="glock", p=0.0, until=None):
    for (t, d, m) in notes:
        if until is not None and t >= until:
            continue
        if fn == "glock":
            x = I.glock(F(m), vel * R.uniform(0.92, 1.05), _r())
        elif fn == "fife":
            x = I.fife(F(m), d * 0.9, vel * R.uniform(0.94, 1.04), _r())
        elif fn == "vibes":
            x = I.vibes(F(m), vel * R.uniform(0.92, 1.05), _r(), dur=max(1.2, d + 0.8), damp=d + 0.35)
        elif fn == "musicbox":
            x = I.musicbox(F(m), vel * R.uniform(0.92, 1.05), _r())
        else:
            x = I.brass(F(m), d * 0.9, vel, _r(), "horn", scoop=-10)
        b.add(name, x, t, p)


def build():
    b = Band()
    # ---------------- hook: motif + doubling arpeggio, cut on the flash
    mel(b, "glock", theme(0.0, bars=[1, 2]), 0.7)
    for k, f in enumerate(T.DOUBLINGS):            # each doubling: twice as many arpeggio notes, one step higher
        n = 2 ** min(k, 4)
        for j in range(n):
            m = [65, 69, 72, 77][j % 4] + 12 * (j // 4 % 2) + (k // 3) * 2
            b.add("glock", I.glock(F(m), 0.45, _r(), 0.9), T.fr(f) + j * 0.16 / n, 0.3)
    for bar in range(3):
        pizz(b, bar * 2.0, CHB[bar % 2 + 1] if bar < 2 else CHB[3], 0.55)
    mel(b, "glock", theme(4.0, bars=[3]), 0.6, until=T.FLASH - 0.05)
    b.add("cymbal", I.cymbal(0.5, _r(), 1.4), T.FLASH - 0.6, 0.0)
    b.cues.append((0.0, "hook motif + doubling arpeggio, cut on the white flash"))

    # ---------------- story: theme on glock; players join on each "Day"
    days = {10: 10.9, 20: 15.3, 30: 19.5}
    for bar in range(1, 9):
        tb = STORY0 + (bar - 1) * 2.0
        if tb >= CLIMB0:
            break
        ch = CHB[bar]
        if tb < days[10]:
            pizz(b, tb, ch, 0.55)
        else:
            oompah(b, tb, ch, 0.55, 0.32 if tb >= days[20] else 0.0, pah=tb >= days[20] - 0.1)
        if tb >= days[20] - 0.1:
            snare_bar(b, tb, 0.35 if tb < days[30] else 0.5)
        if tb >= days[30] - 0.1:
            b.add("triangle", I.triangle(0.5, _r()), tb, 0.4)
    mel(b, "glock", theme(STORY0), 0.7, until=CLIMB0 - 0.1)
    roll(b, CLIMB0 - 0.5, CLIMB0, 0.3, 0.7)
    b.cues.append((STORY0, "theme on glock; oompah from day 10, horns + snare from day 20, triangle from day 30"))

    # ---------------- climb: fife + horn theme, marching snare, roll into the dead stop
    bars = int((STOP - CLIMB0) // 2.0)
    for bar in range(1, bars + 1):
        tb = CLIMB0 + (bar - 1) * 2.0
        oompah(b, tb, CHB[bar], 0.7, 0.42)
        snare_bar(b, tb, 0.6 + 0.04 * bar)
    mel(b, "fife", theme(CLIMB0, bars=range(1, bars + 1)), 0.7, "fife", until=STOP - 1.5)
    mel(b, "horn", theme(CLIMB0, bars=range(1, bars + 1), transpose=-12), 0.45, "horn", -0.2, until=STOP - 1.5)
    roll(b, STOP - 1.5, STOP - 0.02, 0.4, 1.0)
    for m in (53, 57, 60, 65):
        b.add("stab", I.brass(F(m), 0.18, 0.9, _r(), "stab"), STOP - 0.02, 0.0)
    b.cues.append((CLIMB0, "climb: fife + horn theme, march snare, roll -> stab, dead stop on \"Then,\""))

    # ---------------- tension -> hit -> golden pad
    for t, v in I.snare_roll(STOP + 0.25, HIT - 0.02, 0.15, 1.0, _r(), rate=22.0):
        b.add("timpani", I.timpani(F(41), v * 0.6, _r(), 0.5), t, 0.0)
    for m in (41, 53, 57, 60, 65, 69):
        b.add("stab", I.brass(F(m), 0.9, 1.0, _r(), "stab"), HIT, 0.1 * (m % 3 - 1))
    b.add("timpani", I.timpani(F(41), 1.0, _r(), 2.2), HIT, 0.0)
    b.add("cymbal", I.cymbal(0.9, _r(), 3.0), HIT, 0.0)
    b.add("pad", I.pad([F(53), F(57), F(60), F(65)], DRY0 - HIT - 1.3, 0.55, _r(), att=0.8, rel=0.4), HIT + 0.3, 0.0)
    mel(b, "vibes", theme(HIT + 1.0, bars=[5, 6], q=0.6), 0.55, "vibes", until=DRY0 - 0.4)
    b.cues.append((HIT, "tutti hit on \"Day forty-nine\", golden pad + vibes; dead stop at \"Luckily\""))

    # ---------------- snowball: ostinato, arpeggio doubling its rate each beat
    nb = int((SLOW0 - SNOW0) / Q)
    for k in range(nb):
        t = SNOW0 + k * Q
        root = [41, 41, 46, 48][(k // 4) % 4]
        b.add("pluck", I.pluck(F(root), 0.6, _r(), 0.5), t, -0.15)
        b.add("pluck", I.pluck(F(root + 12), 0.45, _r(), 0.4), t + Q / 2, -0.15)
        n = 2 ** min(3, k // 3)
        for j in range(n):
            m = [65, 69, 72, 77, 81, 84][j % 6] + (2 if k >= nb // 2 else 0)
            b.add("glock", I.glock(F(m), 0.35 + 0.04 * min(k, 8), _r(), 0.7), t + j * Q / n, 0.25)
    b.add("cymbal", I.cymbal(0.6, _r(), 1.8), SLOW0 - 0.05, 0.0)
    b.cues.append((SNOW0, "snowball ostinato: arpeggio rate doubles every 3 beats"))

    # ---------------- 350 years: half-speed music box
    mel(b, "musicbox", theme(SLOW0 + 0.2, bars=[1, 2, 3], q=0.7), 0.6, "musicbox", until=END0 - 0.2)
    b.add("pad", I.pad([F(53), F(57), F(60)], END0 - SLOW0 - 1.0, 0.3, _r(), att=1.2, rel=0.8), SLOW0, 0.0)
    b.cues.append((SLOW0, "350 years: the theme half-speed on a music box"))

    # ---------------- end: golden reprise
    for bar, ch in enumerate([CHB[5], CHB[6]]):
        tb = END0 + bar * 2.0
        oompah(b, tb, ch, 0.45, 0.28)
    mel(b, "vibes", theme(END0, bars=[5, 6]), 0.65, "vibes")
    last = END0 + 4.3
    for m in (65, 69, 72, 77):
        b.add("vibes", I.vibes(F(m), 0.6, _r(), dur=2.5), last + 0.03 * (m % 4), 0.0)
    b.add("pad", I.pad([F(53), F(57), F(60), F(65)], T.DUR - last - 0.5, 0.45, _r(), att=0.3, rel=0.6), last, 0.0)
    b.add("tuba", I.brass(F(29 + 12), 1.4, 0.6, _r(), "tuba"), last, -0.1)
    b.add("triangle", I.triangle(0.5, _r(), 2.0), last, 0.4)
    b.cues.append((END0, "golden reprise on vibes, final F chord rings out"))

    # silence where the story needs it: the dead stop after the hit/pad and the deadpan joke
    for k in b.tr:
        x = b.tr[k]
        a, e = ns(DRY0), ns(SNOW0)
        x[:, a:e] = 0.0
        a2 = ns(T.FLASH)
        x[:, a2: ns(STORY0) - 1] *= 0.0
    return b


TARGET = {"fife": -3.0, "glock": -6.0, "tuba": -2.5, "pah": -7.5, "snare": -5.5, "cymbal": -11.0, "stab": -3.0, "timpani": -5.0,
          "pad": -3.5, "vibes": -2.0, "musicbox": -1.5, "pluck": -4.0, "triangle": -15.0, "horn": -6.0}


def render(b, ref=-20.0):
    hall = make_ir(1.5, 7, pre=0.018, hf=1.4)
    dry = np.zeros((2, N))
    wet = np.zeros((2, N))
    levels = {}
    for k, x in b.tr.items():
        if not np.any(x):
            continue
        L = integrated(x)
        g = dbg(ref + TARGET.get(k, -6) - L)
        levels[k] = (round(L, 1), round(ref + TARGET.get(k, -6), 1))
        x = x * g
        b.tr[k] = x
        dry += x
        wet += b.send[k] * x
    out = dry + 0.7 * convolve_st(wet.mean(0), hall)
    out = hp(out, 30, 2)
    # hard stops survive the reverb: the deadpan stays dry
    out[:, ns(DRY0 + 0.25): ns(SNOW0)] *= 0.0
    return out, levels
