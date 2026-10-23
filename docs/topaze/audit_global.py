#!/usr/bin/env python3
"""Audit global des cartes : (1) sorties separees (objets ignores vs comptes) (2) poches inaccessibles avec objet/item
(3) raccords de bord de carte (praticable d'un cote, bloque de l'autre). Usage depuis la racine du depot."""
import sys, glob, json, collections, os
sys.path[:0] = ['/tmp/gx', 'docs/topaze', 'tools/topaze/maps']
import route_test as R
V = [(0,-1),(0,1),(-1,0),(1,0)]
def comps(nav, starts, ignore_objs):
    saved = nav.objs
    if ignore_objs: nav.objs = set()
    seen = {}; cid = 0
    for s in starts:
        if s in seen or not (0 <= s[0] < nav.w and 0 <= s[1] < nav.h): continue
        if nav.blocked(*s): continue
        cid += 1; seen[s] = cid; q = collections.deque([s])
        while q:
            c = q.popleft()
            for dx, dy in V:
                n = (c[0]+dx, c[1]+dy)
                if n in seen or not (0 <= n[0] < nav.w and 0 <= n[1] < nav.h): continue
                if nav.blocked(*n) or not nav.step_ok(c, n): continue
                seen[n] = cid; q.append(n)
    nav.objs = saved
    return seen
MAPS = {}
for f in sorted(glob.glob('data/maps/*/map.json')):
    n = f.split('/')[2]
    try: MAPS[n] = (R.Nav(n), json.load(open(f)))
    except Exception: pass
ID2N = {j['id']: n for n, (nav, j) in MAPS.items()}
out = []
def say(s): out.append(s)
# (3) raccords
for n, (nav, j) in MAPS.items():
    for c in j.get('connections') or []:
        m = ID2N.get(c['map'])
        if not m or c['direction'] not in ('up','down','left','right'): continue
        nav2 = MAPS[m][0]; d = c['direction']; off = c['offset']; bad = []
        if d in ('up','down'):
            y1 = 0 if d == 'up' else nav.h-1; y2 = nav2.h-1 if d == 'up' else 0
            for x in range(nav.w):
                x2 = x - off
                if 0 <= x2 < nav2.w:
                    a = not nav.blocked(x,y1); b = not nav2.blocked(x2,y2)
                    if a != b: bad.append((x, 'A' if a else 'B'))
        else:
            x1 = 0 if d == 'left' else nav.w-1; x2_ = nav2.w-1 if d == 'left' else 0
            for y in range(nav.h):
                y2 = y - off
                if 0 <= y2 < nav2.h:
                    a = not nav.blocked(x1,y); b = not nav2.blocked(x2_,y2)
                    if a != b: bad.append((y, 'A' if a else 'B'))
        if bad and n < m: say(f'RACCORD {n} <-> {m} ({d}, off {off}) : {len(bad)} cases desaccordees ; premieres {bad[:8]}')
# (1) sorties
for n, (nav, j) in MAPS.items():
    exits = {}
    for w in j['warp_events']: exits[(w['x'], w['y'])] = 'warp>' + w['dest_map'][4:]
    for c in j.get('connections') or []:
        m = ID2N.get(c['map'])
        if not m or c['direction'] not in ('up','down','left','right'): continue
        nav2 = MAPS[m][0]; d = c['direction']; off = c['offset']
        rng = range(nav.w) if d in ('up','down') else range(nav.h)
        for i in rng:
            if d == 'up': c1, c2 = (i, 0), (i-off, nav2.h-1)
            elif d == 'down': c1, c2 = (i, nav.h-1), (i-off, 0)
            elif d == 'left': c1, c2 = (0, i), (nav2.w-1, i-off)
            else: c1, c2 = (nav.w-1, i), (0, i-off)
            if 0 <= c2[0] < nav2.w and 0 <= c2[1] < nav2.h and not nav.blocked(*c1) and not nav2.blocked(*c2):
                exits.setdefault(c1, 'conn>' + m)
    if len(exits) < 2: continue
    # une sortie = un point d'entree ; pour les warps on part de la case devant (non bloquee)
    starts = {}
    for (x, y), lab in exits.items():
        cand = [(x, y+1), (x, y-1), (x-1, y), (x+1, y), (x, y)] if lab.startswith('warp') else [(x, y)]
        s = next((c for c in cand if 0 <= c[0] < nav.w and 0 <= c[1] < nav.h and not nav.blocked(*c)), None)
        starts[(x, y)] = s
    for ign in (True, False):
        pts = [p for p in starts.values() if p]
        cm = comps(nav, pts, ign)
        g = collections.defaultdict(set)
        for (x, y), lab in exits.items():
            s = starts[(x, y)]
            g[cm.get(s, 0)].add(lab.split('>')[0] + '>' + lab.split('>')[1])
        if len(g) > 1:
            tag = 'SORTIES SEPAREES (objets ignores)' if ign else 'SORTIES SEPAREES (avec PNJ/objets)'
            say(f'{tag} {n} : ' + ' | '.join(f'[{k}] ' + ','.join(sorted(v)[:5]) + ('...' if len(v) > 5 else '') for k, v in g.items()))
            if ign: break
open('/tmp/gx/audit_global.txt', 'w').write('\n'.join(out))
print(len(MAPS), 'cartes,', len(out), 'lignes')
