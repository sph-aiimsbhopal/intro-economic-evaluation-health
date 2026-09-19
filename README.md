# Economic Evaluation in Health

**A one-day workshop at AIIMS Bhopal, Wednesday 23 September 2026, 09:30 to 16:30**
SAMVAD (Board Room, First Floor, Medical College Building), AIIMS Bhopal, Saket Nagar
School of Public Health, with the Regional Resource Centre for Health Technology Assessment
Open to faculty, senior and junior residents, and research project staff, across departments.
Enquiries: hta@aiimsbhopal.edu.in

Everything used on the day is here, and stays here afterwards:
**[open the workshop page](https://sph-aiimsbhopal.github.io/intro-economic-evaluation-health/)**

## What the day is for

By 16:30 you should be able to pick up an economic evaluation in your own field and say whether you
believe it. Not whether the arithmetic is right, but whether the choices behind it, the comparator,
the perspective, the time horizon, the outcome measure, add up to an answer you would act on.

No prior training in health economics, modelling or statistics is assumed. Every exercise is on paper,
or on your phone.

## How the day runs

Your group of three or four is handed **one published Indian economic evaluation** at registration,
and keeps it all day. After each session you apply what was just taught to that paper, using the
prompts on its sheet and the appraisal checklist. In the second-last session, groups report back in
pairs, each pair chosen so that the two papers disagree in an instructive way.

| | Session |
|---|---|
| 1 | Where economic evidence enters health policy |
| 2 | What economic evaluation is, and what it is not |
| 3 | Thresholds, opportunity cost and budget impact |
| 4 | Costing your own service, with a worksheet |
| 5 | Framing the question |
| 6 | Outcomes, discounting and the ICER |
| 7 | Modelling in half an hour |
| 8 | Handling uncertainty |
| 9 | Group appraisal report-back |
| 10 | Close and feedback |

The [programme](EE-Health-Workshop-Agenda.pdf) and the [brochure](EE-Health-Workshop-Brochure.pdf)
have the full timings and the registration details.

## Try these on your phone

Six short interactive pages. Each takes a few minutes, explains the idea it makes visible, and works
on a phone. Five of them appear during the day.

| Widget | What it makes visible |
|---|---|
| [Classify the study](widgets/classifier/) | full evaluation or partial, in two questions |
| [Which costs count](widgets/cost-classifier/) | direct or indirect, and under whose perspective |
| [QALY builder](widgets/qaly-builder/) | a QALY is an area, and three different lives give the same one |
| [Discounting](widgets/discounting/) | why prevention looks worse than treatment |
| [The cost-effectiveness plane](widgets/ce-plane/) | quadrants, dominance, and the threshold line |
| [Uncertainty](widgets/uncertainty/) | tornado, the cloud of simulations, and the curve it makes |

## Slides and handouts

All eight decks are in [`slides/`](slides/) and open in any browser, with no internet needed. Arrow
keys move, **Esc** shows the overview.

Each deck also downloads as an **editable PowerPoint file** (`slides/<deck>.pptx`), linked from the
[workshop page](https://sph-aiimsbhopal.github.io/intro-economic-evaluation-health/). The text is real
text you can rewrite, the speaker notes travel with it, and the layout matches the browser version.
Diagrams, equations and the embedded widgets arrive as pictures, since PowerPoint has no equivalent.

| Handout | What it is |
|---|---|
| [Appraisal checklist](handouts/appraisal-checklist.html) | the eleven principles of the Indian Reference Case, as a form to fill in |
| [Paper pack](handouts/paper-pack.pdf) | the eight papers, one page each, with a prompt for every session |
| [Costing worksheet](handouts/costing-worksheet.pdf) | two pages of A4 for the Session 4 exercise |
| [Reading list](handouts/reading-list.html) | every citation used in the day, annotated |

## Use of AI

These slides, widgets and handouts were developed with **Claude** (Anthropic), which compressed months
of drafting into days: building the decks and the interactive widgets, assembling the paper pack, and
turning the Indian Reference Case into an appraisal form.

The teaching judgements are human: what to cover, what to cut, which papers to set, and what each
session should leave people able to do. **Every citation, figure and PMID was verified against the
primary source**, and the organising team is responsible for the content.

## After the day

The slides, handouts and widgets stay at this address, so you can reuse them when you teach, or send
a link to a colleague who asks what an ICER is. Teaching content is licensed
[CC BY-NC-SA 4.0](LICENSE-CONTENT.md) and the code [MIT](LICENSE). The published studies discussed
here belong to their authors and publishers and are not reproduced.

---

## Running the workshop

Facilitators start with **[`handouts/faculty-blueprint.md`](handouts/faculty-blueprint.md)**: the run
sheet, with timings, group logistics, roles, which slides to skip, and the print list. The
[paper pack key](handouts/paper-pack-facilitator.pdf) and the
[poll question bank](handouts/poll-bank.html) are for facilitators, not participants.

The generated handouts are rebuilt from their sources:

```bash
cd handouts
python3 build_paperpack.py    # paper-pack.html + the facilitator key, from papers.py
python3 build_polls.py        # poll-bank.html + poll-bank.xlsx
```

The brochure and agenda are rebuilt from `src/` (see `src/README.md`). PDFs are printed from the HTML
at A4; every sheet is sized to one page, so check nothing has spilled off the bottom before printing.

The PowerPoint files are generated, not hand-made. After editing a deck, rebuild them:

```bash
cd src && ./pptx-all.sh
```

`pptx-extract.mjs` measures every block in the rendered deck (position, size, font, colour) and
screenshots only what cannot be text; `pptx-build.py` writes those measurements out as native
PowerPoint text boxes, shapes and tables. Check the result before shipping: the fastest way is
`soffice --headless --convert-to pdf slides/<deck>.pptx` and a look at the pages.

**House conventions.** Decks are 1280 x 720 with a 14 pt floor: a slide that does not fit is split or
shortened, never scaled down. No em dashes in slides or widgets. Every published study cited is
checked against its PubMed record, and constructed teaching examples are labelled as constructed. After
editing a deck, serve this folder and run the checker, which reports content past 700 px of the 720 px
slide, em dashes and HTTP errors:

```bash
python3 -m http.server 8765
node src/chk.mjs opening block1 block2 costing block3a block3b modelling block3c
```

**Publishing.** Pushing to `main` publishes the site through `.github/workflows/pages.yml`. The site
address is printed on the widget slides and encoded in the QR code on the Session 1 slide
(`assets/img/site-qr.png`); if the repository is renamed, regenerate the QR and update those slides
together.
