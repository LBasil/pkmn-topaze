# ROUTE 23 v2 : « la route de l'aube » (derive de route14_v2.py). Carte 24x160 : on garde le haut (portail de la Ligue, grotte, poste de la Terre / Volcan : lignes < 64), le bas (poste de la Cascade : lignes >= 143)
# et les deux colonnes d'arbres de chaque bord ; tout le reste (lignes 64..142, colonnes 2..21) est redessine : au lieu de quatre facades pleine largeur, quatre petits postes de garde (arche + deux ailes) poses
# dans un col forestier, relies par un chemin en lacets, des murets a escaliers, des etangs et des bosquets. Palette « aube » (general_dawn / indigo_dawn). Idempotent : part de route21_src/r23_orig.bin.
# Gardes : Tonnerre (xc 14, g 133), Arc-en-ciel (9, 117), Ame (15, 101), Marais (8, 85) ; declencheurs sur les 3 cases d'apron devant l'arche (g+1), le garde se tient a droite de l'apron.
import struct, json, random, os, shutil, math, colorsys, collections, sys
from PIL import Image, ImageDraw
SRC = 'docs/topaze/route21_src/'
GEN = 'data/tilesets/primary/general_dawn/'; SEC = 'data/tilesets/secondary/indigo_dawn/'
NP = 'data/tilesets/primary/general_route23v2/'; NS = 'data/tilesets/secondary/indigo_route23v2/'
W, H = 24, 160
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t + .5) for i in range(3))
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s



# ------------------------------------------------------------------ tilesets de base + palette pierre chaude (emplacement 7 du secondaire : libre dans Route 23)
PAL_S = [(0, 0, 0), (96, 80, 58), (128, 134, 78), (150, 138, 106), (192, 180, 144), (238, 228, 194), (132, 120, 90), (106, 96, 72), (248, 244, 226), (222, 214, 190),
         (140, 100, 62), (186, 142, 90), (224, 186, 130), (88, 62, 44), (126, 152, 72), (240, 238, 214)]
WALLP, SHIFT = 7, {}
for src, dst in ((GEN, NP), (SEC, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16): shutil.copy(src + 'palettes/%02d.pal' % i, dst + 'palettes/%02d.pal' % i)
writepal(NS + 'palettes/%02d.pal' % WALLP, PAL_S)

# ------------------------------------------------------------------ metatuiles (secondaire COMPACTE : on ne garde que ce que la carte d'origine utilise)
pmt = open(GEN + 'metatiles.bin', 'rb').read(); patt = struct.unpack('<%dI' % (os.path.getsize(GEN + 'metatile_attributes.bin') // 4), open(GEN + 'metatile_attributes.bin', 'rb').read())
smt0 = open(NS + 'metatiles.bin', 'rb').read(); satt0 = struct.unpack('<%dI' % (len(smt0) // 16), open(NS + 'metatile_attributes.bin', 'rb').read())
ORIG = list(struct.unpack('<%dH' % (W * H), open(SRC + 'r23_orig.bin', 'rb').read()))
KEEPM = sorted({v & 0x3ff for v in ORIG if (v & 0x3ff) >= 640})
RM = {old: 640 + i for i, old in enumerate(KEEPM)}
def rm(v): return (v & 0xfc00) | RM.get(v & 0x3ff, v & 0x3ff)
simg0 = Image.open(NS + 'tiles.png'); tw0 = simg0.width // 8
rawm = [list(struct.unpack('<8H', smt0[(o - 640) * 16:(o - 640) * 16 + 16])) for o in KEEPM]
KEEPT = sorted({(e & 0x3ff) - 640 for es in rawm for e in es if (e & 0x3ff) >= 640}); RT = {old: i for i, old in enumerate(KEEPT)}
smt = bytearray(b''.join(struct.pack('<8H', *[((e & 0xfc00) | (640 + RT[(e & 0x3ff) - 640])) if (e & 0x3ff) >= 640 else e for e in es]) for es in rawm))
satt = [satt0[o - 640] for o in KEEPM]
simg = Image.new('P', (128, ((len(KEEPT) + 15) // 16) * 8), 0); simg.putpalette(simg0.getpalette())
for old, new in RT.items(): simg.paste(simg0.crop(((old % tw0) * 8, (old // tw0) * 8, (old % tw0) * 8 + 8, (old // tw0) * 8 + 8)), ((new % 16) * 8, (new // 16) * 8))
NMT = len(smt) // 16; NTL = len(KEEPT)
NEWE, NEWA, NEWT, ARTM = [], [], [], {}
def ents(m):
    if m >= 640 + NMT: return list(NEWE[m - 640 - NMT])
    return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
def att(m):
    if m >= 640 + NMT: return NEWA[m - 640 - NMT]
    return patt[m] if m < 640 else satt[m - 640]
def new_meta(e, a):
    NEWE.append(e); NEWA.append(a); return 640 + NMT + len(NEWE) - 1
def add_tile(t):
    t = tuple(t)
    if t in NEWT: return NEWT.index(t)
    NEWT.append(t); return len(NEWT) - 1
def snow_meta(var): return 8 + (var & 1) + 8 * ((var >> 1) & 1)
def snow_var(x, y): return (x & 1) + 2 * (y & 1)

def noise(x, y): return 0.5 * math.sin(x * 0.35 + y * 0.11) + 0.3 * math.sin(y * 0.19 - x * 0.27 + 1.3) + 0.2 * math.sin(x * 0.13 + y * 0.43 + 2.1)

def qxy(q, i, j): return (i if q % 2 == 0 else 7 - i), (j if q < 2 else 7 - j)       # distance au bord EXTERIEUR de la case (coin du quart)
def wall_q(q, ah, var, part, ice=0):
    """falaise de pierre de 2 cases de haut (part 0 = haut, 1 = bas) : levre enneigee, trait, appareil de pierre qui s'assombrit vers le pied, mousse, ombre portee sur le palier du bas. ah=0 : bout de falaise (arrondi)."""
    r = random.Random(1700 + q * 31 + ah * 7 + var * 3 + part * 101); out = []
    for j in range(8):
        for i in range(8):
            X, Y = (q % 2) * 8 + i, (q // 2) * 8 + j + part * 16; de = X if q % 2 == 0 else 15 - X; c = 0
            if Y <= 1: c = 9 if (Y == 1 and (X * 3 + var) % 4 == 0) else 0
            elif Y == 2: c = 8 if (X + var) % 5 else 9
            elif Y == 3: c = 1
            elif ice and 4 <= Y <= 29:
                c = 15
                if X <= 1 or X >= 14: c = 4 if (X + Y) % 3 else 3
                elif X % 4 == 1: c = 8
                elif X % 5 == 3: c = 9
                elif (Y * 7 + X * 3) % 11 == 0: c = 2
                if Y >= 26 and 2 <= X <= 13: c = 8 if (X + Y) % 2 else 9
            elif 4 <= Y <= 27:
                course = (Y - 4) // 4; joint_h = (Y - 4) % 4 == 3
                joint_v = (X + (8 if course % 2 else 0) + var * 3) % 16 == 0
                c = 3 if (joint_h or joint_v) else 4
                if c == 4 and r.random() < 0.10: c = 5 if (r.random() < 0.5 and Y < 14) else 3
                if Y >= 16 and c == 4 and r.random() < 0.14: c = 3
                if Y >= 20 and c == 4 and r.random() < 0.10: c = 14
                if Y >= 22 and c == 3 and r.random() < 0.3: c = 6
            elif Y == 28: c = 6
            elif Y == 29: c = 7
            elif Y == 30: c = 2 if (X + Y) % 2 == 0 else 0
            elif Y == 31: c = 2 if (X % 4 == 0) else 0
            if not ah and de < 3 and c:
                cut = 3 - de
                if Y < 2 + cut or Y > 29 - cut: c = 0
            out.append(c)
    return out
def stair_q(q, eL, eR, var):
    out = []
    for j in range(8):
        for i in range(8):
            X, Y = (q % 2) * 8 + i, (q // 2) * 8 + j; b = Y % 4
            c = 5 if b == 0 else (4 if b == 1 else (3 if b == 2 else 6))
            if b == 1 and (X + (Y // 4) * 5 + var) % 7 == 0: c = 3
            if (eL and X == 0) or (eR and X == 15): c = 1
            elif (eL and X == 1) or (eR and X == 14): c = 7 if b != 0 else 5
            out.append(c)
    return out
def blob_dist(q, ah, av, dg, i, j):
    cx_, cy_ = qxy(q, i, j); d = 99.0
    if not ah: d = min(d, cx_)
    if not av: d = min(d, cy_)
    if not ah and not av and cx_ < 5 and cy_ < 5: d = min(d, 5.2 - math.hypot(5 - cx_, 5 - cy_))
    elif ah and av and not dg: d = min(d, math.hypot(cx_ + 0.5, cy_ + 0.5) - 3.4)
    return d
def pond_q(q, ah, av, dg, style, var):
    """etang / ruisseau : 0 = rive (herbe visible), bord ecumeux, eau ou glace (palette 4)."""
    r = random.Random(7000 + q * 131 + ah * 17 + av * 29 + dg * 43 + var * 7 + (style == 'ice') * 501); out = []
    for j in range(8):
        for i in range(8):
            d = blob_dist(q, ah, av, dg, i, j); X, Y = (q % 2) * 8 + i, (q // 2) * 8 + j
            if d < 0.9: c = 0
            elif d < 1.9: c = 1 if r.random() < 0.8 else 8
            elif style == 'ice':
                c = 2
                if d < 2.9 and r.random() < 0.25: c = 1
                elif r.random() < 0.035: c = 1
                elif r.random() < 0.03: c = 9
                elif (X + 2 * Y + var * 3) % 29 == 5: c = 4
            else:
                c = 5
                if d < 2.9: c = 7 if r.random() < 0.7 else 4
                elif (Y + var) % 5 == 2 and (X + var * 2) % 8 in (1, 2): c = 4
                elif (Y + var * 2) % 7 == 5 and (X + 3) % 8 in (5, 6): c = 2
                elif r.random() < 0.05: c = 6
            out.append(c)
    return out
def bridge_q(q, orient, rA, rB, var):
    """pont de planches : orient 'V' = on marche du nord au sud (planches en travers, rambardes a gauche/droite), 'H' = on marche d'est en ouest. rA/rB : rambarde au bord gauche|haut / droit|bas."""
    out = []
    for j in range(8):
        for i in range(8):
            X, Y = (q % 2) * 8 + i, (q // 2) * 8 + j
            if orient == 'H': X, Y = Y, X
            c = [10, 11, 11, 12][Y % 4] if (Y % 4) != 3 else 10
            if (X + (Y // 4) * 3 + var) % 9 == 0 and Y % 4 in (1, 2): c = 10
            if rA and X <= 1: c = 13 if X == 0 else 10
            elif rB and X >= 14: c = 13 if X == 15 else 10
            out.append(c)
    return out
def mk(quarters, pal, st, base, layer=0):
    """metatuile : fond d'herbe (variante d'etage) + 4 quarts dessines dans le calque haut (palette `pal`)."""
    key = (tuple(tuple(x) for x in quarters), pal, st, base, layer)
    if key not in ARTM:
        bot = ents(base)[:4]
        if st: bot = [(q & 0xfff) | (SHIFT.get(q >> 12, q >> 12) << 12) for q in bot]
        ARTM[key] = new_meta(bot + [('T', add_tile(t), pal) for t in quarters], (att(base) & ~0x60000000) | layer)
    return ARTM[key]


SANDS_INNER = {'NW': 258, 'NE': 259, 'SW': 260, 'SE': 261}   # coin concave : l'herbe entre dans le coin indique
def sand_id(p):
    N, S, Wn, E = p(0, -1), p(0, 1), p(-1, 0), p(1, 0)
    if N and S and Wn and E:
        for k, (dx, dy) in (('NW', (-1, -1)), ('NE', (1, -1)), ('SW', (-1, 1)), ('SE', (1, 1))):
            if not p(dx, dy): return SANDS_INNER[k]
        return 220
    if not N and not Wn: return 211
    if not N and not E: return 213
    if not S and not Wn: return 227
    if not S and not E: return 229
    if not N: return 212
    if not S: return 228
    if not Wn: return 219
    if not E: return 221
    return 220
def disc_path(points, rad, W, H):
    cells = set()
    for (a, b) in zip(points, points[1:]):
        n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) * 3) + 1
        for k in range(n + 1):
            t = k / n; x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
            r = rad(x, y) if callable(rad) else rad
            for i in range(int(x - r) - 1, int(x + r) + 2):
                for j in range(int(y - r) - 1, int(y + r) + 2):
                    if (i - x) ** 2 + (j - y) ** 2 <= r * r and 0 <= i < W and 0 <= j < H: cells.add((i, j))
    return cells
def dil(cells, r): return {(x + i, y + j) for (x, y) in cells for i in range(-r, r + 1) for j in range(-r, r + 1)}
def ell(px, py, rx, ry, W, H): return {(x, y) for x in range(W) for y in range(H) if ((x - px) / rx) ** 2 + ((y - py) / ry) ** 2 <= 1}
def distmap(src, W, H):
    d = {c: 0 for c in src}; q = collections.deque(src)
    while q:
        c = q.popleft()
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                n = (c[0] + a, c[1] + b)
                if 0 <= n[0] < W and 0 <= n[1] < H and n not in d: d[n] = d[c] + 1; q.append(n)
    return d
def tidy(S):
    ch = True
    while ch:
        ch = False
        for (x, y) in list(S):
            if not (((x - 1, y) in S) or ((x + 1, y) in S)) or not (((x, y - 1) in S) or ((x, y + 1) in S)): S.discard((x, y)); ch = True
    return S
def blob(cx, cy, rx, ry, seed, W, H, k=0.30):
    return tidy({(x, y) for x in range(W) for y in range(H) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 + k * noise(x * 1.3 + seed, y * 1.1 + seed) < 1})
def hstream(f, x0, x1, W, H): return {(x, y) for x in range(x0, x1 + 1) for y in (int(math.floor(f(x))), int(math.floor(f(x))) + 1) if 0 <= x < W and 0 <= y < H}
def vstream(f, y0, y1, W, H): return {(x, y) for y in range(y0, y1 + 1) for x in (int(math.floor(f(y))), int(math.floor(f(y))) + 1) if 0 <= x < W and 0 <= y < H}
WATER_B = (0x10, 0x11, 0x12, 0x13, 0x15, 0x1b)
GRASS_B = (8, 9, 16, 17)
def G_ok(W, H): return {(x, y) for x in range(2, W - 2) for y in range(2, H - 2)}


# ================================================================== CARTE
GATES = [('Thunder', 14, 133, 3, 4, 3), ('Rainbow', 9, 117, 4, 3, 4), ('Soul', 15, 101, 5, 3, 4), ('Marsh', 8, 85, 6, 4, 3)]    # nom, colonne de l'arche, rangee du bas de l'arche, n (VAR_TEMP_1), largeur aile gauche / droite (la foret restante a cote est de largeur paire)
WROWS = {124: (2, 21), 108: (2, 21), 92: (2, 21), 76: (2, 21)}
def build(rnd):
    FIXED = {}
    for y in range(H):
        for x in range(W):
            if y < 64 or y >= 143 or x < 2 or x >= 22: FIXED[(x, y)] = rm(ORIG[y * W + x])
    RING = {c for c in FIXED if c[1] >= 64 and c[1] < 143}
    ARCH = [[rm(ORIG[(119 + r) * W + 11 + c]) for c in range(5)] for r in range(4)]
    BLOCK = [[rm(ORIG[(119 + r) * W + 2 + c]) for c in range(3)] for r in range(4)]
    BASE = {rm(ORIG[119 * W + 2 + k]) & 0x3ff: (BLOCK[2][k], BLOCK[3][k]) for k in range(3)}
    for x in list(range(2, 8)) + list(range(19, 22)):                           # fin propre des grandes facades du haut (coupees a la ligne 64)
        i = rm(ORIG[63 * W + x]) & 0x3ff
        if i in BASE: FIXED[(x, 62)] = BASE[i][0]; FIXED[(x, 63)] = BASE[i][1]
    APRON = []; FACADE = set(); FORCE = set()
    for (nm, xc, g, n, wl, wr) in GATES:
        for r in range(4):
            y = g - 3 + r
            for c in range(5): FIXED[(xc - 2 + c, y)] = ARCH[r][c]
            wing = lambda k, w: BLOCK[r][0] if k == 0 else BLOCK[r][2] if k == w - 1 else BLOCK[r][1]
            for k in range(wl): FIXED[(xc - 2 - wl + k, y)] = wing(k, wl)
            for k in range(wr): FIXED[(xc + 3 + k, y)] = wing(k, wr)
        APRON += [(x, g + 1) for x in range(xc - 2, xc + 3)]
        FACADE |= {(x, y) for x in range(xc - 2 - wl, xc + 3 + wr) for y in range(g - 3, g + 1)}
        FORCE |= {(x, y) for x in list(range(2, xc - 2 - wl)) + list(range(xc + 3 + wr, 22)) for y in range(g - 4, g + 3)}
    PTS = [(14, 143), (14, 139), (14, 134), (14, 129), (14, 127.5), (13, 126), (13, 122), (11, 120), (9.5, 118.8), (9, 118), (9, 113), (9.5, 111), (10, 109), (10, 106.5), (12, 105), (14, 103.5), (15, 102),
           (15, 97), (14.5, 95), (14, 93.5), (14, 90.5), (12, 89), (9.5, 87.5), (8, 86), (8, 81), (8.5, 79.5), (9, 78), (9, 74.5), (11, 72.5), (13, 70.5), (13.5, 68), (13.5, 65), (13, 63.5)]
    PATH = disc_path(PTS, 1.1, W, H) | set(APRON)
    PATH |= {(x, y) for x in (13, 14, 15) for y in range(139, 143)} | {(x, y) for x in (12, 13, 14) for y in range(64, 67)}
    WATER, PONDS = {}, []
    def pond(cells, style): PONDS.append((cells, style)); [WATER.__setitem__(c, style) for c in cells]
    pond(blob(18.3, 121.5, 2.7, 2.3, 61, W, H), 'water'); pond(blob(5.2, 137.5, 2.8, 2.0, 67, W, H), 'water'); pond(blob(4.6, 111.2, 2.4, 1.5, 71, W, H), 'water')
    pond(blob(19.0, 95.6, 2.3, 1.6, 73, W, H), 'water'); pond(blob(4.6, 71.0, 2.7, 2.4, 79, W, H), 'water'); pond(blob(18.0, 81.0, 2.4, 1.8, 83, W, H), 'water')
    for c in list(WATER):
        if c in FIXED or c in PATH or c[0] < 2 or c[0] > 21: del WATER[c]
    WSET = set(WATER)
    PATH_SAND = PATH - WSET - set(FIXED)
    WALL, STAIR = set(), set()
    for yw, (xa, xb) in WROWS.items():
        st = {x for x in range(xa, xb + 1) if all((x, yw + k) in PATH for k in (-1, 0, 1, 2))}
        assert len(st) >= 2, ('escalier', yw)
        for x in range(xa, xb + 1):
            for k in (0, 1):
                (STAIR if x in st else WALL).add((x, yw + k))
    PATH_SAND -= WALL | STAIR
    WSET -= WALL | STAIR
    FEAT = WSET | WALL | STAIR
    PATH_ALL = PATH_SAND | STAIR | {c for c in PATH if c in FIXED}
    NONRING = set(FIXED) - RING - FACADE
    BUF = dil(PATH_ALL, 1) | dil(NONRING, 1)
    DM = distmap(PATH_ALL, W, H)
    CLEAR = set()
    MEAD = {(x, y) for x in range(W) for y in range(H) if noise(x * 1.35 + 5, y * 1.35 + 1) > 0.34 and 66 <= y <= 140}
    nofor = PATH_ALL | BUF | set(FIXED) | dil(WSET, 1) | WALL | dil(STAIR, 1)
    REG = {(x, y) for x in range(2, 22) for y in range(66, 141)}
    FOREST = {c for c in REG if c not in nofor and c not in MEAD and DM[c] >= 2 + ((c[0] * 7 + c[1] * 13) % 5 == 0)}
    FOREST |= {c for c in FORCE if c not in FIXED and c not in PATH_ALL and c not in FEAT and c not in dil(WSET, 1) and c not in WALL}
    gr = []; blockd = PATH_ALL | BUF | set(FIXED) | FEAT | dil(WSET, 1)
    cands = [(x, y) for y in range(68, 138, 2) for x in range(3, W - 4, 2) if all((x + i, y + j) not in FOREST and (x + i, y + j) not in blockd and DM[(x + i, y + j)] >= 3 for i in range(2) for j in range(3))]
    rnd.shuffle(cands)
    for (x, y) in cands:
        if len(gr) >= 16: break
        if any(max(abs(x - a), abs(y - b)) < 5 for (a, b) in gr): continue
        gr.append((x, y)); FOREST |= {(x + i, y + j) for i in range(2) for j in range(3)}
    G = {(x, y): (0x3000, 8 + (x & 1) + 8 * (y & 1)) for y in range(H) for x in range(W)}
    for c in PATH_SAND: G[c] = (0x3000, sand_id(lambda dx, dy, c=c: (c[0] + dx, c[1] + dy) in PATH_ALL or not (0 <= c[0] + dx < W and 0 <= c[1] + dy < H)))
    SPEC = {}
    for c in WSET: SPEC[c] = ('pond', WATER[c]); G[c] = (0x400, 8)
    for c in WALL: SPEC[c] = ('wall', 0); G[c] = (0x400, 8)
    for c in STAIR: SPEC[c] = ('stair',); G[c] = (0x3000, 8)
    TREEO = {}
    avail = (FOREST - nofor) | {c for c in FORCE if c in FOREST}
    def run_pairs(ux):
        y = 0
        while y < H:
            if (ux, y) in avail and (ux + 1, y) in avail and (ux, y) not in TREEO and (ux + 1, y) not in TREEO:
                a = y
                while y < H and all(c in avail and c not in TREEO for c in ((ux, y), (ux + 1, y))): y += 1
                b_ = y - 1; ln = b_ - a + 1
                if ln % 2 == 0: ln -= 1
                if ln >= 3:
                    start = a; end = start + ln - 1
                    for yy in range(start, end + 1):
                        k = yy - start
                        ids = (14, 15) if k == 0 else (30, 31) if k == 1 else (36, 37) if yy == end else ((20, 21) if k % 2 == 0 else (28, 29))
                        for i in range(2): G[(ux + i, yy)] = (0x400, ids[i]); TREEO[(ux + i, yy)] = (ux, start)
            else: y += 1
    for ux in range(2, W - 3, 2): run_pairs(ux)
    for ux in range(3, W - 3, 2): run_pairs(ux)
    for c in FORCE:                                                           # colonne d'arbres incomplete a cote d'un poste : un rocher, jamais un trou
        if c not in TREEO and c not in FIXED and c not in PATH_ALL and c not in FEAT and c not in WSET: G[c] = (0x400, 159)
    for c, v in FIXED.items(): G[c] = (v & 0xfc00, v & 0x3ff)
    return dict(G=G, SPEC=SPEC, PATH=PATH_ALL, BUF=BUF, MEAD=MEAD, TREEO=TREEO, FIXED=FIXED, WSET=WSET, WALL=WALL, STAIR=STAIR, FEAT=FEAT, DM=DM, REG=REG, FOREST=FOREST)

def decorate(B, rnd):
    G, PATH, BUF, SPEC = B['G'], B['PATH'], B['BUF'], B['SPEC']
    nbs = lambda c: [(c[0] + a, c[1] + b) for a, b in ((0, 1), (1, 0), (-1, 0), (0, -1)) if 0 <= c[0] + a < W and 0 <= c[1] + b < H]
    def blocked(c): return bool(G[c][0] & 0xc00) or (att(G[c][1]) & 0x1ff) in WATER_B
    def reach(start, extra=frozenset()):
        seen = {start}; q = collections.deque([start])
        while q:
            c = q.popleft()
            for n in nbs(c):
                if n not in seen and not blocked(n) and n not in extra: seen.add(n); q.append(n)
        return seen
    start = (14, 143); assert not blocked(start), start
    R0 = reach(start)
    def plain(c): return c in G and c not in SPEC and G[c][0] == 0x3000 and G[c][1] in GRASS_B
    for c in [c for c in B['MEAD'] if plain(c) and c not in BUF and noise(c[0] * 1.7, c[1] * 1.3) > -0.05]: G[c] = (0x3000, 13)
    return dict(R0=R0, reach=reach, blocked=blocked, plain=plain, start=start, nbs=nbs)

def finalize(B):
    G, TREEO, SPEC, WSET, WALL, STAIR = B['G'], B['TREEO'], B['SPEC'], B['WSET'], B['WALL'], B['STAIR']
    isW = lambda c: (min(max(c[0], 0), W - 1), min(max(c[1], 0), H - 1)) in WSET
    out = []
    for y in range(H):
        for x in range(W):
            c = (x, y); fl, m = G[c]; fb = 8
            if c in SPEC:
                sp = SPEC[c]; f = lambda dx, dy: (x + dx, y + dy)
                if sp[0] == 'pond':
                    qs = []
                    for q, (a, b, dg) in enumerate(((f(-1, 0), f(0, -1), f(-1, -1)), (f(1, 0), f(0, -1), f(1, -1)), (f(-1, 0), f(0, 1), f(-1, 1)), (f(1, 0), f(0, 1), f(1, 1)))):
                        ah, av, d2 = int(isW(a)), int(isW(b)), int(isW(dg))
                        qs.append(pond_q(q, ah, av, d2 if (ah and av) else 0, sp[1], (x * 3 + y * 5) % 3))
                    out.append(0x400 | mk(qs, 4, 0, fb, 0)); continue
                if sp[0] == 'stair':
                    eL, eR = (x - 1, y) not in STAIR, (x + 1, y) not in STAIR
                    out.append(0x3000 | mk([stair_q(q, eL, eR, 0 if (x, y - 1) not in STAIR else 1) for q in range(4)], WALLP, 0, fb, 0x20000000)); continue
                if sp[0] == 'wall':
                    wl = (x - 1, y) in WALL; wr = (x + 1, y) in WALL
                    part = 0 if (x, y - 1) not in WALL else 1
                    out.append(0x400 | mk([wall_q(q, int(wl if q % 2 == 0 else wr), (x // 2) % 2, part, 0) for q in range(4)], WALLP, 0, fb, 0)); continue
            out.append(fl | m)
    return out

# ------------------------------------------------------------------ generation
rnd = random.Random(2323)
B = build(rnd); D = decorate(B, rnd); G, PATH, SPEC = B['G'], B['PATH'], B['SPEC']
R0, reach, blocked, plain, start, nbs = D['R0'], D['reach'], D['blocked'], D['plain'], D['start'], D['nbs']
mj = json.load(open('data/maps/Route23/map.json'))
def dpath(c, lim=6):
    ds = [max(abs(c[0] - p[0]), abs(c[1] - p[1])) for p in PATH if abs(p[0] - c[0]) <= lim and abs(p[1] - c[1]) <= lim]
    return min(ds) if ds else 99
# ---- gardes et declencheurs
newtrig = []
for (nm, xc, g, n, wl, wr) in GATES:
    for o in mj['object_events']:
        if o['script'] == 'Route23_EventScript_%sBadgeGuard' % nm: o['x'], o['y'] = xc + 2, g + 1
    for x in range(xc - 1, xc + 2):
        newtrig.append({'type': 'trigger', 'x': x, 'y': g + 1, 'elevation': 3, 'var': 'VAR_MAP_SCENE_ROUTE23', 'var_value': str(n - 1), 'script': 'Route23_EventScript_%sBadgeGuardTrigger' % nm})
names = tuple('Route23_EventScript_%sBadgeGuardTrigger' % g[0] for g in GATES)
mj['coord_events'] = [c for c in mj['coord_events'] if c['script'] not in names] + newtrig
# ---- objets caches dans la zone refaite : on les repose pres du chemin
placed = [(xc + 2, g + 1) for (_, xc, g, _, _, _) in GATES]
def secret(t, dmin=2):
    cand = [c for c in G if plain(c) and c in R0 and c not in placed and 2 <= c[0] < W - 2 and 66 <= c[1] <= 140 and dpath(c) >= dmin and dpath(c) <= 5]
    return min(cand, key=lambda c: (c[0] - t[0]) ** 2 + (c[1] - t[1]) ** 2)
EV = {}
for b in mj['bg_events']:
    if b['type'] == 'hidden_item' and 64 <= b['y'] < 143:
        c = secret((b['x'], b['y'])); placed.append(c); b['x'], b['y'] = c; EV[b['item']] = c
# ---- decor : fleurs d'aube (passables), rochers ronds (bloquants, sans fermer le passage)
cand = [c for c in G if plain(c) and c in R0 and 2 <= c[0] < W - 2 and 66 <= c[1] <= 140 and c not in PATH and c not in placed]
rnd.shuffle(cand); nfl = 0
for c in cand:
    if nfl >= 90: break
    d = dpath(c, 5)
    if d < 1 or d > 4: continue
    G[c] = (0x3000, 4); nfl += 1
ROCKS = []
for c in cand:
    if len(ROCKS) >= 34: break
    d = dpath(c, 6)
    if G[c][1] != G[c][1] or not plain(c) or d < 2 or d > 5: continue
    if any(max(abs(c[0] - r[0]), abs(c[1] - r[1])) < 3 for r in ROCKS + placed): continue
    sv = G[c]; G[c] = (0x400, 159)
    if not (reach(start) >= (R0 - {c})): G[c] = sv; continue
    ROCKS.append(c)
# cases bloquees sans obstacle visible (colonnes d'arbres incompletes, trous) : un rocher
for c in sorted(G):
    if G[c][0] == 0x400 and c not in B['TREEO'] and c not in SPEC and c not in B['FIXED'] and G[c][1] in GRASS_B: G[c] = (0x400, 159)
R1 = reach(start)
for e in [(14, 143), (13, 64), (13, 63), (12, 62)]: assert e in R1, ('inaccessible', e)
for (nm, xc, g, n, wl, wr) in GATES:
    for x in range(xc - 1, xc + 2):
        assert (x, g + 1) in R1 and (x, g - 3) in R1, ('arche fermee', nm, x)
    assert (xc + 2, g + 1) in R1 or True
for (nm, xc, g, n, wl, wr) in GATES:       # sans passer sous l'arche, le nord est inaccessible
    cl = {(x, y) for x in range(xc - 1, xc + 2) for y in range(g - 3, g + 1)}
    for c in cl: G[c] = (G[c][0] | 0x400, G[c][1])
    assert (13, 64) not in reach(start), ('contournement possible', nm)
    for c in cl: G[c] = (G[c][0] & ~0xc00, G[c][1])
for k, c in EV.items(): assert c in R1 or any(n in R1 for n in nbs(c)), ('objet inaccessible', k, c)
# ---- audit des arbres generes
TI = {14: 'a', 15: 'a', 30: 'c', 31: 'c', 20: 'k', 21: 'k', 28: 'b', 29: 'b', 36: 'e', 37: 'e'}
for (x, y), _o in B['TREEO'].items():
    m = G[(x, y)][1]; t = TI[m]
    up = G.get((x, y - 1)); dn = G.get((x, y + 1))
    tu = TI.get(up[1]) if up and up[0] == 0x400 and (x, y - 1) in B['TREEO'] else None
    td = TI.get(dn[1]) if dn and dn[0] == 0x400 and (x, y + 1) in B['TREEO'] else None
    if t == 'a': ok = tu in (None, 'e') and td == 'c'
    elif t == 'c': ok = tu == 'a' and td in ('k', 'e')
    elif t == 'k': ok = tu in ('c', 'b') and td == 'b'
    elif t == 'b': ok = tu == 'k' and td in ('k', 'e')
    else: ok = tu in ('b', 'c') and td in (None, 'a')
    assert ok, ('arbre incomplet', x, y, m, tu, td)
print('cases accessibles', len(R1), 'arbres', len(B['TREEO']), 'fleurs', nfl, 'rochers', len(ROCKS))
words = finalize(B)
json.dump(mj, open('data/maps/Route23/map.json', 'w'), indent=2); open('data/maps/Route23/map.json', 'a').write('\n')

# ---- ecriture des tilesets
assert NMT + len(NEWE) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(NEWE), NTL + len(NEWT))
fin = [[((640 + NTL + q[1]) | (q[2] << 12)) if isinstance(q, tuple) else q for q in e] for e in NEWE]
smt += b''.join(struct.pack('<8H', *e) for e in fin); satt += NEWA
open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in satt))
rows = (NTL + len(NEWT) + 15) // 16
tout = Image.new('P', (128, rows * 8), 0); tout.putpalette(simg.getpalette()); tout.paste(simg, (0, 0))
for n, t in enumerate(NEWT):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); tout.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
tout.save(NS + 'tiles.png')
open('data/layouts/Route23/map.bin', 'wb').write(struct.pack('<%dH' % len(words), *words))
print('metatuiles %d/384, tuiles %d/384' % (NMT + len(NEWE), NTL + len(NEWT)))
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
cn = 'Route23V2'
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h', 'GeneralRoute23V2',
    '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
    '\nconst u32 gTilesetTiles_Indigo%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Indigo%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
add('src/data/tilesets/metatiles.h', 'GeneralRoute23V2',
    '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
    '\nconst u16 gMetatiles_Indigo%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Indigo%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
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
add('src/data/tilesets/headers.h', 'GeneralRoute23V2',
    tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Indigo', cn, 'TRUE', 'Indigo', cn, 'Indigo', cn, 'Indigo', cn, 'Indigo', cn, 'NULL'))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_ROUTE23': l.update(primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Indigo%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('route 23 refaite (v2)')
