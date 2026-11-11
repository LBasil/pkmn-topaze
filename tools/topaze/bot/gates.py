#!/usr/bin/env python3
"""Planificateur d'obstacles a CS pour l'autopilote : rochers (Eclate-Roc) et rochers Force (Force).

`plan(nav, start, goal, boulders, rocks)` : recherche en largeur sur l'etat (case du joueur, positions des rochers Force) ; un pas vers un rocher Force le
pousse d'une case si la case derriere est libre (comme le moteur : pas de mur, pas d'objet, pas de warp, meme regle d'altitude). Les rochers a
briser sont traites comme des murs tant qu'on peut faire sans ; sinon (`allow_rocks=True`) comme des cases franchissables et la liste de ceux
qu'il faut briser (cases visitees) est renvoyee. Renvoie (liste de ('move'|'push'|'smash', direction, case), rochers_a_briser) ou None.
Python pur, testable hors emulateur : `python3 gates.py MtEmber_Exterior 39 19 29 7`.
"""
import sys, os, collections
D4 = (('UP', (0, -1)), ('DOWN', (0, 1)), ('LEFT', (-1, 0)), ('RIGHT', (1, 0)))

def plan(nav, start, goal, boulders, rocks=(), allow_rocks=False, limit=400000):
    boulders = frozenset(boulders); rocks = frozenset(rocks)
    base = set(nav.objs) - boulders - rocks            # autres objets (dresseurs, PNJ) : murs
    saved = nav.objs; nav.objs = set()                  # les murs d'objets sont geres ici (base / boulders / rocks)
    try: return _plan(nav, start, goal, boulders, rocks, base, allow_rocks, limit)
    finally: nav.objs = saved

def _plan(nav, start, goal, boulders, rocks, base, allow_rocks, limit):

    def free(c, bs):
        return not nav.blocked(*c) and c not in base and c not in bs and (allow_rocks or c not in rocks) and (c not in nav.warps or c == goal)
    s0 = (start, boulders); prev = {s0: None}; q = collections.deque([s0]); n = 0; end = None
    while q:
        st = q.popleft(); c, bs = st
        if c == goal: end = st; break
        n += 1
        if n > limit: return None
        for d, (dx, dy) in D4:
            m = (c[0] + dx, c[1] + dy)
            if not (0 <= m[0] < nav.w and 0 <= m[1] < nav.h) or not nav.step_ok(c, m): continue
            if m in bs:                                  # poussee
                b2 = (m[0] + dx, m[1] + dy)
                if not (0 <= b2[0] < nav.w and 0 <= b2[1] < nav.h) or not nav.step_ok(m, b2) or b2 in rocks or b2 in base or b2 in bs or b2 in nav.warps or nav.blocked(*b2): continue
                ns = (m, (bs - {m}) | {b2}); act = ('push', d, m)
            elif free(m, bs): ns = (m, bs); act = ('move', d, m)
            else: continue
            if ns in prev: continue
            prev[ns] = (st, act); q.append(ns)
    if end is None: return None
    out = []; st = end
    while prev[st]: p, a = prev[st]; out.append(a); st = p
    out.reverse()
    smash = [a[2] for a in out if a[2] in rocks]
    return out, smash

def nav_static(name):
    sys.path.insert(0, '/tmp/gx'); sys.path.insert(0, 'docs/topaze')
    import route_test as R
    return R.Nav(name)

def objs_of(mj, gfx):
    return [(o['x'], o['y']) for o in mj['object_events'] if gfx in o['graphics_id'] and 'ITEM' not in o['graphics_id']]

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
    name = sys.argv[1]; a = tuple(map(int, sys.argv[2:4])); b = tuple(map(int, sys.argv[4:6]))
    nav = nav_static(name); bo = objs_of(nav.mj, 'PUSHABLE_BOULDER'); ro = objs_of(nav.mj, 'ROCK_SMASH')
    r = plan(nav, a, b, bo, ro) or plan(nav, a, b, bo, ro, allow_rocks=True)
    if not r: print('PAS DE SOLUTION', 'boulders', bo, 'rocks', ro)
    else: print(len(r[0]), 'pas ; pousses :', sum(1 for x in r[0] if x[0] == 'push'), '; rochers a briser :', r[1])
