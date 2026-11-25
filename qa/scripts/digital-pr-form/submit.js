// node submit.js <path> <formIndex> <mode: noobjective|full> [width]
// Fills a Digital PR form and submits it. Tracking hosts (GTM/GA/Meta/Bing/Clarity) are blocked so no conversion is recorded.
const {chromium}=require('playwright');
const BLOCK=/googletagmanager|google-analytics|analytics\.google|doubleclick|facebook\.(net|com)|connect\.facebook|bat\.bing|clarity\.ms|googleadservices/;
(async()=>{const [path,idx,mode,w]=process.argv.slice(2);const b=await chromium.launch();
 const c=await b.newContext({viewport:{width:+(w||1440),height:900}});
 await c.route(u=>BLOCK.test(u.toString()),r=>r.abort());
 const p=await c.newPage(); const blocked=[];p.on('requestfailed',r=>{if(BLOCK.test(r.url()))blocked.push(new URL(r.url()).host)});
 let ajax=null;p.on('response',async r=>{if(r.url().includes('admin-ajax.php')&&r.request().method()==='POST'){try{ajax=await r.text()}catch(e){}}});
 await p.goto('https://marketixdigital.com.au'+path+'?st='+Date.now(),{waitUntil:'load',timeout:90000});
 if(await p.$('input[name="post_password"]')){await p.fill('input[name="post_password"]','mxprev');await Promise.all([p.waitForNavigation(),p.click('form.post-password-form input[type="submit"]')]);}
 const f=(await p.$$('form.elementor-form'))[+idx]; await f.scrollIntoViewIfNeeded(); await p.mouse.wheel(0,200); await p.waitForTimeout(500);
 const v={name:'TEST – Claude (please ignore)',job_title:'QA test',email:'test@marketixdigital.com.au',phone:'0400 000 000',company:'Marketix QA test',website:'marketixdigital.com.au',
  message:'Test submission to check the new Digital PR enquiry form. Please ignore.'};
 for(const [k,val] of Object.entries(v)) await (await f.$('[name="form_fields['+k+']"]')).fill(val);
 if(mode==='full'){const ob=await f.$$('input[name="form_fields[objectives][]"]');await ob[0].check();await ob[2].check();}
 await (await f.$$('input[name="form_fields[investment]"]'))[5].check();
 // wait for Turnstile (up to 25s)
 let tok=0;for(let i=0;i<25;i++){tok=await f.evaluate(f=>{const t=f.querySelector('[name="cf-turnstile-response"]');return t?t.value.length:-1});if(tok>0)break;await p.waitForTimeout(1000)}
 console.log('turnstile token length:',tok);
 await Promise.all([p.waitForResponse(r=>r.url().includes('admin-ajax.php')&&r.request().method()==='POST',{timeout:60000}).catch(()=>null),f.$eval('button[type=submit]',x=>x.click())]);
 await p.waitForTimeout(6000);
 console.log('ajax response:',(ajax||'none').slice(0,400));
 console.log('final URL:',p.url());
 console.log('messages:',await p.evaluate(()=>[...document.querySelectorAll('.elementor-message,.elementor-field-group .elementor-error, .elementor-message-danger')].map(e=>e.textContent.trim()).join(' | ')).catch(()=>'(navigated)'));
 console.log('blocked tracking hosts:',[...new Set(blocked)].join(', ')||'none');
 await b.close()})()
