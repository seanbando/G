# Cold open shot plan (0:00–1:52). Times from vo-timings.tsv / edit-cues.csv.
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
seg(0.00, 4.57, card=[["MAY 31, 2003", "type"], ["3:30 AM", "amber"], ["MURPHY, NORTH CAROLINA", "type"]], bg="loc-murphy-street.png")
seg(4.57, 8.30, src="K clip.mp4")
seg(8.30, 11.89, src="H clip.mp4", **{"in": 2.0})
seg(11.89, 16.83, src="A clip.mp4", **{"in": 0.0})
seg(16.83, 21.20, src="04 postell clip.mp4", tag=["JEFF POSTELL", "Murphy police officer, age 21"])
seg(21.20, 25.65, src="05 save a lot clip.mp4", crop="1220:686:300:150")
seg(25.65, 30.40, src="A clip.mp4", **{"in": 3.0})
seg(30.40, 35.72, src="I clip.mp4")
seg(35.72, 41.95, card=[['"JERRY WILSON"', "type"], ["HOMELESS", "type"], ["FROM OHIO", "type"]])
seg(41.95, 45.65, src="L02 savealot backlot.mp4")
seg(45.65, 50.39, src="A clip.mp4", **{"in": 4.5})
seg(50.39, 53.87, src="07 wanted poster clip.mp4")
seg(53.87, 58.26, src="J clip.mp4")
seg(58.26, 63.56, number=dict(value=1000000, prefix="$", label="REWARD  \u00b7  200+ FEDERAL AGENTS", land=2.6))
seg(63.56, 68.00, src="10 rudolph clip.mp4", tag=["ERIC RUDOLPH", "The Olympic Park bomber"])
seg(68.00, 72.50, src="23e live tv - word of an explosion.mp4", **{"in": 0.5})
seg(72.50, 74.59, src="30b media scrum 1996.mp4", **{"in": 1.0})
seg(74.59, 78.10, card=[["WHY WAS HE SO", "big"], ["HARD TO CATCH?", "big"]])
seg(78.10, 86.00, card=[["1 · THE WRONG MAN", "type"], ["88 DAYS", "amber"]])
seg(86.00, 89.00, src="26c jewell on cnn as the hero.mp4")
seg(89.00, 91.80, src="26a jewell hugged by police officer 1996-07-28.jpg", motion="pan_left")
seg(91.80, 95.79, card=[["2 · NO NAME", "type"], ["18 MONTHS", "amber"]])
seg(95.79, 100.56, card=[["3 · BUILT FOR HIDING", "type"], ["5 YEARS", "amber"]], bg="loc-nantahala.jpg")
seg(100.56, 106.50, card=[["COURT RECORDS · FBI CASE HISTORY", "small"], ["JUSTICE DEPARTMENT REVIEW", "small"], ["NEWS REPORTING FROM THE TIME", "small"]])
seg(106.50, 111.06, src="30g news crews outside during search 1996-07-31.jpg", motion="pan_right")

MUSIC = [dict(start=0, end=74.6, bed="bed-A.mp3", gain=-17), dict(start=74.0, end=112.46, bed="bed-B.mp3", gain=-19)]
SFX = [
    (0.15, "sfx-typewriter-keys-long.mp3", -16), (0.1, "sfx-night-forest.mp3", -24),
    (11.9, "sfx-car-idle-gravel.mp3", -18), (30.5, "sfx-gravel-footsteps.mp3", -14),
    (35.8, "sfx-typewriter-keys-medium.mp3", -16), (41.4, "sfx-flashlight-click.mp3", -10),
    (50.4, "sfx-paper-slide.mp3", -14), (53.7, "sfx-helicopter-distant.mp3", -16),
    (58.3, "sfx-typewriter-keys-medium.mp3", -16), (60.5, "sfx-riser.mp3", -14), (63.5, "sfx-boom-hit.mp3", -10),
    (74.6, "sfx-typewriter-keys-medium.mp3", -16), (78.2, "sfx-typewriter-keys-medium.mp3", -16),
    (86.0, "sfx-whoosh.mp3", -16), (91.9, "sfx-typewriter-keys-short.mp3", -16),
    (95.9, "sfx-typewriter-keys-medium.mp3", -16), (100.6, "sfx-typewriter-keys-long.mp3", -16),
]
