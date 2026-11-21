# Fact-check: Pause on a Stock (Nov 21, 2026)

Window: $1,000 at the 12/31/2020 close -> value at the 12/31/2025 close, dividends reinvested, splits adjusted (5-year total return).
Method: calendar-year total returns 2021-2025 chained in Python; cross-checked against split-adjusted closing prices (within 0.5% for non-dividend payers; dividend payers higher by about their yield).
Main source: totalrealreturns.com nominal annual returns (dividends reinvested); second source chartrow.com where available; closing prices from Macrotrends, financialcontent, StockAlarm, SPDR GLD fact sheet, Coca-Cola investor relations.

| Box | 2021 | 2022 | 2023 | 2024 | 2025 | $1,000 -> | Confidence |
|---|---|---|---|---|---|---|---|
| NVDA (wildcard) | +125.48% | -50.3% | +239.02% | +171.2% | +38.92% | $14,313 | High |
| PLTR | -22.68% | -64.74% | +167.45% | +340.48% | +135.03% | $7,549 | High |
| XOM | +57.58% | +87.46% | -6.26% | +11.26% | +15.98% | $3,573 | Medium-high |
| JPM | +27.75% | -12.64% | +30.63% | +44.29% | +37.27% | $2,888 | Medium-high |
| META | +23.13% | -64.22% | +194.13% | +66.05% | +13.09% | $2,433 | Medium-high |
| AMD | +56.91% | -54.99% | +127.59% | -18.06% | +77.30% | $2,335 | High |
| GLD | -4.15% | -0.77% | +12.69% | +26.66% | +63.68% | $2,222 | High |
| QQQ | +27.42% | -32.58% | +54.86% | +25.58% | +20.77% | $2,018 | High |
| SPY | +28.73% | -18.18% | +26.18% | +24.89% | +17.72% | $1,954 | High |
| TSLA | +49.76% | -65.03% | +101.72% | +62.52% | +11.36% | $1,912 | High |
| NFLX | +11.41% | -51.05% | +65.11% | +83.07% | +5.19% | $1,734 | High |
| KO | +11.37% | +10.61% | -4.43% | +8.88% | +15.60% | $1,482 | High |
| PFE | +66.69% | -10.41% | -41.26% | -2.22% | +0.65% | $863 | Medium (Pfizer's proxy shows 2024 TSR -5.3% vs -2.22%; either way it lost money) |
| DIS | -14.51% | -43.91% | +4.26% | +24.44% | +3.30% | $643 | Medium-high |
| SPCX (since IPO) | IPO $135 (June 12, 2026) | | | | last found close $137.36 (Nov 16, 2026) | about $1,017 | Update on publish day |

Script claims:
- "Nvidia about fourteen thousand": $14,313. OK
- "Palantir about seventy-five hundred": $7,549. OK
- "Exxon beat Tesla, Meta and Netflix": $3,573 vs $1,912 / $2,433 / $1,734. OK
- "Pfizer and Disney, you lost money": $863, $643. OK (even with the Pfizer 2024 discrepancy, still below $1,000)
- "SpaceX since its June IPO, basically flat": $135 -> $137.36 = +1.7%. RE-CHECK the price on posting day.
- "S&P 500 box about nineteen fifty": SPY $1,954. OK. Note: 8 of the 13 five-year boxes beat SPY, 5 didn't, so the script asks "how many of your three beat it", not "the S&P beat most".

To verify before showing on screen: 2020 starting prices and the META/JPM/PFE/DIS 2025 closes came partly from memory in the research pass; boxes show only "$1,000 -> $X" (the chained totals), not raw prices, unless re-checked.

Caption disclaimer: "Historical results, not predictions. $1,000 invested 12/31/2020, valued 12/31/2025, dividends reinvested, no fees or taxes. SpaceX shown since its June 12, 2026 IPO. Not financial advice."

## Added: PTON (Peloton), Nov 21, 2026
$1,000 at the 12/31/2020 close ($151.72; CMC Markets, AverageAnnualReturn) -> 12/31/2025 close ($6.16; Stock Analysis, Stock Titan). No dividends, no splits. 1000 x 6.16 / 151.72 = $40.60 -> shown as "$41". High confidence.
