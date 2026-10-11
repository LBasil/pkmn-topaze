# CELADOPOLE (ex-Celadon / Celadon City, LAYOUT_CELADON_CITY 60x40) : la grande ville marchande de Kanto, 10 ans apres l'aura.
# Les batiments qui ont un interieur (grand magasin, copropriete + jardin de toit, Centre, casino + salle des lots, arene, restaurant, maison, hotel)
# sont recopies de la carte FireRed puis REPLACES dans une composition organique ; les ~13 batiments decoratifs sans porte disparaissent
# (regle « chaque maison sert a quelque chose ») : la nature a repris leur place (forets d'arbres FR, cristaux d'amethyste, pelouse).
# Couleurs = celles de la Route 18 (teinte amethyste identique). Tilesets propres (copies de General + CeladonCity, eau animee conservee).
# Idempotent : part de route21_src/cel_orig.bin. Lancer depuis la racine : python3 docs/topaze/celadopole_town.py puis celadopole_events.py
import struct, json, random, os, shutil, math, colorsys, collections
from PIL import Image, ImageDraw
SP = 'data/tilesets/primary/general/'; SS = 'data/tilesets/secondary/celadon_city/'
NP = 'data/tilesets/primary/general_celadopole/'; NS = 'data/tilesets/secondary/celadon_celadopole/'
W, H = 60, 40
OW, OH = 60, 40
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_amethyst(c):
    """identique a la Route 18 : jaunes/verts -> lilas, verts sombres -> indigo, bleus legerement decales ; rouges et gris inchanges"""
    h, l, s = hls(c)
    if s < 0.08: return c
    if 28 <= h < 70 and s > 0.1: return rgb(284, min(1, l * 1.0 + 0.02), min(0.5, s * 0.6 + 0.05))
    if 70 <= h <= 175: return rgb(274, min(1, l + 0.03), min(0.7, s * 0.6 + 0.05)) if l > 0.42 else rgb(258, min(1, l * 1.18), min(0.8, s * 0.9))
    if 180 <= h <= 235: return rgb(h + 8, l, s)
    return c
for src, dst in ((SP, NP), (SS, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16):
        pp = readpal(src + 'palettes/%02d.pal' % i); writepal(dst + 'palettes/%02d.pal' % i, [pp[0]] + [tint_amethyst(c) for c in pp[1:16]])
pmt = open(SP + 'metatiles.bin', 'rb').read()
smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = list(struct.unpack('<%dI' % (len(smt) // 16), open(NS + 'metatile_attributes.bin', 'rb').read()))
NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
def ents(m): return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
if not os.path.exists('docs/topaze/route21_src/cel_orig.bin'): shutil.copy('data/layouts/CeladonCity/map.bin', 'docs/topaze/route21_src/cel_orig.bin')
O = struct.unpack('<%dH' % (OW * OH), open('docs/topaze/route21_src/cel_orig.bin', 'rb').read())      # carte d'origine (60x40), conservee pour rendre le script idempotent
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
# ------------------------------------------------------------------ plan : batiments (chunks d'origine)
CH = {'dept': (9, 5, 9, 10), 'condo': (27, 3, 7, 9), 'center': (46, 7, 5, 5), 'gc': (31, 17, 10, 5), 'gym': (8, 26, 8, 5),
      'rest': (36, 25, 4, 5), 'house1': (40, 25, 4, 5), 'hotel': (48, 25, 4, 5), 'fountain': (12, 18, 3, 4), 'pond': (24, 21, 6, 3)}
POS = {'dept': (8, 4), 'condo': (23, 3), 'center': (47, 8), 'gc': (30, 18), 'fountain': (17, 20), 'pond': (44, 21),
       'gym': (7, 26), 'rest': (31, 27), 'house1': (37, 28), 'hotel': (44, 27)}
DOOR_ORIG = {'dept': [(11, 14), (15, 14)], 'condo': [(30, 11)], 'center': [(48, 11)], 'gc': [(34, 21), (39, 20)], 'gym': [(11, 30)],
             'rest': [(37, 29)], 'house1': [(41, 29)], 'hotel': [(49, 29)]}
ROOF_ORIG = [(29, 5), (30, 4), (31, 5)]
G = {}; OCC = {}; WALK = set()
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            assert (x + i, y + j) not in OCC, ('chevauchement', name, OCC[(x + i, y + j)], (x + i, y + j))
            assert 0 <= x + i < W and 0 <= y + j < H, (name, x + i, y + j)
            OCC[(x + i, y + j)] = name
def grass(x, y): return 0x3000 | ((9 if y % 2 else 17) if x % 2 else (8 if y % 2 else 16))
for y in range(H):
    for x in range(W): G[(x, y)] = grass(x, y)
DOOR = {}; ROOF = []
for k, (ox, oy, cw, ch) in CH.items():
    dx, dy = POS[k]; claim(dx, dy, cw, ch, k)
    for j in range(ch):
        for i in range(cw):
            v = ov(ox + i, oy + j); G[(dx + i, dy + j)] = v; c = (dx + i, dy + j)
            if not (v & 0xc00):                                   # case sans collision : herbe -> libre ; autre (parvis, marche, porte) -> praticable mais protegee
                if (v & 0x3ff) in (8, 9, 16, 17): OCC.pop(c, None)
                else: WALK.add(c)
    DOOR[k] = [(dx + x - ox, dy + y - oy) for (x, y) in DOOR_ORIG.get(k, [])]
    if k == 'condo': ROOF = [(dx + x - ox, dy + y - oy) for (x, y) in ROOF_ORIG]
EXITS = {'W': [(0, 22), (0, 23), (0, 24)], 'E': [(W - 1, 12), (W - 1, 13), (W - 1, 14)]}
START = (0, 23)
# ------------------------------------------------------------------ voies : splines lissees, disques empiles (largeur 3 = r 1.6, largeur 2 = r 1.1)
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
            if 0 <= x < W and 0 <= y < H and (x + .5 - cx - .5) ** 2 + (y + .5 - cy - .5) ** 2 <= r * r and (x, y) not in OCC: WAY.add((x, y))
def road(pts, r, wob=None):
    Pn = catmull(pts); n = len(Pn)
    for i, (cx, cy) in enumerate(Pn):
        if wob:
            ax, ay, sd = wob; fe = min(1.0, i / 10, (n - 1 - i) / 10)
            cx += ax * (vnoise(i * .05, 3.3, sd) - .5) * 2 * fe; cy += ay * (vnoise(i * .05, 7.7, sd) - .5) * 2 * fe
        stamp(cx, cy, r)
ROADS = [
    # boulevard est-ouest (sinueux) : sortie est -> centre -> condos -> grand magasin
    ([(59, 13), (55, 12.6), (51, 14.4), (47, 15.6), (43, 15.0), (38, 14.6), (33, 14.9), (28.5, 13.4), (24, 14.6), (19, 16.2), (14, 15.8), (9.5, 15.2)], 1.05, (0,1.7,21)),
    # avenue centrale : boulevard -> place du casino -> rue du sud
    ([(27, 14.5), (26.6, 18), (26.4, 22.5), (25.8, 27), (26.6, 31), (28.5, 34.5)], 0.9, (1.3,0,22)),
    # route de l'ouest : sortie ouest -> place de la fontaine -> avenue
    ([(0, 23), (4, 23.4), (8, 22.4), (12.5, 23.6), (15, 26), (19, 26.6), (23, 25.6), (26.4, 24)], 1.05, (0,1.2,23)),
    # place du casino
    ([(29, 25), (34, 25.2), (39, 24.8)], 1.05, None),
    # rue du sud (commerces, arene), sinueuse, puis boucle est
    ([(3, 35), (7, 33.5), (12, 34.4), (17, 35.5), (22, 34.6), (27, 33.6), (32, 34.3), (37, 35.3), (42, 34.6), (46, 33.4), (50, 34.2), (53, 31.5)], 1.05, (0,1.5,24)),
    # boucle est : rue du sud -> bassin -> boulevard
    ([(53, 31.5), (52.6, 27), (52, 22), (52.4, 17), (54, 13.5)], 0.9, (0.8,0,25)),
    # chemin du bassin
    ([(39, 24.8), (44, 25.8), (49, 25.2), (52, 23.5)], 0.9, (0,0.8,26)),
]
for pts, r, wob in ROADS: road(pts, r, wob)
# place de la fontaine : disque de pave autour du bassin d'ornement
for y in range(17, 27):
    for x in range(12, 25):
        if ((x + .5 - 18.5) / 4.0) ** 2 + ((y + .5 - 22) / 3.2) ** 2 <= 1 and (x, y) not in OCC: WAY.add((x, y))
for k, ds in DOOR.items():                                          # parvis 3 de large x 2 de profondeur devant chaque porte
    for (x, y) in ds:
        for b in (1, 2):
            for a in (-1, 0, 1):
                c = (x + a, y + b)
                if c not in OCC and 0 <= c[0] < W and 0 <= c[1] < H: WAY.add(c)
for c in sum(EXITS.values(), []): WAY.add(c)
WAY -= {c for c in WAY if c in OCC}
print('voies', len(WAY), 'cases')
# ------------------------------------------------------------------ sentier + clairiere de geode (acces garde par un arbre a couper), poche est (objet cache, arbre a couper)
BLK = {}                       # case -> ('cry'|'big'|'bush'|'sign', ...) ; bloquantes
FLW = set()                    # fleurs (praticables)
UW, UH = W // 2, H // 2
def ucells(ux, uy): return [(2 * ux + i, 2 * uy + j) for j in (0, 1) for i in (0, 1)]
GATE = {'glade': [(36, 12), (37, 12)], 'east': [(54, 20), (54, 21)]}      # [arbre a couper, buisson bloquant] : ouverture a 2 cases
road([(36.5, 14.5), (36.5, 12), (36.5, 10)], 1.0)
GLADE_UNITS = {(ux, uy) for uy in range(1, 5) for ux in range(15, 23) if ((2 * ux + 1 - 37.2) / 4.6) ** 2 + ((2 * uy + 1 - 6.4) / 3.3) ** 2 <= 1}
GLADE_UNITS = {u for u in GLADE_UNITS if all(c not in OCC for c in ucells(*u))}
GLADE = {c for u in GLADE_UNITS for c in ucells(*u)}
POCKET_UNITS = {(27, 10), (28, 10)}
POCKET = {c for u in POCKET_UNITS for c in ucells(*u)} - set(GATE['east'])
WAY -= GLADE | POCKET | set(GATE['glade']) | set(GATE['east'])
KEEP = set(WAY) | GLADE | POCKET | set(GATE['glade']) | set(GATE['east'])
for (x, y) in sum(DOOR.values(), []): KEEP.add((x, y + 1))
# ------------------------------------------------------------------ forets : unites 2x2 (familles de tuiles FR), lisiere irreguliere + bosquets
GROVES = [(20.5, 8.5, 3.2, 5.5), (5.5, 18.5, 3.8, 2.6), (46, 18.2, 5.5, 2.2), (22.2, 18.8, 1.9, 2.0), (38.5, 7.2, 8.6, 4.8), (47.5, 4.5, 3.5, 2.0),
          (12.5, 30.5, 1.2, 1.1), (36, 36.2, 3.0, 1.3), (21, 31, 1.5, 1.2), (51, 28.5, 1.0, 1.6), (41, 20, 1.2, 1.0), (30, 30.8, 0.9, 0.9), (12, 21, 1.6, 1.4), (5.5, 8.5, 1.8, 4.5), (19.5, 29.8, 3.4, 2.4), (4.6, 29.5, 1.8, 3.0), (43.2, 9.0, 1.8, 3.0)]
TU = set()
def unit_ok(ux, uy): return all(c not in OCC and c not in KEEP and c not in BLK for c in ucells(ux, uy))
for uy in range(UH):
    for ux in range(UW):
        d = min(ux, uy, UW - 1 - ux, UH - 1 - uy)
        T = 1.15 + 2.3 * vnoise(ux * .42, uy * .42, 11)
        inside = d < T
        cx, cy = 2 * ux + 1, 2 * uy + 1
        for (gx, gy, rx, ry) in GROVES:
            if ((cx - gx) / rx) ** 2 + ((cy - gy) / ry) ** 2 < 0.75 + 0.6 * vnoise(ux * .9, uy * .9, 5): inside = True
        if inside and unit_ok(ux, uy): TU.add((ux, uy))
# anneau d'arbres force autour de la clairiere, de la poche et du sentier (la prairie ne doit pas les contourner)
FORCED = set()
def ring(cells, r=2):
    for (ux, uy) in [(x, y) for y in range(UH) for x in range(UW)]:
        if any(abs(c[0] - q[0]) <= r and abs(c[1] - q[1]) <= r for c in ucells(ux, uy) for q in cells) and unit_ok(ux, uy): TU.add((ux, uy)); FORCED.add((ux, uy))
TRAILC = {(x, y) for y in range(10, 14) for x in (36, 37)}
ring(GLADE | TRAILC - set(GATE['glade']), 2); ring(POCKET | set(GATE['east']), 2)
VOIDSKIP = set()
def void_fill():
    """comble les vides de prairie >= 5x5 (hors voies/batiments) avec des unites d'arbres"""
    for _ in range(80):
        TUC = {c for u in TU for c in ucells(*u)}
        free = lambda c: c not in OCC and c not in KEEP and c not in BLK and c not in WAY and c not in TUC and c not in VOIDSKIP and 0 <= c[0] < W and 0 <= c[1] < H
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
NEED = {(x, y + 1) for (x, y) in sum(DOOR.values(), [])} | set(EXITS['W']) | set(EXITS['E'])
for k in ('glade', 'east'): BLK[GATE[k][1]] = ('bush', 0)
NEED_GATE = {GATE['glade'][0], GATE['east'][0]}
r0 = reach()
assert NEED <= r0, ('acces manquants', sorted(NEED - r0))
assert NEED_GATE <= r0, ('arbres a couper inaccessibles', sorted(NEED_GATE - r0))
assert GLADE and all(c in reach(start=GATE['glade'][0]) for c in GLADE), 'clairiere inaccessible'
assert all(c in reach(start=GATE['east'][0]) for c in POCKET), 'poche est inaccessible'
# la clairiere et la poche ne doivent s'ouvrir QUE par l'arbre a couper
assert not (GLADE & r0 - {GATE['glade'][0]}) or True
only = reach(extra={GATE['glade'][0], GATE['east'][0]})
leak = (GLADE | POCKET) & only
assert not leak, ('clairiere/poche ouvertes sans couper', sorted(leak)[:8])
# ------------------------------------------------------------------ cristaux, buissons, fleurs (tirages separes : les retouches ne deplacent pas le reste)
def can_block(c, extra=()):
    if c in OCC or c in BLK or c in KEEP or c in WAY: return False
    return NEED | NEED_GATE <= reach(set(extra) | {c})
def near(c, S, r=1): return any((c[0] + a, c[1] + b) in S for a in range(-r, r + 1) for b in range(-r, r + 1))
PIN = lambda: {k for k, v in OCC.items() if v == 'pin'}
rc = random.Random(1601)
for (mx, my) in ((36, 5), (6, 21), (49, 19)):                   # grandes formations d'amethyste 2x2 (clairiere, parc ouest, rive du bassin)
    cells = [(mx + i, my + j) for j in (0, 1) for i in (0, 1)]
    if all(c not in OCC and c not in WAY and c not in BLK for c in cells) and NEED | NEED_GATE <= reach(set(cells)):
        for (i, j), c in zip(((0, 0), (1, 0), (0, 1), (1, 1)), cells): BLK[c] = ('big', i, j)
        print('formation', (mx, my))
cands = [(x, y) for y in range(2, H - 2) for x in range(2, W - 2) if (x, y) not in OCC and (x, y) not in WAY and (x, y) not in BLK and (x, y) not in KEEP]
rc.shuffle(cands); ncry = 0; pins = PIN()
for c in cands:
    if ncry >= 46: break
    if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q, v in BLK.items() if v[0] in ('cry', 'big')): continue
    if not (near(c, WAY, 2) or near(c, pins, 1)): continue
    if can_block(c): BLK[c] = ('cry', rc.randrange(3)); ncry += 1
print('cristaux', ncry)
rb = random.Random(1602); nb = 0
rb.shuffle(cands)
for c in cands:
    if nb >= 22: break
    if c in BLK or not near(c, pins, 1) or near(c, WAY, 1): continue
    if can_block(c): BLK[c] = ('bush', 0); nb += 1
print('buissons', nb)
rf = random.Random(1603)
fc = [c for c in cands if c not in BLK and c not in OCC and c not in WAY]
rf.shuffle(fc); nf = 0; blds = {k for k, v in OCC.items() if v != 'pin'}
for c in fc:
    if nf >= 70: break
    if near(c, WAY, 1) or near(c, blds, 1):
        FLW.add(c); nf += 1
        for d_ in rf.sample([(1, 0), (0, 1), (1, 1), (-1, 0)], rf.randrange(0, 3)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if n in fc and n not in BLK and n not in OCC and n not in WAY: FLW.add(n)
print('fleurs', len(FLW))
# poches inaccessibles (hors clairiere/poche) : on comble de buissons
rr = reach()
for c in sorted({(x, y) for y in range(H) for x in range(W) if not blocked((x, y))} - rr - GLADE - POCKET - set(GATE['glade'][:1]) - set(GATE['east'][:1])):
    BLK[c] = ('bush', 0)
assert NEED <= reach()
# ------------------------------------------------------------------ panneaux et PNJ
SIGN = {}; SIGN_CELLS = []
def near4(c, S): return any((c[0] + a, c[1] + b) in S for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
def place_sign(name, want):
    best = None
    for y in range(H):
        for x in range(W):
            c = (x, y)
            if blocked(c) or c in WAY or c in KEEP or c in FLW or not near4(c, WAY): continue
            if not NEED | NEED_GATE <= reach({c}): continue
            d_ = abs(x - want[0]) + abs(y - want[1])
            if best is None or d_ < best[0]: best = (d_, c)
    c = best[1]; BLK[c] = ('sign', 0); SIGN[name] = list(c)
for nm, w_ in (('city', (4, 21)), ('gym', (15, 31)), ('dept', (17, 14)), ('mansion', (25, 12)), ('gamecorner', (29, 23)), ('prize', (40, 22)), ('tips1', (36, 17)), ('tips2', (50, 17))):
    place_sign(nm, w_)
NPC = {}; OBJ_CELLS = set(GATE['glade'] + GATE['east'])
def place_npc(name, want, need=(), rowfree=0, region=None):
    r = reach(); best = None
    for c in r:
        if c in BLK or c in OCC or c in OBJ_CELLS: continue
        if region is None and c in KEEP and c not in WAY: continue
        if region is not None and c not in region: continue
        cells = [(c[0] + i, c[1]) for i in range(-rowfree, rowfree + 1)] + [(c[0] + a, c[1] + b) for (a, b) in need]
        if not all(q in r and q not in OBJ_CELLS and q not in BLK for q in cells): continue
        d_ = abs(c[0] - want[0]) + abs(c[1] - want[1])
        if best is None or d_ < best[0]: best = (d_, c)
    c = best[1]; NPC[name] = list(c); OBJ_CELLS.add(c)
    for (a, b) in need: OBJ_CELLS.add((c[0] + a, c[1] + b))
place_npc('grunt1', (50, 17), rowfree=2)
place_npc('poli', (35, 16), need=[(1, 0), (2, 0)]); NPC['fat'] = [NPC['poli'][0] + 2, NPC['poli'][1]]
place_npc('girl', (14, 21), need=[(1, 0), (0, 1), (1, 1)])
place_npc('woman', (21, 24), rowfree=1)
place_npc('oldman2', (31, 26))
place_npc('tutor', (43, 25))
place_npc('grunt2', (38, 36), rowfree=2)
place_npc('oldman1', (12, 32))
place_npc('boy', (23, 13))
place_npc('scientist', (48, 26))
place_npc('ether', (36, 7), region=GLADE)
NPC['tree1'] = list(GATE['east'][0]); NPC['tree2'] = list(GATE['glade'][0])
place_npc('hidden', (57, 21), region=POCKET)
json.dump(NPC, open('/tmp/celadopole_npc.json', 'w')); json.dump(SIGN, open('/tmp/celadopole_signs.json', 'w'))
json.dump({k: [list(c) for c in v] for k, v in DOOR.items()}, open('/tmp/celadopole_doors.json', 'w'))
json.dump({'roof': [list(c) for c in ROOF], 'exitW': [list(c) for c in EXITS['W']], 'exitE': [list(c) for c in EXITS['E']]}, open('/tmp/celadopole_misc.json', 'w'))
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
PAL = [(0, 0, 0), (64, 44, 92), (214, 198, 236), (198, 180, 224), (170, 150, 200), (238, 228, 250), (118, 82, 168), (168, 127, 200), (209, 172, 237), (122, 108, 146),
       (96, 70, 120), (150, 130, 180), (230, 220, 244), (186, 166, 214), (140, 120, 170), (80, 56, 110)]
PAL_C = [(0, 0, 0), (30, 10, 52), (94, 44, 142), (142, 84, 202), (188, 132, 236), (228, 200, 252), (252, 242, 255), (46, 36, 112), (84, 72, 172),
         (132, 122, 222), (198, 192, 250), (40, 30, 66), (214, 64, 152), (176, 168, 192), (96, 88, 118), (255, 246, 200)]
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
    """grande formation d'amethyste 2x2 (32x32) : socle de roche, geodes, 5 prismes"""
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
def solid(n): return (n in WAY) or (n in OCC and OCC[n] not in ('pin', 'trunk', 'void')) or n in WALK or not (0 <= n[0] < W and 0 <= n[1] < H)
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
open('data/layouts/CeladonCity/map.bin', 'wb').write(struct.pack('<%dH' % (W * H), *[G[(x, y)] for y in range(H) for x in range(W)]))
open('data/layouts/CeladonCity/border.bin', 'wb').write(struct.pack('<4H', 0x414, 0x415, 0x41c, 0x41d))      # bordure hors carte : foret d'arbres FR (phase haut = lignes paires)
# ---- layouts.json + en-tetes C (idempotents)
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
cn = 'Celadopole'
add('src/data/tilesets/graphics.h', 'GeneralCeladopole',
    '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
    '\nconst u32 gTilesetTiles_Celadon%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Celadon%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
add('src/data/tilesets/metatiles.h', 'GeneralCeladopole',
    '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
    '\nconst u16 gMetatiles_Celadon%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Celadon%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
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
add('src/data/tilesets/headers.h', 'GeneralCeladopole',
    tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Celadon', cn, 'TRUE', 'Celadon', cn, 'Celadon', cn, 'Celadon', cn, 'Celadon', cn, 'NULL'))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_CELADON_CITY': l.update(width=W, height=H, primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Celadon%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('Celadopole ecrite')
