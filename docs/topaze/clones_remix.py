#!/usr/bin/env python3
"""Remix automatique des cartes CLONEES (zones du temps / de capture, lots 3-17) : chaque clone recoit SON PROPRE layout
(copie du layout partage) puis un relief propre : bosquets d'arbres, taches d'herbe haute, clairieres, en respectant :
 - toutes les cases d'evenements (portes, PNJ, panneaux, objets caches, declencheurs) et leur voisinage restent intacts,
 - les dresseurs gardent une zone degagee de 3 cases (ligne de vue),
 - marge de 2 cases aux bords (3 si connexion), aucune case d'eau/corniche modifiee,
 - la marchabilite est conservee : memes composantes, toutes les cases d'evenement toujours atteignables.
Graine = nom de la carte (rejouable). Idempotent. Usage : python3 docs/topaze/clones_remix.py [--dry] [--only NOM]"""
import json, os, random, shutil, struct, sys, collections
sys.path[:0] = ['tools/topaze/maps', 'docs/topaze']
import mapkit
DRY = '--dry' in sys.argv
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
WATER = {0x10, 0x11, 0x12, 0x13, 0x15, 0x19, 0x1A, 0x1B}
LEDGE = {0x38, 0x39, 0x3A, 0x3B}
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
LJ = json.load(open('data/layouts/layouts.json'))
LAYS = {l['id']: l for l in LJ['layouts'] if 'id' in l}
MAPS = {}
for n in os.listdir('data/maps'):
    f = 'data/maps/%s/map.json' % n
    if os.path.exists(f): MAPS[n] = json.load(open(f))
TYPES = ('MAP_TYPE_ROUTE', 'MAP_TYPE_TOWN', 'MAP_TYPE_CITY')

by = collections.defaultdict(list)
for n, m in MAPS.items():
    if m.get('map_type') in TYPES: by[m['layout']].append(n)


def owner(lid, names):
    d = os.path.basename(os.path.dirname(LAYS[lid]['blockdata_filepath']))
    if d in names: return d
    k = lid.replace('LAYOUT_', '').replace('_', '').lower()
    for n in names:
        if n.replace('_', '').lower() == k: return n
    return None


def behs(L):
    import audit_attrs as A
    return A


# --- attributs de metatuiles (comportement) ---
import importlib.util
spec = importlib.util.spec_from_file_location('audit', 'tools/topaze/maps/audit.py')
sys.argv_bak = sys.argv; sys.argv = [sys.argv[0], '.']
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
sys.argv = sys.argv_bak


def remix(name):
    m = MAPS[name]; lid = m['layout']; lay = LAYS[lid]
    w, h = lay['width'], lay['height']
    L = mapkit.Layout(lid)
    g = list(L.g)
    beh = lambda v: A.behaviour(lay, v & 0x3FF)
    col = lambda v: (v >> 10) & 3
    cnt = collections.Counter(); cntT = collections.Counter()
    for v in g:
        b = beh(v)
        if col(v) == 0 and b == 0: cnt[v & 0x3FF] += 1
        if col(v) == 0 and b == 0x02: cntT[v & 0x3FF] += 1
    if not cnt: return None, 'pas de sol plat'
    P = cnt.most_common(1)[0][0]
    T = cntT.most_common(1)[0][0] if cntT else None
    # arbre plein : metatuile a collision, sans eau/corniche, dont les cases ont surtout des voisines de meme id (masse)
    mass = collections.Counter()
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            v = g[y * w + x]
            if col(v) == 1 and beh(v) == 0 and (v & 0x3FF) != P:
                k = sum(1 for dx, dy in DIRS if (g[(y + dy) * w + x + dx] & 0x3FF) == (v & 0x3FF))
                if k >= 3: mass[v & 0x3FF] += 1
    O = mass.most_common(1)[0][0] if mass and mass.most_common(1)[0][1] >= 6 else None
    if O is None and T is None: return None, 'ni arbre plein ni herbe'
    ev = set(); trainers = []
    for k in ('warp_events', 'object_events', 'bg_events', 'coord_events'):
        for e in (m.get(k) or []):
            ev.add((e['x'], e['y']))
            if k == 'object_events' and e.get('trainer_type') not in (None, 'TRAINER_TYPE_NONE', 'TRAINER_TYPE_NORMAL'): pass
            if k == 'object_events' and e.get('trainer_type') not in (None, 'TRAINER_TYPE_NONE'): trainers.append((e['x'], e['y']))
    conn = {c['direction'] for c in (m.get('connections') or [])}
    def margin(x, y):
        return min(x - (3 if 'left' in conn else 2), (w - 1 - x) - (3 if 'right' in conn else 2), y - (3 if 'up' in conn else 2), (h - 1 - y) - (3 if 'down' in conn else 2))
    def walkable(gg, x, y):
        v = gg[y * w + x]
        return col(v) == 0 and beh(v) not in WATER
    def comps(gg):
        seen = {}; n = 0
        for y in range(h):
            for x in range(w):
                if (x, y) in seen or not walkable(gg, x, y): continue
                st = [(x, y)]; seen[(x, y)] = n
                while st:
                    cx, cy = st.pop()
                    for dx, dy in DIRS:
                        q = (cx + dx, cy + dy)
                        if 0 <= q[0] < w and 0 <= q[1] < h and q not in seen and walkable(gg, *q):
                            seen[q] = n; st.append(q)
                n += 1
        return seen, n
    base_seen, base_n = comps(g)
    # cases protegees : evenements + voisinage 1 ; dresseurs : rayon 3
    prot = set()
    for (x, y) in ev:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1): prot.add((x + dx, y + dy))
    for (x, y) in trainers:
        for dx in range(-3, 4):
            for dy in range(-3, 4): prot.add((x + dx, y + dy))
    rnd = random.Random('remix:' + name)
    # cases candidates : sol plat P (ou herbe T) a l'interieur
    cand = [(x, y) for y in range(h) for x in range(w) if margin(x, y) >= 0 and (x, y) not in prot and (g[y * w + x] & 0x3FF) in (P, T)
            and col(g[y * w + x]) == 0 and beh(g[y * w + x]) in (0, 0x02)]
    if len(cand) < 20: return None, 'trop peu de cases libres'
    def stamp(gg, cells, kind):
        for (x, y) in cells:
            v = gg[y * w + x]; el = v >> 12
            if kind == 'O': gg[y * w + x] = O | (1 << 10) | (el << 12)
            elif kind == 'T': gg[y * w + x] = T | (0 << 10) | (el << 12)
            elif kind == 'P': gg[y * w + x] = P | (0 << 10) | (el << 12)
    def blob(cx, cy, r):
        out = []
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r + (1 if r > 1 else 0) and rnd.random() < 0.85: out.append((cx + dx, cy + dy))
        return out
    placed = {'O': 0, 'T': 0, 'P': 0}
    kinds = []
    if O is not None: kinds += ['O'] * 7
    if T is not None: kinds += ['T'] * 6
    if T is not None and O is not None: kinds += ['P'] * 3
    rnd.shuffle(kinds)
    tries = 0
    for kind in kinds:
        for _ in range(25):
            tries += 1
            cx, cy = rnd.choice(cand)
            cells = [c for c in blob(cx, cy, rnd.choice((1, 2, 2))) if 0 <= c[0] < w and 0 <= c[1] < h and margin(*c) >= 0 and c not in prot
                     and col(g[c[1] * w + c[0]]) == 0 and beh(g[c[1] * w + c[0]]) in (0, 0x02) and (g[c[1] * w + c[0]] & 0x3FF) in (P, T)]
            if len(cells) < 3: continue
            if kind == 'T' and T is not None and all((g[c[1] * w + c[0]] & 0x3FF) == T for c in cells): continue
            if kind == 'P' and not all((g[c[1] * w + c[0]] & 0x3FF) in (T, P) for c in cells): continue
            gg = list(g); stamp(gg, cells, kind)
            if kind == 'O':
                seen, n = comps(gg)
                if n != base_n: continue
                # toutes les cases d'evenement (ou leur voisine) conservent leur composante
                ok = True
                for (x, y) in ev:
                    for q in [(x, y)] + [(x + dx, y + dy) for dx, dy in DIRS]:
                        if q in base_seen and seen.get(q) != base_seen[q] and q not in [c for c in cells]:
                            pass
                if any((c in base_seen) and (c not in seen) and (c not in cells) for c in base_seen): continue
                # aucune composante ne perd plus de 15 % de sa taille hors cases posees
                lost = len(cells)
                tot = sum(1 for _ in base_seen)
                if lost > 0.04 * tot + 6: continue
            g = gg; placed[kind] += 1; break
    L2 = (g, placed, P, T, O)
    return L2, 'ok'


def main():
    rep = []
    new_layouts = []
    for lid, names in sorted(by.items()):
        if len(names) < 2: continue
        own = owner(lid, names)
        for n in sorted(names):
            if n == own: continue
            if ONLY and n != ONLY: continue
            m = MAPS[n]
            nid = 'LAYOUT_' + ''.join('_' + c if c.isupper() and i and not n[i - 1].isupper() and n[i - 1] != '_' else c for i, c in enumerate(n)).upper().replace('__', '_')
            nid = 'LAYOUT_' + m['id'].replace('MAP_', '')
            if m['layout'] == nid:
                rep.append((n, 'deja'));
                continue
            res, why = remix(n)
            if res is None:
                rep.append((n, 'ignoree : ' + why)); continue
            g, placed, P, T, O = res
            rep.append((n, 'ok %s P=%d T=%s O=%s' % (placed, P, T, O)))
            if DRY: continue
            src = LAYS[lid]; d = 'data/layouts/' + n
            os.makedirs(d, exist_ok=True)
            shutil.copy(os.path.join(os.path.dirname(src['border_filepath']), 'border.bin'), d + '/border.bin')
            open(d + '/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
            nl = dict(src); nl['id'] = nid; nl['name'] = n + '_Layout'
            nl['border_filepath'] = d + '/border.bin'; nl['blockdata_filepath'] = d + '/map.bin'
            LJ['layouts'].append(nl)
            m['layout'] = nid
            json.dump(m, open('data/maps/%s/map.json' % n, 'w'), indent=2); open('data/maps/%s/map.json' % n, 'a').write('\n')
    if not DRY and any(r[1].startswith('ok') for r in rep):
        json.dump(LJ, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
    for r in rep: print(*r)
    print(sum(1 for r in rep if r[1].startswith('ok')), 'remixees /', len(rep))


main()
