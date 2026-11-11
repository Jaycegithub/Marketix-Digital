import json, csv, re, os, difflib, urllib.parse, collections, html
sys_path = '/tmp/claude-0/-home-user-Marketix-Digital/11ecfe0b-7dc4-58e1-b6b3-f632aaff687c/scratchpad/wp/v90'
os.chdir(sys_path)
import crawl_both as cb

live = json.load(open('live_inventory.json'))
dev = json.load(open('dev_inventory.json'))
seeds = json.load(open('seeds.json'))
OUT = '/home/user/Marketix-Digital/qa'
os.makedirs(OUT, exist_ok=True)

DEVB = 'https://dev.marketixdigital.com.au'


def dev_follow(path, hops=0, chain=None):
    """follow dev redirects; return final status, final url, chain"""
    chain = chain or []
    info = dev.get(path)
    if info is None:
        st, loc, body, ct = cb.fetch(DEVB + urllib.parse.quote(path, safe='/%?=&'))
        info = {'status': st, 'location': loc}
        if st == 200 and body:
            info.update(cb.parse(body, DEVB + path, ('dev.marketixdigital.com.au',)))
        dev[path] = info
    st = info['status']
    if st in (301, 302, 307, 308) and hops < 6:
        loc = info['location'] or ''
        chain.append((st, loc))
        p = urllib.parse.urlparse(loc)
        if p.netloc == 'dev.marketixdigital.com.au':
            return dev_follow(p.path + (('?' + p.query) if p.query else ''), hops + 1, chain)
        # external (old site / pdf host): check it
        st2, loc2, _, _ = cb.fetch(loc)
        return st2, loc, chain
    return st, DEVB + path, chain


def norm(s):
    return re.sub(r'\s+', ' ', (s or '').replace(' ', ' ')).strip().lower()


rows = []
live_pages = {p: v for p, v in live.items() if v['status'] == 200 and not p.lower().endswith('.pdf')}
live_redirects = {p: v for p, v in live.items() if v['status'] in (301, 302, 307, 308)}
live_404 = {p: v for p, v in live.items() if v['status'] in (404, 410)}
for p, v in sorted(live.items()):
    if v['status'] not in (200, 301, 302, 307, 308):
        continue
    fst, furl, chain = dev_follow(p)
    first = chain[0][0] if chain else fst
    if first == 200:
        cls = 'unchanged'
    elif first == 301 and fst == 200:
        cls = 'moved (301)'
    elif first == 302:
        tgt = chain[0][1]
        cls = 'awaiting migration (302 -> %s)' % ('homepage' if urllib.parse.urlparse(tgt).path in ('', '/') else
                                                   '/industries/' if urllib.parse.urlparse(tgt).path == '/industries/' else
                                                   'old site' if 'old.marketix' in tgt else tgt)
    elif fst in (404, 410):
        cls = 'REMOVED - 404'
    else:
        cls = 'other: %s' % fst
    d = dev.get(p, {}) if first == 200 else {}
    lv = v if v['status'] == 200 else {}
    rows.append({
        'live_url': 'https://marketixdigital.com.au' + p, 'live_status': v['status'],
        'live_redirect_to': v.get('location') or '', 'in_live_sitemap': p in set(seeds['live_sitemap']),
        'dev_first_status': first, 'dev_final_status': fst, 'dev_final_url': furl, 'redirect_hops': len(chain),
        'treatment': cls,
        'title_match': (norm(lv.get('title')) == norm(d.get('title'))) if lv and d else '',
        'desc_match': (norm(lv.get('description')) == norm(d.get('description'))) if lv and d and lv.get('description') else '',
        'h1_live': lv.get('h1', ''), 'h1_dev': d.get('h1', ''),
        'h1_match': (norm(lv.get('h1')) == norm(d.get('h1'))) if lv and d else '',
        'dev_h1_count': d.get('h1_count', ''),
        'words_live': lv.get('words', ''), 'words_dev': d.get('words', ''),
        'robots_live': lv.get('robots', ''), 'canonical_live': lv.get('canonical', ''), 'canonical_dev': d.get('canonical', ''),
    })

with open(OUT + '/url-comparison.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)


def export(inv, name, base):
    with open(OUT + '/' + name, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['url', 'status', 'redirect_to', 'title', 'meta_description', 'h1', 'h1_count', 'canonical', 'robots', 'words', 'internal_links', 'images'])
        for p, v in sorted(inv.items()):
            w.writerow([base + p, v['status'], v.get('location') or '', v.get('title', ''), v.get('description', ''), v.get('h1', ''),
                        v.get('h1_count', ''), v.get('canonical', ''), v.get('robots', ''), v.get('words', ''), len(v.get('links', [])), v.get('images', '')])


export(live, 'live-motocms-urls.csv', 'https://marketixdigital.com.au')
export(dev, 'staging-wordpress-urls.csv', DEVB)

c = collections.Counter(r['treatment'] for r in rows)
print('treatment counts:', dict(c))
print('live pages 200:', len(live_pages), '| live redirects:', len(live_redirects), '| live 404 links:', len(live_404))
for r in rows:
    if r['treatment'].startswith('REMOVED') or r['treatment'].startswith('other'):
        print('  !!', r['live_url'], r['treatment'])
mig = [r for r in rows if r['treatment'] == 'unchanged' and r['live_status'] == 200]
print('migrated pages compared:', len(mig),
      '| title match', sum(1 for r in mig if r['title_match'] is True),
      '| desc match', sum(1 for r in mig if r['desc_match'] is True), 'of', sum(1 for r in mig if r['desc_match'] != ''),
      '| h1 match', sum(1 for r in mig if r['h1_match'] is True))
print('dev pages with h1 count != 1:', [(r['live_url'][30:], r['dev_h1_count']) for r in mig if r['dev_h1_count'] not in (1, '')][:30])
chains = [r for r in rows if r['redirect_hops'] and r['redirect_hops'] > 1]
print('redirect chains (>1 hop):', len(chains), [(r['live_url'][30:], r['redirect_hops']) for r in chains][:10])
print('live 404 links:', sorted(live_404)[:20])
json.dump(rows, open('comparison.json', 'w'), indent=1)
json.dump(dev, open('dev_inventory_plus.json', 'w'), indent=1)
