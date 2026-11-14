# 01 — Asset Prompts: characters, locations, recreated scenes

How to make every recreated asset so it looks the same each time it appears.
Shot numbers in the creator's "Create list" refer to their Shot list tab. Check them against `shot-list.md` before you file assets; the two numberings differ.

## The rule for real people (stricter than the Create list)
- **Never generate a real person's face.** That covers victims and officials, and also Rudolph, Jewell and Postell. Their faces appear only in their real photos.
- AI characters are **stand-ins**: same build, hair, outfit and lighting, but always **from behind, in silhouette, or with the face in shadow / out of frame**.
- Character sheets therefore show **back, three-quarter-back and side-in-shadow** views, not a front face view.
- Use the real photo only to match build, clothing and era, not the face.
- The recreation look is **stylized 3D (game-engine render), not photoreal**, so nobody mistakes it for real footage. This matches the competitors (Uncovering labels theirs "made by humans").

## Workflow (do it in this order)
1. **Style frame.** Generate ONE image with the master style below until you love it. Save it as `00-style.png`. Every later image uses it as a style reference.
2. **Character sheets.** One image per character using the sheet template. Pick the best and save as `char-<name>.png`.
3. **Location plates.** One empty wide shot per location (no people). Save as `loc-<name>.png`.
4. **Scene stills.** For each scene, upload character sheet + location plate + style frame as references, then use the scene prompt. Make 4, pick 1.
5. **Animate.** Put the chosen still into an image-to-video tool (Kling, Runway, Veo, Hailuo, etc.) with the motion prompt. 5s clips, cut to 3–8s in the edit.
6. **File naming.** `scene-A-01.png`, `scene-A-01.mp4`, so the editor can find them by scene letter.

Tool notes: any image tool that accepts **reference images** works (Midjourney with character/style reference, Flux Kontext, ChatGPT images, Gemini image, Ideogram). The key is to always feed the same `00-style.png` plus the character sheet and location plate. Never generate a character from text alone after the sheet exists.

## Master style (add to EVERY prompt)
```
Stylized cinematic 3D render, game-engine look, slightly simplified realistic proportions, matte materials. Dark, desaturated color grade with cool teal-blue shadows; warm amber is the only accent color. Soft film grain, shallow depth of field, 16:9. Faces never visible: hidden in shadow, turned away, or out of frame. No text, no logos, no watermarks.
```

## Character sheet template
```
Character reference sheet on a plain dark gray background, three views side by side: back view, three-quarter back view, side view with the face in deep shadow. [CHARACTER DESCRIPTION]. Same outfit in all three views. Full body, neutral standing pose, even studio lighting. [MASTER STYLE]
```

| File | Character description (paste into [CHARACTER DESCRIPTION]) |
|---|---|
| `char-rudolph-1998` | A thin man around 30, short dark hair, plain 1990s clothes: faded dark denim jacket, gray t-shirt, jeans, work boots |
| `char-rudolph-2003` | A thin, fit man in his mid-30s, fresh short haircut, clean-shaven jawline seen only from the side in shadow, dark zip jacket, dark pants, worn boots |
| `char-jewell-1996` | A heavyset man in his early 30s, short hair, wearing a 1996 private security guard uniform: light blue shirt, dark pants, belt with radio, generic security patch (no logo) |
| `char-postell-2003` | A young slim police officer around 21, short hair, dark navy small-town police uniform, duty belt, holding a flashlight |
| `char-911-caller` | A man's silhouette in a dark jacket and cap, completely black against light, no features |
| `char-student` | A college student in late-1990s casual clothes: oversized flannel shirt, jeans, backpack, seen from behind |
| `char-fbi-agent` | A federal agent in a navy windbreaker with plain yellow block letters on the back (no real insignia), khakis, 1990s gear |

## Location plate template
```
Wide establishing shot, no people. [LOCATION DESCRIPTION]. [MASTER STYLE]
```

| File | Location description |
|---|---|
| `loc-olympic-park-1996` | A crowded city park at night in summer 1996, a lit concert stage in the distance, a tall metal sound-and-light tower, a park bench in the foreground, warm stage light against blue night |
| `loc-payphone-1996` | An empty city street at night, an old 1990s payphone on a pole under a single streetlight, wet pavement |
| `loc-apartment-media` | A two-story apartment complex in daylight, TV news vans with satellite dishes parked out front (no logos), reporters' tripods |
| `loc-sandy-springs` | A plain suburban office building in winter daylight, front entrance and a small parking lot |
| `loc-otherside-lounge` | A small single-story bar exterior at night, February, red and blue police lights reflecting on the wall |
| `loc-birmingham-clinic` | A small clinic entrance on a city sidewalk on a cold gray morning at 7:30 AM, a gray 1990s Nissan compact pickup parked at the curb |
| `loc-nantahala` | Steep Appalachian ridges covered in dense bare winter trees, mist in the hollows, an old logging road, gray light |
| `loc-hidden-camp` | A small tarp shelter tucked on a steep forested slope at dusk, a half-buried plastic barrel, far below the tiny warm lights of a small town |
| `loc-andrews-1998` | A small-town gas station in daylight, 1998, a few white task-force trailers in the lot |
| `loc-murphy-street` | A quiet small-town main street at 3:30 AM, one streetlight, a parked patrol car, mountains black behind |
| `loc-savealot-backlot` | The back of a small grocery store at night: cinderblock wall, two dumpsters, a loading door, dense pine trees right behind, one bright flashlight beam on the ground |

## Scene prompts (still → animate)
Upload the listed character sheet(s), location plate and `00-style.png` as references. Paste the still prompt + master style. Then animate the chosen still with the motion prompt.

| Scene | Refs | Still prompt | Motion prompt (image-to-video) |
|---|---|---|---|
| **A. The stop** | postell-2003, rudolph-2003, savealot-backlot | A patrol car with headlights off rolls into the back lot; a police officer seen from behind raises a flashlight; the amber beam lands on a man crouched beside a dumpster, his face turned away into shadow | Slow push-in toward the dumpster as the flashlight beam sweeps across and stops on the crouched figure |
| **B. The backpack** | jewell-1996, olympic-park | A green military-style backpack alone under a park bench at night, low angle; behind it, out of focus, a security guard seen from behind looks toward it; crowd and stage lights far back | Very slow push-in on the backpack; crowd lights flicker softly in the background |
| **C. Clearing the crowd** | jewell-1996, olympic-park | Security guards seen from behind with arms out, moving concertgoers back from the tall tower at night | Guards wave the crowd back; people drift away from camera |
| **D. The call** | 911-caller, payphone | A black silhouette at a payphone under a streetlight lifts the receiver; small digital clock on a building nearby (no readable text needed, add 12:58 in the edit) | Hand lifts the receiver; slight camera drift; streetlight hum |
| **E. Walking the wrong way** | rudolph-1998, student, birmingham-clinic | On a cold street, a few people run toward rising smoke while one man in a denim jacket walks calmly the other way; camera behind him, a student in flannel follows at a distance | Camera tracks behind the walking man; runners pass in the opposite direction |
| **F. The plate** | birmingham-clinic | Close-up of a hand writing on a small notepad with a pen; in the soft background a gray compact pickup pulls away from the curb. Plate unreadable | Pen moves across paper; truck drives off out of focus |
| **G. Into the woods** | nantahala | An empty gray compact pickup parked at a misty trailhead, then fresh boot prints leading into the trees | Slow pan from the truck to the prints and into the dark trees |
| **H. Living rough** | rudolph-2003, hidden-camp | Hands gathering acorns from wet leaves (close-up), and the tarp camp on the slope looking down at small town lights at dusk; man only seen from behind | Hands sift leaves; second shot: slow pull-back from the camp to reveal the town lights below |
| **I. The night raid** | rudolph-2003, murphy-street, savealot-backlot | A figure in a dark jacket seen from behind slips between buildings at night and lifts a dumpster lid | Figure moves in from the dark edge of frame; lid lifts slowly |
| **J. The manhunt** | fbi-agent, nantahala | A helicopter with a searchlight sweeps a misty ridge; below, agents in navy windbreakers and a bloodhound walk through the trees, seen from behind | Helicopter crosses frame; searchlight sweeps; agents move uphill away from camera |

## Graphics (templates, not AI)
Build each type ONCE in your editor (CapCut / Premiere / After Effects), save it as a template, and reuse it. Every text element types on with the typewriter effect + keystroke SFX (style sheet §8).

| Type | How |
|---|---|
| Dark topo map + amber pins | Google Earth Studio (free) or a static map screenshot → desaturate, darken, tint teal → amber pin + label template. One base style, one copy per place. |
| Typewriter text cards | Typewriter font (e.g. Courier Prime / Special Elite), off-white on black, type-on animation, blinking cursor. |
| Highlight sweep | Document/photo on a dark background, slow push-in, amber rectangle at ~40% opacity wiping left→right across the key line. |
| Push-in | Scale 100% → 115% over ~6 seconds, ease in/out. |
| Name + date card | Lower-left corner, Anton caps name, smaller typewriter date line below, typed on. |
| Split screen | Two photos side by side, thin amber divider, label under each. |
| End screen | 20 seconds: video slot left, subscribe right, dark background. |
