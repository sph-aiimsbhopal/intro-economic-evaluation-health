import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p = await (await b.newContext({viewport:{width:794,height:1123}})).newPage();
await p.goto('file:///home/claude/brochure/brochure.html', {waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{
  const mm = 96/25.4; const H = 297*mm;
  const out=[];
  document.querySelectorAll('.page').forEach((pg,i)=>{
    const r=pg.getBoundingClientRect();
    let bottom=0;
    pg.querySelectorAll(':scope > *').forEach(c=>{ bottom=Math.max(bottom, c.getBoundingClientRect().bottom - r.top); });
    out.push(`page${i+1}: box=${Math.round(r.height)}px limit=${Math.round(H)}px contentBottom=${Math.round(bottom)}px scrollH=${pg.scrollHeight}`);
    pg.querySelectorAll(':scope > *').forEach(c=>{
      const q=c.getBoundingClientRect();
      out.push(`   ${c.className||c.tagName} h=${Math.round(q.height)} top=${Math.round(q.top-r.top)} bot=${Math.round(q.bottom-r.top)}`);
    });
  });
  return out.join('\n');
}));
await b.close();
