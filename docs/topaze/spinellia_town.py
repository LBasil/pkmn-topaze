# SPINELLIA (ex-Lavanville / Lavender Town) : la ville de la Tour Spinelle, cimetiere de Kanto abandonne depuis l'aura (il y a 10 ans).
# Les batiments d'origine (tour, centre, boutique, maisons) sont recopies de la carte FireRed puis recolores (bleu-ardoise crepusculaire, rouge de spinelle),
# agrandis dans une carte 40x30 : foret de pins sombre en bordure, avenues de gravier, cimetiere de steles, cristaux de spinelle.
# Tilesets propres (copies de General + LavenderTown, eau animee conservee). Lancer depuis la racine : python3 docs/topaze/spinellia_town.py puis spinellia_events.py
import struct, json, random, os, shutil, math, colorsys, collections
from PIL import Image, ImageDraw
SP = 'data/tilesets/primary/general/'; SS = 'data/tilesets/secondary/lavender_town/'
NP = 'data/tilesets/primary/general_spinellia/'; NS = 'data/tilesets/secondary/lavender_spinellia/'
W, H = 40, 30
OW, OH = 24, 20
rnd = random.Random(1010)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def spinel(c):
    """pelouses/arbres -> bleu-vert crepusculaire ; sable -> gravier gris-violet ; toits violets -> bleu cobalt ; tour olive -> ardoise ; rouges et gris inchanges"""
    h, l, s = hls(c)
    if s < 0.07: return c
    if 70 <= h <= 175: return rgb(196 + (h - 120) * 0.1, l * 0.8, min(0.6, s * 0.62))
    if 30 <= h < 70: return rgb(258, l * 0.97, min(0.2, s * 0.3))
    if 245 <= h <= 305: return rgb(218, l * 0.95, min(0.7, s * 1.0))
    return c
for src, dst in ((SP, NP), (SS, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16):
        pp = readpal(src + 'palettes/%02d.pal' % i); writepal(dst + 'palettes/%02d.pal' % i, [pp[0]] + [spinel(c) for c in pp[1:16]])
pmt = open(SP + 'metatiles.bin', 'rb').read()
smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = list(struct.unpack('<%dI' % (len(smt) // 16), open(NS + 'metatile_attributes.bin', 'rb').read()))
patt = struct.unpack('<%dI' % (os.path.getsize(SP + 'metatile_attributes.bin') // 4), open(SP + 'metatile_attributes.bin', 'rb').read())
NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
def ents(m): return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
if not os.path.exists('docs/topaze/route21_src/lav_orig.bin'): shutil.copy('data/layouts/LavenderTown/map.bin', 'docs/topaze/route21_src/lav_orig.bin')
O = struct.unpack('<%dH' % (OW * OH), open('docs/topaze/route21_src/lav_orig.bin', 'rb').read())      # carte d'origine (24x20), conservee pour rendre le script idempotent
def ov(x, y): return O[y * OW + x]
used = set()
for v in set(x & 0x3ff for x in O):
    for e in ents(v): used.add(e >> 12)
print('palettes utilisees', sorted(used))
ART_PAL = 7; TREE_PAL = 8
assert ART_PAL not in used and TREE_PAL not in used, used
PAL = [(0, 0, 0), (20, 14, 32), (96, 92, 112), (126, 122, 142), (70, 66, 86), (156, 152, 170), (232, 228, 240), (110, 112, 128), (150, 152, 168),
       (78, 80, 96), (46, 60, 70), (40, 28, 52), (196, 24, 56), (240, 90, 120), (255, 170, 190), (120, 10, 40)]
# ------------------------------------------------------------------ plan
G = {}; OCC = {}
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            assert (x + i, y + j) not in OCC, ('chevauchement', name, OCC[(x + i, y + j)], (x + i, y + j))
            assert 0 <= x + i < W and 0 <= y + j < H, (name, x + i, y + j)
            OCC[(x + i, y + j)] = name
def grass(x, y): return 0x3000 | ((9 if y % 2 else 17) if x % 2 else (8 if y % 2 else 16))
for y in range(H):
    for x in range(W): G[(x, y)] = grass(x, y)
def chunk(ox, oy, cw, ch, dx, dy, name):
    claim(dx, dy, cw, ch, name)
    for j in range(ch):
        for i in range(cw): G[(dx + i, dy + j)] = ov(ox + i, oy + j)
BUILD = {'tower': (15, 0, 7, 7, 27, 2), 'center': (4, 2, 4, 4, 9, 4), 'vol': (8, 8, 5, 4, 5, 12), 'house1': (3, 13, 5, 4, 6, 21), 'house2': (8, 13, 5, 4, 15, 21), 'mart': (18, 12, 4, 4, 31, 21)}
DOOR = {'tower': (30, 8), 'center': (11, 7), 'vol': (7, 15), 'house1': (8, 24), 'house2': (17, 24), 'mart': (33, 24)}
for k, (ox, oy, cw, ch, dx, dy) in BUILD.items(): chunk(ox, oy, cw, ch, dx, dy, k)
for i in range(5): G[(15 + i, 21)] = ov(3 + i, 13)                  # maison 2 : meme rangee de toit que la maison 1 (supprime la frise de pierres flottante)
# bordure : pins 2x2 (haut y0-1, bas y28-29, gauche x0-1, droite x38-39), avec 3 trouees pour les sorties
EXITS = {'N': [(x, 0) for x in range(18, 22)], 'S': [(19, H - 1), (20, H - 1)], 'W': [(0, 18), (0, 19)]}
GAPS = {'N': [(x, y) for x in range(18, 22) for y in range(0, 2)], 'S': [(x, y) for x in range(18, 22) for y in range(H - 2, H)], 'W': [(x, y) for x in range(0, 2) for y in range(18, 20)]}
GAP = {c for g in GAPS.values() for c in g}
PINE = (0x414, 0x415, 0x41c, 0x41d)
PINES = set()
def pine(x, y):
    assert all((x + i, y + j) not in OCC for i in (0, 1) for j in (0, 1)), ('pin sur batiment', x, y)
    for j in (0, 1):
        for i in (0, 1): G[(x + i, y + j)] = PINE[j * 2 + i]; OCC[(x + i, y + j)] = 'pin'
for x in range(0, W, 2):
    for y in (0, H - 2):
        if (x, y) not in GAP and (x + 1, y) not in GAP and not (y == 0 and 26 <= x <= 33): pine(x, y)
for y in range(2, H - 2, 2):
    for x in (0, W - 2):
        if (x, y) not in GAP and (x, y + 1) not in GAP: pine(x, y)
for c in GAP: G[c] = grass(*c)
# ---- voies (2 cases de large)
WAY = set()
def road(pts):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for k in range(n + 1):
            x = int(round(x0 + (x1 - x0) * k / n)); y = int(round(y0 + (y1 - y0) * k / n))
            for c in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)):
                if c not in OCC and 0 <= c[0] <= W - 1 and 0 <= c[1] <= H - 1: WAY.add(c)
road([(19, 0), (19, 18)]); road([(19, 18), (19, 28)])
road([(0, 18), (19, 18)]); road([(19, 18), (37, 18)])
road([(29, 9), (29, 17)]); road([(30, 9), (30, 17)])
road([(11, 8), (11, 17)]); road([(7, 16), (7, 17)])
road([(8, 25), (8, 26)]); road([(17, 25), (17, 26)]); road([(33, 25), (33, 26)])
road([(8, 26), (34, 26)])
for k, (x, y) in DOOR.items():                                      # parvis 3 de large x 2 de profondeur centre sur la porte
    if k == 'tower': continue
    for b in (1, 2):
        for a in (-1, 0, 1): WAY.add((x + a, y + b))
for c in (EXITS['N'] + EXITS['S'] + EXITS['W']): WAY.add(c)
for c in [(9, 8), (5, 16), (10, 16), (6, 25), (15, 25), (31, 25)]: WAY.discard(c)   # croix bleues de Basil
WAY -= {c for c in WAY if c in OCC}
# ---- art
def newimg(w, h): return Image.new('P', (w, h), 0)
GRAV = {}
def path_tile(mask):
    """gravier 16x16 ; mask = (N,E,S,W) : True si la voisine est aussi une voie ; bords erodes + liseré sombre du cote pelouse"""
    im = newimg(16, 16); r = random.Random(5)
    base = [[r.choice((2, 2, 2, 3, 2, 4, 2, 5 if r.random() < .3 else 2)) for _ in range(16)] for _ in range(16)]
    px = im.load()
    for y in range(16):
        for x in range(16):
            d = 99
            if not mask[0]: d = min(d, y)
            if not mask[2]: d = min(d, 15 - y)
            if not mask[3]: d = min(d, x)
            if not mask[1]: d = min(d, 15 - x)
            for (a, b, ca, cb, dx_, dy_) in ((0, 3, 0, 3, x, y), (0, 1, 0, 1, 15 - x, y), (2, 3, 2, 3, x, 15 - y), (1, 2, 1, 2, 15 - x, 15 - y)):
                if not mask[ca] and not mask[cb]:
                    dd = math.hypot(max(0, 3 - dx_), max(0, 3 - dy_)); d = min(d, int(dd) if dd > 0 else d)
            if d < 1: continue
            px[x, y] = 1 if d == 1 else (4 if d == 2 else base[y][x])
    return im
def stele(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((2, 12, 14, 16), fill=11)
    d.rectangle((3, 13, 12, 14), fill=10)
    if var == 0:   # stele arrondie
        d.rectangle((4, 4, 11, 13), fill=8, outline=1); d.pieslice((4, 1, 11, 8), 180, 360, fill=8, outline=1); d.rectangle((9, 5, 10, 13), fill=7)
        d.line([(7, 4), (7, 9)], fill=9); d.line([(5, 6), (9, 6)], fill=9); d.point((6, 3), fill=6)
    elif var == 1:  # croix
        d.rectangle((6, 2, 9, 13), fill=8, outline=1); d.rectangle((3, 5, 12, 8), fill=8, outline=1); d.rectangle((7, 3, 7, 12), fill=6); d.rectangle((8, 3, 9, 12), fill=7); d.rectangle((6, 6, 9, 7), fill=8)
        d.line([(4, 6), (11, 6)], fill=6)
    elif var == 2:  # dalle basse
        d.rectangle((3, 7, 12, 13), fill=8, outline=1); d.rectangle((10, 8, 12, 13), fill=7); d.line([(4, 8), (9, 8)], fill=6); d.line([(5, 10), (9, 10)], fill=9)
    else:           # stele brisee
        d.polygon([(4, 13), (4, 5), (7, 3), (8, 6), (11, 4), (11, 13)], fill=8, outline=1); d.rectangle((9, 6, 10, 13), fill=7); d.point((6, 5), fill=6)
        d.rectangle((1, 12, 3, 13), fill=7, outline=1)
    return im
def prism(d, x, base, w, h):
    half = max(2, w // 2); top = base - h; sh = top + max(3, half + 1)
    d.polygon([(x - half, base), (x - half, sh), (x, top), (x + half, sh), (x + half, base)], fill=12, outline=1)
    d.polygon([(x - half + 1, base - 1), (x - half + 1, sh + 1), (x, top + 2), (x, base - 1)], fill=13)
    d.polygon([(x + 1, top + 2), (x + half - 1, sh + 1), (x + half - 1, base - 1), (x + 1, base - 1)], fill=15)
    d.point((x - half + 1, sh + 1), fill=14); d.point((x - 1, top + 3), fill=6)
def fence(kind):
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((0, 13, 16, 16), fill=11)
    if kind == 'h':
        d.rectangle((0, 6, 15, 7), fill=4, outline=1); d.rectangle((0, 11, 15, 12), fill=4, outline=1)
        for x in (1, 5, 9, 13): d.rectangle((x, 3, x + 1, 13), fill=7, outline=1); d.point((x, 2), fill=5); d.point((x + 1, 2), fill=5)
    else:
        d.rectangle((6, 0, 9, 15), fill=7, outline=1); d.line([(7, 0), (7, 15)], fill=5); d.rectangle((8, 0, 9, 15), fill=4)
        for y in (3, 11): d.rectangle((5, y, 10, y + 2), fill=9, outline=1); d.point((7, y), fill=5)
    return im
TP = [(0, 0, 0), (8, 36, 44), (30, 44, 52), (20, 60, 72), (34, 100, 116), (60, 150, 168), (110, 200, 214), (170, 236, 244)] + [(0, 0, 0)] * 8
def tree_img(var):
    """arbre 1x1 (16x16) : houppier conique sombre, reflets, tronc ; palette 8 = palette des pins FR (memes teintes)"""
    o, d1, d2, m1, m2, l1, l2 = 1, 3, 2, 4, 5, 6, 7
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((2, 13, 15, 16), fill=d1)
    d.rectangle((7, 11, 8, 14), fill=d2, outline=o)
    for k, (y0, hw) in enumerate(((1, 3), (5, 5), (9, 7))):
        d.polygon([(8 - hw, y0 + 5), (8, y0 - 1 if k == 0 else y0), (7 + hw, y0 + 5)], fill=m1, outline=o)
        d.polygon([(8 - hw + 1, y0 + 4), (8, y0 + (0 if k == 0 else 1)), (8, y0 + 4)], fill=l1)
        d.polygon([(8, y0 + 1), (7 + hw - 1, y0 + 4), (8, y0 + 4)], fill=m2 if var != 1 else d2)
    for (x, y) in (((7, 3), (5, 8), (9, 10)), ((8, 2), (4, 9), (10, 11)), ((7, 4), (6, 9), (11, 10)))[var]: d.point((x, y), fill=l2)
    return im
def parapet():
    im = newimg(112, 16); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 111, 15), fill=8, outline=1); d.line([(1, 1), (110, 1)], fill=6); d.rectangle((1, 2, 110, 3), fill=8)
    d.rectangle((1, 12, 110, 14), fill=9)
    for x in range(3, 109, 6): d.rectangle((x, 5, x + 3, 11), fill=7, outline=1); d.point((x + 1, 6), fill=5)
    return im
def crown():
    """toit de la tour (7x2 cases) : toit pyramidal d'ardoise a pans, plateforme a creneaux, fleche de spinelle"""
    im = newimg(112, 32); d = ImageDraw.Draw(im)
    d.polygon([(1, 31), (20, 12), (91, 12), (110, 31)], fill=9, outline=1)
    d.polygon([(3, 30), (21, 13), (56, 13), (56, 30)], fill=7)
    d.polygon([(56, 13), (90, 13), (108, 30), (56, 30)], fill=4)
    for y in range(16, 30, 4):
        x0 = 1 + int((31 - y) * 19 / 19) if False else 0
        d.line([(max(3, 21 - (y - 13) * 18 // 18 - 0), y), (min(108, 91 + (y - 13)), y)], fill=1)
    d.line([(21, 13), (3, 30)], fill=5); d.line([(56, 13), (56, 30)], fill=1)
    d.rectangle((24, 7, 87, 12), fill=8, outline=1); d.line([(25, 8), (86, 8)], fill=6)
    for x in range(27, 86, 8): d.rectangle((x, 4, x + 3, 7), fill=8, outline=1)
    d.rectangle((50, 1, 61, 7), fill=7, outline=1); d.line([(51, 2), (60, 2)], fill=5)
    prism(d, 56, 3, 7, 9)
    prism(d, 18, 12, 7, 12); prism(d, 94, 12, 7, 12)
    return im
def crystal(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((1, 12, 15, 16), fill=11)
    if var == 0: prism(d, 4, 14, 5, 9); prism(d, 9, 15, 7, 14); prism(d, 13, 14, 4, 7)
    elif var == 1: prism(d, 6, 15, 6, 11); prism(d, 12, 14, 5, 8); d.rectangle((1, 13, 3, 14), fill=7)
    else: prism(d, 8, 15, 8, 14); d.rectangle((2, 13, 4, 14), fill=7); d.rectangle((12, 12, 14, 14), fill=7)
    return im
def monument():
    """grande formation de spinelle 2x2 (32x32) sur un socle de pierre"""
    im = newimg(32, 32); d = ImageDraw.Draw(im)
    d.ellipse((1, 24, 31, 32), fill=11)
    d.rectangle((4, 26, 27, 30), fill=9, outline=1); d.line([(5, 27), (26, 27)], fill=8); d.rectangle((5, 29, 26, 29), fill=4)
    prism(d, 7, 27, 7, 12); prism(d, 25, 27, 6, 10); prism(d, 12, 28, 8, 17); prism(d, 20, 28, 8, 20); prism(d, 16, 29, 10, 26)
    for (x, y) in ((15, 8), (19, 13), (10, 18), (22, 17)): d.point((x, y), fill=6)
    return im
NEWT = []; NEWE = []; NEWA = []
def add_tile(t):
    t = tuple(t)
    if t in NEWT: return NEWT.index(t)
    NEWT.append(t); return len(NEWT) - 1
def slice4(im): return [add_tile(list(im.crop(((q % 2) * 8, (q // 2) * 8, (q % 2) * 8 + 8, (q // 2) * 8 + 8)).getdata())) for q in range(4)]
def art_meta(tiles4, base_m, covered, pal=None):
    e = ents(base_m)[:4] + [(('B' if pal == TREE_PAL else 'A'), t) for t in tiles4]; a = (0x20000000 if covered else 0)
    if e in NEWE and NEWA[NEWE.index(e)] == a: return 640 + NMT + NEWE.index(e)
    NEWE.append(e); NEWA.append(a); return 640 + NMT + len(NEWE) - 1
# ---- bloquer des cases (steles, cristaux, pins) en gardant tout accessible
BLK = {}
def free_cells():
    return {(x, y) for y in range(H) for x in range(W) if (x, y) not in OCC and (x, y) not in BLK}
DOORS = {k: v for k, v in DOOR.items()}
for i in range(7): BLK[(27 + i, 2)] = ('parapet', i)
def start_reach(extra=frozenset()):
    seen = {(19, 0)}; q = collections.deque(seen)
    fc = free_cells() - set(extra)
    while q:
        c = q.popleft()
        for d_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if n in fc and n not in seen: seen.add(n); q.append(n)
    return seen
NEED = {(x, y + 1) for (x, y) in DOOR.values()} | {c for e in EXITS.values() for c in e}
KEEP = set(WAY) | NEED
for (x, y) in DOOR.values():
    for a in range(-1, 2):
        for b in range(0, 3): KEEP.add((x + a, y + b))
def can_block(c):
    if c in OCC or c in BLK or c in KEEP: return False
    r = start_reach({c})
    return NEED <= r
for (mx, my) in ((14, 10), (23, 21)):
    claim(mx, my, 2, 2, 'monument'); BLK[(mx, my)] = ('big', 0, 0); BLK[(mx + 1, my)] = ('big', 1, 0); BLK[(mx, my + 1)] = ('big', 0, 1); BLK[(mx + 1, my + 1)] = ('big', 1, 1)
for c in list(BLK): OCC.pop(c, None)
r_ = start_reach(); assert NEED <= r_, 'monument bloque un acces'
# cimetiere : steles en quinconce au sud-est de la tour (x22..37, y10..17), allee centrale x30..31 libre
FENCE = {}
for x in range(22, 38):
    for y in (9, 17):
        if x not in (29, 30, 31): FENCE[(x, y)] = 'h'
for y in range(10, 17):
    for x in (22, 37): FENCE[(x, y)] = 'v'
for c in FENCE: assert c not in OCC and c not in WAY, ('cloture sur voie/batiment', c)
for c in FENCE: BLK[c] = ('fence', FENCE[c])
GRAVES = [(x, y) for y in (11, 13, 15) for x in (24, 26, 28, 33, 35)]
for c in GRAVES: BLK[c] = ('stele', rnd.randrange(4))
for c in range(0): pass
# steles isolees + cristaux de spinelle + bosquets de pins (groupes de 2x2) hors des voies
def near_way(c, r=1): return any((c[0] + a, c[1] + b) in WAY for a in range(-r, r + 1) for b in range(-r, r + 1))
cands = [(x, y) for y in range(2, H - 2) for x in range(2, W - 2) if (x, y) not in OCC and (x, y) not in WAY and not (21 <= x <= 38 and 8 <= y <= 18) and not (34 <= x <= 37 and 2 <= y <= 9)]
rnd.shuffle(cands)
# pins : unites 2x2 alignees sur le damier pair, a distance des voies
def pine_cells(x, y): return [(x + i, y + j) for i in (0, 1) for j in (0, 1)]
PUNITS = {(x, y) for (x, y) in [(x, y) for y in range(0, H, 2) for x in range(0, W, 2)] if G[(x, y)] == PINE[0] and G[(x + 1, y + 1)] == PINE[3]}
pcount = 0
if not any(c in OCC or c in WAY for c in pine_cells(2, 8)): pine(2, 8); PUNITS.add((2, 8))   # rond vert de Basil
for _ in range(4):                      # bosquets : les pins FR n'existent qu'en masse, rattaches a la bordure (leur fond sombre se fond dans la masse)
    order = [(x, y) for y in range(2, H - 3, 2) for x in range(2, W - 3, 2)]; rnd.shuffle(order)
    for (x, y) in order:
        cells = pine_cells(x, y)
        if any(c in OCC or c in BLK or c in KEEP or near_way(c) for c in cells): continue
        if any((c[0] + a, c[1] + b) in OCC and OCC[(c[0] + a, c[1] + b)] != 'pin' for c in cells for a in (-1, 0, 1) for b in (-1, 0, 1)): continue
        if not any(n in PUNITS for n in ((x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2))): continue
        if not NEED <= start_reach(set(cells)): continue
        if rnd.random() < 0.45: pine(x, y); PUNITS.add((x, y)); pcount += 1
print('pins interieurs', pcount)
ncry = 0
for c in cands:
    if c in OCC or c in BLK or near_way(c) or c in KEEP: continue
    rr = rnd.random()
    if rr < 0.09 and not any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q, v in BLK.items() if v[0] == 'cry') and can_block(c): BLK[c] = ('cry', rnd.randrange(3)); ncry += 1
    elif rr < 0.27 and can_block(c): BLK[c] = ('stele', rnd.randrange(4))
print('cristaux', ncry, 'steles', sum(1 for v in BLK.values() if v[0] == 'stele'))
# ---- panneaux (metatuile 2, bloquant) et PNJ
SIGN = {}
def near_path(c): return any((c[0] + a, c[1] + b) in WAY for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
def place_sign(name, want):
    best = None
    for y in range(H):
        for x in range(W):
            c = (x, y)
            if c in OCC or c in WAY or c in KEEP or not near_path(c) or BLK.get(c, ('', 0))[0] in ('fence', 'big'): continue
            old = BLK.pop(c, None); ok = NEED <= start_reach({c}); 
            if old: BLK[c] = old
            if not ok: continue
            d_ = abs(x - want[0]) + abs(y - want[1])
            if best is None or d_ < best[0]: best = (d_, c)
    c = best[1]; BLK.pop(c, None); BLK[c] = ('sign', 0); SIGN[name] = list(c); KEEP.add(c)
for nm, w_ in (('town', (21, 15)), ('tower', (32, 10)), ('vol', (4, 14)), ('notice', (8, 6))): place_sign(nm, w_)
NPC = {}
def place_npc(name, want):
    r = start_reach(); best = None
    for c in r:
        if c in BLK or c in OCC or c in KEEP and c not in WAY: continue
        if any(v == list(c) for v in SIGN.values()) or any(v == list(c) for v in NPC.values()): continue
        d_ = abs(c[0] - want[0]) + abs(c[1] - want[1])
        if best is None or d_ < best[0]: best = (d_, c)
    NPC[name] = list(best[1])
for nm, w_ in (('girl', (23, 20)), ('worker', (14, 17)), ('boy', (7, 19))): place_npc(nm, w_)
json.dump(NPC, open('/tmp/spinellia_npc.json', 'w')); json.dump({k: v for k, v in SIGN.items()}, open('/tmp/spinellia_signs.json', 'w'))
# poches inaccessibles : on comble
for _ in range(3):
    r = start_reach()
    for c in sorted(free_cells() - r):
        if c not in KEEP: BLK[c] = ('stele', rnd.randrange(4)) if rnd.random() < .6 else ('cry', rnd.randrange(3))
r = start_reach()
assert NEED <= r, ('inaccessible', sorted(NEED - r))
for c in sorted(free_cells() - r): print('poche restante', c)
# ---- v10 (Basil : « de-aere la ville ») : bosquets de pins agrandis depuis la bordure, petits groupes de steles et quelques cristaux de plus dans les vides.
# Generateur aleatoire A PART (le decor des versions precedentes ne bouge pas) ; memes regles : jamais pres d'une voie, acces BFS, pins en masse rattachee a la bordure.
rnd2 = random.Random(2026)
def lawn(c): return c not in OCC and c not in BLK and c not in WAY
n_before = sum(1 for y in range(H) for x in range(W) if lawn((x, y)))
npin2 = 0
for _ in range(6):
    order = [(x, y) for y in range(2, H - 3, 2) for x in range(2, W - 3, 2)]; rnd2.shuffle(order)
    for (x, y) in order:
        cells = pine_cells(x, y)
        if any(c in OCC or (c in BLK and BLK[c][0] != 'stele') or c in KEEP or near_way(c) for c in cells): continue          # une stele isolee peut etre remplacee
        if any((c[0] + a, c[1] + b) in OCC and OCC[(c[0] + a, c[1] + b)] != 'pin' for c in cells for a in (-1, 0, 1) for b in (-1, 0, 1)): continue
        if sum(1 for n in ((x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)) if n in PUNITS) < 1: continue
        if not NEED <= start_reach(set(cells)): continue
        if rnd2.random() < 0.85:
            for c in cells: BLK.pop(c, None)
            pine(x, y); PUNITS.add((x, y)); npin2 += 1
WOODS = []
# petits bois 4x4 cases (2x2 unites de pins : chaque unite touche 2 voisines, donc la masse tient) poses dans les plus grands vides (rangee de troncs ajoutee plus bas)
nwood = 0
def occupied(c): return c in OCC or c in BLK or c in WAY
for _ in range(9):
    best = None
    for y in range(2, H - 5, 2):
        for x in range(2, W - 5, 2):
            cells = [(x + i, y + j) for i in range(4) for j in range(4)]
            if any(c in OCC or (c in BLK and BLK[c][0] != 'stele') or c in KEEP or near_way(c) for c in cells): continue          # une stele isolee peut etre remplacee par le bois
            if any((c[0] + a, c[1] + b) in OCC and OCC[(c[0] + a, c[1] + b)] != 'pin' for c in cells for a in (-1, 0, 1) for b in (-1, 0, 1)): continue
            if (21 <= x + 4 and x <= 38 and 8 <= y + 4 and y <= 18): continue          # pas dans le cimetiere
            if any(max(abs(x - bx), abs(y - by)) < 5 for (bx, by) in WOODS): continue
            if not NEED <= start_reach(set(cells)): continue
            room = sum(1 for a in range(-3, 8) for b in range(-3, 8) if 0 <= x + a < W and 0 <= y + b < H and not (occupied((x + a, y + b)) and BLK.get((x + a, y + b), ('',))[0] != 'stele'))
            sc = room + rnd2.random() * 4
            if best is None or sc > best[0]: best = (sc, x, y)
    if best is None: break
    _, x, y = best; WOODS.append((x, y))
    for i in range(4):
        for j in range(4): BLK.pop((x + i, y + j), None)
    for (ux, uy) in ((x, y), (x + 2, y), (x, y + 2), (x + 2, y + 2)): pine(ux, uy); PUNITS.add((ux, uy))
    nwood += 1
nst2 = ncr2 = 0
for _ in range(2):
    order = [(x, y) for y in range(2, H - 2) for x in range(2, W - 2)]; rnd2.shuffle(order)
    for c in order:
        if c in OCC or c in BLK or c in KEEP or near_way(c) or not lawn(c): continue
        if (21 <= c[0] <= 38 and 8 <= c[1] <= 18): continue          # cimetiere de la tour : inchange
        near_st = sum(1 for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2) if BLK.get((c[0] + a, c[1] + b), ('',))[0] == 'stele')
        near_cr = any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q, v in BLK.items() if v[0] == 'cry')
        rr = rnd2.random()
        if rr < 0.04 and not near_cr and can_block(c): BLK[c] = ('cry', rnd2.randrange(3)); ncr2 += 1
        elif rr < (0.34 if near_st else 0.07) and near_st < 4 and can_block(c): BLK[c] = ('stele', rnd2.randrange(4)); nst2 += 1
n_after = sum(1 for y in range(H) for x in range(W) if lawn((x, y)))
print('v10 : pins +%d, bois %d, steles +%d, cristaux +%d ; pelouse libre %d -> %d' % (npin2, nwood, nst2, ncr2, n_before, n_after))
# ---- pas de pin isole : une unite interieure doit toucher au moins 2 autres unites (bordure comprise)
changed = True
while changed:
    changed = False
    for (x, y) in sorted(PUNITS):
        if x in (0, W - 2) or y in (0, H - 2): continue
        n = sum(1 for q in ((x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)) if q in PUNITS or not (0 <= q[0] < W and 0 <= q[1] < H))
        if n < 2:
            PUNITS.discard((x, y)); changed = True
            for c in pine_cells(x, y): OCC.pop(c, None); G[c] = grass(*c)
# ---- pins FR : variantes de bord (gauche/droite) et rangee de troncs sous les masses (tuiles 0x24..0x27)
P = {c for c, n in OCC.items() if n == 'pin'}
def is_pine(c): return c in P or not (0 <= c[0] < W and 0 <= c[1] < H)
TRUNK = {}
for (x, y) in sorted(P):
    if y % 2 == 1 and not is_pine((x, y + 1)):
        c = (x, y + 1)
        if c in OCC or c in WAY or c in KEEP or c in TRUNK or BLK.get(c, ('', 0))[0] in ('sign', 'fence', 'big', 'parapet', 'crown'): continue
        old = BLK.pop(c, None); OCC[c] = 'trunk'
        if NEED <= start_reach(): TRUNK[c] = 1
        else: OCC.pop(c)
        if old and c not in TRUNK: BLK[c] = old
for c in TRUNK: BLK.pop(c, None)
P2 = P | set(TRUNK)
for (x, y) in P2:
    role = 'K' if (x, y) in TRUNK else ('T' if y % 2 == 0 else 'B')
    left = (x % 2 == 0) and not ((x - 1, y) in P2 or not (0 <= x - 1 < W))
    right = (x % 2 == 1) and not ((x + 1, y) in P2 or not (0 <= x + 1 < W))
    base = {'T': (0x14, 0x15, 0x16, 0x17), 'B': (0x1c, 0x1d, 0x1e, 0x1f), 'K': (0x24, 0x25, 0x26, 0x27)}[role]
    if role == 'T' and (x, y - 1) not in P2 and 0 <= y - 1: base = (0x0e, 0x0f, 0x0e, 0x0f)
    G[(x, y)] = 0x400 | (base[2] if left else base[3] if right else base[x % 2])
print('troncs', len(TRUNK))
# ---- colonne droite du Pokecentre (5 de large) et case de chemin (7,27) : ajoutees APRES tout le hasard pour ne pas deplacer le decor
for j in range(4):
    c = (13, 4 + j); BLK.pop(c, None); G[c] = ov(8, 2 + j); OCC[c] = 'center'; WAY.discard(c)
BLK.pop((7, 27), None); WAY.add((7, 27))
# ---- ecriture des metatuiles
PT = {}
for c in sorted(WAY):
    mask = tuple(((c[0] + dx, c[1] + dy) in WAY or (c[0] + dx, c[1] + dy) in OCC and OCC[(c[0] + dx, c[1] + dy)] not in ('pin',) or not (0 <= c[0] + dx < W and 0 <= c[1] + dy < H)) for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)))
    if mask not in PT: PT[mask] = slice4(path_tile(mask))
    G[c] = 0x3000 | art_meta(PT[mask], G[c] & 0x3ff, True)
ST = [slice4(stele(v)) for v in range(4)]; CR = [slice4(crystal(v)) for v in range(3)]
MON = monument(); PARA = parapet(); CROWN = crown()
for j in range(2):
    for i in range(7):
        if sum(1 for q in CROWN.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)).getdata() if q): BLK[(27 + i, j)] = ('crown', i, j)
for c, val in BLK.items():
    if val[0] == 'big':
        i, j = val[1], val[2]; G[c] = 0x400 | art_meta(slice4(MON.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))), G[c] & 0x3ff, False)
    elif val[0] == 'tree': G[c] = 0x400 | art_meta(slice4(tree_img(val[1])), G[c] & 0x3ff, False, TREE_PAL)
    elif val[0] == 'parapet': G[c] = 0x400 | art_meta(slice4(PARA.crop((val[1] * 16, 0, val[1] * 16 + 16, 16))), G[c] & 0x3ff, False)
    elif val[0] == 'crown': G[c] = 0x400 | art_meta(slice4(CROWN.crop((val[1] * 16, val[2] * 16, val[1] * 16 + 16, val[2] * 16 + 16))), G[c] & 0x3ff, False)
    elif val[0] == 'sign': G[c] = 0x400 | 2
    elif val[0] == 'fence': G[c] = 0x400 | art_meta(slice4(fence(val[1])), G[c] & 0x3ff, False)
    else: G[c] = 0x400 | art_meta(ST[val[1]] if val[0] == 'stele' else CR[val[1]], G[c] & 0x3ff, False)
assert NMT + len(NEWE) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(NEWE), NTL + len(NEWT))
print('metatuiles', NMT + len(NEWE), 'tuiles', NTL + len(NEWT))
NEWE = [[((640 + NTL + q[1]) | ((TREE_PAL if q[0] == 'B' else ART_PAL) << 12)) if isinstance(q, tuple) else q for q in e] for e in NEWE]
smt += b''.join(struct.pack('<8H', *e) for e in NEWE); satt += NEWA
open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in satt))
rows = (NTL + len(NEWT) + 15) // 16
out = Image.new('P', (128, rows * 8), 0); out.putpalette(simg.getpalette()); out.paste(simg, (0, 0))
for n, t in enumerate(NEWT):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
out.save(NS + 'tiles.png'); writepal(NS + 'palettes/%02d.pal' % ART_PAL, PAL); writepal(NS + 'palettes/%02d.pal' % TREE_PAL, TP)
open('data/layouts/LavenderTown/map.bin', 'wb').write(struct.pack('<%dH' % (W * H), *[G[(x, y)] for y in range(H) for x in range(W)]))
open('data/layouts/LavenderTown/border.bin', 'wb').write(struct.pack('<4H', *PINE))                 # bordure hors carte : foret de pins
# ---- layouts.json + en-tetes C
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
cn = 'Spinellia'
add('src/data/tilesets/graphics.h', 'GeneralSpinellia',
    '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
    '\nconst u32 gTilesetTiles_Lavender%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Lavender%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
add('src/data/tilesets/metatiles.h', 'GeneralSpinellia',
    '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
    '\nconst u16 gMetatiles_Lavender%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Lavender%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
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
add('src/data/tilesets/headers.h', 'GeneralSpinellia',
    tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Lavender', cn, 'TRUE', 'Lavender', cn, 'Lavender', cn, 'Lavender', cn, 'Lavender', cn, 'NULL'))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_LAVENDER_TOWN': l.update(width=W, height=H, primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Lavender%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({k: list(v) for k, v in DOOR.items()}, open('/tmp/spinellia_doors.json', 'w'))
print('Spinellia ecrite')
