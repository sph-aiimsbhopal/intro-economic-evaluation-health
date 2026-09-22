#!/usr/bin/env python3
"""Assemble the eight participant-kit variants.

    python3 kit-build.py

Each group's kit is identical except for its paper brief and the paper itself.
Reproduced papers are bound in unaltered, with a divider sheet before each that
carries the citation and the licence; nothing is stamped onto a paper's own
pages, because several are licensed NoDerivatives.

Expects, already built into kit/:
    kit-front.pdf  kit-back.pdf  kit-slides.pdf  checklist.pdf  reading-list.pdf
    papers/<file>.pdf
and in handouts/: costing-worksheet.pdf, paper-pack.pdf
"""
import pathlib, subprocess, sys, warnings
warnings.filterwarnings("ignore")
import pypdf

ROOT = pathlib.Path(__file__).parent.parent
KIT = ROOT / "kit"
OUT = KIT / "variants"
OUT.mkdir(parents=True, exist_ok=True)

# group number -> (short label, pdf file or None, full citation, licence or None)
GROUPS = {
 1: ("Thiagarajan 2026, sentinel node biopsy in early oral cancer", "Thiagarajan_2026.pdf",
     "Thiagarajan S, Sharda S, Chugh Y, Gupta N, Pramesh CS, Prinja S. Sentinel lymph-node biopsy guided "
     "neck dissection versus elective neck dissection in the management of early-stage oral cancer: a "
     "cost-utility analysis. Cancer Med 2026;15(2):e71571. PMID 41644818.", "CC BY 4.0"),
 2: ("Guleria 2025, laparoscopic IPOM for ventral hernia", "Guleria_2025.pdf",
     "Guleria M, et al. Review for cost-effectiveness analysis of laparoscopic intra-peritoneal onlay mesh "
     "repair for ventral hernia. Cost Eff Resour Alloc 2025;23(1):27. PMID 40495189.", "CC BY-NC-ND 4.0"),
 3: ("Uy 2021, surgery for rheumatic mitral valve disease", None,
     "Uy FMM, et al. Cost-utility analysis of heart surgeries for young adults with severe rheumatic mitral "
     "valve disease in the Philippines. Int J Cardiol 2021;338:50-57. PMID 34090957. "
     "doi:10.1016/j.ijcard.2021.05.059", None),
 4: ("Kaur 2022, population screening for diabetes and hypertension", "Kaur_2022.pdf",
     "Kaur G, Chauhan AS, Prinja S, et al. Cost-effectiveness of population-based screening for diabetes "
     "and hypertension in India: an economic modelling study. Lancet Public Health 2022;7(1):e65-e73. "
     "PMID 34774219.", "CC BY-NC-ND 4.0"),
 5: ("Sharma 2016, Kangaroo Ward Care for very low birth weight infants", "Sharma_2016.pdf",
     "Sharma D, et al. To compare cost effectiveness of 'Kangaroo Ward Care' with 'Intermediate intensive "
     "care' in stable very low birth weight infants: a randomized control trial. Ital J Pediatr "
     "2016;42(1):64. PMID 27412638.", "CC BY 4.0"),
 6: ("Patel 2015, ward-based NIV for COPD respiratory failure", "Patel_2015_workshop.pdf",
     "Patel D, et al. Cost-effectiveness of noninvasive ventilation for chronic obstructive pulmonary "
     "disease-related respiratory failure in Indian hospitals without ICU facilities. Lung India "
     "2015;32(6):549-556. PMID 26664158.", "CC BY-NC-SA 4.0"),
 7: ("Gupta 2022, peritoneal dialysis first", "Gupta_2022.pdf",
     "Gupta D, Jyani G, Ramachandran R, et al. Peritoneal dialysis-first initiative in India: a "
     "cost-effectiveness analysis. Clin Kidney J 2022;15(1):128-135. PMID 35035943.", "CC BY-NC 4.0"),
 8: ("Srinivasan 2024, childhood AML at a tertiary centre", "Srinivasan_2024.pdf",
     "Srinivasan A, et al. Cost-effectiveness of treating childhood acute myeloid leukemia at a tertiary "
     "care centre in India. Pediatr Blood Cancer 2024;71(11):e31242. PMID 39126354.", "CC BY-NC-ND 4.0"),
}

REFCASE = KIT / "papers" / "Sharma_2023_reference_case.pdf"
REFCASE_CITE = ("Sharma D, Prinja S, Aggarwal AK, Rajsekar K, Bahuguna P. Development of the Indian "
                "Reference Case for undertaking economic evaluation for health technology assessment. "
                "Lancet Reg Health Southeast Asia 2023;16:100241. PMID 37694178.")

DIV_CSS = """
@page { size: A4 portrait; margin: 0 }
* { box-sizing:border-box }
body { margin:0; font:10.5pt/1.5 Arial, Helvetica, sans-serif; color:#10141A;
       -webkit-print-color-adjust:exact; print-color-adjust:exact }
.page { width:210mm; height:297mm; padding:40mm 22mm 20mm; page-break-after:always;
        display:flex; flex-direction:column }
.page:last-child { page-break-after:auto }
.kick { font-size:8.5pt; letter-spacing:.14em; text-transform:uppercase; color:#7A8394; margin:0 0 4mm }
h1 { font-size:24pt; line-height:1.15; color:#162a6c; margin:0 0 6mm; font-weight:700 }
.rule { height:2.2pt; background:#162a6c; margin:0 0 7mm; width:40mm }
.cite { font-size:10.5pt; line-height:1.55; margin:0 0 6mm; max-width:150mm }
.lic { font-size:9.5pt; color:#5A6273; border-left:3pt solid #162a6c; padding-left:5mm; margin:0 0 8mm }
.note { font-size:10pt; color:#222833; max-width:150mm }
.note b { color:#162a6c }

.page.nt { padding:18mm 18mm 16mm }
.nt .ntk { font-size:8.5pt; letter-spacing:.14em; text-transform:uppercase; color:#7A8394;
           display:flex; justify-content:space-between; margin:0 0 4mm }
.nt .ln { height:8mm; border-bottom:.4pt solid #BFC6D4 }
"""


def divider_pdf(pages_html, out):
    src = KIT / "_div.html"
    src.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{DIV_CSS}</style>"
                   f"</head><body>{''.join(pages_html)}</body></html>")
    subprocess.run(["node", "/home/claude/tools/pdf.mjs", "kit/_div.html", str(out)],
                   check=True, capture_output=True)
    src.unlink()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_dividers():
    """One PDF per divider, built in a single browser run for speed."""
    order = []
    pages = []

    pages.append(f"""<div class="page">
      <p class="kick">Reference</p><h1>The Indian<br>Reference Case</h1><div class="rule"></div>
      <p class="cite">{esc(REFCASE_CITE)}</p>
      <p class="lic">Reproduced unaltered under CC BY-NC-ND 4.0.</p>
      <p class="note">Eleven principles and twelve recommendations, written for India by the group behind
      most of the papers cited today. The appraisal checklist in this kit is this document turned into a
      form. <b>This is the thing to keep.</b> When you next referee a paper, or design a study of your
      own, it is the document that settles the method questions before they become arguments.</p>
    </div>""")
    order.append("refcase")

    for g, (short, pdf, cite, lic) in GROUPS.items():
        if pdf:
            body = (f'<p class="lic">Reproduced unaltered under {lic}.</p>'
                    f'<p class="note">This is the paper your group holds. The prompts on your paper\'s '
                    f'sheet, earlier in this kit, take you through it session by session. By Session 9 you '
                    f'should be able to say whether you would act on it, and which single choice in it you '
                    f'would most want to argue about.</p>')
        else:
            body = ('<p class="lic">Not reproduced here: this journal is subscription-only and carries no '
                    'licence permitting redistribution.</p>'
                    '<p class="note">AIIMS Bhopal holds institutional access, and the article is on the '
                    'publisher\'s site at the DOI above. Your facilitator has a reading copy for the day. '
                    '<b>Everything else works the same:</b> the prompts on your paper\'s sheet, earlier in '
                    'this kit, take you through it session by session.</p>')
        pages.append(f"""<div class="page">
          <p class="kick">Your group's paper &middot; Group {g}</p>
          <h1>{esc(short)}</h1><div class="rule"></div>
          <p class="cite">{esc(cite)}</p>
          {body}
        </div>""")
        order.append(f"g{g}")

    for n in range(1, 5):                       # four ruled pages at the back of every kit
        pages.append(f"""<div class="page nt">
          <p class="ntk"><span>Notes</span><span>Economic Evaluation in Health &middot; AIIMS Bhopal
          &middot; 23 September 2026</span></p>
          {'<div class="ln"></div>' * 31}
        </div>""")
        order.append(f"notes{n}")

    divider_pdf(pages, KIT / "_dividers.pdf")
    return order


def main():
    need = ["kit-front.pdf", "kit-back.pdf", "kit-slides.pdf", "checklist.pdf", "reading-list.pdf"]
    missing = [n for n in need if not (KIT / n).exists()]
    if missing:
        sys.exit("missing: " + ", ".join(missing))

    order = build_dividers()
    div = pypdf.PdfReader(KIT / "_dividers.pdf")
    div_page = {name: i for i, name in enumerate(order)}

    front = pypdf.PdfReader(KIT / "kit-front.pdf")
    back = pypdf.PdfReader(KIT / "kit-back.pdf")
    slides = pypdf.PdfReader(KIT / "kit-slides.pdf")
    checklist = pypdf.PdfReader(KIT / "checklist.pdf")
    reading = pypdf.PdfReader(KIT / "reading-list.pdf")
    worksheet = pypdf.PdfReader(ROOT / "handouts" / "costing-worksheet.pdf")
    pack = pypdf.PdfReader(ROOT / "handouts" / "paper-pack.pdf")
    refcase = pypdf.PdfReader(REFCASE) if REFCASE.exists() else None
    if refcase is None:
        print("  note: Sharma_2023_reference_case.pdf not present, leaving it out for now")

    for g, (short, pdf, cite, lic) in GROUPS.items():
        w = pypdf.PdfWriter()
        for p in front.pages:                    w.add_page(p)     # cover, the day, widgets, glossary
        w.add_page(pack.pages[g])                                  # this group's paper brief
        for p in checklist.pages:                w.add_page(p)
        for p in worksheet.pages:                w.add_page(p)
        for p in slides.pages:                   w.add_page(p)
        for p in reading.pages:                  w.add_page(p)
        if refcase:
            w.add_page(div.pages[div_page["refcase"]])
            for p in refcase.pages:              w.add_page(p)
        w.add_page(div.pages[div_page[f"g{g}"]])
        if pdf:
            for p in pypdf.PdfReader(KIT / "papers" / pdf).pages:
                w.add_page(p)
        for p in back.pages:                     w.add_page(p)
        for n in range(1, 5):
            w.add_page(div.pages[div_page[f"notes{n}"]])

        out = OUT / f"kit-group-{g}.pdf"
        with open(out, "wb") as fh:
            w.write(fh)
        mb = out.stat().st_size / 1048576
        print(f"  group {g}: {len(w.pages):3d} pages, {mb:5.1f} MB  {short}")

    (KIT / "_dividers.pdf").unlink()


if __name__ == "__main__":
    main()
