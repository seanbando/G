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
| `onscreen_text_from_script_only` | leave off | The pause questions need on-screen text that isn't spoken word-for-word |

**Style previews:**
- [Whiteboard](https://www.youtube.com/watch?v=NRxRhXGQKKA) (Canvas, Growth plan) · [Marker Whiteboard](https://www.youtube.com/watch?v=dUxwqyc4QY8) (Whiteboard with a marker drawing)
- [Dry Erase](https://www.youtube.com/watch?v=i6Ifu_mkxhI) (Sketch, Growth plan)
- [Classic](https://www.youtube.com/watch?v=h8f12Cwe9Gs) (Sketch, works on any plan)

## `prompt` (1580 of 4,000 characters)

```
Beginner-friendly explainer for 18 to 40 year-old Americans who are new to investing. It follows one dollar from tapping "buy" in an investing app to owning a tiny slice of Apple, through five stops. Stop 1, your app: the dollar becomes an order at the market price. Stop 2, the market maker: a big trading company that works like a store keeping stock on the shelf, buying slightly cheaper than it sells; market makers often pay apps for orders, which is one reason trading can be free. Stop 3, the stock exchange: a matchmaker for buyers and sellers; the bell rings on Wall Street at 9:30 a.m. Eastern but the computers are in New Jersey; the market is open 9:30 to 4 on weekdays. Stop 4, the seller: the dollar goes to a stranger, not Apple; Apple only got money when it first sold shares in December 1980, like a band paid only for the first sale of a concert ticket. Stop 5, the clearinghouse (the DTCC): the trade becomes final the next business day; the paperwork is registered to Cede & Co., which works like a coat check, but the stock is yours; SIPC protects accounts if a broker fails, not if a stock falls. After the trip: the opening trap ($500 share vs $5 share, explained with pizzas: price times number of shares), two ways to make money (Maya buys 10 shares at $200 and sells to Jordan at $250 for a $500 profit; dividends), why prices move (the price is the last trade), an S&P 500 index fund as a basket of about 500 companies, about 10% a year historically so $1 could become about $45 in 40 years (an example, not a promise), and the 2007-2009 and 2020 drops.
```

## `video_instructions` (1438 of 2,000 characters)

```
Simple whiteboard explainer with a recurring cast; one idea per scene, uncluttered, big readable numbers, no stock photos. Hero: a dollar bill with a simple face, in most scenes. Recurring road map with five numbered stops left to right: 1 Your App, 2 Market Maker, 3 Exchange, 4 Seller, 5 Clearinghouse. Show it between stops and tick off finished stops. Draw each character the same way every time: YOU, a stick figure holding a phone; THE APP, a phone with a face; THE MARKET MAKER, a friendly store clerk with two price signs; THE EXCHANGE, a building with a face; THE SELLER, a retired teacher holding a roof estimate; THE CLEARINGHOUSE, a referee labelled DTCC; MAYA and JORDAN, two young investors. Key visuals: two pizzas (3 slices x $500 vs a million slices x $5); a store shelf of Apple stock; a bell on Wall Street with an arrow to a data center in New Jersey; a concert ticket passed fan to fan; an "OWNER: ???" paper in the opening that becomes "Cede & Co." at stop 5; a coat check counter; a SIPC shield; a see-saw for price; a basket of company logos; a bumpy road with potholes for market drops; a stopwatch reading "under 1 second". There are five silent 2 to 3 second pauses right after a question. During each one, keep the question large on screen: "A or B?"; "A) Apple  B) Your app  C) A stranger"; "10 shares, bought at $200, sold at $250"; "Last trade $250.00. Someone pays $250.05. Price now?"; "$5, $15, or $45?".
```

The full scene-by-scene drawing notes are in `scripts/04-script-follow-one-dollar.md` if you want to adjust anything above.
