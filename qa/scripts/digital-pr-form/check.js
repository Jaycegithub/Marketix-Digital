// node check.js <path> : inspect both forms, links and validation on the (password) preview, screenshots at 1440 + 390
const {chromium}=require('playwright');
(async()=>{const path=process.argv[2];const b=await chromium.launch();
for(const w of [1440,390]){const c=await b.newContext({viewport:{width:w,height:900}});const p=await c.newPage();
 await p.goto('https://marketixdigital.com.au'+path+'?ck='+Date.now(),{waitUntil:'load',timeout:90000});
 if(await p.$('input[name="post_password"]')){await p.fill('input[name="post_password"]','mxprev');await Promise.all([p.waitForNavigation(),p.click('form.post-password-form input[type="submit"]')]);}
 await p.addStyleTag({content:'*{content-visibility:visible!important}'});
 const info=await p.evaluate(()=>{
  const forms=[...document.querySelectorAll('form.elementor-form')].map(f=>({name:f.getAttribute('name'),
   fields:[...f.querySelectorAll('.elementor-field-group')].filter(g=>getComputedStyle(g).display!=='none').map(g=>{const l=g.querySelector('label.elementor-field-label');const i=g.querySelector('input:not([type=checkbox]):not([type=radio]),textarea,select');
     const opts=[...g.querySelectorAll('input[type=checkbox],input[type=radio]')];
     return [(l&&l.textContent.trim())||g.textContent.trim().slice(0,40), i?(i.getAttribute('placeholder')||''):'', i?i.required:null, opts.length?opts.length+' '+opts[0].type+(opts[0].required?' req':''):''].join(' | ')}),
   button:(f.querySelector('button[type=submit]')||{}).textContent.trim()}));
  const links=[...document.querySelectorAll('.elementor-location-header ~ * a, main a, [data-elementor-type="wp-page"] a')].filter(a=>/request-an-investment-briefing|#digital-pr-strategy|#contact/.test(a.getAttribute('href')||'')).map(a=>a.textContent.trim().slice(0,30)+' -> '+a.getAttribute('href'));
  const anchor=document.getElementById('digital-pr-strategy');
  return {forms,links,anchor:!!anchor,sw:document.documentElement.scrollWidth}});
 if(w===1440) console.log(JSON.stringify(info,null,1)); else console.log('390 scrollWidth',info.sw);
 // screenshot the two forms
 const fs=await p.$$('form.elementor-form');
 for(let i=0;i<fs.length;i++){const panel=await fs[i].evaluateHandle(f=>f.closest('.e-con.e-child')?.parentElement?.closest('.e-con')||f);await panel.scrollIntoViewIfNeeded();await p.waitForTimeout(800);await panel.screenshot({path:__dirname+`/shot_form${i}_${w}.png`})}
 if(w===1440){ // validation: submit empty bottom form
  const f=fs[fs.length-1];await f.scrollIntoViewIfNeeded();
  await f.$eval('button[type=submit]',x=>x.click());await p.waitForTimeout(800);
  console.log('empty submit: invalid fields =',await f.evaluate(f=>[...f.querySelectorAll('input,textarea')].filter(i=>!i.checkValidity()).map(i=>i.name+':'+i.type).join(', ')));
  await f.$eval('input[type=checkbox]',x=>x.click());
  console.log('after 1 objective ticked: invalid checkboxes =',await f.evaluate(f=>[...f.querySelectorAll('input[type=checkbox]')].filter(i=>!i.checkValidity()).length));
 }
 // anchor click from hero CTA scrolls to form
 if(w===390){await p.evaluate(()=>scrollTo(0,0));await p.click('a[href="#digital-pr-strategy"] >> nth=0');await p.waitForTimeout(1500);
  console.log('390 after CTA click, form panel top =',await p.evaluate(()=>Math.round(document.getElementById('digital-pr-strategy').getBoundingClientRect().top)));}
 await c.close()}
await b.close()})()
