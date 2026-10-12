# ROUTES 16 + 17 v2 : CARTES NOUVELLES (v1 = habillage de l'ancien trace, gardee dans la branche route16-v1-reference). « du quartz a l'ametyste » : Route 16 (depart : Bourg Quartz, neige, a l'EST) puis Route 17 (voie cyclable, 160 cases, vers le SUD)
# jusqu'a la Route 18 (arrivee : Amethiolite, lilas). Une seule famille de tilesets (`general_route16` / `celadon_route16`) :
#   - etage 0 = neige de Bourg Quartz (palettes primaires 0..6 de `general_celadopole`),
#   - etage 1 = lilas d'amethyste (palettes de `general_route18` pour les palettes 0, 3, 5 d'origine, rangees dans les emplacements 7, 8, 9),
#   - 10 = palette d'art amethyste, 12 = palette d'art quartz, 11 = voie cyclable (melange).
# L'etage de chaque case suit la distance parcourue depuis Bourg Quartz (route 16 d'est en ouest puis route 17 du nord au sud) + un champ lisse :
# des plaques de lilas apparaissent dans la neige puis prennent le dessus (fonte progressive), la Route 17 finit entierement lilas comme la Route 18.
# Decor : bosquets d'arbres (arbres FR 2x2) et cristaux (quartz cote neige, amethyste cote lilas) dans les prairies, sans jamais couper un acces (BFS).
# Idempotent : part de route21_src/r16_orig.bin / r17_orig.bin. Lancer depuis la racine : python3 docs/topaze/route16_dress.py
import struct, json, random, os, shutil, math, colorsys, collections, sys
from PIL import Image, ImageDraw
SRC = 'docs/topaze/route21_src/'
GEN = 'data/tilesets/primary/general/'; SEC = 'data/tilesets/secondary/celadon_city/'
NP = 'data/tilesets/primary/general_route16/'; NS = 'data/tilesets/secondary/celadon_route16/'
DIMS = {'Route16': (48, 20), 'Route17': (24, 80)}

def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t + .5) for i in range(3))
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s

# ------------------------------------------------------------------ palettes
PAL_A = [(0, 0, 0), (30, 10, 52), (94, 44, 142), (142, 84, 202), (188, 132, 236), (228, 200, 252), (252, 242, 255), (46, 36, 112), (84, 72, 172),
         (132, 122, 222), (198, 192, 250), (40, 30, 66), (214, 64, 152), (176, 168, 192), (96, 88, 118), (255, 246, 200)]
def quartz(c):
    if c == (0, 0, 0): return c
    h, l, s = hls(c); return rgb(196, min(0.97, 0.18 + l * 0.85), min(0.75, 0.25 + s * 0.4))
PAL_Q = [quartz(c) for c in PAL_A]
ART_AME, ART_QTZ, SHIFT = 10, 12, {0: 7, 3: 8, 5: 9}        # emplacements : art amethyste, art quartz ; palette d'origine -> emplacement lilas
for src, dst in ((GEN, NP), (SEC, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    shutil.copytree(src + 'anim', dst + 'anim') if os.path.isdir(src + 'anim') else None
    for i in range(16): shutil.copy(src + 'palettes/%02d.pal' % i, dst + 'palettes/%02d.pal' % i)
for i in range(7): shutil.copy('data/tilesets/primary/general_celadopole/palettes/%02d.pal' % i, NP + 'palettes/%02d.pal' % i)
for i in (4, 6): shutil.copy('data/tilesets/primary/general_route18/palettes/%02d.pal' % i, NP + 'palettes/%02d.pal' % i)      # palettes 4 et 6 = eau (mer, rivages) : bleu profond de la Route 18 partout
for o, sl in SHIFT.items(): writepal(NS + 'palettes/%02d.pal' % sl, readpal('data/tilesets/primary/general_route18/palettes/%02d.pal' % o))
pc, pa = readpal('data/tilesets/secondary/celadon_celadopole/palettes/11.pal'), readpal('data/tilesets/secondary/celadon_route18/palettes/11.pal')
writepal(NS + 'palettes/11.pal', [pc[0]] + [lerp(pc[k], pa[k], .5) for k in range(1, 16)])
writepal(NS + 'palettes/%02d.pal' % ART_AME, PAL_A); writepal(NS + 'palettes/%02d.pal' % ART_QTZ, PAL_Q)

# ------------------------------------------------------------------ metatuiles
pmt = open(GEN + 'metatiles.bin', 'rb').read(); patt = struct.unpack('<%dI' % (os.path.getsize(GEN + 'metatile_attributes.bin') // 4), open(GEN + 'metatile_attributes.bin', 'rb').read())
smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = list(struct.unpack('<%dI' % (len(smt) // 16), open(NS + 'metatile_attributes.bin', 'rb').read()))
NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
def ents(m): return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
def att(m): return patt[m] if m < 640 else satt[m - 640]
NEWE, NEWA, VAR, NEWT = [], [], {}, []
def new_meta(e, a):
    NEWE.append(e); NEWA.append(a); return 640 + NMT + len(NEWE) - 1
def variant(m, st):
    """metatuile m a l'etage st (0 = telle quelle, 1 = palettes 0/3/5 -> lilas)."""
    if st == 0: return m
    if (m, 1) in VAR: return VAR[(m, 1)]
    e = ents(m); out = [(q & 0xfff) | (SHIFT.get(q >> 12, q >> 12) << 12) for q in e]
    VAR[(m, 1)] = m if out == e else new_meta(out, att(m)); return VAR[(m, 1)]
def add_tile(t):
    t = tuple(t)
    if t in NEWT: return NEWT.index(t)
    NEWT.append(t); return len(NEWT) - 1

# ------------------------------------------------------------------ art : petits cristaux (prismes) 16x16
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
    im = newimg(16, 16); d = ImageDraw.Draw(im); d.ellipse((1, 12, 15, 16), fill=11)
    if var == 0: prism(d, 4, 14, 5, 9); prism(d, 9, 15, 7, 14); prism(d, 13, 14, 4, 7)
    elif var == 1: prism(d, 6, 15, 6, 11); prism(d, 12, 14, 5, 8); d.rectangle((1, 13, 3, 14), fill=13); d.point((2, 12), fill=14)
    else: prism(d, 8, 15, 8, 14); d.rectangle((2, 13, 4, 14), fill=13); d.rectangle((12, 12, 14, 14), fill=13); d.point((13, 11), fill=14)
    return im
def slice4(im): return [add_tile(list(im.crop(((q % 2) * 8, (q // 2) * 8, (q % 2) * 8 + 8, (q // 2) * 8 + 8)).getdata())) for q in range(4)]
def big(var):
    im = newimg(32, 32); d = ImageDraw.Draw(im); d.ellipse((1, 24, 31, 32), fill=11)
    if var == 0: prism(d, 9, 28, 8, 17); prism(d, 19, 30, 12, 27); prism(d, 27, 28, 7, 13)
    elif var == 1: prism(d, 7, 29, 9, 19); prism(d, 17, 30, 10, 28); prism(d, 26, 29, 8, 15); d.rectangle((1, 26, 5, 28), fill=13); d.point((3, 25), fill=14)
    else: prism(d, 12, 30, 12, 27); prism(d, 24, 29, 8, 17); prism(d, 4, 28, 5, 11)
    return im
SMT = {('s', v): slice4(small(v)) for v in range(3)}
for v in range(3):
    bi = big(v)
    for q in range(4): SMT[('b', v, q)] = slice4(bi.crop(((q % 2) * 16, (q // 2) * 16, (q % 2) * 16 + 16, (q // 2) * 16 + 16)))
ARTM = {}
def art_meta(var, st, base):
    """case = fond d'herbe (variante d'etage) + cristal (calque haut) ; palette d'art selon l'etage."""
    k = (var, st, base)
    if k not in ARTM:
        sl = ART_AME if st else ART_QTZ; bot = ents(base)[:4]
        if st: bot = [(q & 0xfff) | (SHIFT.get(q >> 12, q >> 12) << 12) for q in bot]
        ARTM[k] = new_meta(bot + [('T', t, sl) for t in SMT[var]], att(base) & ~0x60000000)
    return ARTM[k]

# ------------------------------------------------------------------ etage (fonte neige -> lilas)
def noise(x, y): return 0.5 * math.sin(x * 0.35 + y * 0.11) + 0.3 * math.sin(y * 0.19 - x * 0.27 + 1.3) + 0.2 * math.sin(x * 0.13 + y * 0.43 + 2.1)
def stage(L, x, y):
    W, H = DIMS[L]
    s = (47 - x) / 47 * 0.30 if L == 'Route16' else 0.30 + 0.70 * y / (H - 1)
    j = ((x * 73856093) ^ (y * 19349663)) % 1000 / 1000.0 - 0.5
    return 1 if s + 0.16 * noise(x, y) > 0.60 else 0


# ================================================================== CARTES NOUVELLES
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
WATER_B = (0x10, 0x11, 0x12, 0x13, 0x15, 0x1b)
GRASS_B = (8, 9, 16, 17)

def build(L, rnd):
    W, H = DIMS[L]
    SEA, FIXED, WALL = {}, {}, set()
    if L == 'Route17':
        orig = list(struct.unpack('<%dH' % (24 * 160), open(SRC + 'r17_orig.bin', 'rb').read()))
        def cx(y):
            env = min(1.0, y / 7.0, (H - 1 - y) / 12.0)
            return 9.5 + 2.5 * (y / (H - 1)) ** 1.5 + 3.6 * math.sin(y / 2.7) * env
        PATH = disc_path([(cx(y), y) for y in range(H)], lambda x, y: 1.25 + 0.35 * math.sin(y * 0.7), W, H)
        PATH |= {(x, y) for y in (0, 1) for x in range(8, 12)} | {(x, y) for y in (H - 2, H - 1) for x in range(8, 17)}
        for y in range(H - 14, H):
            for x in list(range(0, 8)) + list(range(17, 24)): SEA[(x, y)] = orig[(y + 80) * 24 + x]
        MEAD = set()
        for k, yc in enumerate((11, 25, 39, 53)): MEAD |= ell(cx(yc) + (7.0 if k % 2 == 0 else -7.0), yc, 5.2, 4.2, W, H)
        BUF = dil(PATH, 1)
        DM = distmap(PATH, W, H)
        FOREST = {(x, y) for y in range(H) for x in range(W) if (x, y) not in PATH | BUF | MEAD and (x, y) not in SEA and DM[(x, y)] >= 2.6 + 1.3 * math.sin(y * 0.9 + x * 0.4)}
    else:
        orig = list(struct.unpack('<%dH' % (48 * 20), open(SRC + 'r16_orig.bin', 'rb').read()))
        PATH = disc_path([(47, 13), (44, 13), (41.5, 10.5), (39, 8), (37, 9.5), (35.5, 12.5), (31, 12.5)], 1.3, W, H)
        PATH |= {(x, y) for x in range(29, 36) for y in (12, 13)}
        PATH |= disc_path([(29, 12.5), (26.5, 14.5), (23.5, 16.2), (21, 14), (18.5, 11), (15.5, 9.2), (12.5, 8), (10.5, 6.6)], 1.3, W, H)
        PATH |= disc_path([(21, 14), (16.5, 15.5), (12.5, 16.5), (10.2, 18), (9.5, 19)], 1.3, W, H)
        PATH |= {(x, y) for y in (17, 18, 19) for x in range(8, 12)} | {(x, 12) for x in (45, 46, 47)} | {(x, 14) for x in (45, 46, 47)}
        for y in (3, 4, 5):
            for x in range(9, 14): FIXED[(x, y)] = orig[y * 48 + x]
        PATH -= set(FIXED)
        WALLU = [(x, y) for x in (30, 32) for y in list(range(0, 12, 2)) + [14, 16, 18]]
        WALL = {(x + i, y + j) for (x, y) in WALLU for i in range(2) for j in range(2)}
        BUF = dil(PATH, 1) | dil(set(FIXED), 1)
        MEAD = ell(21, 5.5, 6, 2.5, W, H) | ell(37, 6.5, 4, 2, W, H) | ell(36, 16, 4, 1.4, W, H) | ell(11.5, 7, 6.5, 4.2, W, H) | ell(7, 14, 3.5, 3.5, W, H)
        DM = distmap(PATH, W, H)
        FOREST = {(x, y) for y in range(H) for x in range(W) if (y <= 2 or y >= 17 or x <= 2 or x >= 44) or ((x, y) not in MEAD and DM[(x, y)] >= 2.6 + 1.3 * math.sin(y * 0.9 + x * 0.4))}
        FOREST |= WALL
        FOREST -= PATH | (BUF - WALL) | set(FIXED)
    FOREST -= set(SEA)
    # ---- bosquets isoles dans les prairies (arbres entiers 2x2, jamais contre le chemin)
    gr = []; blockd = PATH | BUF | set(FIXED) | set(SEA)
    DMP = distmap(PATH, W, H)
    cands = [(x, y) for y in range(4, H - 4, 2) for x in range(4, W - 4, 2) if all((x + i, y + j) not in FOREST and (x + i, y + j) not in blockd and DMP[(x + i, y + j)] >= 3 for i in range(2) for j in range(2))]
    rnd.shuffle(cands)
    for (x, y) in cands:
        if len(gr) >= (11 if L == 'Route16' else 16): break
        if any(max(abs(x - a), abs(y - b)) < 5 for (a, b) in gr): continue
        gr.append((x, y)); FOREST |= {(x + i, y + j) for i in range(2) for j in range(2)}
        if rnd.random() < 0.6:                                   # parfois un second arbre accole (paire)
            for (dx, dy) in rnd.sample([(2, 0), (-2, 0), (0, 2), (0, -2)], 4):
                cs2 = {(x + dx + i, y + dy + j) for i in range(2) for j in range(2)}
                if all(c in G_ok(W, H) and c not in FOREST and c not in blockd and DMP[c] >= 3 for c in cs2): FOREST |= cs2; break
    G = {(x, y): (0x3000, 8 + (x & 1) + 8 * (y & 1)) for y in range(H) for x in range(W)}
    for c in PATH: G[c] = (0x3000, sand_id(lambda dx, dy, c=c: (c[0] + dx, c[1] + dy) in PATH or not (0 <= c[0] + dx < W and 0 <= c[1] + dy < H)))
    TREEO, TREES = {}, []
    def put_tree(x, y):
        cs = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        for c, m in zip(cs, (28, 29, 20, 21)): G[c] = (0x400, m); TREEO[c] = (x, y)
        TREES.append((x, y))
    if L == 'Route16':
        for (x, y) in WALLU: put_tree(x, y)
    nofor = PATH | BUF | set(FIXED) | set(SEA)
    for uy in range(0, H, 2):                       # reseau de 2x2 aligne : masses d'arbres nettes, jamais de trou d'une case
        for ux in range(0, W, 2):
            cs = [(ux, uy), (ux + 1, uy), (ux, uy + 1), (ux + 1, uy + 1)]
            if sum(c in FOREST for c in cs) >= 3 and not any(c in nofor or c in TREEO for c in cs): put_tree(ux, uy)
    assert WALL <= set(TREEO), 'mur de foret incomplet'
    for c, v in FIXED.items(): G[c] = (v & 0xfc00, v & 0x3ff)
    for c, v in SEA.items(): G[c] = (v & 0xfc00, v & 0x3ff)
    return dict(W=W, H=H, G=G, PATH=PATH, BUF=BUF, MEAD=MEAD, TREEO=TREEO, FIXED=FIXED, SEA=SEA, FOREST=FOREST)

def G_ok(W, H): return {(x, y) for x in range(2, W - 2) for y in range(2, H - 2)}
def decorate(L, B, rnd):
    W, H, G, PATH, BUF = B['W'], B['H'], B['G'], B['PATH'], B['BUF']
    nbs = lambda c: [(c[0] + a, c[1] + b) for a, b in ((0, 1), (1, 0), (-1, 0), (0, -1)) if 0 <= c[0] + a < W and 0 <= c[1] + b < H]
    def blocked(c): return bool(G[c][0] & 0xc00) or (att(G[c][1]) & 0x1ff) in WATER_B
    def reach(start, extra=frozenset()):
        seen = {start}; q = collections.deque([start])
        while q:
            c = q.popleft()
            for n in nbs(c):
                if n not in seen and not blocked(n) and n not in extra: seen.add(n); q.append(n)
        return seen
    start = (47, 13) if L == 'Route16' else (9, 0)
    assert not blocked(start), start
    R0 = reach(start)
    def plain(c): return c in G and G[c][0] == 0x3000 and G[c][1] in GRASS_B
    # ---- herbes hautes dans les clairieres
    TALL = [c for c in B['MEAD'] if plain(c) and c not in BUF and noise(c[0] * 1.7, c[1] * 1.3) > 0.12]
    for c in TALL: G[c] = (0x3000, 13)
    # ---- evenements : signes, dresseurs, objets caches
    EV = {}
    def near_path(c, dmin, dmax):
        d = min(max(abs(c[0] - p[0]), abs(c[1] - p[1])) for p in B['PATH'] if abs(p[0] - c[0]) <= dmax and abs(p[1] - c[1]) <= dmax) if any(abs(p[0] - c[0]) <= dmax and abs(p[1] - c[1]) <= dmax for p in B['PATH']) else 99
        return dmin <= d <= dmax
    def pick(target, dmin=2, dmax=2, avoid=(), rad=99):
        cand = [c for c in G if plain(c) and c not in EV.values() and 2 <= c[0] < W - 2 and 2 <= c[1] < H - 2 and near_path(c, dmin, dmax) and c in R0
                and all(max(abs(c[0] - a[0]), abs(c[1] - a[1])) >= 4 for a in avoid) and max(abs(c[0] - target[0]), abs(c[1] - target[1])) <= rad]
        if not cand: return None
        return min(cand, key=lambda c: (c[0] - target[0]) ** 2 + (c[1] - target[1]) ** 2 + rnd.random())
    return dict(R0=R0, reach=reach, blocked=blocked, plain=plain, pick=pick, EV=EV, start=start, nbs=nbs)

def place_all(L, B, D, rnd):
    W, H, G, PATH, BUF, MEAD = B['W'], B['H'], B['G'], B['PATH'], B['BUF'], B['MEAD']
    R0, reach, blocked, plain, pick, EV, start = D['R0'], D['reach'], D['blocked'], D['plain'], D['pick'], D['EV'], D['start']
    mj = json.load(open('data/maps/%s/map.json' % L))
    def face(c):
        p = min(PATH, key=lambda q: (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2)
        dx, dy = p[0] - c[0], p[1] - c[1]
        return ('RIGHT' if dx > 0 else 'LEFT') if abs(dx) >= abs(dy) else ('DOWN' if dy > 0 else 'UP')
    placed = []
    trainers = [o for o in mj['object_events'] if o.get('trainer_type') == 'TRAINER_TYPE_NORMAL']
    if L == 'Route16':
        tg = [(41, 9), (38, 16), (27, 10), (25, 15), (19, 8), (15, 13), (12, 10), (11, 16)]
    else:
        ys = [8, 15, 22, 29, 36, 43, 50, 56, 61, 64]
        tg = [(round(9.5 + 2.5 * (y / (H - 1)) ** 1.5 + 4.6 * math.sin(y / 5.6) * min(1, y / 7, (H - 1 - y) / 12)) + (3 if i % 2 else -3), y) for i, y in enumerate(ys)]
    for o, t in zip(trainers, tg):
        c = pick(t, 2, 2, avoid=placed, rad=8)
        if c is None: c = pick(t, 2, 3, avoid=placed, rad=12)
        assert c, ('dresseur', o['script'], t)
        placed.append(c); EV[o['script']] = c
        o['x'], o['y'] = c; o['movement_type'] = 'MOVEMENT_TYPE_FACE_' + face(c); o['movement_range_x'] = 0; o['movement_range_y'] = 0
        o['trainer_sight_or_berry_tree_id'] = '2'
    # ---- panneaux (tuile de panneau, bloquante)
    keep_bg, signs = [], [b for b in mj['bg_events'] if b['type'] == 'sign']
    if L == 'Route16':
        want = {'Route16_EventScript_RouteSign': (7, 16)}
    else:
        want = {'Route17_EventScript_RouteSign': (11, 70), 'Route17_EventScript_TrainerTips1': (10, 18), 'Route17_EventScript_TrainerTips2': (12, 40)}
    for b in signs:
        if b['script'] not in want: continue
        c = pick(want[b['script']], 2, 2, avoid=placed + list(EV.values()), rad=10)
        assert c, b['script']
        G[c] = (0x400, 2); EV[b['script']] = c; b['x'], b['y'] = c; keep_bg.append(b)
    for b in mj['bg_events']:
        if b['type'] == 'hidden_item':
            if L == 'Route16': keep_bg.append(b); continue
    if L == 'Route17':
        meadc = sorted(c for c in MEAD if plain(c) and c in R0 and c not in B['BUF'] and 3 <= c[0] <= W - 4 and c[1] < H - 16)
        hid = [b for b in mj['bg_events'] if b['type'] == 'hidden_item']
        for i, b in enumerate(hid):
            sel = [c for c in meadc if min([99] + [max(abs(c[0] - a[0]), abs(c[1] - a[1])) for a in placed]) >= 3]
            c = sel[(i * 37 + 11) % len(sel)] if sel else meadc[0]
            placed.append(c); b['x'], b['y'] = c; keep_bg.append(b)
    mj['bg_events'] = keep_bg
    # ---- cristaux
    ART = {}
    if L == 'Route16':
        ART[(31, 12)] = (('s', 1), G[(31, 12)][1]); G[(31, 12)] = (0x400, G[(31, 12)][1])
    def dpath(c, lim=7):
        ds = [max(abs(c[0] - p[0]), abs(c[1] - p[1])) for p in PATH if abs(p[0] - c[0]) <= lim and abs(p[1] - c[1]) <= lim]
        return min(ds) if ds else 99
    BIGO = []
    nbig = 3 if L == 'Route16' else 10
    bc = [(x, y) for y in range(3, H - 4) for x in range(3, W - 5) if all(plain((x + i, y + j)) and (x + i, y + j) in R0 and (x + i, y + j) not in placed for i in range(2) for j in range(2))]
    rnd.shuffle(bc)
    for (x, y) in bc:
        if len(BIGO) >= nbig: break
        cs = [(x + i, y + j) for j in range(2) for i in range(2)]
        if not (2 <= min(dpath(c) for c in cs) and max(dpath(c) for c in cs) <= 6): continue
        if any(max(abs(x - o[0]), abs(y - o[1])) < 5 for o in BIGO) or any(max(abs(x - q[0]), abs(y - q[1])) < 3 for q in list(ART) + placed): continue
        sv = {c: G[c] for c in cs}
        for c in cs: G[c] = (0x400, G[c][1])
        if not (reach(start, set(ART) | set(cs)) >= (R0 - set(ART) - set(cs) - {c for c in R0 if blocked(c)})):
            for c in cs: G[c] = sv[c]
            continue
        v = rnd.randrange(3); BIGO.append((x, y))
        for q, c in enumerate(cs): ART[c] = (('b', v, q), sv[c][1])
    cand = [c for c in G if plain(c) and c in R0 and 2 <= c[0] < W - 2 and 2 <= c[1] < H - 2 and c not in PATH and c not in placed and c not in ART]
    rnd.shuffle(cand); lim = 16 if L == 'Route16' else 60; ncry = 0
    pts = placed + list(EV.values())
    for c in cand:
        if ncry >= lim: break
        d = min(max(abs(c[0] - p[0]), abs(c[1] - p[1])) for p in PATH if abs(p[0] - c[0]) <= 6 and abs(p[1] - c[1]) <= 6) if any(abs(p[0] - c[0]) <= 6 and abs(p[1] - c[1]) <= 6 for p in PATH) else 99
        if d < 2 or d > 5: continue
        if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q in list(ART) + pts): continue
        ART[c] = (('s', rnd.randrange(3)), G[c][1])
        G[c] = (0x400, G[c][1])
        if not (reach(start, set(ART)) >= (R0 - set(ART) - {c for c in R0 if blocked(c)})): del ART[c]; G[c] = (0x3000, G[c][1]); continue
        ncry += 1
    return mj, ART, EV, placed

def finalize(L, B, ART):
    W, H, G, TREEO = B['W'], B['H'], B['G'], B['TREEO']
    ST = {(x, y): stage(L, x, y) for y in range(H) for x in range(W)}
    out = []
    for y in range(H):
        for x in range(W):
            c = (x, y); fl, m = G[c]
            if c in ART:
                v, base = ART[c]; out.append((0x400) | art_meta(v, ST[c], base)); continue
            wat = (att(m) & 0x1ff) in WATER_B
            st = ST[TREEO[c]] if c in TREEO else (1 if wat else ST[c])
            out.append(fl | variant(m, st))
    return out

# ------------------------------------------------------------------ generation
res, MJ = {}, {}
for L in DIMS:
    rnd = random.Random(1616 if L == 'Route16' else 1717)
    B = build(L, rnd); D = decorate(L, B, rnd)
    mj, ART, EV, placed = place_all(L, B, D, rnd)
    # controle d'acces : tous les evenements et sorties atteignables, aucune case perdue
    R1 = D['reach'](D['start'])
    ends = [(9, 19), (10, 6)] if L == 'Route16' else [(9, 79), (12, 79), (16, 79)]
    for e in ends: assert e in R1, ('sortie inaccessible', L, e)
    for k, c in EV.items():
        assert any(n in R1 for n in D['nbs'](c)) or c in R1, ('evenement inaccessible', L, k, c)
    print(L, 'cases accessibles', len(R1), 'arbres', len(B['TREEO']), 'cristaux', len(ART), 'lilas', sum(stage(L, x, y) for y in range(B['H']) for x in range(B['W'])))
    res[L] = finalize(L, B, ART); MJ[L] = mj
# ---- evenements : Route 16 (portes : maison + Bourg Quartz seulement), Route 17 (jonction Route 18 recalee), Bourg Quartz (indices de warp)
m16 = MJ['Route16']
m16['object_events'] = [o for o in m16['object_events'] if o['graphics_id'] != 'OBJ_EVENT_GFX_CUT_TREE']
m16['warp_events'] = [w for w in m16['warp_events'] if w['dest_map'] in ('MAP_ROUTE16_HOUSE', 'MAP_CELADON_CITY')]
m16['bg_events'] = [b for b in m16['bg_events'] if b.get('script') != 'Route16_EventScript_CyclingRoadSign']
m17 = MJ['Route17']
for w in m17['warp_events']: w['y'] = DIMS['Route17'][1] - 1
for L, mj in MJ.items(): json.dump(mj, open('data/maps/%s/map.json' % L, 'w'), indent=2); open('data/maps/%s/map.json' % L, 'a').write('\n')
cj = json.load(open('data/maps/CeladonCity/map.json')); k = 1
for w in sorted((w for w in cj['warp_events'] if w['dest_map'] == 'MAP_ROUTE16'), key=lambda w: w['y']): w['dest_warp_id'] = str(k); k += 1
json.dump(cj, open('data/maps/CeladonCity/map.json', 'w'), indent=2); open('data/maps/CeladonCity/map.json', 'a').write('\n')

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
for L, G in res.items(): open('data/layouts/%s/map.bin' % L, 'wb').write(struct.pack('<%dH' % len(G), *G))
open('data/layouts/Route16/border.bin', 'wb').write(struct.pack('<4H', 28, 29, 20, 21))      # hors carte : foret (et non plus la mer)
print('metatuiles %d/384, tuiles %d/384' % (NMT + len(NEWE), NTL + len(NEWT)))

# ---- enregistrement des tilesets
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
cn = 'Route16'
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h', 'GeneralRoute16',
    '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
    '\nconst u32 gTilesetTiles_Celadon%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Celadon%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
add('src/data/tilesets/metatiles.h', 'GeneralRoute16',
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
add('src/data/tilesets/headers.h', 'GeneralRoute16',
    tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Celadon', cn, 'TRUE', 'Celadon', cn, 'Celadon', cn, 'Celadon', cn, 'Celadon', cn, 'NULL'))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') in ('LAYOUT_ROUTE16', 'LAYOUT_ROUTE17'): l.update(primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Celadon%s' % cn)
    if l.get('id') == 'LAYOUT_ROUTE17': l['height'] = DIMS['Route17'][1]
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('routes 16 et 17 habillees')
