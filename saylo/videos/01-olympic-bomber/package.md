# 01 — Packaging

**Title:** Why the Olympic Bomber Was So Hard to Catch
**Test against (Test & Compare):** How a Rookie Cop Caught the Olympic Bomber

## Thumbnail A — approved
Base image: `thumbnail-base.webp` · text mockup: `thumbnail-text-mockup.png` (placeholder font)

Prompt that produced the approved base:
```
3D isometric miniature diorama at night, 16:9, camera close and low at a 35-degree angle. Focus on the corner of a small-town grocery store's back lot: a cinderblock wall, one dumpster, a few parking lines, dense dark pine trees right behind the wall, mountain ridges fading to black above. Everything is matte white-gray clay, heavily desaturated. A tiny gray police officer figure stands at the lower left edge holding a flashlight; its beam crosses the asphalt and hits a crouching human figure beside the dumpster. The beam and the crouching figure are bright saturated amber-orange, the only color in the image. The dumpster and crouching figure fill the right-center of the frame and are large and clearly readable. Top third of the frame is dark and empty for text. Clean render, high contrast, tilt-shift depth of field. No text, no logos, no faces.
```

**Overlay (Canva):** "5 YEARS" centered in the dark sky at the top, Anton font, off-white, the "5" in the same amber as the beam. No arrow needed.
**Finishing tweaks:** dim the white wall lamp above the door; darken the wall behind the figure ~10%.
**FINAL (Nov 15, 2026): `thumbnail-final.jpg`** (re-exported at 1920x1080, 4:4:4 colour, light sharpening, 375 KB, upload this; the first 1280x720 export looked blurry once posted on YouTube). Made with `python saylo/tools/make_thumbnail.py thumbnail-base.webp thumbnail-final.jpg --text "5 YEARS" --amber "5" --accent "#F39A2B" --dim "835,410,150,0.65" --darken "1200,290,1672,790,0.10"`: real Anton font, "5" in the beam's amber, wall lamp dimmed, wall behind the figure darkened 10%. Phone preview: `thumbnail-final_phone.png`.
**Phone-size test:** passed (story reads at 168px wide). Bottom-right (timestamp area) is empty wall.

Lessons from v1 of the image: the first render was too wide — the figure was a few pixels at phone size, and the light came from a wall lamp (read as a security light). Fixed by moving the camera close and adding the officer holding the flashlight.

## Thumbnail B — optional test
```
3D isometric miniature terrain model, 16:9, aerial view at a 45-degree angle. Vast steep Appalachian mountains covered in pine forest, rendered in matte white-gray clay, heavily desaturated. A tiny white helicopter in the upper right casts a searchlight cone onto the trees. A faint grid of search lines is drawn across the mountains in thin white. Deep in a ravine, outside the searchlight, one tiny campsite glows bright saturated amber-orange, the only color in the image. Clean render, dramatic shadows, tilt-shift depth of field. Leave the left third dark and clear for text. No text, no logos.
```
Overlay: "200 AGENTS" in a white box label + one white arrow to the campsite.

**MADE (Nov 16, 2026): `thumbnail-b.jpg`** (1920x1080, 432 KB). Built in Blender instead of an AI image (same clay
look as the video, no credits): `build/blender/T_thumb_hunt.py` rendered at 2560x1440 → `thumbnail-b-base.png`, then
`python saylo/tools/make_thumbnail.py thumbnail-b-base.png thumbnail-b.jpg --text "200 AGENTS" --amber "200" --accent "#F39A2B" --align left --left 0.045 --cap 0.15 --top 0.07 --arrow "0.255,0.33,0.348,0.815"`.
Why: it says the title's "hard to catch" at a glance (200 agents, a helicopter searchlight on the wrong ridge, one
tiny amber camp it keeps missing). A ("5 YEARS", the capture) shows the ending; B shows the problem. Phone test passed.
**Use:** upload both in YouTube's Test & Compare (Studio → video → Thumbnail → "Test & compare"), let YouTube pick by watch time.

## YouTube upload copy (FINAL v2, Nov 15, 2026)
Chapter times are measured from the joined chapter files of FINAL v2 (18:31).

SEO (vidIQ, Nov 15, 2026): "olympic bomber" ~3.8K searches/mo at low competition (41), "richard jewell" ~7.8K (64),
"true crime documentary" ~1M (49), "fbi most wanted" ~22.6K, "centennial olympic park" ~13.8K (22); "eric rudolph"
itself is under 750/mo. The most-viewed videos on this case are about Richard Jewell (60 Minutes 1.2M, NYT Retro Report
925K), and "largest manhunt in US history" is the phrase the WRAL doc (205K) ranks on. So: the first two lines carry
Olympic Bomber + Richard Jewell + Eric Rudolph + Centennial Olympic Park + 1996 Atlanta Olympics + manhunt, and the
hashtags lead with #RichardJewell over #EricRudolph.

Tags (456 characters, most important first):
`olympic bomber, eric rudolph, richard jewell, olympic park bombing, centennial olympic park bombing, 1996 atlanta olympics bombing, atlanta olympic bombing, eric rudolph manhunt, eric rudolph capture, largest manhunt in us history, fbi ten most wanted, fbi most wanted, true crime documentary, manhunt documentary, olympic bomber documentary, richard jewell true story, jeff postell, murphy north carolina, nantahala national forest, on the run, true crime`

```
The Olympic Bomber hid from the FBI for five years. In 1996 a pipe bomb exploded in Centennial Olympic Park during the Atlanta Olympics, and the FBI spent 88 days investigating the wrong man: Richard Jewell, the security guard who found the bomb and helped clear the crowd. The real bomber, Eric Rudolph, struck three more times, landed on the FBI's Ten Most Wanted list, and vanished into the mountains of western North Carolina in one of the largest manhunts in U.S. history.

He was finally caught at 3:30 in the morning behind a grocery store in Murphy, North Carolina, by Jeff Postell, a 21-year-old rookie cop. This true crime documentary covers the three things that made Eric Rudolph so hard to catch: the wrong man, a bomber with no name, and the Nantahala National Forest.

From the Centennial Olympic Park bombing to the Sandy Springs and Otherside Lounge bombings around Atlanta and the Birmingham clinic bombing, here is how the case went cold, how the manhunt played out, and how it finally ended.

0:00 3:30 AM in Murphy
1:49 The Park
4:07 The Wrong Man
6:58 Same Hands
7:59 Birmingham
9:21 Who He Was
10:23 The Hunt
12:57 Five Years
14:35 The Stop
15:52 The Deal
16:45 What It Actually Was
18:10 One Question

Do you think he really made it five years out there alone? Tell me in the comments.

Sources: court records, the FBI's case history, the Justice Department's review of the Jewell investigation, and news reporting from the time.

Archival footage and photos are used briefly, with commentary, for news reporting and education:
- Photos: Atlanta Journal-Constitution, via Georgia State University Library / Digital Library of Georgia
- 1996 broadcast and newspaper footage: Retro Report
- 1996 footage: AP Archive
- 1998 search and 2003 arrest footage: WYFF News 4
- Jeff Postell interview and 2003 footage: WLOS News 13
- Birmingham clinic aerial: Forgotten History
- 2003 arrest footage: LIFE
- Short scene from "Richard Jewell" (2019, Warner Bros. Pictures), shown on screen as a dramatization
- Sound tower photo: Don Ramey Logan, CC BY-SA 4.0, via Wikimedia Commons
- Public domain: FBI, U.S. Army, U.S. Department of Justice, Federal Bureau of Prisons

Recreations and 3D scenes were made for this video. They're illustrations, not real footage, and they don't show anyone's real face.

#TrueCrime #OlympicBomber #RichardJewell #EricRudolph #Manhunt
```

## Description credits (required: keep in the YouTube description)
Archival material used briefly with commentary:
- Photos: Atlanta Journal-Constitution, via Georgia State University Library / Digital Library of Georgia.
- 1996 broadcast and front-page footage: excerpts via Retro Report.
- Photos: Harrison Keely, CC BY 4.0, via Wikimedia Commons (if used in later chapters).
