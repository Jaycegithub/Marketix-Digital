// node axe.js n1 n2 ... : axe-core (wcag2a/aa) at 390 and 1350 on zz-preview-<n>
const {chromium}=require('playwright');const {open}=require('./pw.js');
(async()=>{const b=await chromium.launch();
for(const n of process.argv.slice(2)) for(const w of [390,1350]){const {c,p}=await open(b,`zz-preview-${n}`,w,'ax');
 await p.addStyleTag({content:'*{content-visibility:visible!important}'});
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<H;y+=700){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(50)}
 await p.evaluate(()=>scrollTo(0,0));await p.mouse.move(0,0);await p.waitForTimeout(600);
 await p.addScriptTag({url:'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js'});
 const v=await p.evaluate(async()=>(await axe.run(document,{runOnly:['wcag2a','wcag2aa']})).violations.map(x=>({id:x.id,n:x.nodes.length,t:x.nodes.slice(0,3).map(d=>d.target.join(' ').slice(-70))})));
 console.log(n,w,v.length?JSON.stringify(v):'0 violations');await c.close()}
await b.close()})()
