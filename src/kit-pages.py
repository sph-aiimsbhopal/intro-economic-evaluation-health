#!/usr/bin/env python3
"""Front and back matter for the participant kit.

    python3 kit-pages.py            # writes kit/kit-front.html and kit/kit-back.html

QR codes are generated here and each one is decoded again before it is written,
so a code that does not scan never reaches the printer.
"""
import base64, io, pathlib, sys
import qrcode
import cv2
import numpy as np

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
OUT = ROOT / "kit"
OUT.mkdir(exist_ok=True)

SITE = "https://sph-aiimsbhopal.github.io/intro-economic-evaluation-health/"

WIDGETS = [
    ("classifier", "Classify the study", "Full evaluation or partial, in two questions. Eight real studies to sort."),
    ("cost-classifier", "Which costs count", "Direct or indirect, and whose costs they are under each perspective."),
    ("qaly-builder", "QALY builder", "Drag the corners. A QALY is an area, and three different lives give the same one."),
    ("discounting", "Discounting", "What a discount rate does to a programme whose benefits arrive in thirty years."),
    ("ce-plane", "Cost-effectiveness plane", "Quadrants, dominance, and the threshold line. Move the line and watch the verdict flip."),
    ("uncertainty", "Uncertainty", "Tornado diagram, the cloud of simulations, and the acceptability curve it makes."),
]

GLOSSARY = [
    ("Opportunity cost", "The health forgone elsewhere because a resource was used here. Not the price tag."),
    ("Economic evaluation", "An analysis of both costs and consequences, for two or more alternatives. Anything less is partial."),
    ("CMA, CEA, CUA, CBA", "The four full types, differing only in how consequences are valued: assumed equal, natural units, QALYs, or money."),
    ("Comparator", "What the intervention is compared against. Should be what actually happens now, not nothing."),
    ("Perspective", "Whose costs and effects are counted. India's default is abridged societal, with the payer view reported alongside."),
    ("Time horizon", "How long the analysis follows costs and effects. Must be long enough for the benefits to arrive."),
    ("Micro-costing", "Counting every resource used for one patient, then valuing each. Bottom up."),
    ("Gross costing", "Dividing a department's total spend by its patients. Top down: sees every rupee, makes every patient average."),
    ("Annuitisation", "Spreading a capital item's cost over its working life, with discounting. Not straight-line depreciation."),
    ("QALY", "A year of life weighted by its quality, 1 for full health and 0 for a state as good as being dead. An area, not a score."),
    ("DALY", "A year of healthy life lost. You minimise DALYs; you maximise QALYs. The two cannot share a league table."),
    ("Discounting", "Valuing future costs and effects less than present ones. India asks for 3%, varied from 0 to 5%."),
    ("ICER", "Incremental cost divided by incremental effect, against the next best option. A ratio between two options, never a property of one."),
    ("Average ratio", "Total cost over total effect. Looks like an ICER, answers no decision."),
    ("Dominance", "An option that costs more and does less. Strike it out; no threshold rescues it."),
    ("Extended dominance", "An option you would never choose because a better-value option below it would already have been accepted. Shows up as an ICER that falls as you read down."),
    ("Threshold, lambda", "The most you are willing to pay for one more unit of health. Where it comes from, and whether to believe it, is Session 6."),
    ("Net monetary benefit", "Health gained valued at the threshold, minus what it cost. Both terms in rupees, which avoids the ratio's traps."),
    ("Budget impact", "What adopting it costs the budget next year for everyone eligible. A separate question from cost-effectiveness."),
    ("DSA and PSA", "One-way and probabilistic sensitivity analysis: move one input at a time, or draw all of them from distributions at once."),
    ("CEAC", "Acceptability curve. The share of simulations in which the option is good value, plotted across thresholds."),
    ("Indian Reference Case", "Eleven principles and twelve recommendations setting the method defaults for economic evaluation in India."),
]


def qr_datauri(url: str) -> str:
    """Make a QR, decode it again, and refuse to return one that does not scan."""
    q = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
                      box_size=10, border=2)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw = buf.getvalue()

    arr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_GRAYSCALE)
    decoded, _, _ = cv2.QRCodeDetector().detectAndDecode(arr)
    if decoded != url:
        sys.exit(f"QR check failed for {url!r}: decoded {decoded!r}")
    print(f"  QR ok: {url}")
    return "data:image/png;base64," + base64.b64encode(raw).decode()


def logo(name: str) -> str:
    return "data:image/png;base64," + base64.b64encode((HERE / name).read_bytes()).decode()


CSS = """
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box }
body { margin:0; font: 10.5pt/1.45 Arial, Helvetica, sans-serif; color:#10141A;
       -webkit-print-color-adjust:exact; print-color-adjust:exact }
.page { width:210mm; height:297mm; padding:20mm 18mm 16mm; page-break-after:always;
        position:relative; display:flex; flex-direction:column }
.page:last-child { page-break-after:auto }
h1 { font-size:28pt; line-height:1.1; color:#162a6c; margin:0 0 .35em; font-weight:700 }
h2 { font-size:17pt; color:#162a6c; margin:0 0 .5em; font-weight:700 }
h3 { font-size:11pt; color:#162a6c; margin:0 0 .15em; font-weight:700 }
p { margin:0 0 .7em }
.lede { font-size:12.5pt; line-height:1.5 }
.dim { color:#5A6273 } .faint { color:#9AA1B0 }
.rule { height:2.2pt; background:#162a6c; margin:0 0 6mm }
.foot { margin-top:auto; font-size:7.5pt; color:#9AA1B0; display:flex; justify-content:space-between;
        border-top:.3pt solid #E3E6EE; padding-top:2mm }

/* cover */
.cover { padding:0 }
.cband { background:#162a6c; color:#fff; padding:16mm 18mm 12mm }
.cband .kick { font-size:8.5pt; letter-spacing:.14em; text-transform:uppercase; color:#AEBBE0; margin:0 0 6mm }
.cband h1 { color:#fff; font-size:34pt; margin:0 0 3mm }
.cband .sub { font-size:13pt; color:#D6DEF2; margin:0 }
.cbody { padding:12mm 18mm 16mm; display:flex; flex-direction:column; flex:1 1 auto }
.kitword { font-size:15pt; font-weight:700; color:#162a6c; letter-spacing:.02em; margin:0 0 8mm }
.meta { font-size:11pt; line-height:1.7; margin:0 0 10mm }
.meta b { color:#162a6c }
.nameplate { border:1.2pt solid #162a6c; padding:7mm 8mm; margin-top:auto }
.nameplate .nt { font-size:8.5pt; letter-spacing:.12em; text-transform:uppercase; color:#162a6c; margin:0 0 5mm }
.nameplate .row { display:flex; gap:8mm; margin-bottom:6mm }
.nameplate .f { flex:1 1 auto }
.nameplate .f span { font-size:8.5pt; color:#7A8394; display:block; margin-bottom:1mm }
.nameplate .f i { display:block; border-bottom:.6pt solid #9AA1B0; height:7mm }
.logos { display:flex; gap:8mm; align-items:center; margin-bottom:8mm }
.logos img { height:17mm }

/* agenda */
table { width:100%; border-collapse:collapse; font-size:10pt }
td, th { padding:2.4mm 3mm; border-bottom:.3pt solid #D8DCE6; vertical-align:top; text-align:left }
th { background:#162a6c; color:#fff; font-size:9pt; letter-spacing:.04em }
td.n { width:8mm; font-weight:700; color:#162a6c; text-align:center }
td.t { width:26mm; white-space:nowrap; color:#5A6273; font-variant-numeric:tabular-nums }
tr.brk td { color:#9AA1B0; font-style:italic; background:#F5F7FB }

/* widgets */
.qgrid { display:grid; grid-template-columns:1fr 1fr; gap:7mm 8mm; margin-top:3mm }
.qcell { border:.5pt solid #D8DCE6; padding:5mm; display:flex; gap:5mm; align-items:flex-start }
.qcell img { width:30mm; height:30mm; flex:0 0 30mm }
.qcell p { font-size:9pt; line-height:1.4; margin:0; color:#5A6273 }

/* glossary */
.gl { column-count:2; column-gap:9mm; font-size:9pt; line-height:1.38 }
.gl div { break-inside:avoid; margin-bottom:2.6mm }
.gl b { color:#162a6c }

/* feedback */
.fb .q { margin-bottom:6mm }
.fb .q p { margin:0 0 2mm; font-size:10.5pt }
.fb .scale { display:flex; gap:4mm; font-size:9pt; color:#5A6273 }
.fb .scale span { border:.5pt solid #9AA1B0; padding:1.6mm 0; flex:1 1 0; text-align:center }
.fb .lines { background:repeating-linear-gradient(to bottom, transparent 0 7mm, #D8DCE6 7mm 7.15mm); }
.notesheet { flex:1 1 auto;
  background:repeating-linear-gradient(to bottom, transparent 0 7mm, #D8DCE6 7mm 7.15mm) }

/* licences */
.lic { font-size:8.5pt; line-height:1.4 }
.lic div { margin-bottom:3mm; padding-left:5mm; text-indent:-5mm }
.lic b { color:#162a6c }

/* back cover */
.back { justify-content:center; align-items:center; text-align:center }
.back img { width:46mm; height:46mm; margin-bottom:6mm }
.back .u { font-size:11pt; font-weight:700; color:#162a6c; word-break:break-all }
"""

FOOT = ('<div class="foot"><span>Economic Evaluation in Health &middot; AIIMS Bhopal '
        '&middot; 23 September 2026</span><span>{}</span></div>')


def front() -> str:
    qcells = "".join(
        f'<div class="qcell"><img src="{qr_datauri(SITE + "widgets/" + slug + "/")}">'
        f'<div><h3>{name}</h3><p>{desc}</p></div></div>'
        for slug, name, desc in WIDGETS)

    agenda_rows = [
        ("09:30", "", "Registration and welcome", "Sign-in, your kit, your paper, and how the day will run."),
        ("09:40", "1", "Where economic evidence enters health policy",
         "How decisions about what the health system pays for are made in India, and where you come in."),
        ("10:00", "2", "What economic evaluation is, and what it is not",
         "Opportunity cost. The two questions that sort every study into six boxes."),
        ("10:40", "3", "Framing the question",
         "Decision problem, comparator, perspective, time horizon: the four choices made before any arithmetic."),
        ("11:20", "", "Tea", ""),
        ("11:40", "4", "Costing your own service",
         "Worksheet exercise. Micro-costing against gross costing, shared overheads, annuitised capital."),
        ("12:35", "5", "Outcomes, discounting and the ICER",
         "What a QALY is. Why the future is worth less. Average against incremental, and dominance."),
        ("13:15", "", "Lunch", ""),
        ("14:05", "6", "Thresholds, opportunity cost and budget impact",
         "Where a threshold comes from, India's own estimate, and why affordability is a separate test."),
        ("14:45", "7", "Modelling in half an hour",
         "Decision trees and Markov models at reading level, and what to distrust in a published one."),
        ("15:10", "", "Tea", ""),
        ("15:25", "8", "Handling uncertainty",
         "One-way and probabilistic sensitivity analysis, the tornado, the cloud, the acceptability curve."),
        ("15:55", "9", "Group appraisal report-back",
         "Four pairs of groups, six minutes each. Would you act on this paper, and why?"),
        ("16:20", "10", "Close and feedback", "What to do on Monday, where the material lives."),
    ]
    rows = "".join(
        f'<tr class="brk"><td class="t">{t}</td><td class="n"></td><td colspan="2"><em>{s}</em></td></tr>'
        if not n and not d else
        f'<tr><td class="t">{t}</td><td class="n">{n}</td><td><strong>{s}</strong></td><td class="dim">{d}</td></tr>'
        for t, n, s, d in agenda_rows)

    gl = "".join(f"<div><b>{t}.</b> {d}</div>" for t, d in GLOSSARY)

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Economic Evaluation in Health: participant kit</title><style>{CSS}</style></head><body>

<div class="page cover">
  <div class="cband">
    <p class="kick">School of Public Health &nbsp;&middot;&nbsp; Regional Resource Centre for HTA &nbsp;&middot;&nbsp; AIIMS Bhopal</p>
    <h1>Economic Evaluation<br>in Health</h1>
    <p class="sub">A one-day workshop on reading and appraising published economic evaluations</p>
  </div>
  <div class="cbody">
    <div class="logos"><img src="{logo('aiims.png')}"><img src="{logo('htain.png')}"></div>
    <p class="kitword">Participant kit</p>
    <p class="meta">
      <b>Wednesday 23 September 2026</b>, 09:30 to 16:30<br>
      SAMVAD (Board Room, First Floor, Medical College Building)<br>
      AIIMS Bhopal, Saket Nagar<br>
      <span class="dim">For faculty, senior and junior residents, and research project staff</span>
    </p>
    <div class="nameplate">
      <p class="nt">This kit belongs to</p>
      <div class="row">
        <div class="f"><span>Name</span><i></i></div>
        <div class="f"><span>Department</span><i></i></div>
      </div>
      <div class="row" style="margin-bottom:0">
        <div class="f"><span>Group</span><i></i></div>
        <div class="f" style="flex:2 1 auto"><span>Your paper</span><i></i></div>
      </div>
    </div>
  </div>
</div>

<div class="page">
  <h1>What this day is for</h1>
  <div class="rule"></div>
  <p class="lede">By 16:30 you should be able to pick up an economic evaluation in your own field and say
  whether you believe it. Not whether the arithmetic is right, but whether the choices behind it, the
  comparator, the perspective, the time horizon, the outcome measure, add up to an answer you would act on.</p>
  <p>No prior training in health economics, modelling or statistics is assumed. Every exercise is on
  paper, or on your phone.</p>
  <h2 style="margin-top:8mm">How the day runs</h2>
  <p>Your group of three or four was handed <strong>one published Indian economic evaluation</strong> at
  registration, and keeps it all day. After each session you apply what was just taught to that paper,
  using the prompts on its sheet and the appraisal checklist in this kit. In Session 9 the groups report
  back in pairs, each pair chosen so that the two papers disagree in an instructive way.</p>
  <p>The morning takes a cost-effectiveness ratio apart and builds one. Only after lunch does the day ask
  what such a ratio is worth, which is why thresholds come sixth rather than third.</p>
  <h2 style="margin-top:8mm">One house rule</h2>
  <p class="lede">You are allowed to disagree with a published paper, and by this evening you should be
  able to say exactly which choice you disagree with. Publication is not a quality mark. Some of the
  papers in this room are strong and some are weak; finding out which is the exercise.</p>
  <p class="dim" style="margin-top:8mm">Everything here stays online afterwards, free to reuse and to
  pass on to your own students. The address is on the back cover.</p>
  {FOOT.format('What this day is for')}
</div>

<div class="page">
  <h1>The day</h1>
  <div class="rule"></div>
  <table>
    <tr><th>Time</th><th>&nbsp;</th><th>Session</th><th>What it covers</th></tr>
    {rows}
  </table>
  <p class="dim" style="margin-top:5mm; font-size:9.5pt">Timings are the plan, not a promise. The slides
  and handouts name sessions by number, so a session that runs long does not put anything in this kit out
  of step.</p>
  {FOOT.format('The day')}
</div>

<div class="page">
  <h1>Six things to try<br>on your own phone</h1>
  <div class="rule"></div>
  <p>Each takes a few minutes, explains the idea it makes visible, and works on a phone. Five appear
  during the day; all six are worth ten minutes on your own afterwards. Point your camera at a code.</p>
  <div class="qgrid">{qcells}</div>
  {FOOT.format('Interactive pages')}
</div>

<div class="page">
  <h1>Words you will hear today</h1>
  <div class="rule"></div>
  <div class="gl">{gl}</div>
  {FOOT.format('Glossary')}
</div>

</body></html>"""


def back() -> str:
    notes = "".join(
        f'<div class="page"><h2>Notes</h2><div class="rule"></div><div class="notesheet"></div>'
        f'{FOOT.format("Notes")}</div>' for _ in range(4))

    licences = [
        ("Sharma D, Prinja S, Aggarwal AK, Rajsekar K, Bahuguna P.",
         "Development of the Indian Reference Case for undertaking economic evaluation for health technology assessment.",
         "Lancet Reg Health Southeast Asia 2023;16:100241.", "CC BY-NC-ND 4.0"),
        ("Thiagarajan S, Sharda S, Chugh Y, Gupta N, Pramesh CS, Prinja S.",
         "Sentinel lymph-node biopsy guided neck dissection versus elective neck dissection in the management of early-stage oral cancer: a cost-utility analysis.",
         "Cancer Med 2026;15(2):e71571.", "CC BY 4.0"),
        ("Guleria M, et al.",
         "Review for cost-effectiveness analysis of laparoscopic intra-peritoneal onlay mesh repair for ventral hernia.",
         "Cost Eff Resour Alloc 2025;23(1):27.", "CC BY-NC-ND 4.0"),
        ("Kaur G, Chauhan AS, Prinja S, et al.",
         "Cost-effectiveness of population-based screening for diabetes and hypertension in India.",
         "Lancet Public Health 2022;7(1):e65-e73.", "CC BY-NC-ND 4.0"),
        ("Sharma J, et al.",
         "To compare cost effectiveness of Kangaroo Ward Care with Intermediate intensive care for stable very low birth weight infants.",
         "Ital J Pediatr 2016;42(1):64.", "CC BY 4.0"),
        ("Patel D, et al.",
         "Cost-effectiveness of noninvasive ventilation for chronic obstructive pulmonary disease-related respiratory failure in Indian hospitals without ICU facilities.",
         "Lung India 2015;32(6):549-556.", "CC BY-NC-SA 4.0"),
        ("Gupta N, et al.",
         "Peritoneal dialysis-first initiative in India: a cost-effectiveness analysis.",
         "Clin Kidney J 2022;15(1):128-135.", "CC BY-NC 4.0"),
        ("Srinivasan A, et al.",
         "Cost-effectiveness of treating childhood acute myeloid leukemia at a tertiary care centre in India.",
         "Pediatr Blood Cancer 2024;71(11):e31242.", "CC BY-NC-ND 4.0"),
    ]
    lic = "".join(
        f"<div><b>{a}</b> {t} <em>{j}</em> Reproduced unaltered under <b>{L}</b>.</div>"
        for a, t, j, L in licences)

    fb_rows = "".join(
        f'<div class="q"><p>{q}</p><div class="scale">'
        '<span>Not at all</span><span>A little</span><span>Fairly</span><span>Very</span><span>Completely</span>'
        '</div></div>'
        for q in [
            "I can now say whether a published economic evaluation answers a question worth answering.",
            "I can identify the comparator, perspective and time horizon in a paper, and say why each matters.",
            "I could explain an ICER, and its limits, to a colleague on Monday.",
            "I know where to find Indian unit-cost data for a study of my own.",
            "The paper my group worked on was the right level of difficulty.",
        ])

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Economic Evaluation in Health: participant kit, back matter</title><style>{CSS}</style></head><body>

<div class="page fb">
  <h1>Feedback</h1>
  <div class="rule"></div>
  <p class="dim">Please leave this page with us before you go. It decides what the next one of these
  looks like.</p>
  {fb_rows}
  <div class="q" style="flex:1 1 auto; display:flex; flex-direction:column">
    <p><strong>One thing that should be cut, and one thing that needed more time.</strong></p>
    <div class="lines" style="flex:1 1 auto; min-height:38mm"></div>
  </div>
  <div class="q" style="margin-bottom:0">
    <p><strong>Would you send a colleague to this? What would you tell them it is?</strong></p>
    <div class="lines" style="height:26mm"></div>
  </div>
  {FOOT.format('Feedback')}
</div>

{notes}

<div class="page">
  <h1>Sources and licences</h1>
  <div class="rule"></div>
  <p>The papers reproduced in this kit are published under Creative Commons licences that permit
  non-commercial redistribution. They appear unaltered, each with its original citation. No fee was
  charged for this workshop.</p>
  <div class="lic">{lic}</div>
  <p style="margin-top:6mm; font-size:9pt" class="dim">One paper used in the workshop,
  <strong>Uy FMM, et al. Cost-utility analysis of heart surgeries for young adults with severe rheumatic
  mitral valve disease, Int J Cardiol 2021;338:50-57</strong>, is not open access and could not be
  reproduced here. Its group has the citation and a link; AIIMS Bhopal holds institutional access.</p>
  <p style="margin-top:6mm; font-size:9pt" class="dim">The teaching material in this kit, the slides,
  checklist, worksheet and glossary, is licensed CC BY-NC-SA 4.0. Developed with Claude (Anthropic); the
  teaching judgements are human, and every citation and figure was verified against the primary source.</p>
  {FOOT.format('Sources and licences')}
</div>

<div class="page back">
  <img src="{qr_datauri(SITE)}">
  <p class="u">sph-aiimsbhopal.github.io/<br>intro-economic-evaluation-health</p>
  <p class="dim" style="max-width:120mm; margin-top:6mm">Every slide, handout and interactive page from
  today lives here, and stays here. Free to reuse and to pass on to your own students.</p>
  <p class="faint" style="margin-top:10mm; font-size:9pt">School of Public Health, with the Regional
  Resource Centre for Health Technology Assessment, AIIMS Bhopal<br>
  hta@aiimsbhopal.edu.in</p>
</div>

</body></html>"""


(OUT / "kit-front.html").write_text(front())
(OUT / "kit-back.html").write_text(back())
print(f"wrote {OUT/'kit-front.html'} and {OUT/'kit-back.html'}")
