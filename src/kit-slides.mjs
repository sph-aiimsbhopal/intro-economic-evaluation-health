// Participant kit, slides section: two slides to an A4 portrait page, each the
// full width of the text block with ruled space beneath to write in, and a
// divider page before each session.
//
//   node kit-slides.mjs [outfile]
//
// Needs a static server on the repo root at :8766.
//
// At 186 mm the slide sits at 0.55 of its projected size, so the deck's 14 pt
// floor prints at about 7.7 pt and body text at about 11 pt. Four to a page
// would be 0.26 and put the floor at 3.6 pt, which is why this is a 2-up.
import { chromium } from 'playwright';
import { mkdtempSync, rmSync, readFileSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const out = process.argv[2] || '/home/claude/ws/kit/kit-slides.pdf';

// session number, deck, title, and whether the deck ends with a cover for the
// next session (redundant here, since the kit has divider pages)
const DECKS = [
  ['1', 'opening',   'Where economic evidence enters health policy', false],
  ['2', 'block1',    'What economic evaluation is, and what it is not', true],
  ['3', 'block3a',   'Framing the question', true],
  ['4', 'costing',   'Costing your own service', false],
  ['5', 'block3b',   'Outcomes, discounting and the ICER', true],
  ['6', 'block2',    'Thresholds, opportunity cost and budget impact', true],
  ['7', 'modelling', 'Modelling in half an hour', false],
  ['8', 'block3c',   'Handling uncertainty', false],
];

// what each session adds, and which Reference Case rows it covers
const ADDS = {
  '1': ['How decisions about what the health system pays for are actually made in India, who asks the questions, and where you come into it.', 'is this evidence anyone will act on?'],
  '2': ['Opportunity cost. The two questions that sort every study into six boxes. Why a trial is a partial evaluation.', 'is it an economic evaluation at all?'],
  '3': ['Decision problem, comparator, perspective, time horizon. The four choices made before any arithmetic.', '1, 2, 3, 7'],
  '4': ['Identify, measure, value. Micro-costing against gross costing, shared overheads, annuitised capital, and where Indian unit costs already exist.', '5'],
  '5': ['What a QALY is and where its weights come from. Discounting. Average against incremental, dominance, and the ICER.', '6, 8, 12'],
  '6': ['Where a threshold comes from, India’s own estimate, and why affordability this year is a separate test from cost-effectiveness.', 'the yardstick the verdict is held against'],
  '7': ['Decision trees and Markov models at reading level: why a model exists, what a cycle is, and what to distrust in a published one.', '4'],
  '8': ['One-way and probabilistic sensitivity analysis, the tornado diagram, the cloud, and the acceptability curve.', '9, 10'],
};

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const work = mkdtempSync(join(tmpdir(), 'kit-'));
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.6 });
const p = await ctx.newPage();

const blocks = [];          // divider pages and slide blocks, in reading order

for (const [sess, deck, title, dropLast] of DECKS) {
  await p.goto(`http://localhost:8766/slides/${deck}.html`);
  await p.evaluate(() => Reveal.configure({ transition: 'none', backgroundTransition: 'none' }));
  await p.addStyleTag({ content: '.reveal .controls, .reveal .progress, .reveal .slide-number { display:none !important }' });
  await p.waitForTimeout(1100);

  const total = await p.evaluate(() => Reveal.getTotalSlides());
  const last = dropLast ? total - 1 : total;       // the trailing next-session cover
  blocks.push({ kind: 'divider', sess, title, slides: last });

  for (let i = 0; i < last; i++) {
    await p.evaluate(n => Reveal.slide(n), i);
    await p.waitForTimeout(260);
    const file = join(work, `${deck}-${i}.png`);
    await p.screenshot({ path: file });
    blocks.push({
      kind: 'slide', sess, n: i + 1,
      src: 'data:image/png;base64,' + readFileSync(file).toString('base64'),
    });
  }
  console.log(`  ${deck}: ${last} slides${dropLast ? ' (next-session cover dropped)' : ''}`);
}
await ctx.close();

// ---------------------------------------------------------------- pages
const slideBlock = s => `<div class="blk">
  <div class="cap">Session ${s.sess} &middot; slide ${s.n}</div>
  <img src="${s.src}">
  <div class="lines"></div>
</div>`;

const dividerPage = d => `<div class="page div">
  <div class="dnum">${d.sess}</div>
  <h1>${esc(d.title)}</h1>
  <p class="dlede">${esc(ADDS[d.sess][0])}</p>
  <p class="drow"><span>On the appraisal checklist:</span> ${esc(ADDS[d.sess][1])}</p>
  <p class="dslides">${d.slides} slides follow. After this session, take your paper and the prompts on its sheet.</p>
</div>`;

const pages = [];
let i = 0;
while (i < blocks.length) {
  if (blocks[i].kind === 'divider') { pages.push(dividerPage(blocks[i])); i++; continue; }
  const a = blocks[i];
  const next = blocks[i + 1];
  const bb = next && next.kind === 'slide' ? next : null;
  pages.push(`<div class="page">${slideBlock(a)}${bb ? slideBlock(bb) : ''}
    <div class="run"><span>Economic Evaluation in Health &middot; AIIMS Bhopal &middot; 23 September 2026</span><span>Session ${a.sess}</span></div>
  </div>`);
  i += bb ? 2 : 1;
}

const doc = `<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Economic Evaluation in Health: slides</title>
<style>
  @page { size: A4 portrait; margin: 12mm 12mm 14mm; }
  * { box-sizing: border-box }
  body { margin:0; font: 10pt/1.4 Arial, Helvetica, sans-serif; color:#10141A;
         -webkit-print-color-adjust:exact; print-color-adjust:exact }
  .page { height: 271mm; display:flex; flex-direction:column; page-break-after:always; position:relative }
  .page:last-child { page-break-after:auto }
  .blk { flex:0 0 130mm; display:flex; flex-direction:column }
  .cap { font-size:7.5pt; letter-spacing:.08em; text-transform:uppercase; color:#7A8394;
         margin-bottom:1.2mm }
  .blk img { width:186mm; height:104.6mm; display:block; border:.4pt solid #C9CEDA }
  .lines { flex:1 1 auto; margin-top:2mm;
           background:repeating-linear-gradient(to bottom, transparent 0 5.6mm, #BFC6D4 5.6mm 5.75mm) }
  .run { flex:0 0 auto; margin-top:auto; font-size:7.5pt; color:#9AA1B0;
         display:flex; justify-content:space-between; padding-top:2mm }

  .div { justify-content:center; text-align:left }
  .div .dnum { font-size:64pt; font-weight:700; color:#162a6c; line-height:1 }
  .div h1 { font-size:26pt; line-height:1.15; margin:.15em 0 .5em; color:#162a6c; font-weight:700 }
  .div .dlede { font-size:13pt; line-height:1.45; max-width:150mm; margin:0 0 1.2em }
  .div .drow { font-size:10.5pt; color:#222833; border-left:3pt solid #162a6c; padding-left:5mm; margin:0 0 1.6em }
  .div .drow span { font-weight:700 }
  .div .dslides { font-size:9.5pt; color:#7A8394; margin:0 }
</style></head><body>
${pages.join('\n')}
</body></html>`;

const ctx2 = await b.newContext({ viewport: { width: 794, height: 1123 } });
const q = await ctx2.newPage();
await q.setContent(doc, { waitUntil: 'networkidle' });
await q.emulateMedia({ media: 'print' });
await q.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
await b.close();
rmSync(work, { recursive: true, force: true });
console.log(`kit slides: ${blocks.filter(x => x.kind === 'slide').length} slides, ${pages.length} pages -> ${out}`);
