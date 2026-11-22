// node textcheck.js n1 n2 ... : every doc text block (<n>.json) must appear on zz-preview-<n>
const {chromium}=require('playwright');const fs=require('fs');const {open}=require('./pw.js');
const norm=s=>s.replace(/[–—]/g,'-').replace(/^Step \d+:\s*/i,'').replace(/…/g,'...').replace(/[×]/g,'x').replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/ /g,' ').replace(/\s+/g,' ').trim().toLowerCase();
(async()=>{const b=await chromium.launch();
for(const n of process.argv.slice(2)){const rows=JSON.parse(fs.readFileSync(__dirname+`/${n}.json`));const {c,p}=await open(b,`zz-preview-${n}`,1440,'tc');
 const txt=norm(await p.evaluate(()=>document.body.textContent));const miss=[];let total=0;
 for(const r of [1,7,8,10,11,12,13,14,17]) for(const cell of rows[r]||[]) for(const bl of cell){const t=norm(bl.text||'');if(!t||t==='[image]'||t.includes('iconify.design'))continue;total++;if(!txt.includes(t))miss.push(r+': '+bl.text.slice(0,90))}
 console.log(`== ${n}: ${total-miss.length}/${total} blocks found`);miss.forEach(m=>console.log('   MISSING',m));await c.close()}
await b.close()})()
