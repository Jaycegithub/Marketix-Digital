const {chromium}=require('playwright');const fs=require('fs');
const pages=JSON.parse(fs.readFileSync(process.argv[3]||"qa_pages.json"));const NW=+(process.argv[4]||3);const W=+process.argv[2];
const PH=/lorem ipsum|add your heading text here|click edit button|this is the heading|\bTODO\b|placeholder text|\bTEST\b - |Warning: |Notice: |Fatal error|Deprecated: |undefined\b|\[object Object\]|NaN\b|dev\.marketixdigital/i;
(async()=>{const b=await chromium.launch();const res=[];let idx=0;
async function worker(){while(idx<pages.length){const path=pages[idx++];
 const p=await b.newPage({viewport:{width:W,height:900}});const errs=[];
 p.on('pageerror',e=>errs.push('JS: '+e.message.slice(0,120)));
 p.on('console',m=>{if(m.type()==='error'&&!/Failed to load resource|net::ERR|youtube|google|facebook|bing|hs-|clickcease|goodreviews|ERR_BLOCKED|Content Security/i.test(m.text()))errs.push('console: '+m.text().slice(0,120))});
 await p.route(/youtube|ytimg|googletagmanager|google-analytics|bing\.com|facebook|js\.hs-scripts|js\.hubspot|clickcease|goodreviews|doubleclick/,r=>r.abort());
 let r=null;
 for(let a=0;a<3&&!r;a++){try{await p.goto('https://dev.marketixdigital.com.au'+path,{waitUntil:'load',timeout:90000});
  if(await p.title()==='One moment, please...'){await p.waitForTimeout(6000);continue}
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}window.scrollTo(0,0)});
  await p.waitForTimeout(1200);
  r=await p.evaluate(([W,PHs])=>{const PH=new RegExp(PHs,'i');
   const imgs=[...document.images].filter(i=>i.offsetParent&&i.complete&&i.naturalWidth===0&&!/youtube|ytimg|facebook|bing/.test(i.src)).map(i=>i.src.split('/').pop()).slice(0,5);
   const txt=document.body.innerText;const m=txt.match(PH);
   const over=[];document.querySelectorAll('.elementor-widget,img,h1,h2,h3,p,a.elementor-button').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&(r.right>W+2)&&getComputedStyle(e).position!=='fixed'&&!e.closest('.elementor-location-popup,.swiper,[aria-hidden=true],.elementor-nav-menu--dropdown'))over.push((e.className.baseVal||e.className||e.tagName).toString().split(' ').slice(0,2).join('.')+':'+Math.round(r.right))});
   const big=[];document.querySelectorAll('h1,h2,p,a,span').forEach(e=>{const f=parseFloat(getComputedStyle(e).fontSize);if(f>(W<500?56:96)&&e.offsetHeight)big.push(Math.round(f))});
   const font=getComputedStyle(document.querySelector('h1,h2')||document.body).fontFamily;
   const h1=document.querySelectorAll('h1').length;
   return {hscroll:document.documentElement.scrollWidth>W+2,over:over.slice(0,3),imgs,ph:m?txt.substr(Math.max(0,m.index-40),100).replace(/\s+/g,' '):'',big:big.slice(0,2),font:font.split(',')[0],h1,title:document.title};},[W,PH.source]);
 }catch(e){await p.waitForTimeout(4000);}}
 res.push({path,W,...(r||{fail:true}),errs:[...new Set(errs)].slice(0,4)});await p.close();}}
await Promise.all(Array.from({length:NW},worker));
fs.writeFileSync('qa_audit_'+W+(process.argv[3]?"_re":"")+'.json',JSON.stringify(res,null,1));
const bad=res.filter(x=>x.fail||x.hscroll||x.over?.length||x.imgs?.length||x.ph||x.big?.length||x.errs.length||!/Poppins/i.test(x.font||''));
console.log('W',W,'pages',res.length,'flagged',bad.length);bad.forEach(x=>console.log(JSON.stringify(x)));
await b.close();})();
