# Faculty workshop — handover to a new session

**Workshop:** Economic Evaluation in Health
**Date:** Wednesday, 23 September 2026, 09:30–16:30
**Host:** School of Public Health, AIIMS Bhopal, with the Regional Resource Centre for HTA, AIIMS Bhopal
**Audience:** ~25 faculty and senior residents, mixed departments
**Convener:** Dr Abhijit P. Pakhare

This file exists so a fresh session can pick the work up without the previous
conversation. Everything below was decided or verified in that conversation and
exists nowhere else.

---

## 1. Where things stand

**Done and on disk** (this folder, `faculty-workshop-2026-09-23/`):

| File | What it is |
|------|------------|
| `EE-Health-Workshop-Brochure.pdf` | 2-page A4 brochure, print-ready |
| `EE-Health-Workshop-Agenda.pdf` | 1-page A4 programme sheet |
| `brochure.html`, `agenda.html` | the built, self-contained pages (logos embedded) |
| `src/` | editable sources + build scripts (see §6) |

**Registration form is live:** <https://forms.gle/Te2jRPjubgbfywmm8>
Title "Economic Evaluation in Health (23rd Sep 2026)"; collects name,
designation, department, contact, prior knowledge. The brochure QR encodes this
short link.

**Still blank on the printed pieces — fill before circulating:**

1. **Venue room** (brochure details bar says only "AIIMS Bhopal, Saket Nagar")
2. **Contact e-mail** (currently `hta@aiimsbhopal.edu.in` — confirm it is right
   for a School of Public Health event)
3. **Facilitator column on the agenda** — deliberately left empty; the convener
   fills the names

**19 Sep 2026: this folder is now a standalone git repository.** The workshop no longer lives inside
the PG course repo, which is a different course. This folder holds everything needed to run the day and
works offline: `index.html` (landing page), `slides/` (8 decks), `handouts/`, `widgets/`, `assets/`,
`vendor/` (reveal.js), plus the brochure, the agenda and their sources in `src/`. One commit on `main`,
no remote yet. Start from `handouts/faculty-blueprint.md`.

The five teaching blocks were copied from the PG course and **adapted for this audience**: the
"MD Community Medicine" line became "Faculty and senior residents", cover kickers carry the session
time instead of a block number, and speaker notes and a few slide lines written for exam-facing
residents (dissertation, viva, "students") were rewritten for faculty who supervise, sit on committees
and referee. No teaching content, figure or citation changed. All eight decks pass `src/chk.mjs`.

New for this day: `slides/opening.html`, `costing.html`, `modelling.html`; `handouts/paper-pack.pdf`
(and the facilitator key), `costing-worksheet.pdf`, `poll-bank.html` + `.xlsx`, `faculty-blueprint.md`.
The paper pack is generated from `handouts/papers.py` by `build_paperpack.py`.

Citation corrections found while verifying: Gupta is **2022**, not 2021; Srinivasan is **open access**
(CC BY-NC-ND); the published Comment on it is **2025;72(1):e31305, PMID 39228042**.

**Registration form is live:** <https://forms.gle/Te2jRPjubgbfywmm8>
Title "Economic Evaluation in Health (23rd Sep 2026)"; collects name,
designation, department, contact, prior knowledge. The brochure QR encodes this
short link.

**Still blank on the printed pieces — fill before circulating:**

1. **Venue room** (brochure details bar says only "AIIMS Bhopal, Saket Nagar")
2. **Contact e-mail** (currently `hta@aiimsbhopal.edu.in` — confirm it is right
   for a School of Public Health event)
3. **Facilitator column on the agenda** — deliberately left empty; the convener
   fills the names

**Built 18 Sep 2026 (second session):** all seven items in §4, in the repo clone, not yet committed
to git. Start from `handouts/faculty-blueprint.md`, which is the run sheet and lists every new file.
New decks: `slides/opening.html`, `costing.html`, `modelling.html` (all pass chk.mjs, as do the five
PG decks). Handouts: `paper-pack.pdf` (participants), `paper-pack-facilitator.pdf` (key, do not hand
out), `costing-worksheet.pdf`, `poll-bank.html` + `.xlsx`. Paper pack is generated from
`handouts/papers.py` by `build_paperpack.py`. Corrections found: Gupta is 2022 not 2021; Srinivasan
is open access (CC BY-NC-ND); the Comment on it is 2025;72(1):e31305. The new files are not yet
linked from `index.html`.

---

## 2. What already exists in the repository

Repo: <https://github.com/sph-aiimsbhopal/intro-economic-evaluation-health>
Site: <https://sph-aiimsbhopal.github.io/intro-economic-evaluation-health/>
Local clone: `../intro-economic-evaluation-health/` (same parent folder)

Built for the PG course and **reusable as-is for most of the faculty day**:

| Asset | Contents |
|-------|----------|
| `slides/block1.html` | 26 slides — what economic evaluation is / is not |
| `slides/block2.html` | 23 slides — thresholds, opportunity cost, HTAIn, budget impact |
| `slides/block3a.html` | 17 slides — decision problem, comparator, perspective, horizon |
| `slides/block3b.html` | 25 slides — QALYs, discounting, ICER, NMB (incl. formula slides) |
| `slides/block3c.html` | 22 slides — DSA, PSA, CEAC |
| `widgets/` | 6 standalone interactive pages, phone-friendly |
| `handouts/appraisal-checklist.html` | 11 Reference Case principles as a printable form |
| `handouts/reading-list.html` | every citation, PMIDs verified |
| `handouts/blueprint.md` | instructor notes for the PG version |

### Repository state — read this before touching git

- The project **moved** from `drpakhare/` to the `sph-aiimsbhopal/` organisation.
- `README.md` and `PUBLISHING.md` were edited to the new URLs **but are not
  committed and not pushed**.
- The local clone sits inside Dropbox and accumulates **stale git lock files**
  that the Cowork device bridge cannot delete. Before any git work, the user must
  run in Terminal:
  ```bash
  cd ~/Dropbox/HTAIn/"Introduction to Economic Evaluation in Health"/intro-economic-evaluation-health
  rm -f .git/*.lock
  git remote set-url origin https://github.com/sph-aiimsbhopal/intro-economic-evaluation-health.git
  ```
- A `_to_delete/` folder in the parent holds superseded files; safe to remove.
- GitHub Pages must be switched on for the new repo: **Settings → Pages → Source:
  GitHub Actions**.

---

## 3. The day, as designed

Welcome and close are brief (10 min each); no formal inaugural. Arithmetic is exact.

| Time | Session | Min |
|------|---------|-----|
| 09:30 | Registration and welcome | 10 |
| 09:40 | **Where economic evidence enters health policy** | 20 |
| 10:00 | What economic evaluation is, and what it is not | 40 |
| 10:40 | Thresholds, opportunity cost and budget impact | 40 |
| 11:20 | *Tea* | 20 |
| 11:40 | **Costing your own service** — worksheet, hands-on | 55 |
| 12:35 | Framing the question | 40 |
| 13:15 | *Lunch* | 50 |
| 14:05 | Outcomes, discounting and the ICER | 40 |
| 14:45 | **Modelling in half an hour** | 25 |
| 15:10 | *Tea* | 15 |
| 15:25 | Handling uncertainty | 30 |
| 15:55 | Group appraisal report-back | 25 |
| 16:20 | Close and feedback | 10 |

**Bold = new material that does not exist yet.**

### The mechanic that holds the day together

Each group is handed **one published economic evaluation at registration** and
works on it all day, applying each principle to that paper as it is taught. By
15:55 the appraisal form is already filled in, so the final slot is pure
report-back. This is why the report-back fits in 25 minutes and why nobody has to
read a paper cold after lunch.

25 participants → **8 groups of 3**. Eight report-backs will not fit 25 minutes,
so they are **paired by specialty: 4 contrasts, 6 minutes each**. Each pair is a
designed contrast (see §5).

---

## 4. What needs building

Priority order. There are only a few days, so build top-down and stop where time
runs out — the existing five blocks already cover most of the day.

1. **Paper pack** — eight one-page briefs, one per paper (§5), to go in the
   folder with the existing appraisal checklist. Highest value, lowest effort.
2. **Poll question bank** — Socrative-style MCQs timed to each session. No
   laptops in the room; participants answer on phones. Roughly 2–3 questions per
   session, ~20 total.
3. **Costing worksheet** — paper, A4, for the 55-minute hands-on session.
   Participants cost one episode of care in their own department.
4. **Costing slides** (~20) — micro vs gross costing, bottom-up vs top-down,
   step-down allocation of shared overheads, annuitising capital, and where
   Indian unit-cost data already exists (NHSCD, CHSI, PMJAY rates, HTAIn costing
   handbook).
5. **Modelling slides** (~14) — decision tree vs Markov at *reading* level: why a
   model exists, what a cycle is, what to distrust. Not model-building.
6. **Opening slides** (~8) — "Where economic evidence enters health policy".
   How decisions get made in India, who asks the questions, where clinicians and
   researchers come in. Replaces the PG deck's opening.
7. **Facilitator blueprint** — timings, group logistics, who runs what.

### Content decisions already made

- **Keep cervical cancer as the worked spine** running through the existing
  blocks. Do not re-spine the course — every figure in it is verified and
  re-doing it risks introducing citation errors. Specialty relevance comes from
  the paper pack, not from rewriting the slides.
- **Budget impact** belongs beside "cost-effective is not the same as funded" in
  Block 2, not as its own session.
- **Cut for this audience:** the six-box classification grid in depth, extended
  dominance, the QALY-vs-DALY argument, the discounting derivation.
- Framing throughout is **research and appraisal**, not "justify your department
  to a purchase committee" — that framing was explicitly rejected.
- "Clinical faculty" is deliberately de-emphasised; the day is open to faculty
  and senior residents across departments.

---

## 5. The eight appraisal papers

Chosen to vary deliberately in method and quality — a pack where every paper is
excellent teaches nothing. Two per specialty cluster.

### Oncology and surgery

**1. Thiagarajan S, et al.** Sentinel lymph-node biopsy guided neck dissection
versus elective neck dissection in the management of early-stage oral cancer — a
cost-utility analysis. *Cancer Medicine* 2026. **PMID 41644818.**
Markov, payer perspective, lifetime horizon, 3% discounting, one-way + PSA, 94%
probability of cost-effectiveness.
*Teaching point:* judges against 1× GDP per capita, the rule the day will already
have taught them was retired by its own authors. A live disagreement with a paper.

**2. Guleria C, Kumar D, Sahoo KC.** Review for cost-effectiveness analysis of
laparoscopic intra-peritoneal onlay mesh for ventral hernia repair in Indian
settings. *Cost Eff Resour Alloc* 2025;23(1):27. **PMID 40495189.** Open access.
An **HTAIn study**. NHSCD costs, meta-analysis of RCTs.
*Teaching points:* outcome is cost per **wound infection averted** — a natural
unit that cannot go in any league table; and it concludes the technology is **not**
cost-effective, which is rare in print.

### Cardiology and medicine

**3. Uy J, et al.** Cost-utility analysis of heart surgeries for young adults with
severe rheumatic mitral valve disease in India. *Int J Cardiol* 2021.
**PMID 34090957.** Markov, public payer, QALYs, DSA + PSA. Repair dominates the
standard of care.
*Teaching point:* a dominant strategy that is nonetheless not what most centres
do — the gap between analysis and practice is the discussion.

**4. Kaur G, et al.** Cost-effectiveness of population-based screening for
diabetes and hypertension in India: an economic modelling study.
*Lancet Public Health* 2022;7(1):e65–e73. **PMID 34774219** (verified 18 Sep 2026, Europe PMC MEDLINE record + DOI 10.1016/S2468-2667(21)00199-7; epub 12 Nov 2021).
DHR-funded. Hybrid decision tree + Markov, societal perspective, NHSCD and CHSI
costs, primary utility collection in 962 patients, PSA.
*Teaching point:* the conclusion flips on a **health-system** assumption — what
share of newly diagnosed patients Health and Wellness Centres actually treat —
not on anything clinical. Best paper in the pack for showing where an ICER really
comes from.

### Critical care, anaesthesia, neonatology

**5. Sharma D, et al.** To compare cost effectiveness of "Kangaroo Ward Care" with
"Intermediate intensive care" in stable very low birth weight infants (birth
weight < 1100 grams): a randomized control trial. *Ital J Pediatr* 2016.
**PMID 27412638.** Open access.
*Teaching point:* **the deliberately weak paper.** Titled a cost-effectiveness
analysis; actually a cost comparison. No QALYs or DALYs, no discounting, no
sensitivity analysis, horizon ends at discharge. A good group takes it apart in
fifteen minutes — that is the point.

**6. Patel SP, et al.** Cost-effectiveness of noninvasive ventilation for chronic
obstructive pulmonary disease-related respiratory failure in Indian hospitals
without ICU facilities. *Lung India* 2015. **PMID 26664158.** Open access.
Decision-analytic, lifetime, societal, 3% discounting, QALYs, one-way, two-way
and probabilistic analysis. Technically competent.
*Teaching points:* every parameter from published literature rather than Indian
primary data; judges against GDP per capita, in 2012 USD.

### Paediatrics, infectious disease, nephrology

**7. Gupta D, et al.** Peritoneal dialysis–first initiative in India: a
cost-effectiveness analysis. *Clin Kidney J* **2022;15(1):128–135** (epub 15 Jul 2021; cite as 2022). **PMID 35035943**, PMC8757426,
DOI 10.1093/ckj/sfab126 (verified 18 Sep 2026). Open access.
Markov, societal, models the real Pradhan Mantri National Dialysis Programme
scenario alongside current practice.
*Teaching point:* reports the **price at which PD consumables would have to be
procured** (≈ INR 70/unit) for the policy to be cost-effective on direct costs
alone — an analysis that ends in a negotiating position rather than a verdict.

**8. Srinivasan S, et al.** Cost-effectiveness of treating childhood acute myeloid
leukemia at a tertiary care center in North India. *Pediatr Blood Cancer* 2024.
**PMID 39126354.** Retrospective real-world costs and outcomes, cost per DALY
averted, 30% treatment-related mortality.
*Teaching points:* DALYs rather than QALYs, so it cannot be compared with the
other seven; and there is a **published Comment on it (PMID 39228042)**, letting
that group compare their own appraisal against a peer-reviewed one.

### Suggested pairing for the report-back

| Pair | Contrast |
|------|----------|
| Thiagarajan × Guleria | a well-built model vs one concluding *not* cost-effective |
| Kaur × Uy | policy-assumption-driven vs clinically-driven conclusion |
| Sharma × Patel | a paper that is not really a CEA vs a competent one |
| Gupta × Srinivasan | ends in a price negotiation vs ends in a DALY ratio |

> **Resolved 18 Sep 2026:** papers 4 and 7 verified (PMIDs 34774219, 35035943). Originally: **Two PMIDs (papers 4 and 7) were unconfirmed.** PubMed and Europe PMC were both
> rate-limiting. Verify both before anything is printed — the project standard is
> that every citation is checked against PubMed, authors, journal, year, volume,
> pages and PMID.

---

## 6. House conventions — keep these

**Slides**

- Geometry **1280 × 720** (true 16:9 at 96 px/inch, so 1 pt = 1.333 px).
- Type scale in `assets/css/slides.css`: band title 40 pt, cover 54 pt, claim
  32 pt, lede 30 pt, body 28 pt, small 22 pt, table 21 pt, citation 14 pt.
- **Nothing smaller than 14 pt.** A slide that does not fit gets split or
  shortened, never scaled down.
- reveal.js 5.1.0 is **vendored** in `vendor/` so decks work with no internet.
- Navy title band `#162a6c`, Arial — from the supplied PowerPoint template.
- **No em dashes** anywhere in slides or widgets (a standing request).
- Citations trimmed to author/journal/year on the slide; full reference on a
  **Sources** slide closing each deck.
- Speaker notes exist on every slide but **no slide tells the audience to press S**.

**Verification**

- `src/chk.mjs` walks every slide of a deck in a headless browser and reports
  overflow past 700 px, em-dash count and HTTP errors. **Run it after any slide
  edit.** Usage: serve the repo root on port 8765, then
  `node chk.mjs block1 block2 block3a block3b block3c`.
  It measures each slide **while it is the present one** — reveal.js hides the
  others and hidden elements return zero-size rects, which once produced a silent
  all-clear on a deck with 18 real overflows.
- Every published study cited anywhere is checked against PubMed. Constructed
  teaching examples are labelled as constructed on the slide.

**Print pieces**

- A4, Lato, palette driven entirely by CSS custom properties in the `:root` block.
- `src/palettes.py <name>` recolours both brochure and agenda in one command;
  `indigo` is the current scheme (`teal` was the earlier R-workshop scheme, kept
  for reference; `maroon` and `charcoal` are alternatives).
- Rebuild: `python3 build.py` then `node topdf.mjs` (brochure) /
  `node agendapdf.mjs` (agenda). `meas.mjs` reports whether each page still fits
  exactly within 297 mm.

---

## 7. Open questions for the convener

1. Venue room, and confirmed contact e-mail.
2. Facilitator allocation across the six resource persons.
3. Whether lunch is confirmed — it was removed from the brochure's details bar
   but still appears in the page-2 registration panel and as a row in the agenda.
4. Whether the closing session should end with a concrete next step. The brochure
   promises participants will "take part in producing" HTA evidence; that
   promise needs an answer by 16:30.
