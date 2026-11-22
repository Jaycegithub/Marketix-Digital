"""Parse a Google Docs HTML export (page-content table) into rows -> cells -> blocks.
usage: python3 -I parse_doc.py <doc.html> <out.json>
block = {t: p|li|img, html, text, bold, italic}  (bold/italic = the whole block's text is bold/italic)"""
import json, re, sys, html as H, urllib.parse
from bs4 import BeautifulSoup, NavigableString, Tag

def style(t): return (t.get('style') or '') if isinstance(t, Tag) else ''
def is_bold(s): return bool(re.search(r'font-weight:\s*(700|bold)', s))
def is_ital(s): return 'font-style:italic' in s.replace(' ', '')

def real_href(h):
    if 'google.com/url' in h:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(h).query).get('q')
        if q: return q[0]
    return h

def runs(node, b=False, i=False, href=None):
    """yield (text, bold, italic, href) runs in order"""
    for c in node.children:
        if isinstance(c, NavigableString):
            if str(c): yield (str(c), b, i, href)
        elif c.name == 'br': yield ('\n', b, i, href)
        elif c.name == 'img': continue
        else:
            s = style(c)
            nb = is_bold(s) if 'font-weight' in s else (b or c.name in ('b', 'strong'))
            ni = i or is_ital(s) or c.name in ('i', 'em')
            nh = real_href(c.get('href')) if c.name == 'a' and c.get('href') else href
            yield from runs(c, nb, ni, nh)

def block(el, t):
    rs = [r for r in runs(el)]
    text = ''.join(r[0] for r in rs)
    text = re.sub(r'[ \t ]+', ' ', text).strip()
    if not text:
        return {'t': 'img', 'html': '', 'text': '[image]', 'bold': False, 'italic': False} if el.find('img') else None
    vis = [r for r in rs if r[0].strip()]
    bold = all(r[1] for r in vis); ital = all(r[2] for r in vis)
    out = []
    for txt, rb, ri, rh in rs:
        e = H.escape(txt, quote=False).replace('\n', '<br>')
        if not txt.strip(): out.append(e); continue
        if ri: e = '<em>%s</em>' % e
        if rb: e = '<strong>%s</strong>' % e
        if rh: e = '<a href="%s">%s</a>' % (H.escape(rh), e)
        out.append(e)
    h = ''.join(out).strip()
    for tag in ('strong', 'em'):  # merge adjacent identical tags
        h = re.sub(r'</%s>(\s*)<%s>' % (tag, tag), r'\1', h)
    return {'t': t, 'html': re.sub(r'[ \t\r\n]+', ' ', h), 'text': text, 'bold': bold, 'italic': ital}

def cell_blocks(td):
    out = []
    for el in td.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if el.find_parent(['p', 'li']) is not None and el.name != 'li': continue
        b = block(el, 'li' if el.name == 'li' else 'p')
        if b: out.append(b)
    return out

soup = BeautifulSoup(open(sys.argv[1], encoding='utf-8').read(), 'lxml')
tb = soup.body.find('table')
trs = tb.find_all('tr', recursive=False) or tb.find('tbody').find_all('tr', recursive=False)
rows = [[cell_blocks(td) for td in tr.find_all('td', recursive=False)] for tr in trs]
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False)
for i, r in enumerate(rows):
    print(i, [len(c) for c in r], ' | '.join(c[0]['text'][:50] if c else '' for c in r))
