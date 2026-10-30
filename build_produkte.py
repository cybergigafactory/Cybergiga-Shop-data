#!/usr/bin/env python3
"""Regenerate produkte.json: published products of Printify shop 29296471, store order (newest published first).

Nur lesend: GET auf die Printify-API und GET auf die Store-Links.
Regel (README): visible nur, wenn Printify visible ist UND der Store-Link HTTP 200 liefert.
link_status 0 = keine Antwort (Timeout) nach allen Versuchen.
Token kommt aus PRINTIFY_API_TOKEN, steht im Header (nicht in der Kommandozeile) und wird nie ausgegeben.
Optional: Zielpfad als 1. Argument (Standard: produkte.json neben diesem Skript).
"""
import json, os, subprocess, sys, time, urllib.request, urllib.error

SHOP = 29296471


def get(path):
    for i in range(5):
        req = urllib.request.Request('https://api.printify.com/v1/' + path, headers={
            'Authorization': 'Bearer ' + os.environ['PRINTIFY_API_TOKEN'], 'User-Agent': 'cgf-build-produkte'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503) and i < 4:
                time.sleep(3 + 3 * i); continue
            raise SystemExit(f'GET {path}: HTTP {e.code}')
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            time.sleep(2 + 2 * i)
    raise SystemExit(f'GET {path}: keine Antwort')


def link_status(url, tries=3):
    code = 0
    for i in range(tries):
        out = subprocess.run(['curl', '-s', '-o', '/dev/null', '-L', '-w', '%{http_code}',
                              '--max-time', str(30 + 15 * i), url], capture_output=True, text=True).stdout
        code = int(out or 0)
        if code in (200, 404):
            return code
        time.sleep(2)
    return code


def cats(t):
    t = t.lower(); c = []
    if 'sweatshirt' in t: c = ['Sweatshirts']
    elif 'hoodie' in t: c = ['Hoodies']
    elif 't-shirt' in t: c = ['Shirts']
    elif 'mug' in t or 'tasse' in t: c = ['Tassen']
    elif 'tote' in t or 'tasche' in t: c = ['Taschen']
    if 'kinder' in t: c.append('Kinder')
    return c


prods = []; page = 1
while True:
    d = get(f'shops/{SHOP}/products.json?limit=50&page={page}'); prods += d['data']
    if page >= d.get('last_page', 1): break
    page += 1

archiv = set()
_ap = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'produkte-archiv.json')
if os.path.exists(_ap):
    archiv = {a['id'] for a in json.load(open(_ap))}
out = []
for p in prods:
    if p['id'] in archiv: continue
    ext = p.get('external') or {}
    if not ext.get('id'): continue
    en = [v for v in p['variants'] if v['is_enabled']]
    imgs = p.get('images', [])
    img = next((i['src'] for i in imgs if i.get('is_default')), imgs[0]['src'] if imgs else None)
    url = ext.get('handle') or None
    st = link_status(url) if url else 0
    out.append({'id': p['id'], 'title': p['title'], 'image': img,
                'price': min(v['price'] for v in en) / 100 if en else None,
                'currency': 'EUR', 'url': url, 'categories': cats(p['title']),
                'visible': bool(p['visible'] and st == 200), 'link_ok': st == 200, 'link_status': st,
                '_sid': int(ext['id'])})
out.sort(key=lambda x: -x['_sid'])
for o in out: o.pop('_sid')
target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'produkte.json')
with open(target, 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(len(out), 'products;', sum(o['visible'] for o in out), 'visible;',
      sum(1 for o in out if not o['url']), 'without url;',
      'status:', {s: sum(1 for o in out if o['link_status'] == s) for s in sorted({o['link_status'] for o in out})})
