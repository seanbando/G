# Chapter 3: Same Hands (6:47-7:48). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Real material: AJC archive photos of the Otherside Lounge (credited). No 1997 news video in the creator's downloads.
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
BG = "#0B0D10"; FG = "#F3F1E9"; AMBER = "#E0A040"

seg(407.12, 410.35, card=[["SAME HANDS", "big"]])  # "January 16th, 1997."
seg(410.35, 414.41, effect="date-center", ov={"title": "JANUARY 16, 1997", "subtitle": "SANDY SPRINGS  ·  NORTH OF ATLANTA", "backgroundImage": "loc-sandy-springs.png", "foreground": FG})  # "A bomb goes off at a building in Sandy Springs"
seg(414.41, 417.05, src="L08 sandy springs.mp4")                                   # "where an abortion clinic has its offices"
seg(417.05, 420.63, card=[["POLICE", "type"], ["FIREFIGHTERS", "type"], ["FEDERAL AGENTS", "amber"]], bg="loc-sandy-springs.png")  # "Police show up. Firefighters, federal agents." (note #6: not lights on a door)
seg(420.63, 423.47, number=dict(value=1, prefix="+", suffix=" HOUR", label="RESPONDERS WORKING THE SCENE", land=0.6))  # "About an hour later"
seg(423.47, 426.33, src="wyff sandy springs second blast 1997.mp4", **{"in": 0.6})  # "a second bomb explodes in the parking lot" (real footage: the blast, then the aerial of the smoke)
seg(426.33, 432.73, effect="stacked-highlight", ov={"title": "SET TO HIT|WHOEVER CAME RUNNING", "backgroundImage": "loc-sandy-springs.png", "accent": AMBER})  # "That second one was for them… several responders were hurt"
seg(432.73, 435.17, card=[["FEBRUARY 21, 1997", "type"], ["ATLANTA", "amber"]])   # "A month after that, February 21st"
seg(435.17, 437.33, src="L09 otherside.mp4")                                       # "it's the Otherside Lounge" (first ~2 s only: a flame appears later)
seg(437.33, 439.33, src="41a otherside lounge after the bombing 1997-02-21.jpg", motion="push_in")  # "a lesbian bar in Atlanta"
seg(439.33, 440.85, card=[["5 PEOPLE", "amber"], ["INJURED", "type"]])             # "Five people injured."
seg(440.85, 442.31, src="41g police security at otherside 1997-02-21.jpg", motion="push_in")  # "Police sweep the area"
seg(442.31, 445.63, card=[["A SECOND DEVICE", "type"], ["THE SAME TRICK", "amber"]])  # "find a second device outside, the same trick"
seg(445.63, 449.41, card=[["BOMB SQUAD", "type"], ["DEFUSES IT IN TIME", "amber"]], bg="loc-otherside-lounge.png")  # "the bomb squad takes care of it before it goes off" (note #7: no ambulances)
seg(449.41, 452.73, effect="paper-typewriter", ov={"title": "THE LETTERS"})  # "Letters start showing up at news organizations" (paper-typewriter types ~5 chars/s)
seg(452.73, 455.29, card=[["SIGNED:", "type"], ["“ARMY OF GOD”", "amber"]])  # "signed 'Army of God,' taking credit"
seg(455.29, 462.55, src="blender H_bombings.mp4")  # 3D hero (build/blender/H_three_bombings.py): the three nights as dated prints  # "investigators are pretty sure it's one person. Same construction, same habits, same kind of target."
seg(462.55, 468.26, card=[["SUSPECT:", "type"], ["NO NAME", "amber"]])             # "What they don't have is a name… almost another year"

MUSIC = [dict(start=407.0, end=468.26, bed="bed-A.mp3", gain=-18)]
SFX = [(407.15, "sfx-typewriter-keys-medium.mp3", -15), (407.15, "sfx-typewriter-ding.mp3", -16),
       (410.4, "sfx-typewriter-keys-medium.mp3", -16), (420.7, "sfx-clock-ticking.mp3", -15),
       (423.5, "sfx-boom-hit.mp3", -9), (426.35, "sfx-low-hit.mp3", -13), (426.4, "sfx-pen-scribble.mp3", -17),
       (432.8, "sfx-typewriter-keys-short.mp3", -16), (439.4, "sfx-typewriter-keys-short.mp3", -16),
       (440.9, "sfx-paper-slide.mp3", -16), (442.4, "sfx-typewriter-keys-medium.mp3", -16), (445.7, "sfx-typewriter-keys-medium.mp3", -16), (417.1, "sfx-typewriter-keys-medium.mp3", -16),
       (449.5, "sfx-typewriter-keys-long.mp3", -16), (452.8, "sfx-typewriter-keys-medium.mp3", -16), (452.8, "sfx-stamp-thud.mp3", -13),
       (455.4, "sfx-whoosh.mp3", -16), (462.6, "sfx-typewriter-keys-short.mp3", -16),
       (466.5, "sfx-stamp-thud.mp3", -12)]
CUES = """407.12 whip right
423.47 shake 0.3
426.33 shake 0.2
432.73 whip left
"""
