# Cold open shot plan (0:00–1:51). Re-cut Nov 15, 2026 on word timestamps (vo-words.json) per the creator's
# part-1 feedback: every cut starts on the word it illustrates (times = first word of the phrase in the comment).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
# Hook re-cut (creator note: first 20 s was the same street + parked car). One shot per phrase, street only from 8.9 s.
seg(0.00, 4.50, card=[["MAY 31, 2003", "type"], ["3:30 AM", "amber"]])                 # "3:30 in the morning. May 31st, 2003."
seg(4.50, 8.90, effect="date-center", ov={"title": "MURPHY, NORTH CAROLINA", "subtitle": "A MOUNTAIN TOWN OF ABOUT 1,600", "backgroundImage": "loc-nantahala.jpg", "foreground": "#F3F1E9"})  # "Murphy, North Carolina, a mountain town of about 1,600 people"
seg(8.90, 11.10, src="blender H_murphy_street.mp4")  # "where, at that hour": 3D clay diorama of Murphy's main street (build/blender/H_diorama_murphy_street.py)
seg(11.10, 14.32, src="K clip.mp4")                                                     # "the only thing moving is the occasional patrol car"
seg(14.32, 17.38, src="04b postell clip.mp4", **{"in": 1.0})                            # "The officer in that car is 21 years old"
seg(17.38, 21.92, src="04 postell clip.mp4", tag=["JEFF POSTELL", "Murphy police officer, age 21"])  # "His name is Jeff Postell"
seg(21.92, 24.28, src="05 save a lot clip.mp4", crop="1220:686:300:150")               # "swings around behind the Save-A-Lot"
seg(24.28, 25.66, src="L02 savealot backlot.mp4")                                       # "with his lights off"
seg(25.66, 30.68, src="A clip.mp4", **{"in": 0.0})                                      # "he spots a man crouched" (flashlight)
seg(30.68, 35.74, src="L clip.mp4")                                                     # "The man bolts, then gives up" (runs, slips, hands up)
seg(35.74, 41.98, card=[['"JERRY WILSON"', "type"], ["HOMELESS", "type"], ["FROM OHIO", "type"]])  # "He says his name is Jerry Wilson"
seg(41.98, 47.02, card=[['"JERRY WILSON"', "type"], ["IT'S A LIE", "amber"]])         # "It's a lie, and a pretty good one."
seg(47.02, 50.10, src="blender H_savealot.mp4")  # "the man standing in that parking lot": 3D clay diorama of the back lot (build/blender/H_diorama_savealot.py)
seg(50.10, 53.86, src="07 wanted poster clip.mp4")                                      # "Ten Most Wanted"
seg(53.86, 56.10, src="wyff helicopter search 1998.mp4")                               # "Helicopters with heat cameras" (real search footage, WYFF)
seg(56.10, 58.28, src="J clip.mp4")                                                     # "had flown over these exact hills looking for him"
seg(58.28, 59.64, src="wyff search team woods 1998.mp4", **{"in": 0.9})                 # "At one point more than" (real search team + dog, WYFF)
seg(59.64, 63.62, src="blender H_agents.mp4")  # 3D hero (build/blender/H_agents_200.py): 200+ lands on "two hundred"  # "200 federal agents"
seg(63.62, 67.54, src="10 rudolph clip.mp4", tag=["ERIC RUDOLPH", "The Olympic Park bomber"])  # "His real name was Eric Rudolph"
# News-footage balance (creator, Nov 15): real footage only where it IS the thing named, short, rest original.
seg(67.54, 70.14, src="ap street after the blast 1996.mp4", **{"in": 1.8})            # "after a bomb went off at the Atlanta Olympics" (real AP footage, that night)
seg(70.14, 74.68, number=dict(value=88, suffix=" DAYS", label="CHASING THE WRONG MAN", land=71.42 - 70.14 + 0.5))  # "the FBI had spent 88 days chasing someone else"
seg(74.68, 81.59, src="blender H_title.mp4")  # 3D hero (build/blender/H_title_three.py): the question, then 3 slabs stack         # "So why was he so hard to catch?… three"
seg(81.59, 86.20, card=[["1 · THE WRONG MAN", "type"], ["88 DAYS", "amber"]])          # "For the first 88 days… the wrong man"
seg(86.20, 92.06, src="C clip.mp4", **{"in": 1.0})                                     # "the guard who'd helped save people that night" (C = clearing the crowd)
seg(92.06, 95.79, card=[["2 · NO NAME", "type"], ["18 MONTHS", "amber"]])              # "Then for a year and a half… didn't have a name"
seg(95.79, 99.10, src="L05 nantahala.mp4")                                              # "he walked into a place…"
seg(99.10, 100.62, card=[["3 · BUILT FOR HIDING", "type"], ["5 YEARS", "amber"]], bg="L05 nantahala.mp4")  # "built for hiding"
seg(100.62, 111.06, card=[["COURT RECORDS · FBI CASE HISTORY", "small"], ["JUSTICE DEPARTMENT REVIEW", "small"], ["NEWS REPORTING FROM THE TIME", "small"]])  # "I'm working from court records"

MUSIC = [dict(start=0, end=74.7, bed="bed-A.mp3", gain=-17), dict(start=74.0, end=112.46, bed="bed-B.mp3", gain=-19)]
SFX = [
    (0.15, "sfx-typewriter-keys-long.mp3", -16), (0.1, "sfx-night-forest.mp3", -24),
    (11.1, "sfx-car-idle-gravel.mp3", -18), (30.7, "sfx-gravel-footsteps.mp3", -14),
    (35.8, "sfx-typewriter-keys-medium.mp3", -16), (42.0, "sfx-typewriter-keys-short.mp3", -16),
    (25.7, "sfx-flashlight-click.mp3", -10), (50.1, "sfx-paper-slide.mp3", -14), (53.8, "sfx-helicopter-distant.mp3", -16),
    (58.3, "sfx-typewriter-keys-medium.mp3", -16), (61.6, "sfx-riser.mp3", -14), (63.6, "sfx-boom-hit.mp3", -10),
    (74.7, "sfx-typewriter-keys-medium.mp3", -16), (81.6, "sfx-typewriter-keys-medium.mp3", -16),
    (86.2, "sfx-whoosh.mp3", -16), (92.1, "sfx-typewriter-keys-short.mp3", -16),
    (99.1, "sfx-typewriter-keys-short.mp3", -16), (100.7, "sfx-typewriter-keys-long.mp3", -16),
]
# Dead air cut out of the narration (creator: "dead spaces"); everything after moves up. Hook pauses 1.35-1.45 s -> ~0.45 s.
TRIMS = [(40.85, 41.75), (44.45, 45.40)]
CUES = """59.64 punch
63.62 zoomthru
63.63 shake 0.25
"""
