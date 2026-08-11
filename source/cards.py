# -*- coding: utf-8 -*-
"""One-page interviewer cards + process SOP. Self-teaching: no prior reading required."""

# (id, question, listen for, red flag)
INTERN = [
("1","Tell me about something in marketing you taught yourself in the last month. Where did you apply it?",
 "Specific source, specific application","Vague; nothing from the last month"),
("2","Walk me through: spend 50,000, 1,000 clicks, 40 conversions. CPC and CPA? (out loud)",
 "50 and 1,250, calmly, self-checks","Freezes; unit errors"),
("3","What's the difference between a keyword and a search term?",
 "Bid on vs actually typed","Says they're the same"),
("4","Pick any product you use daily. Who's the customer and what would you test first?",
 "Customer before ad; ONE clear test","Lists features; wants to test five things"),
("5","You're given an unclear task and your manager is in meetings all day. What do you do?",
 "Attempts it, writes down specific questions, asks once","Waits; or guesses on something big"),
("6","Tell me about feedback that stung. What did you do with it?",
 "Real example, no defensiveness, changed behaviour","Can't recall any; reframes as other's fault"),
("7","What part of a marketing job do you think you'd dislike?",
 "Something real, and how they'd still do it well","'Nothing, I'd love it all'"),
("8","What should I have asked you that I didn't?",
 "Reveals their real strength or worry","'Nothing'"),
]

ASSOCIATE = [
("1","Describe a campaign you built end to end. Structure, keywords, negatives, bidding — walk me through the settings.",
 "Settings-level detail, not summary","Stays general at every follow-up"),
("2","What do you do with the search terms report each week?",
 "Promote converters, add negatives, spot intent drift","Never opens it"),
("3","CPA is rising but CPC is flat. What does that tell you?",
 "CVR has fallen — problem is after the click","Says lower the bids"),
("4","What's the Meta learning phase and how do you avoid living in it?",
 "~50 events/ad set/week; consolidate, stop editing","Doesn't know; edits daily"),
("5","Conversions dropped 40% week on week. First five checks, in order?",
 "Tracking and change history FIRST","Jumps to bids or blames algorithm"),
("6","Tell me about a mistake that cost a client money. What did you do in the first hour?",
 "Disclosed immediately; added a control","Never made one; blames a tool"),
("7","What's your personal QA before you hand something over?",
 "An actual checklist they use every time","'I just double-check it'"),
("8","How do you feel about negative lists, naming conventions, weekly pacing checks?",
 "Reliability is the job; has a system","Treats it as beneath them"),
]

MANAGER = [
("1","A client's MER fell from 3.2 to 2.4 while platform ROAS held at 4.0. Explain it to the founder.",
 "Marginal vs average return; double counting","Says performance is fine because ROAS held"),
("2","How do you derive a target ROAS from the client's P&L?",
 "AOV → COGS/fees → contribution margin → 1/CM","Uses the number the client always used"),
("3","Client says 60% of leads are junk. Your plan?",
 "Define junk, sample, fix at source, move to CPQL","'That's the sales team's problem'"),
("4","Would you run PMax for lead gen? Argue both sides.",
 "Conditions it: brand exclusions, OCI, lead scoring","Blanket yes or blanket no"),
("5","How do you prove your ads caused the sales?",
 "Geo holdout, lift test, brand holdout","Points at the ROAS column"),
("6","If CPL misses target this month, who's accountable and what does that look like?",
 "Takes it; knew early, told early, has a plan","Distributes blame across four parties"),
("7","A client demands a 50% CPL cut in 30 days. You think it's impossible. How does that go?",
 "States constraint, offers real trade-off, in writing","Says yes; or refuses flatly"),
("8","You're asked to present numbers that flatter performance. What do you do?",
 "Declines clearly, offers honest framing","Agrees, or can't locate the line"),
]

SENIOR = [
("1","Spend went 20L→28L, revenue 70L→84L. Break-even ROAS is 2.5. Keep the extra spend?",
 "Marginal ROAS 1.75 — no. Average hides it","Says yes because average is 3.0"),
("2","A client at 85% non-brand impression share wants to double spend. What do you tell them?",
 "No headroom on search; names where growth comes from","Promises linear scaling"),
("3","You inherit 6 accounts, 2 at renewal risk, team of 4. First 30 days — and what will you NOT do?",
 "Diagnoses first; names what he won't do","Generic 30/60/90; promises everything"),
("4","Your biggest client is 40% of revenue and over-serviced. First move?",
 "Audit where hours go, then scope or fee","Asks to hire immediately"),
("5","A manager is technically strong but defensive with clients. What do you do?",
 "Observed calls, specific evidence, timeline","Removes from client contact, or tolerates it"),
("6","Describe a hire that didn't work out. What did you miss in the interview?",
 "Owns the missed signal; changed the process","Blames the candidate entirely"),
("7","What process have you built that's still used after you stopped enforcing it?",
 "Specific artefact; explains why it survived","Nothing; or a doc nobody opened"),
("8","In a pitch, you don't know the answer in front of the prospect. What do you say?",
 "Says so, says how he'd find out, follows up","Bluffs; deflects"),
]

CARDS = [
("Intern", INTERN, "45 min",
 "Learning agility (20%) · Numeracy (15%) · Problem solving (15%) · Attitude (8%)",
 "Would this person teach themselves something useful in a week with no instructions?",
 "Skill is not the point at this level. You are buying curiosity and arithmetic. If Q1 and Q2 are weak, "
 "the rest of the interview will not save it."),
("Associate", ASSOCIATE, "60 min",
 "Google Ads craft (20%) · Meta craft (15%) · Measurement (15%) · Diagnosis (13%) · Ownership (10%)",
 "Would you let them make live changes next month with one review — and trust them to tell you if they broke something?",
 "Push every claim to settings level. Someone who did the work gets MORE specific under questioning; "
 "someone who watched it happen gets more general."),
("Manager", MANAGER, "60 min",
 "Google (15%) · Meta (12%) · Measurement (13%) · Commercial (14%) · Diagnosis (13%) · Client handling (12%) · Ownership (10%)",
 "Would you give them an account and go on leave for two weeks — and would the client be calmer or more anxious?",
 "The commercial questions (Q1, Q2) separate a manager from a senior associate more reliably than any platform question. "
 "Push back once on a correct answer and watch what happens."),
("Sr. Manager", SENIOR, "60 min",
 "Commercial & forecasting (18%) · Client leadership (14%) · Measurement (12%) · Strategy (12%) · People & process (11%)",
 "Would you put them in front of your largest client next week, and let them hire the next three people?",
 "Q1 is the highest-signal question on this card. Anyone senior who cannot separate marginal from average return "
 "will scale an account into a loss and report it as a win."),
]

SOP = {
"title": "Performance Marketing Hiring — How We Run It",
"intro": "Five stages. Nobody spends interviewer time on a candidate who has not already cleared an objective bar. "
         "If you are running a stage, you only need to read your own row.",
"stages": [
("1","Application review","HR","5 min",
 "Reject anything with no hands-on account access for Associate and above. 'Managed campaigns' on a CV means nothing "
 "until they name the platform and the account.",
 "Shortlist → stage 2"),
("2","HR screen (call)","HR","20 min",
 "Fixed script: notice period, compensation range, reason for leaving, which platforms they personally operated (not "
 "supervised), and availability. No technical judgment required — do not attempt to assess skill here.",
 "Pass → book them in for the supervised assessment"),
("3","Assessment (in office, supervised)","HR invigilates","0 min of assessing",
 "Sit them at a laptop with '1. Candidate Assessment.html' open. They enter their details, you enter your name as "
 "invigilator, and they work through it alone under a countdown. Intern 30 min through Sr. Manager 50 min. "
 "Every question offers a choice of two; there is a built-in calculator; they may skip. Afterwards open "
 "'2. Grader.html', load their result file, score the written answers, print it.",
 "80%+ proceed · 65–79% borderline, hiring manager decides · under 65% reject"),
("4","Practical case (candidate, at home)","Hiring manager","20 min to review",
 "Send the case for their level and track from the Case Studies tab of the interview kit. Cap it at 3 hours and say so "
 "in writing. Always run a short walkthrough — change one assumption mid-conversation and see if they can re-reason.",
 "Pass → book the final interview"),
("5","Final interview","Hiring manager (+ dept head for Manager and above)","45–60 min",
 "Use the one-page card for that level. Eight questions, nothing else. Take the grader printout in with you — it tells "
 "you which two areas to dig into. Score the card immediately afterwards, before you discuss the candidate with anyone.",
 "Complete the scorecard in the interview kit"),
("6","Decision","All interviewers","15 min",
 "Everyone submits their scorecard BEFORE the debrief. Read evidence, not conclusions. A '1' on any must-pass "
 "competency is a no-hire regardless of total score. Record the known weakness you are accepting and hand it to the "
 "new joiner's manager on day one.",
 "Offer / reject within 48 hours"),
],
"rules": [
 "Never send the Grader file to a candidate. It contains every answer.",
 "Never skip the assessment to save time on a candidate you already like. That is exactly when it earns its keep.",
 "Do not discuss a candidate with another interviewer before both scorecards are submitted. Talking first is how one "
 "confident voice overwrites two honest ones.",
 "Reject within 48 hours with one specific reason. The market for good performance marketers is small and it talks.",
 "If a candidate scores below 65% but you want to proceed anyway, that is allowed — but write down why. Review those "
 "decisions in six months and see whether your instinct beat the test.",
],
"assessment_notes": [
 "EVERY question is bucketed into one of four capabilities, and the grader scores each separately: "
 "Theoretical Knowledge (do they know how it works), Calculation Capability (can they do the arithmetic, including "
 "working backwards from a target), Strategic Mindset (do they reason about trade-offs and consequence), and "
 "Problem Solving Approach (given something broken, what do they do and in what order).",
 "Read the SHAPE of the four scores, not the total. Strong knowledge with weak calculation is a very different hire "
 "from the reverse — and calculation is the hardest of the four to train, so weight it accordingly.",
 "The mix shifts by level. Intern is weighted towards knowledge and calculation; Sr. Manager is weighted towards "
 "strategy. An intern is not expected to have formed strategic judgment yet.",
 "Difficulty is tiered: Intern foundational · Associate intermediate · Manager intermediate-to-advanced · "
 "Sr. Manager advanced. Manager papers draw from both intermediate and advanced questions.",
 "Every candidate gets a different question set, sampled live from a pool several times the size of the test. Two "
 "people sitting side by side will not see the same questions, and the options are reshuffled per person.",
 "Each question offers a choice of two FROM THE SAME capability. They can dodge a question they dislike, but not a "
 "whole capability — so the diagnostic still holds. The grader shows which one they picked and which they turned down.",
 "A calculator is built in and they are told to use it. Knowing what to calculate is the skill; mental arithmetic speed is not.",
 "Skipping is allowed, scores as incorrect, and is counted separately. Watch where skips CLUSTER — two skips both in "
 "Calculation is a clear finding; two scattered skips are not.",
 "The paper is X scored questions PLUS written answers, marked separately then combined 70/30. The written answers are "
 "not part of the 'X of Y' score — the grader states both numbers so there is no confusion.",
 "Note: the four assessment capabilities are not the same as the ten interview competencies in the workbook. The "
 "assessment tests what can be measured on paper; the scorecard covers ownership, attitude and client handling, which cannot be.",
],
"calibration": "Run this once, with everyone in the room at the same time — never one-to-one. Take one recorded or "
               "roleplayed candidate, have everyone score them independently on the card, then compare. The disagreements "
               "teach the standard faster than any document. 45 minutes, repeated once every two quarters. That is the "
               "entire training requirement.",
}
