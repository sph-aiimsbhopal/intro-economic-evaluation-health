#!/usr/bin/env python3
"""Build the faculty-workshop paper pack from one data file.

    python3 build_paperpack.py

writes  paper-pack.html               (participants: eight one-page briefs)
        paper-pack-facilitator.html   (facilitators: the key)

Every citation here was checked on 18 September 2026 against its PubMed record (Europe PMC
mirror, or PubMed's record page), with volume, issue and pages confirmed against Crossref or the publisher. Do not edit a citation without re-checking it.
No em dashes anywhere: house rule.
"""
import html, pathlib
from papers import PAPERS, SESSIONS, PAIRS

HERE = pathlib.Path(__file__).parent
E = html.escape

CSS = """
@page{ size:A4; margin:8mm 10mm 8mm }
.pk{ max-width:1000px; margin:0 auto; padding:18px 22px 40px }
.sheet{ break-after:page; page-break-after:always; margin-bottom:40px }
.sheet:last-child{ break-after:auto; page-break-after:auto }
.top{ background:var(--band); color:#fff; padding:10px 16px; display:flex; justify-content:space-between;
  align-items:flex-end; gap:12px; -webkit-print-color-adjust:exact; print-color-adjust:exact }
.top .kick{ font-size:.66rem; text-transform:uppercase; letter-spacing:.14em; font-weight:700; opacity:.85; margin:0 0 2px }
.top .grp{ font-size:1.35rem; font-weight:700; margin:0 }
.top .clu{ font-size:.78rem; opacity:.9; text-align:right }
h1.t{ font-size:1.12rem; line-height:1.3; margin:12px 0 4px; color:var(--ink) }
.cit{ font-size:.8rem; color:var(--ink-dim); margin:0 0 4px; line-height:1.45 }
.acc{ display:inline-block; font-size:.72rem; font-weight:700; padding:1px 7px; border-radius:2px; margin-right:6px;
  -webkit-print-color-adjust:exact; print-color-adjust:exact }
.acc.oa{ background:var(--fill-good); color:var(--good); border:1px solid var(--edge-good) }
.acc.cl{ background:var(--fill-bad); color:var(--bad); border:1px solid var(--edge-bad) }
.pk h2{ margin:10px 0 5px; font-size:.84rem; padding-bottom:3px }
.pk p, .pk li{ font-size:.84rem; line-height:1.33 }
.pk p{ margin:.3em 0 }
.sum{ background:var(--panel); border-left:4px solid var(--band); padding:6px 12px; margin:4px 0;
  -webkit-print-color-adjust:exact; print-color-adjust:exact }
.sum p{ margin:.25em 0 }
table.pr{ margin:4px 0; font-size:.82rem }
table.pr th{ padding:4px 7px; font-size:.74rem; -webkit-print-color-adjust:exact; print-color-adjust:exact }
table.pr td{ padding:3px 7px; line-height:1.3 }
table.pr td:first-child{ font-weight:700; color:var(--band); width:1%; font-variant-numeric:tabular-nums }
table.pr td .s{ display:block; font-weight:400; color:var(--ink-dim); font-size:.9em; white-space:normal; width:9.5em }
.rb{ border:1px solid var(--line); padding:6px 12px; margin-top:6px; font-size:.92rem }
.rb p{ margin:.2em 0 }
.foot{ font-size:.7rem; color:var(--ink-faint); margin-top:6px }
table.key{ font-size:.86rem } table.key td{ padding:4px 7px; line-height:1.35 }
table.key td:first-child{ width:22%; font-weight:700 }
.tp li{ margin:.25em 0 }
.warnbox{ border-left:4px solid var(--warn); background:rgba(138,90,0,.07); padding:6px 12px; margin:6px 0; font-size:.86rem;
  -webkit-print-color-adjust:exact; print-color-adjust:exact }
.cover h1{ font-size:1.3rem; margin:8px 0 4px }
table.ov{ font-size:.84rem } table.ov td{ padding:4px 7px }
@media print{
  body{ font-size:10pt }
  .pk{ padding:0; max-width:none }
  .sheet{ margin:0; height:280mm; overflow:hidden }
}
"""

def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="stylesheet" href="../assets/css/tokens.css">
<link rel="stylesheet" href="../assets/css/handout.css">
<style>{CSS}</style>
</head>
<body>
<div class="pk">
"""

TAIL = "</div>\n</body>\n</html>\n"

def cite(p, title=True):
    return (f"<p class=\"cit\"><strong>{E(p['authors'])}</strong> {E(p['title']) if title else ''} "
            f"<em>{E(p['journal'])}</em> {E(p['vol'])}. "
            f"<span class=\"pmid\">PMID {p['pmid']}"
            + (f" &nbsp;·&nbsp; {p['pmcid']}" if p.get('pmcid') else "")
            + f" &nbsp;·&nbsp; doi:{E(p['doi'])}</span></p>")

def access(p):
    if p['oa']:
        return ("<p class=\"cit\"><span class=\"acc oa\">Open access</span>"
                f"Full text free at doi.org/{E(p['doi'])}. Read it; this sheet only gets you started.</p>")
    return ("<p class=\"cit\"><span class=\"acc cl\">Not open access</span>"
            "Work from this sheet and the abstract. <strong>Not reported in the abstract</strong> is an "
            "acceptable answer to a prompt, and worth saying out loud.</p>")

def participant():
    out = [head("Paper pack: eight published economic evaluations",
                "One-page briefs for the group appraisal exercise, faculty workshop, 23 September 2026.")]
    # cover sheet
    out.append('<div class="sheet cover">')
    out.append('<div class="top"><div><p class="kick">Economic Evaluation in Health &nbsp;·&nbsp; AIIMS Bhopal &nbsp;·&nbsp; 23 September 2026</p>'
               '<p class="grp">Paper pack</p></div><div class="clu">Group appraisal exercise</div></div>')
    out.append("""<h1>Your group has one paper, and it stays with you all day</h1>
<p>Each group of three has been given one published economic evaluation from India. After each session,
spend a few minutes applying what was just taught to <strong>your</strong> paper, using the prompts on its
sheet and the <strong>appraisal checklist</strong>. By the report-back the checklist should be full
and you should be able to say, in one sentence, whether you believe the paper's conclusion.</p>
<p>The eight papers were chosen to differ. Some are strong, some are not, and at least one calls itself
something it is not. Do not assume that publication means quality, or that a paper from a well-known group is
right.</p>
<h2>The eight papers</h2>
<table class="ov"><thead><tr><th>Group</th><th>Cluster</th><th>Paper</th><th>Access</th></tr></thead><tbody>""")
    for p in PAPERS:
        out.append(f"<tr><td><strong>{p['n']}</strong></td><td>{E(p['cluster'])}</td>"
                   f"<td>{E(p['short'])}</td><td>{'open' if p['oa'] else 'abstract only'}</td></tr>")
    out.append("</tbody></table>")
    out.append("""<h2>Report-back, the last session</h2>
<p>Groups report in <strong>pairs</strong>, chosen so that the two papers contrast. Each pair has six minutes:
<strong>two minutes per group</strong>, then two minutes on what the contrast shows.</p>
<p>In your two minutes, give: (1) what the paper compared and what it concluded, in one sentence; (2) the one
principle it handles <strong>best</strong>; (3) the one it handles <strong>worst</strong>, and whether that
changes the conclusion; (4) your verdict: <em>would you act on this paper?</em></p>
<table class="ov"><thead><tr><th>Pair</th><th>Groups</th><th>Papers</th></tr></thead><tbody>""")
    byn = {p['n']: p for p in PAPERS}
    for i, (a, b, c) in enumerate(PAIRS, 1):
        out.append(f"<tr><td><strong>{i}</strong></td><td>{a} and {b}</td>"
                   f"<td>{E(byn[a]['short'].split(',')[0])} and {E(byn[b]['short'].split(',')[0])}</td></tr>")
    out.append("</tbody></table><p class=\"foot\">Each pair was chosen because the two papers differ in an instructive way. "
               "Working out how is part of the exercise.</p></div>")

    for p in PAPERS:
        out.append('<div class="sheet">')
        out.append(f'<div class="top"><div><p class="kick">Paper pack &nbsp;·&nbsp; 23 September 2026</p>'
                   f'<p class="grp">Group {p["n"]}</p></div><div class="clu">{E(p["cluster"])}<br>'
                   f'reports with Group {p["partner"]}</div></div>')
        out.append(f'<h1 class="t">{E(p["title"].rstrip("."))}</h1>')
        out.append(cite(p, title=False)); out.append(access(p))
        out.append('<h2>What the paper says it did, and found</h2><div class="sum">')
        for para in p['summary']:
            out.append(f"<p>{para}</p>")
        out.append("</div>")
        out.append('<h2>Your prompts through the day</h2><table class="pr"><thead><tr><th>After</th><th>Ask of your paper</th></tr></thead><tbody>')
        for t, s, i in SESSIONS:
            q = p['prompts'][i]
            out.append(f"<tr><td>Session {t}<span class=\"s\">{E(s)}</span></td><td>{q}</td></tr>")
        out.append("</tbody></table>")
        out.append('<p class="foot">The summary paraphrases the published abstract and is not a substitute for it. '
                   'Citation checked against the MEDLINE record, September 2026. By the report-back: would you act on this paper, and why?</p>')
        out.append("</div>")
    out.append(TAIL)
    return "\n".join(out)

def facilitator():
    out = [head("Paper pack: facilitator key",
                "What each group should find, the teaching point of each paper, and how the report-back pairs work.")]
    out.append('<div class="sheet cover">')
    out.append('<div class="top"><div><p class="kick">Facilitators only &nbsp;·&nbsp; 23 September 2026</p>'
               '<p class="grp">Paper pack: the key</p></div><div class="clu">Do not hand out</div></div>')
    out.append("""<h1>What each paper is for</h1>
<p>The participant sheets are deliberately neutral: they paraphrase what each paper says about itself and ask
questions, but do not say which papers are weak. The groups find that out. This key is for circulating
facilitators, so that a group that is stuck can be nudged toward the point without being handed it.</p>
<p><strong>How to nudge:</strong> ask the prompt again, then point at the relevant row of the appraisal checklist.
Only if they are still stuck after the session on that principle, name the issue.</p>
<table class="ov"><thead><tr><th>Group</th><th>Paper</th><th>Its job in the pack</th></tr></thead><tbody>""")
    for p in PAPERS:
        out.append(f"<tr><td><strong>{p['n']}</strong></td><td>{E(p['short'])}</td><td>{p['job']}</td></tr>")
    out.append("</tbody></table></div><div class=\"sheet\"><div class=\"top\"><div><p class=\"kick\">Facilitators only</p><p class=\"grp\">Report-back</p></div><div class=\"clu\">the last session</div></div><h2>Report-back pairs</h2>"
               '<table class="ov"><thead><tr><th>Pair</th><th>Groups</th><th>What the contrast should surface</th></tr></thead><tbody>')
    for i, (a, b, c) in enumerate(PAIRS, 1):
        out.append(f"<tr><td><strong>{i}</strong></td><td>{a} and {b}</td><td>{E(c)}</td></tr>")
    out.append("</tbody></table><p class=\"small dim\">Four pairs at six minutes is 24 minutes. Keep one minute "
               "in hand. Cut a group off at two minutes; the contrast is the point, not the summary.</p></div>")

    for p in PAPERS:
        out.append('<div class="sheet">')
        out.append(f'<div class="top"><div><p class="kick">Facilitator key &nbsp;·&nbsp; Group {p["n"]}</p>'
                   f'<p class="grp">{E(p["short"])}</p></div><div class="clu">{E(p["cluster"])}<br>pairs with Group {p["partner"]}</div></div>')
        out.append(cite(p))
        out.append('<h2>The paper against the checklist</h2><table class="key"><tbody>')
        for k, v in p['grid']:
            out.append(f"<tr><td>{E(k)}</td><td>{v}</td></tr>")
        out.append("</tbody></table>")
        out.append('<h2>What a good group finds</h2><ul class="tp">')
        for t in p['teach']:
            out.append(f"<li>{t}</li>")
        out.append("</ul>")
        if p.get('check'):
            out.append(f'<div class="warnbox"><strong>Before the day:</strong> {p["check"]}</div>')
        out.append("</div>")
    out.append(TAIL)
    return "\n".join(out)

if __name__ == "__main__":
    (HERE / "paper-pack.html").write_text(participant())
    (HERE / "paper-pack-facilitator.html").write_text(facilitator())
    for f in ("paper-pack.html", "paper-pack-facilitator.html"):
        n = (HERE / f).read_text().count("—")
        print(f, "em dashes:", n)
