# Chapter 8: The Stop (VO 14:09-15:26). Cut on word timestamps (vo-words.json); each cut starts on the word in its comment.
# Creator clips on their lines: 04/04b Postell, A (flashlight), K2 (second car), 69/69b (arrest). Real: booking photo
# (slow push), FBI poster, WYFF helicopter/bloodhound/reward callbacks and search teams, WLOS Postell interview.
# 3D: back-lot callback; TRUCK 1998 + ARREST 2003 pins; "the right mountains" -> one camp dot.
S = []
def seg(a, b, **k): S.append(dict(start=a, end=b, **k))
AMBER = "#E0A040"

seg(849.12, 850.74, src="blender H_savealot.mp4", **{"in": 1.0})                         # "Back to the parking lot."
seg(850.74, 854.14, src="04 postell clip.mp4", **{"in": 1.0})                            # "Postell isn't thinking about the Ten Most Wanted list."
seg(854.14, 856.08, src="A clip.mp4", **{"in": 1.0})                                      # "He thinks he's caught a prowler."
seg(856.08, 858.20, src="K2 police car.mp4")                                              # "Then another officer who responded"
seg(858.20, 861.34, card=[['"JERRY WILSON"', "type"]])                                     # "takes a long look at 'Jerry Wilson'"
seg(861.34, 863.84, src="Eric Rudolph, FBI Ten Most Wanted poster.png", motion="push_in")  # "and thinks he looks an awful lot like Eric Rudolph."
seg(863.84, 866.98, src="69 rudolph arrest clip.mp4", crop="830:900:548:15")  # crop removes the LIFE watermark (note #12)                                     # "Under questioning, the man finally admits it."
seg(866.98, 872.54, src="eric rudolph mugshot.jpg", motion="push_in", tag=["ERIC ROBERT RUDOLPH", "Booked May 31, 2003"])  # "His real name is Eric Robert Rudolph. No shootout. No standoff." (long hold)
seg(872.54, 873.92, card=[["FIVE YEARS", "amber"]])                                       # "After five years,"
seg(873.92, 875.00, src="wyff helicopter search 1998.mp4", **{"in": 0.5})                 # "the helicopters,"
seg(875.00, 875.92, src="wyff bloodhound 1998.mp4", **{"in": 0.6})                         # "the dogs"
seg(875.92, 877.82, src="wyff reward one million 1998.mp4")                               # "and a million-dollar reward,"
seg(877.82, 882.04, src="04b postell clip.mp4", **{"in": 2.0})                            # "the guy was picked up by a 21-year-old rookie who thought he'd caught a burglar."
seg(882.04, 887.68, src="wlos postell interview.mp4")                                     # "Postell said in interviews afterward that he didn't recognize him. He was just doing his rounds."
seg(887.68, 889.64, src="69b rudolph arrest clip.mp4", crop="830:900:548:15")  # crop removes the LIFE watermark (note #12)                                    # "And here's the part that gets me"
seg(889.64, 899.22, src="blender H_arrest.mp4")                                           # "where was this? Murphy. Near where they'd found his abandoned truck… he hadn't gone far." (3D)
seg(899.22, 902.44, effect="stacked-highlight", ov={"title": "THE PART PEOPLE|GET WRONG", "backgroundImage": "loc-nantahala.jpg", "accent": AMBER})  # "And that's the part people get wrong about this manhunt."
seg(902.44, 905.14, card=[["THE FBI WASN'T SEARCHING", "type"], ["THE WRONG PLACE", "amber"]])  # "The FBI wasn't searching the wrong place."
seg(905.14, 908.80, src="wyff search team on a trail 1998.mp4")                           # "Investigators believed he was still in western North Carolina,"
seg(908.80, 912.26, src="wyff searchers by the road 1998.mp4", **{"in": 2.5})             # "and some people on the task force kept the search focused there"
seg(912.26, 915.94, card=[["OTHERS FIGURED:", "type"], ["DEAD OUT THERE, OR LONG GONE", "amber"]])  # "even when others figured he'd died out there or slipped away."
seg(915.94, 917.16, card=[["THEY WERE RIGHT.", "amber"]])                                 # "They were right."
seg(917.16, 926.63, src="blender H_campsite.mp4")                                         # "They were searching the right mountains… finding his campsite… two very different things." (3D)

MUSIC = [dict(start=849.1, end=889.7, bed="bed-A.mp3", gain=-18), dict(start=889.5, end=926.63, bed="bed-B.mp3", gain=-19)]
SFX = [(849.15, "sfx-typewriter-ding.mp3", -16), (849.2, "sfx-night-forest.mp3", -22), (854.2, "sfx-flashlight-click.mp3", -11),
       (856.1, "sfx-car-idle-gravel.mp3", -17), (858.25, "sfx-typewriter-keys-medium.mp3", -16), (861.4, "sfx-paper-slide.mp3", -15),
       (866.98, "sfx-boom-hit.mp3", -10), (866.99, "sfx-camera-shutter.mp3", -12), (872.6, "sfx-typewriter-keys-short.mp3", -16),
       (873.95, "sfx-helicopter-distant.mp3", -16), (875.0, "sfx-dogs-distant.mp3", -14), (875.95, "sfx-stamp-thud.mp3", -13),
       (889.7, "sfx-whoosh.mp3", -17), (899.3, "sfx-pen-scribble.mp3", -16), (902.5, "sfx-typewriter-keys-medium.mp3", -16),
       (912.3, "sfx-typewriter-keys-medium.mp3", -16), (916.0, "sfx-low-hit.mp3", -13), (917.2, "sfx-whoosh.mp3", -18)]
CUES = """849.12 whip right
866.98 zoomthru
866.99 shake 0.3
"""
