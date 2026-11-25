import re
N,B,H,P="NARRATOR","BUCK","HAMLET","PAUSE"
S=[]  # (section, speaker, tag, text, source_key)
def sec(name): S.append(("SECTION",None,None,name,None))
def L(sp,text,tag="",src=None): S.append(("LINE",sp,tag,text,src))

sec("HOOK")
L(N,"When you tap buy on one dollar of Apple stock, Apple usually gets none of it.","HOOK")
L(N,"Your dollar goes somewhere else, and it passes through several companies on the way.")
L(N,"This video follows that one dollar from your pocket all the way to Wall Street.")
L(B,"I'm the dollar, and nobody asked me if I wanted to travel.","gag")
L(N,"By the end, you'll know exactly who ends up holding your dollar.","PROMISE 1")
L(N,"You'll also find out whose name is on your stock, and it probably isn't yours.","PROMISE 2")
L(H,"He was perfectly safe in here with me, and now he wants adventure.","gag")
L(N,"And you'll get three checks worth doing before you ever tap buy.","PROMISE 3")
L(N,"Once you see this route, the buy button won't look so simple again.")
L(N,"This trip has five stops, and it's one common route, since real orders can skip some.","",'routing')
L(B,"Five stops sounds like a lot of walking for one dollar.","gag")

sec("THE DEVICE · WHAT YOUR DOLLAR BUYS")
L(N,"Before the dollar moves, you need to know what it's actually buying.")
L(N,"Picture a company as a pizza that's been cut into slices.")
L(N,"Each slice is a small piece of ownership, and that slice is called a share.")
L(N,"The stock market is simply the place where people trade those slices.")
L(N,"Here's a simple example to show how slices work, with made-up numbers.","EXAMPLE")
L(N,"Say a pizza shop is worth one hundred dollars and is cut into one hundred slices.","EXAMPLE")
L(N,"Each slice is worth one dollar, so owning one slice means owning one percent.","EXAMPLE")
L(N,"If the shop grows to two hundred dollars, your slice is worth two dollars.","EXAMPLE")
L(N,"If the shop shrinks to fifty dollars, your slice is worth fifty cents.","EXAMPLE")
L(H,"Fifty cents is exactly why I keep my coins at home.","gag")
L(N,"Now comes the part where a price tag can fool you.")
L(N,"Say Company A's stock costs five hundred dollars a share, and Company B's costs five dollars.","EXAMPLE")
L(N,"The five-hundred-dollar share looks like the bigger company, and that's the trap.","EXAMPLE")
L(N,"Company A is cut into only three slices, so its whole pizza is worth fifteen hundred dollars.","EXAMPLE")
L(N,"Company B is cut into a million slices, so its whole pizza is worth five million.","EXAMPLE")
L(N,"The cheap slice came from the far bigger pizza.","EXAMPLE")
L(N,"Price times the number of shares is called market cap, the company's market value.")
L(N,"Apple is cut into roughly fifteen billion shares, which is how its value reaches trillions.","",'apple_shares')
L(B,"So I'm buying a crumb of a slice, and I'm still proud of it.","gag")

sec("STOP 1 · YOUR APP")
L(N,"Stop one is the investing app on your phone.")
L(N,"Say it's Tuesday morning, and you buy one dollar of Apple.","EXAMPLE")
L(N,"One Apple share costs a few hundred dollars, so your dollar buys a crumb.")
L(N,"Many big apps sell these crumbs, and they're called fractional shares.","",'fractional')
L(N,"You place a market order, which means buy right away at the available price.","",'market_order')
L(N,"The price you saw on screen can change before your order goes through.","",'market_order')
L(N,"Your broker may also bundle your crumb with other customers' orders before it buys.","",'fractional')
L(N,"Your broker can send that order to an exchange or a market maker, or fill it itself.","",'routing')
L(B,"I've been turned into paperwork, and nobody even said thank you.","gag")

sec("STOP 2 · THE MARKET MAKER")
L(N,"Stop two is a kind of company most people have never heard of.")
L(N,"Many retail orders don't go straight to a stock exchange.","",'pfof')
L(N,"Brokers often send them to a trading firm called a market maker instead.","",'pfof')
L(N,"Picture a currency booth at the airport, with one price to buy and one to sell.")
L(N,"A market maker works the same way, regularly posting a buy price and a sell price.","",'market_maker')
L(N,"Say it will buy Apple at two hundred fifty dollars and sell at two hundred fifty and two cents.","EXAMPLE")
L(N,"That two-cent gap is called the spread, and the market maker tries to earn it.","",'market_maker')
L(N,"It can lose money too, because the price can move against it a minute later.","",'market_maker')
L(N,"Citadel Securities says it executes about a third of all U.S. retail stock trading volume.","",'citadel')
L(N,"Market makers often pay brokers for sending them orders, which is called payment for order flow.","",'pfof')
L(N,"That's one reason many apps charge no commission on stock trades.","",'pfof')
L(N,"Your broker still has to try to get you the best available deal, considering price and how reliably the order can be filled.","",'best_ex')
L(H,"Everyone on this trip gets paid except the pig, apparently.","gag")
L(N,"If the market maker has the shares, it can sell them straight from its own inventory.","",'market_maker')
L(N,"If it doesn't, your order can head to stop three.")

sec("STOP 3 · THE EXCHANGE")
L(N,"Stop three is the stock exchange, the place most people picture when they hear Wall Street.")
L(N,"The New York Stock Exchange still rings its opening bell on Wall Street at nine thirty in the morning, Eastern time.","",'nyse_hours')
L(N,"The computers that match its trades sit in a data center in Mahwah, New Jersey.","",'nyse_mahwah')
L(N,"Nasdaq's main U.S. data center sits in Carteret, New Jersey.","",'nasdaq_carteret')
L(B,"I came all this way for Wall Street, and I got New Jersey.","gag")
L(N,"An exchange works like a matchmaker that keeps two lists.")
L(N,"One list holds buyers, and the other list holds sellers.")
L(N,"When a buyer and a seller agree on a price, the exchange matches them.")
L(N,"Regular trading runs from nine thirty to four, Eastern time, Monday through Friday.","",'nyse_hours')
L(N,"Market holidays and a few early-close days are the exceptions.","",'nyse_hours')
L(N,"Some apps let you trade earlier or later, when far fewer people are trading.","",'extended')
L(N,"Fewer traders can mean bigger price jumps and a wider gap between buy and sell prices.","",'extended')

sec("CHECKPOINT 1")
L(N,"Quick check, because look at how far your dollar has already come.","CHECKPOINT 1")
L(N,"Stop one turned your dollar into an order inside your app.","CHECKPOINT 1")
L(N,"Stop two was a market maker, which may sell to you from its own shelf.","CHECKPOINT 1")
L(N,"Stop three was an exchange, which matches buyers with sellers.","CHECKPOINT 1")
L(N,"The next stop is where your dollar actually changes hands.","RE-HOOK")

sec("STOP 4 · THE SELLER")
L(N,"Pick how much of your dollar Apple gets, all of it, half, or none.","QUIZ")
S.append(("LINE",P,"QUIZ","3 seconds. On screen: \"Pick how much of your dollar Apple gets, all of it, half, or none.\"",None))
L(N,"Usually none of it, because Apple isn't the one selling you the share.","PROMISE 1",'secondary')
L(N,"Think of a concert ticket that gets resold between fans.")
L(N,"The band gets paid when the box office sells the ticket the first time.")
L(N,"When you buy that ticket later from another fan, your money goes to the fan.")
L(N,"Apple's box-office moment came when it first sold shares to the public.","",'apple_ipo')
L(N,"That happened on December twelfth, nineteen eighty, at twenty-two dollars a share.","",'apple_ipo')
L(N,"Today, your dollar goes to whoever sold you the share.","",'secondary')
L(N,"It could be your own broker, a market maker, a big fund, or a retired teacher.","",'routing')
L(N,"Say the retired teacher is selling a little stock to help pay for a new roof.","EXAMPLE")
L(B,"Tell her I'll pay for the roof myself, so she doesn't have to sell.","gag")
L(N,"Your dollar buys a crumb of her stock, so your dollar ends up helping pay for that roof.","EXAMPLE")
L(N,"Promise one, done, because your dollar went to the seller, not to Apple.","PROMISE 1 (closed)")
L(N,"Apple still cares about its price, partly because its executives are often paid in stock.")

sec("STOP 5 · MAKING IT OFFICIAL")
L(N,"Stop five is where your trade becomes official.")
L(N,"Your trade is matched, but the paperwork isn't finished yet.")
L(N,"Since May twenty-eighth, twenty twenty-four, most U.S. stock trades settle one business day later.","",'t1')
L(N,"That means your Tuesday trade is usually final on Wednesday.","",'t1')
L(N,"Behind the scenes, companies in a group called the D-T-C-C clear and settle the trade.","",'dtcc')
L(N,"They guarantee eligible trades, work out what each firm owes, and hold the shares.","",'dtcc')
L(H,"A referee for money is the first sensible thing I've heard today.","gag")
L(N,"Now for the paperwork promise from the start of this video.","PROMISE 2")
L(N,"Many shares held through brokerages are registered under one name, Cede and Company.","",'cede')
L(N,"Cede and Company is the name the Depository Trust Company uses on the official record.","",'cede')
L(N,"It's a bit like a coat check at a restaurant.")
L(N,"The hanger tag doesn't have your name, but your ticket proves the coat is yours.")
L(N,"Your brokerage's records are that ticket, and they list you as the beneficial owner.","",'cede')
L(N,"Promise two, done, because the name on the record isn't yours, but the shares are.","PROMISE 2 (closed)")
L(N,"The gains are yours, and so are the losses.")
L(N,"Voting with a fractional share depends on your broker's rules.","",'voting')

sec("CHECKPOINT 2")
L(N,"Quick check before the big part, because the whole route is on the map now.","CHECKPOINT 2")
L(N,"Your dollar became an order, took one possible route, and reached a seller.","CHECKPOINT 2")
L(N,"It settled a business day later, with Cede and Company on the record.","CHECKPOINT 2")
L(N,"The order itself can go through in a fraction of a second, and settlement follows a business day later.","CHECKPOINT 2",'t1')
L(N,"Now comes the part that matters most, which is how one dollar turns into more dollars.","RE-HOOK")

sec("HOW A SHARE MAKES MONEY")
L(N,"There are two main ways to make money from owning a stock.")
L(N,"The first is selling for more than you paid.")
L(N,"Here's a made-up example to show how that works.","EXAMPLE")
L(N,"Say Maya buys ten shares at two hundred dollars each, which costs two thousand dollars.","EXAMPLE")
L(N,"A year later, Jordan offers two hundred fifty dollars a share for all ten.","EXAMPLE")
L(N,"Maya sells and makes five hundred dollars, before taxes and any fees.","EXAMPLE")
L(N,"If Jordan had offered one hundred fifty dollars a share, Maya would have lost five hundred.","EXAMPLE")
L(N,"The second way is dividends, when a company shares part of its profits with its owners.","",'dividends')
L(N,"Not every company pays dividends, and the ones that do can cut them.","",'dividends')
L(H,"Dividends sound like savings that pay you rent, and I approve.","gag")
L(N,"The price you usually see is the last-traded price, the last price someone actually paid.","",'last_trade')
L(N,"Say Apple's last trade was two hundred fifty dollars even.","EXAMPLE")
L(N,"The cheapest seller wants two hundred fifty dollars and five cents, and a buyer pays it.","EXAMPLE")
L(N,"The last-trade price now becomes two hundred fifty dollars and five cents.","EXAMPLE")
L(N,"Millions of small deals like that, every day, are what make a stock chart move.")
L(N,"Prices mostly move on what buyers and sellers expect a company to earn later.")
L(N,"Good news can lift a price in minutes, and bad news can sink it.")
L(N,"In his nineteen eighty-seven letter, Warren Buffett passed on a lesson from his teacher, Benjamin Graham.","",'buffett')
L(N,"In the short run, the market is a voting machine, but in the long run it is a weighing machine.","",'buffett')
L(N,"Day to day, prices follow moods, and over many years they tend to follow profits.")

sec("TODAY · THE BASKET")
L(N,"Picking single companies isn't the only way to own stocks.")
L(N,"An S and P five hundred index fund is a basket holding slices of about five hundred companies.","",'index_fund')
L(N,"You buy a slice of the fund, and the fund owns the companies for you.","",'index_fund')
L(N,"The biggest companies get the biggest weight inside the basket.","",'index_fund')
L(B,"I'm spread across five hundred companies now, and I've never felt so thin.","gag")
L(H,"A basket holding five hundred companies is the first investment I'd happily sit in.","gag payoff")
L(N,"Over long periods, the S and P five hundred has historically returned roughly ten percent a year.","",'sp_return')
L(N,"That's with dividends reinvested and before inflation, and it's history, not a promise.","",'sp_return')
L(N,"Here's what a steady ten percent a year would do to one dollar.","EXAMPLE")
L(N,"After forty years of steady ten percent growth, one dollar becomes about forty-five dollars.","EXAMPLE",'math45')
L(N,"Real markets don't move in a straight line, and the drops can be brutal.")
L(N,"From late two thousand seven to early two thousand nine, the S and P five hundred lost more than half its value.","",'crash2008')
L(N,"In twenty twenty, it fell almost thirty-four percent between February nineteenth and March twenty-third.","",'crash2020')
L(N,"The broad index came back both times, but a single company doesn't always come back.","",'crash2020')
L(H,"This is exactly why I sleep with one eye open.","gag")

sec("THREE CHECKS BEFORE YOU TAP BUY")
L(N,"Here are the three checks worth doing before you ever tap buy.","PROMISE 3")
L(N,"Check one is the size of the company, not just the price of one share.","CHECK 1")
L(N,"Price times shares is the number that tells you how big the pizza really is.","CHECK 1")
L(N,"Check two is how your order works, since a market order takes the available price.","CHECK 2",'market_order')
L(N,"Your app should explain its order types and how it routes your orders.","CHECK 2",'rule606')
L(N,"Check three is whether your brokerage is an S-I-P-C member, and what that covers.","CHECK 3",'sipc')
L(N,"If a member firm fails with customer assets missing, S-I-P-C can help recover them.","CHECK 3",'sipc')
L(N,"Protection goes up to five hundred thousand dollars per customer, including two hundred fifty thousand in cash.","CHECK 3",'sipc')
L(N,"That protection is for a failed brokerage, not for a stock that falls.","CHECK 3",'sipc')
L(B,"Nobody insures my feelings either, and I've been through a lot today.","gag")
L(H,"These checks keep money safe, which makes this the only list I trust.","gag")
L(N,"That's promise three, and notice that none of these checks tells you what to buy.","PROMISE 3 (closed)")

sec("ENDING")
L(N,"The whole trip is on the map now, from your pocket to a retired teacher's new roof.","CALLBACK")
L(N,"Apple never got your dollar, but you now own a tiny piece of Apple.","CALLBACK")
L(N,"Before I ask you something, I'll go first with my own story.")
L(N,"The first stock I ever bought was Nvidia, one of the biggest companies in the market.")
L(N,"I picked it because I think it's tied to where the world is heading, and that's my reason, not advice.")
L(N,"The first time I opened a candlestick chart, I was completely lost.")
L(N,"I started learning about money because I want to be financially free.")
L(B,"I offered to pay for that roof, and somehow I ended up inside it.","gag payoff")
L(N,"Next time, we'll break down how to read a candlestick chart without getting lost.","NEXT VIDEO")
L(N,"Tell me in the comments which stop surprised you most, and what your first stock was.","COMMENT PROMPT")
L(N,"If this made the stock market make more sense, a like really helps the channel.","OUTRO")

SOURCES={
 'apple_shares':("Apple has roughly fifteen billion shares outstanding; at about $354 a share that's roughly $5.3 trillion","Apple Form 10-K / 10-Q cover page (shares outstanding); share count and ~$354 price confirmed by the creator, Nov 2026","https://investor.apple.com/sec-filings/","✅ (Nov 2026)"),
 'fractional':("Fractional shares; brokers may bundle fractional orders","SEC Investor.gov, Investor Bulletin: Fractional Share Investing","https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/investor-bulletin-fractional-share-investing","✅"),
 'market_order':("Market order buys at the available price; price can change before execution","SEC Investor.gov, Market Order","https://www.investor.gov/introduction-investing/investing-basics/glossary/market-order","✅"),
 'pfof':("Many retail orders routed to market makers; payment for order flow; no-commission apps","SEC Investor.gov, Payment for Order Flow","https://www.investor.gov/introduction-investing/investing-basics/glossary/payment-order-flow","✅"),
 'market_maker':("Market makers quote buy and sell prices, earn the spread, carry inventory risk","SEC Investor.gov, Market Maker","https://www.investor.gov/introduction-investing/investing-basics/glossary/market-maker","✅"),
 'citadel':("Citadel Securities executes about a third (approx. 35%) of U.S.-listed retail volume","Citadel Securities, 1H 2026 Market Structure & Flows","https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/1h-2026-market-structure-flows/","✅"),
 'routing':("Orders can go to an exchange, to a market maker, or be filled internally by the broker; brokers can fill fractional orders as principal","SEC Investor.gov, Executing an Order; SEC Rule 605 FAQ","https://www.investor.gov/introduction-investing/investing-basics/how-stock-markets-work/executing-order ; https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/frequently-asked-questions-rule-605-regulation-nms","✅"),
 'best_ex':("Broker's duty to seek best execution: price, speed, likelihood of execution","SEC Investor.gov, Best Execution","https://www.investor.gov/introduction-investing/investing-basics/glossary/best-execution","✅"),
 'nyse_hours':("NYSE opens 9:30 a.m. ET; regular hours 9:30-4:00 Mon-Fri, except holidays and early closes","NYSE, Holidays and Trading Hours","https://www.nyse.com/markets/hours-calendars","✅"),
 'nyse_mahwah':("NYSE trading systems in Mahwah, New Jersey","NYSE (per creator's fact-check)","https://www.nyse.com/","✅"),
 'nasdaq_carteret':("Nasdaq's primary U.S. data center in Carteret, New Jersey","Nasdaq (per creator's fact-check)","https://www.nasdaq.com/","✅"),
 'extended':("Extended-hours trading: less liquidity, wider spreads, bigger price swings","SEC Investor.gov, Extended-Hours Trading","https://www.investor.gov/introduction-investing/investing-basics/glossary/extended-hours-trading","✅"),
 'apple_ipo':("Apple IPO December 12, 1980 at $22 a share","Apple Investor Relations FAQ","https://investor.apple.com/faq/default.aspx","✅"),
 'secondary':("Secondary-market trades pay the seller, not the issuing company","SEC Investor.gov","https://www.investor.gov/introduction-investing/investing-basics/how-stock-markets-work","✅"),
 't1':("T+1 settlement since May 28, 2024","SEC Investor.gov, New T+1 Settlement Cycle investor bulletin","https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/new-t1-settlement-cycle-what-investors-need-know-investor-bulletin","✅"),
 'dtcc':("DTCC group: NSCC clears and guarantees eligible trades; DTC settles and holds securities; netting","DTCC","https://www.dtcc.com/","✅"),
 'cede':("Cede & Co. is DTC's nominee registered owner; brokerage records show the beneficial owner","SEC Investor.gov, Holding Your Securities","https://www.investor.gov/introduction-investing/investing-basics/how-stock-markets-work/holding-your-securities","✅"),
 'voting':("Fractional-share voting depends on the broker (e.g. Robinhood aggregates; Schwab generally doesn't)","Robinhood / Schwab help pages (per creator's fact-check)","https://robinhood.com/us/en/support/","✅"),
 'sipc':("SIPC: up to $500,000 per customer incl. $250,000 cash, for missing assets at a failed member firm; not market losses","SIPC, What SIPC Protects; Investors with Multiple Accounts (separate account capacities can qualify separately)","https://www.sipc.org/for-investors/what-sipc-protects ; https://www.sipc.org/for-investors/investors-with-multiple-accounts","✅"),
 'dividends':("Dividends are discretionary and can be cut","SEC Investor.gov, Dividend","https://www.investor.gov/introduction-investing/investing-basics/glossary/dividend","✅"),
 'last_trade':("Displayed price is usually the last-traded price (can be delayed or bid/ask)","SEC Investor.gov","https://www.investor.gov/","✅"),
 'buffett':("Graham's voting machine / weighing machine line in Buffett's 1987 letter","Berkshire Hathaway 1987 Chairman's Letter","https://www.berkshirehathaway.com/letters/1987.html","✅"),
 'index_fund':("Index fund owns the companies; buyers own fund shares; cap-weighted","SEC Investor.gov, Index Funds","https://www.investor.gov/introduction-investing/investing-basics/glossary/index-funds","✅"),
 'sp_return':("S&P 500 about 10.6% a year 1957-2025, dividends reinvested, before inflation","Aswath Damodaran, NYU Stern historical returns","https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html","✅"),
 'math45':("$1 x 1.10^40 = $45.26","Calculation","—","✅"),
 'crash2008':("S&P 500 fell about 57% from October 2007 to March 2009","S&P Dow Jones Indices / AAII","https://www.aaii.com/","✅"),
 'crash2020':("S&P 500 fell 33.8% from February 19 to March 23, 2020; index later recovered","AAII (per creator's fact-check)","https://www.aaii.com/","✅"),
 'rule606':("Brokers publish order-routing disclosures (SEC Rule 606)","SEC Investor.gov, order routing","https://www.investor.gov/","✅"),
}

def words(t): return len(re.findall(r"[A-Za-z0-9'’-]+",t))
out=["# Follow $1 From Your Pocket to Wall Street (v2, format-guide rewrite)","",
"Rewritten in the format from `docs/script-format-guide.md`. Spoken words only, plus `[SOURCE: …]` tags for the on-screen source captions. Facts come from the fact-checked v1 script; see `factcheck.md`.","",
"Voices: NARRATOR = Yaboy · BUCK = Larry (the dollar on the trip) · HAMLET = Grampa Werthers (the piggy bank the dollar left behind).",""]
n=0; total=0; fact_rows=[]; seen=set(); counts={N:0,B:0,H:0}
for kind,sp,tag,text,src in S:
    if kind=="SECTION": out+=[f"## {text}",""]; continue
    if sp==P:
        out+=[f"[PAUSE: {text}]",""]; total+=3; continue
    n+=1; sid=f"S{n:03d}"; w=words(text); secs=max(2,round(w/3)); total+=w/3; counts[sp]+=1
    head=f"**{sid} · {sp} · ~{secs} s" + (f" · {tag}" if tag else "") + "**"
    out+=[head,text]
    if src:
        cl,name,url,ok=SOURCES[src]; out.append(f"[SOURCE: {name}]")
        fact_rows.append((sid,cl,name,url,ok))
    out.append("")
out+=["---","","**End screen (on screen, small):** Not financial advice. For education only.",""]
open('/home/user/G/scripts/long-form/01-follow-one-dollar-v2/script.md','w').write("\n".join(out))
fc=["# Fact-check table: Follow $1 (v2)","","| Line | Claim | Source | URL | ✅ |","|---|---|---|---|---|"]
for sid,cl,name,url,ok in fact_rows: fc.append(f"| {sid} | {cl} | {name} | {url} | {ok} |")
open('/home/user/G/scripts/long-form/01-follow-one-dollar-v2/factcheck.md','w').write("\n".join(fc)+"\n")
allw=sum(words(t) for k,sp,_,t,_ in S if k=="LINE" and sp!=P)
lens=[words(t) for k,sp,_,t,_ in S if k=="LINE" and sp!=P]
print(f"{n} lines, {allw} words, ~{total/60:.1f} min at 180 wpm incl. pause; voices {counts}")
print("over 14 words:",sum(1 for x in lens if x>14),"| over 20:",[ (i+1,x) for i,x in enumerate(lens) if x>20])
txt=" ".join(t for k,sp,_,t,_ in S if k=="LINE" and sp!=P)
print("questions:",txt.count("?"),"| digits/symbols:",re.findall(r"\S*[0-9$%&]\S*",txt) or "none")
