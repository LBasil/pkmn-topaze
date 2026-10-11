# ROUTE 20 <-> ROUTE 19 : tilesets differents -> plus de connexion, pas simples sur les cases d'eau communes (Route20 x=119, y ; Route19 x=0, y+40).
# Ordre : route20_dress -> route20_events -> chrondrolia_events (recalcule les ids des warps Route 20 <-> Chrondrolia). Idempotent.
import json, struct
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
def grid(n, w, h): return struct.unpack('<%dH' % (w * h), open('data/layouts/%s/map.bin' % n, 'rb').read())
g20, g19 = grid('Route20', 120, 20), grid('Route19', 24, 60)
ok = lambda g, w, x, y: (g[y * w + x] & 0xc00) == 0
YS = [y for y in range(20) if ok(g20, 120, 119, y) and ok(g19, 24, 0, y + 40)]
assert len(YS) >= 8, YS
a = json.load(open('data/maps/Route20/map.json')); b = json.load(open('data/maps/Route19/map.json'))
a['connections'] = [c for c in a['connections'] if c['map'] != 'MAP_ROUTE19']; b['connections'] = [c for c in b['connections'] if c['map'] != 'MAP_ROUTE20']
ka = [w for w in a['warp_events'] if w['dest_map'] not in ('MAP_ROUTE19', 'MAP_CINNABAR_ISLAND')]
cin = [w for w in a['warp_events'] if w['dest_map'] == 'MAP_CINNABAR_ISLAND']
kb = [w for w in b['warp_events'] if w['dest_map'] != 'MAP_ROUTE20']
a['warp_events'] = ka + [warp(119, y, 'MAP_ROUTE19', len(kb) + i) for i, y in enumerate(YS)] + cin
b['warp_events'] = kb + [warp(0, y + 40, 'MAP_ROUTE20', len(ka) + i) for i, y in enumerate(YS)]
jdump(a, 'data/maps/Route20/map.json'); jdump(b, 'data/maps/Route19/map.json')
f = 'src/field_control_avatar.c'; t = open(f).read()
if 'LAYOUT_ROUTE19' not in t:
    t = t.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE20;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE20 || gMapHeader.mapLayoutId == LAYOUT_ROUTE19;', 1); open(f, 'w').write(t)
print('Route 20 <-> 19 : %d warps' % len(YS), YS)
