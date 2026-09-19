# Economic Evaluation in Health: faculty workshop, 23 September 2026

One-day workshop for about 25 faculty and senior residents at **AIIMS Bhopal**, hosted by the School of
Public Health with the Regional Resource Centre for Health Technology Assessment.
Convener: Dr Abhijit P. Pakhare.

Everything needed to run the day is in this folder, and it works with **no internet**: reveal.js is
vendored in `vendor/`. Open `index.html` to start.

## What is here

| Folder | Contents |
|---|---|
| `slides/` | Eight decks: `opening`, `block1`, `block2`, `costing`, `block3a`, `block3b`, `modelling`, `block3c` |
| `handouts/` | Paper pack (participant and facilitator versions), appraisal checklist, costing worksheet, poll bank, reading list, run sheet |
| `widgets/` | Six standalone interactive pages, phone friendly |
| `assets/` | Styles and design tokens |
| `src/` | Sources and build scripts for the brochure and the agenda |

Start with **`handouts/faculty-blueprint.md`**: the run sheet, with timings, group logistics, roles,
which slides to skip, and the print list.

## The mechanic of the day

Each group of three holds **one published Indian economic evaluation** at registration and works on it
all day, applying each session to it using the prompts on its sheet and the appraisal checklist. At
15:55 the groups report back in **four pairs**, each pair chosen so the two papers contrast.

## Rebuilding the generated handouts

```bash
cd handouts
python3 build_paperpack.py    # paper-pack.html + paper-pack-facilitator.html, from papers.py
python3 build_polls.py        # poll-bank.html + poll-bank.xlsx
```

The PDFs are printed from those HTML files at A4. Each sheet is sized to one page; if you edit the
content, check that nothing has spilled off the bottom before printing.

## House conventions

- Decks are **1280 x 720**, with a **14 pt floor**. A slide that does not fit is split or shortened,
  never scaled down.
- **No em dashes** anywhere in slides or widgets.
- Every published study cited has been checked against its PubMed record. Constructed teaching examples
  are labelled as constructed on the slide.
- After editing any deck, serve this folder and run the checker from the course repository
  (`src/chk.mjs` in the workshop folder):

```bash
python3 -m http.server 8765
node chk.mjs opening block1 block2 costing block3a block3b modelling block3c
```

It reports content past 700 px of the 720 px slide, em dashes, and HTTP errors.

## Where the material came from

The five teaching blocks began as a postgraduate course, *Introduction to Economic Evaluation in
Health* (a separate repository), and were adapted here for a faculty audience: audience lines,
speaker notes and examples were rewritten, and session times added to the covers. The opening, costing
and modelling decks, the paper pack, the costing worksheet, the poll bank and the run sheet were
written for this day.

Teaching content is licensed **CC BY-NC-SA 4.0** (`LICENSE-CONTENT.md`); code is **MIT** (`LICENSE`).
Published studies cited in these materials belong to their authors and publishers and are not
reproduced here.
