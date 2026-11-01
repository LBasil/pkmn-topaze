#!/usr/bin/env python3
"""Audit de cartes (extérieurs) : taille, accessibilité, déplacement, densité d'événements.
Usage : python3 tools/topaze/maps/audit.py <racine_depot> [out.json]
Lance sur le dépôt Topaze ET sur le FireRed d'origine pour comparer (mêmes noms de cartes)."""
import json, os, re, struct, sys
from collections import deque

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
WATER = {0x10, 0x11, 0x12, 0x13, 0x15, 0x19, 0x1A, 0x1B}   # eau : Surf requis (0x16 flaque / 0x17 eau peu profonde = marchables)
LEDGE = {0x38, 0x39, 0x3A, 0x3B}
GRASS = {0x02}
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load_layouts():
    d = json.load(open(os.path.join(ROOT, 'data/layouts/layouts.json')))['layouts']
    return {l['id']: l for l in d if 'id' in l}


def load_attr_paths():
    t = open(os.path.join(ROOT, 'src/data/tilesets/metatiles.h')).read()
    return {m.group(1): m.group(2) for m in re.finditer(r'gMetatileAttributes_(\w+)\[\]\s*=\s*INCBIN_U32\("([^"]+)"\)', t)}


LAYOUTS = load_layouts()
ATTR = load_attr_paths()
_acache = {}


def attrs(tsname):
    k = tsname.replace('gTileset_', '')
    if k not in _acache:
        p = os.path.join(ROOT, ATTR[k]) if k in ATTR else None
        _acache[k] = struct.unpack('<%dI' % (os.path.getsize(p) // 4), open(p, 'rb').read()) if p and os.path.exists(p) else ()
    return _acache[k]


def behaviour(lay, mid):
    a = attrs(lay['primary_tileset']) if mid < 640 else attrs(lay['secondary_tileset'])
    i = mid if mid < 640 else mid - 640
    return (a[i] & 0x1FF) if i < len(a) else 0


def load_maps():
    out = {}
    base = os.path.join(ROOT, 'data/maps')
    for n in os.listdir(base):
        f = os.path.join(base, n, 'map.json')
        if os.path.exists(f):
            m = json.load(open(f)); out[m['id']] = m
    return out


MAPS = load_maps()


def bfs(start_cells, walk, w, h):
    dist = {}
    q = deque()
    for c in start_cells:
        if c in walk: dist[c] = 0; q.append(c)
    while q:
        x, y = q.popleft()
        for dx, dy in DIRS:
            n = (x + dx, y + dy)
            if n in walk and n not in dist:
                dist[n] = dist[(x, y)] + 1; q.append(n)
    return dist


def audit(mid):
    m = MAPS[mid]
    lay = LAYOUTS.get(m['layout'])
    if not lay: return None
    w, h = lay['width'], lay['height']
    p = os.path.join(ROOT, lay['blockdata_filepath'])
    if not os.path.exists(p): return None
    g = struct.unpack('<%dH' % (w * h), open(p, 'rb').read())
    walk, water, grass, ledge = set(), set(), set(), set()
    for y in range(h):
        for x in range(w):
            v = g[y * w + x]; mid_ = v & 0x3FF; col = (v >> 10) & 3
            b = behaviour(lay, mid_)
            if b in WATER: water.add((x, y)); continue
            if col != 0: continue
            walk.add((x, y))
            if b in GRASS: grass.add((x, y))
            if b in LEDGE: ledge.add((x, y))
    # composantes
    seen, comps = set(), []
    for c in walk:
        if c in seen: continue
        d = bfs([c], walk, w, h); seen |= set(d); comps.append(set(d))
    comps.sort(key=len, reverse=True)
    # points d'entrée : bords connectés
    edges = {}
    for cn in (m.get('connections') or []):
        nm = MAPS.get(cn['map']); nl = LAYOUTS.get(nm['layout']) if nm else None
        nw, nh = (nl['width'], nl['height']) if nl else (w, h)
        off = cn['offset']; d = cn['direction']
        if d in ('up', 'down'):
            y = 0 if d == 'up' else h - 1
            cells = [(x, y) for x in range(max(0, off), min(w, off + nw))]
        elif d in ('left', 'right'):
            x = 0 if d == 'left' else w - 1
            cells = [(x, y) for y in range(max(0, off), min(h, off + nh))]
        else: continue
        edges[d] = [c for c in cells if c in walk]
    # composante principale = celle qui contient le plus de portes/bords
    pts = [(wp['x'], wp['y']) for wp in (m.get('warp_events') or [])]
    def score(cmp): return sum(1 for q in pts if q in cmp) + sum(len(e) > 0 and any(c in cmp for c in e) for e in edges.values()) * 3
    main = max(comps, key=lambda c: (score(c), len(c))) if comps else set()
    def adj_main(q):
        x, y = q
        return q in main or any((x + dx, y + dy) in main for dx, dy in DIRS)
    unreach_warps = [(wp['x'], wp['y'], wp['dest_map']) for wp in (m.get('warp_events') or []) if not adj_main((wp['x'], wp['y']))]
    unreach_edges = [d for d, cs in edges.items() if not any(c in main for c in cs)]
    objs = (m.get('object_events') or []); sg = (m.get('bg_events') or [])
    unreach_objs = [(o['x'], o['y'], o['graphics_id'].replace('OBJ_EVENT_GFX_', '')) for o in objs if not adj_main((o['x'], o['y']))]
    unreach_signs = [(s['x'], s['y'], s.get('script', '')) for s in sg if s['type'] == 'sign' and not adj_main((s['x'], s['y']))]
    trainers = sum(1 for o in objs if o.get('trainer_type') not in (None, 'TRAINER_TYPE_NONE'))
    # forme du terrain
    corr = dead = 0
    for (x, y) in main:
        nb = sum(((x + dx, y + dy) in walk) for dx, dy in DIRS)
        if nb <= 1 and (x, y) not in pts: dead += 1
        lr = ((x - 1, y) not in walk) and ((x + 1, y) not in walk)
        ud = ((x, y - 1) not in walk) and ((x, y + 1) not in walk)
        if (lr or ud) and nb >= 2: corr += 1
    open3 = sum(all((x + dx, y + dy) in walk for dx in (-1, 0, 1) for dy in (-1, 0, 1)) for (x, y) in main)
    # distances
    bld = {}
    for wp in (m.get('warp_events') or []):
        dm = wp['dest_map']
        key = ('CENTER' if 'POKEMON_CENTER' in dm else 'GYM' if dm.endswith('_GYM') or 'GYM' in dm.split('_')[-2:] else 'MART' if 'MART' in dm else dm.replace('MAP_', ''))
        bld.setdefault(key, []).append((wp['x'], wp['y']))
    def door_cell(c):
        x, y = c
        if c in main: return c
        for dx, dy in DIRS:
            if (x + dx, y + dy) in main: return (x + dx, y + dy)
        return None
    res = {'id': mid, 'layout': m['layout'], 'w': w, 'h': h, 'area': w * h,
           'screens': round(w / 15 * h / 10, 1), 'walk': len(walk), 'walk_pct': round(100 * len(walk) / (w * h), 1),
           'water_pct': round(100 * len(water) / (w * h), 1), 'grass': len(grass), 'ledges': len(ledge),
           'comps': [len(c) for c in comps[:5]], 'main': len(main), 'isolated': len(walk) - len(main),
           'corridor_pct': round(100 * corr / max(1, len(main)), 1), 'open3_pct': round(100 * open3 / max(1, len(main)), 1), 'deadends': dead,
           'warps': len(pts), 'buildings': len({q for q in [tuple(v[0]) for v in bld.values()]}), 'building_kinds': sorted(bld),
           'npcs': len(objs), 'signs': len([s for s in sg if s['type'] == 'sign']), 'trainers': trainers,
           'connections': {c['direction']: c['map'].replace('MAP_', '') for c in (m.get('connections') or [])},
           'unreach_warps': unreach_warps, 'unreach_edges': unreach_edges, 'unreach_objs': unreach_objs, 'unreach_signs': unreach_signs,
           'weather': m.get('weather'), 'type': m.get('map_type')}
    # parcours entre points clés
    keys = {}
    for k, cs in bld.items():
        dc = door_cell(cs[0])
        if dc: keys[k] = dc
    for d, cs in edges.items():
        cm = [c for c in cs if c in main]
        if cm: keys['EXIT_' + d] = cm[len(cm) // 2]
    paths = {}
    names = list(keys)
    tort = []
    for a in names:
        d = bfs([keys[a]], main, w, h)
        for b in names:
            if a < b and keys[b] in d:
                man = abs(keys[a][0] - keys[b][0]) + abs(keys[a][1] - keys[b][1])
                paths['%s>%s' % (a, b)] = (d[keys[b]], man)
                if man >= 6: tort.append(d[keys[b]] / man)
    res['paths'] = paths
    res['tortuosity'] = round(sum(tort) / len(tort), 2) if tort else None
    # mur de PNJ : portes de bâtiment atteignables uniquement par 1 case (goulot d'accès)
    return res


if __name__ == '__main__':
    only = [a for a in sys.argv[3:]] if len(sys.argv) > 3 else None
    out = {}
    for mid, m in sorted(MAPS.items()):
        if m.get('map_type') not in ('MAP_TYPE_CITY', 'MAP_TYPE_TOWN', 'MAP_TYPE_ROUTE', 'MAP_TYPE_OCEAN_ROUTE', 'MAP_TYPE_UNDERWATER'): continue
        if only and mid not in only: continue
        try:
            r = audit(mid)
        except Exception as e:
            r = {'id': mid, 'error': repr(e)}
        if r: out[mid] = r
    json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else '/dev/stdout', 'w'), indent=1, default=list)
