# Research: Why the Friend Who Quit Ended Up Richest (Money Ladder)

A worked example, not a real story. All four friends save $100 a month starting at age 22 and are checked at 62.
Monthly contributions, monthly compounding (annual rate / 12), computed in Python on November 13, 2026.

| Friend | Plan | Put in | Value at 62 |
|---|---|---|---|
| 1 | Cash under the mattress, 22 to 62 (480 months) | $48,000 | $48,000 |
| 2 | Savings account at 4% a year, 22 to 62 | $48,000 | $118,196 |
| 3 | Index fund at 10% a year, starting at 32, 30 years (360 months) | $36,000 | $226,049 |
| 4 | Index fund at 10% a year, 22 to 32 (120 months), then no more deposits, left to grow to 62 | $12,000 | $406,359 |

For reference, 40 years at 10% would be $632,408 (not used in the script).

## Rates
- **10% a year:** the stock market's long-run average. The S&P 500 returned about 10.6% a year with dividends reinvested from 1957 through 2025, before inflation (Aswath Damodaran, NYU Stern annual data); after inflation, roughly 6.5%. Never guaranteed; real returns vary a lot year to year. (Same source as `scripts/shorts/01-one-dollar-owns-the-world/research.md`.)
- **4% a year:** an illustrative savings-account rate. Actual rates change; the script presents it as "a savings account paying four percent", not a current quote.

## Concept
- **Compound interest/growth:** returns earn returns, so money invested earlier has more years for growth to build on itself.
