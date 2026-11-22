// node measure.js n1 n2 ... -> heights_<n>.json {sectionIndex: mobile height px}
const {chromium}=require('playwright');const fs=require('fs');const {open}=require('./pw.js');
(async()=>{const b=await chromium.launch();
for(const n of process.argv.slice(2)){const {c,p}=await open(b,`zz-preview-${n}`,390,'ms');
 await p.addStyleTag({content:'*{content-visibility:visible!important}'});
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<H;y+=700){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(60)}
 await p.waitForTimeout(800);
 const h=await p.evaluate(()=>{const o={};[...document.querySelectorAll('[data-elementor-type="wp-page"] > .e-con')].forEach((s,i)=>o[i]=Math.round(s.getBoundingClientRect().height));return o});
 fs.writeFileSync(__dirname+`/heights_${n}.json`,JSON.stringify(h));console.log(n,JSON.stringify(h));await c.close()}
await b.close()})()
