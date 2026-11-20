# Fact check: Why Paying the Minimum Costs You More

| Claim | Status | Basis |
|---|---|---|
| $1,000 phone *can* cost $1,766 paying only the minimum | Verified for the example | Simulated: 22% APR, minimum = larger of $25 or 1% + interest, no new purchases; $1,766.46 |
| "A typical card charging about 22%" | Verified | Fed G.19 Q3 2026: 22.36% on accounts assessed interest |
| First minimum $28, $18 interest, $10 to the phone | Verified | $28.33 = $18.33 + $10.00 |
| "Five years and ten months" | Verified | 70 months exactly |
| Minimum "keeps you paying interest for years" | Verified | 70 months vs 12 at $100/month |
| $100 a month: paid off in one year, about $115 interest | Verified | 12 months, $114.89 |
| Statement box showing how long the minimum takes; required by law | Verified | CARD Act / Regulation Z minimum payment disclosure (CFPB) |
| Minimum formula | Simplified, fair | Varies by card ($25 to $40 floors); a $40 floor gives 34 months and about $350 interest. Said in the description |
| Monthly interest | Simplified, fair | Real cards use a daily rate; difference is small |

Description: "Example: $1,000 balance, 22% APR (Fed average on cards charged interest, Q3 2026), minimum = 1% + interest with a $25 floor, no new purchases. Your card's formula and rate may differ; check the minimum payment box on your statement. Not financial advice."


## Outside review (applied)
Independent re-run matched: minimum only 70 months, $766.46 interest, $1,766.46 total; $100/month 12 months, $114.89 interest, $1,114.89 total (fixed 22% APR, APR/12 monthly, minimum = max($25, interest + 1%), capped at balance, on time, no fees, no new purchases). Changes: "will cost" -> "can cost" (issuer formulas differ), "almost six years" -> "five years and ten months", line 3 split into short sentences, statement line names the real "Minimum Payment Warning" box and says it *estimates*.

## v3 script (Nov 20, 2026): "Why Banks Love People Who Pay the Minimum" (guess hook + year ladder + reveal)
Escalator version kept in script-escalator.md. Same model: $1,000, 22% APR, APR/12 monthly, minimum = max($25, interest + 1% of balance), no new purchases.
| Point | Paid so far | Still owe | Voice |
|---|---|---|---|
| Month 1 | $28.33 ($18.33 interest, $10.00 principal) | $990.00 | "about $28, $18 to the bank, $10 to the phone" |
| End of year 1 | $321.91 | $886.38 | "$320 paid, still owe $886" |
| End of year 2 | $622.02 | $769.99 | "$620 paid, still owe $770" |
| End of year 3 | $922.02 | $625.38 | "$920 paid, almost a whole phone; still owe $625" |
| Month 70 (5 yrs 10 mo) | $1,766.46 | $0 | "$1,766, almost two phones" (1.77x) |
| $100/month | $1,114.89, 12 months | $0 | "one year, about $115 interest" |
"Banks love" = framing: the $766 of interest is the issuer's revenue on this balance. The Minimum Payment Warning box is required by the CARD Act (Reg Z) and gives an estimate.
