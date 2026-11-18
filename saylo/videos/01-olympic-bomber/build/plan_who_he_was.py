# Chapter 5: Who He Was (VO 9:09-10:08). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Real material: WYFF (his home, the truck hauled out, searchers, a local's bite), creator's Army/G/L05 clips, photos.
# 3D: clay mountains diorama (build/blender/H_diorama_mountains.py) with MURPHY / TOPTON / NANTAHALA.
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))

seg(549.76, 552.29, card=[["WHO HE WAS", "big"]])                                      # "Rudolph was born in 1966 in"
seg(552.29, 553.97, card=[["BORN 1966", "type"], ["MERRITT ISLAND, FLORIDA", "amber"]])  # "Merritt Island, Florida."
seg(553.97, 556.31, card=[["1981", "amber"], ["HIS FATHER DIES", "type"]])            # "His dad died in 1981" (young eric rudolph.jpg includes a 2003 arrest photo: not used)
seg(556.31, 563.11, src="blender H_mountains.mp4")                                      # "his mother moved the kids up to the mountains around Topton and Murphy… Nantahala National Forest" (3D)
seg(563.11, 569.15, card=[["REPORTEDLY, IN THE 1980s", "type"], ["A CHURCH IN MISSOURI", "amber"]])  # "According to reporting… a church in Missouri"
seg(569.15, 573.09, card=[["CHRISTIAN IDENTITY", "big"], ["A WHITE SUPREMACIST RELIGIOUS MOVEMENT", "type"]])  # "tied to Christian Identity, which is a white supremacist religious movement"
seg(573.09, 577.93, src="52 army clip.mp4", tag=["ERIC RUDOLPH", "U.S. Army, 101st Airborne"])  # "Rudolph went into the Army in 1987, served with the 101st Airborne"
seg(577.93, 581.87, card=[["FORT CAMPBELL, KENTUCKY", "type"], ["1987 – 1989", "amber"]], bg="52b 101st patch.jpg")  # "at Fort Campbell, Kentucky, and was out by 1989"
seg(581.87, 583.25, src="wyff rudolph home 1998.mp4")                                    # "Then he went home." (real: his home near Murphy)
seg(583.25, 584.71, src="G clip.mp4")                                                    # "Back to the woods."
seg(584.71, 590.25, card=[["PEOPLE WHO KNEW HIM:", "type"], ["HE KNEW THAT FOREST", "amber"]])  # "People who knew him said… he knew that forest"
seg(590.25, 594.35, src="G clip.mp4", **{"in": 1.5})                                     # "Hunting, camping, the old logging roads, the hollows."
# BITE 594.35: a local to WYFF, "He knows the area incredibly well. He grew up here."
seg(594.35, 596.57, card=[["FEBRUARY 1998", "type"], ["ABOUT A WEEK AFTER BIRMINGHAM", "amber"]])  # "About a week after Birmingham,"
seg(596.57, 600.15, src="wyff rudolph truck found 1998.mp4")                            # "agents found his gray Nissan abandoned near Murphy" (real: the truck hauled out)
seg(600.15, 604.75, src="L05 nantahala.mp4")                                            # "And he was just gone. Into more than half a million acres of mountain"
seg(604.75, 608.06, src="wyff searchers in the woods 1998.mp4")                         # "that he knew better than anyone looking for him."

MUSIC = [dict(start=549.7, end=608.06, bed="bed-D.mp3", gain=-18)]
SFX = [(549.8, "sfx-typewriter-keys-short.mp3", -15), (549.8, "sfx-typewriter-ding.mp3", -16), (552.3, "sfx-typewriter-keys-medium.mp3", -16),
       (554.0, "sfx-paper-slide.mp3", -16), (556.4, "sfx-whoosh.mp3", -17), (563.2, "sfx-typewriter-keys-medium.mp3", -16),
       (569.2, "sfx-typewriter-keys-medium.mp3", -16), (573.1, "sfx-paper-slide.mp3", -17), (578.0, "sfx-typewriter-keys-short.mp3", -16),
       (583.3, "sfx-wind-gust.mp3", -18), (584.8, "sfx-typewriter-keys-medium.mp3", -16), (590.3, "sfx-night-forest.mp3", -20),
       (594.4, "sfx-typewriter-keys-short.mp3", -16), (600.2, "sfx-low-hit.mp3", -14), (604.8, "sfx-helicopter-distant.mp3", -19)]
CUES = """549.76 whip right
"""
BITES = [dict(at=594.35, src="bite wyff he knows the area 1998.mp4", dur=4.2)]
