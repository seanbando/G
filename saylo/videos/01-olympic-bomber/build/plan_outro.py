# Outro (VO 17:43-18:04, + 2 s tail). One question for the comments, the next video, a short subscribe ask.
# The "NEXT: THE D.C. SNIPERS" card is where YouTube's end-screen video element goes: link the channel's existing
# D.C. Snipers video there (it's the creator's first upload).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))

seg(1063.04, 1067.74, card=[["DID HE REALLY MAKE IT", "type"], ["FIVE YEARS ALONE?", "amber"]])  # "So, do you think Eric Rudolph really made it five years out there alone?"
seg(1067.74, 1071.66, src="L06 hidden camp.mp4", **{"in": 1.0})                                  # "Or did somebody in those mountains help him? I go back and forth on it."
seg(1071.66, 1073.78, card=[["TELL ME IN THE COMMENTS", "amber"]])                               # "Tell me what you think in the comments."
seg(1073.78, 1080.80, card=[["NEXT:", "type"], ["THE D.C. SNIPERS", "big"]])                     # "…my video on the D.C. snipers is right here."
seg(1080.80, 1086.20, card=[["SAYLO", "big"], ["SUBSCRIBE FOR MORE", "amber"]])                  # "And subscribe if you want more of these. I've got a long list."

MUSIC = [dict(start=1063.0, end=1086.20, bed="bed-B.mp3", gain=-18, fade=2.5)]
SFX = [(1063.1, "sfx-typewriter-keys-medium.mp3", -16), (1071.7, "sfx-typewriter-keys-short.mp3", -16),
       (1073.8, "sfx-typewriter-keys-short.mp3", -16), (1080.9, "sfx-typewriter-keys-short.mp3", -16)]
CUES = ""
# Dead air before the outro: 2.9 s -> ~1.2 s (after "Then one night, a rookie was.")
TRIMS = [(1060.70, 1062.40)]
