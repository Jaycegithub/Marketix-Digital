"""Build service/industry page data from a parsed doc + live service-page sections.
usage: python3 -I build.py <name>   -> writes out_<name>.json (Elementor data list)"""
import json, copy, random, re, sys, os
D = os.path.dirname(os.path.abspath(__file__))
name = sys.argv[1]
rows = json.load(open(f'{D}/{name}.json'))
SH = json.loads(json.load(open(f'{D}/src_2627.json'))['meta']['_elementor_data'])   # Shopify SEO
AI = json.loads(json.load(open(f'{D}/src_2666.json'))['meta']['_elementor_data'])   # AI SEO (process section)
SY = json.loads(json.load(open(f'{D}/src_1295.json'))['meta']['_elementor_data'])   # SEO Agency Sydney (case studies)
media = {m['source_url'].split('/')[-1]: m for m in json.load(open(f'{D}/media.json'))}

def nid(): return '%07x' % random.getrandbits(28)
def reid(e):
    e['id'] = nid()
    for c in e.get('elements', []): reid(c)
def find(e, i):
    if e.get('id') == i: return e
    for c in e.get('elements', []):
        r = find(c, i)
        if r: return r
def parent_of(e, i):
    for c in e.get('elements', []):
        if c.get('id') == i: return e
        r = parent_of(c, i)
        if r: return r
def remove(root, i):
    p = parent_of(root, i); p['elements'] = [c for c in p['elements'] if c['id'] != i]
def setT(root, i, t, key='title'): find(root, i)['settings'][key] = t
def clone_of(root, i, t=None, key='title'):
    c = copy.deepcopy(find(root, i)); c['id'] = nid()
    for x in c.get('elements', []): reid(x)
    if t is not None: c['settings'][key] = t
    return c
def glyph(fn):
    m = media['marketix-glyph-%s.svg' % fn]
    return {'library': 'svg', 'value': {'id': m['id'], 'url': m['source_url']}}
def inner(b):
    h = b['html']
    for _ in range(2): h = re.sub(r'^<(strong|em)>(.*)</\1>$', r'\2', h, flags=re.S)
    return h

ICONS = {
 'link': ['text-link-analysis', 'target', 'compass', 'megaphone', 'file-content', 'file-report'],
 'local': ['target', 'google', 'map-pin', 'top-speed', 'file-content', 'link-chain', 'bar-chart'],
 'content': ['file-search', 'keyword-search', 'compass', 'copy-text', 'refresh', 'sitemap', 'graph-up'],
}.get(name, [])
ICONIFY = json.load(open(f'{D}/icons/icons.json'))
def topic_glyph(title):
    t = title.lower()
    for keys, g in ((('link',), 'link-chain'), (('technical',), 'settings-1'), (('local', 'destination'), 'location'),
                    (('conversion', 'tracking', 'measurement', 'reporting'), 'graph-up'),
                    (('keyword', 'research', 'search demand'), 'search-akar'), (('content',), 'file-content')):
        if any(k in t for k in keys): return g
    return 'multiple-pages'

R = lambda r, c=0: rows[r][c] if c < len(rows[r]) else []
sec = {i: copy.deepcopy(s) for i, s in enumerate(SH)}

# ---------- hero
hero = sec[0]; b = R(1)
setT(hero, '0cbb755', b[0]['text']); setT(hero, '9e7a157', b[1]['text'])
remove(hero, '1625dc8'); remove(hero, 'a85a6a0'); remove(hero, 'f9cfd3a')
ip = next(i for i, x in enumerate(b) if x['text'].startswith('Our approach follows'))
intro = [x for x in b[2:ip] if x['t'] == 'p']
after = [x for x in b[ip + 2:] if x['t'] == 'p']
setT(hero, 'c0dd6aa', intro[0]['html'])
col = parent_of(hero, 'c0dd6aa'); k = [c['id'] for c in col['elements']].index('c0dd6aa')
for j, x in enumerate(intro[1:]): col['elements'].insert(k + 1 + j, clone_of(hero, 'c0dd6aa', x['html']))
setT(hero, '269136f', b[ip]['html']); setT(hero, '12f3e84', after[0]['html'])
col = parent_of(hero, '12f3e84'); k = [c['id'] for c in col['elements']].index('12f3e84')
for j, x in enumerate(after[1:]): col['elements'].insert(k + 1 + j, clone_of(hero, '12f3e84', x['html']))
bul = [x for x in b if x['t'] == 'li']; il = find(hero, '5658623')
tmpl = il['settings']['icon_list'][0]
il['settings']['icon_list'] = [dict(copy.deepcopy(tmpl), _id=nid(), text=x['html']) for x in bul]

# ---------- case studies
if name == 'link':
    cs = sec[3]; b = R(4); setT(cs, 'bbbe794', b[0]['text']); setT(cs, '2d8c5ae', b[1]['html'])
else:
    cs = copy.deepcopy(SY[3])

# ---------- backed-by (3 items)
bk = sec[6]; b = R(7); remove(bk, 'fbfdea6'); setT(bk, '932f2a4', b[0]['text'])
for wid, (t, d) in zip(('caf7b1b', 'f444a94', '41e9057'), [(b[1], b[2]), (b[3], b[4]), (b[5], b[6])]):
    setT(bk, wid, t['text'], 'title_text'); setT(bk, wid, d['html'], 'description_text')

# ---------- services
sv = sec[7]; b = R(8); remove(sv, 'da7cd59'); remove(sv, '1f42297')
setT(sv, '2f74151', b[0]['text']); setT(sv, '495a9fc', b[1]['html'])
grid = find(sv, 'd074d17'); card_t = find(sv, '91c43b0')
pairs, icon_specs, pend = [], [], None
rest = b[2:]; i = 0
while i < len(rest):
    x = rest[i]
    if 'iconify.design' in x['text']: pend = '/'.join(x['text'].rstrip('/').split('/')[-2:]); i += 1; continue
    if x['bold'] and i + 1 < len(rest) and not rest[i + 1]['bold']:
        pairs.append((x, rest[i + 1])); icon_specs.append(pend); pend = None; i += 2; continue
    i += 1
cards = []
for n_, (t, d) in enumerate(pairs):
    c = copy.deepcopy(card_t); reid(c)
    ib = [x for x in c['elements'] if x.get('widgetType') == 'icon-box'][0]
    hd = [x for x in c['elements'] if x.get('widgetType') == 'heading'][0]
    ib['settings']['title_text'] = t['text']
    if icon_specs[n_]:
        g = ICONIFY[icon_specs[n_]]; ib['settings']['selected_icon'] = {'library': 'svg', 'value': {'id': g['id'], 'url': g['url']}}
    elif n_ < len(ICONS):
        ib['settings']['selected_icon'] = glyph(ICONS[n_])
    else:  # doc names no icon: same glyph the other industry pages use for that topic
        ib['settings']['selected_icon'] = glyph(topic_glyph(t['text']))
    hd['settings']['title'] = d['html']; c['elements'] = [ib, hd]; cards.append(c)
grid['elements'] = cards

# ---------- CTA
cta = sec[9]; b = R(10); setT(cta, '9209c3a', b[0]['text']); setT(cta, '9d972da', b[1]['html'])

# ---------- process (from AI SEO page)
pr = copy.deepcopy(AI[11]); b = R(11)
setT(pr, '0d4d9ad', b[0]['text'])
lab = find(pr, 'dd4a97c'); hdr = parent_of(pr, 'dd4a97c')
sub = clone_of(pr, '8c80e95', '<strong>%s</strong>' % b[1]['text'])
hdr['elements'] = [find(pr, '0d4d9ad'), sub]
steps = [(b[i], b[i + 1]) for i in range(2, 14, 2)]
for cid, (t, d), n in zip(('563794a', '3ac0b29', '814bbeb', '965dc59', '019a0b5', '1f44dd8'), steps, range(1, 7)):
    c = find(pr, cid); hs = [x for x in c['elements'] if x.get('widgetType') == 'heading']
    hs[0]['settings']['title'] = '%02d' % n
    hs[1]['settings']['title'] = re.sub(r'^Step\s*\d+:\s*', '', t['text'])
    hs[2]['settings']['title'] = d['html']
pr['settings']['_title'] = 'Process'

# ---------- why choose
wy = sec[10]; b = R(12); b2 = R(12, 1)
remove(wy, '97537f4'); setT(wy, 'eaa68c3', b[0]['text']); setT(wy, '84f4dec', '<strong>%s</strong>' % b[1]['text'])
colw = find(wy, '80bfaa1'); keep = [find(wy, 'eaa68c3'), find(wy, '84f4dec')]
for x in b[2:]:
    if x['bold'] and x['italic'] and ('→' in x['text'] or '>' in x['text']): keep.append(clone_of(wy, 'bde9b02', x['text']))
    elif x['bold'] and x['italic']: keep.append(clone_of(wy, '59dd553', inner(x)))
    elif x['text'].startswith('Our approach starts'): keep.append(clone_of(wy, 'eaacf3a', x['html']))
    else: keep.append(clone_of(wy, 'cfded6d', x['html']))
colw['elements'] = keep
items = [x for x in b2[1:] if x['t'] != 'img']
apart_ids = ('b73c175', 'fb034aa', '5246e39', '98ed043', '4dd1583', '13311eb')
for wid in apart_ids[len(items):]: remove(wy, wid)
for wid, x in zip(apart_ids, items):
    h = x['html']
    if '<strong>' not in h and ':' in h:
        a, z = h.split(':', 1); h = '<strong>%s:</strong>%s' % (a, z)
    setT(wy, wid, h, 'title_text')

# ---------- my journey
jy = sec[11]; b = R(13); colj = find(jy, 'b16729a')
colj['elements'] = [find(jy, '34e7914'), find(jy, '8558baa')] + [clone_of(jy, 'dc3ea5e', x['html']) for x in b[2:]]

# ---------- FAQ
fq = sec[12]; b = R(14); setT(fq, 'a163f8d', b[1]['html'])
acc = find(fq, 'eb73a4b'); it_t = acc['settings']['items'][0]; el_t = acc['elements'][0]
qa = []
for x in b[2:]:
    if x['bold'] and x['text'].rstrip().endswith('?') and x['t'] == 'p': qa.append([x['text'], []])
    elif qa: qa[-1][1].append(x)
def answer_html(bl):
    out, ul = [], []
    for x in bl:
        if x['t'] == 'li': ul.append('<li>%s</li>' % x['html']); continue
        if ul: out.append('<ul>%s</ul>' % ''.join(ul)); ul = []
        if x['t'] == 'p': out.append('<p>%s</p>' % x['html'])
    if ul: out.append('<ul>%s</ul>' % ''.join(ul))
    return ''.join(out)
new_items, new_els = [], []
for q, bl in qa:
    it = copy.deepcopy(it_t); it['_id'] = nid(); it['item_title'] = q
    el = copy.deepcopy(el_t); reid(el)
    te = [x for x in el['elements'] if x.get('widgetType') == 'text-editor'][0]
    te['settings']['editor'] = answer_html(bl); el['elements'] = [te]
    new_items.append(it); new_els.append(el)
acc['settings']['items'] = new_items; acc['elements'] = new_els

# ---------- contact
ct = sec[15]; b = R(17); setT(ct, 'f392ea2', b[1]['text'])
paras = [x for x in b[2:] if x['t'] == 'p']
setT(ct, '8f00e5a', paras[0]['html'])
if len(paras) > 1: setT(ct, '3e84537', paras[1]['html'])
else: remove(ct, '3e84537')

order = [sec[0], sec[1], sec[2], cs, sec[4], sec[5], bk, sv, sec[8], cta, pr, wy, jy, fq, sec[13], sec[14], ct]
CIS = json.load(open(f'{D}/heights_{name}.json')) if os.path.exists(f'{D}/heights_{name}.json') else {}
for k_, s in enumerate(order):
    reid(s)
    css = s['settings'].get('custom_css') or ''
    css = re.sub(r'/\*mx-cis\*/.*?/\*mx-cis\*/', '', css, flags=re.S).strip()
    if str(k_) in CIS and k_ >= 2:
        css = (css + '\n' if css else '') + '/*mx-cis*/@media (max-width:767px){selector{contain-intrinsic-size:auto %dpx}}/*mx-cis*/' % CIS[str(k_)]
    s['settings']['custom_css'] = css
    s['settings']['css_classes'] = ' '.join(c for c in (s['settings'].get('css_classes') or '').split() if c != 'mx-no-cv')
json.dump(order, open(f'{D}/out_{name}.json', 'w'))
print(name, 'sections', len(order), 'services', len(cards), 'faq', len(qa), 'hero bullets', len(bul), 'cis', len(CIS))
