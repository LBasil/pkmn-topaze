#!/usr/bin/env python3
"""Retours Basil 21/10 : « je ne peux pas surf sur nos eaux non animees ». Les mares/mers dessinees en tuiles statiques des routes v2 (9, 13..17)
n'avaient ni comportement d'eau ni altitude 1 : elles etaient de simples murs bleus. On detecte les metatuiles bleu-eau (couleur dominante)
dont tous les blocs sont (collision 1, altitude 0), on leur donne le comportement MB_OCEAN_WATER (attribut 0x22000415 : eau + rencontres d'eau)
et on met leurs blocs en (collision 0, altitude 1) comme l'eau d'origine. Idempotent (apres passage ils ne sont plus detectes)."""
import sys, os, struct, collections
sys.path.insert(0, 'tools/topaze/maps'); sys.path.insert(0, '/tmp/aud')
import mapkit as K
LAYOUTS = ['LAYOUT_ROUTE9', 'LAYOUT_ROUTE13', 'LAYOUT_ROUTE14', 'LAYOUT_ROUTE15', 'LAYOUT_ROUTE16', 'LAYOUT_ROUTE17']
WATER = {0x10, 0x11, 0x12, 0x13, 0x15, 0x16, 0x17, 0x50, 0x51, 0x52, 0x53, 0x14, 0x18, 0x19, 0x1a, 0x1b, 0x1c}
def is_water_art(L, mid):
    px = list(L.metatile_img(mid).convert('RGB').getdata())
    return sum(1 for r, g, b in px if b >= 190 and 120 <= g <= 215 and r < 150 and b > g + 25) / 256 >= 0.45
for lid in LAYOUTS:
    L = K.Layout(lid)
    def attr_path(mid): return os.path.join((L.prim if mid < 640 else L.sec).d, 'metatile_attributes.bin'), (mid if mid < 640 else mid - 640)
    def beh(mid):
        p, i = attr_path(mid); return struct.unpack('<I', open(p, 'rb').read()[i * 4:i * 4 + 4])[0]
    use = collections.defaultdict(collections.Counter)
    for y in range(L.h):
        for x in range(L.w):
            v = L.get(x, y); use[v & 0x3ff][(v >> 10 & 3, v >> 12)] += 1
    ids = []
    for mid, c in use.items():
        if (beh(mid) & 0x1ff) in WATER: continue
        if set(c) != {(1, 0)}: continue
        try:
            if is_water_art(L, mid): ids.append(mid)
        except Exception: pass
    for mid in ids:
        p, i = attr_path(mid); raw = bytearray(open(p, 'rb').read())
        old = struct.unpack('<I', raw[i * 4:i * 4 + 4])[0]
        raw[i * 4:i * 4 + 4] = struct.pack('<I', (old & 0x80000000) | 0x22000415)
        open(p, 'wb').write(raw)
    n = 0
    for k, v in enumerate(L.g):
        if (v & 0x3ff) in ids and (v >> 10 & 3) == 1 and (v >> 12) == 0:
            L.g[k] = (v & 0x3ff) | (1 << 12); n += 1
    if ids: L.save()
    print(lid, 'metatuiles', len(ids), 'blocs', n)
