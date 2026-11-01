#!/usr/bin/env python3
"""Confort de navigation des villes : distances porte-à-porte, boucle de courses, redondance des chemins (nb de routes sans case commune),
goulots (cases dont la suppression coupe un trajet clé). Usage : python3 navigability.py <racine_depot> [out.json]"""
import json, os, sys, itertools
import networkx as nx
import importlib.util
root = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/dev/stdout'
sys.argv = [sys.argv[0], root]
spec = importlib.util.spec_from_file_location('audit', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit.py'))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
import struct
CITIES = ['PALLET_TOWN', 'VIRIDIAN_CITY', 'PEWTER_CITY', 'CERULEAN_CITY', 'LAVENDER_TOWN', 'VERMILION_CITY', 'CELADON_CITY', 'FUCHSIA_CITY', 'SAFFRON_CITY', 'CINNABAR_ISLAND']
FRAMES_RUN = 8 / 60.0       # course : ~8 images par case ; marche : 16 images par case


def grid(mid):
    m = A.MAPS[mid]; lay = A.LAYOUTS[m['layout']]; w, h = lay['width'], lay['height']
    g = struct.unpack('<%dH' % (w * h), open(os.path.join(A.ROOT, lay['blockdata_filepath']), 'rb').read())
    walk = set()
    for y in range(h):
        for x in range(w):
            v = g[y * w + x]
            if A.behaviour(lay, v & 0x3FF) in A.WATER: continue
            if (v >> 10) & 3 == 0: walk.add((x, y))
    return m, w, h, walk


def analyse(mid):
    m, w, h, walk = grid(mid)
    G = nx.Graph()
    for c in walk:
        for dx, dy in A.DIRS:
            n = (c[0] + dx, c[1] + dy)
            if n in walk: G.add_edge(c, n)
    comp = max(nx.connected_components(G), key=len)
    G = G.subgraph(comp).copy()
    def door(c):
        if c in G: return c
        for dx, dy in A.DIRS:
            if (c[0] + dx, c[1] + dy) in G: return (c[0] + dx, c[1] + dy)
    pts = {}
    for i, wp in enumerate(m.get('warp_events') or []):
        dm = wp['dest_map']
        if 'ROUTE' in dm and 'ENTRANCE' not in dm: kind = 'EXIT'
        elif 'POKEMON_CENTER' in dm: kind = 'CENTER'
        elif dm.endswith('_GYM') or dm.endswith('DOJO'): kind = 'GYM'
        elif 'MART' in dm: kind = 'MART'
        else: kind = 'DOOR'
        d = door((wp['x'], wp['y']))
        if d: pts.setdefault((kind, dm), d)
    for dname, cs in {}.items(): pass
    for cn in (m.get('connections') or []):
        d = cn['direction']
        cells = {'up': [(x, 0) for x in range(w)], 'down': [(x, h - 1) for x in range(w)], 'left': [(0, y) for y in range(h)], 'right': [(w - 1, y) for y in range(h)]}[d]
        cells = [c for c in cells if c in G]
        if cells: pts[('EXIT', 'edge_' + d)] = cells[len(cells) // 2]
    names = list(pts)
    res = {'id': mid}
    # distances porte-à-porte (toutes portes de bâtiments + sorties)
    P = [pts[n] for n in names]
    dist = {p: dict(nx.single_source_shortest_path_length(G, p)) for p in set(P)}
    pair = [dist[a][b] for a, b in itertools.combinations(P, 2) if a in dist and b in dist[a]]
    res['n_points'] = len(P)
    res['mean_pair'] = round(sum(pair) / max(1, len(pair)), 1)
    res['max_pair'] = max(pair) if pair else None
    def first(kind): return [pts[n] for n in names if n[0] == kind]
    cen, gym, mart, ex = first('CENTER'), first('GYM'), first('MART'), first('EXIT')
    # boucle de courses : sortie -> Centre -> Arène -> Boutique -> Centre (aller-retour typique d'un joueur)
    def d(a, b): return dist[a][b]
    if cen and gym:
        c, g_ = cen[0], gym[0]
        loop = d(c, g_) * 2 + (d(c, mart[0]) * 2 if mart else 0)
        res['loop_center_gym_mart'] = loop
        res['center_gym'] = d(c, g_)
        if mart: res['center_mart'] = d(c, mart[0])
        if ex:
            res['exit_to_center_min'] = min(d(e, c) for e in ex)
            res['exit_to_gym_min'] = min(d(e, g_) for e in ex)
            res['exit_to_gym_max'] = max(d(e, g_) for e in ex)
    # redondance : nb de chemins sans case commune (Menger) entre paires clés ; 1 = un seul chemin, goulot
    red = {}
    def disjoint(a, b):
        if a == b: return None
        try: return len(list(nx.node_disjoint_paths(G, a, b, cutoff=3)))
        except Exception: return None
    if cen and gym: red['center-gym'] = disjoint(cen[0], gym[0])
    if cen and mart: red['center-mart'] = disjoint(cen[0], mart[0])
    for e in ex:
        if cen: red['exit-center'] = min(red.get('exit-center', 9), disjoint(e, cen[0]) or 9)
    res['disjoint_paths'] = red
    # goulots : cases dont le retrait déconnecte des points clés (points d'articulation séparant >= 2 points)
    arts = set(nx.articulation_points(G))
    sep = 0
    if arts:
        for a in arts:
            H = G.copy(); H.remove_node(a)
            comps = list(nx.connected_components(H))
            if len(comps) > 1:
                cnt = [sum(1 for p in P if p in c) for c in comps]
                if sum(1 for x in cnt if x > 0) >= 2: sep += 1
    res['chokepoints'] = sep
    # boucles : nombre cyclomatique (cycles indépendants) ramené à 100 cases
    cyc = G.number_of_edges() - G.number_of_nodes() + 1
    res['cycles_per_100'] = round(100 * cyc / max(1, G.number_of_nodes()), 1)
    return res


if __name__ == '__main__':
    out = {c: analyse('MAP_' + c) for c in CITIES}
    json.dump(out, open(OUT, 'w'), indent=1)
