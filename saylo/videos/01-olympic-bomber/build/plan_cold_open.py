# Cold open shot plan (0:00–1:51). Re-cut Nov 15, 2026 on word timestamps (vo-words.json) per the creator's
# part-1 feedback: every cut starts on the word it illustrates (times = first word of the phrase in the comment).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
seg(0.00, 4.50, card=[["MAY 31, 2003", "type"], ["3:30 AM", "amber"], ["MURPHY, NORTH CAROLINA", "type"]], bg="loc-murphy-street.png")
seg(4.50, 12.36, src="loc-murphy-street.png", motion="push_in", fx=("fog", "flicker"))   # "Murphy, North Carolina… a mountain town" (no L01 clip)
seg(12.36, 17.38, src="K clip.mp4")                                                     # "the occasional patrol car" / "The officer in that car"
seg(17.38, 21.92, src="04 postell clip.mp4", tag=["JEFF POSTELL", "Murphy police officer, age 21"])  # "His name is Jeff Postell"
seg(21.92, 24.28, src="05 save a lot clip.mp4", crop="1220:686:300:150")               # "swings around behind the Save-A-Lot"
seg(24.28, 25.66, src="L02 savealot backlot.mp4")                                       # "with his lights off"
seg(25.66, 30.68, src="A clip.mp4", **{"in": 0.0})                                      # "he spots a man crouched" (flashlight)
seg(30.68, 35.74, src="L clip.mp4")                                                     # "The man bolts, then gives up" (runs, slips, hands up)
seg(35.74, 41.98, card=[['"JERRY WILSON"', "type"], ["HOMELESS", "type"], ["FROM OHIO", "type"]])  # "He says his name is Jerry Wilson"
seg(41.98, 47.02, card=[['"JERRY WILSON"', "type"], ["IT'S A LIE", "amber"]])         # "It's a lie, and a pretty good one."
seg(47.02, 50.10, src="A clip.mp4", **{"in": 4.5})                                      # "the man standing in that parking lot"
seg(50.10, 53.86, src="07 wanted poster clip.mp4")                                      # "Ten Most Wanted"
seg(53.86, 58.28, src="J clip.mp4")                                                     # "Helicopters with heat cameras"
seg(58.28, 63.62, number=dict(value=200, suffix="+", label="FEDERAL AGENTS", land=59.64 - 58.28 + 0.5))  # "At one point… 200 federal agents"
seg(63.62, 67.54, src="10 rudolph clip.mp4", tag=["ERIC RUDOLPH", "The Olympic Park bomber"])  # "His real name was Eric Rudolph"
seg(67.54, 70.14, src="23e live tv - word of an explosion.mp4", **{"in": 0.5})         # "after a bomb went off at the Atlanta Olympics"
seg(70.14, 74.68, src="30b media scrum 1996.mp4", **{"in": 1.0})                       # "the FBI had spent 88 days chasing someone else"
seg(74.68, 81.59, card=[["WHY WAS HE SO", "big"], ["HARD TO CATCH?", "big"]])         # "So why was he so hard to catch?… three"
seg(81.59, 86.20, card=[["1 · THE WRONG MAN", "type"], ["88 DAYS", "amber"]])          # "For the first 88 days… the wrong man"
seg(86.20, 92.06, src="26c jewell on cnn as the hero.mp4")                             # "the guard who'd helped save people"
seg(92.06, 95.79, card=[["2 · NO NAME", "type"], ["18 MONTHS", "amber"]])              # "Then for a year and a half… didn't have a name"
seg(95.79, 99.10, src="L05 nantahala.mp4")                                              # "he walked into a place…"
seg(99.10, 100.62, card=[["3 · BUILT FOR HIDING", "type"], ["5 YEARS", "amber"]], bg="L05 nantahala.mp4")  # "built for hiding"
seg(100.62, 111.06, card=[["COURT RECORDS · FBI CASE HISTORY", "small"], ["JUSTICE DEPARTMENT REVIEW", "small"], ["NEWS REPORTING FROM THE TIME", "small"]])  # "I'm working from court records"

MUSIC = [dict(start=0, end=74.7, bed="bed-A.mp3", gain=-17), dict(start=74.0, end=112.46, bed="bed-B.mp3", gain=-19)]
SFX = [
    (0.15, "sfx-typewriter-keys-long.mp3", -16), (0.1, "sfx-night-forest.mp3", -24),
    (12.4, "sfx-car-idle-gravel.mp3", -18), (30.7, "sfx-gravel-footsteps.mp3", -14),
    (35.8, "sfx-typewriter-keys-medium.mp3", -16), (42.0, "sfx-typewriter-keys-short.mp3", -16),
    (25.7, "sfx-flashlight-click.mp3", -10), (50.1, "sfx-paper-slide.mp3", -14), (53.8, "sfx-helicopter-distant.mp3", -16),
    (58.3, "sfx-typewriter-keys-medium.mp3", -16), (61.6, "sfx-riser.mp3", -14), (63.6, "sfx-boom-hit.mp3", -10),
    (74.7, "sfx-typewriter-keys-medium.mp3", -16), (81.6, "sfx-typewriter-keys-medium.mp3", -16),
    (86.2, "sfx-whoosh.mp3", -16), (92.1, "sfx-typewriter-keys-short.mp3", -16),
    (99.1, "sfx-typewriter-keys-short.mp3", -16), (100.7, "sfx-typewriter-keys-long.mp3", -16),
]
CUES = """59.64 punch
63.62 zoomthru
63.63 shake 0.25
"""
