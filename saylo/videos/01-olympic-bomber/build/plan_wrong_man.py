# Chapter 2: The Wrong Man (4:00-6:47). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Creator, Nov 15: mix in short real 1996 news clips (under 7 s each, on the exact line they show; Retro Report's
# raw archival only, never their interviews or graphics; logos/watermark cropped). 7 clips, ~20 s in this chapter.
# Earlier note: no third-party video here; real material = AJC archive photos (credited),
# everything else is the creator's clips, typed cards and Template Library effects. The Oct 26 letter is typed by us
# (Retro Report's letter shot is their own graphic, not 1996 footage).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
BG = "#0B0D10"; FG = "#F3F1E9"; AMBER = "#E0A040"

seg(240.01, 241.72, card=[["THE WRONG MAN", "big"]])  # "It started with a tip."
seg(241.72, 247.70, card=[["BEFORE THE OLYMPICS", "type"], ["CAMPUS POLICE OFFICER", "type"], ["PIEDMONT COLLEGE · NORTH GEORGIA", "amber"]])  # "Before the Olympicsâ€¦ Piedmont College"
seg(247.70, 254.22, effect="paper-typewriter", ov={"title": "A TIP FROM THE COLLEGE"})  # "After the bombing, people from the college contacted investigators"
seg(254.22, 257.28, effect="stacked-highlight", ov={"title": "THE ‘HERO BOMBER’|THEORY", "backgroundImage": "loc-olympic-park-1996.png", "accent": AMBER})  # "That tip pointed the FBI toward a theory"
seg(257.28, 262.34, src="Replica of Centennial Bombing Backpack.jpg", motion="push_in")  # "someone plants a device so they can find it and be the hero"
seg(262.34, 265.94, src="15b jewell security at park 1996.mp4", **{"in": 0.5})  # "Jewell was an ex-cop who badly wanted to be a cop again"
seg(265.94, 267.72, card=[["LIVED WITH HIS MOTHER", "type"]])                     # "he lived with his mom"
seg(267.72, 270.16, src="26d jewell tv interview 1996.mp4")  # "doing interviews all week"
seg(270.16, 272.56, card=[["SUSPICION", "type"], ["ISN'T EVIDENCE", "amber"]])    # "Suspicion isn't evidence, though."
seg(272.56, 275.14, card=[["PHYSICAL EVIDENCE TYING HIM TO THE BAG:", "type"], ["NONE", "amber"]])  # "Nothing physical tied him to the backpack"
seg(275.14, 277.94, card=[["WITNESSES PUTTING HIM NEAR IT:", "type"], ["NONE", "amber"]])  # "no witness put him near it before he found it"
seg(277.94, 279.44, src="30k media scrum around jewell 1996.mp4", **{"in": 0.5})  # "Didn't matter."
seg(279.44, 283.46, src="L07 apartment media.mp4")                                 # "reporters camped outside his mother's apartment"
seg(283.46, 287.00, src="30l agent carries box out 1996.mp4", **{"in": 0.4})  # "agents carried boxes of their stuff out on live TV"
seg(287.00, 289.46, card=[["LATE-NIGHT TV", "type"], ["JOKES ABOUT JEWELL", "amber"]])  # "Jay Leno was making jokes about him"
seg(289.46, 291.66, src="27d ajc paper on the street 1996.mp4", **{"in": 0.4})  # "It wasn't only the newspaper."
seg(291.66, 298.42, src="Tom Brokaw, NBC, 1996.JPG", motion="push_in", tag=["TOM BROKAW", "NBC News, reportedly"])  # "On NBC, Tom Brokaw reportedly told viewersâ€¦"
seg(298.42, 301.88, card=[["NBC", "type"], ["PAID JEWELL A SETTLEMENT", "amber"]])  # "NBC later paid Jewell a settlement"
seg(301.88, 304.10, card=[["CNN", "type"], ["SETTLED TOO", "amber"]])               # "CNN settled with him too."
seg(304.10, 308.60, src="33b bobi jewell talks to reporters 1996-07-30.jpg", motion="push_in", tag=["BOBI JEWELL", "Richard Jewell's mother"])  # "Jewell's mother, Bobiâ€¦"
seg(308.60, 313.52, card=[["BOBI JEWELL ASKS", "type"], ["PRESIDENT CLINTON", "amber"], ["TO CLEAR HER SON'S NAME", "type"]])  # "She was crying, and she asked President Clinton"
seg(313.52, 319.78, src="30a investigators arrive at jewell apartment 1996-07-30.jpg", motion="pan_right")  # "Picture that, a mother who'd watched agents carry her things out"
seg(319.78, 323.50, src="33b bobi jewell talks to reporters 1996-07-30.jpg", motion="pull_out")  # "now begging the Presidentâ€¦ on camera"
seg(323.50, 329.96, effect="paper-typewriter", ov={"title": "JUSTICE DEPARTMENT REVIEW"})  # "A Justice Department reviewâ€¦ one detail"
seg(329.96, 332.60, src="35b agents bring jewell in 1996.mp4", **{"in": 1.0})  # "They brought Jewell in"
seg(332.60, 334.94, card=[["A TRAINING VIDEO", "big"], ["FOR FIRST RESPONDERS", "type"]])  # "a training video for first responders"
seg(334.94, 341.12, card=[["● REC", "amber"], ["MIRANDA RIGHTS", "big"], ["PRESENTED AS PART OF THE VIDEO", "type"]])  # "Then partway throughâ€¦ Miranda rights"
seg(341.12, 344.56, effect="stacked-highlight", ov={"title": "CRITICIZED BY THE|JUSTICE DEPARTMENT", "backgroundImage": "30a investigators arrive at jewell apartment 1996-07-30.jpg", "accent": AMBER})  # "That's specifically what the Justice Department criticized"
seg(344.56, 348.20, src="loc-payphone-1996.png", motion="push_in", fx=("flicker",))  # "the thing that should've cleared him was sitting there the whole time"
seg(348.20, 349.86, card=[["PHONE RECORDS", "type"], ["JULY 27, 1996", "amber"]])  # "It's in the phone records."
seg(349.86, 355.98, effect="clock-badge", ov={"title": "12:57 AM", "subtitle": "GBI AGENT CALLS THE BOMB SQUAD", "backgroundImage": "loc-olympic-park-1996.png", "accent": AMBER})  # "A GBI agent called the bomb squad at 12:57"
seg(355.98, 360.22, effect="clock-badge", ov={"title": "12:58 AM", "subtitle": "911 CALL FROM A PAYPHONE", "backgroundImage": "loc-payphone-1996.png", "accent": AMBER})  # "One minute later, at 12:58, the bomber called 911"
seg(360.22, 363.45, src="D clip.mp4")                                              # "from a payphone several blocks away"
seg(363.45, 368.53, number=dict(value=1, suffix=" MINUTE", label="BETWEEN THE TWO CALLS", land=0.5))  # "One minute. Jewell's lawyers kept coming back to that"
seg(368.53, 376.11, src="35 park map clip.mp4")                                    # "For Jewell to be the callerâ€¦ point out the bagâ€¦ a payphoneâ€¦ through a packed park"
seg(376.11, 380.33, effect="map-callout", ov={"title": "BENCH TO PAYPHONE: ~60 SEC", "images": ["Centennial Park Bomb Map.jpg"], "accent": AMBER})  # "in about sixty seconds"
seg(380.33, 382.03, card=[["NOT A PROFILE", "type"]])                               # "didn't need a profile"
seg(382.03, 384.41, effect="stacked-highlight", ov={"title": "A CLOCK|AND A MAP", "backgroundImage": "Centennial Park Bomb Map.jpg", "accent": AMBER})  # "It needed a clock and a map."
seg(384.41, 389.03, card=[["OCTOBER 26, 1996", "type"], ["DAY 88", "amber"]])     # "On October 26th, 1996, 88 days in"
seg(389.03, 394.23, effect="paper-typewriter", ov={"title": "NOT CONSIDERED A TARGET"})  # "the U.S. Attorney's office sent his lawyers a letterâ€¦ no longer a target"
seg(394.23, 399.00, src="37 reno clip.mp4", tag=["JANET RENO", "U.S. Attorney General"])  # "Attorney General Janet Reno later saidâ€¦ sorry about the leak"
# BITE 399.00: Jewell's Oct 28, 1996 press conference, "the FBI trampled on my rights as a citizen"
seg(399.00, 403.99, src="36e jewell walks past truck 1996.mp4")  # "That's three monthsâ€¦ on the wrong man"
seg(403.99, 407.12, src="loc-sandy-springs.png", motion="push_in", fx=("fog", "flicker"))  # "And the real bomber wasn't finished."

MUSIC = [dict(start=240.0, end=346.0, bed="bed-B.mp3", gain=-19), dict(start=344.5, end=386.0, bed="bed-C.mp3", gain=-18),
         dict(start=384.4, end=407.12, bed="bed-B.mp3", gain=-19)]
SFX = [(240.05, "sfx-typewriter-keys-medium.mp3", -15), (240.05, "sfx-typewriter-ding.mp3", -16),
       (241.8, "sfx-typewriter-keys-medium.mp3", -16), (247.8, "sfx-typewriter-keys-long.mp3", -16),
       (254.3, "sfx-pen-scribble.mp3", -16), (266.0, "sfx-typewriter-keys-short.mp3", -16),
(270.2, "sfx-typewriter-keys-short.mp3", -16),
       (274.2, "sfx-stamp-thud.mp3", -12), (277.0, "sfx-stamp-thud.mp3", -12), (277.95, "sfx-low-hit.mp3", -14),
(287.0, "sfx-typewriter-keys-short.mp3", -16), (291.7, "sfx-paper-slide.mp3", -16),
       (298.5, "sfx-typewriter-keys-short.mp3", -16), (301.9, "sfx-typewriter-keys-short.mp3", -16), (304.1, "sfx-camera-shutter.mp3", -18),
       (308.7, "sfx-typewriter-keys-medium.mp3", -16), (323.6, "sfx-typewriter-keys-long.mp3", -16), (332.6, "sfx-typewriter-keys-short.mp3", -16),
       (335.0, "sfx-typewriter-keys-medium.mp3", -16), (341.2, "sfx-pen-scribble.mp3", -16), (348.2, "sfx-typewriter-keys-short.mp3", -16),
       (349.9, "sfx-clock-tick.mp3", -12), (356.0, "sfx-clock-tick.mp3", -12), (360.3, "sfx-payphone-pickup.mp3", -14),
       (363.5, "sfx-clock-ticking.mp3", -15), (368.6, "sfx-whoosh.mp3", -16), (376.2, "sfx-pen-tick.mp3", -14),
       (380.4, "sfx-typewriter-keys-short.mp3", -16), (384.5, "sfx-typewriter-keys-medium.mp3", -16), (389.1, "sfx-typewriter-keys-long.mp3", -16),
       (394.3, "sfx-paper-slide.mp3", -16), (404.0, "sfx-low-hit.mp3", -14)]
CUES = """240.01 whip right
363.45 punch
368.53 whip left
"""
# News bite: narration pauses, the real clip plays with its own sound (see build_part1.py)
BITES = [dict(at=399.00, src="bite jewell fbi trampled my rights 1996.mp4", dur=4.4)]
