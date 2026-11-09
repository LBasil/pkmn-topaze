#!/usr/bin/env python3
"""Analyseur de cohérence des cartes (toutes les maps : extérieurs ET intérieurs).

Contrôles : tuiles (ids valides, collisions vs comportements), warps (destination, retour, case marchable),
connexions (réciproques, bords alignés), événements (hors carte, sur un mur, doublons, scripts inexistants),
déplacement (zones isolées, arrivée dans une zone coupée, pièges à sens unique via les rebords, sortie impossible),
rencontres sauvages (herbe/eau sans table, table sans herbe/eau).

Comparaison avec FireRed d'origine (--ref <racine>) : un problème n'est « nouveau » que s'il n'existe pas déjà dans
la carte d'origine de même identifiant (on n'imite pas FireRed : on isole juste ce que Topaze a introduit).

Usage : python3 tools/topaze/maps/analyze.py <racine_topaze> [--ref <racine_firered>] [--out rapport.json] [--md rapport.md]
"""
import json, os, re, struct, sys, hashlib, argparse
from collections import deque, defaultdict

DIRS = {'right': (1, 0), 'left': (-1, 0), 'down': (0, 1), 'up': (0, -1)}
D4 = list(DIRS.values())
WATER = {0x10, 0x11, 0x12, 0x15, 0x19, 0x1A, 0x1B}          # eau (Surf) ; 0x13 cascade traitée à part
WATERFALL = 0x13
IMPASS = set(range(0x30, 0x38))
LEDGE = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}
SPECIAL_MOVE = set(range(0x40, 0x59)) | {0x23, 0x26, 0x27, 0xD0, 0xD1, 0x50, 0x51, 0x52, 0x53}   # glace, glissades, tourniquets, courants
DOORISH = {0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x71}
ARROW = {0x62: (1, 0), 0x63: (-1, 0), 0x64: (0, -1), 0x65: (0, 1)}
NOSCRIPT = {'', '0x0', '0', 'NULL', None}


class Root:
    """Charge un dépôt (Topaze ou FireRed) : layouts, maps, attributs de tuiles, labels de scripts, rencontres."""
    def __init__(self, path):
        self.path = os.path.abspath(path)
        j = lambda p: json.load(open(os.path.join(self.path, p), encoding='utf-8'))
        self.layouts = {l['id']: l for l in j('data/layouts/layouts.json')['layouts'] if 'id' in l}
        self.maps = {}
        base = os.path.join(self.path, 'data/maps')
        for n in sorted(os.listdir(base)):
            f = os.path.join(base, n, 'map.json')
            if os.path.exists(f):
                m = json.load(open(f, encoding='utf-8')); m['_dir'] = n; self.maps[m['id']] = m
        t = open(os.path.join(self.path, 'src/data/tilesets/metatiles.h')).read()
        self.attr_path = {m.group(1): m.group(2) for m in re.finditer(r'gMetatileAttributes_(\w+)\[\]\s*=\s*INCBIN_U32\("([^"]+)"\)', t)}
        self._attr = {}; self._blk = {}
        self.labels = self._labels()
        self.wild = self._wild()

    def _labels(self):
        L = set(); rx = re.compile(r'^([A-Za-z_]\w*)::?', re.M)
        for dp, _, fs in os.walk(os.path.join(self.path, 'data')):
            for f in fs:
                if f.endswith(('.inc', '.s')):
                    try: L.update(rx.findall(open(os.path.join(dp, f), encoding='utf-8', errors='ignore').read()))
                    except OSError: pass
        return L

    def _wild(self):
        p = os.path.join(self.path, 'src/data/wild_encounters.json')
        out = defaultdict(set)
        if not os.path.exists(p): return out
        for g in json.load(open(p))['wild_encounter_groups']:
            for e in g.get('encounters', []):
                for k in ('land_mons', 'water_mons', 'fishing_mons', 'rock_smash_mons'):
                    if k in e: out[e['map']].add(k)
        return out

    def attrs(self, ts):
        k = ts.replace('gTileset_', '')
        if k not in self._attr:
            p = os.path.join(self.path, self.attr_path[k]) if k in self.attr_path else None
            self._attr[k] = struct.unpack('<%dI' % (os.path.getsize(p) // 4), open(p, 'rb').read()) if p and os.path.exists(p) else ()
        return self._attr[k]

    def tile(self, lay, mid):
        """(comportement, type de rencontre, id valide) d'un métatuile."""
        if mid < 640: a = self.attrs(lay['primary_tileset']); i = mid
        else: a = self.attrs(lay['secondary_tileset']); i = mid - 640
        if i >= len(a): return 0, 0, False
        return a[i] & 0x1FF, (a[i] >> 24) & 7, True

    def grid(self, lay):
        p = os.path.join(self.path, lay['blockdata_filepath'])
        if not os.path.exists(p): return None
        raw = open(p, 'rb').read(); n = lay['width'] * lay['height']
        if len(raw) != n * 2: return ['size', len(raw), n * 2]
        return struct.unpack('<%dH' % n, raw)


def analyse_map(R, mid, cache):
    """Retourne (stats, issues). issue = (code, sévérité, clé stable, message)."""
    m = R.maps[mid]; I = []
    def add(code, sev, key, msg): I.append((code, sev, str(key), msg))
    lay = R.layouts.get(m['layout'])
    if not lay: add('E01', 'E', m['layout'], 'layout %s introuvable' % m['layout']); return None, I
    g = R.grid(lay)
    if g is None: add('E01', 'E', 'blockdata', 'fichier map.bin absent'); return None, I
    if isinstance(g, list): add('E01', 'E', 'blocksize', 'map.bin = %d octets, attendu %d' % (g[1], g[2])); return None, I
    w, h = lay['width'], lay['height']
    cell = {}; bad_tiles = 0
    for y in range(h):
        for x in range(w):
            v = g[y * w + x]; mt = v & 0x3FF; col = (v >> 10) & 3
            b, enc, ok = R.tile(lay, mt)
            if not ok: bad_tiles += 1
            cell[(x, y)] = (b, col, enc, mt)
    if bad_tiles: add('E02', 'E', 'tiles', '%d cases utilisent un métatuile absent du tileset' % bad_tiles)
    inb = lambda x, y: 0 <= x < w and 0 <= y < h
    warps = m.get('warp_events') or []; objs = m.get('object_events') or []; bgs = m.get('bg_events') or []; coords = m.get('coord_events') or []
    wcell = {(q['x'], q['y']) for q in warps}

    land = lambda c: cell[c][1] == 0 and cell[c][0] not in IMPASS and cell[c][0] not in WATER and cell[c][0] != WATERFALL
    surf = lambda c: cell[c][0] in WATER
    walk = {c for c in cell if land(c)}
    water = {c for c in cell if surf(c)}
    special = any(v[0] in SPECIAL_MOVE for v in cell.values())

    # --- warps
    for i, q in enumerate(warps):
        c = (q['x'], q['y'])
        if not inb(*c): add('E05', 'E', 'warp@%d,%d' % c, 'warp %d hors carte (%d,%d)' % (i, *c)); continue
        dm = R.maps.get(q['dest_map'])
        if q['dest_map'] in ('MAP_DYNAMIC', 'MAP_UNDEFINED'): continue
        if not dm: add('E03', 'E', 'warp@%d,%d' % c, 'warp %d vers carte inexistante %s' % (i, q['dest_map'])); continue
        wid = q['dest_warp_id']
        if wid != 'WARP_ID_DYNAMIC':
            try:
                k = int(wid)
                dw = dm.get('warp_events') or []
                if k >= len(dw): add('E04', 'E', 'warp@%d,%d' % c, 'warp %d (%s) : id destination %d, mais %s n\'a que %d warps' % (i, 'x=%d,y=%d' % c, k, q['dest_map'], len(dw)))
                else:
                    back = dw[k]
                    if back['dest_map'] != mid and back['dest_map'] != 'MAP_DYNAMIC': add('W06', 'W', 'warp@%d,%d>%s' % (c[0], c[1], q['dest_map']), 'warp %d -> %s : le warp %d de là-bas ne revient pas ici (mène à %s)' % (i, q['dest_map'], k, back['dest_map']))
            except ValueError: add('E04', 'E', 'warp@%d,%d' % c, 'dest_warp_id invalide %r' % wid)
        b, col, _, _ = cell[c]
        sib = any(abs(q2['x'] - c[0]) + abs(q2['y'] - c[1]) == 1 and q2['dest_map'] == q['dest_map'] for q2 in warps)
        if col != 0 and b not in DOORISH and not sib:
            add('W07', 'W', 'warp@%d,%d' % c, 'warp %d (%d,%d) sur une case bloquée qui n\'est pas une porte' % (i, *c))
        if c == (0, 0): add('E07', 'E', 'warp@%d,%d' % c, 'warp %d encore en (0,0) : position jamais placée' % i)
    nodoor = [c for c, (b, col, _, _) in cell.items() if b in DOORISH and c not in wcell and b not in (0x66, 0x71) and col == 0]
    lone = [c for c in nodoor if not any(abs(c[0] - q['x']) + abs(c[1] - q['y']) <= 2 for q in warps)]
    ferry = not warps or any('ReturnFerry' in str(o.get('script', '')) for o in objs)
    if lone and not ferry:
        add('W08', 'W', 'doors', '%d tuile(s) de porte/échelle/tapis de sortie SANS warp à proximité : (%s)' % (len(lone), ' '.join('(%d,%d)' % c for c in sorted(lone)[:4])))
    elif nodoor:
        add('I08', 'I', 'doors', '%d tuiles de porte/tapis sans warp (carte à sortie par script/ferry, ou tapis voisin d\'un vrai warp)' % len(nodoor))
    # --- connexions
    for cn in (m.get('connections') or []):
        t = R.maps.get(cn['map'])
        if not t: add('E09', 'E', 'conn' + cn['direction'], 'connexion %s vers carte inexistante %s' % (cn['direction'], cn['map'])); continue
        rev = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}.get(cn['direction'])
        if not any(r['map'] == mid and r['direction'] == rev for r in (t.get('connections') or [])):
            add('W10', 'W', 'conn' + cn['direction'], 'connexion %s -> %s sans retour' % (cn['direction'], cn['map']))
        else:
            back = [r for r in t['connections'] if r['map'] == mid and r['direction'] == rev][0]
            if back['offset'] != -cn['offset'] and rev:
                add('W10', 'W', 'connoff' + cn['direction'], 'connexion %s -> %s : décalages incohérents (%d / %d)' % (cn['direction'], cn['map'], cn['offset'], back['offset']))
        tl = R.layouts.get(t['layout']);
        if not tl: continue
        tg = cache(R, tl)
        if not tg or isinstance(tg, list): continue
        tw, th = tl['width'], tl['height']; off = cn['offset']; d = cn['direction']; mism = tot = both = 0
        rng = range(max(0, off), min(w if d in ('up', 'down') else h, off + (tw if d in ('up', 'down') else th)))
        for s in rng:
            if d == 'up': a = (s, 0); o = (s - off, th - 1)
            elif d == 'down': a = (s, h - 1); o = (s - off, 0)
            elif d == 'left': a = (0, s); o = (tw - 1, s - off)
            else: a = (w - 1, s); o = (0, s - off)
            ob = tg[o[1] * tw + o[0]]; oc = (ob >> 10) & 3; obeh = R.tile(tl, ob & 0x3FF)[0]
            here = a in walk; there = oc == 0 and obeh not in IMPASS and obeh not in WATER
            if here or there: tot += 1
            if here and there: both += 1
            if here != there and not (a in water or obeh in WATER): mism += 1
        if tot and mism / tot > 0.34 and mism >= 3 and both == 0:
            add('W11', 'W', 'edge' + cn['direction'], 'bord %s vers %s : aucun passage possible (%d/%d cases marchables d\'un seul côté)' % (cn['direction'], cn['map'], mism, tot))
    # --- événements
    for kind, lst, key in (('PNJ', objs, 'object'), ('panneau', bgs, 'bg'), ('déclencheur', coords, 'coord')):
        seen = defaultdict(list)
        for i, o in enumerate(lst):
            c = (o['x'], o['y'])
            if not inb(*c): add('E12', 'E', '%s@%d,%d' % (key, c[0], c[1]), '%s %d hors carte (%d,%d)' % (kind, i, *c)); continue
            sc = o.get('script')
            if sc not in NOSCRIPT and sc not in R.labels and not str(sc).startswith(('0x', 'LOCALID')) and not re.fullmatch(r'\d+', str(sc)):
                add('E14', 'E', '%s@%d,%d' % (key, c[0], c[1]), '%s %d (%d,%d) : script %s inexistant' % (kind, i, c[0], c[1], sc))
            if key == 'object':
                seen[c].append((o.get('local_id') or o.get('graphics_id'), str(o.get('flag', '0')) not in ('0', '', 'None')))
                b, col, _, _ = cell[c]
                if col != 0 and b not in WATER and b != 0x80 and o.get('graphics_id') not in ('OBJ_EVENT_GFX_ITEM_BALL',) and not any((c[0] + dx, c[1] + dy) in walk for dx, dy in D4):
                    add('W13', 'W', 'object@%d,%d' % c, 'PNJ %d (%s) en (%d,%d) posé sur une case bloquée' % (i, str(o.get('graphics_id')).replace('OBJ_EVENT_GFX_', ''), *c))
            if key == 'coord' and c in cell and cell[c][1] != 0 and c not in wcell:
                add('W13', 'W', 'coord@%d,%d' % c, 'déclencheur %d en (%d,%d) sur case bloquée (jamais déclenché)' % (i, *c))
        for c, ids in seen.items():
            if len(ids) > 1 and not any(f for _, f in ids): add('W16', 'W', 'dup%d_%d' % c, '%d PNJ empilés sur (%d,%d)' % (len(ids), *c))
    # --- déplacement (graphe orienté, rebords gérés)
    def step(c, d):
        n = (c[0] + d[0], c[1] + d[1])
        if not inb(*n): return None
        if n in LEDGE_C:
            if LEDGE_C[n] != d: return None
            j = (n[0] + d[0], n[1] + d[1])
            return j if (j in walkall) else None
        return n if n in walkall else None
    LEDGE_C = {c: LEDGE[v[0]] for c, v in cell.items() if v[0] in LEDGE and v[1] == 0}
    walkall = walk | water | set(LEDGE_C) | {c for c in wcell if inb(*c) and cell[c][1] == 0}
    walkall = (walkall - set(LEDGE_C)) | set()
    walkall |= {c for c in wcell if inb(*c)}
    # cases de rebord : traversables seulement par saut (gérées dans step) ; on les garde hors de walkall
    edge_cells = set()
    for cn in (m.get('connections') or []):
        d = cn['direction']
        if d in DIRS:
            dx, dy = DIRS[d]
            for c in list(walkall):
                if not inb(c[0] + dx, c[1] + dy) and (c[0] in (0, w - 1) if dx else c[1] in (0, h - 1)):
                    if (dx == 1 and c[0] == w - 1) or (dx == -1 and c[0] == 0) or (dy == 1 and c[1] == h - 1) or (dy == -1 and c[1] == 0): edge_cells.add(c)
    exits = set(edge_cells)
    for q in warps:
        c = (q['x'], q['y'])
        if not inb(*c): continue
        exits.add(c)
        b = cell[c][0]
        if cell[c][1] != 0 or b not in DOORISH:        # porte bloquée visuellement (comptoir…) : on accepte la case voisine
            for d in D4:
                n = (c[0] + d[0], c[1] + d[1])
                if n in walkall: exits.add(n)
    adj = defaultdict(list); radj = defaultdict(list)
    for c in walkall:
        for d in D4:
            n = step(c, d)
            if n is not None: adj[c].append(n); radj[n].append(c)
    # composantes non orientées (sur les arêtes existantes)
    und = defaultdict(set)
    for c, ns in adj.items():
        for n in ns: und[c].add(n); und[n].add(c)
    comp_of = {}; comps = []
    for c in walkall:
        if c in comp_of: continue
        q = deque([c]); comp_of[c] = len(comps); cur = {c}
        while q:
            u = q.popleft()
            for v in und[u]:
                if v not in comp_of: comp_of[v] = len(comps); cur.add(v); q.append(v)
        comps.append(cur)
    def score(cp): return len(cp & exits) * 3 + len(cp) * 0.001
    main = max(comps, key=score) if comps else set()
    stats = dict(w=w, h=h, area=w * h, walk=len(walk), grass=sum(1 for v in cell.values() if v[2] == 1), watercells=len(water),
                 warps=len(warps), objs=len(objs), bgs=len(bgs), comps=len(comps), main=len(main), special=special,
                 type=m.get('map_type'), layout=m['layout'], hash=hashlib.md5(open(os.path.join(R.path, lay['blockdata_filepath']), 'rb').read()).hexdigest()[:10])
    # warps sans aucune case marchable autour (cul-de-sac local) ; l'accessibilité entre zones est testée globalement
    for i, q in enumerate(warps):
        c = (q['x'], q['y'])
        if inb(*c) and c not in walkall and not any(n in walkall for n in [(c[0] + dx, c[1] + dy) for dx, dy in D4]):
            add('W17', 'W', 'warp@%d,%d' % c, 'warp %d (%d,%d) -> %s : aucune case marchable autour' % (i, c[0], c[1], q['dest_map']))
    def reach(c):
        if c in main: return True
        for dx, dy in D4:
            n = (c[0] + dx, c[1] + dy)
            if n in main: return True
            if n in cell and cell[n][0] == 0x80 and (n[0] + dx, n[1] + dy) in main: return True     # parler par-dessus un comptoir
        return False
    if not special and exits:
        # pièges à sens unique : atteignables depuis l'entrée mais sans retour possible vers une sortie
        start = {c for c in main}
        rev = set(exits & main); q = deque(rev)
        while q:
            u = q.popleft()
            for v in radj[u]:
                if v in main and v not in rev: rev.add(v); q.append(v)
        trap = main - rev
        if trap:
            add('W19', 'W', 'trap', 'piège à sens unique : %d cases d\'où l\'on ne peut plus sortir (ex. %s)' % (len(trap), sorted(trap)[0]))
    if warps or m.get('connections'):
        if not (exits & main) and (m.get('map_type') != 'MAP_TYPE_UNDERWATER'):
            add('E20', 'E', 'noexit', 'aucune sortie atteignable dans la zone principale')
    # --- rencontres
    wild = R.wild.get(mid, set())
    gl = stats['grass']; wl = len(water) + sum(1 for v in cell.values() if v[2] == 2)
    if gl and 'land_mons' not in wild and m.get('map_type') in ('MAP_TYPE_ROUTE', 'MAP_TYPE_TOWN', 'MAP_TYPE_CITY') and gl >= 12:
        add('I21', 'I', 'grass', '%d cases d\'herbe/rencontre sans table de Pokémon sauvages' % gl)
    if 'land_mons' in wild and not gl:
        add('W22', 'W', 'noland', 'table de Pokémon terrestres mais aucune case de rencontre')
    if ('water_mons' in wild or 'fishing_mons' in wild) and not wl:
        add('W22', 'W', 'nowater', 'table eau/pêche mais aucune case d\'eau')
    return stats, I, (main, exits, cell, w, h, comp_of, edge_cells)


KNOWN = {}
def load_known(root):
    p = os.path.join(root, 'tools/topaze/maps/known_intentional.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def run(root, ref=None):
    R = Root(root); gcache = {}
    def cache(R_, lay):
        k = (R_.path, lay['id'])
        if k not in gcache: gcache[k] = R_.grid(lay)
        return gcache[k]
    res = {}
    for mid in sorted(R.maps):
        try:
            r = analyse_map(R, mid, cache)
            stats, issues = r[0], r[1]
        except Exception as e:
            stats, issues = None, [('E99', 'E', 'crash', 'analyse impossible : %r' % e)]
        res[mid] = dict(stats=stats, issues=issues, name=R.maps[mid]['name'])
    # arrivée dans une zone coupée : pour chaque warp entrant, la case d'arrivée doit être dans la zone principale
    return R, res


def arrival_checks(R, res):
    """Chaque warp A->B arrive sur la case du warp k de B : cette case doit être atteignable dans B."""
    cache = {}
    def main_of(mid):
        if mid not in cache:
            cache[mid] = analyse_map(R, mid, lambda R_, lay: R_.grid(lay))
        return cache[mid]
    out = defaultdict(list)
    for mid, m in R.maps.items():
        for i, q in enumerate(m.get('warp_events') or []):
            wid = q['dest_warp_id']
            if wid == 'WARP_ID_DYNAMIC' or q['dest_map'] not in R.maps: continue
            try: k = int(wid)
            except ValueError: continue
            dm = R.maps[q['dest_map']]; dw = dm.get('warp_events') or []
            if k >= len(dw): continue
            try: r = main_of(q['dest_map'])
            except Exception: continue
            if not r or len(r) < 3: continue
            main, exits, cell, w, h = r[2][:5]
            c = (dw[k]['x'], dw[k]['y'])
            if not (0 <= c[0] < w and 0 <= c[1] < h): continue
            comp_of = r[2][5]
            if c in comp_of or any((c[0] + dx, c[1] + dy) in comp_of for dx, dy in D4): continue
            out[q['dest_map']].append(('E23', 'E', 'arr@%d,%d' % c, 'on arrive (depuis %s) en (%d,%d) sans aucune case marchable autour' % (mid, *c)))
    return out


def global_reach(R, store, start='MAP_PALLET_TOWN_PLAYERS_HOUSE_2F'):
    """Zones (carte, composante) jamais atteignables depuis la chambre du joueur par warps + connexions."""
    info = {}
    for mid in R.maps:
        try: r = analyse_map(R, mid, lambda R_, lay: R_.grid(lay))
        except Exception: continue
        if r and len(r) == 3: info[mid] = r[2]
    def comps_at(mid, x, y):
        t = info.get(mid)
        if not t: return set()
        co = t[5]
        if (x, y) in co: return {co[(x, y)]}
        return {co[(x + dx, y + dy)] for dx, dy in D4 if (x + dx, y + dy) in co}
    adj = defaultdict(set)
    for mid, m in R.maps.items():
        if mid not in info: continue
        wa, ha, co = info[mid][3], info[mid][4], info[mid][5]
        for cn in (m.get('connections') or []):
            b = cn['map']
            if b not in info: continue
            off = cn['offset']; d = cn['direction']; wb, hb, cb = info[b][3], info[b][4], info[b][5]
            if d == 'up': pairs = [((x, 0), (x - off, hb - 1)) for x in range(wa)]
            elif d == 'down': pairs = [((x, ha - 1), (x - off, 0)) for x in range(wa)]
            elif d == 'left': pairs = [((0, y), (wb - 1, y - off)) for y in range(ha)]
            elif d == 'right': pairs = [((wa - 1, y), (0, y - off)) for y in range(ha)]
            else: continue
            for pa, pb in pairs:
                if pa in co and pb in cb: adj[(mid, co[pa])].add((b, cb[pb])); adj[(b, cb[pb])].add((mid, co[pa]))
        for q in (m.get('warp_events') or []):
            dm = q['dest_map']
            if dm not in info: continue
            try: k = int(q['dest_warp_id'])
            except ValueError: continue
            dw = R.maps[dm].get('warp_events') or []
            if not 0 <= k < len(dw): continue
            for ca in comps_at(mid, q['x'], q['y']):
                for cb_ in comps_at(dm, dw[k]['x'], dw[k]['y']): adj[(mid, ca)].add((dm, cb_))
    if start not in info: return {}
    # le chemin retour existe : on relie aussi dans l'autre sens les warps bidirectionnels, sinon Cut/PNJ-portes sont ignorés (voulu)
    seen = set(); q = deque()
    for c in comps_at(start, 6, 6): seen.add((start, c)); q.append((start, c))
    # entrées par script (warp MAP,x,y / setdynamicwarp) et points de Vol : le joueur y arrive sans passer par une porte
    rx = re.compile(r'^\s*(?:warp|warpsilent|warpdoor|setwarp|setescapewarp)\s+(MAP_\w+)\s*,\s*(?:\w+\s*,\s*)?(-?\d+)\s*,\s*(-?\d+)', re.M)
    for dp, _, fs in os.walk(os.path.join(R.path, 'data')):
        for f in fs:
            if not f.endswith(('.inc', '.s')): continue
            for mm, x, y in rx.findall(open(os.path.join(dp, f), encoding='utf-8', errors='ignore').read()):
                for c in comps_at(mm, int(x), int(y)):
                    if (mm, c) not in seen: seen.add((mm, c)); q.append((mm, c))
    hp = os.path.join(R.path, 'src/data/heal_locations.json')
    if os.path.exists(hp):
        for e in json.load(open(hp)).get('heal_locations', []):
            mm = e.get('map')
            if mm in info:
                for c in comps_at(mm, e.get('x', 0), e.get('y', 0)):
                    if (mm, c) not in seen: seen.add((mm, c)); q.append((mm, c))
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen: seen.add(v); q.append(v)
    def greach(mid, c):
        co = info[mid][5]; cell = info[mid][2]
        if co.get(c) is not None and (mid, co[c]) in seen: return True
        for dx, dy in D4:
            n = (c[0] + dx, c[1] + dy)
            if n in co and (mid, co[n]) in seen: return True
            n2 = (n[0] + dx, n[1] + dy)
            if n in cell and cell[n][0] == 0x80 and n2 in co and (mid, co[n2]) in seen: return True     # par-dessus un comptoir
        return False
    out = defaultdict(list)
    for mid, m in R.maps.items():
        if mid not in info: continue
        co = info[mid][5]
        for c in sorted(set(co.values())):
            if (mid, c) in seen: continue
            cells = [k for k, v in co.items() if v == c]
            ev = []
            for q_ in (m.get('warp_events') or []):
                if c in comps_at(mid, q_['x'], q_['y']): ev.append('warp (%d,%d)->%s' % (q_['x'], q_['y'], q_['dest_map'].replace('MAP_', '')))
            for o in (m.get('object_events') or []):
                if c in comps_at(mid, o['x'], o['y']) and not greach(mid, (o['x'], o['y'])): ev.append('PNJ %s (%d,%d)' % (str(o.get('graphics_id')).replace('OBJ_EVENT_GFX_', ''), o['x'], o['y']))
            for sgn in (m.get('bg_events') or []):
                if c in comps_at(mid, sgn['x'], sgn['y']) and not greach(mid, (sgn['x'], sgn['y'])): ev.append('%s (%d,%d)' % (sgn['type'], sgn['x'], sgn['y']))
            if ev:
                out[mid].append(('G01', 'E' if any(e.startswith('warp') for e in ev) else 'W', 'zone@%d,%d' % min(cells),
                                 'zone de %d cases jamais atteignable depuis le début du jeu, contient : %s%s' % (len(cells), ', '.join(ev[:4]), ' …' if len(ev) > 4 else '')))
    for mid, m in R.maps.items():
        if mid not in info: continue
        w_, h_ = info[mid][3], info[mid][4]
        for o in m.get('object_events') or []:
            c = (o['x'], o['y'])
            if 0 <= c[0] < w_ and 0 <= c[1] < h_ and not greach(mid, c):
                out[mid].append(('W18', 'W', 'object@%d,%d' % c, 'PNJ/objet %s en (%d,%d) hors de portée du joueur' % (str(o.get('graphics_id')).replace('OBJ_EVENT_GFX_', ''), *c)))
        for sgn in m.get('bg_events') or []:
            c = (sgn['x'], sgn['y'])
            if sgn['type'] in ('sign', 'hidden_item', 'secret_base') and 0 <= c[0] < w_ and 0 <= c[1] < h_ and not greach(mid, c):
                out[mid].append(('W18', 'W', 'bg@%d,%d' % c, '%s en (%d,%d) hors de portée du joueur' % (sgn['type'], *c)))
    # cartes entières jamais atteintes : probablement inutilisées -> une seule info, on ne les détaille pas
    for mid in list(R.maps):
        if mid in info and not any((mid, c) in seen for c in set(info[mid][5].values())):
            out[mid] = [('I09', 'I', 'unused', 'carte jamais atteinte depuis le début du jeu (inutilisée ?)')]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root'); ap.add_argument('--ref'); ap.add_argument('--out'); ap.add_argument('--md')
    a = ap.parse_args()
    R, res = run(a.root)
    for mid, extra in list(arrival_checks(R, res).items()) + list(global_reach(R, res).items()):
        seen = set()
        for it in extra:
            if it[2] in seen: continue
            seen.add(it[2]); res[mid]['issues'].append(it)
    ref = None
    if a.ref:
        RR, ref = run(a.ref)
        for mid, extra in list(arrival_checks(RR, ref).items()) + list(global_reach(RR, ref).items()):
            for it in extra: ref[mid]['issues'].append(it)
    known = load_known(a.root)
    for mid, r in res.items():
        why = known.get(mid)
        if why:
            r['issues'] = [('I10', 'I', i[2], '[volontaire : %s] %s' % (why, i[3])) if i[1] in 'EW' else i for i in r['issues']]
    report = []
    sev_n = defaultdict(int)
    for mid, r in res.items():
        st = r['stats']; refr = ref.get(mid) if ref else None
        base = {(i[0], i[2]) for i in refr['issues']} if refr else set()
        same_layout = bool(refr and refr['stats'] and st and refr['stats']['hash'] == st['hash'])
        new = []
        for code, sev, key, msg in r['issues']:
            baseline = (code, key) in base
            new.append(dict(code=code, sev=sev, msg=msg, baseline=baseline))
        cmp_notes = []
        if refr and refr['stats'] and st:
            a_, b_ = st['area'], refr['stats']['area']
            if b_ and not same_layout:
                if abs(a_ - b_) / b_ > .5: cmp_notes.append('taille %dx%d vs %dx%d FireRed' % (st['w'], st['h'], refr['stats']['w'], refr['stats']['h']))
                wp, rp = st['walk'] / max(1, a_), refr['stats']['walk'] / max(1, b_)
                if abs(wp - rp) > .25: cmp_notes.append('%d%% marchable vs %d%% FireRed' % (wp * 100, rp * 100))
                if st['warps'] < refr['stats']['warps'] * .5 and refr['stats']['warps'] >= 4: cmp_notes.append('%d warps vs %d FireRed' % (st['warps'], refr['stats']['warps']))
        report.append(dict(id=mid, name=r['name'], stats=st, issues=new, ref_present=bool(refr), same_as_ref=same_layout, notes=cmp_notes))
        for i in new:
            if not i['baseline']: sev_n[i['sev']] += 1
    if a.out: json.dump(report, open(a.out, 'w'), indent=1, default=list)
    if a.md: write_md(a.md, report, a.ref)
    print('cartes analysées : %d | nouveaux problèmes : E=%d W=%d I=%d' % (len(report), sev_n['E'], sev_n['W'], sev_n['I']))


def write_md(path, report, ref):
    L = ['# Analyse des cartes Topaze', '',
         'Problèmes **nouveaux** = absents de la carte FireRed de même identifiant (ou carte inchangée sans le défaut).' if ref else '',
         '']
    tot = defaultdict(lambda: defaultdict(int))
    for r in report:
        for i in r['issues']:
            if not i['baseline']: tot[i['code']][i['sev']] += 1
    L += ['| Code | Nb |', '|---|---|'] + ['| %s | %d |' % (c, sum(v.values())) for c, v in sorted(tot.items())] + ['']
    for sev, title in (('E', 'Erreurs (casse le jeu)'), ('W', 'Avertissements'), ('I', 'Infos')):
        rows = [(r, i) for r in report for i in r['issues'] if i['sev'] == sev and not i['baseline']]
        if not rows: continue
        L += ['## %s (%d)' % (title, len(rows)), '']
        cur = None
        for r, i in rows:
            if r['id'] != cur: L.append('- **%s** (`%s`)' % (r['name'], r['id'])); cur = r['id']
            L.append('  - `%s` %s' % (i['code'], i['msg']))
        L.append('')
    n = [(r['id'], r['notes']) for r in report if r['notes']]
    if n:
        L += ['## Écarts de gabarit avec FireRed (info, pas forcément un défaut)', ''] + ['- `%s` : %s' % (a, ' ; '.join(b)) for a, b in n]
    open(path, 'w').write('\n'.join(L))


if __name__ == '__main__':
    main()
