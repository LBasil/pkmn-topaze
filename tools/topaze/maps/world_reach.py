#!/usr/bin/env python3
"""Accessibilité GLOBALE : graphe (carte, zone marchable) relié par les connexions et les warps, depuis la chambre du joueur.
L'eau compte comme marchable (Surf), les arbres/rochers (objets) sont ignorés : on cherche les zones COUPÉES du monde (mur total).
Usage : python3 tools/topaze/maps/world_reach.py <racine_depot> [out.json]"""
import json, os, struct, sys
from collections import deque, defaultdict
sys.argv_root = sys.argv[1] if len(sys.argv) > 1 else '.'
sys.argv = [sys.argv[0], sys.argv_root] + sys.argv[2:]
import importlib.util
spec = importlib.util.spec_from_file_location('audit', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit.py'))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
DIRS = A.DIRS

def maps_walk(m, surf=True):
    lay = A.LAYOUTS.get(m['layout'])
    if not lay: return None
    w, h = lay['width'], lay['height']
    p = os.path.join(A.ROOT, lay['blockdata_filepath'])
    if not os.path.exists(p): return None
    g = struct.unpack('<%dH' % (w * h), open(p, 'rb').read())
    walk = set()
    for y in range(h):
        for x in range(w):
            v = g[y * w + x]
            b = A.behaviour(lay, v & 0x3FF)
            if b in A.WATER and surf: walk.add((x, y)); continue
            if b in A.WATER: continue
            if (v >> 10) & 3 == 0: walk.add((x, y))
    return w, h, walk

def main():
    maps = A.MAPS
    info = {}
    for mid, m in maps.items():
        r = maps_walk(m)
        if not r: continue
        w, h, walk = r
        comp = {}; n = 0
        for c in walk:
            if c in comp: continue
            d = A.bfs([c], walk, w, h)
            for k in d: comp[k] = n
            n += 1
        info[mid] = (w, h, walk, comp)
    def comps_at(mid, x, y):
        w, h, walk, comp = info[mid]
        if (x, y) in comp: return {comp[(x, y)]}
        return {comp[(x + dx, y + dy)] for dx, dy in DIRS if (x + dx, y + dy) in comp}
    adj = defaultdict(set)
    for mid, m in maps.items():
        if mid not in info: continue
        for cn in (m.get('connections') or []):
            b = cn['map']
            if b not in info: continue
            off = cn['offset']; d = cn['direction']
            wa, ha, wk, cm = info[mid]; wb, hb, wkb, cmb = info[b]
            pairs = []
            if d == 'up': pairs = [((x, 0), (x - off, hb - 1)) for x in range(wa)]
            elif d == 'down': pairs = [((x, ha - 1), (x - off, 0)) for x in range(wa)]
            elif d == 'left': pairs = [((0, y), (wb - 1, y - off)) for y in range(ha)]
            elif d == 'right': pairs = [((wa - 1, y), (0, y - off)) for y in range(ha)]
            for pa, pb in pairs:
                if pa in cm and pb in cmb:
                    adj[(mid, cm[pa])].add((b, cmb[pb])); adj[(b, cmb[pb])].add((mid, cm[pa]))
        for wp in (m.get('warp_events') or []):
            dm = wp['dest_map']
            if dm not in maps or dm not in info: continue
            try: di = int(wp['dest_warp_id'])
            except Exception: continue
            dws = maps[dm].get('warp_events') or []
            if not (0 <= di < len(dws)): continue
            dw = dws[di]
            for ca in comps_at(mid, wp['x'], wp['y']):
                for cb in comps_at(dm, dw['x'], dw['y']):
                    adj[(mid, ca)].add((dm, cb))     # trajet aller (le retour existe via le warp inverse)
    start_m = 'MAP_PALLET_TOWN_PLAYERS_HOUSE_2F'
    seeds = {(start_m, c) for c in comps_at(start_m, 6, 6)}
    seen = set(seeds); q = deque(seeds)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen: seen.add(v); q.append(v)
    out = {'reached_comps': len(seen), 'cut_off': []}
    for mid, m in maps.items():
        if mid not in info: continue
        w, h, walk, comp = info[mid]
        ncomp = (max(comp.values()) + 1) if comp else 0
        for c in range(ncomp):
            if (mid, c) in seen: continue
            cells = [k for k, v in comp.items() if v == c]
            ev = []
            for wp in (m.get('warp_events') or []):
                if c in comps_at(mid, wp['x'], wp['y']): ev.append(('warp', wp['x'], wp['y'], wp['dest_map'].replace('MAP_', '')))
            for o in (m.get('object_events') or []):
                if c in comps_at(mid, o['x'], o['y']): ev.append(('obj', o['x'], o['y'], o['graphics_id'].replace('OBJ_EVENT_GFX_', '')))
            for s in (m.get('bg_events') or []):
                if c in comps_at(mid, s['x'], s['y']): ev.append(('bg', s['x'], s['y'], s.get('script', s.get('item', ''))))
            if ev: out['cut_off'].append({'map': mid, 'cells': len(cells), 'events': ev[:8], 'n_events': len(ev)})
    return out

if __name__ == '__main__':
    r = main()
    json.dump(r, open(sys.argv[2] if len(sys.argv) > 2 else '/dev/stdout', 'w'), indent=1)
