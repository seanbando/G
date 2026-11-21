# Chapter 9: The Deal (VO 15:26-16:19). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Creator clips: 75 (marshals escort), 24 (Alice Hawthorne), 45 (Emily Lyons). Photo: ADX Florence. 3D: buried
# explosives markers on the clay mountains. Numbers punch on their words (style sheet: 250 lbs, 6 life sentences).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
AMBER = "#E0A040"

seg(926.63, 929.20, card=[["THE DEAL", "big"]])                                              # "Prosecutors wanted him executed."
seg(929.20, 931.16, card=[["APRIL 2005", "amber"]])                                          # "In April 2005,"
seg(931.16, 933.28, src="75 marshals escort clip.mp4")                                       # "Rudolph made a deal instead."
seg(933.28, 935.82, card=[["PLEADS GUILTY", "type"], ["TO ALL FOUR BOMBINGS", "amber"]])    # "He pleaded guilty to all four bombings,"
seg(935.82, 941.94, src="blender H_caches.mp4")                                              # "to stay off death row he told investigators where he'd buried explosives in the North Carolina woods" (3D)
seg(941.94, 946.48, src="blender H_250.mp4")  # 3D number (build/blender/H_agents_200.py --arg value=250 …)  # "Agents reportedly dug up around 250 pounds of dynamite."
seg(946.48, 952.08, effect="paper-typewriter", ov={"title": "RUDOLPH'S STATEMENT"})          # "He put out a written statement afterward. In it, he said the point of the Olympic bomb was to"
seg(952.08, 957.80, effect="stacked-highlight", ov={"title": "“CONFOUND, ANGER|AND EMBARRASS”", "backgroundImage": "loc-olympic-park-1996.png", "accent": AMBER})  # "'confound, anger and embarrass' the government… That was his reason."
seg(957.80, 961.38, src="24 hawthorne clip.mp4", tag=["ALICE HAWTHORNE", "Killed July 27, 1996"])  # "One woman dead in a park full of people at a concert."
seg(961.38, 964.34, card=[["BIRMINGHAM", "type"], ["+ ATLANTA", "type"]])                    # "Across the Birmingham and Atlanta cases, he got"
seg(964.34, 970.20, src="blender H_six.mp4")  # 3D number: "six consecutive life sentences, plus another hundred and twenty years. No parole."
seg(970.20, 975.06, src="79 adx florence.jpg", motion="push_in", tag=["ADX FLORENCE", "Federal supermax, Colorado"])  # "He's at the federal supermax in Florence, Colorado, and he isn't coming out."
seg(975.06, 979.92, src="45 lyons clip.mp4", tag=["EMILY LYONS", "Nurse, Birmingham"])      # "Emily Lyons, the nurse from Birmingham, was in court for it."

MUSIC = [dict(start=926.6, end=979.92, bed="bed-C.mp3", gain=-18)]
SFX = [(926.7, "sfx-typewriter-keys-short.mp3", -15), (926.7, "sfx-typewriter-ding.mp3", -16), (929.3, "sfx-typewriter-keys-short.mp3", -16),
       (933.3, "sfx-typewriter-keys-medium.mp3", -16), (933.9, "sfx-stamp-thud.mp3", -13), (935.9, "sfx-shovel-dirt.mp3", -15),
       (944.2, "sfx-low-hit.mp3", -13), (946.5, "sfx-typewriter-keys-long.mp3", -16), (952.1, "sfx-pen-scribble.mp3", -16),
       (961.4, "sfx-typewriter-keys-short.mp3", -16), (964.8, "sfx-cell-door.mp3", -12), (969.0, "sfx-typewriter-keys-short.mp3", -16)]
CUES = """926.63 whip right
944.24 punch
964.84 punch
964.85 shake 0.25
"""
