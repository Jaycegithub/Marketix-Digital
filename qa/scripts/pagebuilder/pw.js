// shared: open a password-protected preview page
module.exports.open=async(b,slug,w,q='pv')=>{const c=await b.newContext({viewport:{width:w,height:900}});const p=await c.newPage();
 await p.goto(`https://marketixdigital.com.au/${slug}/?${q}=${Date.now()}`,{waitUntil:'load',timeout:90000});
 if(await p.$('input[name="post_password"]')){await p.fill('input[name="post_password"]','mxprev');await Promise.all([p.waitForNavigation({timeout:90000}),p.click('form.post-password-form input[type="submit"]')]);}
 await p.mouse.move(0,0);return {c,p}};
