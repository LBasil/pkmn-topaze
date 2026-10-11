# ROUTE 18 <-> ROUTE 17 : tilesets differents (Route 18 a ses propres tilesets amethyste) -> plus de connexion, pas simples sur les cases communes (Route18 y=0 ; Route17 y=159).
# Ordre : route18_dress -> route18_events. Idempotent.
import json, struct
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
def grid(n, w, h): return struct.unpack('<%dH' % (w * h), open('data/layouts/%s/map.bin' % n, 'rb').read())
g18, g17 = grid('Route18', 60, 20), grid('Route17', 24, 160)
ok = lambda g, w, x, y: (g[y * w + x] & 0xc00) == 0
XS = [x for x in range(24) if ok(g18, 60, x, 0) and ok(g17, 24, x, 159)]
assert len(XS) >= 8, XS
a = json.load(open('data/maps/Route18/map.json')); b = json.load(open('data/maps/Route17/map.json'))
a['connections'] = [c for c in a['connections'] if c['map'] != 'MAP_ROUTE17']; b['connections'] = [c for c in b['connections'] if c['map'] != 'MAP_ROUTE18']
ka = [w for w in a['warp_events'] if w['dest_map'] != 'MAP_ROUTE17']; kb = [w for w in b['warp_events'] if w['dest_map'] != 'MAP_ROUTE18']
a['warp_events'] = ka + [warp(x, 0, 'MAP_ROUTE17', len(kb) + i) for i, x in enumerate(XS)]
b['warp_events'] = kb + [warp(x, 159, 'MAP_ROUTE18', len(ka) + i) for i, x in enumerate(XS)]
jdump(a, 'data/maps/Route18/map.json'); jdump(b, 'data/maps/Route17/map.json')
f = 'src/field_control_avatar.c'; t = open(f).read()
if 'LAYOUT_ROUTE17' not in t:
    t = t.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE19;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE19 || gMapHeader.mapLayoutId == LAYOUT_ROUTE17;', 1); open(f, 'w').write(t)
print('Route 18 <-> 17 : %d warps' % len(XS), XS)
