# Chapter 10: What It Actually Was (VO 16:19-17:43). Cut on word timestamps; each cut starts on the word in its comment.
# The silent Jewell hold (style sheet): after "He was 44." the music drops out and his photo holds, no transitions.
# Callbacks use each creator clip on the line it stands for (E student, F pen, Postell, A flashlight, dioramas).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
AMBER = "#E0A040"

seg(979.92, 982.76, card=[["WHAT IT ACTUALLY WAS", "big"]])                                  # "Richard Jewell was never charged with anything,"
seg(982.76, 987.25, src="15b jewell security at park 1996.mp4", **{"in": 0.5})              # "because he never did anything except notice a backpack and get people away from it." (real 1996)
seg(987.25, 990.92, card=[["SUED SEVERAL NEWS OUTLETS", "type"], ["SETTLED WITH SOME", "amber"]])  # "He sued several news outlets and settled with some of them."
seg(990.92, 995.76, src="81 jewell later clip.mp4", tag=["RICHARD JEWELL", "Back in police work, Georgia"])  # "He went back into police work in Georgia…"
seg(995.76, 1000.44, card=[["AUGUST 2007", "type"], ["RICHARD JEWELL DIES AT 44", "amber"]])  # "He died in August 2007. Heart trouble. He was 44."
seg(1000.44, 1005.10, src="Jewell later, in police uniform.jpg", motion="push_in")           # (silent hold)
seg(1005.10, 1008.22, src="75 marshals escort clip.mp4", **{"in": 2.0})                     # "He did live long enough to see Rudolph plead guilty."
seg(1008.22, 1015.06, effect="film-window", ov={"images": ["Richard Jewell, 1996.png"], "background": "#0B0D10"})  # "for the last eleven years… 'the Olympic bomber guy.'"
seg(1015.06, 1020.72, effect="stacked-highlight", ov={"title": "THE SAME MISTAKE|TWICE", "backgroundImage": "loc-nantahala.jpg", "accent": AMBER})  # "What bugs me most is that it's the same mistake twice, pointed in opposite directions."
seg(1020.72, 1025.08, src="36e jewell walks past truck 1996.mp4")                           # "In 1996 the FBI looked at a man who did everything right" (real 1996)
seg(1025.08, 1028.14, card=[["THEY SAW A BOMBER", "type"], ["HE FIT THEIR PROFILE", "amber"]])  # "and saw a bomber, because he fit their profile."
seg(1028.14, 1033.32, src="loc-andrews-1998.jpg", motion="pan_left")                        # "Then for five years, some people in those mountains looked at a man who'd killed two people"
seg(1033.32, 1037.06, card=[["THEY SAW A FOLK HERO", "type"], ["HE FIT A STORY THEY LIKED", "amber"]])  # "and saw a folk hero, because he fit a story they liked."
seg(1037.06, 1040.90, card=[["NOT THE PROFILE", "type"], ["NOT THE REWARD", "amber"]])      # "The profile didn't catch Rudolph, and neither did the reward."
seg(1040.90, 1045.20, src="E clip.mp4", **{"in": 2.0})                                      # "What caught him was a college student who saw a man walking the wrong way,"
seg(1045.20, 1046.76, src="F clip.mp4", **{"in": 4.0})                                      # "a stranger with a pen,"
seg(1046.76, 1049.24, src="04 postell clip.mp4", **{"in": 2.0})                             # "and a kid cop who pulled behind a grocery store"
seg(1049.24, 1051.10, src="blender H_savealot.mp4", **{"in": 1.2})                          # "at 3:30 in the morning."
seg(1051.10, 1053.58, src="blender H_campsite.mp4", **{"in": 0.4})                          # "Everybody knew roughly where he was." (the right mountains, lit)
seg(1053.58, 1057.82, card=[["FOR FIVE YEARS, NOBODY WAS", "type"], ["IN THE RIGHT SPOT AT THE RIGHT MINUTE", "amber"]])  # "For five years, nobody was in the right spot at the right minute."
seg(1057.82, 1063.04, src="A clip.mp4")                                                      # "Then one night, a rookie was."

MUSIC = [dict(start=979.9, end=1000.6, bed="bed-C.mp3", gain=-18), dict(start=1004.6, end=1063.04, bed="bed-D.mp3", gain=-18)]
SILENCE = [[1000.5, 1004.9]]
SFX = [(980.0, "sfx-typewriter-keys-medium.mp3", -15), (980.0, "sfx-typewriter-ding.mp3", -16), (987.6, "sfx-typewriter-keys-medium.mp3", -16),
       (995.8, "sfx-typewriter-keys-medium.mp3", -16), (1015.1, "sfx-pen-scribble.mp3", -16), (1025.1, "sfx-typewriter-keys-medium.mp3", -16),
       (1033.4, "sfx-typewriter-keys-medium.mp3", -16), (1037.1, "sfx-typewriter-keys-short.mp3", -16), (1045.3, "sfx-pen-tick.mp3", -13),
       (1049.3, "sfx-night-forest.mp3", -22), (1053.6, "sfx-typewriter-keys-long.mp3", -16), (1057.9, "sfx-flashlight-click.mp3", -11)]
CUES = """979.92 whip right
"""
# News bite after "…and get people away from it.": Jewell, Oct 28, 1996, "For 88 days, I lived a nightmare."
BITES = [dict(at=987.25, src="bite jewell 88 days a nightmare 1996.mp4", dur=3.5)]
