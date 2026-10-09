# FORET CALCINEE (carte de l'ex Viridian Forest, 54x69), generee avec la meme machinerie que la Route 2 (etage 2 seulement). Lancer apres forest_cinder.py.
# (en-tete herite de) ROUTE 2 « la route du crépuscule » : relie Opanihrum (opale noire, sud) à Pyropia (braise, nord) ; les couleurs glissent de l'opale à la braise
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
PRI = 'data/tilesets/primary/general_cinder/'; SEC = 'data/tilesets/secondary/cinder_forest/'
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
    if 60 <= h <= 180: h = 14 + (h - 120) * 0.1; s = min(0.10, s * 0.2); l = l * 0.42
    elif 25 <= h < 60: h = 18 + (h - 40) * 0.2; s = s * 0.6; l = l * 0.5
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
PALS[ROCK_SLOT] = stage_pal(3, 0.5)
def lighten(c):
    h, l, s = colorsys.rgb_to_hls(*[x / 255 for x in c]); r, g, b = colorsys.hls_to_rgb(0.07, min(0.5, l * 1.18 + 0.02), min(0.1, s * 0.3 + 0.015))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
for _s in (1, 3, 4): PALS[_s] = [PALS[_s][0]] + [lighten(c) for c in PALS[_s][1:]]          # roche : meme palette violet-gris sur toute la route
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
W, H = 46, 48
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
def stage_at(x, y): return 2
def stage_smooth(x, y): return 2
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
# ======================================================================== FORET CALCINEE : sentier tortueux (l'ancien coupe-feu), clairieres, cratere central
DY = 9
def FX(x): return x if x <= 6 else int(round(6 + (x - 6) * 38 / 46))
def FY(y): return y if y <= 12 else (y - DY if y >= 50 else int(round(12 + (y - 12) * (38 - DY) / 38)))
def P(c): return (FX(c[0]), FY(c[1]))
def PB(b): return (FX(b[0]), FY(b[1]), FX(b[2]), FY(b[3]))
S_DOOR, N_DOOR = P((29, 50)), (5, 9)
S_ROWS = [0, 1, 2, 3, 4, 5, 2]                       # lignes du tuyau (art) pour y=50..56 : on voit la face nord avec la porte, puis le tuyau qui part hors carte
N_ROWS = [2, 5, 2, 5, 3, 4, 2, 5, 6, 7]              # y=0..9 : le tuyau vient du haut de la carte, la porte est en bas (face sud)
BUILD = {(S_DOOR[0] - 1 + i, S_DOOR[1] + j) for i in range(3) for j in range(7)} | {(4 + i, j) for i in range(3) for j in range(10)}
for c in BUILD: OCC[c] = 'tuyau'
for x in list(range(0, 4, 2)) + [7] + list(range(8, W, 2)): tree(x, 0)
for x in list(range(0, S_DOOR[0] - 2, 2)) + list(range(S_DOOR[0] + 2, W - 2, 2)): tree(x, H - 2)
for y in range(2, H - 2, 2): tree(0, y); tree(W - 2, y)
PATH = set()
WAY = [P(c) for c in [(29, 49), (29, 44), (45, 42), (45, 36), (12, 35), (12, 28), (44, 27), (44, 19), (8, 17)]] + [(6, 12), (5, 10)]
SPURS = [(P(a), P(b)) for a, b in [((12, 35), (9, 45)), ((44, 19), (47, 14)), ((30, 18), (30, 12)), ((12, 28), (9, 25))]]
CLEARINGS = [PB(b) for b in [(3, 46, 10, 52), (43, 9, 50, 15), (24, 6, 36, 12), (14, 38, 28, 46)]]
VOLC = P((3, 41))                                       # volcan (4x4), au nord-ouest de la clairiere sud-ouest
GIANT = P((7, 21))                                      # grand arbre calcine (3x4) qui barre la diagonale gauche
def seg(a, b):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        t = k / max(1, n); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        for i in (0, 1): PATH.add((int(round(x)) + i, int(round(y))))
        PATH.add((int(round(x)) + 1, int(round(y)) + 1))
for a_, b_ in zip(WAY, WAY[1:]): seg(a_, b_)
for a_, b_ in SPURS: seg(a_, b_)
PATH -= BUILD
def path_id(x, y):
    N = (x, y - 1) in PATH; S = (x, y + 1) in PATH; Wn = (x - 1, y) in PATH; E = (x + 1, y) in PATH
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
OBJ0 = {'youngster': (26, 47), 'boy': (33, 46), 'rick': (48, 38), 'doug': (17, 39), 'sammy': (22, 31), 'anthony': (30, 9), 'charlie': (20, 14),
       'ball_pokeball': (5, 48), 'ball_antidote': (48, 11), 'ball_potion': (9, 49), 'ball_potion2': (27, 44)}
HID0 = {'potion': (4, 51), 'antidote': (49, 14)}
SIGNS0 = {'tips1': (32, 47), 'tips2': (43, 39), 'tips3': (24, 38), 'tips4': (15, 31), 'tips5': (30, 31), 'exit': (9, 13)}
OBJ = {k: P(v) for k, v in OBJ0.items()}; HID = {k: P(v) for k, v in HID0.items()}; SIGNS = {k: P(v) for k, v in SIGNS0.items()}
RES = dil(list(OBJ.values()) + list(HID.values()) + list(SIGNS.values()), 1)
CORR = dil(PATH, 2)
NOGO = {(x, y) for x in range(3, FX(12)) for y in range(FY(18), FY(28))}      # la diagonale gauche est fermee : que des arbres autour de l'arbre geant
CORR -= (NOGO - PATH)
for (x0, y0, x1, y1) in CLEARINGS: CORR |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
CR = P((20, 40))
for i in range(4):
    for j in range(4): OCC[(VOLC[0] + i, VOLC[1] + j)] = 'reserve-volcan'
for i in range(3):
    for j in range(3): OCC[(CR[0] + i, CR[1] + j)] = 'reserve'
for i in range(3):
    for j in range(4):
        if (GIANT[0] + i, GIANT[1] + j) not in OCC: OCC[(GIANT[0] + i, GIANT[1] + j)] = 'reserve-geant'
rnd = random.Random(3030)
bad_ = [c for c in list(OBJ.values()) + list(HID.values()) + list(SIGNS.values()) if c in OCC]
assert not bad_, ('cases deja prises', bad_, [(c, OCC[c]) for c in bad_])
# ---- herbes hautes : dans les couloirs et les clairieres, jamais sur le chemin
TALL = []
tries = 0
while len(TALL) < 14 and tries < 20000:
    tries += 1; x0 = rnd.randint(3, W - 8); y0 = rnd.randint(4, H - 8); w, h = rnd.choice([(2, 4), (2, 5), (3, 3), (4, 2), (5, 2), (6, 2), (3, 4), (2, 3)])
    cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    if any(c not in CORR or c in OCC or c in RES for c in cells): continue
    if any(c in dil(PATH, 0) for c in cells): continue
    TALL.append((x0, y0, x0 + w - 1, y0 + h - 1))
    for c in cells: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M, st=1)
# ---- foret : arbres sur un reseau 2x2 partout sauf couloirs/clairieres ; un tiers sont des squelettes calcines (art)
DEAD = []
for y in range(2, H - 2, 2):
    for x in range(2, W - 4, 2):
        cells = [(x + i, y + j) for i in range(2) for j in range(2)]
        if any(c in CORR or c in OCC or c in RES for c in cells): continue
        if rnd.random() < 0.05: continue
        east = x >= 44
        if rnd.random() < (0.25 if east else 0.55): tree(x, y); claim(x, y, 2, 2, 'arbre')
        else:
            kind = rnd.choice(['boulder', 'thorns', 'spire', 'spire', 'dead'] if east else ['dead', 'dead', 'boulder', 'thorns', 'spire'])
            DEAD.append((x, y, kind)); claim(x, y, 2, 2, kind)
# ---- herbe cendree : zones de sol gris clair (c'etait une foret), hors arbres, chemin et objets
ASH = set()
for y in range(2, H - 2):
    for x in range(2, W - 2):
        c = (x, y)
        if c in OCC or c in RES: continue
        n = math.sin(x * 0.45 + y * 0.3) + math.sin(y * 0.6 - x * 0.2) + math.sin(x * 0.17 + y * 0.5)
        if n > 0.5: put(x, y, 0x3000, GRASS_M, st=1); ASH.add(c)
RIDGE = set(); WALL = set(); BLOB = {}

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
for st in (2,):
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
for st in (2,):
    ART[('sm0', st)] = meta(small(st, 0), st); ART[('sm1', st)] = meta(small(st, 1), st)
    b = big(st); ART[('big', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(3) for i in range(3)}
def sign_art(st):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im); d.ellipse((2, 12, 14, 15), fill=13)
    d.rectangle((7, 8, 8, 14), fill=6, outline=5); d.rectangle((2, 2, 13, 9), fill=8, outline=5)
    for y in (4, 6): d.line([(4, y), (11, y)], fill=6)
    return im
for st in (2,): ART[('sign', st)] = meta(sign_art(st), st)
for st in (2,):
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
for st in (2,):
    for mask in ():
        pass
ART_PLACE = {}
def art1(x, y, name):
    claim(x, y, 1, 1, 'cristal'); ART_PLACE[(x, y)] = ART[(name, stage_at(x, y))]
def art_big(x0, y0):
    st = stage_at(x0 + 1, y0 + 1); claim(x0, y0, 3, 3, 'pierre du degrade')
    for (i, j), k in ART[('big', st)].items(): ART_PLACE[(x0 + i, y0 + j)] = k

# ---- art specifique a la foret
from PIL import ImageOps
def dead_img(st, var):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((3, 25, 29, 31), fill=13)
    d.polygon([(12, 29), (13, 12), (17, 12), (19, 29)], fill=6, outline=5)
    for p, q in (((14, 14), (6, 5)), ((15, 12), (23, 3)), ((16, 19), (25, 11)), ((14, 21), (6, 15)), ((6, 5), (3, 7)), ((23, 3), (27, 4))):
        d.line([p, q], fill=5, width=3); d.line([p, q], fill=6, width=1)
    d.line([(14, 14), (14, 27)], fill=7); d.line([(16, 18), (16, 25)], fill=10)
    for p in ((6, 5), (23, 3), (25, 11), (6, 15)): d.point(p, fill=11)
    d.point((15, 13), fill=12)
    if var: im = ImageOps.mirror(im)
    return im
def log_img(st):
    im = ground_bg(32, 16, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 11, 30, 15), fill=13)
    d.rounded_rectangle((1, 3, 30, 13), radius=4, fill=7, outline=5)
    d.line([(5, 5), (28, 5)], fill=8); d.line([(5, 12), (28, 12)], fill=6)
    for x in range(9, 28, 5): d.line([(x, 7), (x, 10)], fill=6)
    d.line([(14, 8), (20, 9)], fill=10); d.point((17, 8), fill=11)
    d.ellipse((0, 2, 7, 13), fill=14, outline=5); d.ellipse((2, 5, 5, 10), fill=6); d.point((3, 7), fill=10); d.point((3, 8), fill=11)
    return im
def crater_img(st):
    im = ground_bg(48, 48, st); d = ImageDraw.Draw(im)
    d.ellipse((1, 20, 47, 47), fill=13)
    d.ellipse((2, 6, 45, 42), fill=14, outline=5)
    d.ellipse((6, 11, 41, 37), fill=6, outline=5)
    d.ellipse((10, 15, 37, 33), fill=12)
    d.ellipse((14, 18, 33, 30), fill=10)
    d.ellipse((19, 21, 28, 27), fill=11)
    for p, q in (((24, 24), (8, 14)), ((24, 24), (40, 16)), ((24, 24), (36, 35)), ((24, 24), (12, 34))):
        d.line([p, q], fill=10)
    for p in ((6, 12), (42, 14), (38, 36), (10, 36), (24, 9)): d.point(p, fill=12)
    d.line([(6, 10), (16, 7)], fill=15); d.line([(30, 7), (40, 10)], fill=15)
    return im
def ash_img(st):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 10, 14, 15), fill=13); d.ellipse((1, 9, 14, 14), fill=7); d.ellipse((3, 8, 11, 12), fill=14)
    d.point((6, 10), fill=6); d.point((9, 11), fill=6)
    return im
def giant_img(st):
    im = ground_bg(48, 64, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 52, 46, 63), fill=13)
    d.polygon([(4, 61), (13, 44), (15, 22), (33, 22), (35, 44), (44, 61), (30, 56), (18, 56)], fill=6, outline=5)
    for p, q in (((18, 28), (4, 10)), ((30, 24), (44, 4)), ((14, 38), (1, 32)), ((34, 36), (47, 26)), ((24, 22), (24, 2)), ((4, 10), (1, 14)), ((44, 4), (47, 8)), ((4, 10), (7, 1))):
        d.line([p, q], fill=5, width=6); d.line([p, q], fill=6, width=4)
    d.line([(19, 26), (17, 54)], fill=7); d.line([(27, 28), (28, 52)], fill=10); d.line([(24, 24), (24, 30)], fill=10)
    d.ellipse((20, 38, 28, 48), fill=5); d.ellipse((22, 40, 26, 46), fill=12); d.point((24, 43), fill=11)
    for p in ((6, 12), (40, 6), (4, 30), (45, 24), (22, 3), (8, 4)): d.point(p, fill=11)
    for p in ((15, 56), (33, 56), (19, 55)): d.point(p, fill=12)
    return im
def boulder_img(st):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((1, 22, 31, 31), fill=13)
    d.polygon([(3, 27), (4, 13), (11, 5), (22, 4), (29, 12), (30, 27)], fill=14, outline=5)
    d.polygon([(17, 27), (18, 10), (22, 5), (29, 12), (30, 27)], fill=6)
    d.line([(6, 12), (12, 7), (20, 6)], fill=15); d.line([(10, 25), (14, 16), (21, 19)], fill=10); d.point((14, 17), fill=11); d.point((8, 20), fill=12)
    return im
def thorns_img(st):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 24, 30, 31), fill=13); d.ellipse((6, 21, 26, 29), fill=6, outline=5)
    for k, (x, tx, ty) in enumerate(((8, 3, 6), (12, 9, 3), (16, 16, 1), (20, 24, 4), (24, 29, 9), (14, 5, 14), (19, 27, 15))):
        d.line([(x, 24), (tx, ty)], fill=5, width=3); d.line([(x, 24), (tx, ty)], fill=6, width=1)
        d.point((tx, ty), fill=11 if k % 2 else 10)
    return im
def spire_img(st):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((1, 24, 31, 31), fill=13)
    shape(d, st, 10, 28, 6, 22, -1); shape(d, st, 22, 29, 7, 26, 1); shape(d, st, 16, 30, 5, 13)
    return im
def volcano_img(st):
    im = ground_bg(64, 64, st); d = ImageDraw.Draw(im)
    d.ellipse((0, 50, 63, 63), fill=13)
    d.polygon([(2, 60), (20, 24), (26, 13), (38, 13), (44, 24), (62, 60)], fill=14, outline=5)
    d.polygon([(34, 13), (38, 13), (44, 24), (62, 60), (38, 60)], fill=6)
    d.line([(24, 15), (4, 58)], fill=15); d.line([(26, 16), (12, 46)], fill=15)
    d.ellipse((23, 8, 41, 19), fill=6, outline=5); d.ellipse((26, 10, 38, 17), fill=10); d.ellipse((29, 11, 35, 15), fill=11)
    for pts in (((31, 16), (28, 30), (24, 46), (23, 58)), ((35, 16), (38, 30), (44, 44), (50, 58)), ((32, 17), (33, 34), (33, 50))):
        d.line(pts, fill=12, width=3); d.line(pts, fill=10, width=1)
    d.ellipse((22, 0, 34, 8), fill=9); d.ellipse((30, 0, 44, 6), fill=8); d.ellipse((26, 3, 38, 10), fill=9)
    for p in ((10, 54), (52, 54), (30, 58), (44, 40)): d.point(p, fill=11)
    return im
for st in (2,):
    b = giant_img(st); ART[('giant', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(4) for i in range(3)}
    for var in (0, 1):
        b = dead_img(st, var); ART[('dead', st, var)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
    b = log_img(st); ART[('log', st)] = [meta(b.crop((0, 0, 16, 16)), st), meta(b.crop((16, 0, 32, 16)), st)]
    b = crater_img(st); ART[('crater', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(3) for i in range(3)}
    ART[('ash', st)] = meta(ash_img(st), st)
    for nm, fn in (('boulder', boulder_img), ('thorns', thorns_img), ('spire', spire_img)):
        b = fn(st); ART[(nm, st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
    b = volcano_img(st); ART[('volcano', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(4) for i in range(4)}
# ---- placement
DOORS = {S_DOOR, N_DOOR}
for j in range(7):
    for i in range(3): ART_PLACE[(S_DOOR[0] - 1 + i, S_DOOR[1] + j)] = ART[('tube', 2)][(i, S_ROWS[j])]
for j in range(10):
    for i in range(3): ART_PLACE[(4 + i, j)] = ART[('tube', 2)][(i, N_ROWS[j])]
# grand arbre calcine sur la diagonale gauche : il barre le chemin (les cases de chemin dessous sont remplacees)
for j in range(4):
    for i in range(3):
        c = (GIANT[0] + i, GIANT[1] + j)
        if c in OCC and OCC[c] not in ('chemin', 'reserve-geant'): raise AssertionError(('arbre geant', c, OCC[c]))
        OCC[c] = 'arbre geant'; ART_PLACE[c] = ART[('giant', 2)][(i, j)]
for c in SIGNS.values(): claim(c[0], c[1], 1, 1, 'panneau'); ART_PLACE[c] = ART[('sign', 2)]
for (x, y, kind) in DEAD:
    arts = ART[('dead', 2, rnd.randrange(2))] if kind == 'dead' else ART[(kind, 2)]
    for (i, j), k in arts.items(): ART_PLACE[(x + i, y + j)] = k
for i in range(3):
    for j in range(3): del OCC[(CR[0] + i, CR[1] + j)]
claim(CR[0], CR[1], 3, 3, 'cratere')
for (i, j), k in ART[('crater', 2)].items(): ART_PLACE[(CR[0] + i, CR[1] + j)] = k
for i in range(4):
    for j in range(4): del OCC[(VOLC[0] + i, VOLC[1] + j)]
claim(VOLC[0], VOLC[1], 4, 4, 'volcan')
for (i, j), k in ART[('volcano', 2)].items(): ART_PLACE[(VOLC[0] + i, VOLC[1] + j)] = k
def near(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if (x + i, y + j) in OCC or (x + i, y + j) in ART_PLACE: return True
    return False
PATH_D = dil(PATH, 1)
TRAINERS = {'rick': 3, 'doug': 4, 'sammy': 3, 'anthony': 4, 'charlie': 4}
LINE = {(OBJ[k][0] + dx * d_, OBJ[k][1] + dy * d_) for k in TRAINERS for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)) for d_ in range(1, 6)}
# ---- bandes d'herbe hautes OBLIGATOIRES : tranches qui coupent tout le couloir (on verifie que le joueur ne peut pas les contourner)
def walk_blocked(c):
    return (c in ART_PLACE and c not in DOORS) or bool(G[c] & 0xc00)
def reach(extra):
    s0 = (S_DOOR[0], S_DOOR[1] - 1); seen_ = {s0}; q_ = collections.deque([s0])
    while q_:
        c = q_.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n_ = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n_[0] < W and 0 <= n_[1] < H and n_ not in seen_ and n_ not in extra and not walk_blocked(n_): seen_.add(n_); q_.append(n_)
    return seen_
NOBAND = dil({(S_DOOR[0], S_DOOR[1] - 1), (5, 10)}, 2) | RES | LINE
BAND_ALL = set(); BANDS = []
_dist = {(S_DOOR[0], S_DOOR[1] - 1): 0}; _q = collections.deque([(S_DOOR[0], S_DOOR[1] - 1)])
while _q:
    c = _q.popleft()
    for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n_ = (c[0] + d_[0], c[1] + d_[1])
        if 0 <= n_[0] < W and 0 <= n_[1] < H and n_ not in _dist and not walk_blocked(n_): _dist[n_] = _dist[c] + 1; _q.append(n_)
_maxd = _dist[(5, 10)]
_OBJC = set(OBJ.values()) | set(SIGNS.values()) | set(HID.values())
_cand = []
for d0 in range(8, _maxd - 8):
    layer = {c for c, v in _dist.items() if d0 <= v <= d0 + 1}
    if layer & (dil({(S_DOOR[0], S_DOOR[1] - 1), (5, 10)}, 3) | _OBJC | BAND_ALL) or any(not (1 <= c[0] < W - 1 and 1 <= c[1] < H - 1) for c in layer): continue
    _cand.append((len(layer), d0, layer))
_cand.sort(key=lambda t: t[0])
_used = []; (lambda *a: None)('maxd', _maxd, 'cands', [(n,d) for n,d,_ in _cand[:12]], 'nolayer', sum(1 for d0 in range(8,_maxd-8)))
for n_, d0, layer in _cand:
    if n_ > 80 or len(BANDS) >= 5: break
    if any(abs(d0 - u) < 7 for u in _used): continue
    if (5, 10) in reach(layer | BAND_ALL): continue
    BANDS.append(layer); BAND_ALL |= layer; _used.append(d0)
_PD = dil(PATH, 1) | LINE | set(RES); _k = 0
_SAFE = _OBJC | dil({(S_DOOR[0], S_DOOR[1] - 1), (5, 10)}, 2)
for cells in BANDS:
    for c in sorted(cells):
        if c in _PD: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M, st=1)
_TG = [(t[0], t[1]) for t in TALL] + list(OBJ.values()) + list(HID.values()) + [(5, 10)]
def _keeps(sq):
    r_ = reach(set(sq))
    return all(t in r_ for t in _TG if t not in sq)
for cells in BANDS:
    for c in sorted(cells):
        if c in _PD or OCC.get(c) in ('haie', 'arbre', 'herbe'): continue
        done_ = False
        for ax, ay in ((c[0], c[1]), (c[0] - 1, c[1]), (c[0], c[1] - 1), (c[0] - 1, c[1] - 1)):
            sq = [(ax + i, ay + j) for i in range(2) for j in range(2)]
            if all(1 <= q[0] < W - 1 and 1 <= q[1] < H - 1 and q not in OCC and q not in ART_PLACE and q not in _PD and q not in _SAFE and not (G[q] & 0xc00) for q in sq) and _keeps(sq):
                tree(ax, ay); claim(ax, ay, 2, 2, 'arbre'); done_ = True; break
        if not done_:
            _k += 1; OCC[c] = 'haie'; ART_PLACE[c] = ART[(('sm0', 'sm1', 'stump')[_k % 3], 2)]
print('bandes obligatoires', len(BANDS), [len(b) for b in BANDS])
assert len(BANDS) >= 3, 'pas assez de bandes obligatoires'
DARK = variant(GRASS_M, 2)
OPEN = sorted(c for c in CORR if c not in OCC and c not in RES and c not in PATH_D and c not in LINE and c not in ASH and 2 <= c[0] <= W - 3 and 2 <= c[1] <= H - 4)
def scatter(n, fn):
    k = tries = 0
    while k < n and tries < 3000:
        tries += 1; c = rnd.choice(OPEN)
        if fn(c): k += 1
def one(name):
    def f(c):
        if near(c[0], c[1], 1) or c in ART_PLACE: return False
        claim(c[0], c[1], 1, 1, name); ART_PLACE[c] = ART[(name_map[name], 2)]; return True
    return f
name_map = {'vent': 'vent', 'souche': 'stump', 'cendre': 'ash', 'obsidienne0': 'sm0', 'obsidienne1': 'sm1'}
for nm, n in (('vent', 12), ('souche', 14), ('cendre', 10), ('obsidienne0', 5), ('obsidienne1', 4)): scatter(n, one(nm))
def logf(c):
    a, b = c, (c[0] + 1, c[1])
    if b not in OPEN or near(a[0], a[1], 1) or near(b[0], b[1], 1): return False
    claim(a[0], a[1], 2, 1, 'tronc'); ART_PLACE[a] = ART[('log', 2)][0]; ART_PLACE[b] = ART[('log', 2)][1]; return True
scatter(7, logf)
# ---- accessibilite
ART_RAW_BLOCK = set(ART_PLACE) - DOORS
def blocked(c):
    return c in ART_RAW_BLOCK or bool(G[c] & 0xc00)
seen = {(S_DOOR[0], S_DOOR[1] - 1)}; q = collections.deque([(S_DOOR[0], S_DOOR[1] - 1)])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n): seen.add(n); q.append(n)
for c in [(5, 10), S_DOOR, N_DOOR] + list(OBJ.values()) + list(HID.values()): assert c in seen, ('inaccessible', c)
for (x0, y0, x1, y1) in TALL: assert (x0, y0) in seen, ('herbe inaccessible', x0, y0)
for c in SIGNS.values(): assert any((c[0] + dx, c[1] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), ('panneau inaccessible', c)
# ---- dresseurs : regard orienté vers le chemin sans obstacle
FACE = {}
for k, sight in TRAINERS.items():
    x, y = OBJ[k]; ok = None
    for dn, (dx, dy) in (('UP', (0, -1)), ('DOWN', (0, 1)), ('LEFT', (-1, 0)), ('RIGHT', (1, 0))):
        for dist in range(1, sight + 1):
            c = (x + dx * dist, y + dy * dist)
            if blocked(c) and c not in PATH: break
            if c in PATH and dist >= 2: ok = dn; break
        if ok: break
    assert ok, ('dresseur sans ligne de vue', k)
    FACE[k] = ok
print('regards', FACE)

# ------------------------------------------------------------------ ecriture
for _m in (468, 469, 476, 477): variant(_m, 2)
NT = 0
ART_ID = {}
for k, ents in enumerate(ART_E):
    SEC_ENT.append([(640 + t) | (slot << 12) for (_, t, slot) in ents] + [0, 0, 0, 0]); SEC_ATT.append(0)
    ART_ID[k] = 640 + len(SEC_ENT) - 1
assert len(SEC_ENT) <= 384 and len(ART_T) <= 384, (len(SEC_ENT), len(ART_T))
for c, k in ART_PLACE.items(): G[c] = (0x3000 if c in DOORS else 0x400) | ART_ID[k]
rows = max(1, (len(ART_T) + 15) // 16)
out = Image.new('P', (128, rows * 8), 0); out.putpalette([c for p in PALS[ART_SLOT[2]] for c in p])
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
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/ViridianForest/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/ViridianForest/border.bin', 'wb').write(struct.pack('<6H', *[0x400 | variant(m, 2) for m in (468, 469, 468, 476, 477, 476)]))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_VIRIDIAN_FOREST': l.update(width=W, height=H, primary_tileset='gTileset_GeneralCinder', secondary_tileset='gTileset_CinderForest')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'w': W, 'h': H, 'obj': OBJ, 'hid': HID, 'signs': SIGNS, 'face': FACE, 'sight': TRAINERS, 'sdoor': S_DOOR, 'ndoor': N_DOOR, 'tall': TALL, 'path': sorted(PATH)}, open('/tmp/forest_info.json', 'w'))
blk = sorted([x, y] for (x, y) in ((x, y) for y in range(H) for x in range(W)) if blocked((x, y)))
json.dump({'w': W, 'h': H, 'blocked': blk}, open('/tmp/forest_col.json', 'w'))
print('foret : metatuiles', len(SEC_ENT), 'tuiles art', len(ART_T))
