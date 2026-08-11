# Performance Marketing — Candidate Assessment Process

Hiring toolkit for digital / performance marketing roles across **Lead Generation** and
**Ecommerce**, at four levels: Intern, Associate, Manager, Sr. Manager.

Two audiences use this folder. **HR and interviewers** need only the four numbered files.
**A developer** maintaining or extending the assessment needs `/source`.

---

## 1. Files for HR and interviewers

| File | Who holds it | What it is |
|---|---|---|
| `1. Candidate Assessment (open in office).html` | HR — open on a laptop for the candidate | The supervised, timed test. **Contains no answers.** Auto-submits to Supabase database. |
| `2. Grader (internal - do not share).html` | Hiring manager and HR only | Loads a result file and scores it. **Contains every answer — never send this to a candidate.** |
| `3. Interviewer Cards + Process SOP.pdf` | Everyone running a stage | Page 1 the process, page 2 how the assessment works, pages 3–6 one interview card per level. Print it. |
| `4. HR Candidate Dashboard.html` | HR & Recruiters only | **Private Master Dashboard.** Lists all candidates from Supabase, lets HR evaluate written answers & sync final scores (Passcode: `admin123`). |
| `Performance Marketing Interview Kit.xlsx` | Read once during onboarding | Full framework: 123 interview questions with answer keys, competency model, weighted scorecards, case studies, debrief protocol. |

### Running it

1. **HR screen** (20 min) — logistics and knockouts only, no technical judgment.
2. **Supervised assessment** — sit the candidate at a laptop with file 1. They enter their
   details, HR enters their own name as invigilator, and the candidate works alone under a
   countdown. Nothing is transmitted anywhere; at the end they download a result file.
3. **Grade it** — open file 2, load their result, score the written answers 0–3. Print the page.
4. **Practical case** — only for those who pass. Cases are in the workbook.
5. **Final interview** — use the one-page card for that level. Take the grader printout in with
   you; it tells you which capabilities to probe.
6. **Decide** — scorecards submitted before the debrief, must-pass gate applied.

### How the assessment is built

- Every question belongs to one of four capabilities, scored separately:
  **Theoretical Knowledge**, **Calculation Capability**, **Strategic Mindset**,
  **Problem Solving Approach**.
- Difficulty is tiered: Intern foundational · Associate intermediate ·
  Manager intermediate + advanced · Sr. Manager advanced.
- Each session is **sampled live** from a pool several times the size of the paper, so no two
  candidates get the same test. Answer options are reshuffled per candidate.
- Each question offers a **choice of two from the same capability** — a candidate can dodge a
  question, not a subject.
- **Skipping** is allowed, scores as incorrect, and is reported separately.
- A **calculator** is built in and candidates are told to use it.
- Score = 70% scored questions + 30% written. Bands: 80%+ proceed · 65–79% borderline ·
  under 65% stop.

> The four assessment capabilities are **not** the same as the ten interview competencies in the
> workbook. The assessment measures what can be tested on paper; the scorecard covers ownership,
> attitude and client handling, which cannot.

---

## 2. `/source` — for the developer

The two HTML tools are **generated**, not hand-written. The question bank lives in Python and is
compiled into a single self-contained HTML file with no dependencies, no server and no network calls.

```
source/
  testbank.py      base question bank + helper constructors (mcq / num / wr)
  extra_junior.py  additional Intern and Associate questions
  extra_senior.py  additional Manager and Sr. Manager questions
  extra_cat.py     questions added to fill capability gaps
  taxonomy.py      >> the file you will edit most <<
                   maps every question ID to a capability + difficulty,
                   sets slot counts, time limits and probe text per level
  pools.py         merges everything into per-level pools, rebalances answer positions, audits
  cards.py         content for the interviewer cards and the process SOP
  build_tool.py    generates files 1 and 2
  build_cards.py   generates file 3
```

### Rebuilding

```bash
cd source
python pools.py        # audit: pool sizes, ratios, bank composition. Run this first.
python build_tool.py   # regenerates files 1 and 2 into the parent folder
python build_cards.py  # regenerates file 3 (HTML; print to PDF from a browser)
```

Requires Python 3.9+ and `openpyxl` only if you also rebuild the workbook. Output location
defaults to the parent folder; override with the `ASSESSMENT_OUT` environment variable.

### Adding a question

1. Append it to the relevant `extra_*.py` using `mcq(...)`, `num(...)` or `wr(...)`.
   Give it a unique ID.
2. Add that ID to `taxonomy.py` under the right capability and difficulty. **The build fails
   loudly if any question is untagged or any ID is duplicated** — that is intentional.
3. Run `python pools.py` and check the ratio column stays at 1.5x or above.
4. Rebuild.

### Two invariants worth protecting

- **The candidate file must never contain an answer key.** `candidate_data()` in `build_tool.py`
  explicitly whitelists the fields that get written out. Do not switch it to a blacklist.
- **Answer positions must stay near 25/25/25/25.** `pools.rebalance()` handles the stored bank
  and the tool reshuffles at runtime. An earlier version had 82% of correct answers on option B,
  which meant a candidate could score 95% by always picking B.

### Known limits

- A browser-based test cannot be proctored by itself — that is why it is run supervised in office.
- The questions have not yet been validated against real candidate outcomes. After 10–15 people,
  check the grader's per-question view for items everyone gets right or everyone gets wrong;
  those are not discriminating and should be swapped out.
- Figures are sized for the Indian market (read as INR). Rescale for other markets — the
  reasoning being tested is currency-independent.
