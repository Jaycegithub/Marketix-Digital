import json, urllib.parse, collections, concurrent.futures, csv
import crawl_both as cb
live = json.load(open('live_inventory.json'))
D = 'https://dev.marketixdigital.com.au'
def follow(url):
    chain, seen = [], set()
    for _ in range(8):
        st, loc, body, ct = cb.fetch(url)
        if body and 'One moment, please' in body:
            st, loc, body, ct = cb.fetch(url)
        if st in (301, 302, 307, 308):
            if loc in seen: return chain, 'LOOP', loc
            seen.add(loc); chain.append((st, loc)); url = loc
        else:
            return chain, st, url
    return chain, 'TOO_MANY', url
def test(p):
    v = live[p]
    chain, fst, furl = follow(D + urllib.parse.quote(p, safe='/%?=&'))
    exp = ''
    if p.startswith('/blog/') and v['status'] in (301, 302) and v.get('location'):
        exp = urllib.parse.urlparse(v['location']).path  # live destination path
    return p, v['status'], chain, fst, furl, exp
paths = [p for p, v in live.items() if v['status'] in (200, 301, 302, 307, 308)]
with concurrent.futures.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(test, paths))
issues = collections.defaultdict(list); rows = []
for p, lst, chain, fst, furl, exp in sorted(res):
    fp = urllib.parse.urlparse(furl).path
    first = chain[0][0] if chain else fst
    if fst in ('LOOP', 'TOO_MANY'): issues['loop'].append(p)
    elif len(chain) > 1: issues['chain'].append((p, len(chain), [c[1] for c in chain]))
    if fst not in (200,) and fst not in ('LOOP', 'TOO_MANY'): issues['final_not_200'].append((p, fst, furl))
    if exp and fst == 200 and fp != exp and fp != '/insights/': issues['blog_mismatch'].append((p, exp, fp))
    if first == 307 or first == 308: issues['non301'].append(p)
    rows.append([ 'https://marketixdigital.com.au' + p, lst, first, len(chain), ' > '.join('%s %s' % c for c in chain), fst, furl])
with open('/home/user/Marketix-Digital/qa/redirect-test.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['live_url', 'live_status', 'staging_first_status', 'hops', 'chain', 'final_status', 'final_url']); w.writerows(rows)
c = collections.Counter((r[2], r[3]) for r in rows)
print('tested', len(rows), 'first-status/hops:', dict(c))
for k, v in issues.items(): print(k, len(v)); [print('   ', x) for x in v[:25]]
blog = [r for r in rows if '/blog/' in r[0]]
print('blog urls', len(blog), 'single-hop 301 to 200:', sum(1 for r in blog if r[2] == 301 and r[3] == 1 and r[5] == 200))
