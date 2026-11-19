# Picture timeline of the $1 short, mirrored (read-only) from remotion/src/videos/dollar/story.ts + cast.ts so every
# sound lands on its frame. Lock these numbers before the sound is made: any later picture change means a re-run.
import json

FPS = 30
TOTAL = 2070
DUR = TOTAL / FPS            # 69.0 s exactly
fr = lambda f: f / FPS

FLASH = fr(205)
# id: (first frame, end frame, light, scene)
SHOTS = {
    1: (0, 75, "day", "table"), 2: (75, 154, "day", "full"), 3: (154, 209, "day", "summit"), 4: (209, 326, "day", "table"),
    5: (326, 458, "day", "wallet"), 6: (458, 584, "day", "house"), 7: (584, 717, "day", "street"), 8: (717, 817, "day", "hill"),
    9: (817, 882, "day", "rich"), 10: (882, 1150, "day", "half"), 11: (1150, 1292, "day", "full"), 12: (1292, 1362, "golden", "summit"),
    13: (1362, 1527, "day", "table"), 14: (1527, 1604, "day", "snowball"), 15: (1604, 1709, "day", "full"),
    16: (1709, 1897, "day", "slow"), 17: (1897, 1978, "day", "full"), 18: (1978, TOTAL, "golden", "end"),
}
XFADE = {12: 8, 13: 8, 16: 8, 17: 8}
# hard cuts inside shots (camera keys with cut: true) and the shot changes: a soft whoosh lives on the big reframes
CUTS_IN_SHOT = [245, 422, 657, 1226, 1457, 1799, 2020]
# story events (frames)
DOUBLINGS = [30 + 5 * k for k in range(9)]          # bills on the table double every 5 f from "doubling" (f 30..70)
HILL_RISE = 717                                       # the money hill heaves up (kick)
FAR_RISE0, FAR_RISE1 = 1152, 1190                     # the far bank fills: "one more doubling" -> "Day forty-nine" (kick)
SNOW0, SNOW1 = 1529, 1604                             # the money snowball rolls
GROW0, GROW1 = 1722, 1872                             # 350 years: tree + beard grow
RICH_SHOCK = 832                                      # the richest person's face drops
CRANE = 2020                                          # final crane out


def shot_t(i):
    a, b = SHOTS[i][:2]
    return fr(a), fr(b)


def words(path):
    return json.load(open(path, encoding="utf-8"))
