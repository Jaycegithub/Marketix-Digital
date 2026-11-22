"""Map every Iconify icon named in the parsed docs to a white glyph in the media library (reuse if the SVG matches, else upload).
usage: python3 resolve_icons.py ../a.json ../b.json   (writes icons.json: 'prefix/name' -> {id,url}; also ../media.json)"""
import json, re, sys, os, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../live'))
from lv import req, UA
H = os.path.dirname(os.path.abspath(__file__))
ic = json.load(open(os.path.join(H, 'icons.json'))) if os.path.exists(os.path.join(H, 'icons.json')) else {}
want = set()
for f in sys.argv[1:]:
    for b in json.load(open(f))[8][0]:
        if 'iconify.design' in b['text']: want.add('/'.join(b['text'].rstrip('/').split('/')[-2:]))
media, pg = [], 1
while True:
    r = req('GET', f'wp/v2/media?per_page=100&page={pg}&_fields=id,source_url,mime_type')
    media += r
    if len(r) < 100: break
    pg += 1
json.dump(media, open(os.path.join(H, '..', 'media.json'), 'w'))
glyphs = [m for m in media if '/marketix-glyph-' in m['source_url'] and m['source_url'].endswith('.svg')]
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=60).read().decode()
def norm(s): return re.sub(r'\s+', '', re.sub(r'<svg[^>]*>', '', s)).lower().replace('currentcolor', '#ffffff').replace('#fff"', '#ffffff"')
cache = {}
def body(m):
    if m['id'] not in cache:
        try: cache[m['id']] = norm(get(m['source_url']))
        except Exception: cache[m['id']] = None
    return cache[m['id']]
for w in sorted(want):
    if w in ic: continue
    pre, nm = w.split('/')
    svg = get(f'https://api.iconify.design/{pre}/{nm}.svg?color=%23FFFFFF&width=24&height=24')
    n = norm(svg)
    hit = next((m for m in sorted(glyphs, key=lambda m: nm not in m['source_url']) if body(m) == n), None)
    if hit:
        ic[w] = {'id': hit['id'], 'url': hit['source_url']}; print('reuse', w, '->', hit['id'], hit['source_url'].split('/')[-1]); continue
    fn = f'marketix-glyph-{nm}.svg'
    if any(m['source_url'].split('/')[-1] == fn for m in glyphs): fn = f'marketix-glyph-{pre}-{nm}.svg'
    open(os.path.join(H, pre + '__' + nm + '.svg'), 'w').write(svg)
    m = req('POST', 'wp/v2/media', raw=svg.encode(), headers={'Content-Type': 'image/svg+xml', 'Content-Disposition': f'attachment; filename="{fn}"'})
    ic[w] = {'id': m['id'], 'url': m['source_url']}; glyphs.append(m); cache[m['id']] = n
    print('upload', w, '->', m['id'], fn)
json.dump(ic, open(os.path.join(H, 'icons.json'), 'w'), indent=1)
print('icons named:', len(want))
