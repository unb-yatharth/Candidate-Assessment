# -*- coding: utf-8 -*-
"""Maps every question to one of four assessment categories and a difficulty tier.

Categories
  THEO  Theoretical Knowledge      - do they know how the platforms and concepts work
  CALC  Calculation Capability     - can they do the arithmetic the job actually requires
  STRAT Strategic Mindset          - do they reason about trade-offs, allocation and consequence
  PROB  Problem Solving Approach   - given a broken or ambiguous situation, what do they do and in what order

Difficulty
  low   Intern
  mid   Associate  (also available to Manager)
  high  Manager and Sr. Manager
"""

THEO  = "Theoretical Knowledge"
CALC  = "Calculation Capability"
STRAT = "Strategic Mindset"
PROB  = "Problem Solving Approach"

CATEGORIES = [THEO, CALC, STRAT, PROB]

# which difficulty tiers each level draws from
LEVEL_DIFF = {
    "intern":    {"low"},
    "associate": {"mid"},
    "manager":   {"mid", "high"},
    "senior":    {"high"},
}

# how many questions of each category a session contains (slot counts)
SLOTS = {
    "intern":    {THEO: 4, CALC: 6, STRAT: 2, PROB: 3},   # 15
    "associate": {THEO: 5, CALC: 5, STRAT: 3, PROB: 5},   # 18
    "manager":   {THEO: 5, CALC: 4, STRAT: 6, PROB: 5},   # 20
    "senior":    {THEO: 3, CALC: 3, STRAT: 7, PROB: 5},   # 18
}

WRITTEN_SLOTS = {"intern": 2, "associate": 3, "manager": 3, "senior": 3}
MINUTES = {"intern": 30, "associate": 40, "manager": 45, "senior": 50}


def _spread(ids, cat, diff):
    return {i: (cat, diff) for i in ids}


MAP = {}

# ------------------------------------------------------------------ INTERN (low)
MAP |= _spread(["I01","I02","I03","I04","I05","I06","I07","I08","I19","I20",
                "I21","I22","I23","I24","I26","I27"], THEO, "low")
MAP |= _spread(["I09","I10","I11","I12","I13","I14","I29","I30","I31","I32",
                "I33","I34","I35","I36"], CALC, "low")
MAP |= _spread(["I25","I28","I38"], STRAT, "low")
MAP |= _spread(["I15","I16","I37","I17","I39","I18","I40","I41","I42","I43",
                "I44","I45"], PROB, "low")

# --------------------------------------------------------------- ASSOCIATE (mid)
MAP |= _spread(["A01","A03","A04","A05","A06","A07","A09","A10","A11","A12",
                "A13","A19","A20","A25","A26","A27","A28","A29","A30","A32",
                "A34"], THEO, "mid")
MAP |= _spread(["A15","A16","A17","A18","A35","A36","A37","A38","A39","A40",
                "A41","A42"], CALC, "mid")
MAP |= _spread(["A02","A14","A31","A33","A44","A48","A49","A54"], STRAT, "mid")
MAP |= _spread(["A08","A43","A45","A46","A21","A22","A23","A24","A47","A50",
                "A51","A52","A53"], PROB, "mid")

# ------------------------------------------------------- MANAGER (mid and high)
MAP |= _spread(["M06","M11","M12","M14","M28","M36","M48"], THEO, "mid")
MAP |= _spread(["M01","M02","M03","M05","M07","M10","M13","M22","M29","M30",
                "M31","M32","M33"], THEO, "high")
MAP |= _spread(["M17","M18","M19","M39","M40","M41"], CALC, "mid")
MAP |= _spread(["M15","M16","M37","M38","M42","M43","M44"], CALC, "high")
MAP |= _spread(["M35"], STRAT, "mid")
MAP |= _spread(["M04","M08","M09","M27","M20","M47","M49","M25","M51","M53",
                "M56","M59"], STRAT, "high")
MAP |= _spread(["M34","M46","M24","M26","M52","M54","M55","M57","M58"], PROB, "mid")
MAP |= _spread(["M21","M45","M23","M50"], PROB, "high")

# ------------------------------------------------------------- SR MANAGER (high)
MAP |= _spread(["S34","S35","S36","S14","S16","S17","S18","S48","S51"], THEO, "high")
MAP |= _spread(["S01","S02","S03","S05","S25","S26","S27","S28","S29","S30",
                "S31","S32"], CALC, "high")
MAP |= _spread(["S04","S06","S07","S08","S37","S38","S09","S10","S13","S15",
                "S20","S21","S24","S40","S43","S44","S45","S50"], STRAT, "high")
MAP |= _spread(["S33","S39","S11","S12","S19","S22","S23","S41","S42","S46",
                "S47","S49","S52","S53","S54"], PROB, "high")

# ------------------------------------------------- new questions added this round
MAP |= _spread(["N01","N02","N03","N04","N05","N06","N07","N08"], STRAT, "low")
MAP |= _spread(["N09","N10","N11","N12"], CALC, "low")
MAP |= _spread(["N13","N14","N15","N16","N17"], CALC, "mid")
MAP |= _spread(["N18","N19","N20","N21"], STRAT, "mid")
MAP |= _spread(["N22","N23"], THEO, "low")
MAP |= _spread(["N24","N25","N26"], CALC, "high")


# ---------------------------------------------- what to probe, per weak category
PROBE_MAP = {
    THEO: "Theoretical knowledge is the gap. This is the most trainable of the four, so it is not "
          "automatically disqualifying — but check whether the gaps are foundational or peripheral. "
          "Probe with GA-01, GA-03, GA-09, MT-01, MT-08 from the workbook and ask them to walk through "
          "a real account at settings level.",
    CALC: "Calculation capability is the gap, and this is the hardest of the four to train. "
          "Re-run a live calculation out loud in the interview before going any further — give them "
          "MX-02 and MX-07 and watch whether they can set the problem up, not just get the number. "
          "Someone who cannot work backwards from a target to a required CPC will struggle to plan a budget.",
    STRAT: "Strategic mindset is the gap. They may execute well but not see consequence or trade-off. "
           "At Associate level this is coachable; at Manager and above it is the core of the job. "
           "Probe with MX-21, GA-24, GA-29, MT-20 and the level-appropriate case study.",
    PROB: "Problem solving is the gap - they may know the theory but not know what to do when something "
          "breaks. Probe with SI-01, SI-09, GA-20 and press hard on sequence: what do they check first, "
          "second, third, and why that order.",
    "written": "The written answers are the gap - usually ownership, honesty or the ability to explain "
               "something clearly. Probe with OA-04, OA-06, OA-08, OA-13 and ask for a specific example "
               "behind every general claim.",
}

CATEGORY_BLURB = {
    THEO:  "Do they know how the platforms and the concepts actually work?",
    CALC:  "Can they do the arithmetic this job requires, including working backwards from a target?",
    STRAT: "Do they reason about trade-offs, allocation and consequence rather than tactics alone?",
    PROB:  "Given something broken or ambiguous, what do they do — and in what order?",
}
