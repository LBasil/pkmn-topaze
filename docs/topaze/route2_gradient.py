# ROUTE 2 « la route du crépuscule » : relie Opanihrum (opale noire, sud) à Pyropia (braise, nord) ; les couleurs glissent de l'opale à la braise
# (ardoise bleu nuit -> violet -> cendre et terre brûlée). Carte entièrement nouvelle (26x56) : deux moitiés séparées par une falaise pleine largeur ;
# on ne passe de l'une à l'autre que par la Forêt de Jade (portails de pierre au sud et au nord de la falaise). Cristaux d'opale -> obsidienne.
# Technique : 3 « étages » de palettes (t=0 grenat, 0.5 mélange, 1 opale). Les métatuiles d'Emeraude utilisées (herbe, arbres, sable...)
# sont recopiées dans le tileset secondaire avec des numéros de palette différents (variantes) ; l'étage de chaque case suit un champ
# lisse + le gradient sud->nord, ce qui donne un fondu progressif.
# Emplacements de palettes : étage0 = primaire 0,2,5 (+ art 6) ; étage1 = primaire 1,3,4 (+ art 10) ; étage2 = secondaire 7,8,9 (+ art 11) ; 12 = panneau.
# Lancer depuis la racine : python3 docs/topaze/route2_gradient.py  puis  route2_events.py
import struct, json, random, sys, colorsys, collections, os, re, math, shutil
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
EM = '../pokeemerald/data/'
PRI = 'data/tilesets/primary/general_dusk/'; SEC = 'data/tilesets/secondary/dusk_road/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
# ------------------------------------------------------------------ teintes : GRENAT (Grenalux) et OPALE NOIRE (Opanihrum)
def tint_garnet(r, g, b):      # (nom conserve) teinte du depart = OPALE NOIRE
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.10 and l > 0.93: return r, g, b
    if s > 0.45 and (h >= 180 or h < 25): return r, g, b
    if 78 <= h <= 175: h = 168 + (h - 120) * 0.12; s = min(1, s * 0.5); l = l * 0.8
    else: h = 232; s = min(0.42, s * 0.55 + 0.10); l = min(1, l * 0.72)
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_opal(r, g, b):        # (nom conserve) teinte d'arrivee = BRAISE (cendre, terre brulee, lave)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.08: return r, g, b
    if 60 <= h <= 180: h = 14 + (h - 120) * 0.1; s = min(0.30, s * 0.45); l = l * 0.58
    elif 25 <= h < 60: h = 18 + (h - 40) * 0.2; s = s * 0.8; l = l * 0.62
    elif 180 < h <= 260: h = 8 + (h - 215) * 0.05; s = 0.9; l = min(0.55, l * 0.9)
    else: h = 12; s = min(1, s * 0.9); l = l * 0.7
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t + .5) for i in range(3))
def hlerp(a, b, t):
    """melange en teinte (HLS), toujours par le violet : opale (170..230) -> violet -> braise (15), au lieu d'un gris boueux en RVB."""
    ha, la, sa = colorsys.rgb_to_hls(*[c / 255 for c in a]); hb, lb, sb = colorsys.rgb_to_hls(*[c / 255 for c in b])
    if sa < 0.06 or sb < 0.06: return lerp(a, b, t)
    dh = hb - ha
    if dh < 0: dh += 1
    h = (ha + dh * t) % 1.0
    r, g, bb = colorsys.hls_to_rgb(h, la + (lb - la) * t, sa + (sb - sa) * t)
    return int(r * 255 + .5), int(g * 255 + .5), int(bb * 255 + .5)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
ORIG = [readpal(EM + 'tilesets/primary/general/palettes/%02d.pal' % i) for i in range(16)]
TS_ = (0.0, 0.5, 1.0)
def desat(c, f):
    h, l, s = colorsys.rgb_to_hls(*[x / 255 for x in c]); r, g, b = colorsys.hls_to_rgb(h, l, s * f)
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def stage_pal(i, t):
    out = [c if k == 0 else lerp(tint_garnet(*c), tint_opal(*c), t) for k, c in enumerate(ORIG[i])]
    if i == 5: out = [out[0]] + [desat(c, 0.35 + 0.45 * t) for c in out[1:]]       # sable : pale au sud (avenue d'Opanihrum), terre brulee au nord
    return out
SLOT = {0: {0: 0, 2: 2, 5: 5, 3: 12}, 1: {0: 1, 2: 3, 5: 4, 3: 12}, 2: {0: 7, 2: 8, 5: 9, 3: 12}}     # palette d'origine -> emplacement, par etage
ART_SLOT = {0: 6, 1: 10, 2: 11}; ROCK_SLOT = 12
PALS = {}                                        # emplacement -> palette
for st in range(3):
    for o, s in SLOT[st].items():
        if o != 3: PALS[s] = stage_pal(o, TS_[st])
PALS[ROCK_SLOT] = stage_pal(3, 0.5)          # roche : meme palette violet-gris sur toute la route
# ------------------------------------------------------------------ metatuiles : variantes par etage
mt = open(EM + 'tilesets/primary/general/metatiles.bin', 'rb').read(); patt = open(EM + 'tilesets/primary/general/metatile_attributes.bin', 'rb').read()
hdr = open('include/constants/metatile_behaviors.h').read()
OKB = {int(m, 16) for m in re.findall(r'#define MB_\w+\s+(0x[0-9A-Fa-f]+)', hdr)}
def conv(v):
    b, layer = v & 0xff, v >> 12
    if b not in OKB: b = 0
    a = b | (layer << 29)
    if b == 0x02: a |= 0x1000200
    elif b in (0x10, 0x11, 0x12, 0x15): a |= 0x22000400
    elif b == 0x13: a |= 0x2000600
    return a
PATT32 = [conv(struct.unpack('<H', patt[i * 2:i * 2 + 2])[0]) for i in range(len(patt) // 2)]
SEC_ENT = []; SEC_ATT = []; VAR = {}
def variant(m, st, special=None):
    """numero de metatuile FireRed pour la metatuile primaire m a l'etage st (etage 0 : la primaire elle-meme si aucune palette ne change)."""
    key = (m, st)
    if key in VAR: return VAR[key]
    e = list(struct.unpack('<8H', mt[m * 16:m * 16 + 16]))
    out = [(q & 0xfff) | (SLOT[st].get(q >> 12, q >> 12) << 12) for q in e]
    if out == e: VAR[key] = m; return m
    SEC_ENT.append(out); SEC_ATT.append(PATT32[m]); VAR[key] = 640 + len(SEC_ENT) - 1
    return VAR[key]
# ------------------------------------------------------------------ carte
W, H = 26, 56
GRASS_M, FLOWER_M, TALL_M = 1, 4, 13
TREE = [[468, 469], [476, 477]]
G = {}; OCC = {}; STG = {}
rnd = random.Random(1010)
def stage_at(x, y):
    if x <= 3 or x >= W - 4 or y <= 3 or y >= H - 4: return stage_smooth(x, y)      # bordure d'arbres : meme etage que les arbres, sans grain
    t = max(0.0, min(1.0, (H - 1 - y) / 26.0))
    n = 0.35 * math.sin(x * 0.55 + y * 0.21) + 0.25 * math.sin(y * 0.37 - x * 0.3) + 0.2 * math.sin(x * 0.23 + y * 0.6)
    j = ((x * 73856093) ^ (y * 19349663)) % 1000 / 1000.0 - 0.5               # grain : fondu irregulier aux frontieres
    return max(0, min(2, int(round(2 * t + n * 0.45 + j * 0.5))))
def stage_smooth(x, y):
    t = max(0.0, min(1.0, (H - 1 - y) / 26.0))
    n = 0.35 * math.sin(x * 0.55 + y * 0.21) + 0.25 * math.sin(y * 0.37 - x * 0.3) + 0.2 * math.sin(x * 0.23 + y * 0.6)
    return max(0, min(2, int(round(2 * t + n * 0.3))))
def put(x, y, raw_flags, m, special=None, st=None):
    st = stage_at(x, y) if st is None else st
    G[(x, y)] = raw_flags | variant(m, st, special)
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            assert 0 <= x + i < W and 0 <= y + j < H, (name, x + i, y + j)
            assert (x + i, y + j) not in OCC, 'chevauchement %s / %s en %s' % (name, OCC[(x + i, y + j)], (x + i, y + j))
            OCC[(x + i, y + j)] = name
for y in range(H):
    for x in range(W): put(x, y, 0x3000, GRASS_M)
TREECELLS = set()
def tree(x, y):
    st = stage_smooth(x, y)
    TREECELLS.update((x + i, y + j) for i in range(2) for j in range(2))
    for j in range(2):
        for i in range(2): put(x + i, y + j, 0x400, TREE[j][i], st=st)
# ---- portes : sud (Opanihrum) x=12..13 ; nord (Pyropia) x=12..13
S_GATE, N_GATE = (12, 13), (12, 13)
for x in range(0, W, 2):
    if x != 12: tree(x, H - 2); tree(x, 0)
for y in range(2, H - 2, 2):
    tree(0, y); tree(W - 2, y)
PATH = set()
WALL_Y0, WALL_Y1 = 28, 33                         # falaise pleine largeur : la foret passe dessous
HS = (12, 26)                       # portails de pierre 3x3 (coin haut-gauche)
DOOR_S, DOOR_N = (13, 33), (13, 26)
RIDGE_Y = [9, 16, 40, 47]
GAPS = [(15, 20), (4, 9), (4, 9), (16, 21)]       # breches (nord -> sud)
WAY_S = [(12, H - 3), (12, H - 5), (18, 50), (18, 44), (6, 43), (6, 37), (13, 36), (13, 34)]
WAY_N = [(12, 25), (9, 25), (6, 20), (6, 13), (17, 12), (17, 6), (13, 3), (13, 1)]
def seg(a, b):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        t = k / max(1, n); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        for i in (0, 1): PATH.add((int(round(x)) + i, int(round(y))))
        PATH.add((int(round(x)) + 1, int(round(y)) + 1))
for W_ in (WAY_S, WAY_N):
    for a_, b_ in zip(W_, W_[1:]): seg(a_, b_)
PATH -= {(HS[0] + i, HS[1] + j) for i in range(3) for j in range(8)}
PATH |= {(12, H - 1), (13, H - 1), (12, H - 2), (13, H - 2), (12, 0), (13, 0), (12, 1), (13, 1)}
def path_id(x, y):
    N = (x, y - 1) in PATH or y == 0; S = (x, y + 1) in PATH or y == H - 1; Wn = (x - 1, y) in PATH; E = (x + 1, y) in PATH
    if N and S and Wn and E: return 289
    if not N and not Wn and S and E: return 280
    if not N and not E and S and Wn: return 282
    if not S and not Wn and N and E: return 296
    if not S and not E and N and Wn: return 298
    if not N and S and Wn and E: return 281
    if not S and N and Wn and E: return 297
    if not Wn and N and S and E: return 288
    if not E and N and S and Wn: return 290
    return 289
for (x, y) in PATH:
    if 0 <= x < W and 0 <= y < H: put(x, y, 0x3000, path_id(x, y)); OCC[(x, y)] = 'chemin'
def dil(cells, r):
    return {(x + i, y + j) for (x, y) in cells for i in range(-r, r + 1) for j in range(-r, r + 1)}
CLEAR = dil(PATH, 1)
HS_CELLS_ = {(HS[0] + i, HS[1] + j) for i in range(3) for j in range(8)}
# ---- panneaux, PNJ, objets (cases reservees avant les falaises)
SIGN_S, SIGN_N = (10, H - 4), (10, 5)
NPC = {'hiker': (21, 52), 'miner': (18, 20), 'ether': (21, 43), 'heal': (21, 5)}
RES = dil([SIGN_S, SIGN_N] + list(NPC.values()), 1) | dil(HS_CELLS_, 1)
for c in NPC.values(): OCC[c] = 'pnj'
# ---- falaise pleine largeur (la foret passe dessous) ; les deux portails sont dedans / devant
rnd = random.Random(2020)
def wob(seed_):
    r = random.Random(seed_); v = 0; out = []
    for x in range(W):
        v = max(-1, min(1, v + r.choice((-1, 0, 0, 1)))); out.append(v)
    return out
WALL = set(); BLOB = {}; RIDGE = set()
HS_CELLS = {(HS[0] + i, HS[1] + j) for i in range(3) for j in range(8)}
wt, wbm = wob(5), wob(9)
for x in range(2, W - 2):
    top = WALL_Y0 + (1 if wt[x] > 0 else 0); bot = WALL_Y1 - (1 if wbm[x] < 0 else 0)
    for y in range(top, bot + 1):
        if (x, y) not in HS_CELLS: WALL.add((x, y))
for c in WALL: RIDGE.add(c); OCC[c] = 'roche'; BLOB[c] = (13, 29)
# ---- crêtes de roche (serpentin) : amas irreguliers separes du chemin d'une case d'herbe
def ridge_ok(c):
    x, y = c
    return 2 <= x <= W - 3 and 3 <= y <= H - 5 and c not in OCC and c not in CLEAR and c not in RES and c not in RIDGE
for k, (ry, (g0, g1)) in enumerate(zip(RIDGE_Y, GAPS)):
    wb = wob(77 + k); cells = set()
    for x in range(2, W - 2):
        if g0 <= x <= g1: continue
        edge = min(abs(x - g0), abs(x - g1))
        th = 3 + wb[x] + (0 if edge > 1 else -1)
        for j in range(th): cells.add((x, ry - 1 + j + (wb[(x * 3) % W] if edge > 2 else 0)))
    cells = {c for c in cells if ridge_ok(c)}
    for _ in range(2):
        cells = {c for c in cells if sum(((c[0] + a, c[1] + b) in cells) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 2 or ((c[0] - 1, c[1]) in cells and (c[0] + 1, c[1]) in cells)}
    seen_, keep = set(), set()
    for c0 in sorted(cells):
        if c0 in seen_: continue
        comp, st_ = {c0}, [c0]
        while st_:
            p = st_.pop()
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (p[0] + a, p[1] + b)
                if q in cells and q not in comp: comp.add(q); st_.append(q)
        seen_ |= comp
        if len(comp) >= 4: keep |= comp
    cells = keep
    cx = sum(c[0] for c in cells) / len(cells)
    for c in cells: RIDGE.add(c); OCC[c] = 'roche'; BLOB[c] = (cx, ry)
print('falaise+cretes', len(RIDGE))
LEDGES = []
# ---- pierre (monument) : 3x3 libre loin du chemin
PATH_M = {(x + i, y + j) for (x, y) in PATH for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2)}
STONE = next((x, y) for y in range(3, 7) for x in range(W - 7, 3, -1) if all((x + i, y + j) not in PATH_M and (x + i, y + j) not in OCC and (x + i, y + j) not in RES for i in range(3) for j in range(3)))
for j in range(3):
    for i in range(3): OCC[(STONE[0] + i, STONE[1] + j)] = 'reserve'
# ---- herbes hautes
TALL = []
tries = 0
while len(TALL) < 10 and tries < 3000:
    tries += 1; x0 = rnd.randint(2, W - 8); y0 = rnd.randint(3, H - 8); w = rnd.randint(3, 5); h = rnd.randint(3, 4)
    cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    if x0 + w > W - 3 or y0 + h > H - 4 or any(c in OCC or c in RES for c in cells): continue
    if any(c in HN_CELLS for c in cells) if False else False: continue
    if not any((x + dx, y + dy) in PATH for (x, y) in cells for dx in (-3, 3) for dy in (-3, 3)): continue
    TALL.append((x0, y0, x0 + w - 1, y0 + h - 1))
    for c in cells: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M)

# ---- art : cristaux (prismes de grenat -> domes d'opale), pierre du degrade
LG = E.load('general', 'petalburg')
def grass_cols(st):
    L = (LG[0], LG[1], [stage_pal(i, TS_[st]) for i in range(6)] + LG[2][6:], LG[3], LG[4])
    cnt = collections.Counter(E.metatile(L, GRASS_M).convert('RGB').getdata()); cols = [c for c, _ in cnt.most_common(4)]
    while len(cols) < 4: cols.append(cols[-1])
    return cols
GARNET = [(8, 10, 24), (22, 26, 52), (46, 54, 98), (92, 106, 168), (236, 242, 255), (255, 104, 186), (70, 240, 218), (186, 116, 255)]      # opale (depart)
OPAL = [(16, 6, 8), (46, 16, 16), (92, 34, 26), (156, 64, 34), (255, 224, 168), (255, 96, 32), (255, 172, 40), (255, 64, 84)]                # braise / obsidienne (arrivee)
def art_pal(st):
    g = grass_cols(st); t = TS_[st]
    cols = [lerp(GARNET[i], OPAL[i], t) for i in range(8)]
    sh = tuple(int(c * 0.55) for c in min(g, key=sum))
    return [(0, 0, 0)] + g + cols + [sh, lerp((70, 80, 106), (104, 64, 54), t), lerp((128, 140, 172), (178, 122, 98), t)], g
for st in range(3):
    p, _ = art_pal(st); PALS[ART_SLOT[st]] = p
# indices : 1-4 sol | 5 contour | 6 sombre | 7 corps | 8 clair | 9 reflet | 10,11,12 etincelles | 13 ombre
def newimg(w, h, pal): im = Image.new('P', (w, h), 1); im.putpalette([c for p in pal for c in p]); return im
def ground_bg(w, h, st):
    pal, g = art_pal(st); im = newimg(w, h, pal)
    L = (LG[0], LG[1], [stage_pal(i, TS_[st]) for i in range(6)] + LG[2][6:], LG[3], LG[4])
    src = E.metatile(L, GRASS_M).convert('RGB').load(); px = im.load()
    for y in range(h):
        for x in range(w):
            c = src[x % 16, y % 16]; px[x, y] = 1 + g.index(c) if c in g else 1
    return im
def prism(d, cx, base, hw, h, tilt=0):
    top = base - h; L, R = cx - hw, cx + hw; tx = cx + tilt
    d.polygon([(L, base), (L, top + hw), (tx, top), (R, top + hw), (R, base), (cx, base + hw // 2)], fill=7, outline=5)
    d.polygon([(cx, base + hw // 2), (cx, top + 3), (R, top + hw), (R, base)], fill=6)
    d.polygon([(L + 1, top + hw), (tx, top + 1), (cx, top + 3), (cx - 1, base - 1), (L + 1, base - 1)], fill=7)
    d.polygon([(tx, top + 1), (tx + 3 + hw // 2, top + hw - 1), (cx, top + hw + 2)], fill=8)
    d.line([(L + 2, top + hw + 2), (L + 2, base - 4)], fill=9); d.point((tx, top + 2), fill=10)
def dome(d, cx, base, rx, ry):
    top = base - ry
    d.ellipse((cx - rx, top, cx + rx, base + ry // 4), fill=7, outline=5)
    d.pieslice((cx - rx + 1, top + 1, cx + rx - 1, base + ry // 4 - 1), 300, 80, fill=6)
    d.pieslice((cx - rx + 2, top + 2, max(cx - rx + 4, cx + rx - 5), max(top + 4, base - ry // 2)), 170, 290, fill=8)
    for k, c in enumerate((10, 11, 12, 10, 11, 12)):
        x = cx - rx + 2 + k * max(2, (2 * rx - 6) // 5); y = top + ry // 2 + (k % 3) * max(2, ry // 4)
        d.polygon([(x, y), (x + 2, y - 2), (x + 4, y + 1), (x + 2, y + 4)], fill=c)
    d.ellipse((cx - rx // 2, top + 3, cx - rx // 2 + 3, top + 6), fill=9)
def shape(d, st, cx, base, rx, h, tilt=0):
    """etage 0 : dome d'opale ; etages 1-2 : eclats d'obsidienne aux reflets de braise."""
    if st == 0: dome(d, cx, base, rx, h)
    else: prism(d, cx, base, rx, h, tilt)
def small(st, var):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im); d.ellipse((1, 11, 15, 15), fill=13)
    if var == 0: shape(d, st, 8, 13, 4, 10)
    else: shape(d, st, 5, 13, 3, 7, -1); shape(d, st, 11, 13, 4, 9, 1)
    return im
def big(st):
    im = ground_bg(48, 48, st); d = ImageDraw.Draw(im); d.ellipse((1, 36, 47, 47), fill=13)
    shape(d, st, 10, 42, 6, 18, -2); shape(d, st, 38, 43, 6, 16, 2); shape(d, st, 24, 44, 10, 38, 1)
    shape(d, st, 15, 44, 5, 26, -1); shape(d, st, 33, 45, 5, 24, 1)
    return im
ART_T = []
def add_tile(t):
    t = tuple(t)
    if t in ART_T: return ART_T.index(t)
    ART_T.append(t); return len(ART_T) - 1
ART_E = []
def meta(block, st):
    ents = []
    for q in range(4):
        x, y = (q % 2) * 8, (q // 2) * 8
        ents.append(('A', add_tile(list(block.crop((x, y, x + 8, y + 8)).getdata())), ART_SLOT[st]))
    ART_E.append(ents); return len(ART_E) - 1
def vent_img(st):
    """fissure de braise dans le sol."""
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im); d.ellipse((1, 8, 15, 15), fill=13)
    rr = random.Random(5 + st)
    for k in range(2):
        x, y = 3 + k * 4, 6 + k * 3
        pts = [(x, y)]
        for _ in range(4): x += rr.randint(1, 3); y += rr.randint(-2, 2); pts.append((x, min(14, max(3, y))))
        d.line(pts, fill=6, width=3); d.line(pts, fill=10 + k)
    d.point((8, 7), fill=12)
    return im
def tube_img(st):
    im = ground_bg(48, 128, st); d = ImageDraw.Draw(im)
    d.ellipse((0, 118, 47, 127), fill=13)
    d.rectangle((4, 16, 43, 118), fill=7, outline=5)
    d.rectangle((5, 17, 10, 117), fill=8); d.rectangle((38, 17, 42, 117), fill=6)
    for y in range(34, 100, 12):
        d.line([(5, y), (42, y)], fill=6); d.line([(5, y + 1), (42, y + 1)], fill=8)
        d.rectangle((3, y - 1, 44, y + 2), outline=5)
    d.line([(23, 22), (23, 96)], fill=9)
    d.ellipse((13, 56, 34, 74), fill=6, outline=5); d.ellipse((17, 60, 30, 70), fill=5)
    d.ellipse((20, 62, 27, 68), fill=11); d.point((23, 64), fill=12); d.point((25, 66), fill=10)
    d.rectangle((2, 0, 45, 20), fill=14, outline=5)
    for y in range(4, 20, 5):
        d.line([(3, y), (44, y)], fill=13)
        for x in range(5 + (y % 2) * 4, 44, 8): d.line([(x, y), (x, y + 4)], fill=13)
    d.line([(3, 19), (44, 19)], fill=15)
    d.rectangle((18, 4, 29, 15), fill=5); d.ellipse((18, 0, 29, 9), fill=5)
    d.rectangle((20, 6, 27, 15), fill=6); d.ellipse((20, 2, 27, 9), fill=6)
    d.line([(21, 15), (26, 15)], fill=8)
    for lx in (13, 34): d.rectangle((lx, 5, lx + 1, 8), fill=11); d.point((lx, 4), fill=12)
    d.rectangle((2, 100, 45, 120), fill=14, outline=5)
    for y in range(103, 120, 5):
        d.line([(3, y), (44, y)], fill=13)
        for x in range(5 + (y % 2) * 4, 44, 8): d.line([(x, y), (x, y + 4)], fill=13)
    d.line([(3, 101), (44, 101)], fill=15)
    d.rectangle((18, 109, 29, 123), fill=5); d.ellipse((18, 104, 29, 114), fill=5)
    d.rectangle((20, 111, 27, 123), fill=6); d.ellipse((20, 106, 27, 113), fill=6)
    d.line([(21, 123), (26, 123)], fill=8)
    for lx in (13, 34): d.rectangle((lx, 111, lx + 1, 114), fill=11); d.point((lx, 110), fill=12)
    return im
def house_img(st):
    """portail de pierre 3x3 (la porte est la case basse centrale)."""
    im = ground_bg(48, 48, st); d = ImageDraw.Draw(im)
    d.ellipse((0, 40, 47, 47), fill=13)
    d.rectangle((6, 24, 41, 43), fill=14, outline=5)
    for y in range(27, 43, 5):
        d.line([(7, y), (40, y)], fill=13)
        for x in range(9 + (y % 2) * 4, 40, 8): d.line([(x, y), (x, y + 4)], fill=13)
    d.line([(7, 25), (40, 25)], fill=15)
    d.polygon([(2, 24), (9, 4), (38, 4), (45, 24)], fill=7, outline=5)
    d.polygon([(2, 24), (9, 4), (12, 4), (7, 24)], fill=6)
    for y in range(8, 24, 4): d.line([(9 - (y - 4) // 3, y), (38 + (y - 4) // 3, y)], fill=6)
    d.line([(10, 5), (37, 5)], fill=8); d.line([(10, 6), (37, 6)], fill=8)
    d.rectangle((2, 22, 45, 25), fill=6, outline=5)
    d.rectangle((18, 29, 29, 43), fill=5); d.ellipse((18, 26, 29, 34), fill=5)
    d.rectangle((20, 31, 27, 43), fill=6); d.ellipse((20, 28, 27, 34), fill=6)
    d.line([(21, 43), (26, 43)], fill=8); d.line([(22, 41), (25, 41)], fill=13)
    for lx in (14, 33): d.rectangle((lx, 31, lx + 1, 34), fill=11); d.point((lx, 30), fill=12)
    d.rectangle((21, 22, 26, 24), fill=8, outline=5); d.point((23, 23), fill=12)
    return im
def stump_img(st):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im); d.ellipse((1, 10, 15, 15), fill=13)
    d.polygon([(4, 14), (5, 5), (7, 3), (8, 6), (10, 2), (12, 5), (12, 14)], fill=6, outline=5)
    d.line([(7, 6), (7, 12)], fill=10); d.line([(10, 5), (10, 9)], fill=11); d.point((8, 9), fill=12)
    d.line([(5, 13), (11, 13)], fill=5)
    return im
ART = {}      # (nom, etage) -> indice(s) de metatuile d'art
for st in range(3):
    ART[('sm0', st)] = meta(small(st, 0), st); ART[('sm1', st)] = meta(small(st, 1), st)
    b = big(st); ART[('big', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(3) for i in range(3)}
def sign_art(st):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im); d.ellipse((2, 12, 14, 15), fill=13)
    d.rectangle((7, 8, 8, 14), fill=6, outline=5); d.rectangle((2, 2, 13, 9), fill=8, outline=5)
    for y in (4, 6): d.line([(4, y), (11, y)], fill=6)
    return im
for st in range(3): ART[('sign', st)] = meta(sign_art(st), st)
for st in range(3):
    ART[('vent', st)] = meta(vent_img(st), st); ART[('stump', st)] = meta(stump_img(st), st)
    pass
b = tube_img(2); ART[('tube', 2)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), 2) for j in range(8) for i in range(3)}
def rock_img(mask, st, var):
    """case de falaise ; mask = bits N(1) E(2) S(4) O(8) : 1 si la voisine est aussi de la roche. Indices : 14 corps, 15 clair, 13 face sombre, 5 contour."""
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im)
    N, E_, S_, W_ = bool(mask & 1), bool(mask & 2), bool(mask & 4), bool(mask & 8)
    x0 = 0 if W_ else 1; x1 = 15 if E_ else 14; y0 = 0 if N else 1; y1 = 15 if S_ else 14
    d.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=14, corners=(not N and not W_, not N and not E_, not S_ and not E_, not S_ and not W_))
    rr = random.Random(var * 31 + mask)
    top_end = 8 if not S_ else 14
    for _ in range(rr.randint(2, 3)):                                      # strates / fissures en diagonale
        sx = rr.randint(x0 + 2, max(x0 + 3, x1 - 6)); sy = rr.randint(y0 + 2, max(y0 + 3, top_end - 2)); ln = rr.randint(3, 6)
        d.line([(sx, sy), (sx + ln, sy + ln // 2)], fill=13); d.line([(sx, sy - 1), (sx + ln - 1, sy + ln // 2 - 1)], fill=15)
    for _ in range(4): d.point((rr.randint(x0 + 2, max(x0 + 3, x1 - 2)), rr.randint(y0 + 1, top_end)), fill=rr.choice((13, 15)))
    if not N:
        d.line([(x0 + 2, y0 + 1), (x1 - 2, y0 + 1)], fill=15)                # arete eclairee
    if not S_:                                                           # face de falaise
        d.rectangle((x0 + 1, 9, x1 - 1, y1 - 1), fill=13)
        for x in range(x0 + 3, x1 - 1, 3): d.line([(x, 10), (x, y1 - 2)], fill=14)
        d.line([(x0 + 1, 9), (x1 - 1, 9)], fill=5)
        d.line([(x0 + 3, y1), (x1 - 3, y1)], fill=5)
    if not W_: d.line([(x0, y0 + 3), (x0, y1 - 3)], fill=5)
    if not E_: d.line([(x1, y0 + 3), (x1, y1 - 3)], fill=5)
    if not N: d.line([(x0 + 3, y0), (x1 - 3, y0)], fill=5)
    return im
ROCK = {}
for st in range(3):
    for mask in range(16):
        for var in (range(4) if mask == 15 else range(2)): ROCK[(mask, st, var)] = meta(rock_img(mask, st, var), st)
ART_PLACE = {}
def art1(x, y, name):
    claim(x, y, 1, 1, 'cristal'); ART_PLACE[(x, y)] = ART[(name, stage_at(x, y))]
def art_big(x0, y0):
    st = stage_at(x0 + 1, y0 + 1); claim(x0, y0, 3, 3, 'pierre du degrade')
    for (i, j), k in ART[('big', st)].items(): ART_PLACE[(x0 + i, y0 + j)] = k
for j in range(3):
    for i in range(3): del OCC[(STONE[0] + i, STONE[1] + j)]
art_big(*STONE)
for (x, y) in sorted(RIDGE):
    m = (((x, y - 1) in RIDGE) * 1) | (((x + 1, y) in RIDGE) * 2) | (((x, y + 1) in RIDGE) * 4) | (((x - 1, y) in RIDGE) * 8)
    bx, by = BLOB[(x, y)]; ART_PLACE[(x, y)] = ROCK[(m, 2 if (x, y) in WALL else stage_smooth(bx, by), (x * 3 + y * 5) % 4 if m == 15 else (x + y) % 2)]                                  # la pierre du degrade, a l'est du chemin
# ---- panneaux, portails, pierre
for c in NPC.values(): assert OCC[c] == 'pnj'
for j in range(3):
    for i in range(3): del OCC[(STONE[0] + i, STONE[1] + j)]
art_big(*STONE)
claim(*SIGN_S, 1, 1, 'panneau'); ART_PLACE[SIGN_S] = ART[('sign', 0)]
claim(*SIGN_N, 1, 1, 'panneau'); ART_PLACE[SIGN_N] = ART[('sign', 2)]
DOORS = {DOOR_S, DOOR_N}
for (hx, hy), nm in ((HS, 'tuyau'),):
    for j in range(8):
        for i in range(3):
            c = (hx + i, hy + j)
            if c in OCC and OCC[c] == 'roche': del OCC[c]
    claim(hx, hy, 3, 8, nm)
    for (i, j), k in ART[('tube', 2)].items(): ART_PLACE[(hx + i, hy + j)] = k
for c in NPC.values(): assert c not in ART_PLACE, ('PNJ sur un decor', c)
# ---- bosquets d'arbres
def near(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if (x + i, y + j) in OCC or (x + i, y + j) in ART_PLACE: return True
    return False
def free_tree(x, y): return 2 <= x <= W - 4 and 2 <= y <= H - 4 and all((x + i, y + j) not in OCC and not near(x + i, y + j, 1) and (x + i, y + j) not in RES for i in range(2) for j in range(2))
def grove(cx, cy, n, spread):
    k = tries = 0
    while k < n and tries < 800:
        tries += 1; x = int(rnd.gauss(cx, spread)); y = int(rnd.gauss(cy, spread))
        if free_tree(x, y):
            tree(x, y); claim(x, y, 2, 2, 'arbre'); k += 1
            for j in range(-2, 4):
                for i in range(-2, 4):
                    c = (x + i, y + j)
                    if 0 <= c[0] < W and 0 <= c[1] < H and c not in OCC and c not in TREECELLS: put(c[0], c[1], 0x3000, GRASS_M, st=stage_smooth(x, y))
for (cx, cy, n, s) in ((4, 52, 4, 2), (21, 49, 3, 1.8), (21, 37, 4, 2), (4, 37, 4, 1.8), (10, 46, 2, 1.5), (22, 44, 2, 1.3), (4, 23, 4, 2), (21, 23, 3, 2),
                       (21, 12, 4, 2), (4, 11, 4, 2), (9, 6, 3, 1.5), (21, 3, 2, 1.5), (5, 4, 3, 1.5), (14, 20, 2, 1.5), (8, 30, 0, 1)):
    grove(cx, cy, n, s)
# ---- cristaux / fissures de braise epars (opale au sud, obsidienne et braise au nord), fleurs
placed = tries = 0
GR = lambda: [variant(GRASS_M, s) for s in range(3)]
while placed < 30 and tries < 4000:
    tries += 1; x, y = rnd.randint(2, W - 3), rnd.randint(2, H - 4)
    if (x, y) not in OCC and (x, y) not in ART_PLACE and not near(x, y, 1) and (x, y) not in RES and G[(x, y)] & 0x3ff in GR():
        st = stage_at(x, y); r_ = rnd.random(); name = 'stump' if st > 0 and r_ < 0.18 * st else 'vent' if r_ < 0.15 + 0.3 * st else rnd.choice(('sm0', 'sm1'))
        art1(x, y, name); placed += 1
# ---- foret brulee : souches calcinees de plus en plus nombreuses vers la falaise
k_ = tries = 0
while k_ < 34 and tries < 6000:
    tries += 1; x, y = rnd.randint(2, W - 3), rnd.randint(16, 52)
    if WALL_Y0 - 1 <= y <= WALL_Y1 + 1 or rnd.random() > 1 - abs(y - 30) / 22.0: continue
    if (x, y) not in OCC and (x, y) not in ART_PLACE and not near(x, y, 1) and (x, y) not in RES and G[(x, y)] & 0x3ff in GR():
        art1(x, y, 'stump'); k_ += 1
for _ in range(34):
    cx, cy = rnd.randint(2, W - 3), rnd.randint(2, H - 4)
    for _ in range(rnd.randint(3, 7)):
        x, y = cx + rnd.randint(-2, 2), cy + rnd.randint(-1, 1)
        if 1 <= x < W - 1 and 1 <= y < H - 2 and (x, y) not in OCC and (x, y) not in ART_PLACE and (x, y) not in RES and G[(x, y)] & 0x3ff in GR():
            put(x, y, 0x3000, FLOWER_M)
for c in NPC.values(): del OCC[c]
# ---- accessibilite : les deux moities ne communiquent pas (sauf par la foret)
ART_RAW_BLOCK = set(ART_PLACE) - DOORS
def blocked(c):
    return c in ART_RAW_BLOCK or bool(G[c] & 0xc00)
def flood(s0):
    seen = {s0}; q = collections.deque([s0])
    while q:
        c = q.popleft()
        for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n): seen.add(n); q.append(n)
    return seen
seenS = flood((12, H - 1)); seenN = flood((12, 0))
assert not (seenS & seenN), ('les deux moities communiquent', sorted(seenS & seenN)[:5])
for c in [(x, H - 1) for x in S_GATE] + [DOOR_S, (SIGN_S[0] + 1, SIGN_S[1]), NPC['hiker'], NPC['ether']]: assert c in seenS, ('inaccessible S', c)
for c in [(x, 0) for x in N_GATE] + [DOOR_N, (SIGN_N[0] + 1, SIGN_N[1]), NPC['miner'], NPC['heal']]: assert c in seenN, ('inaccessible N', c)
for (x0, y0, x1, y1) in TALL: assert (x0, y0) in seenS | seenN or (x1, y1) in seenS | seenN, ('herbe inaccessible', x0, y0)
seen = seenS | seenN
# ------------------------------------------------------------------ ecriture
for _m in (468, 469, 476, 477): variant(_m, 1)
NT = 0
ART_ID = {}
for k, ents in enumerate(ART_E):
    SEC_ENT.append([(640 + t) | (slot << 12) for (_, t, slot) in ents] + [0, 0, 0, 0]); SEC_ATT.append(0)
    ART_ID[k] = 640 + len(SEC_ENT) - 1
assert len(SEC_ENT) <= 384 and len(ART_T) <= 384, (len(SEC_ENT), len(ART_T))
for c, k in ART_PLACE.items(): G[c] = (0x3000 if c in DOORS else 0x400) | ART_ID[k]
rows = max(1, (len(ART_T) + 15) // 16)
out = Image.new('P', (128, rows * 8), 0); out.putpalette([c for p in PALS[ART_SLOT[0]] for c in p])
for i, t in enumerate(ART_T):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, ((i % 16) * 8, (i // 16) * 8))
out.save(SEC + 'tiles.png')
open(SEC + 'metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *e) for e in SEC_ENT))
open(SEC + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in SEC_ATT))
FILL = ORIG
for i in range(16):
    writepal(SEC + 'palettes/%02d.pal' % i, PALS.get(i, [(0, 0, 0)] * 16) if i >= 7 else ORIG[i])
    writepal(PRI + 'palettes/%02d.pal' % i, PALS.get(i, ORIG[i]) if i <= 6 else ORIG[i])
shutil.copy(EM + 'tilesets/primary/general/tiles.png', PRI + 'tiles.png'); shutil.copy(EM + 'tilesets/primary/general/metatiles.bin', PRI + 'metatiles.bin')
open(PRI + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in PATT32))
def add(path, text):
    s = open(path).read()
    if 'GeneralDusk' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralDusk[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralDusk[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_DuskRoad[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_DuskRoad[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralDusk[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralDusk[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_DuskRoad[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_DuskRoad[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralDusk =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralDusk,
    .palettes = gTilesetPalettes_GeneralDusk,
    .metatiles = gMetatiles_GeneralDusk,
    .metatileAttributes = gMetatileAttributes_GeneralDusk,
    .callback = NULL,
};

const struct Tileset gTileset_DuskRoad =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_DuskRoad,
    .palettes = gTilesetPalettes_DuskRoad,
    .metatiles = gMetatiles_DuskRoad,
    .metatileAttributes = gMetatileAttributes_DuskRoad,
    .callback = NULL,
};
''')
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/Route2/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/Route2/border.bin', 'wb').write(struct.pack('<4H', *[0x400 | variant(m, 1) for m in (468, 469, 476, 477)]))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_ROUTE2': l.update(width=W, height=H, primary_tileset='gTileset_GeneralDusk', secondary_tileset='gTileset_DuskRoad')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'signS': SIGN_S, 'signN': SIGN_N, 'doorS': DOOR_S, 'doorN': DOOR_N, 'npc': NPC, 'w': W, 'h': H, 'tall': TALL, 'ledges': LEDGES, 'path': sorted(PATH)}, open('/tmp/route2_info.json', 'w'))
blk = sorted([x, y] for (x, y) in ((x, y) for y in range(H) for x in range(W)) if blocked((x, y)))
json.dump({'w': W, 'h': H, 'blocked': blk}, open('/tmp/route2_col.json', 'w'))
print('route 2 : metatuiles', len(SEC_ENT), 'tuiles art', len(ART_T))
