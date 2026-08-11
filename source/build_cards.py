# -*- coding: utf-8 -*-
import os, html
import cards as C

DEST = os.environ.get("ASSESSMENT_OUT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
e = lambda s: html.escape(str(s))

CSS = """
@page{size:A4;margin:11mm}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;color:#16223a;
background:#e9edf3;font-size:10.2pt;line-height:1.35;-webkit-font-smoothing:antialiased}
.page{width:210mm;min-height:297mm;background:#fff;margin:14px auto;padding:11mm;
box-shadow:0 2px 14px rgba(0,0,0,.10);page-break-after:always;position:relative}
.page:last-child{page-break-after:auto}
.top{background:#1f3864;color:#fff;padding:9px 14px;border-radius:6px;display:flex;
justify-content:space-between;align-items:center;margin-bottom:9px}
.top h1{font-size:14pt;font-weight:700;letter-spacing:-.2px;white-space:nowrap}
.top .r{font-size:8.2pt;text-align:right;color:#c3d0e6;line-height:1.3;flex:none;padding-left:14px}
.meta{display:flex;gap:9px;margin-bottom:9px;font-size:8.6pt}
.meta>div{flex:1;border:1px solid #d9e0ec;border-radius:5px;padding:5px 8px}
.meta b{display:block;font-size:7.1pt;text-transform:uppercase;letter-spacing:.6px;color:#7b8aa5}
.fill{border-bottom:1px solid #c8d2e2;display:inline-block;min-width:56px;height:11px}
.wt{background:#eef3fb;border-left:3px solid #2e5c9a;padding:6px 10px;border-radius:0 5px 5px 0;
font-size:8.5pt;margin-bottom:9px;color:#2c3d5e}
table{width:100%;border-collapse:collapse}
th{background:#2e5c9a;color:#fff;font-size:7.3pt;text-transform:uppercase;letter-spacing:.6px;
padding:5px 7px;text-align:left;font-weight:700}
td{padding:6px 7px;border-bottom:1px solid #e4e9f2;vertical-align:top}
tr:nth-child(even) td{background:#f7f9fd}
.n{font-weight:700;color:#2e5c9a;font-size:11pt;text-align:center;width:20px}
.q{font-weight:600;font-size:9.6pt;line-height:1.3}
.lf{font-size:8.4pt;color:#1d6b3f;line-height:1.28}
.rf{font-size:8.4pt;color:#96271a;line-height:1.28}
.box{display:flex;gap:3px;justify-content:center}
.box span{width:15px;height:15px;border:1.2px solid #9aa9c2;border-radius:3px;font-size:7pt;
color:#9aa9c2;display:flex;align-items:center;justify-content:center;font-weight:700}
.foot{margin-top:9px;display:flex;gap:9px}
.fbox{flex:1;border:1px solid #d9e0ec;border-radius:5px;padding:8px 10px}
.fbox h3{font-size:7.2pt;text-transform:uppercase;letter-spacing:.6px;color:#7b8aa5;margin-bottom:4px}
.fbox p{font-size:8.5pt;line-height:1.35}
.override{background:#fff8e6;border:1px solid #e6c165}
.override p{font-weight:600;font-size:9pt;color:#6b4f00}
.scale{font-size:7.8pt;color:#7b8aa5;margin-top:7px;text-align:center;border-top:1px solid #e4e9f2;padding-top:6px}
.notes{border:1px solid #d9e0ec;border-radius:5px;margin-top:9px;padding:8px 10px;height:92px}
.notes h3{font-size:7.2pt;text-transform:uppercase;letter-spacing:.6px;color:#7b8aa5}
/* SOP — tuned to fit exactly one page */
.sop .lead{font-size:8.3pt;color:#41516f;margin-bottom:6px;line-height:1.3}
.sop table td{font-size:7.5pt;line-height:1.24;padding:3px 5px}
.sop table th{padding:3px 5px;font-size:6.8pt}
.sop h2{font-size:8.6pt;background:#1f3864;color:#fff;padding:3px 8px;border-radius:4px;margin:6px 0 4px}
.sop li{font-size:7.5pt;margin-bottom:2px;line-height:1.28}
.sop ul,.sop ol{margin-left:13px}
.sop .n{font-size:9pt}
.cal{background:#eef3fb;border-left:3px solid #2e5c9a;padding:6px 10px;border-radius:0 5px 5px 0;
font-size:7.7pt;line-height:1.32}
@media print{body{background:#fff}.page{margin:0;box-shadow:none;width:auto;min-height:auto;padding:0}}
"""

def card(level, rows, mins, weights, override, coach):
    h = f'<div class="page"><div class="top"><h1>Interviewer Card — {e(level)}</h1>'
    h += f'<div class="r">Final interview · {e(mins)}<br>Ask all eight. Nothing else.</div></div>'
    h += ('<div class="meta">'
          '<div><b>Candidate</b><span class="fill" style="min-width:150px"></span></div>'
          '<div><b>Interviewer</b><span class="fill" style="min-width:110px"></span></div>'
          '<div><b>Date</b><span class="fill" style="min-width:80px"></span></div>'
          '<div><b>Assessment score</b><span class="fill" style="min-width:60px"></span>%</div></div>')
    h += f'<div class="wt"><b>What this level is weighted on:</b> {e(weights)}</div>'
    h += ('<table><tr><th style="width:20px"></th><th style="width:39%">Ask this</th>'
          '<th style="width:24%">Listen for</th><th style="width:24%">Red flag</th>'
          '<th style="width:74px;text-align:center">Rating</th></tr>')
    for n, q, lf, rf in rows:
        h += (f'<tr><td class="n">{n}</td><td class="q">{e(q)}</td>'
              f'<td class="lf">{e(lf)}</td><td class="rf">{e(rf)}</td>'
              '<td><div class="box"><span>1</span><span>2</span><span>3</span><span>4</span></div></td></tr>')
    h += '</table>'
    h += '<div class="scale"><b>1</b> below bar &nbsp;·&nbsp; <b>2</b> developing, partial evidence &nbsp;·&nbsp; <b>3</b> at bar for this level &nbsp;·&nbsp; <b>4</b> above bar &nbsp;&nbsp;|&nbsp;&nbsp; Rate on evidence you could quote. If you cannot quote it, you cannot rate it.</div>'
    h += '<div class="foot">'
    h += f'<div class="fbox override"><h3>The question that overrides the score</h3><p>{e(override)}</p></div>'
    h += f'<div class="fbox"><h3>How to run this one</h3><p>{e(coach)}</p></div>'
    h += '</div>'
    h += ('<div class="notes"><h3>Evidence &amp; notes — write while they talk, not after</h3></div>'
          '<div class="foot"><div class="fbox"><h3>Recommendation</h3>'
          '<p>Strong hire &nbsp;/&nbsp; Hire &nbsp;/&nbsp; Borderline &nbsp;/&nbsp; No hire &nbsp;&nbsp; (circle one)</p></div>'
          '<div class="fbox"><h3>If we hire, the weakness we are accepting is</h3>'
          '<p><span class="fill" style="min-width:100%"></span></p></div></div>')
    h += '</div>'
    return h


def sop_page():
    S = C.SOP
    h = '<div class="page sop"><div class="top"><h1>' + e(S["title"]) + '</h1>'
    h += '<div class="r">Page 1: the process. Page 2: the assessment.<br>Pages 3-6: one card per level.</div></div>'
    h += f'<p class="lead">{e(S["intro"])}</p>'
    h += ('<table><tr><th style="width:18px"></th><th style="width:19%">Stage</th><th style="width:13%">Owner</th>'
          '<th style="width:11%">Our time</th><th>What you actually do</th><th style="width:20%">Cut-off / handoff</th></tr>')
    for n, stage, owner, t, doing, cut in S["stages"]:
        h += (f'<tr><td class="n">{n}</td><td><b>{e(stage)}</b></td><td>{e(owner)}</td>'
              f'<td>{e(t)}</td><td>{e(doing)}</td><td>{e(cut)}</td></tr>')
    h += '</table>'
    h += '<h2>Five rules that are not negotiable</h2><ol>'
    for r in S["rules"]:
        h += f'<li>{e(r)}</li>'
    h += '</ol>'
    h += '<h2>The only training required</h2>'
    h += f'<div class="cal">{e(S["calibration"])}</div>'
    h += ('<h2>Files and who holds them</h2><ul>'
          '<li><b>1. Candidate Assessment.html</b> — open on a laptop for the supervised session. Contains no answers.</li>'
          '<li><b>2. Grader.html</b> — hiring manager and HR only. <b>Contains every answer. Never send it out.</b></li>'
          '<li><b>3. Interviewer Cards + Process SOP.pdf</b> — this document. Page 1 is the process, page 2 explains '
          'the assessment, pages 3–6 are one interview card per level.</li>'
          '<li><b>Performance Marketing Interview Kit.xlsx</b> — the full framework, question bank and case studies. '
          'Read once during onboarding; you do not need it in the interview.</li></ul>')
    h += '</div>'

    # --- page 2: how the assessment works
    h += '<div class="page sop"><div class="top"><h1>How the Supervised Assessment Works</h1>'
    h += '<div class="r">Reference for HR and hiring managers.<br>Read once, not before every interview.</div></div>'
    h += ('<p class="lead">The assessment exists to do the measurable half of the filtering before anyone spends '
          'interview time. Everything below is already built into the tool — you do not have to manage any of it.</p>')
    h += '<h2>What it measures</h2>'
    cats = [
        ("Theoretical Knowledge", "Do they know how the platforms and the concepts actually work?"),
        ("Calculation Capability", "Can they do the arithmetic the job requires, including working backwards from a target to a required CPC or CPL?"),
        ("Strategic Mindset", "Do they reason about trade-offs, allocation and consequence — or only about tactics?"),
        ("Problem Solving Approach", "Given something broken or ambiguous, what do they do, and in what order?"),
    ]
    h += '<table><tr><th style="width:26%">Capability</th><th>What it is actually testing</th></tr>'
    for c, d in cats:
        h += f'<tr><td><b>{e(c)}</b></td><td>{e(d)}</td></tr>'
    h += '</table>'
    h += '<h2>How the mix and difficulty change by level</h2>'
    h += ('<table><tr><th>Level</th><th style="width:14%">Difficulty</th><th style="width:9%">Scored</th>'
          '<th style="width:9%">Written</th><th style="width:8%">Time</th><th>Capability mix</th></tr>')
    mix = [
        ("Intern", "Foundational", "15", "2", "30 min", "Knowledge 4 · Calculation 6 · Strategy 2 · Problem solving 3"),
        ("Associate", "Intermediate", "18", "3", "40 min", "Knowledge 5 · Calculation 5 · Strategy 3 · Problem solving 5"),
        ("Manager", "Intermediate + advanced", "20", "3", "45 min", "Knowledge 5 · Calculation 4 · Strategy 6 · Problem solving 5"),
        ("Sr. Manager", "Advanced", "18", "3", "50 min", "Knowledge 3 · Calculation 3 · Strategy 7 · Problem solving 5"),
    ]
    for r in mix:
        h += '<tr>' + "".join(f'<td>{e(x)}</td>' for x in r) + '</tr>'
    h += '</table>'
    h += '<h2>What you need to know when reading a result</h2><ul>'
    for n in S["assessment_notes"]:
        h += f'<li>{e(n)}</li>'
    h += '</ul></div>'
    return h


doc = ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Interviewer Cards</title>"
       f"<style>{CSS}</style></head><body>")
doc += sop_page()
for level, rows, mins, weights, override, coach in C.CARDS:
    doc += card(level, rows, mins, weights, override, coach)
doc += "</body></html>"

os.makedirs(DEST, exist_ok=True)
p = os.path.join(DEST, "sop.html")
with open(p, "w", encoding="utf-8") as fh:
    fh.write(doc)
print("written sop.html:", p, len(doc), "bytes")
