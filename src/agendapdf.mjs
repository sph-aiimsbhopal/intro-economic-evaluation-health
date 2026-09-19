import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p = await (await b.newContext({viewport:{width:794,height:1123}})).newPage();
await p.goto('file:///home/claude/brochure/agenda.html', {waitUntil:'networkidle'});
console.log(await p.evaluate(()=>{
  const pg=document.querySelector('.page'); const r=pg.getBoundingClientRect(); let bot=0;
  pg.querySelectorAll(':scope > *').forEach(c=>bot=Math.max(bot,c.getBoundingClientRect().bottom-r.top));
  return `contentBottom=${Math.round(bot)} limit=${Math.round(r.height)} scrollH=${pg.scrollHeight}`;
}));
await p.emulateMedia({media:'print'});
await p.pdf({path:'/home/claude/brochure/EE-Health-Workshop-Agenda.pdf', format:'A4', printBackground:true, margin:{top:0,bottom:0,left:0,right:0}});
await p.emulateMedia({media:'screen'});
await (await p.$('.page')).screenshot({path:'/home/claude/brochure/agenda.png'});
await b.close();
