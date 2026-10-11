# ROUTE 15 <-> ROUTE 14 : tilesets differents -> plus de connexion, pas simples sur les cases communes (Route15 x=71, y ; Route14 x=0, y+40).
# Ordre : route15_dress -> route15_events. Idempotent.
import json, struct
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
def grid(n, w, h): return struct.unpack('<%dH' % (w * h), open('data/layouts/%s/map.bin' % n, 'rb').read())
g15, g14 = grid('Route15', 72, 20), grid('Route14', 24, 60)
ok = lambda g, w, x, y: (g[y * w + x] & 0xc00) == 0
YS = [y for y in range(20) if ok(g15, 72, 71, y) and ok(g14, 24, 0, y + 40)]
assert len(YS) >= 6, YS
a = json.load(open('data/maps/Route15/map.json')); b = json.load(open('data/maps/Route14/map.json'))
a['connections'] = [c for c in a['connections'] if c['map'] != 'MAP_ROUTE14']; b['connections'] = [c for c in b['connections'] if c['map'] != 'MAP_ROUTE15']
ka = [w for w in a['warp_events'] if w['dest_map'] != 'MAP_ROUTE14']; kb = [w for w in b['warp_events'] if w['dest_map'] != 'MAP_ROUTE15']
a['warp_events'] = ka + [warp(71, y, 'MAP_ROUTE14', len(kb) + i) for i, y in enumerate(YS)]
b['warp_events'] = kb + [warp(0, y + 40, 'MAP_ROUTE15', len(ka) + i) for i, y in enumerate(YS)]
jdump(a, 'data/maps/Route15/map.json'); jdump(b, 'data/maps/Route14/map.json')
f = 'src/field_control_avatar.c'; t = open(f).read()
if 'LAYOUT_ROUTE14' not in t:
    t = t.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE17;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE17 || gMapHeader.mapLayoutId == LAYOUT_ROUTE14;', 1); open(f, 'w').write(t)
print('Route 15 <-> 14 : %d warps' % len(YS), YS)
