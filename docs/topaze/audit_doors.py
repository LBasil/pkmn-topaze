# Audit : tuiles « porte » (comportement MB_WARP_DOOR / MB_NON_ANIMATED_DOOR / MB_ANIMATED_DOOR) sans warp ni panneau sur la case (lancer a la racine).
import sys, glob, json, collections
sys.path[:0] = ['/tmp/gx', 'docs/topaze', 'tools/topaze/maps']
import route_test as R
DOORS = {0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x60}
res = collections.OrderedDict(); tot = 0
for d in sorted(glob.glob('data/maps/*/map.json')):
    name = d.split('/')[2]
    try: nav = R.Nav(name)
    except Exception: continue
    mj = nav.mj
    if mj.get('map_type') not in ('MAP_TYPE_TOWN', 'MAP_TYPE_CITY', 'MAP_TYPE_ROUTE'): continue
    signs = {(b['x'], b['y']) for b in mj.get('bg_events', [])}
    miss = []
    for y in range(nav.h):
        for x in range(nav.w):
            if (nav.attr(x, y) & 0x1ff) in DOORS and (x, y) not in nav.warps and (x, y) not in signs: miss.append((x, y))
    if miss: res[name] = miss; tot += len(miss)
for k, v in res.items(): print(k, len(v), v)
print('TOTAL', tot, 'maps', len(res))
