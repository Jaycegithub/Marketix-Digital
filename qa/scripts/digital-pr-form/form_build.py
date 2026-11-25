"""Build the new Digital PR enquiry form data from template 2903.
usage: python3 form_build.py  -> writes tpl_hero.json (2903, form_name 'Digital PR - Hero')
                                   and tpl_enquiry.json (new template, form_name 'Digital PR - Enquiry')"""
import json, copy, re, random, os
D = os.path.dirname(os.path.abspath(__file__))
t = json.load(open(f'{D}/tpl_2903_orig.json'))
data = json.loads(t['meta']['_elementor_data'])
def nid(): return '%07x' % random.getrandbits(28)
form = data[0]['elements'][0]; s = form['settings']
old = {f['custom_id']: f for f in s['form_fields']}

def fld(cid, label, ftype=None, ph=None, **kw):
    f = {'custom_id': cid, 'field_label': label, 'dynamic': {'active': True}, '_id': old.get(cid, {}).get('_id') or {'job_title': 'b17c2a0', 'objectives': 'c28d3b1', 'investment': 'd39e4c2'}[cid], 'required': 'true'}
    if ftype: f['field_type'] = ftype
    if ph is not None: f['placeholder'] = ph
    f.update(kw); return f

OBJ = ['Strengthen organic search competitiveness', 'Earn relevant editorial backlinks', 'Build industry authority and credibility',
       'Increase brand visibility and media coverage', 'Develop original industry research assets', 'Improve visibility across AI search platforms']
INV = ['$5,000 to under $7,500', '$7,500 to under $10,000', '$10,000 to under $15,000', '$15,000 to under $25,000', '$25,000+',
       'Seeking an investment recommendation']
fields = [
    fld('name', 'Full name', ph='Full name'),
    fld('job_title', 'Job title', ph='Job title'),
    fld('email', 'Work email', 'email', 'email@company.com.au'),
    fld('phone', 'Phone number', 'tel', '04xx xxx xxx'),
    fld('company', 'Company name', ph='Company name'),
    fld('website', 'Website URL', ph='website.com.au'),
    fld('objectives', 'What are your primary objectives?', 'checkbox', field_options='\n'.join(OBJ), css_classes='mx-required-group'),
    fld('investment', 'Anticipated monthly Digital PR investment', 'radio', field_options='\n'.join(INV)),
    {'custom_id': 'investment_note', 'field_type': 'html', 'field_label': '', '_id': 'a0d1e57',
     'field_html': '<p class="mx-field-note" style="margin:-4px 0 0;font-size:13px;line-height:1.4;color:#596785">AUD, excluding GST</p>'},
    fld('message', 'What are your commercial objectives or competitive challenges?', 'textarea',
        'Tell us about your business, priority markets and what you want to achieve through Digital PR.', rows='4'),
    old['page_title'], old['page_url'], old['field_hp'],
]
s['form_fields'] = fields
s['button_text'] = 'Book a Digital PR Strategy Call'
s['custom_css'] = (
    "selector .elementor-field-type-checkbox .elementor-field-subgroup,selector .elementor-field-type-radio .elementor-field-subgroup{display:flex;flex-direction:column;gap:10px;padding-top:2px}"
    "selector .elementor-field-subgroup .elementor-field-option{display:flex;align-items:flex-start;gap:10px;margin:0}"
    "selector .elementor-field-option input{flex:none;width:18px;height:18px;margin:3px 0 0;accent-color:var(--e-global-color-secondary,#3D68EA);cursor:pointer}"
    "selector .elementor-field-option label{font-size:15px;line-height:1.5;color:var(--e-global-color-text,#4A5263);cursor:pointer}"
    "selector .elementor-field-type-html{padding-top:0}")

# lead + confirmation emails: rebuild the "details" table rows for the new fields
ROWS = [('Full name', 'name'), ('Job title', 'job_title'), ('Work email', 'email'), ('Phone number', 'phone'),
        ('Company name', 'company'), ('Website URL', 'website'), ('Primary objectives', 'objectives'),
        ('Anticipated monthly Digital PR investment (AUD, excluding GST)', 'investment'),
        ('Commercial objectives or competitive challenges', 'message')]
row_re = re.compile(r'<tr><td[^>]*>[^<]*</td><td[^>]*>\[field id="(?:website|message|name|company|email|phone)"\]</td></tr>')
for key in ('email_content', 'email_content_2'):
    h = s[key]; rows = row_re.findall(h); assert len(rows) == 6, (key, len(rows))
    tmpl = rows[0]
    new = ''.join(re.sub(r'>[^<]*</td><td', '>%s</td><td' % lab, re.sub(r'\[field id="[^"]+"\]', '[field id="%s"]' % cid, tmpl), count=1)
                  for lab, cid in ROWS)
    start = h.index(rows[0]); end = h.index(rows[-1]) + len(rows[-1])
    s[key] = h[:start] + new + h[end:]

hero = copy.deepcopy(data); hero[0]['elements'][0]['settings']['form_name'] = 'Digital PR - Hero'
enq = copy.deepcopy(data)
for e in enq: e['id'] = 'e' + e['id'][1:]; e['elements'][0]['id'] = 'e' + e['elements'][0]['id'][1:]   # stable ids
enq[0]['elements'][0]['settings']['form_name'] = 'Digital PR - Enquiry'
json.dump(hero, open(f'{D}/tpl_hero.json', 'w')); json.dump(enq, open(f'{D}/tpl_enquiry.json', 'w'))
for f in fields: print(f.get('custom_id'), f.get('field_type', 'text'), '|', f.get('field_label'), '|', f.get('placeholder', ''), '|', (f.get('field_options') or '').replace('\n', ' / ')[:90])
print('emails rows:', [len(re.findall(r'\[field id="', hero[0]['elements'][0]['settings'][k])) for k in ('email_content', 'email_content_2')])
