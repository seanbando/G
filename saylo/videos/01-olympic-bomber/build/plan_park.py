# Chapter 1: The Park (1:51–4:00). Template effects via SAYLO_EFFECTS.
# Re-cut Nov 15, 2026 on word timestamps (vo-words.json): each cut starts on the word in its comment.
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
seg(111.06, 112.56, effect="chapter-type", ov={"title": "The Park", "background": "#0B0D10", "foreground": "#F3F1E9"})
seg(112.56, 119.98, effect="date-center", ov={"title": "JULY 27, 1996", "subtitle": "CENTENNIAL OLYMPIC PARK  ·  ATLANTA", "backgroundImage": "loc-olympic-park-1996.png", "foreground": "#F3F1E9"})  # "Saturday, July 27th, 1996"
seg(119.98, 123.74, src="L03 olympic park.mp4")                                  # "Centennial Olympic Park was where you went"
seg(123.74, 126.24, src="M clip.mp4", **{"in": 0.0})                             # "A little after midnight… thousands of people" (first 2.5 s only)
seg(126.24, 129.10, src="14 park aerial clip.mp4")                               # "packed in front of a stage"
seg(129.10, 131.78, src="L03 olympic park.mp4", **{"in": 5.5})                   # "Jack Mack and the Heart Attack was playing"
seg(131.78, 136.08, src="17 tower.jpg", motion="pan_right")                      # "Working security near the big sound and light tower"
seg(136.08, 141.00, src="26b jewell near park after bombing 1996-07-28.jpg", motion="push_in", tag=["RICHARD JEWELL", "Security guard, age 33"])  # "Richard Jewell"
seg(141.00, 145.74, effect="film-window", ov={"images": ["16b jewell talking to reporters 1996-07-28.jpg"], "background": "#0B0D10"})  # "Former sheriff's deputy… a job"
seg(145.74, 148.50, card=[["JULY 27, 1996", "type"], ["SHORTLY BEFORE 1 AM", "amber"]])  # "Shortly before one in the morning"
seg(148.50, 152.58, src="B clip.mp4")                                            # "a green military-style backpack under a bench"
seg(152.58, 155.78, src="18 backpack replica clip.mp4")                          # "Nobody's sitting there…"
seg(155.78, 161.52, card=[["JEWELL ALERTS GBI OFFICERS", "type"], ["BOMB SQUAD CALLED", "amber"]])  # "Jewell points it out… calls the bomb squad"
seg(161.52, 165.78, src="C clip.mp4")                                            # "Jewell starts helping push people back"
seg(165.78, 170.16, src="L03 olympic park.mp4", **{"in": 7.0})                   # "you try telling a crowd at 1 a.m."
seg(170.16, 175.64, effect="clock-badge", ov={"title": "12:58 AM", "subtitle": "JULY 27, 1996", "backgroundImage": "loc-payphone-1996.png", "accent": "#E0A040"})  # "At 12:58… a payphone"
seg(175.64, 181.32, src="D clip.mp4")                                            # "A man, very calm, says there's a bomb"
seg(181.32, 186.00, effect="map-callout", ov={"title": "CENTENNIAL OLYMPIC PARK", "images": ["Centennial Park Bomb Map.jpg"], "accent": "#E0A040"})  # "According to later reporting… routing the warning"
seg(186.00, 190.52, card=[["THE PARK'S ADDRESS", "type"], ["WASN'T IN THE 911 SYSTEM", "amber"]])  # "the park's address wasn't in her system"
seg(190.52, 194.60, card=[["WARNING: 30 MINUTES", "type"], ["BLAST: ~1:20 AM", "amber"]])  # "He said 30 minutes. It went off at about 1:20."
seg(194.60, 197.46, src="23e live tv - word of an explosion.mp4", **{"in": 0.3})  # "Three pipe bombs, packed with nails"
seg(197.46, 204.26, src="24 hawthorne clip.mp4", tag=["ALICE HAWTHORNE", "Albany, Georgia, age 44"])  # "Alice Hawthorne, 44, from Albany"
seg(204.26, 206.80, card=[["FALLON HAWTHORNE, 14", "type"], ["INJURED", "amber"]])  # "her 14-year-old daughter, Fallon"
seg(206.80, 211.04, card=[["MORE THAN 100", "amber"], ["OTHERS INJURED", "type"]])  # "Over a hundred other people were injured"
seg(211.04, 215.54, src="25 uzunyol clip.mp4", tag=["MELIH UZUNYOL", "Turkish TV cameraman"])  # "Melih Uzunyol"
seg(215.54, 222.16, src="23c investigators sort debris 1996-07-28.jpg", motion="pan_left")  # "Investigators said afterward…"
seg(222.16, 226.08, effect="news-image", ov={"title": "GUARD'S ALERTNESS IN PARK MAKES HIM AN UNEXPECTED HERO", "subtitle": "JULY 28, 1996", "label": "GANNETT NEWS SERVICE", "images": ["16c jewell talking to reporters 1996-07-28.jpg"], "accent": "#E0A040", "background": "#0B0D10"})  # "For three days, Richard Jewell was a hero"
seg(226.08, 227.94, src="26c jewell on cnn as the hero.mp4")                    # "He went on the Today show"
seg(227.94, 233.94, src="27b newsstand - fbi has a suspect.mp4")                # "July 30th… a special edition"
seg(233.94, 240.01, src="27b2 ajc headline close.mp4", **{"in": 0.5})           # "the FBI suspected the 'hero' guard may have planted the bomb" (the real AJC headline, word for word)

MUSIC = [dict(start=111.0, end=196.0, bed="bed-B.mp3", gain=-19), dict(start=194.5, end=224.0, bed="bed-C.mp3", gain=-17),
         dict(start=222.0, end=240.01, bed="bed-B.mp3", gain=-19)]
SFX = [(111.1, "sfx-typewriter-keys-medium.mp3", -15), (111.1, "sfx-typewriter-ding.mp3", -16),
       (120.0, "sfx-crowd-concert.mp3", -22), (126.3, "sfx-crowd-concert.mp3", -22),
       (145.8, "sfx-typewriter-keys-short.mp3", -15), (148.6, "sfx-low-hit.mp3", -16), (155.8, "sfx-typewriter-keys-medium.mp3", -15),
       (170.2, "sfx-clock-tick.mp3", -12), (175.7, "sfx-payphone-pickup.mp3", -14),
       (181.3, "sfx-whoosh.mp3", -16), (186.0, "sfx-typewriter-keys-medium.mp3", -15), (190.5, "sfx-clock-ticking.mp3", -14),
       (194.6, "sfx-boom-hit.mp3", -8), (204.3, "sfx-typewriter-keys-short.mp3", -16), (206.8, "sfx-typewriter-keys-short.mp3", -16),
       (222.2, "sfx-whoosh.mp3", -16), (227.9, "sfx-paper-slide.mp3", -14), (233.9, "sfx-paper-slide.mp3", -14)]
CUES = """111.06 whip right
119.98 whip left
170.16 whip right
194.60 flash
194.61 shake 0.3
222.16 whip right
"""
