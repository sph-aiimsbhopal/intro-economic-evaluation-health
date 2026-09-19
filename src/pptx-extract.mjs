// Walk a reveal.js deck and emit, per slide, a list of primitives with exact
// geometry: text boxes, background rectangles, tables, and images for the few
// things PowerPoint cannot hold as text (SVG diagrams, equations, widgets).
//
//   node extract.mjs <deck> <outdir>
//
// Writes <outdir>/<deck>.json and <outdir>/img/<deck>-<slide>-<i>.png
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'fs';

const deck = process.argv[2];
const out = process.argv[3] || '/home/claude/pptx';
mkdirSync(`${out}/img`, { recursive: true });

const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const p = await ctx.newPage();
await p.goto(`http://localhost:8766/slides/${deck}.html`);
await p.evaluate(() => Reveal.configure({ transition: 'none', backgroundTransition: 'none' }));
await p.waitForTimeout(1200);

const total = await p.evaluate(() => Reveal.getTotalSlides());
const slides = [];

for (let i = 0; i < total; i++) {
  await p.evaluate(n => Reveal.slide(n), i);
  await p.waitForTimeout(260);

  const data = await p.evaluate(() => {
    document.querySelectorAll('[data-shot]').forEach(e => e.removeAttribute('data-shot'));
    const S = document.querySelector('.slides > section.present');
    const sr = S.getBoundingClientRect();
    const scale = sr.width / 1280;            // reveal may scale the stage
    const R = el => {
      const r = el.getBoundingClientRect();
      return { x: (r.left - sr.left) / scale, y: (r.top - sr.top) / scale,
               w: r.width / scale, h: r.height / scale };
    };
    const px = v => parseFloat(v) / scale;
    const rgb = c => {
      const m = c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
      if (!m) return null;
      if (m[4] !== undefined && parseFloat(m[4]) < 0.05) return null;   // transparent
      return [1, 2, 3].map(k => (+m[k]).toString(16).padStart(2, '0')).join('').toUpperCase();
    };
    const INLINE = new Set(['STRONG', 'B', 'EM', 'I', 'SPAN', 'A', 'CODE', 'KBD', 'SUP', 'SUB', 'BR']);

    // --- collect the runs of one element, splitting on <br> ---
    const paraRuns = el => {
      const paras = [[]];
      const walk = (node, st) => {
        if (node.nodeType === 3) {
          let t = node.textContent.replace(/\s+/g, ' ');
          if (st.upper) t = t.toUpperCase();
          if (t.trim() || (paras.at(-1).length && t === ' ')) paras.at(-1).push({ t, ...st });
          return;
        }
        if (node.nodeType !== 1) return;
        if (node.tagName === 'BR') { paras.push([]); return; }
        const cs = getComputedStyle(node);
        const st2 = {
          upper: cs.textTransform === 'uppercase' || st.upper,
          spc: px(cs.letterSpacing) || st.spc || 0,
          b: +cs.fontWeight >= 600 || st.b,
          i: cs.fontStyle === 'italic' || st.i,
          color: rgb(cs.color) || st.color,
          sz: px(cs.fontSize) || st.sz,
        };
        node.childNodes.forEach(c => walk(c, st2));
      };
      const cs = getComputedStyle(el);
      walk(el, { b: +cs.fontWeight >= 600, i: cs.fontStyle === 'italic', color: rgb(cs.color),
                 sz: px(cs.fontSize), upper: cs.textTransform === 'uppercase',
                 spc: px(cs.letterSpacing) || 0 });
      return paras.filter(r => r.length).map(runs => ({ runs }));
    };

    const textItem = (el, opts = {}) => {
      const cs = getComputedStyle(el);
      const item = {
        kind: 'text', rect: R(el),
        align: cs.textAlign === 'start' ? 'left' : cs.textAlign,
        sz: px(cs.fontSize), color: rgb(cs.color) || '10141A',
        line: px(cs.lineHeight) / px(cs.fontSize) || 1.3,
        paras: [],
      };
      const tag = el.tagName;
      if (tag === 'UL' || tag === 'OL') {
        [...el.children].forEach((li, n) => {
          const ps = paraRuns(li);
          ps.forEach((pp, k) => { if (k === 0) pp.bullet = tag === 'UL' ? '•' : `${n + 1}.`; });
          item.paras.push(...ps);
        });
      } else {
        item.paras = paraRuns(el);
      }
      return Object.assign(item, opts);
    };

    const tableItem = el => {
      const cs = getComputedStyle(el);
      const rows = [...el.querySelectorAll('tr')].map(tr => [...tr.children].map(td => {
        const c = getComputedStyle(td);
        return {
          head: td.tagName === 'TH',
          align: c.textAlign === 'start' ? 'left' : c.textAlign,
          fill: rgb(c.backgroundColor),
          color: rgb(c.color),
          paras: paraRuns(td),
        };
      }));
      const widths = [...el.querySelectorAll('tr')][0] ?
        [...[...el.querySelectorAll('tr')][0].children].map(td => R(td).w) : [];
      return { kind: 'table', rect: R(el), sz: px(cs.fontSize), rows, widths };
    };

    const boxOf = el => {
      const cs = getComputedStyle(el);
      const fill = rgb(cs.backgroundColor);
      const t = px(cs.borderTopWidth), b = px(cs.borderBottomWidth),
            l = px(cs.borderLeftWidth), r = px(cs.borderRightWidth);
      const bl = l > 1.5 ? rgb(cs.borderLeftColor) : null;
      const boxed = t > 0 && b > 0 && r > 0;                 // a real border on all sides
      const ruleTop = t > 0 && b === 0 && r === 0;           // just a rule above (e.g. .cite)
      if (!fill && !bl && !boxed && !ruleTop) return null;
      const rect = R(el);
      if (ruleTop && !fill && !bl) {
        return { kind: 'rect', rect: { x: rect.x, y: rect.y, w: rect.w, h: Math.max(t, 1) },
                 fill: rgb(cs.borderTopColor), line: null, rule: true };
      }
      return { kind: 'rect', rect, fill, line: boxed ? rgb(cs.borderTopColor) : null,
               leftBar: bl ? { color: bl, w: l } : null,
               radius: px(cs.borderTopLeftRadius) };
    };

    const items = [];
    const IMG = [];   // selectors to screenshot, filled with a marker index

    const emit = el => {
      const tag = el.tagName;
      const cls = el.className && el.className.baseVal !== undefined ? el.className.baseVal : (el.className || '');
      if (tag === 'ASIDE') return;

      if (tag === 'H2') {                                   // the navy band
        const cs = getComputedStyle(el);
        items.push({ kind: 'rect', rect: R(el), fill: rgb(cs.backgroundColor), full: true });
        const t = textItem(el);
        t.pad = px(cs.paddingLeft);
        t.rect = { x: t.rect.x + t.pad, y: t.rect.y, w: t.rect.w - 2 * t.pad, h: t.rect.h };
        t.vcenter = true;
        items.push(t);
        return;
      }
      if (tag === 'TABLE') { items.push(tableItem(el)); return; }
      if (tag === 'SVG' || tag === 'svg' || tag === 'IFRAME' || tag === 'IMG' ||
          /(^|\s)eq(\s|$)/.test(cls) || /grid6/.test(cls)) {
        el.dataset.shot = IMG.length; IMG.push(R(el)); items.push({ kind: 'image', rect: R(el), idx: IMG.length - 1 });
        return;
      }
      if ((tag === 'UL' || tag === 'OL') && +getComputedStyle(el).columnCount > 1) {
        // CSS columns: split the items into one text box per column
        const lis = [...el.children];
        const mid = R(el).x + R(el).w / 2;
        const cols = [lis.filter(li => R(li).x < mid), lis.filter(li => R(li).x >= mid)];
        cols.forEach(group => {
          if (!group.length) return;
          const rs = group.map(R);
          const rect = { x: Math.min(...rs.map(r => r.x)), y: Math.min(...rs.map(r => r.y)),
                         w: Math.max(...rs.map(r => r.x + r.w)) - Math.min(...rs.map(r => r.x)),
                         h: Math.max(...rs.map(r => r.y + r.h)) - Math.min(...rs.map(r => r.y)) };
          const cs = getComputedStyle(el);
          const item = { kind: 'text', rect, align: 'left', sz: px(cs.fontSize),
                         color: rgb(cs.color) || '10141A',
                         line: px(cs.lineHeight) / px(cs.fontSize) || 1.4, paras: [] };
          group.forEach((li, n) => {
            const ps = paraRuns(li);
            ps.forEach((pp, k) => { if (k === 0) pp.bullet = tag === 'UL' ? '\u2022' : `${lis.indexOf(li) + 1}.`; });
            item.paras.push(...ps);
          });
          items.push(item);
        });
        return;
      }
      const kids = [...el.children].filter(c => c.tagName !== 'ASIDE');
      const blockKids = kids.filter(c => !INLINE.has(c.tagName));
      if (blockKids.length) {                                // a container: box, then recurse
        const box = boxOf(el);
        if (box) items.push(box);
        blockKids.forEach(emit);
        return;
      }
      const box = boxOf(el);
      if (box) items.push(box);
      if (el.textContent.trim()) {
        const cs = getComputedStyle(el);
        const t = textItem(el);
        const padL = px(cs.paddingLeft), padR = px(cs.paddingRight), padT = px(cs.paddingTop);
        t.rect = { x: t.rect.x + padL, y: t.rect.y + padT, w: t.rect.w - padL - padR, h: t.rect.h - padT };
        items.push(t);
      }
    };

    [...S.children].forEach(emit);

    const notes = (S.querySelector('aside.notes')?.textContent || '').replace(/\s+/g, ' ').trim();
    const title = (S.querySelector('h1,h2')?.textContent || '').trim();
    const cover = S.classList.contains('cover');
    return { items, notes, title, cover, shots: IMG.length };
  });

  // screenshot the elements that stay pictures
  for (let k = 0; k < data.shots; k++) {
    const el = await p.$(`[data-shot="${k}"]`);
    const file = `${out}/img/${deck}-${i + 1}-${k}.png`;
    if (el) { await el.screenshot({ path: file, timeout: 8000 }); }
    const it = data.items.find(x => x.kind === 'image' && x.idx === k);
    if (it) it.file = file;
  }
  slides.push(data);
}

writeFileSync(`${out}/${deck}.json`, JSON.stringify({ deck, slides }, null, 1));
console.log(`${deck}: ${slides.length} slides, ${slides.reduce((n, s) => n + s.shots, 0)} images`);
await b.close();
