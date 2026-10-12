# ROUTE 14 <-> ROUTE 13 : tilesets differents -> plus de connexion, pas simples sur les cases communes (Route14 x=23, Route13 x=0, memes y).
# Ordre : route14_v2 -> route15_events -> route14_events. Idempotent.
import json, struct
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
def grid(n, w, h): return struct.unpack('<%dH' % (w * h), open('data/layouts/%s/map.bin' % n, 'rb').read())
g14, g13 = grid('Route14', 24, 60), grid('Route13', 72, 20)
ok = lambda g, w, x, y: (g[y * w + x] & 0xc00) == 0
YS = [y for y in range(20) if ok(g14, 24, 23, y) and ok(g13, 72, 0, y)]
assert len(YS) >= 3, YS
a = json.load(open('data/maps/Route14/map.json')); b = json.load(open('data/maps/Route13/map.json'))
a['connections'] = [c for c in a['connections'] if c['map'] != 'MAP_ROUTE13']; b['connections'] = [c for c in b['connections'] if c['map'] != 'MAP_ROUTE14']
ka = [w for w in a['warp_events'] if w['dest_map'] != 'MAP_ROUTE13']; kb = [w for w in b['warp_events'] if w['dest_map'] != 'MAP_ROUTE14']
a['warp_events'] = ka + [warp(23, y, 'MAP_ROUTE13', len(kb) + i) for i, y in enumerate(YS)]
b['warp_events'] = kb + [warp(0, y, 'MAP_ROUTE14', len(ka) + i) for i, y in enumerate(YS)]
jdump(a, 'data/maps/Route14/map.json'); jdump(b, 'data/maps/Route13/map.json')
print('Route 14 <-> 13 : %d warps' % len(YS), YS)
