# Chapter 6: The Hunt (VO 10:08-12:37). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Real material: WYFF 1998 search footage, reward notice, task force press conference, a searcher's bite; FBI poster;
# Nordmann photo; creator's L11, J, L05, G, Swecker clips. 3D: Andrews pin + search grid on the clay mountains.
# Daniel Rudolph: text only, no images of the act (shot list rule).
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))

seg(608.06, 609.37, card=[["THE HUNT", "big"]])                                              # "May 1998,"
seg(609.37, 611.21, card=[["MAY 1998", "amber"]])                                            # "the FBI puts him on the"
seg(611.21, 613.07, src="Eric Rudolph, FBI Ten Most Wanted poster.png", motion="push_in")    # "Ten Most Wanted list."
seg(613.07, 614.79, src="wyff reward one million 1998.mp4")                                  # "One million dollars."
seg(614.79, 621.25, src="wyff task force press conference 1998.mp4")                         # "He's charged for Birmingham first, and later that year for the Atlanta bombings too"
seg(621.25, 626.39, src="blender H_andrews.mp4")                                             # "The task force sets up in Andrews… about 15 miles from Murphy." (3D)
seg(626.39, 631.29, src="L11 andrews.mp4")                                                   # "Imagine living there in 1998, you go to the gas station"
seg(631.29, 636.21, card=[["FBI WINDBREAKERS", "type"], ["BUYING COFFEE, EVERY DAY, FOR MONTHS", "amber"]])  # "guys in FBI windbreakers buying coffee, every single day, for months"
seg(636.21, 641.15, src="loc-andrews-1998.jpg", motion="pan_right")                          # "Your neighbor probably has a theory… I'd bet everybody did."
seg(641.15, 645.33, src="wyff search teams in a field 1998.mp4")                             # "What comes next is one of the biggest manhunts"
seg(645.33, 651.75, src="wyff searchers by the road 1998.mp4")                               # "At the peak, more than 200 federal agents, working alongside local officers"
seg(651.75, 653.61, src="J clip.mp4", **{"in": 1.0})                                        # "Helicopters with heat cameras."
seg(653.61, 654.85, src="wyff bloodhound 1998.mp4")                                          # "Bloodhounds."
seg(654.85, 659.20, src="blender H_grid.mp4")                                                # "Teams walking ridgelines for weeks. Almost nothing." (3D search grid)
# BITE 659.20: a searcher to WYFF, "I wouldn't say it's tough, but it's a job that we have to do."
seg(659.20, 665.37, src="loc-nantahala.jpg", motion="push_in", fx=("fog",))                 # "Some of that is the land. The Nantahala is steep, densely wooded"
seg(665.37, 669.11, src="L05 nantahala.mp4", **{"in": 2.0})                                 # "all ravines and hollows, and Rudolph had grown up in it."
seg(669.11, 671.69, src="wyff search team on a trail 1998.mp4")                              # "The people searching mostly hadn't."
seg(671.69, 673.83, card=[["THE OTHER PART:", "type"], ["THE PEOPLE", "amber"]])            # "The other part was the people."
seg(673.83, 678.81, src="wyff local resident 1998.mp4")                                      # "A lot of folks in that corner of the state didn't trust the federal government"
seg(678.81, 682.85, card=[["“RUN, RUDOLPH, RUN”", "big"], ["T-SHIRTS FOR SALE", "type"]])  # "'Run, Rudolph, Run' T-shirts were for sale."
seg(682.85, 684.31, card=[["BUMPER STICKERS", "type"]])                                      # "There were bumper stickers."
seg(684.31, 688.49, card=[["REPORTEDLY, A RESTAURANT SIGN:", "type"], ["“RUDOLPH ATE HERE”", "amber"]])  # "A restaurant reportedly put up a sign joking that Rudolph ate there."
seg(688.49, 693.71, card=[["NOT THE WHOLE REGION", "type"], ["PLENTY WERE SICKENED BY WHAT HE'D DONE", "amber"]])  # "I don't want to paint the whole region… sickened by what he'd done"
seg(693.71, 697.87, src="66 swecker clip.mp4", tag=["CHRIS SWECKER", "FBI"])                 # "but the agents felt the cold shoulder, and they said so."
seg(697.87, 701.23, card=[["JULY 1998", "amber"], ["A REAL BREAK", "type"]])                # "July 1998, there's a real break."
seg(701.23, 706.77, card=[["GEORGE NORDMANN", "type"], ["HEALTH FOOD STORE OWNER", "amber"]])  # ("George Nordmann.jpg" is actually a sketch of Rudolph: not used)  # "Rudolph approaches George Nordmann… looking for supplies"
seg(706.77, 712.83, card=[["HE TAKES: FOOD, NORDMANN'S TRUCK", "type"], ["LEAVES: MONEY AND A NOTE", "amber"]])  # "A few days later he comes back and takes food and Nordmann's truck, leaving money and a note"
seg(712.83, 716.93, card=[["THE TRUCK IS RECOVERED", "type"], ["RUDOLPH ISN'T NEAR IT", "amber"]])  # "The truck was later recovered. Rudolph wasn't anywhere near it."
seg(716.93, 718.41, src="wyff search teams in a field 1998.mp4", **{"in": 2.2})             # "The trail went cold."
seg(718.41, 719.41, card=[["AGAIN.", "amber"]])                                              # "Again."
seg(719.41, 725.06, effect="paper-typewriter", ov={"title": "MARCH 1998"})                   # "There's another detail from 1998 that I genuinely didn't believe"
seg(725.06, 730.84, card=[["DANIEL RUDOLPH", "type"], ["ERIC'S BROTHER, SOUTH CAROLINA", "amber"]])  # "In March, Rudolph's brother Daniel set up a video camera in his garage in South Carolina"
seg(730.84, 736.76, card=[["HE SAID IT WAS", "type"], ["A MESSAGE TO THE FBI AND THE MEDIA", "amber"]])  # "and cut off his own hand… He said it was a message" (no images)
seg(736.76, 741.56, card=[["IT GOT INVESTIGATORS", "type"], ["NOWHERE", "amber"]])         # "Doctors reattached it. It got investigators exactly nowhere."
seg(741.56, 745.02, card=[["1999", "amber"], ["THE TASK FORCE SHRINKS", "type"]])          # "After 1999 the task force shrinks."
seg(745.02, 748.26, src="wyff wanted poster on a tree 1998.mp4")                            # "A small team keeps going, the reward stays up"
seg(748.26, 750.32, card=[["THE NATIONAL NEWS", "type"], ["MOVES ON", "amber"]])           # "and the national news moves on."
seg(750.32, 752.78, card=[["SEPTEMBER 11, 2001", "type"]])                                  # "Then September 11th happens"
seg(752.78, 757.35, src="G clip.mp4", **{"in": 4.0})                                        # "and nobody's thinking about a man in the North Carolina woods anymore."

MUSIC = [dict(start=608.0, end=659.2, bed="bed-B.mp3", gain=-19), dict(start=659.0, end=757.35, bed="bed-D.mp3", gain=-18)]
SFX = [(608.1, "sfx-typewriter-keys-short.mp3", -15), (608.1, "sfx-typewriter-ding.mp3", -16), (609.4, "sfx-typewriter-keys-short.mp3", -16),
       (611.3, "sfx-paper-slide.mp3", -15), (613.1, "sfx-stamp-thud.mp3", -13), (621.3, "sfx-whoosh.mp3", -17),
       (631.3, "sfx-typewriter-keys-medium.mp3", -16), (641.2, "sfx-helicopter-distant.mp3", -19), (651.8, "sfx-helicopter-distant.mp3", -16),
       (653.6, "sfx-dogs-distant.mp3", -14), (657.6, "sfx-low-hit.mp3", -14), (671.7, "sfx-typewriter-keys-short.mp3", -16),
       (678.9, "sfx-typewriter-keys-medium.mp3", -16), (682.9, "sfx-typewriter-keys-short.mp3", -16), (684.4, "sfx-typewriter-keys-medium.mp3", -16),
       (688.5, "sfx-typewriter-keys-medium.mp3", -16), (697.9, "sfx-typewriter-keys-short.mp3", -16), (701.3, "sfx-paper-slide.mp3", -16),
       (706.8, "sfx-typewriter-keys-medium.mp3", -16), (712.9, "sfx-typewriter-keys-medium.mp3", -16), (718.42, "sfx-low-hit.mp3", -12),
       (719.5, "sfx-typewriter-keys-short.mp3", -16), (725.1, "sfx-typewriter-keys-medium.mp3", -16), (730.9, "sfx-typewriter-keys-medium.mp3", -16),
       (736.8, "sfx-typewriter-keys-short.mp3", -16), (741.6, "sfx-typewriter-keys-short.mp3", -16), (748.3, "sfx-typewriter-keys-short.mp3", -16),
       (750.4, "sfx-typewriter-keys-short.mp3", -16), (752.8, "sfx-wind-gust.mp3", -18)]
CUES = """608.06 whip right
718.41 shake 0.2
"""
BITES = [dict(at=659.20, src="bite wyff searcher a job we have to do 1998.mp4", dur=5.0)]
