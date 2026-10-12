# ROUTES 5 / 6 / 7 (voisines de Hematown) v2 : DECOR (apres hematown_routes.py, apres apatia_town.py et celadopole_town.py qui exportent leurs ids de decor).
#   Route 5 (Tourmalia)   : v3. Les deux bandes de sable (fermees par des barrieres, jamais atteintes) deviennent deux bosquets de tourmaline : pelouse, grands arbres ronds et amas de cristaux repris de la Route 24
#                           (extraits de sa carte et re-poses sur n'importe quelle herbe), fleurs ; dans la foret, des amas de cristaux remplacent quelques arbres ; 2 arbres et quelques cristaux dans la zone de la pension.
#   Route 6 (Apatia)     : v3. Cimetiere de dragon : squelette (crane + cotes) dans la prairie nord, nids d'oeufs, plumes, griffes, manches a air d'Apatia et cristaux d'apatite (apatia_art_ids.json).
#   Route 7 (Bourg Quartz): cristaux de quartz-glace et bonhommes de neige (decor de la ville, celadopole_art_ids.json).
# Jamais d'acces coupe (BFS sur les points importants : warps, PNJ, panneaux, bords de carte). Idempotent : part des cartes d'origine (route21_src/r5|r6|r7_orig.bin).
# Lancer depuis la racine : PYTHONDONTWRITEBYTECODE=1 python3 docs/topaze/hematown_routes_decor.py
import struct, json, random, os, shutil, collections
SRC = 'docs/topaze/route21_src/'
GRASS = {0x3008: 8, 0x3009: 9, 0x3010: 16, 0x3011: 17}
ROUTES = {'Route5': (48, 40, 'r5'), 'Route6': (24, 40, 'r6'), 'Route7': (24, 20, 'r7')}
def load(name):
    w, h, key = ROUTES[name]
    if not os.path.exists(SRC + key + '_orig.bin'): shutil.copy('data/layouts/%s/map.bin' % name, SRC + key + '_orig.bin')
    return w, h, list(struct.unpack('<%dH' % (w * h), open(SRC + key + '_orig.bin', 'rb').read())), json.load(open('data/maps/%s/map.json' % name))
def save(name, w, h, g): open('data/layouts/%s/map.bin' % name, 'wb').write(struct.pack('<%dH' % (w * h), *g))
class Board:
    def __init__(s, w, h, g, mj):
        s.w, s.h, s.g = w, h, g
        s.imp = {(e['x'], e['y']) for k in ('warp_events', 'object_events', 'bg_events') for e in mj[k]}
        s.imp |= {(x, y) for y in range(h) for x in range(w) if s.walk((x, y)) and (x <= 0 or y <= 0 or x >= w - 1 or y >= h - 1)}
        s.imp = {c for c in s.imp if 0 <= c[0] < w and 0 <= c[1] < h}
        s.base = s.partition(frozenset()); s.blocked = set()
    def walk(s, c, blocked=frozenset()): return 0 <= c[0] < s.w and 0 <= c[1] < s.h and (s.g[c[1] * s.w + c[0]] & 0xc00) == 0 and c not in blocked
    def partition(s, blocked):
        seen = {}; n = 0
        for c in sorted(s.imp):
            if c in seen or not s.walk(c, blocked): continue
            n += 1; seen[c] = n; q = collections.deque([c]); vis = {c}
            while q:
                a = q.popleft()
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    b = (a[0] + d[0], a[1] + d[1])
                    if b not in vis and s.walk(b, blocked): vis.add(b); q.append(b)
            for p in s.imp:
                if p in vis: seen[p] = n
        groups = collections.defaultdict(set)
        for p in s.imp: groups[seen.get(p, 0)].add(p)
        return {frozenset(v) for k, v in groups.items() if k}
    def isgrass(s, c): return 0 <= c[0] < s.w and 0 <= c[1] < s.h and s.g[c[1] * s.w + c[0]] in GRASS
    def free(s, c, m): return s.isgrass(c) and c not in s.blocked and m < c[0] < s.w - 1 - m and m < c[1] < s.h - 1 - m and not any(abs(c[0] - p[0]) <= 2 and abs(c[1] - p[1]) <= 2 for p in s.imp)
    def put(s, cells):                      # cells : {case: id de metatuile (avec la base d'herbe deja choisie)}
        if any(c in s.blocked or not s.isgrass(c) for c in cells): return False
        if s.partition(frozenset(s.blocked | set(cells))) != s.base: return False
        s.blocked |= set(cells)
        for c, m in cells.items(): s.g[c[1] * s.w + c[0]] = (s.g[c[1] * s.w + c[0]] & 0xf000) | m
        return True
    def base_of(s, c): return GRASS[s.g[c[1] * s.w + c[0]]]
    def cands(s, margin=2):
        out = [c for c in ((x, y) for y in range(s.h) for x in range(s.w)) if s.free(c, margin) and sum(1 for d in ((1, 0), (-1, 0), (0, 1), (0, -1)) if s.isgrass((c[0] + d[0], c[1] + d[1]))) >= 2]
        return out
def spaced(c, pts, d): return all(max(abs(c[0] - q[0]), abs(c[1] - q[1])) >= d for q in pts)

# ------------------------------------------------------------------ extraction du decor de la Route 24 (arbres ronds, amas et eclats de tourmaline) -> metatuiles re-posables sur toute herbe
def harvest24():
    pm = open('data/tilesets/secondary/cerulean_pepite/metatiles.bin', 'rb').read()
    ent = lambda m: struct.unpack('<8H', pm[(m - 640) * 16:(m - 640) * 16 + 16])
    g24 = struct.unpack('<%dH' % (24 * 40), open('data/layouts/Route24/map.bin', 'rb').read()); idn = lambda x, y: g24[y * 24 + x] & 0x3ff
    MID, BOT, OV = {792, 793, 796, 797, 800, 805, 806}, {794, 795, 798, 799, 801, 802, 803, 804}, set(range(775, 784))
    trees = set(); clus = set()
    for y in range(1, 39):
        for x in range(23):
            if idn(x, y) in MID and idn(x + 1, y) in MID and idn(x, y + 1) in BOT and idn(x + 1, y + 1) in BOT and idn(x, y - 1) in OV and idn(x + 1, y - 1) in OV:
                trees.add(tuple(ent(idn(x + i, y + j))[4:8] for j in (-1, 0, 1) for i in (0, 1)))
            for ids in ((784, 785, 786, 787), (788, 789, 790, 791)):
                if (idn(x, y), idn(x + 1, y), idn(x, y + 1), idn(x + 1, y + 1)) == ids: clus.add(tuple(ent(m)[4:8] for m in ids))
    shard = ent(807)[4:8]
    assert len(trees) >= 1 and len(clus) == 2, (len(trees), len(clus))
    return sorted(trees), sorted(clus), shard
class Reg:                                  # nouvelles metatuiles du secondaire de la Route 5 : art de la Route 24 sur un fond d'herbe au choix
    def __init__(s):
        s.D = 'data/tilesets/secondary/cerulean_route5/'
        for f in ('metatiles.bin', 'metatile_attributes.bin'): shutil.copy('data/tilesets/secondary/cerulean_pepite/' + f, s.D + f)
        s.mt = bytearray(open(s.D + 'metatiles.bin', 'rb').read()); s.att = bytearray(open(s.D + 'metatile_attributes.bin', 'rb').read())
        s.pm = open('data/tilesets/primary/general_route5/metatiles.bin', 'rb').read(); s.cache = {}; s.n0 = len(s.mt) // 16
    def meta(s, top4, base):
        e = struct.unpack('<4H', s.pm[base * 16:base * 16 + 8]) + tuple(top4)
        if e not in s.cache:
            s.cache[e] = 640 + len(s.mt) // 16; s.mt += struct.pack('<8H', *e); s.att += struct.pack('<I', 0)
        return s.cache[e]
    def flush(s):
        assert len(s.mt) // 16 <= 384, len(s.mt) // 16
        open(s.D + 'metatiles.bin', 'wb').write(s.mt); open(s.D + 'metatile_attributes.bin', 'wb').write(s.att)
        return len(s.mt) // 16 - s.n0
grassid = lambda x, y: 8 + (x & 1) + 8 * (y & 1)

# ------------------------------------------------------------------ Route 5 : bosquets de tourmaline
def route5():
    w, h, g, mj = load('Route5'); rnd = random.Random(515)
    TR, CL, SH = harvest24(); R = Reg()
    def put_tree(x, y, sig):                # cime en (x..x+1, y-1) (case praticable), tronc en (x..x+1, y..y+1)
        for k, (i, j) in enumerate(((0, -1), (1, -1), (0, 0), (1, 0), (0, 1), (1, 1))):
            c = (x + i, y + j); g[c[1] * w + c[0]] = (0x3000 if j < 0 else 0x3400) | R.meta(sig[k], grassid(*c))
    def put_cluster(x, y, sig):
        for k, (i, j) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            c = (x + i, y + j); g[c[1] * w + c[0]] = 0x3400 | R.meta(sig[k], grassid(*c))
    def put_shard(c): g[c[1] * w + c[0]] = 0x3400 | R.meta(SH, grassid(*c))
    # 1) les deux bandes de sable (x 15..18, y 0..26 ; fermees, inaccessibles) -> bosquets
    imp = {(e['x'], e['y']) for k in ('warp_events', 'object_events', 'bg_events') for e in mj[k]}
    assert not any(15 <= x <= 18 or 29 <= x <= 32 for x, y in imp if y <= 26), 'un evenement se trouve dans une bande de sable'
    for x0 in (15, 29):
        for y in range(0, 27):
            for x in range(x0, x0 + 4): g[y * w + x] = 0x3000 | grassid(x, y)
        occ = set(); nt = 0
        for _ in range(400):
            if nt >= 8: break
            x, y = x0 + rnd.randrange(3), rnd.randrange(1, 25)
            foot = {(x + i, y + j) for i in (0, 1) for j in (-1, 0, 1)}
            ring = {(a + dx, b + dy) for a, b in foot for dx in (-1, 0, 1) for dy in (0, 1)}
            if foot & occ or (ring & occ and rnd.random() < 0.8): continue
            put_tree(x, y, rnd.choice(TR)); occ |= foot; nt += 1
        nc = 0
        for _ in range(400):
            if nc >= 3: break
            x, y = x0 + rnd.randrange(3), rnd.randrange(0, 25)
            foot = {(x + i, y + j) for i in (0, 1) for j in (0, 1)}
            if foot & occ: continue
            put_cluster(x, y, rnd.choice(CL)); occ |= foot; nc += 1
        free = [(x, y) for y in range(0, 27) for x in range(x0, x0 + 4) if (x, y) not in occ]; rnd.shuffle(free); ns = 0
        for c in free:
            if ns >= 5: break
            put_shard(c); occ.add(c); ns += 1
        for c in [c for c in free if c not in occ][:12]: g[c[1] * w + c[0]] = 0x3000 | 4          # fleurs
        print('bande x%d : %d arbres, %d amas, %d eclats' % (x0, nt, nc, ns))
    # 2) dans la foret : quelques arbres FR remplaces par un amas de cristaux (meme gabarit 2x2, meme grille)
    TOP, BOT = {20, 21, 22, 23}, {28, 29, 30, 31}
    ident = lambda x, y: g[y * w + x] & 0x3ff
    tree_at = lambda x, y: ident(x, y) in TOP and ident(x + 1, y) in TOP and ident(x, y + 1) in BOT and ident(x + 1, y + 1) in BOT and all(g[(y + j) * w + x + i] & 0xc00 for i in (0, 1) for j in (0, 1))
    blocks = sorted((x, y) for y in range(3, 36, 2) for x in list(range(2, 13, 2)) + list(range(34, 45, 2)) if tree_at(x, y)); rnd.shuffle(blocks); chosen = []
    for b in blocks:
        if len(chosen) >= 14: break
        if all(abs(b[0] - c[0]) > 6 or abs(b[1] - c[1]) > 6 for c in chosen): chosen.append(b)
    for (x, y) in chosen: put_cluster(x, y, rnd.choice(CL))
    # 3) zone de la pension (accessible) : 2 grands arbres, eclats et fleurs, sans jamais couper un acces
    B = Board(w, h, g, mj); base = B.base; ntr = 0
    spots = [(x, y) for y in range(28, 36) for x in range(14, 34) if all(B.free((x + i, y + j), 1) for i in (0, 1) for j in (-1, 0, 1))]; rnd.shuffle(spots); placed = []
    for (x, y) in spots:
        if ntr >= 3: break
        if not spaced((x, y), placed, 6): continue
        sig = rnd.choice(TR); cells = {}
        for k, (i, j) in enumerate(((0, -1), (1, -1), (0, 0), (1, 0), (0, 1), (1, 1))): cells[(x + i, y + j)] = (0x0 if j < 0 else 0x400) | R.meta(sig[k], B.base_of((x + i, y + j)))
        if B.put(cells): ntr += 1; placed.append((x, y))
    cand = B.cands(); rnd.shuffle(cand); ns = 0
    for c in cand:
        if ns >= 5: break
        if spaced(c, placed, 3) and B.put({c: 0x400 | R.meta(SH, B.base_of(c))}): ns += 1; placed.append(c)
    for c in [c for c in cand if c not in B.blocked and spaced(c, placed, 2)][:10]: B.g[c[1] * w + c[0]] = 0x3000 | 4
    n_new = R.flush(); save('Route5', w, h, B.g)
    print('Route5 : %d amas dans la foret, %d grands arbres + %d eclats pres de la pension, +%d metatuiles (%d/384)' % (len(chosen), ntr, ns, n_new, R.n0 + n_new))

# ------------------------------------------------------------------ Route 6 : cimetiere de dragon
def route6():
    A = json.load(open('docs/topaze/apatia_art_ids.json'))
    w, h, g, mj = load('Route6'); B = Board(w, h, g, mj); n = collections.Counter()
    near = lambda c: any(max(abs(c[0] - p[0]), abs(c[1] - p[1])) <= 1 for p in B.imp)
    def one(kind, c, v=0):
        if not B.isgrass(c) or near(c): return
        b = B.base_of(c)
        key = {'nest': 'nest_%d', 'feather': 'feather_%d', 'pole': 'pole_%d', 'sock': 'sock_%d'}.get(kind)
        key = key % b if key else ('rib_%d_%d' % (c[1] % 2, b) if kind == 'rib' else '%s_%d_%d' % (kind, v, b))
        if B.put({c: 0x400 | A[key]}): n[kind] += 1
    def skull(x, y):
        cells = {(x + i, y + j): 0x400 | A['skull_%d_%d_%d' % (i, j, B.base_of((x + i, y + j)))] for i in (0, 1) for j in (0, 1)}
        if all(B.isgrass(c) and not near(c) for c in cells) and B.put(cells): n['skull'] += 1
    # prairie nord : le squelette (crane a l'ouest, cage thoracique en zigzag), la queue au bout, de l'autre cote nids et plumes
    skull(2, 9)
    for c in ((5, 10), (6, 9), (7, 10), (8, 9), (11, 10), (12, 9), (13, 10), (14, 9)): one('rib', c)
    for c, v in (((4, 8), 0), ((10, 8), 1), ((16, 10), 0), ((21, 8), 1)): one('talon', c, v)
    for c in ((9, 10), (3, 8), (15, 8)): one('feather', c)
    for c in ((19, 9), (17, 9)): one('nest', c)
    one('pole', (6, 8)); one('pole', (13, 8)); one('sock', (20, 8)); one('sock', (2, 8))
    # salles laterales du nord : cristaux d'apatite
    for c, v in (((2, 5), 0), ((8, 6), 1), ((21, 5), 2), ((17, 6), 0), ((3, 6), 1)): one('cry', c, v)
    # prairie sud-ouest : nid d'oeufs de dragon
    for c in ((3, 28), (6, 27), (8, 29), (4, 29)): one('nest', c)
    for c in ((5, 28), (7, 28)): one('feather', c)
    one('cry', (2, 27), 2); one('talon', (9, 27), 1); one('rib', (2, 29))
    # un peu partout sur l'herbe plate restante : cristaux et plumes isoles
    rnd = random.Random(616); cand = [c for c in B.cands() if not near(c)]; rnd.shuffle(cand); placed = list(B.blocked)
    for c in cand:
        if n['cry'] >= 9: break
        if spaced(c, placed, 4): one('cry', c, rnd.randrange(3)); placed.append(c)
    save('Route6', w, h, B.g); print('Route6 :', dict(n))

# ------------------------------------------------------------------ Route 7 : cristaux de quartz et bonhommes de neige
def route7():
    A = json.load(open('docs/topaze/celadopole_art_ids.json'))
    w, h, g, mj = load('Route7'); B = Board(w, h, g, mj); rnd = random.Random(707)
    placed = []; nsn = 0; ncr = 0
    wins = [(x, y) for y in range(h) for x in range(w) if all(B.free((x + i, y + j), 1) for i in range(2) for j in range(3))]
    rnd.shuffle(wins)
    for (x, y) in wins:
        if nsn >= 2: break
        if not spaced((x, y), placed, 5): continue
        cells = {(x + i, y + j): 0x400 | A['snow_%d_%d_%d' % (i, j, B.base_of((x + i, y + j)))] for i in range(2) for j in range(3)}
        if B.put(cells): nsn += 1; placed.append((x, y))
    cand = B.cands(); rnd.shuffle(cand)
    for c in cand:
        if ncr >= 7: break
        if spaced(c, placed, 3) and B.put({c: 0x400 | A['cry_%d_%d' % (rnd.randrange(3), B.base_of(c))]}): ncr += 1; placed.append(c)
    save('Route7', w, h, B.g); print('Route7 : %d bonhommes, %d cristaux' % (nsn, ncr))


route5(); route6(); route7()
