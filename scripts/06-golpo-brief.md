# Golpo Brief: Follow $1 From Your Pocket to Wall Street

Settings for making the animation in Golpo with your own ElevenLabs narration. Golpo builds the visuals around the recording, so the voice, words and pauses come from the audio, and these settings only steer the look.

## Before Golpo can run

1. **Golpo plan:** using your own narration (`audio_clip`) needs a paid Golpo plan. The account connected here is on **Free with 0 credits**.
2. **Credits:** about 1 credit per minute of video, so roughly **11 credits** for this video.
3. **Narration file:** one MP3 of the full narration, built with `tools/build_track.py`, under 15 MB.
4. **A public link to that file:** Golpo can only fetch audio from a public https address. Either keep the file in this public GitHub repo and use its raw link, or upload the MP3 yourself in the Golpo app.

## Settings

| Field | Value | Why |
|---|---|---|
| `audio_clip` | the uploaded narration track | Your ElevenLabs voices instead of Golpo's |
| `visual_style` | **Whiteboard** (Canvas) with `pen_style` **marker**, or **Dry Erase** (Sketch) | Whiteboard looks; pick from the previews below |
| `pacing` | `fast` | One sentence per scene, matching the script's short scenes |
| `video_type` | `long` | 16:9 for YouTube |
| `timing` | `auto` | Length follows the narration |
| `language` | `en` | |
| `bg_music` | `lofi` or none | Calm bed that won't fight the voices |
| `onscreen_text_from_script_only` | **on** (`true`) | Any text Golpo writes on screen comes word-for-word from the narration, so it can't write something different from what's said. Every pause question is spoken aloud, so it can still appear. |

**Style previews:**
- [Whiteboard](https://www.youtube.com/watch?v=NRxRhXGQKKA) (Canvas, Growth plan) · [Marker Whiteboard](https://www.youtube.com/watch?v=dUxwqyc4QY8) (Whiteboard with a marker drawing)
- [Dry Erase](https://www.youtube.com/watch?v=i6Ifu_mkxhI) (Sketch, Growth plan)
- [Classic](https://www.youtube.com/watch?v=h8f12Cwe9Gs) (Sketch, works on any plan)

## `prompt` (2379 of 4,000 characters)

```
Beginner-friendly explainer for 18 to 40 year-old Americans who are new to investing. It follows one dollar from tapping "buy" in an investing app to owning a tiny slice of Apple, through five stops. Stop 1, your app: the dollar becomes an order at the market price. Stop 2, the market maker: a big trading company that regularly posts buy and sell prices, like a store that usually keeps stock on the shelf, buying slightly cheaper than it sells; market makers often pay apps for orders, which is one reason many apps charge no commission, and brokers still have to seek the best available deal. Stop 3, the stock exchange: a matchmaker for buyers and sellers; the bell rings on Wall Street at 9:30 a.m. Eastern, but the NYSE's and Nasdaq's trading computers are in New Jersey; regular hours are 9:30 to 4 Eastern, Monday to Friday, except holidays and early closes. Stop 4, the seller: the dollar goes to a stranger, not Apple; Apple got money when it first sold shares in December 1980; when investors trade Apple stock today, the money normally goes to the seller, like a concert ticket resold fan to fan. Stop 5, the clearinghouse: companies in the DTCC group clear and settle the trade, which normally settles one business day later; many brokerage shares are registered under Cede & Co., but the brokerage's records show you as the owner, a bit like a coat check; SIPC can help recover missing assets if a member broker fails (up to $500,000 per customer, including $250,000 cash), not market losses. After the trip: the opening trap ($500 share vs $5 share, explained with pizzas: price times number of shares equals market cap), two ways to make money (Maya buys 10 shares at $200 and sells to Jordan at $250 for a $500 profit; dividends), why prices move (the price usually shown is the last-traded price), an S&P 500 index fund as a basket fund owning about 500 companies, a historical return of roughly 10% a year with dividends reinvested, before inflation, so $1 growing 10% a year for 40 years becomes about $45 (an illustration, not a promise), and the 2007-2009 and 2020 drops. It ends with the narrator's own story: their first stock was Nvidia (their reason, not advice), a candlestick chart confused them at first, and they're learning about money to become financially free. Then it asks viewers which stop surprised them most and what their first stock was.
```

## `video_instructions` (1742 of 2,000 characters)

```
Simple whiteboard explainer with a recurring cast; one idea per scene, uncluttered, big readable numbers, no stock photos. Hero: a dollar bill with a simple face, in most scenes. Recurring road map with five numbered stops left to right: 1 Your App, 2 Market Maker, 3 Exchange, 4 Seller, 5 Clearinghouse. Show it between stops and tick off finished stops. Draw each character the same way every time: YOU, a stick figure holding a phone; THE APP, a phone with a face; THE MARKET MAKER, a friendly store clerk with two price signs; THE EXCHANGE, a building with a face; THE SELLER, a retired teacher holding a roof estimate; THE CLEARINGHOUSE, a referee labelled DTCC; MAYA and JORDAN, two young investors. Key visuals: two pizzas (3 slices x $500 vs a million slices x $5); a store shelf of Apple stock; a bell on Wall Street with an arrow to a data center in New Jersey; a concert ticket passed fan to fan; an "OWNER: ???" paper in the opening that becomes "Cede & Co." at stop 5; a coat check counter; a SIPC shield; a see-saw for price; a basket of company logos; a bumpy road with potholes for market drops; near the end, the narrator holding an Nvidia stock certificate labelled "My first stock" and a confusing candlestick chart; a stopwatch for the order ("a fraction of a second") next to a calendar for settlement ("next business day"). There are five silent 2 to 3 second pauses right after a spoken question. During each one, keep that question large on screen: "Which company is worth more?"; "Was it Apple, your app, or a stranger?"; "How much did Maya just make?"; "What does the last-trade price become?"; "About five dollars, fifteen dollars, or forty-five dollars?". Draw only what the narration is describing at that moment.
```

The full scene-by-scene drawing notes are in `scripts/04-script-follow-one-dollar.md` if you want to adjust anything above.

---

## Render: editorial marker version (2026-11-12)

The creator's brief: a whiteboard finance explainer for adults learning from zero, built around the narration, white background, black outlines, forest-green accents, red only for losses or warnings, diagrams that build as the narrator explains, money paths drawn with arrows, short phone-readable labels, no invented statistics, smooth transitions, expressive editorial marker.

| Field | Value |
|---|---|
| `audio_clip` | `audio/follow-one-dollar-v2-FULL-golpo.mp3` (mono 96 kbps copy; Golpo's uploader rejected the 11.6 MB original) |
| `visual_style` | **Editorial** (Canvas) with `pen_style` **marker** |
| `video_type` | `long` (16:9) |
| `pacing` | `normal` (related steps stay together) |
| `enable_camera_follow` / `visual_animation_style` | `true` / `auto` |
| `bg_music` | `engaging` |
| `onscreen_text_from_script_only` | `true` |
| `prompt` | the `prompt` above, unchanged |

Job: `b2a0bd55-109f-4a9e-8611-c1bf2b644541`. Cost about 12 to 13 credits (12 min 7 s).

`video_instructions` (1988 of 2,000 characters):

```
Whiteboard finance explainer for adults learning from zero, in expressive editorial marker. Clean white background, confident black outlines, restrained forest-green accents; red only for losses, costs or warnings. Polished, approachable, consistent.
Show how each idea works with simple drawings, comparisons, arrows and step-by-step diagrams built progressively as the narrator explains. When money or ownership moves, draw its path clearly with arrows. One main idea per scene; keep related objects visible while the explanation develops and keep related steps together instead of resetting the board each sentence; transition smoothly when the subject changes.
Start immediately on a visual for the opening hook; keep the first 30 seconds active with purposeful reveals and focus changes, then give each example time to land. No long blank moments and no holding a finished drawing without development.
Short labels and essential numbers only, large enough for a phone; never paragraphs. Match every amount, percentage, name and calculation to the audio. Illustrative charts must look illustrative, not like real historical data.
Recurring designs, the same every time: HERO a dollar bill with a simple face; YOU a person holding a phone; THE APP a phone with a face; MARKET MAKER a store clerk with buy and sell price signs; THE EXCHANGE a building with a face; THE SELLER a retired teacher; THE CLEARINGHOUSE a referee labelled DTCC; MAYA and JORDAN two young investors. A road map of five numbered stops (1 Your App, 2 Market Maker, 3 Exchange, 4 Seller, 5 Clearinghouse) returns between stops with finished stops ticked.
Key visuals: two pizzas for share price vs company value; an "OWNER: ???" paper that becomes "Cede & Co."; a coat check; a SIPC shield; a see-saw for price; a basket of companies for an index fund; a bumpy road for market drops.
During each silent pause after a spoken question, keep that question large on screen.
End on a clear visual of the final takeaway.
```
