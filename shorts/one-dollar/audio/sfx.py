# Every sound effect + ambience bed of the $1 short as a cue list timed to the picture (timeline.py), rendered into
# one stereo SFX stem. Levels follow the skill's standard mix: each EVENT has a "naive" level (LU relative to the voice
# stem, as the event's max momentary loudness) and is placed SFX_DB = -6 dB under it; ambience BEDS (integrated
# loudness) are not reduced. Engine (Cue, render, valley reverb) is the bridge short's; the cues are this story's.
import numpy as np
from dsp import (SR, ns, tt, rng, dbg, lp, hp, bp, peq, pan, st, place, fades, widen, make_ir, convolve_st,
                 momentary_max, integrated, colored, smooth_noise)
import sfx_gen as G
import instruments as I
import timeline as T

N = ns(T.DUR)
SFX_DB = -6.0


class Cue:
    def __init__(self, t, name, desc, gen, naive, kind="event", p=0.0, extra=0.0, lpf=None, send=0.12, group=None, cut=None):
        self.t, self.name, self.desc, self.gen, self.naive = t, name, desc, gen, naive
        self.kind, self.p, self.extra, self.lpf, self.send, self.cut = kind, p, extra, lpf, send, cut
        self.group = group or name
        self.applied = naive + (SFX_DB if kind == "event" else 0.0) + extra
        self.measured = None


# ------------------------------------------------ own sounds for this story
def paper(dur, r, rate=18.0, bright=1.0):
    """bills flapping / riffling: dense short band-passed noise ticks (paper), a soft body under them"""
    n = ns(dur)
    y = np.zeros(n)
    cnt = int(rate * dur) + 1
    for tm in np.sort(r.uniform(0, dur, cnt)):
        d = r.uniform(0.012, 0.045)
        k = ns(d)
        t = np.arange(k) / SR
        tick = bp(r.standard_normal(k), r.uniform(1800, 3200) * bright, r.uniform(5500, 9000), 1) * np.exp(-t / (d * 0.35))
        G._place_mono(y, tick * r.uniform(0.3, 1.0), tm)
    body = lp(bp(colored(n, r, 0.4), 500, 4000, 1), 4500) * 0.08 * (0.6 + 0.4 * smooth_noise(n, r, 6))
    return fades(y + body, 0.01, 0.05)


def flip(r):
    """one bill landing on the stack: a quick paper slap"""
    d = 0.09
    t = tt(d)
    y = bp(r.standard_normal(len(t)), 900, 6000, 1) * np.exp(-t / 0.012) + lp(r.standard_normal(len(t)), 600) * np.exp(-t / 0.02) * 0.4
    return fades(y, 0.001, 0.02)


def kaching(r):
    """the till: two bells + a coin rattle (the hook's money sting)"""
    y = np.zeros(ns(1.4))
    G._place_mono(y, I.glock(I.m2f(88), 0.8, r, 1.2) * 0.6, 0.0)
    G._place_mono(y, I.glock(I.m2f(93), 0.9, r, 1.3) * 0.7, 0.09)
    G._place_mono(y, G.rattle(0.35, r, 70) * 0.5, 0.05)
    return y


def rumble(dur, r, peak=0.5, lo=45, hi=220):
    """a mass of money heaving up: low rolling rumble with a paper-hiss top"""
    n = ns(dur)
    t = np.arange(n) / SR
    env = np.where(t < peak, (t / peak) ** 1.5, np.exp(-(t - peak) / (dur * 0.35)))
    low = lp(bp(colored(n, r, 1.6), lo, hi, 2), hi) * 3.0
    hiss = paper(dur, r, 60, 0.8) * 0.5
    return (low + hiss) * env


def boom(r, f=48, dur=1.2):
    t = tt(dur)
    y = np.sin(2 * np.pi * f * t * (1 - 0.25 * t)) * np.exp(-t / 0.32) + lp(r.standard_normal(len(t)), 300) * np.exp(-t / 0.08) * 0.6
    return fades(y, 0.002, 0.1)


def tick(r, hi=True):
    """clock tick (the 350 years)"""
    d = 0.05
    t = tt(d)
    return G.clink(r, 3400 if hi else 2800, d, 0.6) * 0.6 + bp(r.standard_normal(len(t)), 1500, 5000, 1) * np.exp(-t / 0.004) * 0.4


def cues():
    C = []
    R = rng(2026)
    rr = lambda: rng(int(R.integers(1 << 30)))
    add = C.append
    fr = T.fr

    # ------------------------------------------------ ambience beds (not reduced by the -6 dB event rule)
    def amb(dur, seed, birds=0.45, wind=1.0, crick=0.0, town=0.0):
        def g():
            r = rng(seed)
            n = ns(dur)
            x = G.breeze(dur, r, wind, 0.15, 850)
            x += pan(G.bird_chirps(dur, r, birds, "sparrow") * 0.08, 0.5)
            x += pan(G.bird_chirps(dur, r, birds * 0.6, "sparrow") * 0.05, -0.6)
            if crick:
                x += widen(G.crickets(dur, r, 3) * 0.008 * crick, r, 9, 1.0)
            if town:
                x += st(lp(bp(colored(n, r, 0.8), 150, 1400, 1), 1200) * 0.3 * town)
            return fades(x, 0.3, 0.4), 0.0
        return g
    high = lambda dur, seed: (lambda: (fades(G.breeze(dur, rng(seed), 1.4, 0.3, 600), 0.4, 0.4), 0.0))
    # street level (shots 1, 4-9 ground shots): breeze, sparrows, a little town air
    add(Cue(0.0, "amb_street", "street air: breeze, sparrows (hook table)", amb(fr(75) + 0.2, 1, town=0.6), -30, "bed", send=0.0))
    add(Cue(fr(75), "amb_high", "high wind over the money mountains (aerial, summit)", high(fr(209 - 75) + 0.15, 2), -31, "bed", send=0.0))
    add(Cue(fr(205), "amb_street2", "street air (day 0 .. day 40)", amb(fr(882 - 205) + 0.2, 3, town=0.8), -30, "bed", send=0.0))
    add(Cue(fr(882), "amb_high2", "high wind over the buried town (day 48/49, summit)", high(fr(1362 - 882) + 0.2, 4), -30, "bed", send=0.0))
    add(Cue(fr(1358), "amb_table", "quiet street at the table again (luckily / unluckily)", amb(fr(1527 - 1358) + 0.15, 5, birds=0.6), -31, "bed", send=0.0))
    add(Cue(fr(1527), "amb_high3", "wind on the mountain (snowball, halves)", high(fr(1709 - 1527) + 0.15, 6), -31, "bed", send=0.0))
    add(Cue(fr(1705), "amb_years", "350 years: birds, crickets, wind, the town passing", amb(fr(1897 - 1705) + 0.2, 7, birds=0.8, crick=1.0), -30, "bed", send=0.0))
    add(Cue(fr(1893), "amb_golden", "golden evening: soft breeze, blackbirds, crickets", amb(T.DUR - fr(1893), 8, birds=0.35, wind=0.7, crick=1.0), -31, "bed", send=0.0))

    # ------------------------------------------------ hook: one bill, doubling on the table
    add(Cue(fr(3), "bill_set", "a crisp bill laid on the table (\"One dollar\")", lambda r=rr(): (flip(r), 0.0), -14))
    for k, f in enumerate(T.DOUBLINGS):
        add(Cue(fr(f), "double", f"the stack doubles ({2 ** (k + 1)} bills)", lambda r=rr(), k=k: (paper(0.12 + 0.03 * k, r, 40 + 20 * k), 0.0),
                -15 + 1.2 * k, p=0.1 * ((k % 3) - 1), group="doublings"))
    add(Cue(fr(75), "whoosh_aerial", "whoosh up to the aerial over both mountains", lambda r=rr(): (G.whoosh(0.9, r, 0.45, 300, 2800, 0.9, 0.3, 0.3), 0.45), -14))
    add(Cue(fr(77), "kaching", "money sting on \"outgrows\"", lambda r=rr(): (kaching(r), 0.0), -11))
    add(Cue(T.FLASH, "flash", "white flash whoosh + soft boom into \"Day zero\"",
            lambda r=rr(): (widen(G.whoosh(0.75, r, 0.33, 500, 4200, 0.9, 0.09, 0.4) + np.where(tt(0.75) > 0.33, np.exp(-(tt(0.75) - 0.33) / 0.12) * np.sin(2 * np.pi * 62 * (tt(0.75) - 0.33)), 0) * 0.8, r, 12, 0.9), 0.33), -10))

    # ------------------------------------------------ day 0 .. day 10
    add(Cue(fr(245), "bill_close", "paper crinkle on the bill close-up", lambda r=rr(): (paper(0.3, r, 25), 0.0), -18))
    add(Cue(fr(358), "wallet_stuff", "wallet stuffed fat: paper riffle", lambda r=rr(): (paper(0.6, r, 50), 0.0), -15, p=0.2))
    add(Cue(fr(424), "wallet_pop", "bills popping out of the wallet", lambda r=rr(): (paper(0.9, r, 35, 1.2), 0.0), -16, p=0.2))

    # ------------------------------------------------ day 20: the house pours money
    add(Cue(fr(458), "house_pour", "bills pouring out of every window (continuous)",
            lambda r=rr(): (fades(paper(fr(584 - 458) + 0.1, r, 140), 0.15, 0.3), 0.0), -14, p=-0.3))
    add(Cue(fr(536), "house_whoa", "the owner: \"whoa\" (needs the whole house)", lambda r=rr(): (G.whoa(r, 150), 0.0), -18, p=-0.1))
    # ------------------------------------------------ day 30: the street
    add(Cue(fr(586), "street_crowd", "neighbours wading in money: laughs, hoorays, murmur",
            lambda r=rr(): (fades(_crowd(fr(717 - 586), r), 0.2, 0.4), 0.0), -19))
    add(Cue(fr(586), "street_rain", "bills raining on the street", lambda r=rr(): (fades(paper(fr(717 - 586), r, 90, 1.1), 0.2, 0.3), 0.0), -18))
    add(Cue(fr(657), "whoosh_up", "whoosh up over the street", lambda r=rr(): (G.whoosh(0.6, r, 0.25, 400, 2600, 0.8, 0.2, 0.2), 0.25), -17))
    # ------------------------------------------------ day 40: the hill, the richest person
    add(Cue(fr(T.HILL_RISE), "hill_rise", "the money hill heaves up over the rooftops", lambda r=rr(): (rumble(1.6, r, 0.35), 0.35), -10))
    add(Cue(fr(T.HILL_RISE), "hill_boom", "impact on the kick", lambda r=rr(): (boom(r, 52, 1.0), 0.0), -12))
    add(Cue(fr(T.RICH_SHOCK), "rich_gasp", "the richest person's gasp", lambda r=rr(): (G.oof(r, "oh", 120, 1.0), 0.0), -15, p=0.15))
    # ------------------------------------------------ day 48 / 49
    add(Cue(fr(882), "whoosh_half", "whoosh up to the aerial (day 48)", lambda r=rr(): (G.whoosh(0.8, r, 0.4, 300, 2400, 0.9, 0.3, 0.25), 0.4), -15))
    add(Cue(fr(T.FAR_RISE0), "far_rise", "the far bank fills with money (one more doubling)",
            lambda r=rr(): (rumble(fr(T.FAR_RISE1 - T.FAR_RISE0) + 1.4, r, fr(T.FAR_RISE1 - T.FAR_RISE0)), 0.0), -8))
    add(Cue(fr(T.FAR_RISE1), "far_boom", "the big impact on \"Day forty-nine\"", lambda r=rr(): (boom(r, 40, 1.8), 0.0), -9))
    add(Cue(fr(1228), "kaching2", "money sting on \"five hundred sixty-three trillion\"", lambda r=rr(): (kaching(r), 0.0), -13))
    # ------------------------------------------------ luckily / unluckily: a dry deadpan stop (no sting)
    add(Cue(fr(1457), "deadpan", "a single paper flick on the cut to \"Unluckily\"", lambda r=rr(): (flip(r), 0.0), -20))
    # ------------------------------------------------ the snowball
    add(Cue(fr(T.SNOW0), "snow_roll", "the money snowball rolling and growing down the mountain",
            lambda r=rr(): (fades(rumble(fr(T.SNOW1 - T.SNOW0) + 0.3, r, fr(T.SNOW1 - T.SNOW0) * 0.95, 40, 180), 0.05, 0.25), 0.0), -12))
    add(Cue(fr(1600), "whoosh_halves", "whoosh to the two halves", lambda r=rr(): (G.whoosh(0.8, r, 0.35, 300, 2200, 0.9, 0.3, 0.2), 0.35), -16))
    # ------------------------------------------------ 350 years: a slow clock, the tree creaking up
    for k in range(int((T.GROW1 - T.GROW0) / 15)):
        add(Cue(fr(T.GROW0 + 15 * k), "tick", "clock tick (time passing at 10 % a year)", lambda r=rr(), k=k: (tick(r, k % 2 == 0), 0.0), -22, p=0.3, group="ticks"))
    add(Cue(fr(T.GROW0), "tree_grow", "the tree creaking up from a sapling",
            lambda r=rr(): (fades(G.creak(fr(T.GROW1 - T.GROW0), r, 60, 120), 0.3, 0.5), 0.0), -22, p=-0.3))
    # ------------------------------------------------ ending
    add(Cue(fr(1897), "whoosh_gold", "soft whoosh into the golden aerial", lambda r=rr(): (G.whoosh(0.9, r, 0.45, 250, 1800, 0.9, 0.35, 0.15), 0.45), -18))
    add(Cue(fr(1982), "bill_keep", "the bill tucked away (\"keep the dollar\")", lambda r=rr(): (paper(0.25, r, 30), 0.0), -18))
    add(Cue(fr(T.CRANE), "whoosh_crane", "slow whoosh on the crane out", lambda r=rr(): (G.whoosh(1.6, r, 0.9, 200, 1500, 1.0, 0.5, 0.1), 0.9), -20))
    return C


def _crowd(dur, r):
    n = ns(dur)
    out = np.zeros((2, n))
    for v in range(8):
        base, scale = (r.uniform(100, 150), 1.0) if v % 2 else (r.uniform(180, 250), 1.15)
        y = G.babble(dur, r, base, scale, r.uniform(3.6, 4.8), r.uniform(0.5, 0.7), fmax=3400)
        out += pan(lp(y, r.uniform(2400, 3600), 1) * r.uniform(0.3, 0.8), r.uniform(-0.85, 0.85))
    for k in range(5):
        h = G.hurrah(r, r.uniform(110, 240), r.uniform(1.0, 1.2))
        place(out, pan(lp(h, 3200, 1) * r.uniform(0.4, 1.0), r.uniform(-0.8, 0.8)), r.uniform(0.2, dur - 0.9))
    return out


def render(v_ref, on_event=None):
    """v_ref = integrated loudness of the voice stem (stereo). Returns (stereo stem, cue list with measured levels)."""
    C = cues()
    out = np.zeros((2, N))
    send = np.zeros(N)
    for c in C:
        x, anchor = c.gen()
        x = np.asarray(x, float)
        x = pan(x, c.p) if x.ndim == 1 else x
        if c.cut is not None:
            k = ns(c.cut - (c.t - anchor))
            if 0 < k < x.shape[1]:
                x = fades(x[:, :k], 0.0, 0.02)
        tgt = v_ref + c.applied
        cur = momentary_max(x) if c.kind == "event" else integrated(x)
        if np.isfinite(cur):
            x = x * dbg(tgt - cur)
        if c.lpf:
            x = lp(x, c.lpf, 1)
        c.measured = momentary_max(x) - v_ref if c.kind == "event" else integrated(x) - v_ref
        t0 = c.t - anchor
        place(out, x, t0)
        if on_event:
            on_event(c, x, t0)
        if c.send > 0:
            G._place_mono(send, c.send * x.mean(0), t0)
    valley = make_ir(1.1, 77, pre=0.01, hf=1.6, early=[(0.09, 0.45, -0.5), (0.14, 0.3, 0.6), (0.23, 0.2, -0.2)])
    out += 0.55 * convolve_st(send, valley)
    out = hp(out, 25, 2)
    end = ns(T.DUR - 0.12)
    out[:, end:] *= np.linspace(1, 0, N - end)[None, :] ** 2
    return out, C
