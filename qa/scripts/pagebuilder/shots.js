const {chromium}=require('playwright');const {open}=require('./pw.js');
(async()=>{const [slug,out]=process.argv.slice(2);const b=await chromium.launch();
for(const w of [1440,390]){const {c,p}=await open(b,slug,w,'s1');
 await p.addStyleTag({content:'*{content-visibility:visible!important}'});
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<H;y+=700){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(90)}
 await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(1500);
 console.log(slug,w,'height',H,'scrollWidth',await p.evaluate(()=>document.documentElement.scrollWidth));
 await p.screenshot({path:`${out}_${w}.png`,fullPage:true});await c.close()}
await b.close()})()
