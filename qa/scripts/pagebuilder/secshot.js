// node secshot.js <slug> <sectionIndex> <out.png> : screenshot one top-level section of a preview at 1440px
const {chromium}=require('playwright');const {open}=require('./pw.js');
(async()=>{const [slug,idx,out]=process.argv.slice(2);const b=await chromium.launch();const {c,p}=await open(b,slug,1440,'ss');
 await p.addStyleTag({content:'*{content-visibility:visible!important}'});
 const s=(await p.$$('[data-elementor-type="wp-page"] > .e-con'))[+idx];await s.scrollIntoViewIfNeeded();await p.waitForTimeout(1500);
 await s.screenshot({path:out});await b.close()})()
