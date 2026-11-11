"""Full crawl of live (MotoCMS) and staging (WordPress): every URL with status, redirect, title, meta, H1, canonical,
robots, word count, internal links and images. Then a comparison per live URL. Writes CSV exports."""
import re, json, csv, html, urllib.request, urllib.error, urllib.parse, concurrent.futures, time, sys

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36'}
SITES = {'live': 'https://marketixdigital.com.au', 'dev': 'https://dev.marketixdigital.com.au'}
SKIP = re.compile(r'\.(png|jpe?g|gif|webp|svg|css|js|ico|woff2?|ttf|mp4|zip|xml|txt)$', re.I)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


nr = urllib.request.build_opener(NoRedirect)


def fetch(url):
    """status, location (if redirect), body"""
    for a in range(3):
        try:
            r = nr.open(urllib.request.Request(url, headers=UA), timeout=60)
            ct = r.headers.get('Content-Type', '')
            body = r.read().decode('utf-8', 'ignore') if 'html' in ct else ''
            return r.status, None, body, ct
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                return e.code, urllib.parse.urljoin(url, e.headers.get('Location') or ''), '', ''
            if e.code in (404, 410, 403, 500):
                return e.code, None, '', ''
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return 'err', None, '', ''


def text_of(h):
    body = h[h.find('<body'):] if '<body' in h else h
    body = re.sub(r'<(script|style|noscript|header|footer|nav)\b[^>]*>.*?</\1>', ' ', body, flags=re.S | re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body))).strip()


def parse(h, base, host):
    head = h[:h.find('</head>')] if '</head>' in h else h[:200000]
    g = lambda rx: (lambda m: html.unescape(m.group(1)).strip() if m else '')(re.search(rx, head, re.S | re.I))
    h1s = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip() for x in re.findall(r'<h1\b[^>]*>(.*?)</h1>', h, re.S | re.I)]
    links, imgs = set(), set()
    for u in re.findall(r'<a\b[^>]*href=["\']([^"\'#]+)', h, re.I):
        u = urllib.parse.urljoin(base, html.unescape(u))
        p = urllib.parse.urlparse(u)
        if p.netloc in host and not SKIP.search(p.path):
            links.add(p.path or '/')
    for u in re.findall(r'<img\b[^>]*(?:src|data-src)=["\']([^"\']+)', h, re.I):
        imgs.add(urllib.parse.urljoin(base, u))
    return {'title': g(r'<title[^>]*>(.*?)</title>'),
            'description': g(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']*)'),
            'canonical': g(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)'),
            'robots': g(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']*)'),
            'h1': ' | '.join(h1s), 'h1_count': len(h1s), 'words': len(text_of(h).split()),
            'links': sorted(links), 'images': len(imgs)}


def crawl(site, seeds):
    base = SITES[site]
    host = (urllib.parse.urlparse(base).netloc, 'www.' + urllib.parse.urlparse(base).netloc)
    seen, queue, res = set(), list(seeds), {}

    def visit(path):
        st, loc, body, ct = fetch(base + urllib.parse.quote(path, safe='/%?=&'))
        info = {'status': st, 'location': loc}
        if st == 200 and body:
            info.update(parse(body, base + path, host))
        return path, info

    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        while queue:
            batch = [q for q in dict.fromkeys(queue) if q not in seen]
            queue = []
            seen.update(batch)
            for path, info in ex.map(visit, batch):
                res[path] = info
                for l in info.get('links', []):
                    if l not in seen:
                        queue.append(l)
                if info['status'] in (301, 302, 307, 308) and info['location']:
                    p = urllib.parse.urlparse(info['location'])
                    if p.netloc in host and p.path not in seen:
                        queue.append(p.path or '/')
            print(site, 'crawled', len(res), flush=True)
    return res


def sitemap_urls(site):
    out = set()
    try:
        if site == 'live':
            x = urllib.request.urlopen(urllib.request.Request(SITES[site] + '/mt-content/storage/sitemaps/website.xml', headers=UA), timeout=60).read().decode()
            out |= {urllib.parse.urlparse(u).path for u in re.findall(r'<loc>(.*?)</loc>', x)}
        else:
            idx = urllib.request.urlopen(urllib.request.Request(SITES[site] + '/sitemap_index.xml', headers=UA), timeout=60).read().decode()
            for sm in re.findall(r'<loc>(.*?)</loc>', idx):
                x = urllib.request.urlopen(urllib.request.Request(sm, headers=UA), timeout=60).read().decode()
                out |= {urllib.parse.urlparse(u).path for u in re.findall(r'<loc>(.*?)</loc>', x) if not SKIP.search(u)}
    except Exception as e:
        print('sitemap error', site, e)
    return out


if __name__ == '__main__':
    tracker = set()
    for row in csv.reader(open('/root/.claude/projects/-home-user-Marketix-Digital/11ecfe0b-7dc4-58e1-b6b3-f632aaff687c/tool-results/mcp-Google_Drive-blob-1794360119101-9857pr.csv')):
        if row and row[0].startswith('https://marketixdigital.com.au'):
            tracker.add(urllib.parse.urlparse(row[0]).path)
    live_sm, dev_sm = sitemap_urls('live'), sitemap_urls('dev')
    json.dump({'live_sitemap': sorted(live_sm), 'dev_sitemap': sorted(dev_sm), 'tracker': sorted(tracker)}, open('seeds.json', 'w'), indent=1)
    live = crawl('live', {'/'} | live_sm | tracker | {'/thank-you/', '/thank-you-tradie-download/', '/thank-you-7-killer-ways-to-get-more-calls/'})
    json.dump(live, open('live_inventory.json', 'w'), indent=1)
    dev = crawl('dev', {'/'} | dev_sm)
    json.dump(dev, open('dev_inventory.json', 'w'), indent=1)
    print('live', len(live), 'dev', len(dev), 'live sitemap', len(live_sm), 'dev sitemap', len(dev_sm))
