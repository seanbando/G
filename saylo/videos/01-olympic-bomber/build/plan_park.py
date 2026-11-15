# Chapter 1: The Park (1:51–4:00). Template effects via SAYLO_EFFECTS.
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
seg(111.06, 114.50, effect="chapter-type", ov={"title": "The Park", "background": "#0B0D10", "foreground": "#F3F1E9"})
seg(114.50, 119.35, effect="date-center", ov={"title": "JULY 27, 1996", "subtitle": "CENTENNIAL OLYMPIC PARK  ·  ATLANTA", "backgroundImage": "loc-olympic-park-1996.png", "foreground": "#F3F1E9"})
seg(119.35, 123.00, src="L03 olympic park.mp4")
seg(123.00, 126.50, src="14 park aerial clip.mp4")
seg(126.50, 128.95, src="M clip.mp4", **{"in": 0.0})
seg(128.95, 132.37, src="L03 olympic park.mp4", **{"in": 5.5})
seg(132.37, 135.32, src="17 tower.jpg", motion="pan_right")
seg(135.32, 141.00, src="16 jewell ajc clip.mp4", tag=["RICHARD JEWELL", "Security guard, age 33"])
seg(141.00, 148.72, effect="film-window", ov={"images": ["16b jewell talking to reporters 1996-07-28.jpg"], "background": "#0B0D10"})
seg(148.72, 154.50, src="B clip.mp4")
seg(154.50, 161.12, src="18 backpack replica clip.mp4")
seg(161.12, 166.00, src="C clip.mp4")
seg(166.00, 170.13, src="L03 olympic park.mp4", **{"in": 7.0})
seg(170.13, 175.00, effect="clock-badge", ov={"title": "12:58 AM", "subtitle": "JULY 27, 1996", "backgroundImage": "loc-payphone-1996.png", "accent": "#E0A040"})
seg(175.00, 181.00, src="D clip.mp4")
seg(181.00, 185.50, effect="map-callout", ov={"title": "PAYPHONE  ·  A FEW BLOCKS AWAY", "images": ["Centennial Park Bomb Map.jpg"], "accent": "#E0A040"})
seg(185.50, 190.49, card=[["THE PARK'S ADDRESS", "type"], ["WASN'T IN THE 911 SYSTEM", "amber"]])
seg(190.49, 194.54, card=[["WARNING: 30 MINUTES", "type"], ["BLAST: ~1:20 AM", "amber"]])
seg(194.54, 200.00, src="23 bomb scene clip.mp4")
seg(200.00, 203.00, src="23b debris after the bombing 1996-07-28.jpg", motion="push_in")
seg(203.00, 210.77, src="24 hawthorne clip.mp4", tag=["ALICE HAWTHORNE", "Albany, Georgia, age 44"])
seg(210.77, 216.00, src="25 uzunyol clip.mp4", tag=["MELIH UZUNYOL", "Turkish TV cameraman"])
seg(216.00, 222.12, src="23c investigators sort debris 1996-07-28.jpg", motion="pan_left")
seg(222.12, 225.26, src="26c jewell on cnn as the hero.mp4")
seg(225.26, 233.11, effect="news-image", ov={"title": "GUARD'S ALERTNESS IN PARK MAKES HIM AN UNEXPECTED HERO", "subtitle": "JULY 28, 1996", "label": "GANNETT NEWS SERVICE", "images": ["16c jewell talking to reporters 1996-07-28.jpg"], "accent": "#E0A040", "background": "#0B0D10"})
seg(233.11, 238.30, src="27b newsstand - fbi has a suspect.mp4")
seg(238.30, 240.01, src="27c anchor - hero may be a villain.mp4")

MUSIC = [dict(start=111.0, end=196.0, bed="bed-B.mp3", gain=-19), dict(start=194.5, end=224.0, bed="bed-C.mp3", gain=-17),
         dict(start=222.0, end=240.01, bed="bed-B.mp3", gain=-19)]
SFX = [(111.1, "sfx-typewriter-keys-medium.mp3", -15), (111.1, "sfx-typewriter-ding.mp3", -16),
       (119.4, "sfx-crowd-concert.mp3", -22), (127.0, "sfx-crowd-concert.mp3", -22),
       (148.8, "sfx-low-hit.mp3", -16), (170.2, "sfx-clock-tick.mp3", -12), (175.1, "sfx-payphone-pickup.mp3", -14),
       (181.0, "sfx-whoosh.mp3", -16), (185.6, "sfx-typewriter-keys-medium.mp3", -15), (190.5, "sfx-clock-ticking.mp3", -14),
       (194.5, "sfx-boom-hit.mp3", -8), (222.1, "sfx-whoosh.mp3", -16), (225.3, "sfx-paper-slide.mp3", -14), (233.1, "sfx-paper-slide.mp3", -14)]
CUES = """111.06 whip right
119.35 whip left
170.13 whip right
194.54 flash
194.55 shake 0.3
222.12 whip right
233.11 zoomthru
"""
