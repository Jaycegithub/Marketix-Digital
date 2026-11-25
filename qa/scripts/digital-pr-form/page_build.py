"""Build the updated Digital PR page data.
usage: python3 page_build.py <hero_tpl_id> <enquiry_tpl_id> <out.json>"""
import json, copy, random, sys, os
D = os.path.dirname(os.path.abspath(__file__))
hero_tpl, enq_tpl, out = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.loads(json.load(open(f'{D}/page_2049_orig.json'))['meta']['_elementor_data'])
ANCHOR = 'digital-pr-strategy'
def nid(): return '%07x' % random.getrandbits(28)
def find(e, i):
    if e.get('id') == i: return e
    for c in e.get('elements', []):
        r = find(c, i)
        if r: return r
def F(i):
    for s in d:
        r = find(s, i)
        if r: return r
def walk(e, f):
    f(e)
    for c in e.get('elements', []): walk(c, f)

# hero form template
F('f0c8b8e')['settings']['template_id'] = str(hero_tpl)

# bottom form panel: heading + intro + dedicated enquiry form, with the anchor
col = F('c2b0b44'); cs = col['settings']
cs['_element_id'] = ANCHOR
cs['custom_css'] = (cs.get('custom_css') or '') + '\nselector{scroll-margin-top:110px}'
h = F('7f6e58e'); h['settings']['title'] = 'Discuss Your Digital PR Strategy'; h['settings']['header_size'] = 'h3'
intro = copy.deepcopy(F('4cf0851')); intro['id'] = nid()
intro['settings']['title'] = ('Discover how original research and targeted media outreach can strengthen your competitive position, '
                              'build industry authority and support commercial growth.')
intro['settings']['_margin'] = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '8', 'left': '0', 'isLinked': False}
tw = F('1a0ecd9'); tw['settings']['template_id'] = str(enq_tpl); tw['settings']['_title'] = 'Digital PR Enquiry Form'
col['elements'] = [h, intro, tw]

# Our Approach (shared template 1270): page-local copy so its strategy-call button can point to the form
wrap = d[5]; assert wrap['settings'].get('_title') == 'Our Approach Section'
tw5 = [e for e in wrap['elements'] if e.get('widgetType') == 'template' and str(e['settings'].get('template_id')) == '1270'][0]
local = json.load(open(f'{D}/tpl_1270.json'))
def reid(e):
    e['id'] = nid()
    for c in e.get('elements', []): reid(c)
for e in local: reid(e)
wrap['elements'] = [x for e in wrap['elements'] for x in (local if e is tw5 else [e])]

# strategy-call CTAs (and the dead "#contact" link) -> the form
changed = []
def cta(e):
    if e.get('widgetType') != 'button': return
    s = e['settings']; url = (s.get('link') or {}).get('url', '')
    if s.get('text') == 'Book A Strategy Call' or url == '#contact':
        s['link'] = {'url': '#' + ANCHOR, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}
        changed.append((e['id'], s.get('text'), url))
for s in d: walk(s, cta)

# pricing FAQ
acc = []
walk(d[16], lambda e: acc.append(e) if e.get('widgetType') == 'nested-accordion' else None)
a = acc[0]; k = [it['item_title'] for it in a['settings']['items']].index('How much does a Digital PR campaign cost?')
te = [x for x in a['elements'][k]['elements'] if x.get('widgetType') == 'text-editor'][0]
old_answer = te['settings']['editor']
te['settings']['editor'] = ('<p>Our research-led Digital PR programmes start from $5,000 + GST per month. Investment is determined by your '
                            'commercial objectives, competitive landscape, research requirements and the scope of editorial outreach.</p>')
json.dump(d, open(out, 'w'))
print('CTAs re-pointed:', changed)
print('old pricing answer:', old_answer)
