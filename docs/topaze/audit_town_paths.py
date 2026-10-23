#!/usr/bin/env python3
"""Audit : dans chaque ville/route, toutes les portes (warps) sont-elles reliees a la zone d'arrivee (bords de carte, points de vol) ?
Surf / Coupe / Force ne sont pas comptes (cases d'eau bloquees) : un signalement = porte isolee SANS ces capacites."""
import sys, glob, json, collections
sys.path[:0] = ['/tmp/gx', 'docs/topaze', 'tools/topaze/maps']
import route_test as R
V = [(0,-1),(0,1),(-1,0),(1,0)]
H = {e['map']: (e['x'], e['y']) for e in json.load(open('src/data/heal_locations.json'))['heal_locations']}
tot = 0
for f in sorted(glob.glob('data/maps/*/map.json')):
    n = f.split('/')[2]; j = json.load(open(f))
    if j.get('map_type') not in ('MAP_TYPE_TOWN', 'MAP_TYPE_CITY', 'MAP_TYPE_ROUTE'): continue
    try: nv = R.Nav(n)
    except Exception: continue
    nv.objs = set()
    src = []
    for x in range(nv.w):
        for y in (0, nv.h - 1):
            if not nv.blocked(x, y): src.append((x, y))
    for y in range(nv.h):
        for x in (0, nv.w - 1):
            if not nv.blocked(x, y): src.append((x, y))
    if j['id'] in H and not nv.blocked(*H[j['id']]): src.append(H[j['id']])
    seen = set(src); q = collections.deque(src)
    while q:
        c = q.popleft()
        for dx, dy in V:
            m = (c[0]+dx, c[1]+dy)
            if m in seen or not (0 <= m[0] < nv.w and 0 <= m[1] < nv.h): continue
            if nv.blocked(*m) or not nv.step_ok(c, m): continue
            seen.add(m); q.append(m)
    for w in j['warp_events']:
        door = (w['x'], w['y'])
        ok = door in seen or any((door[0]+dx, door[1]+dy) in seen for dx, dy in V)
        if not ok:
            print(n, 'PORTE ISOLEE', door, '->', w['dest_map']); tot += 1
print(tot, 'portes isolees')
