#!/usr/bin/env python3
"""Audit : objets (items, PNJ, dresseurs) dont les cases voisines sont inaccessibles depuis les sorties de la carte (loot enferme)."""
import sys, glob, json, collections
sys.path[:0] = ['/tmp/gx', 'docs/topaze', 'tools/topaze/maps']
import route_test as R
V = [(0,-1),(0,1),(-1,0),(1,0)]
exec(open('docs/topaze/audit_global.py').read().split('MAPS = {}')[0].split('V = ')[0])
tot = 0
for f in sorted(glob.glob('data/maps/*/map.json')):
    n = f.split('/')[2]
    try: nv = R.Nav(n)
    except Exception: continue
    j = json.load(open(f)); nv.objs = set()
    pts = []
    for w in j['warp_events']:
        for c in [(w['x'], w['y']+1), (w['x'], w['y']-1), (w['x']-1, w['y']), (w['x']+1, w['y'])]:
            if 0 <= c[0] < nv.w and 0 <= c[1] < nv.h and not nv.blocked(*c): pts.append(c); break
    for x in range(nv.w):
        for y in (0, nv.h-1):
            if not nv.blocked(x, y): pts.append((x, y))
    for y in range(nv.h):
        for x in (0, nv.w-1):
            if not nv.blocked(x, y): pts.append((x, y))
    if not pts: continue
    # BFS multi-source en une seule composante "atteignable"
    seen = set(pts); q = collections.deque(pts)
    while q:
        c = q.popleft()
        for dx, dy in V:
            m = (c[0]+dx, c[1]+dy)
            if m in seen or not (0 <= m[0] < nv.w and 0 <= m[1] < nv.h): continue
            if nv.blocked(*m) or not nv.step_ok(c, m): continue
            seen.add(m); q.append(m)
    for o in j['object_events']:
        c = (o['x'], o['y'])
        if not (0 <= c[0] < nv.w and 0 <= c[1] < nv.h): continue
        if any((c[0]+dx, c[1]+dy) in seen or c in seen for dx, dy in V): continue
        gfx = o['graphics_id'][14:]
        if gfx in ('SEAGALLOP',) or 'WATER' in gfx: continue
        print(n, 'INACCESSIBLE', c, gfx, o.get('script', '?').split('EventScript_')[-1], o.get('flag')); tot += 1
print(tot, 'objets inaccessibles')
