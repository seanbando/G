# Chapter 4: Birmingham (7:48-9:09 on the VO clock). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Real material: WYFF clinic windows, Forgotten History aerial of the clinic (raw shot only), Sanderson photo, creator's
# Lyons clip. No victims on stretchers (both sources have them: left out). Creator clips E (walking the wrong way),
# F (the plate), L10 (first 3 s only), 50 (young Rudolph).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
AMBER = "#E0A040"

seg(468.26, 471.35, card=[["BIRMINGHAM", "big"]])                                   # "January 29th, 1998."
seg(471.35, 475.75, effect="clock-badge", ov={"title": "7:30 AM", "subtitle": "JANUARY 29, 1998  ·  BIRMINGHAM, ALABAMA", "backgroundImage": "loc-birmingham-clinic.png", "accent": AMBER})  # "About 7:30 a.m., outside the New Woman All Women Health Care clinic"
seg(475.75, 478.05, src="L10 birmingham.mp4")                                      # "in Birmingham, Alabama" (first ~2.3 s: smoke later)
seg(478.05, 483.43, src="Officer Robert Sanderson.jpg", motion="push_in", tag=["ROBERT SANDERSON", "Birmingham police officer"])  # "Robert Sanderson is a Birmingham police officer…"
seg(483.43, 488.81, src="loc-birmingham-clinic.png", motion="push_in", fx=("flicker",))  # "According to accounts… noticed something by the entrance"
seg(488.81, 491.43, src="wyff birmingham clinic windows 1998.mp4")                   # "He's killed." (real: the blown-out entrance)
seg(491.43, 496.85, src="45 lyons clip.mp4", tag=["EMILY LYONS", "Nurse at the clinic"])  # "A nurse, Emily Lyons… lost an eye… years of surgeries"
seg(496.85, 500.83, effect="stacked-highlight", ov={"title": "SET OFF BY|REMOTE CONTROL", "backgroundImage": "loc-birmingham-clinic.png", "accent": AMBER})  # "This bomb was set off by remote control"
seg(500.83, 502.49, src="fh birmingham clinic aerial 1998.mp4")                     # "whoever did it was close enough to watch"
seg(502.49, 506.75, card=[["SOMETHING THAT HADN'T HAPPENED", "type"], ["AT ANY OTHER SCENE", "amber"]])  # "And then something happens that hadn't happened at any of the other scenes."
seg(506.75, 510.95, card=[["PEOPLE RUN TOWARD IT", "type"], ["OR THEY FREEZE", "amber"]])  # "When a bomb goes off, people run toward it, or they freeze."
seg(510.95, 514.37, src="char-student.png", motion="push_in")                       # "A college student nearby noticed one guy doing neither."
seg(514.37, 520.01, src="E clip.mp4")                                               # "He was walking away from it. Not fast. Just strolling off…"
seg(520.01, 522.49, src="E clip.mp4", **{"in": 5.6})                                # "That bugged the student enough to follow him."
seg(522.49, 525.41, card=[["A SECOND WITNESS", "type"]])                            # "Another witness got involved, saw the man climb into"
seg(525.41, 529.23, src="F clip.mp4")                                               # "a gray Nissan pickup, and wrote down the license plate"
seg(529.23, 533.15, effect="stacked-highlight", ov={"title": "THE WHOLE STORY|IN MINIATURE", "backgroundImage": "F. The plate.png", "accent": AMBER})  # "I want to point that out… the whole story in miniature"
seg(533.15, 537.51, effect="case-board", ov={"images": ["loc-olympic-park-1996.png", "loc-sandy-springs.png", "loc-otherside-lounge.png", "30a investigators arrive at jewell apartment 1996-07-30.jpg", "Centennial Park Bomb Map.jpg", "Replica of Centennial Bombing Backpack.jpg"]})  # "Two years of profiles, task forces and FBI theories"
seg(537.51, 539.95, card=[["AND THE CASE BREAKS", "amber"]])                       # "and the case breaks because somebody noticed"
seg(539.95, 541.43, src="E clip.mp4", **{"in": 2.0})                                # "a man walking the wrong way"
seg(541.43, 542.73, src="F clip.mp4", **{"in": 4.0})                                # "and grabbed a pen."
seg(542.73, 547.01, card=[["THE PICKUP IS REGISTERED TO", "type"], ["A 31-YEAR-OLD FROM WESTERN NC", "amber"]])  # "The truck comes back to a 31-year-old from western North Carolina."
seg(547.01, 549.76, src="50 rudolph young clip.mp4", tag=["ERIC ROBERT RUDOLPH", "31, western North Carolina"])  # "Eric Robert Rudolph."

MUSIC = [dict(start=468.2, end=503.0, bed="bed-A.mp3", gain=-18), dict(start=502.4, end=549.76, bed="bed-B.mp3", gain=-19)]
SFX = [(468.3, "sfx-typewriter-keys-short.mp3", -15), (468.3, "sfx-typewriter-ding.mp3", -16), (471.4, "sfx-clock-tick.mp3", -12),
       (478.1, "sfx-paper-slide.mp3", -16), (488.85, "sfx-low-hit.mp3", -13), (491.5, "sfx-paper-slide.mp3", -17),
       (496.9, "sfx-pen-scribble.mp3", -16), (502.5, "sfx-typewriter-keys-medium.mp3", -16), (506.8, "sfx-typewriter-keys-medium.mp3", -16),
       (514.4, "sfx-gravel-footsteps.mp3", -17), (522.5, "sfx-typewriter-keys-short.mp3", -16), (525.5, "sfx-pen-scribble.mp3", -14),
       (529.3, "sfx-pen-scribble.mp3", -17), (533.2, "sfx-whoosh.mp3", -16), (537.6, "sfx-typewriter-keys-short.mp3", -15),
       (541.5, "sfx-pen-tick.mp3", -13), (542.8, "sfx-typewriter-keys-medium.mp3", -16), (547.0, "sfx-boom-hit.mp3", -10)]
CUES = """468.26 whip right
547.01 zoomthru
547.02 shake 0.25
"""
