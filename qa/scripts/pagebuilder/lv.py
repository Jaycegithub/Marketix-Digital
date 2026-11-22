"""Live WP REST helper. Auth is injected by the session proxy (Basic app password)."""
import json, time, urllib.request, urllib.error
BASE = 'https://marketixdigital.com.au/wp-json/'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36'
def req(method, path, body=None, raw=None, headers=None, tries=4):
    url = path if path.startswith('http') else BASE + path
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    h = {'User-Agent': UA, 'Accept': 'application/json'}
    if body is not None and raw is None: h['Content-Type'] = 'application/json'
    h.update(headers or {})
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=h), timeout=120)
            t = r.read().decode() or 'null'
            return json.loads(t)
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:600]
            if e.code >= 500 and i < tries - 1: time.sleep(3 * (i + 1)); continue
            raise RuntimeError(f'{method} {path} -> {e.code}: {msg}')
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if i < tries - 1: time.sleep(3 * (i + 1)); continue
            raise
def walk(e, f):
    f(e)
    for c in e.get('elements', []): walk(c, f)
