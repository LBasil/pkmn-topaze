# ROUTES 5 / 6 / 7 (voisines de Hematown) v2 : DECOR (apres hematown_routes.py, apres apatia_town.py et celadopole_town.py qui exportent leurs ids de decor).
#   Route 5 (Tourmalia)   : v3. Les deux bandes de sable (fermees par des barrieres, jamais atteintes) deviennent deux bosquets de tourmaline : pelouse, grands arbres ronds et amas de cristaux repris de la Route 24
#                           (extraits de sa carte et re-poses sur n'importe quelle herbe), fleurs ; dans la foret, des amas de cristaux remplacent quelques arbres ; 2 arbres et quelques cristaux dans la zone de la pension.
#   Route 6 (Apatia)     : v3. Cimetiere de dragon : squelette (crane + cotes) dans la prairie nord, nids d'oeufs, plumes, griffes, manches a air d'Apatia et cristaux d'apatite (apatia_art_ids.json).
#   Route 7 (Bourg Quartz): cristaux de quartz-glace et bonhommes de neige (decor de la ville, celadopole_art_ids.json).
# Jamais d'acces coupe (BFS sur les points importants : warps, PNJ, panneaux, bords de carte). Idempotent : part des cartes d'origine (route21_src/r5|r6|r7_orig.bin).
# Lancer depuis la racine : PYTHONDONTWRITEBYTECODE=1 python3 docs/topaze/hematown_routes_decor.py
import struct, json, random, os, shutil, collections, math
from PIL import Image
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
        s.img = Image.open(s.D + 'tiles.png'); s.NTL = (s.img.width // 8) * (s.img.height // 8); s.NEWT = []
    def tile(s, t):
        t = tuple(t)
        if t not in s.NEWT: s.NEWT.append(t)
        return s.NEWT.index(t)
    def meta(s, top4, base, att=0):
        e = struct.unpack('<4H', s.pm[base * 16:base * 16 + 8]) + tuple(top4)
        if (e, att) not in s.cache:
            s.cache[(e, att)] = 640 + len(s.mt) // 16; s.mt += struct.pack('<8H', *e); s.att += struct.pack('<I', att)
        return s.cache[(e, att)]
    def flush(s):
        assert len(s.mt) // 16 <= 384 and s.NTL + len(s.NEWT) <= 384, (len(s.mt) // 16, s.NTL + len(s.NEWT))
        if s.NEWT:
            rows = (s.NTL + len(s.NEWT) + 15) // 16; out = Image.new('P', (128, rows * 8), 0); out.putpalette(s.img.getpalette()); out.paste(s.img, (0, 0))
            for n, t in enumerate(s.NEWT):
                ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((s.NTL + n) % 16) * 8, ((s.NTL + n) // 16) * 8))
            out.save(s.D + 'tiles.png')
        open(s.D + 'metatiles.bin', 'wb').write(s.mt); open(s.D + 'metatile_attributes.bin', 'wb').write(s.att)
        return len(s.mt) // 16 - s.n0
grassid = lambda x, y: 8 + (x & 1) + 8 * (y & 1)

# ------------------------------------------------------------------ Route 5 : bosquets de tourmaline
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
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
    WALLS = (6, 12, 18)                      # rangees des 3 murets de terrasse (voir plus bas)
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
            if any(c[1] in WALLS for c in foot): continue
            ring = {(a + dx, b + dy) for a, b in foot for dx in (-1, 0, 1) for dy in (0, 1)}
            if foot & occ or (ring & occ and rnd.random() < 0.8): continue
            put_tree(x, y, rnd.choice(TR)); occ |= foot; nt += 1
        nc = 0
        for _ in range(400):
            if nc >= 3: break
            x, y = x0 + rnd.randrange(3), rnd.randrange(0, 25)
            foot = {(x + i, y + j) for i in (0, 1) for j in (0, 1)}
            if foot & occ or any(c[1] in WALLS for c in foot): continue
            put_cluster(x, y, rnd.choice(CL)); occ |= foot; nc += 1
        free = [(x, y) for y in range(0, 27) for x in range(x0, x0 + 4) if (x, y) not in occ and y not in WALLS]; rnd.shuffle(free); ns = 0
        for c in free:
            if ns >= 5: break
            put_shard(c); occ.add(c); ns += 1
        for c in [c for c in free if c not in occ][:12]: g[c[1] * w + c[0]] = 0x3000 | 4          # fleurs
        print('bande x%d : %d arbres, %d amas, %d eclats' % (x0, nt, nc, ns))
    # 2) couloir central (x 20..27, y 0..27) : plus de rebords a sauter (rangees de 135), un chemin de terre SINUEUX de Azuria (22..25, 0) a la pension puis au sud, herbes hautes par bouquets
    SANDPAL = [(115, 205, 164), (222, 197, 139), (238, 230, 139), (213, 189, 106), (189, 230, 164), (190, 160, 84), (238, 214, 160), (176, 150, 84), (206, 176, 196), (156, 116, 146), (180, 140, 168), (142, 102, 130), (106, 72, 98), (74, 50, 72), (96, 170, 132), (0, 0, 255)]
    writepal(R.D + 'palettes/09.pal', SANDPAL)
    def dquarter(q, ah, av, dg, var):        # un quart (8x8) de terre : depend seulement des 2 voisines cardinales adjacentes et de la diagonale (autotuile a 5 cas par quart)
        r = random.Random(900 + q * 101 + var * 17 + (ah * 4 + av * 2 + dg) * 13); out = []
        for j in range(8):
            for i in range(8):
                cx_, cy_ = (i if q % 2 == 0 else 7 - i) + (0 if True else 0), (j if q < 2 else 7 - j)
                u = r.random(); c = 1
                if u < 0.10: c = 2
                elif u < 0.19: c = 3
                elif u < 0.215: c = 5
                d = 99.0
                if not ah: d = min(d, cx_)
                if not av: d = min(d, cy_)
                if not ah and not av and cx_ < 4 and cy_ < 4: d = min(d, 4.2 - math.hypot(4 - cx_, 4 - cy_))
                elif ah and av and not dg: d = min(d, math.hypot(cx_ + 0.5, cy_ + 0.5) - 3.2)
                if d < 0.9: c = 0
                elif d < 1.9: c = 4 if r.random() < 0.55 else (0 if r.random() < 0.2 else c)
                elif d < 2.6 and r.random() < 0.3: c = 3
                out.append(c)
        return out
    def put_dirt(c, mask, var):
        N, E, S, W, NE, SE, SW, NW = mask; ents = []
        for q, (ah, av, dg) in enumerate(((W, N, NW), (E, N, NE), (W, S, SW), (E, S, SE))):
            vv = var if (ah and av and dg) else 0
            ents.append((640 + R.NTL + R.tile(dquarter(q, ah, av, dg if (ah and av) else 0, vv))) | (9 << 12))
        g[c[1] * w + c[0]] = 0x3000 | R.meta(ents, grassid(*c), 0x20000000)
    for y in range(0, 21):
        for x in range(20, 28): g[y * w + x] = 0x3000 | grassid(x, y)
    for y in range(0, 27):
        for x in (19, 28): g[y * w + x] = 0x3000 | grassid(x, y)          # barrieres interieures supprimees : une seule grande prairie (reste les barrieres de bord, x 14 et 33)
    for x in range(15, 33):
        if g[34 * w + x] & 0x3ff == 231: g[34 * w + x] = 0x3000 | grassid(x, 34)         # barriere du bas supprimee
    g[34 * w + 14] = g[33 * w + 14]; g[34 * w + 33] = g[33 * w + 33]
    for x in range(19, 29): g[27 * w + x] = 0x3000 | grassid(x, 27)       # rebord sud de la pension supprime
    for c in ((20, 23), (20, 24), (20, 25), (26, 23), (26, 24), (26, 25), (27, 23), (27, 24), (27, 25)): g[c[1] * w + c[0]] &= 0x3fff & ~0xc00         # liseres de pelouse praticables
    path = set()
    for x in range(22, 26): path.add((x, 0))
    for y in range(1, 20):
        cx = 23.5 + 3.0 * math.sin(y / 3.4 + 0.4); x0 = int(math.floor(cx - 1.0)); wd = 2 if y in (8, 9, 16) else 3
        for x in range(x0, x0 + wd): path.add((max(20, min(27, x)), y))
    for x in range(20, 25): path.add((x, 20))
    for y in range(20, 27): path.add((20, y))
    for x in range(20, 25): path.add((x, 26))
    for c in ((23, 27), (23, 28), (24, 28), (24, 29), (25, 29)): path.add(c)
    near = lambda c, d: any(max(abs(c[0] - p[0]), abs(c[1] - p[1])) <= d for p in path)
    for c in sorted(path):
        mk = tuple((c[0] + dx, c[1] + dy) in path or ((c[0] + dx, c[1] + dy)[1] < 0) for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)))
        put_dirt(c, mk, (c[0] * 7 + c[1] * 3) % 3)
    # 3 murets de terrasse (la route « monte » vers Azuria : chaque muret = un palier plus haut au nord) ; un escalier de pierre au passage du chemin
    def wquarter(q, ah, var):
        r = random.Random(1300 + q * 31 + ah * 7 + var * 3); out = []
        for j in range(8):
            for i in range(8):
                X, Y = (q % 2) * 8 + i, (q // 2) * 8 + j; dist_end = (X if q % 2 == 0 else 15 - X)
                if Y < 3: c = 0
                elif Y == 3: c = 8
                elif Y == 4: c = 9
                elif Y >= 14: c = 13 if Y == 14 else 14
                else:
                    c = 10 if (Y - 5) % 4 < 2 else 11
                    if (X * 5 + var * 3) % 6 == 0 and r.random() < 0.8: c = 12
                    elif r.random() < 0.12: c = 12
                    elif r.random() < 0.08: c = 8
                if not ah and dist_end < 3 and (Y < 3 + (3 - dist_end) or Y > 13 - (3 - dist_end)): c = 0 if Y < 14 else 14
                out.append(c)
        return out
    def stquarter(q, ah, var):
        out = []
        for j in range(8):
            for i in range(8):
                X, Y = (q % 2) * 8 + i, (q // 2) * 8 + j; b = Y % 4
                c = 8 if b == 0 else (10 if b == 1 else (11 if b == 2 else 12))
                if b == 1 and (X * 3 + (Y // 4) * 5) % 7 == 0: c = 11
                out.append(c)
        return out
    walls = {}
    for yW in WALLS:
        row = sorted(c for c in path if c[1] == yW)
        for (x, y) in row:
            ents = [(640 + R.NTL + R.tile(stquarter(q, 1, 0))) | (9 << 12) for q in range(4)]
            g[y * w + x] = 0x3000 | R.meta(ents, grassid(x, y), 0x20000000)
        for x in range(15, 33):
            if (x, yW) in path: continue
            wl = (x - 1, yW) not in path; wr = (x + 1, yW) not in path          # voisin mur (ou barriere de bord) ?
            ents = [(640 + R.NTL + R.tile(wquarter(q, wl if q % 2 == 0 else wr, (x + yW) % 2))) | (9 << 12) for q in range(4)]
            g[yW * w + x] = 0x3400 | R.meta(ents, grassid(x, yW), 0)
            walls[(x, yW)] = 1
    # herbes hautes : bouquets de part et d'autre du chemin
    tall = set(); free_c = [(x, y) for y in range(3, 21) for x in range(19, 29) if not near((x, y), 1) and y not in WALLS]
    for _ in range(9):
        cx_, cy_ = rnd.choice(free_c); rad = rnd.choice((1.6, 2.0, 2.4))
        for (x, y) in free_c:
            if math.hypot(x - cx_, (y - cy_) * 1.2) <= rad + rnd.random() * 0.5: tall.add((x, y))
    for (x, y) in tall: g[y * w + x] = 0x3000 | 13
    occ2 = set(path) | tall
    for (x, y) in sorted(path):
        pass
    nt2 = 0; trees_c = []
    for _ in range(300):
        if nt2 >= 4: break
        x, y = rnd.randrange(20, 27), rnd.randrange(4, 19)
        foot = {(x + i, y + j) for i in (0, 1) for j in (-1, 0, 1)}
        if any(c in occ2 or near(c, 0) for c in foot) or any(not (20 <= c[0] <= 27) for c in foot) or not spaced((x, y), trees_c, 4): continue
        put_tree(x, y, rnd.choice(TR)); occ2 |= foot; trees_c.append((x, y)); nt2 += 1
    fl = [c for c in free_c if c not in occ2]; rnd.shuffle(fl)
    for c in fl[:3]: g[c[1] * w + c[0]] = 0x3400 | R.meta(SH, grassid(*c))
    for c in fl[3:17]: g[c[1] * w + c[0]] = 0x3000 | 4
    print('couloir : chemin %d cases, %d cases d herbe haute, %d arbres' % (len(path), len(tall), nt2))
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
    print('Route5 : %d grands arbres + %d eclats pres de la pension, +%d metatuiles (%d/384)' % (ntr, ns, n_new, R.n0 + n_new))

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
