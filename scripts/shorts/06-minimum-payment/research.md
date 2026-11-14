# Research: Why Paying the Minimum Costs You More

Checked November 14, 2026. A worked example.

## Example
$1,000 phone bought on a credit card; no new purchases; 22% APR; monthly interest = balance x 22% / 12 (real cards use a daily rate, a small difference); typical minimum = the larger of $25 or 1% of the balance plus that month's interest. Simulated in Python.

| Plan | Months | Interest | Total paid |
|---|---|---|---|
| Minimum only | 70 (about 5.8 years) | $766.46 | $1,766.46 |
| $50 a month | 26 | $257.14 | $1,257.14 |
| $100 a month | 12 | $114.89 | $1,114.89 |
| Minimum with a $40 floor (some issuers, e.g. Chase) | 34 | $349.98 | $1,349.98 |

First minimum payment: $28.33 = $18.33 interest + $10.00 toward the balance.

## Facts
- **APR:** Federal Reserve G.19, Q3 2026: 21.19% average across all accounts, 22.36% on accounts assessed interest (people carrying a balance). Script says "about twenty-two percent".
- **Minimum formula:** most issuers use a small percentage of the balance (often 1%) plus that cycle's interest and fees, with a floor around $25 to $40; it varies by card (Chase states $40 or 1% plus interest and fees). Script says "on a typical card".
- **CARD Act (2009):** statements must show how long paying only the minimum would take and the total cost, plus the monthly payment to clear it in 36 months. Assumes no new purchases.

## Sources
- https://www.lendingtree.com/credit-cards/study/average-credit-card-interest-rate-in-america/
- https://www.cronista.com/en/finance/households-under-pressure-credit-card-debt-is-rising-in-the-us-how-to-lower-your-interest-rate/
- https://www.chase.com/personal/credit-cards/education/basics/how-to-calculate-your-minimum-credit-card-payment
- https://www.nerdwallet.com/credit-cards/learn/credit-card-minimum-payment-keep-rising
- https://www.consumerfinance.gov/ask-cfpb/a-box-on-my-credit-card-bill-says-that-i-will-pay-off-the-balance-in-three-years-if-i-pay-a-certain-amount-what-does-that-mean-do-i-have-to-pay-that-much-if-i-pay-that-much-and-make-new-purchases-will-i-still-owe-nothing-after-three-years-en-36/
- https://consumercomplianceoutlook.org/2010/first-quarter/regulation-z-rules/
