# ROUTE 21 Nord <-> Sud : les deux moities ont des tilesets differents -> plus de connexion, pas simples sur les cases d'eau communes.
# A lancer apres route21_dress.py, avant chrondrolia_events.py (qui recalcule les ids de warps vers Chrondrolia). Idempotent.
import json, struct
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
W_, H_ = 24, 50
def grid(n): return struct.unpack('<%dH' % (W_ * H_), open('data/layouts/%s/map.bin' % n, 'rb').read())
gn, gs = grid('Route21_North'), grid('Route21_South')
ok = lambda g, x, y: (g[y * W_ + x] & 0xc00) == 0
XS = [x for x in range(W_) if ok(gn, x, H_ - 1) and ok(gs, x, 0)]
assert len(XS) >= 6, XS
n = json.load(open('data/maps/Route21_North/map.json')); s = json.load(open('data/maps/Route21_South/map.json'))
n['connections'] = [c for c in n['connections'] if c['map'] != 'MAP_ROUTE21_SOUTH']
s['connections'] = [c for c in s['connections'] if c['map'] != 'MAP_ROUTE21_NORTH']
keepn = [w for w in n['warp_events'] if w['dest_map'] != 'MAP_ROUTE21_SOUTH']; bn = len(keepn)
keeps = [w for w in s['warp_events'] if w['dest_map'] not in ('MAP_ROUTE21_NORTH', 'MAP_CINNABAR_ISLAND')]; bs = len(keeps)
n['warp_events'] = keepn + [warp(x, H_ - 1, 'MAP_ROUTE21_SOUTH', bs + i) for i, x in enumerate(XS)]
s['warp_events'] = keeps + [warp(x, 0, 'MAP_ROUTE21_NORTH', bn + i) for i, x in enumerate(XS)]
jdump(n, 'data/maps/Route21_North/map.json'); jdump(s, 'data/maps/Route21_South/map.json')
f = 'src/field_control_avatar.c'; t = open(f).read()
if 'LAYOUT_ROUTE21_NORTH' not in t:
    t = t.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE21_SOUTH', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE21_SOUTH || gMapHeader.mapLayoutId == LAYOUT_ROUTE21_NORTH', 1)
    open(f, 'w').write(t)
print('Route 21 N<->S : %d warps' % len(XS), XS)
