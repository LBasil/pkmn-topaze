# APATIA (ex-Vermilion / Carmin, LAYOUT_VERMILION_CITY 48x40) : le port du coucher de soleil, 10 ans apres l'aura (arene de HERA, Dragon/Vol, badge Apatite).
# On GARDE la mer, la cote, le ponton, les 7 batiments a interieur et leurs portes (positions d'origine) ; on refait tout le reste : batiments decoratifs supprimes,
# haies/clotures/terrain vague remplaces par des rues sinueuses, une carriere d'apatite, des forets de pins FR et des cristaux d'apatite (bleu-vert, coeur dore).
# Couleurs : herbe or ambre, sable peche, pins vert-bleu, mer indigo. Tilesets propres (copies de General + VermilionCity, eau animee conservee).
# Idempotent : part de route21_src/verm_orig.bin. Lancer depuis la racine : python3 docs/topaze/apatia_town.py puis apatia_events.py
import struct, json, random, os, shutil, math, colorsys, collections
from PIL import Image, ImageDraw
SP = 'data/tilesets/primary/general/'; SS = 'data/tilesets/secondary/vermilion_city/'
NP = 'data/tilesets/primary/general_apatia/'; NS = 'data/tilesets/secondary/vermilion_apatia/'
W, H = 48, 40
OW, OH = 48, 40
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_sunset(c):
    """APATIA = port au coucher de soleil (arene de HERA, Dragon/Vol ; badge Apatite) : herbes -> or ambre, sable -> peche, pins -> vert-bleu d'apatite (ombre complementaire), mer -> bleu indigo du soir ; rouges/gris inchanges"""
    h, l, s = hls(c)
    if s < 0.08: return c
    if 28 <= h < 70 and s > 0.1: return rgb(24, min(0.9, l * 0.9 + 0.08), min(0.75, s * 0.9 + 0.1))
    if 70 <= h <= 175:
        if l > 0.44: return rgb(44, min(0.78, l * 0.95 + 0.04), min(0.62, s * 0.8 + 0.1))
        return rgb(176, l * 0.95, min(0.7, s * 0.9 + 0.08))
    if 180 <= h <= 250: return rgb(h + 14, l * 0.84, min(0.9, s * 0.72))
    return c
for src, dst in ((SP, NP), (SS, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16):
        pp = readpal(src + 'palettes/%02d.pal' % i); writepal(dst + 'palettes/%02d.pal' % i, [pp[0]] + [tint_sunset(c) for c in pp[1:16]])
pmt = open(SP + 'metatiles.bin', 'rb').read()
smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = list(struct.unpack('<%dI' % (len(smt) // 16), open(NS + 'metatile_attributes.bin', 'rb').read()))
NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
def ents(m): return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
O = struct.unpack('<%dH' % (OW * OH), open('docs/topaze/route21_src/verm_orig.bin', 'rb').read())      # carte d'origine (48x40), conservee pour rendre le script idempotent
def ov(x, y): return O[y * OW + x]
used = set()
for v in set(x & 0x3ff for x in O):
    for e in ents(v): used.add(e >> 12)
ART_PAL = 7; CRY_PAL = 11
assert ART_PAL not in used and CRY_PAL not in used, used
# ------------------------------------------------------------------ bruit (reproductible)
def _h(ix, iy, seed): return random.Random((ix * 73856093) ^ (iy * 19349663) ^ (seed * 83492791)).random()
def vnoise(x, y, seed=1):
    ix, iy = math.floor(x), math.floor(y); fx, fy = x - ix, y - iy
    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b, c, d = _h(ix, iy, seed), _h(ix + 1, iy, seed), _h(ix, iy + 1, seed), _h(ix + 1, iy + 1, seed)
    return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy
# ------------------------------------------------------------------ plan : on part de la carte d'origine, on distingue FIXE (mer, cote, ponton, batiments a interieur, rocher) et LIBRE (herbe, pins, decors a supprimer)
def ov(x, y): return O[y * OW + x]
patt = open(SP + 'metatile_attributes.bin', 'rb').read()
def beh(m):
    a = patt[m * 4:m * 4 + 4] if m < 640 else bytes(satt[m - 640].to_bytes(4, 'little'))
    return struct.unpack('<I', a)[0] & 0x1ff
WATERB = {0x10, 0x11, 0x12, 0x15}
GRASSID = {1, 8, 9, 16, 17}
TREEID = {14, 15, 20, 21, 22, 23, 28, 29, 30, 31, 36, 37, 38, 39}
DECOR = [(18, 3, 4, 4), (25, 3, 5, 4), (30, 6, 12, 1), (25, 0, 1, 3), (31, 17, 10, 1), (41, 6, 1, 10), (41, 16, 7, 2), (32, 8, 7, 7), (25, 9, 4, 4)]      # decor a supprimer : maison sans porte x2, cloture, haie, terrain vague
BUILD = [(8, 3, 5, 4), (13, 3, 5, 4), (11, 14, 5, 5), (18, 14, 4, 4), (27, 14, 4, 4), (11, 21, 7, 5), (27, 21, 4, 5)]                      # batiments a interieur (conserves tels quels)
DOORS = {'house1': [(9, 6)], 'center': [(15, 6)], 'fanclub': [(12, 17)], 'house2': [(19, 17)], 'mart': [(29, 17)], 'house3': [(28, 24)], 'gym': [(14, 25)], 'ship': [(22, 34), (23, 34), (24, 34)]}
def inrect(c, r): return r[0] <= c[0] < r[0] + r[2] and r[1] <= c[1] < r[1] + r[3]
G = {}; OCC = {}; WALK = set(); M = set()
for y in range(H):
    for x in range(W):
        v = ov(x, y); c = (x, y); i = v & 0x3ff
        free = (i in GRASSID or i in TREEID or any(inrect(c, r) for r in DECOR)) and not any(inrect(c, r) for r in BUILD)
        if free: M.add(c)
        else:
            G[c] = v; OCC[c] = 'fix'
            if not (v & 0xc00) and beh(i) not in WATERB: WALK.add(c)
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            c = (x + i, y + j); assert c in M and c not in OCC, ('chevauchement', name, c, OCC.get(c)); OCC[c] = name
def grass(x, y): return 0x3000 | ((9 if y % 2 else 17) if x % 2 else (8 if y % 2 else 16))
for c in M: G[c] = grass(*c)
DOOR = {k: [tuple(c) for c in v] for k, v in DOORS.items()}
EXITS = {'N': [(22, 0), (23, 0), (24, 0)], 'E': [(W - 1, 18), (W - 1, 19), (W - 1, 20)]}
START = (23, 0)
for c in sum(EXITS.values(), []): assert c in M, c
# ------------------------------------------------------------------ voies : splines lissees, disques empiles
WAY = set()
def catmull(pts, n=14):
    P = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2 + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)))
    out.append(P[-2]); return out
_h = lambda ix, iy, seed: random.Random((ix * 73856093) ^ (iy * 19349663) ^ (seed * 83492791)).random()
def vnoise(x, y, seed=1):
    ix, iy = math.floor(x), math.floor(y); fx, fy = x - ix, y - iy
    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b, c, d = _h(ix, iy, seed), _h(ix + 1, iy, seed), _h(ix, iy + 1, seed), _h(ix + 1, iy + 1, seed)
    return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy
def stamp(cx, cy, r):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if (x, y) in M and (x - cx) ** 2 + (y - cy) ** 2 <= r * r and (x, y) not in OCC: WAY.add((x, y))
def road(pts, r, wob=None):
    Pn = catmull(pts); n = len(Pn)
    for i, (cx, cy) in enumerate(Pn):
        if wob:
            ax, ay, sd = wob; fe = min(1.0, i / 10, (n - 1 - i) / 10)
            cx += ax * (vnoise(i * .05, 3.3, sd) - .5) * 2 * fe; cy += ay * (vnoise(i * .05, 7.7, sd) - .5) * 2 * fe
        stamp(cx, cy, r)
ROADS = [
    ([(23, 0), (23, 4), (22.6, 8), (23.6, 12), (23.2, 16), (24, 19.2)], 0.95, (0.9, 0, 31)),                                   # avenue du nord (Route 6) -> grande rue
    ([(22.6, 7.4), (19, 7.3), (15, 7.2), (9.5, 7.2)], 0.9, (0, 0.25, 32)),                                                     # facade des maisons du nord (maison, Centre)
    ([(12, 18.6), (16, 18.3), (19, 18.5), (24, 19.2), (29, 18.5), (33, 19.3), (36, 19.4), (41, 19.1), (47, 19)], 0.92, (0, 0.8, 33)),   # grande rue est-ouest : Fan Club, maison, boutique, pont du port, sortie est
    ([(24, 19.5), (25, 22.5), (25.4, 24.6)], 0.9, (0.4, 0, 34)),                                                              # vers la maison du sud
    ([(23.6, 11.6), (28, 11.3), (31, 11.1), (33.5, 11)], 0.9, (0, 0.5, 35)),                                                  # chemin de la carriere
]
for pts, r, wob in ROADS: road(pts, r, wob)
LOT = {(x, y) for y in range(7, 16) for x in range(29, 41) if ((x - 36.5) / 3.0) ** 2 + ((y - 11) / 2.2) ** 2 <= 1 + 0.3 * (vnoise(x * .6, y * .6, 41) - .5)}   # carriere d'apatite (ex-terrain vague)
for c in LOT:
    if c in M and c not in OCC and ((c[0] - 35.5) / 2.7) ** 2 + ((c[1] - 11.2) / 1.8) ** 2 <= 1.1: WAY.add(c)
for k, ds in DOOR.items():                                          # parvis devant chaque porte
    for (x, y) in ds:
        for b in (1, 2):
            for a in (-1, 0, 1):
                c = (x + a, y + b)
                if c in M and c not in OCC: WAY.add(c)
for c in sum(EXITS.values(), []): WAY.add(c)
WAY -= {c for c in WAY if c in OCC}
print('voies', len(WAY), 'cases')
BLK = {}; FLW = set()
FIXSOLID = {c for c in OCC if OCC[c] == 'fix' and c not in WALK and beh(G[c] & 0x3ff) not in WATERB}
UW, UH = W // 2, H // 2
def ucells(ux, uy): return [(2 * ux + i, 2 * uy + j) for j in (0, 1) for i in (0, 1)]
BIGS = [(19, 4), (38, 13), (32, 13), (44, 14)]                 # grandes formations d'apatite 2x2 (jardin de roche, carriere x2, lisiere est)
for (mx, my) in BIGS:
    for c in [(mx + i, my + j) for j in (0, 1) for i in (0, 1)]: WAY.discard(c)
KEEP = set(WAY)
for ds in DOOR.values():
    for (x, y) in ds: KEEP.add((x, y + 1))
# ------------------------------------------------------------------ forets : unites 2x2 (familles de tuiles FR)
GROVES = [(44.5, 16.4, 3.4, 1.0), (31, 14.5, 1.3, 1.1), (39.5, 6.8, 1.6, 1.2), (27, 8.5, 1.2, 1.3), (16.5, 12.5, 1.2, 1.0), (30, 24.0, 0.8, 1.0), (20, 12.5, 1.4, 1.2), (37.5, 18.2, 0.9, 0.5), (28.5, 13.8, 1.7, 1.2), (29.5, 8.2, 1.2, 1.1), (41.5, 12.5, 1.1, 1.3), (26, 16.2, 0.9, 0.6), (32, 16.2, 0.9, 0.5), (37.5, 9.5, 5.2, 4.6), (42, 14, 1.5, 1.2), (36.5, 15.2, 4.8, 2.6), (31, 12.5, 0.8, 1.6)]
TU = set()
def trunk_ok(ux, uy):
    for i in (0, 1):
        c = (2 * ux + i, 2 * uy + 2)
        if c[1] < H and ((c in OCC and OCC[c] != 'pin') or c in BLK): return False
    return True
def unit_ok(ux, uy): return all(c in M and c not in OCC and c not in KEEP and c not in BLK and c not in LOT for c in ucells(ux, uy)) and trunk_ok(ux, uy)
for uy in range(UH):
    for ux in range(UW):
        d = min(uy, UW - 1 - ux)
        T = 1.0 + 2.5 * vnoise(ux * .42, uy * .42, 11)
        inside = d < T and ux >= 12
        cx, cy = 2 * ux + 1, 2 * uy + 1
        for (gx, gy, rx, ry) in GROVES:
            if ((cx - gx) / rx) ** 2 + ((cy - gy) / ry) ** 2 < 0.75 + 0.6 * vnoise(ux * .9, uy * .9, 5): inside = True
        if inside and unit_ok(ux, uy): TU.add((ux, uy))
FORCED = set()
def void_fill():
    for _ in range(80):
        TUC = {c for u in TU for c in ucells(*u)}
        free = lambda c: c in M and c not in OCC and c not in KEEP and c not in BLK and c not in WAY and c not in LOT and c not in TUC and c not in VOIDSKIP
        spot = None
        for y in range(H - 4):
            for x in range(W - 4):
                if all(free((x + i, y + j)) for j in range(5) for i in range(5)): spot = (x, y); break
            if spot: break
        if not spot: break
        added = False
        for (ux, uy) in sorted({((spot[0] + i) // 2, (spot[1] + j) // 2) for j in range(5) for i in range(5)}):
            if unit_ok(ux, uy) and (ux, uy) not in TU: TU.add((ux, uy)); added = True
        if not added: VOIDSKIP.add((spot[0] + 2, spot[1] + 2))
VOIDSKIP = set()
def prune():
    ch = True
    while ch:
        ch = False
        for (ux, uy) in sorted(TU):
            if (ux, uy) in FORCED: continue
            n = sum(1 for q in ((ux - 1, uy), (ux + 1, uy), (ux, uy - 1), (ux, uy + 1)) if q in TU or not (0 <= q[0] < UW and 0 <= q[1] < UH))
            if n < 2: TU.discard((ux, uy)); ch = True
prune(); void_fill(); prune()
for (ux, uy) in TU:
    for c in ucells(ux, uy): OCC[c] = 'pin'
print('unites d arbres', len(TU))
# ------------------------------------------------------------------ accessibilite
def blocked(c): return (c in OCC and c not in WALK) or c in BLK or not (0 <= c[0] < W and 0 <= c[1] < H)
def reach(extra=frozenset(), start=START):
    seen = {start}; q = collections.deque(seen)
    while q:
        c = q.popleft()
        for d_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if n in seen or blocked(n) or n in extra: continue
            seen.add(n); q.append(n)
    return seen
GATE = (19, 24)                                                    # arbre a couper (d'origine) : seul passage vers le parvis de l'arene
NEED = {(x, y + 1) for k, ds in DOOR.items() if k not in ('gym', 'ship') for (x, y) in ds} | {(x, 33) for (x, y) in DOOR['ship']} | set(EXITS['N']) | set(EXITS['E']) | {(36, 20)}
NEED_GATE = {GATE}
r0 = reach()
assert NEED <= r0, ('acces manquants', sorted(NEED - r0))
assert GATE in r0, 'arbre a couper inaccessible'
assert (14, 26) in reach(start=GATE), 'parvis de l arene inaccessible apres coupe'
assert (14, 26) not in reach(extra={GATE}), 'parvis de l arene accessible sans couper'
# ------------------------------------------------------------------ cristaux d'apatite, buissons, fleurs
def can_block(c, extra=()):
    if c in OCC or c in BLK or c in KEEP or c in WAY: return False
    return NEED | NEED_GATE <= reach(set(extra) | {c})
def near(c, S, r=1): return any((c[0] + a, c[1] + b) in S for a in range(-r, r + 1) for b in range(-r, r + 1))
PIN = lambda: {k for k, v in OCC.items() if v == 'pin'}
for (mx, my) in BIGS:
    cells = [(mx + i, my + j) for j in (0, 1) for i in (0, 1)]
    if all(c in M and c not in OCC and c not in BLK for c in cells) and NEED | NEED_GATE <= reach(set(cells)):
        for (i, j), c in zip(((0, 0), (1, 0), (0, 1), (1, 1)), cells): BLK[c] = ('big', i, j)
        print('formation', (mx, my))
rc = random.Random(1701)
cands = [(x, y) for y in range(1, H - 1) for x in range(1, W - 1) if (x, y) in M and (x, y) not in OCC and (x, y) not in WAY and (x, y) not in BLK and (x, y) not in KEEP]
rc.shuffle(cands); ncry = 0; pins = PIN()
for c in cands:
    if ncry >= 34: break
    if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q, v in BLK.items() if v[0] in ('cry', 'big')): continue
    if not (near(c, WAY, 2) or near(c, pins, 1) or near(c, LOT, 2)): continue
    if can_block(c): BLK[c] = ('cry', rc.randrange(3)); ncry += 1
qc = [c for c in cands if c not in BLK and near(c, LOT, 1) and c not in LOT]
rc.shuffle(qc); nq = 0
for c in qc:
    if nq >= 9: break
    if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 2 for q, v in BLK.items() if v[0] in ('cry', 'big')): continue
    if can_block(c): BLK[c] = ('cry', rc.randrange(3)); nq += 1
print('cristaux', ncry, 'carriere', nq)
rb = random.Random(1702); nb = 0; rb.shuffle(cands)
for c in cands:
    if nb >= 14: break
    if c in BLK or not near(c, pins, 1) or near(c, WAY, 1) or near(c, {q for q, v in BLK.items() if v[0] == 'bush'}, 1): continue
    if can_block(c): BLK[c] = ('bush', 0); nb += 1
print('buissons', nb)
rf = random.Random(1703)
fc = [c for c in cands if c not in BLK and c not in OCC and c not in WAY]
rf.shuffle(fc); nf = 0; blds = {k for k, v in OCC.items() if v not in ('pin', 'trunk')}
for c in fc:
    if nf >= 30: break
    if near(c, WAY, 1) or near(c, blds, 1):
        FLW.add(c); nf += 1
        for d_ in rf.sample([(1, 0), (0, 1), (1, 1), (-1, 0)], rf.randrange(0, 3)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if n in fc and n not in BLK and n not in OCC and n not in WAY: FLW.add(n)
print('fleurs', len(FLW))
rr = reach()                                                         # poches libres inaccessibles : comblees de buissons (hors parvis de l'arene derriere l'arbre)
FOREC = reach(start=GATE)
PK = {(x, y) for y in range(H) for x in range(W) if (x, y) in M and not blocked((x, y))} - rr - FOREC
for (ux, uy) in sorted({(c[0] // 2, c[1] // 2) for c in PK}):                  # poches inaccessibles : d'abord des unites d'arbres entieres, puis des buissons
    if all(c in PK for c in ucells(ux, uy)):
        for c in ucells(ux, uy): OCC[c] = 'pin'; PK.discard(c)
        TU.add((ux, uy))
for c in sorted(PK): BLK[c] = ('bush', 0)
assert NEED <= reach()
# ------------------------------------------------------------------ panneaux et PNJ
SIGN = {}
def near4(c, S): return any((c[0] + a, c[1] + b) in S for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
def place_sign(name, want):
    best = None
    for (x, y) in sorted(M):
        c = (x, y)
        if blocked(c) or c in WAY or c in KEEP or c in FLW or not near4(c, WAY): continue
        if not NEED | NEED_GATE <= reach({c}): continue
        d_ = abs(x - want[0]) + abs(y - want[1])
        if best is None or d_ < best[0]: best = (d_, c)
    c = best[1]; BLK[c] = ('sign', 0); SIGN[name] = list(c)
for nm, w_ in (('city', (26, 8)), ('harbor', (34, 18)), ('notice', (45, 18))): place_sign(nm, w_)
NPC = {}; OBJ_CELLS = {GATE}
def place_npc(name, want, rowfree=0, region=None):
    r = reach(); best = None
    for c in r:
        if c in BLK or (c in OCC and c not in WALK) or c in OBJ_CELLS: continue
        if region is not None and c not in region: continue
        cells = [(c[0] + i, c[1]) for i in range(-rowfree, rowfree + 1)]
        if not all(q in r and q not in OBJ_CELLS and q not in BLK for q in cells): continue
        d_ = abs(c[0] - want[0]) + abs(c[1] - want[1])
        if best is None or d_ < best[0]: best = (d_, c)
    c = best[1]; NPC[name] = list(c); OBJ_CELLS.add(c)
place_npc('woman', (21, 11)); place_npc('oldman1', (17, 9)); place_npc('oldman2', (36, 9)); place_npc('aide', (26, 7))
place_npc('machop', (34, 12), region=LOT)
place_npc('sailor', (31, 30)); place_npc('ferry', (24, 33))
NPC['tree'] = list(GATE)
json.dump(NPC, open('/tmp/apatia_npc.json', 'w')); json.dump(SIGN, open('/tmp/apatia_signs.json', 'w'))
json.dump({k: [list(c) for c in v] for k, v in DOOR.items()}, open('/tmp/apatia_doors.json', 'w'))
json.dump({'exitN': [list(c) for c in EXITS['N']], 'exitE': [list(c) for c in EXITS['E']]}, open('/tmp/apatia_misc.json', 'w'))
print('PNJ', NPC); print('panneaux', SIGN)
# ------------------------------------------------------------------ arbres FR : retuilage (haut/bas/tronc/bords), meme logique que Spinellia (validee)
P = {c for c, n in OCC.items() if n == 'pin'}
def is_pine(c): return c in P or not (0 <= c[0] < W and 0 <= c[1] < H)
TRUNK = {}
for (x, y) in sorted(P):
    if y % 2 == 1 and not is_pine((x, y + 1)):
        c = (x, y + 1)
        if c in OCC or c in WAY or c in KEEP or c in BLK or c in FLW or c in TRUNK: continue
        OCC[c] = 'trunk'
        if NEED | NEED_GATE <= reach(): TRUNK[c] = 1
        else: OCC.pop(c)
P2 = P | set(TRUNK)
for (x, y) in P2:
    role = 'K' if (x, y) in TRUNK else ('T' if y % 2 == 0 else 'B')
    left = (x % 2 == 0) and not ((x - 1, y) in P2 or not (0 <= x - 1 < W))
    right = (x % 2 == 1) and not ((x + 1, y) in P2 or not (0 <= x + 1 < W))
    base = {'T': (0x14, 0x15, 0x16, 0x17), 'B': (0x1c, 0x1d, 0x1e, 0x1f), 'K': (0x24, 0x25, 0x26, 0x27)}[role]
    if role == 'T' and (x, y - 1) not in P2 and 0 <= y - 1: base = (0x0e, 0x0f, 0x0e, 0x0f)
    G[(x, y)] = 0x400 | (base[2] if left else base[3] if right else base[x % 2])
print('troncs', len(TRUNK))
assert NEED | NEED_GATE <= reach(), 'acces perdu apres les troncs'
# ------------------------------------------------------------------ art procedural
PAL = [(0, 0, 0), (96, 56, 64), (238, 208, 178), (222, 184, 152), (186, 142, 118), (252, 234, 212), (150, 96, 84), (200, 150, 120), (226, 180, 140), (140, 100, 96),
       (110, 74, 80), (178, 130, 112), (246, 220, 192), (206, 168, 140), (160, 112, 98), (88, 52, 60)]
PAL_C = [(0, 0, 0), (14, 62, 74), (34, 150, 160), (84, 212, 200), (170, 246, 232), (255, 255, 255), (255, 236, 150), (120, 86, 14), (190, 140, 30),
         (240, 190, 60), (255, 232, 140), (30, 54, 70), (232, 120, 100), (176, 190, 196), (96, 112, 120), (255, 246, 200)]   # apatite : bleu-vert, coeur dore (7-10)
def newimg(w, h): return Image.new('P', (w, h), 0)
def prism(d, x, base, w, h):
    half = max(2, w // 2); top = base - h; sh = top + max(3, half + 1)
    d.polygon([(x - half, base), (x - half, sh), (x, top), (x + half, sh), (x + half, base)], fill=3, outline=1)
    d.polygon([(x - half + 1, base - 1), (x - half + 1, sh + 1), (x, top + 2), (x, base - 1)], fill=4)
    d.polygon([(x + 1, top + 2), (x + half - 1, sh + 1), (x + half - 1, base - 1), (x + 1, base - 1)], fill=2)
    if half >= 3 and h >= 9:
        hc = max(1, half // 2); ct = base - max(5, int(h * 0.62)); cs = ct + max(2, hc)
        d.polygon([(x - hc, base - 2), (x - hc, cs), (x, ct), (x + hc, cs), (x + hc, base - 2)], fill=8)
        d.polygon([(x - hc, base - 2), (x - hc, cs + 1), (x, ct + 2), (x, base - 2)], fill=9)
        d.polygon([(x + 1, ct + 2), (x + hc, cs + 1), (x + hc, base - 2), (x + 1, base - 2)], fill=7)
        d.point((x - 1, ct + 3), fill=10)
    d.point((x - half + 1, sh + 1), fill=5); d.point((x - 1, top + 3), fill=6)
def small(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((1, 12, 15, 16), fill=11)
    if var == 0: prism(d, 4, 14, 5, 9); prism(d, 9, 15, 7, 14); prism(d, 13, 14, 4, 7)
    elif var == 1: prism(d, 6, 15, 6, 11); prism(d, 12, 14, 5, 8); d.rectangle((1, 13, 3, 14), fill=13); d.point((2, 12), fill=14)
    else: prism(d, 8, 15, 8, 14); d.rectangle((2, 13, 4, 14), fill=13); d.rectangle((12, 12, 14, 14), fill=13); d.point((13, 11), fill=14)
    return im
def formation():
    """grande formation d'apatite 2x2 (32x32) : socle de roche, geodes, 5 prismes"""
    im = newimg(32, 32); d = ImageDraw.Draw(im)
    d.ellipse((1, 24, 31, 32), fill=11)
    d.rectangle((3, 26, 28, 30), fill=14, outline=1); d.line([(4, 27), (27, 27)], fill=13); d.rectangle((4, 29, 27, 29), fill=11)
    prism(d, 7, 27, 7, 12); prism(d, 25, 27, 6, 10); prism(d, 12, 28, 8, 17); prism(d, 20, 28, 8, 20); prism(d, 16, 29, 10, 26)
    for (x, y) in ((15, 8), (19, 13), (10, 18), (22, 17)): d.point((x, y), fill=6)
    return im
def path_tile(mask, var=0):
    """pave de 16x16 : dalles en appareil decale ; mask = (N,E,S,W) True si la voisine est aussi un pave (ou un batiment) ; bord erode (la nature reprend) ;
    var 1/2 : touffes d'herbe dans les joints (10 ans d'abandon)"""
    im = newimg(16, 16); px = im.load(); seed = 700 + var * 31 + sum((1 << i) for i, m in enumerate(mask) if m) * 7
    r = random.Random(seed)
    slab = {(0, 0): 2, (1, 0): 3, (0, 1): 3, (1, 1): 2}
    for y in range(16):
        for x in range(16):
            band = y // 8; sx = (x + (0 if band == 0 else 8)) // 8 % 2
            c = slab[(sx, band)]
            if y % 8 == 7: c = 4
            elif (x + (0 if band == 0 else 8)) % 8 == 7: c = 4
            elif r.random() < .06: c = 5
            elif r.random() < .05: c = 4
            px[x, y] = c
    for y in range(16):
        for x in range(16):
            d = 99
            if not mask[0]: d = min(d, y)
            if not mask[2]: d = min(d, 15 - y)
            if not mask[3]: d = min(d, x)
            if not mask[1]: d = min(d, 15 - x)
            for (ca, cb, dx_, dy_) in ((0, 3, x, y), (0, 1, 15 - x, y), (2, 3, x, 15 - y), (1, 2, 15 - x, 15 - y)):
                if not mask[ca] and not mask[cb]:
                    dd = math.hypot(max(0, 3 - dx_), max(0, 3 - dy_)); d = min(d, int(dd) if dd > 0 else d)
            if d < 1:
                px[x, y] = 0 if r.random() < .75 else 4
            elif d == 1: px[x, y] = 0 if r.random() < .22 else (4 if r.random() < .6 else px[x, y])
            elif d == 2 and r.random() < .18: px[x, y] = 6 if r.random() < .5 else 7
    if var:
        for _ in range(3 if var == 1 else 5):
            tx, ty = r.randrange(2, 14), r.randrange(3, 14)
            for (a, b, c) in ((0, 0, 6), (0, -1, 7), (-1, 0, 7), (1, 0, 7), (0, -2, 8), (-1, 1, 7), (1, 1, 6)):
                if 0 <= tx + a < 16 and 0 <= ty + b < 16: px[tx + a, ty + b] = c
    return im
def nonempty(im, box): return sum(1 for q in im.crop(box).getdata() if q)
# controle « sprites entiers » : chaque quart rempli (haut ET bas), pas d'image vide
for v in range(3):
    s_ = small(v); assert nonempty(s_, (0, 0, 16, 8)) >= 4 and nonempty(s_, (0, 8, 16, 16)) >= 20, ('cristal incomplet', v)
F_ = formation()
for (i, j) in ((0, 0), (1, 0), (0, 1), (1, 1)): assert nonempty(F_, (i * 16, j * 16, i * 16 + 16, j * 16 + 16)) >= 24, ('formation incomplete', i, j)
NEWT = []; NEWE = []; NEWA = []
def add_tile(t):
    t = tuple(t)
    if t in NEWT: return NEWT.index(t)
    NEWT.append(t); return len(NEWT) - 1
def slice4(im): return [add_tile(list(im.crop(((q % 2) * 8, (q // 2) * 8, (q % 2) * 8 + 8, (q // 2) * 8 + 8)).getdata())) for q in range(4)]
def art_meta(tiles4, base_m, covered, pal='A'):
    e = ents(base_m)[:4] + [(pal, t) for t in tiles4]; a = 0x20000000 if covered else 0
    for k, (e2, a2) in enumerate(zip(NEWE, NEWA)):
        if e2 == e and a2 == a: return 640 + NMT + k
    NEWE.append(e); NEWA.append(a); return 640 + NMT + len(NEWE) - 1
# ---- ecriture de la carte
rv = random.Random(1604); PT = {}; ncell = collections.Counter()
def solid(n): return (n in WAY) or (n in OCC and OCC[n] not in ('pin', 'trunk', 'void', 'fix')) or n in FIXSOLID or not (0 <= n[0] < W and 0 <= n[1] < H)
for c in sorted(WAY):
    if c in OCC and c not in WALK: continue
    mask = tuple(solid((c[0] + dx, c[1] + dy)) for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)))
    var = 0
    if all(mask):
        rr = rv.random(); var = 1 if rr < .13 else (2 if rr < .22 else 0)
    k = (mask, var)
    if k not in PT: PT[k] = slice4(path_tile(mask, var))
    G[c] = 0x3000 | art_meta(PT[k], G[c] & 0x3ff, True)
    ncell[k] += 1
SM = [slice4(small(v)) for v in range(3)]; FM = {}
for (i, j) in ((0, 0), (1, 0), (0, 1), (1, 1)): FM[(i, j)] = slice4(F_.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)))
for c, val in BLK.items():
    if val[0] == 'big': G[c] = 0x400 | art_meta(FM[(val[1], val[2])], G[c] & 0x3ff, False, 'B')
    elif val[0] == 'cry': G[c] = 0x400 | art_meta(SM[val[1]], G[c] & 0x3ff, False, 'B')
    elif val[0] == 'bush': G[c] = 0x400 | 5
    elif val[0] == 'sign': G[c] = 0x400 | 2
for c in FLW: G[c] = 0x3000 | 4
assert NMT + len(NEWE) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(NEWE), NTL + len(NEWT))
print('metatuiles', NMT + len(NEWE), '/384  tuiles', NTL + len(NEWT), '/384  variantes de pave', len(PT))
NEWE = [[((640 + NTL + q[1]) | ((CRY_PAL if q[0] == 'B' else ART_PAL) << 12)) if isinstance(q, tuple) else q for q in e] for e in NEWE]
smt += b''.join(struct.pack('<8H', *e) for e in NEWE); satt += NEWA
open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in satt))
rows = (NTL + len(NEWT) + 15) // 16
out = Image.new('P', (128, rows * 8), 0); out.putpalette(simg.getpalette()); out.paste(simg, (0, 0))
for n, t in enumerate(NEWT):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
out.save(NS + 'tiles.png'); writepal(NS + 'palettes/%02d.pal' % ART_PAL, PAL); writepal(NS + 'palettes/%02d.pal' % CRY_PAL, PAL_C)
open('data/layouts/VermilionCity/map.bin', 'wb').write(struct.pack('<%dH' % (W * H), *[G[(x, y)] for y in range(H) for x in range(W)]))
open('data/layouts/VermilionCity/border.bin', 'wb').write(struct.pack('<4H', 0x414, 0x415, 0x41c, 0x41d))      # bordure hors carte : foret d'arbres FR (phase haut = lignes paires)
# ---- layouts.json + en-tetes C (idempotents)
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
cn = 'Apatia'
add('src/data/tilesets/graphics.h', 'GeneralApatia',
    '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
    '\nconst u32 gTilesetTiles_Vermilion%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Vermilion%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
add('src/data/tilesets/metatiles.h', 'GeneralApatia',
    '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
    '\nconst u16 gMetatiles_Vermilion%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Vermilion%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
tm = '''
const struct Tileset gTileset_%s%s =
{
    .isCompressed = TRUE,
    .isSecondary = %s,
    .tiles = gTilesetTiles_%s%s,
    .palettes = gTilesetPalettes_%s%s,
    .metatiles = gMetatiles_%s%s,
    .metatileAttributes = gMetatileAttributes_%s%s,
    .callback = %s,
};
'''
add('src/data/tilesets/headers.h', 'GeneralApatia',
    tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Vermilion', cn, 'TRUE', 'Vermilion', cn, 'Vermilion', cn, 'Vermilion', cn, 'Vermilion', cn, 'NULL'))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_VERMILION_CITY': l.update(width=W, height=H, primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Vermilion%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('Apatia ecrite')
