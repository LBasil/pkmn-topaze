#!/usr/bin/env python3
"""Prepare les fichiers de la page Dialogues (artifact claude.ai) dans un dossier :
   dlg.json (textes + contexte), sprites.json (PNJ en data-URI), img/<layout>.png (cartes).
   python3 tools/topaze/i18n/mkart.py /tmp/art"""
import sys, os, json, io, base64
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'maps')); sys.path.insert(0, os.path.join(HERE, '..', 'editor'))
import extract, mapkit
from PIL import Image
out = sys.argv[1]; os.makedirs(out + '/img', exist_ok=True)
os.chdir(extract.ROOT)
db = extract.build()
maps = {}
sprites_needed = set()
lay_for = {}
for m, es in db.items():
    if not es: continue
    mj = json.load(open('data/maps/%s/map.json' % m))
    lay_for[m] = mj['layout']
    arr = []
    for e in es:
        w = e['who']
        arr.append({'l': e['label'], 'en': e['en'], 'k': e['kind'], 'c': e['conds'],
                    'w': ({'m': w['map'], 'g': w['gfx'].replace('OBJ_EVENT_GFX_', ''), 'x': w['x'], 'y': w['y'], 'h': w['hide'].replace('FLAG_', '')} if w else None),
                    'a': [{'c': a['conds'], 'm': a['who']['map']} for a in e['also']]})
        if w and w['gfx']: sprites_needed.add(w['gfx'])
    maps[m] = {'layout': lay_for[m], 'e': arr}
# cartes : une image par layout, aussi pour les cartes d'origine des textes partages
need = set(lay_for.values())
for m, d in maps.items():
    for e in d['e']:
        if e['w'] and e['w']['m'] not in lay_for:
            mj = json.load(open('data/maps/%s/map.json' % e['w']['m'])); lay_for[e['w']['m']] = mj['layout']; need.add(mj['layout'])
tot = 0
for lid in sorted(need):
    p = '%s/img/%s.png' % (out, lid)
    if os.path.exists(p): tot += os.path.getsize(p); continue
    try:
        im = mapkit.Layout(lid).render().convert('RGB')
    except Exception as ex:
        print('sans image', lid, type(ex).__name__); continue
    im = im.quantize(colors=48, method=Image.MEDIANCUT, dither=Image.NONE)
    im.save(p, optimize=True); tot += os.path.getsize(p)
print('images', len(need), 'total %.1f Mo' % (tot / 1e6))
# sprites
import server
sp = {}
for g in sorted(sprites_needed):
    d = server.sprite_png(g)
    if d: sp[g.replace('OBJ_EVENT_GFX_', '')] = 'data:image/png;base64,' + base64.b64encode(d).decode()
json.dump(sp, open(out + '/sprites.json', 'w'))
imgs = {f[:-4]: 'data:image/png;base64,' + base64.b64encode(open(out + '/img/' + f, 'rb').read()).decode() for f in sorted(os.listdir(out + '/img'))}
json.dump(imgs, open(out + '/imgs.json', 'w'), separators=(',', ':'))
json.dump({'maps': maps, 'layouts': lay_for}, open(out + '/dlg.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('sprites', len(sp), 'dlg.json %.2f Mo' % (os.path.getsize(out + '/dlg.json') / 1e6))
