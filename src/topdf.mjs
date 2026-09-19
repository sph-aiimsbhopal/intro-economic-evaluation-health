import { chromium } from 'playwright';
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p = await (await b.newContext()).newPage();
await p.goto('file:///home/claude/brochure/brochure.html', {waitUntil:'networkidle'});
await p.emulateMedia({media:'print'});
await p.pdf({path:'/home/claude/brochure/EE-Health-Workshop-Brochure.pdf', format:'A4', printBackground:true, margin:{top:0,bottom:0,left:0,right:0}});
// screenshots for review
await p.setViewportSize({width:794, height:1123});
await p.emulateMedia({media:'screen'});
const pages = await p.$$('.page');
for(let i=0;i<pages.length;i++) await pages[i].screenshot({path:`/home/claude/brochure/p${i+1}.png`});
await b.close();
