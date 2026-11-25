"""python3 preview.py <idsfile> n1 n2 ...  : (re)create password previews zz-preview-<n> from out_<n>.json"""
import json, sys, os
from lv import req
pm = json.load(open('../newpages/pagemeta.json')); f = '../newpages/' + sys.argv[1]
old = json.load(open(f)) if os.path.exists(f) else {}; ids = {}
for n in sys.argv[2:]:
    if n in old:
        p = req('GET', f'wp/v2/pages/{old[n]}?context=edit&_fields=slug'); assert p['slug'] == f'zz-preview-{n}', p
        req('DELETE', f'wp/v2/pages/{old[n]}?force=true')
    else:
        assert not req('GET', f'wp/v2/pages?slug=zz-preview-{n}&status=any&_fields=id')
    t = json.load(open(f'../newpages/{n}.json'))[1][0][0]['text'].strip()
    meta = dict(pm['meta']); meta['_elementor_data'] = open(f'../newpages/out_{n}.json').read()
    r = req('POST', 'wp/v2/pages', {'title': t, 'slug': f'zz-preview-{n}', 'status': 'publish', 'password': 'mxprev', 'template': pm['template'], 'meta': meta})
    ids[n] = r['id']; print(n, old.get(n), '->', r['id'], t)
json.dump(ids, open(f, 'w'))
