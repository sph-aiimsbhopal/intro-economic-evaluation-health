// Facilitator notes handout: two slides per A4 landscape page, each slide on the
// left with its speaker notes in a column beside it.
//
//   node notes-pdf.mjs <deck> [outfile]
//
// Needs a static server on the repo root at :8766. Screenshots every slide,
// lays the pages out in HTML, prints to PDF, and reports any note that did not fit.
import { chromium } from 'playwright';
import { mkdtempSync, rmSync, readFileSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const deck = process.argv[2];
const out = process.argv[3] || `/home/claude/ws/handouts/notes-${deck}.pdf`;
if (!deck) { console.error('usage: node notes-pdf.mjs <deck> [outfile]'); process.exit(1); }

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const work = mkdtempSync(join(tmpdir(), 'notes-'));
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

// ---------------------------------------------------------------- capture
// 1.5x gives about 300 dpi at the 132 mm printed width without bloating the PDF.
const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
const p = await ctx.newPage();
await p.goto(`http://localhost:8766/slides/${deck}.html`);
await p.evaluate(() => Reveal.configure({ transition: 'none', backgroundTransition: 'none' }));
// reveal's own chrome would be printed onto every thumbnail
await p.addStyleTag({ content: '.reveal .controls, .reveal .progress, .reveal .slide-number { display:none !important }' });
await p.waitForTimeout(1200);

const total = await p.evaluate(() => Reveal.getTotalSlides());
const deckTitle = (await p.title()).trim();
const slides = [];

for (let i = 0; i < total; i++) {
  await p.evaluate(n => Reveal.slide(n), i);
  await p.waitForTimeout(280);
  const meta = await p.evaluate(() => {
    const S = document.querySelector('.slides > section.present');
    let title = '';
    const h = S.querySelector('h1, h2');
    if (h) {                                     // <br> in a title must not glue two words together
      const c = h.cloneNode(true);
      c.querySelectorAll('br').forEach(br => br.replaceWith(' '));
      title = c.textContent.replace(/\s+/g, ' ').trim();
    }
    return {
      title,
      notes: (S.querySelector('aside.notes')?.textContent || '').replace(/\s+/g, ' ').trim(),
    };
  });
  const file = join(work, `${i}.png`);
  await p.screenshot({ path: file });
  // the layout page is built with setContent, which cannot load file:// images
  meta.src = 'data:image/png;base64,' + readFileSync(file).toString('base64');
  slides.push({ n: i + 1, ...meta });
}
await ctx.close();

// ---------------------------------------------------------------- lay out
const row = s => `<div class="row">
  <div class="shot"><img src="${s.src}"></div>
  <div class="side">
    <div class="hd"><span class="num">${s.n}</span><span class="ttl">${esc(s.title) || '&nbsp;'}</span></div>
    <div class="notes">${s.notes ? esc(s.notes) : '<span class="none">No speaker note on this slide.</span>'}</div>
  </div>
</div>`;

const pages = Math.ceil(slides.length / 2);
const sheets = [];
for (let i = 0; i < slides.length; i += 2) {
  const second = slides[i + 1] ? row(slides[i + 1]) : '<div class="row blank"></div>';
  sheets.push(`<div class="sheet">
  <div class="rows">
${row(slides[i])}
${second}
  </div>
  <div class="run"><span>${esc(deckTitle)}</span><span>Economic Evaluation in Health &middot; AIIMS Bhopal &middot; 23 September 2026</span><span>page ${sheets.length + 1} of ${pages}</span></div>
</div>`);
}

const doc = `<!DOCTYPE html><html><head><meta charset="utf-8">
<title>${esc(deckTitle)}: speaker notes</title>
<style>
  @page { size: A4 landscape; margin: 11mm 12mm 11mm; }
  * { box-sizing: border-box }
  body { margin:0; font: 10.5pt/1.42 Arial, Helvetica, sans-serif; color:#10141A;
         -webkit-print-color-adjust:exact; print-color-adjust:exact }
  .sheet { height: 188mm; display:flex; flex-direction:column; page-break-after:always }
  .sheet:last-child { page-break-after:auto }
  .rows { flex:1 1 auto; min-height:0; display:flex; flex-direction:column }
  .row { flex:0 0 50%; display:flex; gap:7mm; min-height:0; overflow:hidden }
  .row:first-child { border-bottom:.3pt solid #C9CEDA }
  .row:first-child .side, .row:first-child .shot { padding-bottom:5mm }
  .row:last-child .side, .row:last-child .shot { padding-top:5mm }
  .row.blank { border:0 }
  .shot { flex:0 0 132mm }
  .shot img { width:132mm; height:74.25mm; display:block; border:.4pt solid #C9CEDA }
  .side { flex:1 1 auto; min-width:0 }
  .hd { display:flex; gap:3mm; align-items:baseline; border-bottom:1.6pt solid #162a6c;
        padding-bottom:1.2mm; margin-bottom:2.2mm }
  .num { font-weight:700; color:#fff; background:#162a6c; padding:.4mm 2mm; font-size:9pt; flex:0 0 auto }
  .ttl { font-weight:700; font-size:10.5pt; line-height:1.25 }
  .notes { font-size:10pt; line-height:1.45; color:#222833 }
  .none { color:#9AA1B0; font-style:italic }
  .run { flex:0 0 5mm; font-size:7.5pt; color:#7A8394; display:flex; justify-content:space-between;
         align-items:flex-end; border-top:.3pt solid #E3E6EE; padding-top:1.5mm }
</style></head><body>
${sheets.join('\n')}
</body></html>`;

// ---------------------------------------------------------------- print and check
const ctx2 = await b.newContext({ viewport: { width: 1123, height: 794 } });
const q = await ctx2.newPage();
await q.setContent(doc, { waitUntil: 'networkidle' });
await q.emulateMedia({ media: 'print' });

// the row clips with overflow:hidden, so measure the note against the row's floor,
// not the side column's own scroll height, which grows to fit its content
const clipped = await q.evaluate(() => [...document.querySelectorAll('.row')]
  .map((r, i) => {
    const notes = r.querySelector('.notes');
    if (!notes) return null;
    const over = notes.getBoundingClientRect().bottom - r.getBoundingClientRect().bottom;
    return over > 2 ? { slide: i + 1, over: Math.round(over) } : null;
  }).filter(Boolean));

await q.pdf({ path: out, format: 'A4', landscape: true, printBackground: true, preferCSSPageSize: true });
await b.close();
rmSync(work, { recursive: true, force: true });

if (clipped.length) console.log(`  notes clipped on slide(s): ${clipped.map(c => `${c.slide} (+${c.over}px)`).join(', ')}`);
console.log(`${deck}: ${slides.length} slides -> ${pages} pages -> ${out}`);
