# -*- coding: utf-8 -*-
"""Questions added to fill category gaps, plus multi-step calculation questions
calibrated against the client's existing intern paper (chained metrics, ACOS/TACOS,
working backwards from a target)."""
from testbank import mcq, num

NEW = [
# ---------------------------------------------- STRATEGIC MINDSET, intern level
mcq("N01", "", "You have 10,000 to spend for a local dentist and one week to prove it works. "
    "Which is the best use of the money?",
    ["Split it across Google, Meta, YouTube and Display to see which works",
     "Put it into search ads for high-intent terms like 'dentist near me' in a tight radius",
     "Run Instagram brand awareness ads to build recognition first",
     "Spend it all on one day to get maximum visibility"], 1,
    "One week and a small budget means capturing existing demand, not creating it. Spreading thin learns nothing."),
mcq("N02", "", "A client sells a 200 product and a 40,000 product. Which needs the longer "
    "consideration period, and what does that mean for advertising?",
    ["The 200 one, because more people buy it",
     "The 40,000 one — expect more touchpoints before purchase and don't judge on last-click alone",
     "Both are the same; price does not affect the buying process",
     "The 40,000 one, so you should stop advertising it"], 1,
    "Price drives consideration length, which drives how many touches you need and how you should measure."),
mcq("N03", "", "Your ad is getting lots of clicks but the client says the enquiries are from the wrong city. "
    "What is the most likely cause?",
    ["The ad copy is unclear",
     "The location targeting settings",
     "The budget is too high",
     "The landing page is slow"], 1,
    "Geography problems are almost always a settings problem, not a creative one."),
mcq("N04", "", "A brand has no website, only a phone number. What should you optimise for?",
    ["Website clicks",
     "Calls, using call ads and call tracking",
     "Impressions, to build awareness",
     "Do not advertise until they build a website"], 1,
    "Optimise for the conversion the business can actually receive."),
mcq("N05", "", "Two campaigns have the same CPL. One brings enquiries that close at 20%, the other at 5%. "
    "What should you do?",
    ["Nothing — the CPL is the same, so they perform equally",
     "Move budget towards the campaign that closes at 20%, because the real cost per customer is four times lower",
     "Pause both and rebuild",
     "Increase the budget on both equally"], 1,
    "The cheapest lead is not the cheapest customer. This is the single most important idea in lead gen."),
mcq("N06", "", "A client wants to advertise on every platform at once with a small budget. Your advice:",
    ["Agree — more reach means more sales",
     "Start on one or two where their customers clearly are, learn what works, then expand",
     "Refuse the work",
     "Split the budget equally so nothing is missed"], 1,
    "A small budget spread across five platforms produces five inconclusive tests."),
mcq("N07", "", "Why might you deliberately spend MORE per click on one keyword than another?",
    ["Because it has more search volume",
     "Because it converts better or brings higher-value customers, so it is worth more to you",
     "Because it is a longer phrase",
     "You should always pay the same per click"], 1,
    "Value, not volume, justifies the bid. Understanding this early separates good juniors from average ones."),
mcq("N08", "", "A campaign has been running for three days with 40 clicks and no conversions. "
    "The client wants to shut it down. What is the right response?",
    ["Agree — three days is enough to see it is not working",
     "Explain that 40 clicks is too small a sample to conclude anything, and agree what evidence would justify stopping",
     "Ignore them and keep it running",
     "Double the budget to get results faster"], 1,
    "Sample size, plus agreeing the stopping rule in advance instead of arguing about it later."),

# --------------------------------------- CALCULATION, intern level (multi-step)
num("N09", "", "Impressions 50,000. CTR 2%. CVR 5%. How many leads do you get?", 50,
    "50,000 x 2% = 1,000 clicks. 1,000 x 5% = 50 leads."),
num("N10", "", "Your target CPL is 400 and your conversion rate is 5%. "
    "What is the maximum CPC you can afford?", 20,
    "Max CPC = target CPL x CVR = 400 x 0.05 = 20."),
num("N11", "", "You need 300 leads. CVR is 3% and CPC is 25. What total budget do you need?", 250000,
    "300 / 0.03 = 10,000 clicks. 10,000 x 25 = 250,000."),
num("N12", "", "Campaign A: CPC 18, CVR 6%. What is the CPL?", 300,
    "CPL = CPC / CVR = 18 / 0.06 = 300."),

# ------------------------------------- CALCULATION, associate level (ACOS/TACOS)
num("N13", "", "Ad spend is 60,000 and ad-attributed revenue is 3,00,000. What is the ACOS, as a percentage?", 20,
    "ACOS = spend / ad revenue = 60,000 / 300,000 = 20%. It is the inverse of ROAS."),
num("N14", "", "Ad spend 60,000. Ad revenue 2,00,000. Organic revenue 3,00,000. "
    "What is the TACOS, as a percentage?", 12,
    "TACOS = ad spend / TOTAL revenue = 60,000 / 500,000 = 12%. It shows the true dependence on paid."),
num("N15", "", "Product price 1,200. Target ACOS 25%. CVR 4%. What is the maximum CPC you can afford?", 12,
    "Allowable cost per sale = 1,200 x 25% = 300. Max CPC = 300 x 4% = 12."),
num("N16", "", "Impressions 80,000. CTR 1.5%. CVR 4%. CPC 30. What is the CPA?", 750,
    "1,200 clicks, 48 conversions, spend 36,000. CPA = 36,000 / 48 = 750. Or simply CPC / CVR."),
num("N17", "", "CVR falls from 3% to 2% while CPC stays at 20. What is the new CPA?", 1000,
    "CPA = 20 / 0.02 = 1,000, up from 667. A one-point CVR drop raised CPA by half."),

# ------------------------------------------- STRATEGIC MINDSET, associate level
mcq("N18", "", "A client's CPL target is 500 and you are at 650, with a 2% conversion rate. "
    "Which combination is most likely to close the gap?",
    ["Raise bids by 30% to win more auctions",
     "Pause the weakest ad groups, tighten targeting, and work on landing page conversion rate",
     "Increase the budget to gather more conversion data",
     "Switch to an impression share bidding strategy"], 1,
    "CPL = CPC / CVR. With CVR at 2%, the biggest available lever is conversion rate, not the auction."),
mcq("N19", "", "Prospecting is at 2.2 ROAS on 1,00,000 spend; retargeting is at 6.0 on 30,000. "
    "Blended target is 3.0. What should you do?",
    ["Shift most of the budget into retargeting because its ROAS is higher",
     "Keep investing in prospecting — retargeting only converts demand that prospecting created, and it will not scale on its own",
     "Pause prospecting since it is below the 3.0 target",
     "Cut both budgets until efficiency improves"], 1,
    "Retargeting ROAS is borrowed from prospecting. Starving the top of the funnel collapses both within weeks."),
mcq("N20", "", "You have to choose ONE thing to fix on an account with weak CTR, weak CVR and weak AOV. "
    "How do you decide?",
    ["Fix them in the order they appear in the funnel",
     "Work out which one, if improved by a realistic amount, moves the business metric most",
     "Fix AOV because it affects revenue directly",
     "Fix whichever is furthest from the industry benchmark"], 1,
    "Prioritise by expected impact, not by position in the funnel or by distance from a benchmark."),
mcq("N21", "", "A client asks you to cut spend by 30% but keep lead volume flat. What is the honest answer?",
    ["Agree and try your best",
     "Say it requires a roughly 43% improvement in efficiency, name where that could realistically come from, and be clear about what is achievable in the timeframe",
     "Refuse, because it is impossible",
     "Agree, then explain later if it does not work"], 1,
    "Quantify what is being asked before answering it. Same volume on 70% of budget needs efficiency up by 1/0.7."),

# ------------------------------------------ THEORETICAL KNOWLEDGE, intern level
mcq("N22", "", "What is a 'bid' in an ad auction?",
    ["The amount you pay every time your ad is shown",
     "The maximum you are willing to pay for a click or an outcome",
     "The total budget for the campaign",
     "The price the platform charges for the ad slot"], 1,
    "A maximum, not a fixed price. You usually pay less than your bid."),
mcq("N23", "", "What does 'reach' mean, and how does it differ from impressions?",
    ["They are the same thing",
     "Reach is the number of unique people; impressions is the number of times ads were shown",
     "Reach is clicks; impressions is views",
     "Reach counts only people who engaged with the ad"], 1,
    "Impressions divided by reach gives frequency, which is why the distinction matters."),

# --------------------------------------------- CALCULATION, manager/senior level
num("N24", "", "AOV 4,000. Contribution margin 35%. Target is to make 500 profit per order after ad cost. "
    "What is the maximum CAC?", 900,
    "Contribution = 4,000 x 35% = 1,400. Less 500 target profit = 900 maximum CAC."),
num("N25", "", "Spend 3,00,000 at 4.0 ROAS. You add 1,00,000 more and total revenue becomes 14,00,000. "
    "What is the marginal ROAS on the additional spend?", 2,
    "Was 12,00,000. Now 14,00,000. (14,00,000 - 12,00,000) / 1,00,000 = 2.0 — half the average."),
num("N26", "", "A subscription product bills 800 a month at 70% margin, and the average customer stays "
    "9 months. What is the maximum CAC to break even on lifetime value?", 5040,
    "800 x 0.70 x 9 = 5,040."),
]
