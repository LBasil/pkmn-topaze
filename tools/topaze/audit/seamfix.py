#!/usr/bin/env python3
"""Corrige les tuiles parasites aux jointures sans warp entre maps de tilesets differents.
Le moteur dessine la carte voisine avec le tileset de la carte courante : on remplace, dans la bande
visible (DEPTH tuiles) de chaque carte, les metatiles qui se rendent mal dans le tileset voisin par un
metatile de meme comportement qui rend pareil dans les DEUX tilesets.
Usage: seamfix.py [--apply] [Carte ...]   (sans carte = toutes les connexions)"""
import sys, os, re, json, struct, glob
sys.dont_write_bytecode = True
import numpy as np
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
os.chdir(R)
LAY = {d['id']: d for d in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in d}
MAPS = {}; ID = {}
for f in glob.glob('data/maps/*/map.json'):
    d = json.load(open(f)); n = os.path.basename(os.path.dirname(f)); MAPS[n] = d; ID[d['id']] = n
hdr = open('src/data/tilesets/headers.h').read() + open('src/data/tilesets/metatiles.h').read() + open('src/data/tilesets/graphics.h').read()
def tdir(label):
    n = label.replace('gTileset_', '')
    m = re.search(r'gMetatiles_%s\[\] = INCBIN_U16\("(data/tilesets/\w+/\w+)/metatiles.bin' % n, hdr)
    return m.group(1) if m else None
_T = {}
def tileset(label):
    if label in _T: return _T[label]
    p = tdir(label); sec = '/secondary/' in p
    mt = np.frombuffer(open(p + '/metatiles.bin', 'rb').read(), '<u2').reshape(-1, 8)
    at = np.frombuffer(open(p + '/metatile_attributes.bin', 'rb').read(), '<u4')
    raw = open(p + '/tiles.4bpp', 'rb').read()
    b = np.frombuffer(raw, np.uint8); px = np.empty(len(b) * 2, np.uint8); px[0::2] = b & 15; px[1::2] = b >> 4
    tiles = px.reshape(-1, 8, 8)
    pal = np.zeros((16, 16, 3), np.float32)
    for i in range(16):
        fp = '%s/palettes/%02d.gbapal' % (p, i)
        if os.path.exists(fp):
            c = np.frombuffer(open(fp, 'rb').read(), '<u2')
            pal[i] = np.stack([(c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3], 1)
    _T[label] = (p, sec, mt, at, tiles, pal); return _T[label]
_cache = {}
def render(prim, secd, mid):
    k = (prim, secd, mid)
    if k in _cache: return _cache[k]
    P = tileset(prim); S = tileset(secd)
    if mid < 640: mt = P[2][mid] if mid < len(P[2]) else None
    else: mt = S[2][mid - 640] if mid - 640 < len(S[2]) else None
    if mt is None: _cache[k] = None; return None
    img = np.zeros((16, 16, 3), np.float32)
    for layer in (0, 1):
        for q in range(4):
            e = int(mt[layer * 4 + q]); t = e & 0x3ff; hf = e >> 10 & 1; vf = e >> 11 & 1; pl = e >> 12
            if t < 640: tl = P[4][t] if t < len(P[4]) else None
            else: tl = S[4][t - 640] if t - 640 < len(S[4]) else None
            if tl is None: continue
            if hf: tl = tl[:, ::-1]
            if vf: tl = tl[::-1, :]
            pp = P[5] if pl < 7 else S[5]
            col = pp[pl][tl]
            msk = (tl != 0)[..., None] if layer else np.ones((8, 8, 1), bool)
            y, x = (q // 2) * 8, (q % 2) * 8
            img[y:y+8, x:x+8] = np.where(msk, col, img[y:y+8, x:x+8])
    _cache[k] = img; return img
def attr(prim, secd, mid):
    P = tileset(prim); S = tileset(secd)
    a = P[3][mid] if mid < 640 and mid < len(P[3]) else (S[3][mid - 640] if mid >= 640 and mid - 640 < len(S[3]) else None)
    return None if a is None else int(a) & ~(3 << 29)
def dist(a, b):
    return 1e9 if a is None or b is None else float(np.abs(a - b).mean())
def load(n):
    l = LAY[MAPS[n]['layout']]
    return l, list(struct.unpack('<%dH' % (l['width'] * l['height']), open(l['blockdata_filepath'], 'rb').read()))
DEPTH_V, DEPTH_H = 6, 8
OPP = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
THR = float(os.environ.get('THR', 30))
def strip_cells(w, h, d, off, nw, nh):
    """cellules de la carte (w,h) visibles depuis la voisine placee a `d` avec decalage `off`"""
    out = []
    if d in ('up', 'down'):
        ys = range(0, min(h, DEPTH_V)) if d == 'up' else range(max(0, h - DEPTH_V), h)
        for y in ys:
            for x in range(w):
                if -DEPTH_H <= x - off < nw + DEPTH_H: out.append((x, y))
    else:
        xs = range(0, min(w, DEPTH_H)) if d == 'left' else range(max(0, w - DEPTH_H), w)
        for x in xs:
            for y in range(h):
                if -DEPTH_V <= y - off < nh + DEPTH_V: out.append((x, y))
    return out
def fix_pair(a, b, d, off, apply, report):
    """a possede la connexion (d, off) vers b. Corrige la bande de a vue depuis b et la bande de b vue depuis a."""
    changed = 0
    for (m, n, dd, oo) in ((a, b, d, off), (b, a, OPP[d], -off)):
        la, ma = load(m); lb, _ = load(n)
        # la bande de m est du cote `dd` de m ; la carte courante est n
        cells = strip_cells(la['width'], la['height'], dd, oo, lb['width'], lb['height'])
        pm = (la['primary_tileset'], la['secondary_tileset']); pn = (lb['primary_tileset'], lb['secondary_tileset'])
        if pm == pn: continue
        cand = {}
        for (x, y) in cells:
            i = y * la['width'] + x; u = ma[i] & 0x3ff
            ru = render(*pm, u); bad = dist(ru, render(*pn, u))
            if bad <= THR: continue
            if u not in cand:
                au = attr(*pm, u); best = None
                for v in range(0, 640 + len(tileset(pm[1])[2])):
                    if attr(*pm, v) != au: continue
                    rn = render(*pn, v); rm = render(*pm, v)
                    if rn is None or rm is None: continue
                    s = dist(rm, ru) * 0.5 + dist(rn, ru)
                    if best is None or s < best[0]: best = (s, v)
                cand[u] = best
            best = cand[u]
            if best and best[0] < bad - 2:
                ma[i] = (ma[i] & ~0x3ff) | best[1]; changed += 1
            report.append((m, n, x, y, u, round(bad, 1), best))
        if apply and changed: open(la['blockdata_filepath'], 'wb').write(struct.pack('<%dH' % len(ma), *ma))
    return changed
if __name__ == '__main__':
    apply = '--apply' in sys.argv; only = [x for x in sys.argv[1:] if not x.startswith('--')]
    seen = set(); tot = 0
    for a, dd in MAPS.items():
        for c in dd.get('connections') or []:
            b = ID.get(c['map'])
            if not b or tuple(sorted((a, b))) in seen: continue
            seen.add(tuple(sorted((a, b))))
            if only and not (a in only and b in only): continue
            rep = []; ch = fix_pair(a, b, c['direction'], c['offset'], apply, rep)
            nbad = len(rep); un = sum(1 for r in rep if not (r[6] and r[6][0] < r[5] - 2))
            print('%-26s %-26s mauvaises=%3d corrigees=%3d irreparables=%3d' % (a, b, nbad, ch, un)); tot += ch
    print('total corrigees', tot, '(applique)' if apply else '(simulation)')
