"""After an Elementor CSS cache clear: render every published page/post/category once with a cache-busting query
(Elementor rebuilds each post-<id>.css under the same name), then check that every Elementor stylesheet the
(cached) pages reference returns 200.   usage: python3 regen.py"""
import re, time, urllib.request, urllib.error, concurrent.futures as cf
from lv import req, UA
def get(u, t=90):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=t)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e: return e.code, ''
    except Exception as e: return 0, str(e)
links = []
for typ in ('pages', 'posts', 'categories'):
    pg = 1
    while True:
        q = f'wp/v2/{typ}?per_page=100&page={pg}&_fields=link' + ('&status=publish' if typ != 'categories' else '&hide_empty=true')
        try: r = req('GET', q)
        except RuntimeError: break
        links += [x['link'] for x in r if 'zz-preview' not in x['link']]
        if len(r) < 100: break
        pg += 1
links = sorted(set(links)); ns = int(time.time())
print('urls:', len(links))
def render(u): return get(u + ('&' if '?' in u else '?') + f'regen={ns}')[0]
with cf.ThreadPoolExecutor(6) as ex: codes = list(ex.map(render, links))
print('rendered fresh:', sum(1 for c in codes if c == 200), '| non-200:', [(u, c) for u, c in zip(links, codes) if c != 200][:10])
css = set()
def refs(u):
    c, h = get(u)
    return re.findall(r'https://marketixdigital\.com\.au/wp-content/uploads/elementor/css/[^"\'?]+\.css', h)
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(refs, links): css.update(r)
with cf.ThreadPoolExecutor(8) as ex: st = dict(zip(sorted(css), ex.map(lambda u: get(u, 30)[0], sorted(css))))
missing = [u for u, c in st.items() if c != 200]
print('stylesheets referenced:', len(css), '| missing:', len(missing), missing[:10])
