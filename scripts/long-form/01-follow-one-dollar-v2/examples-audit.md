# Examples audit: Follow $1 (v2)

Every example and number in the script, with the arithmetic recomputed and what the picture must show so it matches the words exactly. Lines tagged EXAMPLE always carry the "EXAMPLE · MADE-UP NUMBERS" badge on screen; real numbers always carry a source tag.

| Line | What's said | Math check | ✅ | What the picture must show |
|---|---|---|---|---|
| S017–S018 | Shop worth $100 cut into 100 slices → each slice $1, one slice = 1% | $100 ÷ 100 = $1; 1 ÷ 100 = 1% | ✅ | Pizza with **100 slices** (`pizza({slices: 100, example: true})`), label "Shop worth $100", EXAMPLE badge |
| S019 | Shop grows to $200 → slice worth $2 | $200 ÷ 100 = $2 | ✅ | Same 100-slice pizza grows; slice tag changes $1 → $2 |
| S020 | Shop shrinks to $50 → slice worth 50 cents | $50 ÷ 100 = $0.50 | ✅ | Pizza shrinks; slice tag $1 → 50¢ |
| S023–S025 | Company A: $500 a share, 3 slices → whole pizza $1,500 | 3 × $500 = $1,500 | ✅ | Pizza with **3 slices**, each tagged $500, total $1,500, EXAMPLE badge |
| S026–S027 | Company B: $5 a share, a million slices → $5 million; the cheap slice is from the far bigger pizza | 1,000,000 × $5 = $5,000,000 (about 3,333× Company A) | ✅ | Much **bigger** pizza, densely sliced, labelled "1,000,000 slices" (can't draw a million lines), EXAMPLE badge |
| S028 | Price × number of shares = market cap | Definition | ✅ | Formula card: Price × shares = market cap |
| S029 | Apple: roughly 15 billion shares → value in the trillions | 15 billion × $200–$300 = $3.0–4.5 trillion | ⚠️ | Real-data line: **source tag** (Apple 10-K share count). ⚠️ Re-check the latest share count before upload |
| S033 | One Apple share costs a few hundred dollars; your $1 buys a crumb | $1 ÷ a few hundred dollars ≈ well under 1% of one share | ⚠️ | Pizza = Apple, **highlighted slice = 1 share**, crumb = your $1. Note: "not to scale: about 15 billion shares". ⚠️ Confirm Apple's price is still in the hundreds before upload |
| S045–S046 | Booth buys at $250.00, sells at $250.02 → two-cent spread | $250.02 − $250.00 = $0.02 | ✅ | Booth with two signs $250.00 / $250.02, **EXAMPLE badge**, gap labelled 2¢ |
| S072–S073 | Quiz: how much of your dollar Apple gets → usually none | Secondary-market trade pays the seller (fact-checked) | ✅ | Three choices on screen: all of it / half / none |
| S081–S083 | Retired teacher sells a little stock; your dollar buys **a crumb of her stock** and helps pay for her roof | $1 buys a fraction of a share (matches S033) | ✅ | Teacher with roof estimate; Buck's crumb goes to her; roof gets a shingle. **Fixed:** the line used to say "buys her share" |
| S088–S090 | Tuesday trade settles Wednesday (T+1) | Tuesday + 1 business day = Wednesday | ✅ | Two calendar pages Tue → Wed |
| S110 | Maya buys 10 shares at $200 → costs $2,000 | 10 × $200 = $2,000 | ✅ | EXAMPLE card: 10 × $200 = $2,000 |
| S111–S112 | Jordan pays $250 a share for all 10 → Maya makes $500 before taxes and fees | 10 × $250 = $2,500; $2,500 − $2,000 = $500 | ✅ | EXAMPLE card: 10 × $250 = $2,500 → +$500 (before taxes and fees) |
| S113 | At $150 a share, Maya would have lost $500 | 10 × $150 = $1,500; $2,000 − $1,500 = $500 | ✅ | Same card, second line: 10 × $150 = $1,500 → −$500 |
| S118–S120 | Last trade $250.00; seller asks $250.05, buyer pays → last-trade price $250.05 | New last trade = $250.05 (+$0.05) | ✅ | Price board `priceBoard({price: '$250.05', change: '+$0.05', example: true})`, flips $250.00 → $250.05 |
| S135–S136 | Steady 10% a year for 40 years: $1 → about $45 | $1 × 1.10^40 = $45.26 → "about $45" | ✅ | Growth path with **EXAMPLE badge** and "steady 10%, illustration, not a promise"; show $45.26 rounded to $45 |
| S133 | S&P 500 historically ~10% a year (dividends reinvested, before inflation) | Damodaran 1957–2025 ≈ 10.6% | ✅ | Real data: **source tag** (NYU Stern / Damodaran) |
| S138–S139 | 2007–2009: lost more than half; 2020: fell almost 34% Feb 19–Mar 23 | ≈ 57% and 33.8% | ✅ | Bumpy road with two potholes; **source tags** |
| S149 | SIPC up to $500,000 per customer incl. $250,000 cash | Fact-checked limits | ✅ | Shield graphic with both limits; **source tag** (SIPC) |

## Fixes made during this audit

- **S083 script:** "Your dollar buys her share" → "Your dollar buys a crumb of her stock". One dollar buys a fraction of a share, as S033 says.
- **Pizza prop:** now draws any slice count cleanly (100 slices for S017, 3 for S025) and takes a `note` ("not to scale") and an EXAMPLE badge.
- **Price board prop:** gets an EXAMPLE badge for made-up prices.

## Still to confirm before upload

- Apple's current share count (S029) and that its share price is still "a few hundred dollars" (S033).
