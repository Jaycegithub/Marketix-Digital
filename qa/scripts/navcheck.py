import json, re, html, urllib.parse, collections, concurrent.futures
import crawl_both as cb
D='https://dev.marketixdigital.com.au'
st,_,home,_=cb.fetch(D+'/?nav='+str(id(cb)))
def links(fragment):
    out=[]
    for a,t in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',fragment,re.S):
        t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',t))).strip()
        out.append((html.unescape(a),t))
    return out
hdr=home[home.find('<header'):home.find('</header>')] if '<header' in home else ''
ftr=home[home.rfind('<footer'):home.rfind('</footer>')] if '<footer' in home else ''
# Elementor theme-builder header/footer
m=re.search(r'data-elementor-type="header".*?(?=<div[^>]+data-elementor-type="wp-page")',home,re.S)
if m: hdr=m.group(0)
m=re.search(r'data-elementor-type="footer".*',home,re.S)
if m: ftr=m.group(0)
res={}
def chk(u):
    full=urllib.parse.urljoin(D+'/',u)
    if not full.startswith(D) : 
        if full.startswith('http'):
            s,l,_,_=cb.fetch(full); return u,s,l
        return u,'n/a',''
    s,l,_,_=cb.fetch(full); return u,s,l
for name,frag in (('header',hdr),('footer',ftr)):
    ls=list(dict.fromkeys(links(frag)))
    with concurrent.futures.ThreadPoolExecutor(8) as ex: r={u:(s,l) for u,s,l in ex.map(chk,[a for a,_ in ls])}
    print('==',name,len(ls),'links')
    for a,t in ls:
        s,l=r[a]
        flag='' if s in (200,'n/a') else '  <-- '+str(s)+' '+(l or '')
        print('  %-40s %s %s%s'%(t[:40],a.replace(D,''),s,flag))
# CTA check across all pages
dev=json.load(open('dev_inventory_plus.json'))
cta=collections.Counter(); bad=[]
pages=json.load(open('qa_pages.json'))
def page(p):
    s,_,b,_=cb.fetch(D+p); return p,b
with concurrent.futures.ThreadPoolExecutor(8) as ex: bodies=dict(ex.map(page,pages))
alllinks=collections.defaultdict(set)
for p,b in bodies.items():
    for a,t in links(b):
        if re.search(r'strategy call|investment briefing|get a proposal',t,re.I):
            ok='/request-an-investment-briefing/' in a
            cta['strategy/briefing ok' if ok else 'strategy/briefing OTHER']+=1
            if not ok: bad.append((p,t,a))
        if re.search(r'search intelligence',t,re.I):
            ok='/search-intelligence-and-advisory/' in a
            cta['search-intel ok' if ok else 'search-intel OTHER']+=1
            if not ok: bad.append((p,t,a))
        u=urllib.parse.urljoin(D+p,a)
        if u.startswith(D): alllinks[urllib.parse.urlparse(u).path].add(p)
    if 'rank-math-breadcrumb' in b or 'breadcrumb' in b.lower(): cta['pages with breadcrumbs']+=1
print('CTA:',dict(cta)); [print('  ',x) for x in bad[:20]]
targets=[t for t in alllinks if not cb.SKIP.search(t)]
with concurrent.futures.ThreadPoolExecutor(8) as ex: st=dict(zip(targets,ex.map(lambda t:cb.fetch(D+urllib.parse.quote(t,safe='/%'))[:2],targets)))
print('unique internal link targets',len(targets))
for t,(s,l) in sorted(st.items()):
    if s!=200: print('  ',s,t,'->',l,'| on',sorted(alllinks[t])[:3])
