# Chapter 7: Five Years (VO 12:37-14:09). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Creator clips on their lines: L06 (hidden camp above Murphy), H (living rough), I (night raid: ONLY under "go through the
# trash"). Real: WLOS 2003 perp walk; Postell's bite (WLOS). 3D: camps on the clay slopes; callbacks to the Murphy
# street and back-lot dioramas.
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
AMBER = "#E0A040"

seg(757.35, 758.40, card=[["FIVE YEARS", "big"]])                                                # "So how do you"
seg(758.40, 760.30, src="loc-hidden-camp.png", motion="push_in", fx=("fog",))                    # "live out there for five years?"
seg(760.30, 768.16, card=[["SOURCE:", "type"], ["RUDOLPH'S OWN ACCOUNT", "amber"], ["+ WHAT AGENTS DUG UP", "type"]])  # "Most of what we know comes from Rudolph himself… and what agents later dug up"
seg(768.16, 774.96, effect="stacked-highlight", ov={"title": "HE HAS EVERY REASON|TO TELL IT THIS WAY", "backgroundImage": "H. Living rough.jpg", "accent": AMBER})  # "Keep that in your head… a tough guy surviving on his own"
seg(774.96, 779.94, src="blender H_camps.mp4")                                                   # "According to those accounts, he moved between hidden camps on the slopes" (3D)
seg(779.94, 782.24, src="L06 hidden camp.mp4")                                                   # "some of them close enough to look down on Murphy."
seg(782.24, 785.42, src="H clip.mp4")                                                            # "He reportedly ate acorns. Salamanders."
seg(785.42, 789.58, src="H clip.mp4", **{"in": 3.2})                                             # "Whatever he could hunt… people's gardens."
seg(789.58, 794.80, card=[["STOLEN GRAIN", "type"], ["BURIED BARRELS OF FOOD", "amber"], ["AGENTS LATER FOUND THEM", "type"]])  # "He stole grain and buried barrels… agents later found them."
# BITE 794.80: Postell (WLOS), "There's no telling how many times we've been right here, right on top of him and not know."
seg(794.80, 799.96, src="66 swecker clip.mp4", tag=["CHRIS SWECKER", "Ran the FBI's Charlotte office"])  # "Chris Swecker, who ran the FBI's Charlotte office, also suspected"
seg(799.96, 801.92, card=[["EMPTY VACATION CABINS", "type"], ["SUSPECTED", "amber"]])            # "he slipped into empty vacation cabins."
seg(801.92, 805.14, src="blender H_murphy_street.mp4")                                           # "And at night, when the town was asleep, he'd come down"
seg(805.14, 806.72, src="I clip.mp4")                                                            # "and go through the trash." (I clip: only here)
seg(806.72, 810.06, src="blender H_savealot.mp4")                                                # "Which is exactly what he was doing behind the Save-A-Lot." (callback)
seg(810.06, 812.00, card=[["HERE'S WHERE IT GETS", "type"], ["MURKY", "amber"]])                 # "Here's where it gets murky, though."
seg(812.00, 817.44, src="04b postell clip.mp4", **{"in": 1.5})                                   # "When Postell found him, he didn't look like a guy who'd been eating salamanders"
seg(817.44, 820.48, src="wlos rudolph perp walk 2003.mp4")                                       # "Clean-shaven, a recent haircut, fit." (real 2003)
seg(820.48, 824.96, card=[["REPORTERS ASK:", "type"], ["WAS SOMEONE LOCAL HELPING HIM?", "amber"]])  # "Reporters started asking right away whether somebody local had been helping him."
seg(824.96, 828.14, effect="stacked-highlight", ov={"title": "A HAIRCUT|ISN'T AN ACCOMPLICE", "backgroundImage": "loc-murphy-street.png", "accent": AMBER})  # "Maybe. But a haircut isn't an accomplice."
seg(828.14, 836.06, card=[["BURIED BARRELS · STOLEN GRAIN", "type"], ["DUMPSTERS · EMPTY CABINS?", "amber"], ["OTHER WAYS TO EXPLAIN IT", "type"]])  # "Between the buried barrels… other ways to explain it."
seg(836.06, 841.86, card=[["RUDOLPH: “I DID IT ALONE”", "type"], ["CHARGED WITH HELPING HIM: NOBODY", "amber"]])  # "Rudolph says no. He did it alone. Nobody was ever charged with helping him."
seg(841.86, 849.12, src="L06 hidden camp.mp4", **{"in": 2.5})                                    # "Me? I'm not sure. I'd be careful with anybody who tells you they know for certain"

MUSIC = [dict(start=757.3, end=849.12, bed="bed-D.mp3", gain=-18)]
SFX = [(757.4, "sfx-typewriter-keys-short.mp3", -15), (757.4, "sfx-typewriter-ding.mp3", -16), (758.5, "sfx-night-forest.mp3", -20),
       (760.4, "sfx-typewriter-keys-long.mp3", -16), (768.2, "sfx-pen-scribble.mp3", -16), (775.0, "sfx-whoosh.mp3", -17),
       (782.3, "sfx-wind-gust.mp3", -19), (789.6, "sfx-shovel-dirt.mp3", -15), (789.7, "sfx-typewriter-keys-medium.mp3", -17),
       (794.9, "sfx-paper-slide.mp3", -17), (800.0, "sfx-typewriter-keys-short.mp3", -16), (802.0, "sfx-dogs-distant.mp3", -22),
       (805.2, "sfx-flashlight-click.mp3", -12), (810.1, "sfx-typewriter-keys-short.mp3", -16), (820.5, "sfx-typewriter-keys-medium.mp3", -16),
       (825.0, "sfx-pen-scribble.mp3", -16), (828.2, "sfx-typewriter-keys-long.mp3", -16), (836.1, "sfx-typewriter-keys-medium.mp3", -16),
       (836.9, "sfx-stamp-thud.mp3", -13)]
CUES = """757.35 whip right
"""
BITES = [dict(at=794.80, src="bite wlos postell right on top of him.mp4", dur=5.95)]
