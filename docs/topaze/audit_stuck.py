#!/usr/bin/env python3
"""Audit : une arrivee par warp tombe-t-elle dans une poche minuscule (joueur coince) ? + warps vers un id inexistant."""
import sys, glob, json, collections
sys.path[:0] = ['/tmp/gx', 'docs/topaze', 'tools/topaze/maps']
import route_test as R
V = [(0,-1),(0,1),(-1,0),(1,0)]
M = {}
for f in sorted(glob.glob('data/maps/*/map.json')):
    n = f.split('/')[2]; M[n] = json.load(open(f))
ID = {j['id']: n for n, j in M.items()}
cache = {}
def nav(n):
    if n not in cache:
        try: cache[n] = R.Nav(n); cache[n].objs = set()
        except Exception: cache[n] = None
    return cache[n]
def region(nv, s, limit=400):
    seen = {s}; q = collections.deque([s])
    while q and len(seen) < limit:
        c = q.popleft()
        for dx, dy in V:
            m = (c[0]+dx, c[1]+dy)
            if m in seen or not (0 <= m[0] < nv.w and 0 <= m[1] < nv.h): continue
            if nv.blocked(*m) or not nv.step_ok(c, m): continue
            seen.add(m); q.append(m)
    return seen
n_bad = 0
for n, j in M.items():
    for i, w in enumerate(j['warp_events']):
        d = w['dest_map']
        if d not in ID: print(n, 'warp', i, 'vers carte inconnue', d); n_bad += 1; continue
        dn = ID[d]; dj = M[dn]
        try: wi = int(w['dest_warp_id'])
        except Exception: continue
        if wi >= len(dj['warp_events']): print(n, 'warp', i, '->', dn, 'dest_warp_id', wi, 'inexistant'); n_bad += 1; continue
        t = dj['warp_events'][wi]; nv = nav(dn)
        if not nv: continue
        cand = [(t['x'], t['y']+1), (t['x'], t['y']-1), (t['x']-1, t['y']), (t['x']+1, t['y']), (t['x'], t['y'])]
        s = next((c for c in cand if 0 <= c[0] < nv.w and 0 <= c[1] < nv.h and not nv.blocked(*c)), None)
        if s is None: print(n, 'warp', i, '->', dn, f'arrivee ({t["x"]},{t["y"]}) entouree de cases bloquees'); n_bad += 1; continue
        r = region(nv, s)
        if len(r) < 6: print(n, 'warp', i, '->', dn, f'arrivee dans une poche de {len(r)} cases'); n_bad += 1
print(n_bad, 'signalements')
