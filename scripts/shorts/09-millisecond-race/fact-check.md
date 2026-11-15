# Fact-check: The $300 Million Cable (checked Nov 15, 2026; revised with outside review)

| Claim (as spoken) | Status | Source |
|---|---|---|
| About $300M, Chicago to New Jersey, straightest path | Verified (reported cost) | Spread Networks: route unveiled June 2010 to Carteret, NJ (Nasdaq data center), reported ~$300M build; about 825 miles, chose the shortest path instead of rail rights-of-way (Wikipedia, Waters Technology, Lightwave) |
| "to make trades a blink faster" | OK | Built for low latency between Chicago and NJ exchanges |
| 2010, round trip about 13 thousandths of a second | Verified | 13.33 ms quoted at launch; ~13 ms later; 12.98 ms after 2012 upgrades |
| Microwave towers beat it; air faster than glass | Verified | Microwave Chicago-NJ ~8.2 ms round trip (McKay Brothers); light slows in glass (refractive index), near light speed in air; Duke/Yale/UIUC/ETH study |
| Sold for about $127M by 2017 | Verified | Zayo agreed in 2017 to acquire Spread Networks for $127M cash |
| Some exchanges give every customer the same cable length, extra coiled | Verified | Cboe/Equinix latency equalization (equal fiber length to each cage, slack stored on Cboe side); CME GLink equidistant cables |
| Holding for years, a blink doesn't matter | Opinion framed as lesson | Not a claim about HFT costs or benefits |

Not used (kept for the description or a part 2): IEX speed bump, a coil of ~38 miles of fiber (now ~44 miles) adding 350 microseconds on purpose.
Avoided: "saved 3 milliseconds" (prior-route baseline not verified); "tunnel" (it was a buried fiber route, not a tunnel); "HFT made trading cheaper" (debated).
Description note: "Spread Networks' Chicago-NJ fiber (2010), reported ~$300M; sold to Zayo for $127M (2017). Not financial advice."

## Revision (outside review, confirmed)
- Hook: "an estimated $300M ... to save 3 milliseconds": Forbes (Sep 27, 2010, Christopher Steiner) reported 825 miles, 13.3 ms round trip, about 3 ms faster than the previous fastest route; cost estimated toward $300M; Spread declined to disclose. Say "estimated".
- Line 3: "can react ... before a rival's order gets there" (not a guarantee of trading first).
- Line 4: 13.33 ms quoted at launch -> "about 13 milliseconds".
- Microwave: industry paper 8.2-9.0 ms round trip by route. Correction to the first draft: heavy rain or snow can disrupt microwave links enough to erase the speed advantage (not "faster even in bad weather"); the script makes no weather claim.
- Sale: Zayo announced the $127M cash deal Nov 27, 2017, closed Feb 28, 2018. Script states the price only; it does not compare it with the build cost or say microwave caused the sale.
- Cable lengths: Cboe documents equal optical lengths (fiber spools) at its NY4/NY5 Secaucus, NJ connections; CME equidistant access is at Aurora, IL (not NJ), so the line names Cboe only.
- Whiteboard: show "3 ms saved" across old vs new route, then "13.33 ms round trip" on the new route alone, so the two numbers never blur.
