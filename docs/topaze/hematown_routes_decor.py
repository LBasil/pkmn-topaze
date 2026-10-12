# ROUTES 5 / 6 / 7 (voisines de Hematown) v2 : DECOR (apres hematown_routes.py, apres apatia_town.py et celadopole_town.py qui exportent leurs ids de decor).
#   Route 5 (Tourmalia)   : la foret d'arbres FR (grille reguliere de 2x2) est decoupee par des clairieres / baies irregulieres (herbe) ou se tient parfois un arbre isole decale de la grille.
#   Route 6 (Apatia)     : nids de dragon, restes (cotes, plumes, griffes) et cristaux d'apatite sur l'herbe (decor d'Apatia, apatia_art_ids.json).
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

# ------------------------------------------------------------------ Route 6 : nids de dragon et restes
def route6():
    A = json.load(open('docs/topaze/apatia_art_ids.json'))
    w, h, g, mj = load('Route6'); B = Board(w, h, g, mj); rnd = random.Random(606)
    cand = B.cands(); rnd.shuffle(cand); placed = []; cnt = collections.Counter()
    plan = [('nest', 4, 5), ('cry', 6, 4), ('rib', 3, 5), ('feather', 4, 4), ('talon', 4, 4)]
    for kind, n, dist in plan:
        for c in cand:
            if cnt[kind] >= n: break
            if not spaced(c, placed, 2): continue
            b = B.base_of(c); key = {'nest': 'nest_%d', 'feather': 'feather_%d'}.get(kind)
            key = key % b if key else '%s_%d_%d' % (kind, rnd.randrange(3 if kind == 'cry' else 2), b)
            if B.put({c: 0x400 | A[key]}): cnt[kind] += 1; placed.append(c)
    save('Route6', w, h, B.g); print('Route6 : %d candidats' % len(cand), dict(cnt))

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

# ------------------------------------------------------------------ Route 5 : clairieres dans la foret
def route5():
    w, h, g, mj = load('Route5'); rnd = random.Random(505)
    TOP, BOT = {20, 21, 22, 23}, {28, 29, 30, 31}
    ident = lambda x, y: g[y * w + x] & 0x3ff
    def tree_at(x, y): return ident(x, y) in TOP and ident(x + 1, y) in TOP and ident(x, y + 1) in BOT and ident(x + 1, y + 1) in BOT and all(g[(y + j) * w + x + i] & 0xc00 for i in (0, 1) for j in (0, 1))
    blocks = {(x, y) for y in range(1, 38, 2) for x in list(range(0, 14, 2)) + list(range(34, 48, 2)) if tree_at(x, y)}
    inner = {b for b in blocks if 2 <= b[0] <= 12 or 34 <= b[0] <= 44}
    inner = {b for b in inner if 3 <= b[1] <= 35}
    used = set(); clearings = []
    seeds = sorted(inner); rnd.shuffle(seeds)
    for s in seeds:
        if len(clearings) >= 9: break
        if any(abs(s[0] - u[0]) <= 8 and abs(s[1] - u[1]) <= 8 for u in used): continue
        cl = {s}; want = rnd.choice((4, 5, 6, 7))
        while len(cl) < want:
            b = rnd.choice(sorted(cl)); d = rnd.choice(((2, 0), (-2, 0), (0, 2), (0, -2)))
            nb = (b[0] + d[0], b[1] + d[1])
            if nb in inner and nb not in cl: cl.add(nb)
            elif rnd.random() < 0.2: break
        clearings.append(cl); used |= cl
    ntree = 0
    for cl in clearings:
        cells = set()
        for (x, y) in cl:
            for i in (0, 1):
                for j in (0, 1): cells.add((x + i, y + j))
        for (x, y) in cells: g[y * w + x] = 0x3000 | (8 + (x & 1) + 8 * (y & 1))
        wins = [(x, y) for (x, y) in sorted(cells) if all((x + i, y + j) in cells for i in (0, 1) for j in (0, 1)) and (x & 1 or not y & 1)]
        taken = set()
        for _ in range(rnd.choice((1, 2, 2))):
            wins = [(x, y) for (x, y) in wins if not any((x + i, y + j) in taken for i in (0, 1) for j in (0, 1))]
            if not wins: break
            x, y = rnd.choice(wins)
            for (i, j, m) in ((0, 0, 20), (1, 0, 21), (0, 1, 28), (1, 1, 29)): g[(y + j) * w + x + i] = 0x400 | m; taken.add((x + i, y + j))
            ntree += 1
    save('Route5', w, h, g)
    B = Board(w, h, g, mj); assert B.base == Board(w, h, list(struct.unpack('<%dH' % (w * h), open(SRC + 'r5_orig.bin', 'rb').read())), mj).base
    print('Route5 : %d clairieres (%d blocs de 2x2 retires), %d arbres isoles' % (len(clearings), sum(len(c) for c in clearings), ntree))

route5(); route6(); route7()
