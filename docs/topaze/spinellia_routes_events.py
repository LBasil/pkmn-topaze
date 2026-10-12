# ROUTES 10 / 12 <-> voisines (Routes 9, 11, 13) : les routes de Spinellia ont maintenant d'autres tilesets que leurs voisines -> plus de connexions, pas simples sur les cases
# communes (meme methode que route15_events.py). Route 8 garde sa connexion (interieur Saffron, jamais emprunte) et ses warps vers Spinellia.
#   Route 9 (72x20)  x=71, y 0..19      <-> Route 10 (24x80)  x=0, y 0..19                 (offset 0)
#   Route 11 (72x20) x=71, y 0..19      <-> Route 12 (24x120) x=0, y 60..79                (offset -60)
#   Route 13 (72x20) y=0,  x 48..71     <-> Route 12 (24x120) y=119, x 0..23               (offset 48)
# Ordre : spinellia_town -> spinellia_routes -> spinellia_routes_events. Idempotent (retire d'abord tous les warps de jonction).
import json, struct
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
SIZE = {'Route9': (72, 20), 'Route10': (24, 80), 'Route11': (72, 20), 'Route12': (24, 120), 'Route13': (72, 20)}
def grid(n): w, h = SIZE[n]; return struct.unpack('<%dH' % (w * h), open('data/layouts/%s/map.bin' % n, 'rb').read())
G = {n: grid(n) for n in SIZE}
ok = lambda n, x, y: (G[n][y * SIZE[n][0] + x] & 0xc00) == 0
M = {n: json.load(open('data/maps/%s/map.json' % n)) for n in SIZE}
MAPID = {n: 'MAP_' + n.upper() for n in SIZE}
LINKS = [('Route9', 'Route10', [((71, y), (0, y)) for y in range(20)]),
         ('Route11', 'Route12', [((71, y), (0, y + 60)) for y in range(20)]),
         ('Route13', 'Route12', [((x + 48, 0), (x, 119)) for x in range(24)])]
for n in M:      # on repart de zero : plus aucun warp de jonction, plus aucune connexion entre ces routes
    partners = {MAPID[b] for a, b, _ in LINKS if a == n} | {MAPID[a] for a, b, _ in LINKS if b == n}
    M[n]['warp_events'] = [w for w in M[n]['warp_events'] if w['dest_map'] not in partners]
    M[n]['connections'] = [c for c in (M[n].get('connections') or []) if c['map'] not in partners]
for a, b, pairs in LINKS:
    pairs = [(pa, pb) for pa, pb in pairs if ok(a, *pa) and ok(b, *pb)]
    assert len(pairs) >= 2, (a, b, len(pairs))
    na, nb = len(M[a]['warp_events']), len(M[b]['warp_events'])
    M[a]['warp_events'] += [warp(pa[0], pa[1], MAPID[b], nb + i) for i, (pa, pb) in enumerate(pairs)]
    M[b]['warp_events'] += [warp(pb[0], pb[1], MAPID[a], na + i) for i, (pa, pb) in enumerate(pairs)]
    print('%s <-> %s : %d warps' % (a, b, len(pairs)))
for n in M: jdump(M[n], 'data/maps/%s/map.json' % n)
f = 'src/field_control_avatar.c'; t = open(f).read()
if 'LAYOUT_ROUTE13' not in t:
    t = t.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE11;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE11 || gMapHeader.mapLayoutId == LAYOUT_ROUTE13;', 1); open(f, 'w').write(t)
