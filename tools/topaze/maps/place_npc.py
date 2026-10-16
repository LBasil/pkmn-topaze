#!/usr/bin/env python3
"""Choisit une case libre pour un PNJ fixe : proche d'un warp donne, sans casser l'accessibilite de tous les warps de la carte. Usage : place_npc.py <Carte> [mot-cle de destination du warp d'ancrage]"""
import sys, os
sys.path.insert(0, 'docs/topaze'); sys.path.insert(0, 'tools/topaze/maps'); sys.path.insert(0, 'tools/topaze/emu'); sys.path.insert(0, '/tmp/gx')
import route_test as R
def reach(nav, start, extra):
    seen = {start}; q = [start]
    while q:
        c = q.pop()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            n = (c[0] + dx, c[1] + dy)
            if n in seen or n in extra or not (0 <= n[0] < nav.w and 0 <= n[1] < nav.h): continue
            if nav.blocked(*n) and n not in nav.warps: continue
            if not nav.step_ok(c, n): continue
            seen.add(n)
            if n not in nav.warps: q.append(n)
    return seen
def choose(name, key=None):
    nav = R.Nav(name); warps = list(nav.warps)
    anchor = next((w for w in warps if key and key in nav.warps[w]['dest_map']), warps[0])
    base = reach(nav, next(c for c in [(anchor[0], anchor[1] + 1), (anchor[0], anchor[1] - 1), (anchor[0] + 1, anchor[1]), (anchor[0] - 1, anchor[1])] if not nav.blocked(*c)), set())
    need = {w for w in warps if w in base}
    best = None
    for c in sorted(base, key=lambda c: abs(c[0] - anchor[0]) + abs(c[1] - anchor[1])):
        d = abs(c[0] - anchor[0]) + abs(c[1] - anchor[1])
        if d < 4 or c in nav.warps or c in nav.objs: continue
        if any(abs(c[0] - w[0]) + abs(c[1] - w[1]) < 2 for w in warps): continue
        # voisins : doit rester dans une zone ouverte (>=3 voisins libres)
        free = sum(1 for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)) if not nav.blocked(c[0] + dx, c[1] + dy))
        if free < 3: continue
        after = reach(nav, next(iter(base - {c})) if False else next(x for x in base if x != c and x not in nav.warps), {c})
        if all(w in after for w in need): best = c; break
    return anchor, best
if __name__ == '__main__':
    print(choose(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
