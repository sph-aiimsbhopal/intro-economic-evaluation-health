import { chromium } from 'playwright';
const decks = process.argv.slice(2);
const LIMIT = 700;                     // of a 720 px slide
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
let bad = 0;
for(const d of decks){
  const ctx = await b.newContext({viewport:{width:1280,height:720}, deviceScaleFactor:1});
  const p = await ctx.newPage();
  const errs=[];
  p.on('pageerror',e=>errs.push(e.message));
  p.on('response',r=>{ if(r.status()>=400 && !r.url().includes('favicon')) errs.push('HTTP'+r.status()+' '+r.url()); });
  await p.goto(`http://localhost:8765/slides/${d}.html`);
  await p.waitForTimeout(900);
  const total = await p.evaluate(()=>Reveal.getTotalSlides());
  const over = [];
  // measure each slide WHILE it is the present one; hidden sections report zero rects
  for(let i=0;i<total;i++){
    await p.evaluate(n=>Reveal.slide(n), i);
    await p.waitForTimeout(140);
    const r = await p.evaluate(()=>{
      const s = document.querySelector('.slides > section.present');
      if(!s) return null;
      const sr = s.getBoundingClientRect();
      let bottom = 0;
      s.querySelectorAll(':scope > *').forEach(c=>{
        if(c.tagName === 'ASIDE') return;
        bottom = Math.max(bottom, c.getBoundingClientRect().bottom - sr.top);
      });
      return { bottom: Math.round(bottom), scrollH: s.scrollHeight,
               title: ((s.querySelector('h1,h2')||{}).textContent||'').slice(0,38) };
    });
    if(r && r.bottom > LIMIT) over.push({slide:i+1, bottom:r.bottom, title:r.title});
  }
  const dash = await p.evaluate(()=>{
    let n=0; document.querySelectorAll('.slides > section').forEach(s=>{
      const c=s.cloneNode(true); c.querySelectorAll('aside').forEach(a=>a.remove());
      n += (c.textContent.match(/—/g)||[]).length; });
    return n;
  });
  console.log(`${d}: ${total} slides | overflow: ${over.length ? JSON.stringify(over) : 'none'} | em-dashes: ${dash} | errors: ${errs.length?errs:'none'}`);
  if(over.length || errs.length) bad++;
  await ctx.close();
}
console.log(bad ? `\n${bad} deck(s) need attention` : '\nall clean');
await b.close();
