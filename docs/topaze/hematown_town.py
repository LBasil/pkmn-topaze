# HEMATOWN (ex-Saffron / Safrania, LAYOUT_SAFFRON_CITY 66x55) : la ville que le soleil a oubliee, 10 ans apres l'aura (arene de NOX, Tenebre, badge Hematite). Option A retenue par Basil.
# Lore : la TEAM ONYBRIS tient la ville ; la cuvette est fermee par des falaises d'hematite et une canopee de pins noirs : le soleil n'y entre jamais (meteo WEATHER_SHADE).
# Les 9 batiments qui ont un interieur (Tour Sylphe, Centre, Boutique, Fan Club, maison, maison du double, dojo, arene, maison de Mr Psychic) sont recopies de la carte FireRed puis REPLACES
# dans une composition organique ; les 4 portails de la ville (N, S, O, E : interieurs-tunnels vers les Routes 5, 6, 7, 8) restent a leur place ; les ~25 batiments decoratifs sans porte
# disparaissent (la nature et les ruines ont repris leur place). Tilesets propres `GeneralHematown` / `SaffronHematown` (copies de General + SaffronCity, teinte « ombre », COMPACTES).
# Idempotent : part de route21_src/saf_orig.bin. Lancer depuis la racine : python3 docs/topaze/hematown_town.py puis hematown_events.py
import struct, json, random, os, shutil, math, colorsys, collections, sys
from PIL import Image, ImageDraw
SP = 'data/tilesets/primary/general/'; SS = 'data/tilesets/secondary/saffron_city/'
NP = 'data/tilesets/primary/general_hematown/'; NS = 'data/tilesets/secondary/saffron_hematown/'
W, H = 66, 55
OW, OH = 66, 55
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_shadow(c, pi, prim):
    """HEMATOWN = ville dans l'ombre (arene de NOX, Tenebre ; badge Hematite) : herbes/pins -> bleu-sarcelle de nuit, sable/pave/ocre -> gris-violet, roche (palette primaire 1) -> hematite gris-rouge sombre ;
    verres, eau, Boutique bleue et Centre rouge conserves (assombris), gris legerement refroidis"""
    h, l, s = hls(c)
    if s < 0.08:
        if l < 0.03: return c
        return rgb(236, l * 0.84, 0.07 if l > 0.1 else 0.0)
    if prim and pi == 1 and (h < 30 or h > 330): return rgb(350, l * 0.72, s * 0.5)
    if 28 <= h < 70 and s > 0.1: return rgb(268, l * 0.70, min(0.26, s * 0.40))
    if 70 <= h <= 175:
        if l > 0.44: return rgb(198, l * 0.62, min(0.40, s * 0.65))
        return rgb(214, l * 0.80, min(0.50, s * 0.75))
    if 180 <= h <= 250: return rgb(h, l * 0.86, s * 0.9)
    if 250 < h <= 330: return rgb(h, l * 0.82, s * 0.7)
    return rgb(h, l * 0.92, s * 0.95)
for src, dst, prim in ((SP, NP, True), (SS, NS, False)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16):
        pp = readpal(src + 'palettes/%02d.pal' % i); writepal(dst + 'palettes/%02d.pal' % i, [pp[0]] + [tint_shadow(c, i, prim) for c in pp[1:16]])
pmt = open(SP + 'metatiles.bin', 'rb').read()
smt0 = open(SS + 'metatiles.bin', 'rb').read(); satt0 = list(struct.unpack('<%dI' % (len(smt0) // 16), open(SS + 'metatile_attributes.bin', 'rb').read()))
NMT = len(smt0) // 16; simg = Image.open(SS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
def ents(m): return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else smt0[(m - 640) * 16:(m - 640) * 16 + 16]))
O = struct.unpack('<%dH' % (OW * OH), open('docs/topaze/route21_src/saf_orig.bin', 'rb').read())      # carte d'origine (66x55), conservee pour rendre le script idempotent
def ov(x, y): return O[y * OW + x]
used = set()
for v in set(x & 0x3ff for x in O):
    for e in ents(v): used.add(e >> 12)
ART_PAL = 7; CRY_PAL = 13
assert ART_PAL not in used and CRY_PAL not in used, used
# ------------------------------------------------------------------ bruit (reproductible)
def _h(ix, iy, seed): return random.Random((ix * 73856093) ^ (iy * 19349663) ^ (seed * 83492791)).random()
def vnoise(x, y, seed=1):
    ix, iy = math.floor(x), math.floor(y); fx, fy = x - ix, y - iy
    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b, c, d = _h(ix, iy, seed), _h(ix + 1, iy, seed), _h(ix, iy + 1, seed), _h(ix + 1, iy + 1, seed)
    return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy
# ------------------------------------------------------------------ plan : batiments (chunks d'origine recopies a de nouvelles positions)
CH = {'silph': (29, 16, 9, 15), 'pc': (22, 34, 5, 5), 'mart': (38, 18, 4, 4), 'fan': (46, 18, 4, 4), 'house': (26, 18, 3, 4), 'copy': (21, 10, 4, 5),
      'dojo': (37, 9, 6, 4), 'gym': (43, 8, 7, 5), 'psy': (41, 34, 5, 5)}
POS = {'silph': (29, 17), 'pc': (20, 36), 'mart': (43, 19), 'fan': (49, 15), 'house': (14, 17), 'copy': (19, 8),
       'dojo': (40, 5), 'gym': (47, 4), 'psy': (46, 37)}
DOOR_ORIG = {'silph': (33, 30), 'pc': (24, 38), 'mart': (40, 21), 'fan': (47, 21), 'house': (27, 21), 'copy': (22, 14), 'dojo': (40, 12), 'gym': (46, 12), 'psy': (43, 38)}
GATES = {'gN': (32, 0, 6, 9), 'gS': (32, 45, 6, 10), 'gW': (0, 24, 9, 6), 'gE': (57, 24, 9, 6)}      # portails : restent a leur place d'origine
G = {}; OCC = {}; WALK = set()
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            c = (x + i, y + j)
            assert 0 <= c[0] < W and 0 <= c[1] < H, (name, c)
            assert c not in OCC, ('chevauchement', name, OCC[c], c)
            OCC[c] = name
def grass(x, y): return 0x3000 | ((9 if y % 2 else 17) if x % 2 else (8 if y % 2 else 16))
for y in range(H):
    for x in range(W): G[(x, y)] = grass(x, y)
GRASSID = {8, 9, 16, 17}
DOOR = {}
for k, (ox, oy, cw, ch) in list(CH.items()) + [(k, v) for k, v in GATES.items()]:
    dx, dy = POS[k] if k in POS else (ox, oy)
    claim(dx, dy, cw, ch, k if k in POS else 'gate')
    for j in range(ch):
        for i in range(cw):
            v = ov(ox + i, oy + j); c = (dx + i, dy + j); G[c] = v
            if not (v & 0xc00):
                if k in POS and (v & 0x3ff) in GRASSID: OCC.pop(c, None)
                else: WALK.add(c)
    if k in DOOR_ORIG: DOOR[k] = [(dx + DOOR_ORIG[k][0] - ox, dy + DOOR_ORIG[k][1] - oy)]
GATEAPP = {'N': [(34, 6), (35, 6)], 'S': [(34, 45), (35, 45)], 'W': [(9, 27)], 'E': [(57, 27)]}
START = (34, 45)
# ------------------------------------------------------------------ relief : falaises d'hematite (autotile de montagne FireRed, ids primaires 104..187) + massifs
def east_x0(y): return 62 - int(2.9 * vnoise(y * .21, 1.9, 41))
ROCK = set()
for y in range(H):
    if 24 <= y <= 29: continue
    for x in range(east_x0(y), W): ROCK.add((x, y))
def blob(cx, cy, rx, ry, seed, k=.55):
    out = set()
    for y in range(max(0, int(cy - ry - 2)), min(H, int(cy + ry + 3))):
        for x in range(max(0, int(cx - rx - 2)), min(W, int(cx + rx + 3))):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 0.78 + k * vnoise(x * .33, y * .33, seed): out.add((x, y))
    return out
MASSIFS = [(4.5, 5, 8.5, 6.5, 51), (3.5, 49.5, 7.5, 5.5, 52), (58, 49, 8.5, 5.5, 53), (57.5, 7, 6.5, 8, 54), (20, 1.5, 11, 3.2, 55)]
for (cx, cy, rx, ry, sd) in MASSIFS: ROCK |= blob(cx, cy, rx, ry, sd)
ROCK = {c for c in ROCK if c not in OCC}
for c in ROCK: OCC[c] = 'rock'
# ------------------------------------------------------------------ monument de l'eclipse (3x3, place de la Tour) et ruines (emplacements d'anciens batiments decoratifs)
MON = (32, 34)
claim(MON[0], MON[1], 3, 3, 'mon')
RUINS = [(14, 12), (26, 11), (53, 10), (13, 31), (53, 33), (28, 42), (40, 41), (54, 40), (9, 40), (22, 28), (46, 29), (38, 12)]
RUIN2 = []
for (x, y) in RUINS:
    if all((x + i, y + j) not in OCC and 1 <= x + i < W - 1 and 1 <= y + j < H - 1 for j in (0, 1) for i in (0, 1)):
        claim(x, y, 2, 2, 'ruin'); RUIN2.append((x, y))
print('ruines 2x2', len(RUIN2), '/', len(RUINS))
# ------------------------------------------------------------------ voies : splines lissees, disques empiles (largeur 3 = r 1.1)
WAY = set()
def catmull(pts, n=14):
    P = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2 + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)))
    out.append(P[-2]); return out
def stamp(cx, cy, r):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if 0 <= x < W and 0 <= y < H and (x - cx) ** 2 + (y - cy) ** 2 <= r * r and (x, y) not in OCC: WAY.add((x, y))
def road(pts, r, wob=None):
    Pn = catmull(pts); n = len(Pn)
    for i, (cx, cy) in enumerate(Pn):
        if wob:
            ax, ay, sd = wob; fe = min(1.0, i / 10, (n - 1 - i) / 10)
            cx += ax * (vnoise(i * .05, 3.3, sd) - .5) * 2 * fe; cy += ay * (vnoise(i * .05, 7.7, sd) - .5) * 2 * fe
        stamp(cx, cy, r)
TX, TY = POS['silph']; TDOOR = DOOR['silph'][0]
ROADS = [
    ([(34.5, 8.6), (35.4, 11.5), (34.8, 14.2), (32.6, 15.6)], 1.15, (0.5, 0, 61)),                                                # portail nord -> anneau de la Tour
    ([(34.5, 45.4), (34.3, 41.5), (33.6, 38.6), (33.2, 37.2)], 1.15, (0.5, 0, 62)),                                               # portail sud -> place de l'eclipse
    ([(8.6, 27), (13, 27.4), (17, 26.2), (21, 27.6), (25.2, 27.2)], 1.1, (0, 0.8, 63)),                                           # portail ouest -> anneau
    ([(57.4, 27), (53, 27.6), (49, 26.4), (45, 27.5), (41, 27.2)], 1.1, (0, 0.8, 64)),                                           # portail est -> anneau
    ([(36, 11.0), (40, 10.4), (44, 10.9), (49.5, 10.2), (53.5, 12.4), (54.5, 17.4), (53.2, 22.5)], 1.0, (0, 0.5, 65)),            # rue des arenes (dojo, arene) -> boucle est
    ([(34.8, 12.4), (30, 12.7), (25.5, 13.6), (21, 14.3), (19, 15.6)], 1.0, (0, 0.6, 66)),                                       # rue du nord-ouest (maison du double)
]
for pts, r, wob in ROADS: road(pts, r, wob)
for t in range(0, 360, 3):                                                                                                       # anneau autour de la Tour (ouvert devant la place de l'eclipse)
    a = math.radians(t); cx = TX + 4.5 + 11.4 * math.cos(a) + 1.3 * (vnoise(t * .05, 2.2, 67) - .5) * 2; cy = TY + 7 + 11.0 * math.sin(a) + 1.3 * (vnoise(t * .05, 6.6, 68) - .5) * 2
    if cy > TY + 15.5 and abs(cx - TX - 4.5) < 4.8: continue
    stamp(cx, cy, 1.05)
for y in range(31, 40):                                                                                                          # place de l'eclipse (disque de pave)
    for x in range(26, 42):
        if ((x - 33.5) / 5.6) ** 2 + ((y - 35.2) / 3.3) ** 2 <= 1 and (x, y) not in OCC: WAY.add((x, y))
for k, ds in DOOR.items():                                                                                                       # parvis 3 de large x 2 de profondeur devant chaque porte
    for (x, y) in ds:
        for b in (1, 2):
            for a in (-1, 0, 1):
                c = (x + a, y + b)
                if 0 <= c[0] < W and 0 <= c[1] < H and c not in OCC: WAY.add(c)
for ap in GATEAPP.values():
    for c in ap:
        if c not in OCC: WAY.add(c)
for y in (8, 9):
    for x in (33, 34, 35, 36):
        if (x, y) not in OCC: WAY.add((x, y))
for y in (44, 43):
    for x in (33, 34, 35, 36):
        if (x, y) not in OCC: WAY.add((x, y))
for x in (9, 10):
    for y in (26, 27, 28):
        if (x, y) not in OCC: WAY.add((x, y))
for x in (56, 55):
    for y in (26, 27, 28):
        if (x, y) not in OCC: WAY.add((x, y))
WAY -= {c for c in WAY if c in OCC}
# branches vers les portes : plus court chemin libre jusqu'au reseau, lisse en spline puis tamponne
def branch(start, seed):
    seen = {start: None}; q = collections.deque([start]); goal = None
    while q:
        c = q.popleft()
        if c in WAY and c != start: goal = c; break
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if n in seen or not (1 <= n[0] < W - 1 and 1 <= n[1] < H - 1) or (n in OCC and n not in WALK): continue
            seen[n] = c; q.append(n)
    if goal is None: return
    p = []; c = goal
    while c is not None: p.append(c); c = seen[c]
    pts = [(a + .5 - .5, b + .5 - .5) for (a, b) in p[::3]] + [p[-1]]
    if len(pts) < 3: [WAY.add(c) for c in p if c not in OCC]; return
    road(pts, 0.95, (0.35, 0.35, seed))
for i, (k, ds) in enumerate(sorted(DOOR.items())):
    (x, y) = ds[0]; branch((x, y + 2), 70 + i)
for c in sum(GATEAPP.values(), []):
    if c not in OCC: WAY.add(c)
WAY -= {c for c in WAY if c in OCC}
print('voies', len(WAY), 'cases')
BLK = {}; FLW = set()
KEEP = set(WAY)
for ds in DOOR.values():
    for (x, y) in ds: KEEP.add((x, y + 1))
for ap in GATEAPP.values(): KEEP |= set(ap)
UW, UH = W // 2, H // 2
def ucells(ux, uy): return [(2 * ux + i, 2 * uy + j) for j in (0, 1) for i in (0, 1)]
BIGS = [(23, 30), (44, 33), (18, 46), (50, 21), (12, 22), (40, 13)]                 # grandes formations d'hematite 2x2
for (mx, my) in BIGS:
    for c in [(mx + i, my + j) for j in (0, 1) for i in (0, 1)]: WAY.discard(c)
KEEP = set(WAY)
for ds in DOOR.values():
    for (x, y) in ds: KEEP.add((x, y + 1))
for ap in GATEAPP.values(): KEEP |= set(ap)
# ------------------------------------------------------------------ forets : unites 2x2 (familles de tuiles FR). Cuvette = ellipse irreguliere ; hors cuvette = canopee noire ; bosquets interieurs
GROVES = [(24.5, 22, 2.6, 2.4), (45, 28.5, 2.4, 2.6), (30, 42.2, 2.6, 1.6), (38, 12.8, 1.5, 1.2), (16, 12, 1.5, 1.6), (48, 41, 1.5, 1.4), (22, 32, 1.3, 1.3), (58, 20, 1.5, 2.4), (9, 19, 2.0, 2.4), (9, 34, 2.0, 2.6), (27, 7, 2.0, 1.5), (45, 46, 3.0, 1.6)]
TU = set()
def trunk_ok(ux, uy):
    for i in (0, 1):
        c = (2 * ux + i, 2 * uy + 2)
        if c[1] < H and ((c in OCC and OCC[c] != 'pin') or c in BLK): return False
    return True
def unit_ok(ux, uy): return all(c not in OCC and c not in KEEP and c not in BLK for c in ucells(ux, uy)) and trunk_ok(ux, uy)
for uy in range(UH):
    for ux in range(UW):
        cx, cy = 2 * ux + 1, 2 * uy + 1
        e = ((cx - 33) / (24.5 + 3.5 * (vnoise(ux * .35, uy * .35, 11) - .5))) ** 2 + ((cy - 27) / (20.5 + 3.5 * (vnoise(ux * .35 + 9, uy * .35, 12) - .5))) ** 2
        inside = e > 1.0
        for (gx, gy, rx, ry) in GROVES:
            if ((cx - gx) / rx) ** 2 + ((cy - gy) / ry) ** 2 < 0.75 + 0.6 * vnoise(ux * .9, uy * .9, 5): inside = True
        if inside and unit_ok(ux, uy): TU.add((ux, uy))
FORCED = set()
VOIDSKIP = set()
VOID = 6
def void_fill():
    for _ in range(80):
        TUC = {c for u in TU for c in ucells(*u)}
        free = lambda c: 0 <= c[0] < W and 0 <= c[1] < H and c not in OCC and c not in KEEP and c not in BLK and c not in WAY and c not in TUC and c not in VOIDSKIP
        spot = None
        for y in range(H - VOID + 1):
            for x in range(W - VOID + 1):
                if all(free((x + i, y + j)) for j in range(VOID) for i in range(VOID)): spot = (x, y); break
            if spot: break
        if not spot: break
        added = False
        for (ux, uy) in sorted({((spot[0] + i) // 2, (spot[1] + j) // 2) for j in range(VOID) for i in range(VOID)}):
            if unit_ok(ux, uy) and (ux, uy) not in TU: TU.add((ux, uy)); added = True
        if not added: VOIDSKIP.add((spot[0] + VOID // 2, spot[1] + VOID // 2))
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
NEED = {(x, y + 1) for ds in DOOR.values() for (x, y) in ds} | set(sum(GATEAPP.values(), []))
r0 = reach()
assert NEED <= r0, ('acces manquants', sorted(NEED - r0))
# ------------------------------------------------------------------ cristaux d'hematite, formations, lampadaires, ruines, buissons, fleurs (tirages separes)
def can_block(c, extra=()):
    if c in OCC or c in BLK or c in KEEP or c in WAY: return False
    return NEED <= reach(set(extra) | {c})
def near(c, S, r=1): return any((c[0] + a, c[1] + b) in S for a in range(-r, r + 1) for b in range(-r, r + 1))
PIN = lambda: {k for k, v in OCC.items() if v == 'pin'}
for (mx, my) in BIGS:
    cells = [(mx + i, my + j) for j in (0, 1) for i in (0, 1)]
    if all(c not in OCC and c not in BLK and c not in KEEP for c in cells) and NEED <= reach(set(cells)):
        for (i, j), c in zip(((0, 0), (1, 0), (0, 1), (1, 1)), cells): BLK[c] = ('big', i, j)
        print('formation', (mx, my))
for i, (x, y) in enumerate(RUIN2):
    cells = [(x + a, y + b) for b in (0, 1) for a in (0, 1)]
    for (a, b), c in zip(((0, 0), (1, 0), (0, 1), (1, 1)), cells): BLK[c] = ('ruin', a, b); OCC.pop(c, None)
for (a, b) in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)): BLK[(MON[0] + a, MON[1] + b)] = ('mon', a, b); OCC.pop((MON[0] + a, MON[1] + b), None)
assert NEED <= reach(), 'acces perdu apres monument/ruines'
cands = [(x, y) for y in range(1, H - 1) for x in range(1, W - 1) if (x, y) not in OCC and (x, y) not in WAY and (x, y) not in BLK and (x, y) not in KEEP]
rc = random.Random(1801); rc.shuffle(cands); ncry = 0; pins = PIN(); rocks = {c for c, v in OCC.items() if v == 'rock'}
for c in cands:
    if ncry >= 46: break
    if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q, v in BLK.items() if v[0] in ('cry', 'big')): continue
    if not (near(c, WAY, 2) or near(c, pins, 1) or near(c, rocks, 1)): continue
    if can_block(c): BLK[c] = ('cry', rc.randrange(3)); ncry += 1
print('cristaux', ncry)
rl = random.Random(1802); lc = [c for c in cands if c not in BLK and near4_ok(c) ] if False else None
def near4(c, S): return any((c[0] + a, c[1] + b) in S for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
lc = [c for c in cands if c not in BLK]; rl.shuffle(lc); nl = 0
for c in lc:
    if nl >= 40: break
    if not near4(c, WAY) or near4(c, {q for q in KEEP if q not in WAY}): continue
    if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 6 for q, v in BLK.items() if v[0] == 'lamp'): continue
    if can_block(c): BLK[c] = ('lamp', 0); nl += 1
print('lampadaires', nl)
rw = random.Random(1804); wc = [c for c in cands if c not in BLK]; rw.shuffle(wc); nw = np_ = 0
for c in wc:
    if nw >= 22 and np_ >= 14: break
    if not (near(c, WAY, 2) or near(c, pins, 1)): continue
    if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 2 for q, v in BLK.items() if v[0] in ('wall', 'pillar')): continue
    if can_block(c):
        if nw < 22 and nw <= np_ + 8: BLK[c] = ('wall', rw.randrange(2)); nw += 1
        elif np_ < 14: BLK[c] = ('pillar', rw.randrange(2)); np_ += 1
print('murets', nw, 'colonnes', np_)
rb = random.Random(1802); nb = 0; rb.shuffle(cands)
for c in cands:
    if nb >= 20: break
    if c in BLK or not near(c, pins, 1) or near(c, WAY, 1): continue
    if can_block(c): BLK[c] = ('bush', 0); nb += 1
print('buissons', nb)
rf = random.Random(1803)
fc = [c for c in cands if c not in BLK and c not in OCC and c not in WAY]
rf.shuffle(fc); nf = 0; blds = {k for k, v in OCC.items() if v not in ('pin', 'trunk', 'rock')}
for c in fc:
    if nf >= 60: break
    if near(c, WAY, 1) or near(c, blds, 1):
        FLW.add(c); nf += 1
        for d_ in rf.sample([(1, 0), (0, 1), (1, 1), (-1, 0)], rf.randrange(0, 3)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if n in fc and n not in BLK and n not in OCC and n not in WAY: FLW.add(n)
print('fleurs', len(FLW))
rr = reach()                                                         # poches libres inaccessibles : d'abord des unites d'arbres entieres, puis des buissons
PK = {(x, y) for y in range(H) for x in range(W) if (x, y) not in OCC and not blocked((x, y))} - rr
for (ux, uy) in sorted({(c[0] // 2, c[1] // 2) for c in PK}):
    if all(c in PK for c in ucells(ux, uy)):
        for c in ucells(ux, uy): OCC[c] = 'pin'; PK.discard(c)
        TU.add((ux, uy))
print('POCHES', len(PK))
for c in sorted(PK): BLK[c] = ('bush', 0)
assert NEED <= reach()
# ------------------------------------------------------------------ panneaux et PNJ
SIGN = {}
def place_sign(name, want):
    best = None
    for y in range(H):
        for x in range(W):
            c = (x, y)
            if blocked(c) or c in WAY or c in KEEP or c in FLW or not near4(c, WAY): continue
            if not NEED <= reach({c}): continue
            d_ = abs(x - want[0]) + abs(y - want[1])
            if best is None or d_ < best[0]: best = (d_, c)
    c = best[1]; BLK[c] = ('sign', 0); SIGN[name] = list(c)
DD = {k: v[0] for k, v in DOOR.items()}
for nm, w_ in (('city', (31, 11)), ('dojo', (DD['dojo'][0] - 2, DD['dojo'][1] + 2)), ('gym', (DD['gym'][0] + 2, DD['gym'][1] + 2)), ('silphproduct', (12, 25)),
               ('tips2', (30, 40)), ('silphco', (DD['silph'][0] - 2, DD['silph'][1] + 1)), ('tips1', (54, 25)), ('psy', (DD['psy'][0] - 2, DD['psy'][1] + 1)), ('fanclub', (DD['fan'][0] + 2, DD['fan'][1] + 1))):
    place_sign(nm, w_)
NPC = {}; OBJ_CELLS = set()
DFRONT = {(x, y + 1) for ds in DOOR.values() for (x, y) in ds}
def place_npc(name, want, need=(), rowfree=0):
    r = reach(); best = None
    for c in r:
        if c in BLK or (c in OCC and c not in WALK) or c in OBJ_CELLS or c in DFRONT or c in sum(GATEAPP.values(), []): continue
        cells = [(c[0] + i, c[1]) for i in range(-rowfree, rowfree + 1)] + [(c[0] + a, c[1] + b) for (a, b) in need]
        if not all(q in r and q not in OBJ_CELLS and q not in BLK and q not in DFRONT for q in cells): continue
        d_ = abs(c[0] - want[0]) + abs(c[1] - want[1])
        if best is None or d_ < best[0]: best = (d_, c)
    c = best[1]; NPC[name] = list(c); OBJ_CELLS.add(c)
    for (a, b) in need: OBJ_CELLS.add((c[0] + a, c[1] + b))
sx, sy = DD['silph']
place_npc('grunt1', (DD['copy'][0] + 2, DD['copy'][1] + 2)); place_npc('grunt2', (27, 14)); place_npc('grunt3', (DD['gym'][0], DD['gym'][1] + 2)); place_npc('grunt4', (25, 23))
place_npc('grunt5', (27, 35)); place_npc('grunt7', (30, 41)); place_npc('grunt6', (46, 24))
NPC['guard'] = [sx + 1, sy + 1]; OBJ_CELLS.add((sx + 1, sy + 1)); OBJ_CELLS.add((sx, sy + 1))
place_npc('youngster', (38, 33)); place_npc('worker', (22, 24)); place_npc('man', (40, 14)); place_npc('boy', (44, 25), need=[(1, 0)]); NPC['pidgeot'] = [NPC['boy'][0] + 1, NPC['boy'][1]]
place_npc('lass', (31, 40)); place_npc('crush', (48, 27))
json.dump(NPC, open('/tmp/hematown_npc.json', 'w')); json.dump(SIGN, open('/tmp/hematown_signs.json', 'w'))
json.dump({k: [list(c) for c in v] for k, v in DOOR.items()}, open('/tmp/hematown_doors.json', 'w'))
print('PNJ', NPC); print('panneaux', SIGN)
# ------------------------------------------------------------------ arbres FR : retuilage (haut/bas/tronc/bords), meme logique que Spinellia / Apatia (validee)
P = {c for c, n in OCC.items() if n == 'pin'}
def is_pine(c): return c in P or not (0 <= c[0] < W and 0 <= c[1] < H)
TRUNK = {}
for (x, y) in sorted(P):
    if y % 2 == 1 and not is_pine((x, y + 1)):
        c = (x, y + 1)
        if c in OCC or c in WAY or c in KEEP or c in BLK or c in FLW or c in TRUNK: continue
        OCC[c] = 'trunk'
        if NEED <= reach(): TRUNK[c] = 1
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
assert NEED <= reach(), 'acces perdu apres les troncs'
# ------------------------------------------------------------------ art procedural
PAL = [(0, 0, 0), (22, 18, 34), (118, 110, 140), (100, 92, 122), (60, 54, 78), (146, 138, 168), (34, 86, 94), (52, 122, 122), (92, 164, 150), (78, 72, 98),
       (48, 42, 64), (40, 36, 56), (164, 156, 186), (130, 122, 152), (70, 64, 90), (26, 22, 40)]
PAL_C = [(0, 0, 0), (18, 10, 22), (96, 92, 112), (150, 148, 170), (205, 205, 225), (246, 246, 255), (196, 46, 52), (108, 20, 34), (150, 56, 44), (238, 88, 68),
         (255, 156, 100), (32, 26, 44), (176, 168, 190), (118, 110, 138), (74, 68, 94), (255, 226, 184)]    # hematite : acier sombre, veines et coeur rouges (6-10)
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
    """grande formation d'hematite 2x2 (32x32) : socle de roche, geodes, 5 prismes"""
    im = newimg(32, 32); d = ImageDraw.Draw(im)
    d.ellipse((1, 24, 31, 32), fill=11)
    d.rectangle((3, 26, 28, 30), fill=14, outline=1); d.line([(4, 27), (27, 27)], fill=13); d.rectangle((4, 29, 27, 29), fill=11)
    prism(d, 7, 27, 7, 12); prism(d, 25, 27, 6, 10); prism(d, 12, 28, 8, 17); prism(d, 20, 28, 8, 20); prism(d, 16, 29, 10, 26)
    for (x, y) in ((15, 8), (19, 13), (10, 18), (22, 17)): d.point((x, y), fill=6)
    return im
def path_tile(mask, var=0):
    """pave sombre de 16x16 : dalles en appareil decale ; mask = (N,E,S,W) True si la voisine est aussi un pave (ou un batiment) ; bord erode (la nature reprend) ;
    var 1/2 : touffes de mauvaises herbes dans les joints (10 ans d'abandon)"""
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
def lamp():
    """lampadaire allume en permanence (palette hematite : acier sombre, lanterne ambre)"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((3, 13, 12, 16), fill=11)
    d.rectangle((6, 5, 8, 14), fill=2, outline=1); d.line([(7, 6), (7, 13)], fill=3)
    d.rectangle((4, 12, 10, 14), fill=14, outline=1); d.line([(5, 13), (9, 13)], fill=13)
    d.rectangle((3, 0, 11, 6), fill=10, outline=1); d.rectangle((4, 1, 10, 5), fill=15); d.line([(4, 3), (10, 3)], fill=10); d.point((6, 2), fill=5)
    return im
def wall(var):
    """muret effondre (pierre grise, mousse)"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((1, 12, 15, 16), fill=10)
    if var == 0:
        d.rectangle((1, 8, 14, 14), fill=13, outline=1); d.rectangle((2, 3, 9, 8), fill=3, outline=1); d.rectangle((10, 6, 13, 8), fill=2, outline=1)
        d.line([(1, 11), (14, 11)], fill=4); d.line([(5, 8), (5, 14)], fill=4); d.line([(9, 8), (9, 14)], fill=4)
    else:
        d.rectangle((1, 9, 14, 14), fill=13, outline=1); d.rectangle((6, 2, 14, 9), fill=3, outline=1); d.rectangle((2, 6, 5, 9), fill=2, outline=1)
        d.line([(1, 12), (14, 12)], fill=4); d.line([(8, 9), (8, 14)], fill=4); d.line([(10, 2), (10, 9)], fill=4)
    for (x, y) in ((3, 8), (4, 8), (8, 3), (12, 9), (7, 14)): d.point((x, y), fill=7)
    d.point((4, 7), fill=8); d.point((10, 8), fill=6)
    return im
def pillar(var):
    """colonne brisee"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((2, 12, 14, 16), fill=10)
    d.rectangle((3, 11, 12, 14), fill=13, outline=1); d.line([(4, 12), (11, 12)], fill=5)
    if var == 0: d.polygon([(5, 11), (5, 4), (7, 2), (10, 5), (10, 11)], fill=3, outline=1)
    else: d.polygon([(5, 11), (5, 6), (8, 1), (10, 3), (10, 11)], fill=3, outline=1)
    d.line([(6, 5), (6, 10)], fill=5); d.line([(9, 6), (9, 10)], fill=2)
    d.point((6, 11), fill=7); d.point((7, 11), fill=8); d.point((9, 12), fill=6)
    return im
def ruin():
    """fondations d'un batiment effondre (32x32) : murs bas ebreches, gravats, mauvaises herbes, une veine d'hematite"""
    im = newimg(32, 32); d = ImageDraw.Draw(im)
    d.ellipse((0, 24, 31, 32), fill=10)
    d.rectangle((1, 18, 30, 29), fill=14, outline=1)                                   # sol des fondations
    d.rectangle((1, 20, 30, 29), fill=4)
    for (x0, y0, x1, y1) in ((1, 14, 10, 29), (21, 12, 30, 29), (1, 26, 30, 30)):
        d.rectangle((x0, y0, x1, y1), fill=13, outline=1)
        d.line([(x0 + 1, y0 + 2), (x1 - 1, y0 + 2)], fill=5)
    d.polygon([(1, 14), (4, 8), (7, 11), (10, 6), (10, 14)], fill=3, outline=1)          # pan de mur brise (gauche)
    d.polygon([(21, 12), (24, 4), (27, 9), (30, 3), (30, 12)], fill=3, outline=1)        # pan de mur brise (droite)
    for (x, y, w_, h_) in ((12, 22, 5, 3), (17, 24, 6, 3), (11, 26, 4, 2)): d.rectangle((x, y, x + w_, y + h_), fill=2, outline=1)
    d.polygon([(14, 21), (15, 14), (17, 21)], fill=6, outline=None); d.polygon([(15, 21), (16, 12), (18, 21)], fill=9, outline=None)          # veine d'hematite qui perce
    for (x, y) in ((3, 12), (5, 11), (24, 9), (27, 8), (8, 27), (22, 27), (13, 19)): d.point((x, y), fill=7)
    for (x, y) in ((4, 13), (25, 10), (9, 26)): d.point((x, y), fill=8)
    return im
def eclipse():
    """monument de l'eclipse (48x48) : disque noir a couronne rouge sur un pilier, socle a deux marches, deux eclats d'hematite"""
    im = newimg(48, 48); d = ImageDraw.Draw(im)
    d.ellipse((1, 38, 47, 48), fill=11)
    d.rectangle((3, 41, 44, 47), fill=13, outline=1); d.line([(4, 42), (43, 42)], fill=3); d.rectangle((4, 46, 43, 46), fill=11)
    d.rectangle((8, 36, 39, 41), fill=14, outline=1); d.line([(9, 37), (38, 37)], fill=13)
    d.rectangle((19, 27, 28, 37), fill=2, outline=1); d.line([(21, 28), (21, 36)], fill=3)
    cx, cy = 24, 17
    for k in range(16):                                                              # rayons de la couronne
        a = math.radians(k * 22.5 + 11); r0, r1 = 14, 19 if k % 2 == 0 else 17
        d.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], fill=10 if k % 2 == 0 else 9, width=1)
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=7, outline=1)
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=9)
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=6)
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=1)
    d.arc((cx - 9, cy - 9, cx + 9, cy + 9), 200, 330, fill=11)
    prism(d, 8, 42, 7, 12); prism(d, 40, 42, 6, 10)
    return im
def nonempty(im, box): return sum(1 for q in im.crop(box).getdata() if q)
# controle « sprites entiers » : chaque quart rempli (haut ET bas), pas d'image vide
for v in range(3):
    s_ = small(v); assert nonempty(s_, (0, 0, 16, 8)) >= 4 and nonempty(s_, (0, 8, 16, 16)) >= 20, ('cristal incomplet', v)
def whole(im, name, lim=(4, 20)):
    assert nonempty(im, (0, 0, im.width, im.height // 2)) >= lim[0] and nonempty(im, (0, im.height // 2, im.width, im.height)) >= lim[1], ('sprite incomplet', name)
for nm_, im_ in (('lamp', lamp()), ('wall0', wall(0)), ('wall1', wall(1)), ('pillar0', pillar(0)), ('pillar1', pillar(1))): whole(im_, nm_)
def whole_grid(im, name, n, lim):
    for j in range(n):
        for i in range(n): assert nonempty(im, (i * 16, j * 16, i * 16 + 16, j * 16 + 16)) >= lim, (name, 'incomplet', i, j)
F_ = formation(); whole_grid(F_, 'formation', 2, 24)
RU_ = ruin(); whole_grid(RU_, 'ruine', 2, 24)
EC_ = eclipse(); whole_grid(EC_, 'eclipse', 3, 24)
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
rv = random.Random(1804); PT = {}; ncell = collections.Counter()
def solid(n): return (n in WAY) or (n in OCC and OCC[n] not in ('pin', 'trunk')) or not (0 <= n[0] < W and 0 <= n[1] < H)
for c in sorted(WAY):
    if c in OCC and c not in WALK: continue
    mask = tuple(solid((c[0] + dx, c[1] + dy)) for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)))
    var = 0
    if all(mask):
        rr_ = rv.random(); var = 1 if rr_ < .13 else (2 if rr_ < .22 else 0)
    k = (mask, var)
    if k not in PT: PT[k] = slice4(path_tile(mask, var))
    G[c] = 0x3000 | art_meta(PT[k], G[c] & 0x3ff, True)
    ncell[k] += 1
SM = [slice4(small(v)) for v in range(3)]; FM = {}; RM = {}; EM = {}
for (i, j) in ((0, 0), (1, 0), (0, 1), (1, 1)):
    FM[(i, j)] = slice4(F_.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))); RM[(i, j)] = slice4(RU_.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)))
for i in range(3):
    for j in range(3): EM[(i, j)] = slice4(EC_.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)))
CT_ = {}
def ctile4(key, im):
    if key not in CT_: CT_[key] = slice4(im)
    return CT_[key]
for c, val in BLK.items():
    base = G[c] & 0x3ff
    if val[0] == 'big': G[c] = 0x400 | art_meta(FM[(val[1], val[2])], base, False, 'B')
    elif val[0] == 'ruin': G[c] = 0x400 | art_meta(RM[(val[1], val[2])], base, False, 'A')
    elif val[0] == 'mon': G[c] = 0x400 | art_meta(EM[(val[1], val[2])], base, False, 'B')
    elif val[0] == 'cry': G[c] = 0x400 | art_meta(SM[val[1]], base, False, 'B')
    elif val[0] == 'lamp': G[c] = 0x400 | art_meta(ctile4(('lamp',), lamp()), base, False, 'B')
    elif val[0] == 'wall': G[c] = 0x400 | art_meta(ctile4(('wall', val[1]), wall(val[1])), base, False, 'A')
    elif val[0] == 'pillar': G[c] = 0x400 | art_meta(ctile4(('pillar', val[1]), pillar(val[1])), base, False, 'A')
    elif val[0] == 'bush': G[c] = 0x400 | 5
    elif val[0] == 'sign': G[c] = 0x400 | 2
for c in FLW: G[c] = 0x3000 | 4
# ---- falaises : autotile de montagne FireRed (signature des 8 voisins -> metatuile primaire 104..187)
MTN = {"11111111": 113, "11111011": 178, "11011011": 121, "11011001": 121, "11011101": 121, "11111101": 179, "10111011": 114, "11101101": 179, "11111001": 121, "11011111": 121, "10110011": 114, "11101100": 112, "10101001": 133, "11001101": 120, "10011011": 122, "11101001": 133, "10011001": 122, "10010001": 122, "10100000": 133, "10101000": 133, "10001001": 159, "11001100": 120, "10100100": 133, "10100010": 134, "00000000": 159, "11000000": 141, "01010001": 135, "00010000": 177, "01000000": 176, "01011000": 135, "10010000": 142, "01010000": 135, "00010001": 177, "11110011": 498, "01010011": 135, "01010101": 135, "00110100": 111, "11000001": 141, "10110111": 114, "11110111": 186, "01110111": 105, "01110110": 105, "00110110": 106, "00110010": 106, "01110010": 106, "01010010": 176, "01100110": 104, "01111110": 105, "11111110": 187}
D8 = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
def is_m(c): return c in ROCK or not (0 <= c[0] < W and 0 <= c[1] < H)
def mtn_id(x, y):
    sig = ''.join('1' if is_m((x + dx, y + dy)) else '0' for dx, dy in D8)
    if sig == '11111111': return (113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 108, 108, 187)[((x * 73856093) ^ (y * 19349663)) % 25]
    if sig in MTN: return MTN[sig]
    return MTN[min(MTN, key=lambda k: sum((a_ != b_) * (4 if i_ < 4 else 1) for i_, (a_, b_) in enumerate(zip(k, sig))))]
for (x, y) in ROCK: G[(x, y)] = 0x400 | mtn_id(x, y)
# ------------------------------------------------------------------ compactage du tileset secondaire (seules les metatuiles/tuiles utilisees sont gardees) + ecriture
sec_old = sorted({v & 0x3ff for v in G.values() if 640 <= (v & 0x3ff) < 640 + NMT})
used_t = set()
for m in sec_old:
    for e in struct.unpack('<8H', smt0[(m - 640) * 16:(m - 640) * 16 + 16]):
        if (e & 0x3ff) >= 640: used_t.add((e & 0x3ff) - 640)
for ent in NEWE:
    for q in ent:
        if not isinstance(q, tuple) and (q & 0x3ff) >= 640: used_t.add((q & 0x3ff) - 640)
used_t = sorted(used_t); tmap = {t: i for i, t in enumerate(used_t)}
assert len(sec_old) + len(NEWE) <= 384 and len(used_t) + len(NEWT) <= 384, (len(sec_old) + len(NEWE), len(used_t) + len(NEWT))
print('metatuiles', len(sec_old) + len(NEWE), '/384  (d origine gardees', len(sec_old), ')  tuiles', len(used_t) + len(NEWT), '/384  variantes de pave', len(PT))
def remap_entry(e):
    t = e & 0x3ff
    return (e & ~0x3ff) | (640 + tmap[t - 640]) if t >= 640 else e
mtmap = {m: 640 + i for i, m in enumerate(sec_old)}
out_mt = [[remap_entry(e) for e in struct.unpack('<8H', smt0[(m - 640) * 16:(m - 640) * 16 + 16])] for m in sec_old]
out_att = [satt0[m - 640] for m in sec_old]
PALMAP = {'A': ART_PAL, 'B': CRY_PAL}
for ent, a in zip(NEWE, NEWA):
    out_mt.append([((640 + len(used_t) + q[1]) | (PALMAP[q[0]] << 12)) if isinstance(q, tuple) else remap_entry(q) for q in ent]); out_att.append(a)
art0 = 640 + NMT
for c in list(G):
    v = G[c]; i = v & 0x3ff
    if 640 <= i < art0: G[c] = (v & ~0x3ff) | mtmap[i]
    elif i >= art0: G[c] = (v & ~0x3ff) | (640 + len(sec_old) + (i - art0))
open(NS + 'metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *e) for e in out_mt)); open(NS + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in out_att))
ntot = len(used_t) + len(NEWT); rows = (ntot + 15) // 16
out = Image.new('P', (128, rows * 8), 0); out.putpalette(simg.getpalette())
tiles_old = [simg.crop(((t % 16) * 8, (t // 16) * 8, (t % 16) * 8 + 8, (t // 16) * 8 + 8)) for t in used_t]
for n, ti in enumerate(tiles_old): out.paste(ti, ((n % 16) * 8, (n // 16) * 8))
for n, t in enumerate(NEWT):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((len(used_t) + n) % 16) * 8, ((len(used_t) + n) // 16) * 8))
out.save(NS + 'tiles.png'); writepal(NS + 'palettes/%02d.pal' % ART_PAL, PAL); writepal(NS + 'palettes/%02d.pal' % CRY_PAL, PAL_C)
open('data/layouts/SaffronCity/map.bin', 'wb').write(struct.pack('<%dH' % (W * H), *[G[(x, y)] for y in range(H) for x in range(W)]))
open('data/layouts/SaffronCity/border.bin', 'wb').write(struct.pack('<4H', 0x414, 0x415, 0x41c, 0x41d))      # bordure hors carte : foret de pins FR (phase haut = lignes paires)
# ---- layouts.json + en-tetes C (idempotents)
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
cn = 'Hematown'
add('src/data/tilesets/graphics.h', 'GeneralHematown',
    '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
    '\nconst u32 gTilesetTiles_Saffron%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Saffron%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
add('src/data/tilesets/metatiles.h', 'GeneralHematown',
    '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
    '\nconst u16 gMetatiles_Saffron%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Saffron%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
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
add('src/data/tilesets/headers.h', 'GeneralHematown',
    tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Saffron', cn, 'TRUE', 'Saffron', cn, 'Saffron', cn, 'Saffron', cn, 'Saffron', cn, 'NULL'))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_SAFFRON_CITY': l.update(width=W, height=H, primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Saffron%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('Hematown ecrite')
