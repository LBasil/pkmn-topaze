# ROUTES 8 / 10 / 12 (voisines de Spinellia) : habillage v1.
# Les trois routes passent sur les tilesets de la ville (GeneralSpinellia / LavenderSpinellia : copies de General + LavenderTown teintees, memes numeros de metatuiles :
# la carte d'origine reste valable telle quelle) ; on y seme quelques steles (par petits groupes) et des cristaux de spinelle sur l'herbe, loin des chemins, des portes,
# des PNJ et des bords de carte, sans jamais separer deux points importants (BFS). Les metatuiles de decor viennent de spinellia_town.py (spinellia_art_ids.json).
# Idempotent : part des cartes d'origine conservees dans docs/topaze/route21_src/r<N>_orig.bin. Ordre : spinellia_town -> spinellia_routes -> spinellia_routes_events.
# Lancer depuis la racine : PYTHONDONTWRITEBYTECODE=1 python3 docs/topaze/spinellia_routes.py
import struct, json, random, os, shutil, collections
SRC = 'docs/topaze/route21_src/'
ART = json.load(open('docs/topaze/spinellia_art_ids.json'))
ROUTES = {'Route8': (72, 20, 'LAYOUT_ROUTE8', 'r8'), 'Route10': (24, 80, 'LAYOUT_ROUTE10', 'r10'), 'Route12': (24, 120, 'LAYOUT_ROUTE12', 'r12')}
GRASS = {0x3008: 8, 0x3009: 9, 0x3010: 16, 0x3011: 17}
# bords de carte laisses libres (connexions / jonctions) : x ou y <= marge
EDGE = {'Route8': dict(l=3, r=3, t=1, b=1), 'Route10': dict(l=3, r=1, t=3, b=3), 'Route12': dict(l=3, r=1, t=3, b=4)}
TARGET = {'Route8': (44, 7, 9), 'Route10': (38, 6, 8), 'Route12': (14, 3, 3)}      # (steles, cristaux, centres de groupes)
STEPS = {'Route8': dict(density=0.12, cry=45), 'Route10': dict(density=0.12, cry=40), 'Route12': dict(density=0.12, cry=45)}
# ---- tilesets
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') in {v[2] for v in ROUTES.values()}:
        l['primary_tileset'] = 'gTileset_GeneralSpinellia'; l['secondary_tileset'] = 'gTileset_LavenderSpinellia'
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
for name, (w, h, lid, key) in ROUTES.items():
    if not os.path.exists(SRC + key + '_orig.bin'): shutil.copy('data/layouts/%s/map.bin' % name, SRC + key + '_orig.bin')
    g = list(struct.unpack('<%dH' % (w * h), open(SRC + key + '_orig.bin', 'rb').read()))
    mj = json.load(open('data/maps/%s/map.json' % name))
    rnd = random.Random(sum(map(ord, name)) * 31)
    walk = lambda c, blocked=frozenset(): 0 <= c[0] < w and 0 <= c[1] < h and (g[c[1] * w + c[0]] & 0xc00) == 0 and c not in blocked
    # points importants : warps, PNJ, panneaux/objets cachés, cellules de bord (connexions)
    imp = {(e['x'], e['y']) for k in ('warp_events', 'object_events', 'bg_events') for e in mj[k]}
    e_ = EDGE[name]
    imp |= {(x, y) for y in range(h) for x in range(w) if walk((x, y)) and (x <= 0 or y <= 0 or x >= w - 1 or y >= h - 1)}
    imp = {c for c in imp if 0 <= c[0] < w and 0 <= c[1] < h}
    def comps(blocked):
        seen = {}; n = 0
        for c in sorted(imp):
            if c in seen or not walk(c, blocked): continue
            n += 1; seen[c] = n; q = collections.deque([c]); vis = {c}
            while q:
                a = q.popleft()
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    b = (a[0] + d[0], a[1] + d[1])
                    if b not in vis and walk(b, blocked): vis.add(b); q.append(b)
            for p in imp:
                if p in vis: seen[p] = n
        return {p: seen.get(p, 0) for p in imp}
    def partition(blocked):
        cm = comps(blocked); groups = collections.defaultdict(set)
        for p, k in cm.items(): groups[k].add(p)
        return {frozenset(v) for k, v in groups.items() if k}
    base = partition(frozenset())
    isgrass = lambda c: 0 <= c[0] < w and 0 <= c[1] < h and g[c[1] * w + c[0]] in GRASS
    cand = []
    for y in range(h):
        for x in range(w):
            c = (x, y)
            if not isgrass(c) or x <= e_['l'] or x >= w - 1 - e_['r'] or y <= e_['t'] or y >= h - 1 - e_['b']: continue
            ok = sum(1 for d in ((1, 0), (-1, 0), (0, 1), (0, -1)) if isgrass((x + d[0], y + d[1]))) >= 2          # jamais dans un couloir d'herbe etroit
            if ok and not any(abs(x - p[0]) <= 2 and abs(y - p[1]) <= 2 for p in imp): cand.append(c)
    rnd.shuffle(cand)
    centers = cand[:TARGET[name][2]]                                # petits groupes de steles autour de quelques centres
    blocked = set(); nst = ncr = 0; cries = []
    def put(c, kind):
        global_ok = partition(frozenset(blocked | {c})) == base
        if not global_ok: return False
        blocked.add(c); gb = GRASS[g[c[1] * w + c[0]]]; v = rnd.randrange(3 if kind == 'cry' else 4)
        g[c[1] * w + c[0]] = (g[c[1] * w + c[0]] & 0xf000) | ART['%s_%d_%d' % (kind, v, gb)]
        return True
    for c in cand:                                                    # cristaux : espaces d'au moins 6 cases
        if ncr >= TARGET[name][1]: break
        if all(max(abs(c[0] - q[0]), abs(c[1] - q[1])) >= 6 for q in cries) and put(c, 'cry'): ncr += 1; cries.append(c)
    order = sorted((c for c in cand if c not in blocked), key=lambda c: min(max(abs(c[0] - q[0]), abs(c[1] - q[1])) for q in centers) + rnd.random() * 3)
    for c in order:
        if nst >= TARGET[name][0]: break
        if put(c, 'stele'): nst += 1
    assert partition(frozenset(c for c in blocked)) == base
    open('data/layouts/%s/map.bin' % name, 'wb').write(struct.pack('<%dH' % (w * h), *g))
    print('%s : %d cases d herbe candidates, %d steles, %d cristaux' % (name, len(cand), nst, ncr))
