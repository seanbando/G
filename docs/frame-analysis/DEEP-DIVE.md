# Deep dive: lighting, color, expressions and every camera move (Nov 19, 2026)

Tools: `tools/analyze_frames.py` (every frame) + `tools/deep_shots.py` (every shot: move type, grade, palette, mid-frame contact sheet).
Contact sheets: `jensen-shots/shots-sheet.jpg`, `google-shots/shots-sheet.jpg`, `ours-v5-shots/shots-sheet.jpg`.

## Numbers per shot (averages)
| | Jensen (139 shots) | Google (38 shots) | Ours, three friends v5 (12 detected shots) |
|---|---|---|---|
| Brightness (0-255) | 120 | 111 | 94 |
| Contrast | 64 | 56 | 64 |
| Saturation | 118 | 122 | 130 |
| Warm vs cool (R-B) | +1 neutral | -19 cool | -14 cool |
| **Vignette (centre brighter than corners)** | **97** | **104** | 56 |
| **Deep shadows (share of frame)** | **17%** | **13%** | 4% |
| Bright highlights | 12% | 7% | 18% (white text/cards) |
| Dominant colours | dark purple, near-black navy, deep greens (brand color) | dark navy, black, grey props | off-white cards + flat navy |

## Camera move in every shot (Jensen, 139 shots)
- push-in 34%, **shake / handheld 30%**, pull-back 22%, tilts 7%, pans 6%, static under 1%.
- Fast moves carry **motion blur**; several shots have a **blurred foreground object** (depth of field) in front of the character.
- Shot sizes rotate: extreme close-up (face fills frame), close, medium, wide establishing, **low angle looking up** for power (the crown), over-the-shoulder, POV.

## Characters and expressions
- Characters are simple 3D "bean" figures (white ball head, stick limbs) with **2D drawn faces**: the look is flat, the world is 3D.
- The face changes on almost every beat: smug sunglasses, huge grin, wide shocked eyes, sweat drop, dizzy spiral eyes, tears, angry brows.
- Identity is carried by **one big accessory**: gold crown (Jensen), hard hats printed META / OPENAI / MICROSOFT / ELON, boxing gloves, pink hair. You know who is who even in a 0.5 s shot.
- About a third of shots are close-ups where the face fills the frame.

## Sets, lighting and props
- **A new set for almost every line:** throne room, gold mine, shovel shop, office, beach, boxing ring, race track, family dinner, port with EXPORT BAN, stock board.
- Lighting recipe: dark set, **coloured key light in the brand colour** (NVIDIA green, AMD red), strong spotlight on the character, corners falling to black.
- **Props say the words:** SHOVELS sign, $$$ register, $100 price board, DRIVER v1.0 screen, IMAGE CONTEST 2012, FAMILY BUSINESS banner, EXPORT BAN gate.
- Particles: gold coins, confetti, money bursts on payoff words.
- Captions: 1-3 words, small white bold with black outline, at about 60% height over the character's torso, swapping about 2x per second.

## What we change (targets for every video)
1. **Light like them:** dark set, spotlight on the subject, vignette about 90-100, deep shadows 10-20%, one brand/story colour per scene as the key light.
2. **A set per line or beat** (street, office, trading floor, bank, bedroom, data center, ring...), from the 3D set library.
3. **Faces big and changing:** close-ups on about 1 in 3 shots; swap the expression on each beat (smug, shocked, crying, sweating, dizzy).
4. **One identity accessory per character** (crown, labelled hat, shoebox for Jay, watch for Maya, glasses for Sam).
5. **Camera mix:** about 35% push-in, 20% pull-back, 25-30% handheld shake on tense lines, plus tilts, low angles and motion blur on whips.
6. **Props carry the key words** instead of text cards.
7. Particles on payoff words.
