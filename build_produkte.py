#!/usr/bin/env python3
"""Regenerate produkte.json: published products of Printify shop 29296471, store order (newest published first)."""
import json,os,urllib.request,subprocess
SHOP=29296471
def get(path):
    out=subprocess.run(['curl','-s','-H','Authorization: Bearer '+os.environ['PRINTIFY_API_TOKEN'],'https://api.printify.com/v1/'+path],capture_output=True,text=True).stdout
    return json.loads(out)
prods=[];page=1
while True:
    d=get(f'shops/{SHOP}/products.json?limit=50&page={page}');prods+=d['data']
    if page>=d.get('last_page',1): break
    page+=1
def cats(t):
    t=t.lower();c=[]
    if 'sweatshirt' in t: c=['Sweatshirts']
    elif 'hoodie' in t: c=['Hoodies']
    elif 't-shirt' in t: c=['Shirts']
    elif 'mug' in t or 'tasse' in t: c=['Tassen']
    elif 'tote' in t or 'tasche' in t: c=['Taschen']
    if 'kinder' in t: c.append('Kinder')
    return c
out=[]
for p in prods:
    ext=p.get('external') or {}
    if not ext.get('id'): continue
    en=[v for v in p['variants'] if v['is_enabled']]
    imgs=p.get('images',[])
    img=next((i['src'] for i in imgs if i.get('is_default')),imgs[0]['src'] if imgs else None)
    out.append({'id':p['id'],'title':p['title'],'image':img,'price':min(v['price'] for v in en)/100 if en else None,
      'currency':'EUR','url':ext.get('handle') or None,'categories':cats(p['title']),'visible':p['visible'],'_sid':int(ext['id'])})
out.sort(key=lambda x:-x['_sid'])
for o in out: o.pop('_sid')
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'produkte.json'),'w'),ensure_ascii=False,indent=2)
print(len(out),'products;',sum(1 for o in out if not o['url']),'without url')
