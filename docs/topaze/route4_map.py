# ROUTE 4 « le flanc de lune » (Route 3 -> Mont Selenite -> Azuria), cendre -> paysage lunaire ; base de route3_map.py (pyropia -> lune)
# (ancien en-tete) ROUTE 3 « la coulee » (Pyropia -> Route 4), generee avec la machinerie de la Route 2 / de la foret (etage 2 seulement).
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
PRI = 'data/tilesets/primary/general_moon/'; SEC = 'data/tilesets/secondary/moon_road/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
# ------------------------------------------------------------------ teintes : GRENAT (Grenalux) et OPALE NOIRE (Opanihrum)
def tint_garnet(r, g, b):      # (nom conserve) teinte du depart = LUNE : poussiere gris-bleu pale, arbres ardoise
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.10 and l > 0.93: return r, g, b
    if s > 0.45 and (h >= 180 or h < 25): return r, g, b
    if 78 <= h <= 175: h = 228 + (h - 120) * 0.05; s = min(0.16, s * 0.3); l = min(0.9, l * 0.85 + 0.16)
    elif 25 <= h < 60: h = 262; s = min(0.12, s * 0.25); l = min(0.92, l * 0.85 + 0.10)
    else: h = 222; s = min(0.22, s * 0.4 + 0.04); l = min(0.9, l * 0.9 + 0.10)
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
# emplacement 12 = palette ROCHE d'origine (pal 1 : roche brune / bord de toit) teintee neutre ; emplacement 10 = palette 3 d'origine (porte, panneau du Centre) teintee braise
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
W, H = 40, 84
GRASS_M, FLOWER_M, TALL_M = 1, 4, 13
TREE = [[468, 469], [476, 477]]
G = {}; OCC = {}; STG = {}
rnd = random.Random(1010)
def _tg(y): return max(0.0, min(1.0, (y - 30) / 34.0))
def stage_at(x, y):
    if x <= 3 or x >= W - 4 or y <= 3 or y >= H - 4: return stage_smooth(x, y)
    n = 0.35 * math.sin(x * 0.55 + y * 0.21) + 0.25 * math.sin(y * 0.37 - x * 0.3) + 0.2 * math.sin(x * 0.23 + y * 0.6)
    j = ((x * 73856093) ^ (y * 19349663)) % 1000 / 1000.0 - 0.5
    return max(0, min(2, int(round(2 * _tg(y) + n * 0.45 + j * 0.5))))
def stage_smooth(x, y):
    n = 0.35 * math.sin(x * 0.55 + y * 0.21) + 0.25 * math.sin(y * 0.37 - x * 0.3) + 0.2 * math.sin(x * 0.23 + y * 0.6)
    return max(0, min(2, int(round(2 * _tg(y) + n * 0.3))))
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
# ======================================================================== ROUTE 4 « le flanc de lune » (VERTICALE) : on monte de la cendre (sud, Route 3) vers le Mont Selenite ; au-dela, le versant lunaire (nord) mene a Azuria
S_DOOR, N_DOOR = (-5, -5), (-5, -5)
SOUTH_COLS = (18, 21); EAST_ROWS = (34, 37)
for x in range(0, W - 2, 2):
    tree(x, 0)
    if not (SOUTH_COLS[0] <= x <= SOUTH_COLS[1]): tree(x, H - 2)
for y in range(2, H - 2, 2):
    tree(0, y)
    if not (EAST_ROWS[0] <= y <= EAST_ROWS[1]): tree(W - 2, y)
PATH = set()
HRIDGES = [(72, 11, 18), (28, 12, 21)]                    # (y haut, breche gauche, breche droite) : crêtes horizontales pleine largeur
CENTER = (22, 59)                                        # Centre classique 5x4 (metatuiles d'origine) : cases (22..26, 60..63), porte en (24, 63)
ARCH1, ARCH2 = (19, 49), (24, 16)                        # grottes : cases (x..x+2, y..y+2), porte en (x+1, y+2)
WAYS = [[(19, 82), (18, 78), (15, 73), (13, 69), (16, 66), (20, 64), (30, 64), (32, 60), (30, 57), (24, 55), (20, 54)],
        [(25, 20), (24, 23), (20, 26), (16, 29), (17, 32), (24, 33), (31, 33), (37, 34), (38, 35)]]
def seg(a, b):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        t = k / max(1, n); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        for i in (0, 1): PATH.add((int(round(x)) + i, int(round(y))))
        PATH.add((int(round(x)) + 1, int(round(y)) + 1))
for WAY in WAYS:
    for a_, b_ in zip(WAY, WAY[1:]): seg(a_, b_)
for ax, ay in (ARCH1, ARCH2): PATH.add((ax + 1, ay + 3)); PATH.add((ax + 1, ay + 4)); PATH.add((ax + 2, ay + 3))
def wob(seed_, n=H):
    r = random.Random(seed_); v = 0; out = []
    for _ in range(n):
        if r.random() < 0.3: v = max(-1, min(1, v + r.choice((-1, 1))))
        out.append(v)
    return out
RIDGE = set(); GAPC = set(); BLOB = {}
for k, (y0, g0, g1) in enumerate(HRIDGES):
    wl, wr = wob(100 + k, W), wob(200 + k, W)
    for x in range(2, W - 2):
        if g0 <= x <= g1:
            for y in range(y0 - 2, y0 + 5): GAPC.add((x, y))
            continue
        sh = int(round(1.6 * math.sin(x * 0.22 + k * 1.7)))
        for y in range(y0 + sh, y0 + sh + 3): RIDGE.add((x, y)); BLOB[(x, y)] = (x, y0)
def _fat0(c, S):
    return any(all(((c[0] + ox + i, c[1] + oy + j) in S) for i in (0, 1) for j in (0, 1)) for ox in (0, -1) for oy in (0, -1))
_chh = True
while _chh:
    _chh = False
    for c in sorted(RIDGE):
        if not _fat0(c, RIDGE): RIDGE.discard(c); _chh = True
# deux bandes de montagne pleine largeur ; chacune porte une grotte (face sud)
MASSIF = set(); DOORS = set()
def band(ytop, ybot, seed, arch, flat_top=False, peak=0):
    wt, wb = wob(seed, W), wob(seed + 1, W)
    for x in range(2, W - 2):
        top = max(2, ytop + 2 * wt[x] - int(round(peak * max(0.0, 1 - ((x - (arch[0] + 1)) / 13.0) ** 2))))
        bot = ybot + (wb[x] if abs(x - (arch[0] + 1)) > 3 else 0)
        top = min(top, bot - 1)
        for y in range(top, bot + 1): MASSIF.add((x, y)); BLOB[(x, y)] = (x, ytop)
    for j in range(3):
        for i in range(3): MASSIF.add((arch[0] + i, arch[1] + j)); BLOB[(arch[0] + i, arch[1] + j)] = (arch[0], arch[1])
    DOORS.add((arch[0] + 1, arch[1] + 2))
band(43, 51, 300, ARCH1, peak=7); band(17, 18, 310, ARCH2, peak=16)
# flancs de la montagne : relient les deux massifs en ANNEAU (une seule montagne, le terrain du milieu est un cratere interieur) ; breche a l'est pour la sortie vers Azuria
_wl, _wr = wob(400, H), wob(401, H)
for y in range(14, 48):
    if EAST_ROWS[0] - 2 <= y <= EAST_ROWS[1] + 2:
        for x in range(2, 5 + _wl[y]): MASSIF.add((x, y)); BLOB[(x, y)] = (2, 30)
        continue
    for x in range(2, 5 + _wl[y]): MASSIF.add((x, y)); BLOB[(x, y)] = (2, 30)
    for x in range(W - 5 - _wr[y], W - 2): MASSIF.add((x, y)); BLOB[(x, y)] = (W - 3, 30)
RIDGE |= MASSIF
PATH -= GAPC
RIDGE -= GAPC
PATH = {c for c in PATH if 0 <= c[0] < W and 0 <= c[1] < H and c not in RIDGE}
def path_id(x, y):
    N = (x, y - 1) in PATH or y == 0; S = (x, y + 1) in PATH or y == H - 1; Wn = (x - 1, y) in PATH; E = (x + 1, y) in PATH or x == W - 1
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
for (x, y) in PATH: put(x, y, 0x3000, path_id(x, y)); OCC[(x, y)] = 'chemin'
for c in RIDGE: OCC[c] = 'roche'
for c in GAPC: OCC[c] = 'herbe'
claim(CENTER[0], CENTER[1], 5, 5, 'centre')
DOORS.add((CENTER[0] + 2, CENTER[1] + 4))
def dil(cells, r):
    return {(x + i, y + j) for (x, y) in cells for i in range(-r, r + 1) for j in range(-r, r + 1)}
PATH_D1 = dil(PATH, 1)
rnd = random.Random(4045)
# ---- lacs : lac de lave (sud, cendre), mare lunaire (nord)
LAKE = set(); LAKE_ST = {}
def lake_shape(cx, cy, rx, ry):
    return {(x, y) for y in range(int(cy - ry) - 1, int(cy + ry) + 2) for x in range(int(cx - rx) - 1, int(cx + rx) + 2)
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.2 * math.sin(x * 1.7 + y * 2.3) <= 1}
_busy = dil(PATH, 2) | dil(RIDGE, 1) | dil(GAPC, 1) | dil({(CENTER[0] + i, CENTER[1] + j) for i in range(5) for j in range(5)}, 2)
for (ya, yb, st_) in ((58, 78, 2), (21, 38, 0)):
    _all = []
    for cy in range(ya, yb):
        for cx in range(4, W - 4):
            cells = lake_shape(cx, cy, 2.6, 3.0)
            if len(cells) >= 18 and not any(c in _busy for c in cells) and all(2 <= c[0] < W - 2 and 2 <= c[1] < H - 3 for c in cells): _all.append((cx, cy, cells))
    print('lacs possibles', st_, len(_all)); assert _all, 'pas de place pour un lac'
    cx, cy, cells = rnd.choice(_all); LAKE |= cells
    for c in cells: LAKE_ST[c] = st_
for c in LAKE: OCC[c] = 'lac'
LAKE_Z = dil(LAKE, 1)
def free_cell(c, r=2):
    return 3 <= c[0] <= W - 4 and 3 <= c[1] <= H - 4 and c not in OCC and c not in GAPC and c not in LAKE_Z and not any((c[0] + i, c[1] + j) in PATH or (c[0] + i, c[1] + j) in RIDGE or (c[0] + i, c[1] + j) in GAPC for i in range(-r, r + 1) for j in range(-r, r + 1))
for _ in range(120):
    if len([1 for v in OCC.values() if v == 'ilot']) > 40: break
    c0 = (rnd.randint(4, W - 5), rnd.randint(4, H - 5))
    if not free_cell(c0): continue
    bw, bh = rnd.choice(((2, 2), (3, 2), (2, 3), (3, 3), (4, 2), (4, 3)))
    blob = {(c0[0] + i, c0[1] + j) for i in range(bw) for j in range(bh)}
    if not all(free_cell(q) for q in blob): continue
    if len(blob) < 4: continue
    for c in blob: RIDGE.add(c); OCC[c] = 'ilot'; BLOB[c] = c0
# ---- panneaux, PNJ, objets caches
def cands_in(xa, xb, ya=3, yb=H - 4, d=(2, 2), extra=()):
    ring = dil(PATH, d[1]) - dil(PATH, d[0] - 1)
    return sorted(c for c in ring if xa <= c[0] <= xb and ya <= c[1] <= yb and c not in OCC and c not in RIDGE and c not in GAPC and c not in LAKE_Z and c not in extra)
SIGNS = {'mtmoon': rnd.choice(cands_in(12, 30, 56, 60)), 'route': rnd.choice(cands_in(8, 28, 74, 80))}
OBJ = {}
DIRS = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}
TR = [('crissy', (20, 40))]
FACE = {}; SIGHT = {}; LINE = set()
for name, (ya, yb) in TR:
    cands = []
    for y in range(ya, yb + 1):
        for x in range(3, W - 3):
            c = (x, y)
            if c in OCC or c in PATH_D1 or c in LAKE_Z or c in GAPC or any(dil({c}, 2) & set(OBJ.values())): continue
            for dn, d in DIRS.items():
                for k in range(2, 5):
                    p = (x + d[0] * k, y + d[1] * k)
                    if not (1 <= p[0] < W - 1 and 1 <= p[1] < H - 1): break
                    if p in PATH and all(((x + d[0] * j, y + d[1] * j) not in OCC) for j in range(1, k)):
                        cands.append((c, dn, k)); break
    assert cands, ('pas de place pour', name)
    c, dn, k = rnd.choice(cands)
    OBJ[name] = c; FACE[name] = dn; SIGHT[name] = k
    d = DIRS[dn]
    for j in range(1, k + 1): LINE.add((c[0] + d[0] * j, c[1] + d[1] * j))
    OCC[c] = 'pnj'
def place_npc(name, xa, xb, ya, yb, r=3):
    cs = sorted(c for c in dil(PATH, r) - PATH_D1 if xa <= c[0] <= xb and ya <= c[1] <= yb and c not in OCC and c not in RIDGE and c not in GAPC and c not in LAKE_Z and c not in LINE and c not in dil(SIGNS.values(), 1)
                and not any(dil({c}, 1) & set(OBJ.values())))
    c = rnd.choice(cs); OBJ[name] = c; OCC[c] = 'pnj'
place_npc('woman', 14, 34, 66, 70)         # a l'accueil du Centre
place_npc('boy', 8, 30, 74, 80)            # pres de l'entree
_PD = dil(PATH, 5)
_dj = [(x, y) for y in range(22, 38) for x in range(3, W - 9) if all(((x + i, y) not in OCC and (x + i, y) not in PATH_D1 and (x + i, y) not in LAKE_Z and (x + i, y) not in GAPC) for i in range(-1, 5)) and (x + 1, y) not in LINE and (x + 2, y) not in LINE and (x + 1, y) in _PD]
_x, _y = rnd.choice(_dj)
OBJ['mpunch'] = (_x, _y); OBJ['mkick'] = (_x + 3, _y); OCC[(_x, _y)] = 'pnj'; OCC[(_x + 3, _y)] = 'pnj'
def hid_cell(xa, xb, ya=3, yb=H - 4):
    cs = [c for c in cands_in(xa, xb, ya, yb, (2, 3)) if c not in LINE and not any((c[0] + i, c[1] + j) in OCC and OCC[(c[0] + i, c[1] + j)] != 'chemin' for i in (-1, 0, 1) for j in (-1, 0, 1))]
    c = rnd.choice(cs); OCC[c] = 'item'; return c
HID = {'great': hid_cell(2, W - 3, 53, 60), 'persim': hid_cell(2, W - 3, 74, 78), 'razz': hid_cell(2, W - 3, 20, 40)}
OBJ['tm05'] = hid_cell(2, W - 3, 20, 40)
for k in ('great', 'persim', 'razz'): del OCC[HID[k]]
del OCC[OBJ['tm05']]
RES = dil(list(OBJ.values()) + list(SIGNS.values()) + list(HID.values()), 1) | LINE
CORR = dil(PATH, 1) | LAKE_Z | LINE | dil(list(OBJ.values()) + list(SIGNS.values()) + list(HID.values()), 2)
CORR -= RIDGE | GAPC
PATCHZ = dil(PATH, 3)
TALL = []
tries = 0
while len(TALL) < 9 and tries < 20000:
    tries += 1; x0 = rnd.randint(3, W - 8); y0 = rnd.randint(3, H - 7); w, h = rnd.choice([(2, 3), (3, 3), (4, 2), (3, 2), (2, 4)])
    cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    if any(c not in PATCHZ or c in OCC or c in RES or c in PATH_D1 or c in LAKE_Z for c in cells): continue
    TALL.append((x0, y0, x0 + w - 1, y0 + h - 1))
    for c in cells: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M, st=1)
DEAD = []
def tree_p(y): return max(0.10, min(0.6, 0.6 - (62 - y) * 0.012))
for (ox, oy) in ((0, 0), (1, 1), (1, 0), (0, 1)):
    for y in range(2 + oy, H - 3, 2):
        for x in range(2 + ox, W - 3, 2):
            cells = [(x + i, y + j) for i in range(2) for j in range(2)]
            if any(c in PATH_D1 or c in OCC or c in RES or c in LAKE_Z or c in RIDGE or c in GAPC for c in cells): continue
            if rnd.random() < tree_p(y): tree(x, y); claim(x, y, 2, 2, 'arbre')
            else:
                kind = rnd.choice(['dead', 'dead', 'boulder', 'thorns'] if y >= 52 else ['crater', 'crater', 'boulder', 'spire'])
                if y < 52 and rnd.random() < 0.55: continue
                DEAD.append((x, y, kind)); claim(x, y, 2, 2, kind)
ASH = set()
for y in range(2, H - 2):
    for x in range(2, W - 2):
        c = (x, y)
        if c in OCC or c in RES: continue
        n = math.sin(x * 0.45 + y * 0.3) + math.sin(y * 0.6 - x * 0.2) + math.sin(x * 0.17 + y * 0.5)
        if n > 0.5: put(x, y, 0x3000, GRASS_M, st=1); ASH.add(c)
# ---- art : cristaux (prismes de grenat -> domes d'opale), pierre du degrade
LG = E.load('general', 'petalburg')
def grass_cols(st):
    L = (LG[0], LG[1], [stage_pal(i, TS_[st]) for i in range(6)] + LG[2][6:], LG[3], LG[4])
    cnt = collections.Counter(E.metatile(L, GRASS_M).convert('RGB').getdata()); cols = [c for c, _ in cnt.most_common(4)]
    while len(cols) < 4: cols.append(cols[-1])
    return cols
GARNET = [(14, 18, 40), (40, 50, 86), (104, 118, 160), (186, 198, 230), (244, 248, 255), (255, 150, 176), (150, 236, 255), (104, 150, 255)]      # opale (depart)
OPAL = [(16, 6, 8), (46, 16, 16), (92, 34, 26), (156, 64, 34), (255, 224, 168), (255, 96, 32), (255, 172, 40), (255, 64, 84)]                # braise / obsidienne (arrivee)
def art_pal(st):
    g = grass_cols(st); t = TS_[st]
    cols = [lerp(GARNET[i], OPAL[i], t) for i in range(8)]
    sh = tuple(int(c * 0.55) for c in min(g, key=sum))
    return [(0, 0, 0)] + g + cols + [sh, lerp((74, 84, 116), (86, 70, 72), t), lerp((138, 150, 184), (146, 120, 116), t)], g
for st in (0, 2):
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
def sign_art(st):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im); d.ellipse((2, 12, 14, 15), fill=13)
    d.rectangle((7, 8, 8, 14), fill=6, outline=5); d.rectangle((2, 2, 13, 9), fill=8, outline=5)
    for y in (4, 6): d.line([(4, y), (11, y)], fill=6)
    return im
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
def lake_tile(x, y, st, var):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im)
    n = (x, y - 1) in LAKE; so = (x, y + 1) in LAKE; w = (x - 1, y) in LAKE; e = (x + 1, y) in LAKE
    x0, y0, x1, y1 = (0 if w else 0), (0 if n else 0), 15, 15
    d.rectangle((0, 0, 15, 15), fill=14)
    L = 3 if not w else 0; R = 12 if not e else 15; T = 3 if not n else 0; B = 12 if not so else 15
    # rebord de roche : tout est roche, puis on creuse le bassin de lave
    d.rectangle((L, T, R, B), fill=6)
    ix0, iy0, ix1, iy1 = L + (1 if not w else 0), T + (1 if not n else 0), R - (1 if not e else 0), B - (1 if not so else 0)
    d.rectangle((ix0, iy0, ix1, iy1), fill=12)
    # coins rentrants : roche dans l'angle si les deux voisins existent mais pas la diagonale
    for (dx, dy, cx, cy) in ((-1, -1, 0, 0), (1, -1, 12, 0), (-1, 1, 0, 12), (1, 1, 12, 12)):
        if (x + dx, y) in LAKE and (x, y + dy) in LAKE and (x + dx, y + dy) not in LAKE: d.rectangle((cx, cy, cx + 3, cy + 3), fill=14); d.rectangle((cx + (0 if dx < 0 else 1), cy + (0 if dy < 0 else 1), cx + (2 if dx < 0 else 3), cy + (2 if dy < 0 else 3)), fill=6)
    if var == 2: d.polygon([(ix0 + 3, iy0 + 4), (ix0 + 8, iy0 + 3), (ix0 + 10, iy0 + 7), (ix0 + 5, iy0 + 8)], fill=6); d.point((ix0 + 6, iy0 + 5), fill=(11 if st == 0 else 10)); d.point((ix1 - 3, iy1 - 3), fill=11)
    elif var == 0: d.ellipse((ix0 + 2, iy0 + 3, ix0 + 7, iy0 + 6), fill=(11 if st == 0 else 10)); d.point((ix0 + 4, iy0 + 4), fill=11); d.ellipse((ix1 - 6, iy1 - 4, ix1 - 2, iy1 - 2), fill=(11 if st == 0 else 10))
    else: d.ellipse((ix1 - 7, iy0 + 2, ix1 - 2, iy0 + 5), fill=(11 if st == 0 else 10)); d.point((ix1 - 4, iy0 + 3), fill=11); d.ellipse((ix0 + 2, iy1 - 5, ix0 + 6, iy1 - 2), fill=(11 if st == 0 else 10)); d.point((ix0 + 4, iy1 - 4), fill=11)
    # contour exterieur de la roche
    for (cond, line) in ((not n, (0, 0, 15, 0)), (not so, (0, 15, 15, 15)), (not w, (0, 0, 0, 15)), (not e, (15, 0, 15, 15))):
        if cond: d.line(line, fill=5)
    # ombre cote sud / roche claire cote nord
    if not n: d.line((1, 1, 14, 1), fill=15)
    return im
# ---- art propre a la Route 4 : cratere, trou, Centre, arche de grotte
def crater_small(st):
    im = ground_bg(32, 32, st); d = ImageDraw.Draw(im)
    d.ellipse((1, 19, 30, 31), fill=13)
    d.ellipse((2, 6, 29, 28), fill=8, outline=5)
    d.ellipse((5, 10, 26, 25), fill=6, outline=5)
    d.ellipse((7, 13, 24, 24), fill=5)
    d.arc((7, 13, 24, 24), 200, 340, fill=7)
    d.line([(6, 8), (13, 6)], fill=9); d.line([(18, 7), (24, 9)], fill=9)
    for p in ((4, 12), (27, 14), (14, 27), (22, 27)): d.point(p, fill=7)
    d.point((15, 19), fill=11)
    return im
def pit_img(st):
    im = ground_bg(16, 16, st); d = ImageDraw.Draw(im)
    d.ellipse((2, 8, 14, 15), fill=13)
    d.ellipse((2, 5, 13, 13), fill=8, outline=5)
    d.ellipse((4, 7, 11, 12), fill=6)
    d.point((6, 6), fill=9); d.point((9, 6), fill=9)
    return im
def center_img(st):
    """Centre Pokemon 5x3 : murs clairs, toit rouge, emblème ; la porte est la case basse du milieu (colonne 2)."""
    im = ground_bg(80, 48, st); d = ImageDraw.Draw(im)
    d.ellipse((0, 39, 79, 47), fill=13)
    d.rectangle((6, 22, 73, 43), fill=9, outline=5); d.rectangle((7, 40, 72, 42), fill=8)
    for x in range(14, 72, 12): d.line([(x, 24), (x, 38)], fill=8)
    d.polygon([(1, 25), (10, 4), (69, 4), (78, 25)], fill=12, outline=5)
    d.polygon([(1, 25), (4, 18), (75, 18), (78, 25)], fill=7)
    for y in range(8, 18, 4): d.line([(10 - (y - 4) // 3, y), (69 + (y - 4) // 3, y)], fill=6)
    d.line([(11, 5), (68, 5)], fill=11); d.rectangle((2, 22, 77, 25), fill=7, outline=5)
    d.ellipse((34, 7, 46, 19), fill=9, outline=5); d.line([(34, 13), (46, 13)], fill=5); d.ellipse((38, 10, 42, 15), fill=9, outline=5)
    d.rectangle((34, 28, 45, 43), fill=5); d.rectangle((36, 30, 43, 43), fill=11); d.line([(40, 30), (40, 43)], fill=5); d.line([(36, 36), (43, 36)], fill=8)
    for x0 in (10, 58):
        d.rectangle((x0, 29, x0 + 11, 37), fill=5); d.rectangle((x0 + 2, 31, x0 + 9, 35), fill=11); d.line([(x0 + 5, 31), (x0 + 5, 35)], fill=5); d.line([(x0 + 2, 33), (x0 + 9, 33)], fill=5)
    d.rectangle((30, 22, 49, 26), fill=8, outline=5); d.rectangle((38, 22, 41, 26), fill=12)
    return im
def arch_img(st):
    """entree de grotte 3x3 taillee dans la montagne ; la porte est la case basse du milieu."""
    im = ground_bg(48, 48, st); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 47, 47), fill=14)
    rr = random.Random(77)
    for _ in range(7):
        sx = rr.randint(1, 36); sy = rr.randint(2, 40); ln = rr.randint(3, 7)
        d.line([(sx, sy), (sx + ln, sy + ln // 2)], fill=13); d.line([(sx, sy - 1), (sx + ln - 1, sy + ln // 2 - 1)], fill=15)
    d.rectangle((5, 24, 42, 47), fill=15, outline=5); d.ellipse((5, 5, 42, 43), fill=15, outline=5)
    d.rectangle((6, 25, 41, 47), fill=8); d.ellipse((6, 6, 41, 42), fill=8)
    d.rectangle((12, 25, 35, 47), fill=5); d.ellipse((12, 12, 35, 38), fill=5)
    d.rectangle((15, 29, 32, 47), fill=6); d.ellipse((15, 17, 32, 34), fill=6)
    d.rectangle((19, 34, 28, 47), fill=5); d.ellipse((19, 24, 28, 38), fill=5)
    d.rectangle((13, 41, 34, 47), fill=5)
    d.rectangle((21, 4, 26, 9), fill=8, outline=5); d.point((23, 6), fill=11)
    d.line([(8, 20), (14, 10)], fill=9); d.line([(34, 10), (40, 20)], fill=9)
    shape(d, 0, 4, 47, 3, 9); shape(d, 0, 43, 47, 3, 8)
    d.line([(0, 47), (11, 47)], fill=13); d.line([(36, 47), (47, 47)], fill=13)
    return im
def art_st(x, y): return 2 if y >= 52 else 0
for st in (0, 2):
    ART[('sm0', st)] = meta(small(st, 0), st); ART[('sm1', st)] = meta(small(st, 1), st)
    ART[('sign', st)] = meta(sign_art(st), st)
    b = boulder_img(st); ART[('boulder', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
for st in (2,):
    ART[('vent', st)] = meta(vent_img(st), st); ART[('stump', st)] = meta(stump_img(st), st); ART[('ash', st)] = meta(ash_img(st), st)
    for var in (0, 1):
        b = dead_img(st, var); ART[('dead', st, var)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
    b = thorns_img(st); ART[('thorns', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
for st in (0,):
    b = spire_img(st); ART[('spire', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
    b = crater_small(st); ART[('crater', st)] = {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
    ART[('pit', st)] = meta(pit_img(st), st)
for c in LAKE: ART[('lake', c)] = meta(lake_tile(c[0], c[1], LAKE_ST[c], 0), LAKE_ST[c])

# ---- placement
def near(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if (x + i, y + j) in OCC or (x + i, y + j) in ART_PLACE: return True
    return False
for c in SIGNS.values(): claim(c[0], c[1], 1, 1, 'panneau'); ART_PLACE[c] = ART[('sign', art_st(*c))]
for (x, y, kind) in DEAD:
    st = 2 if kind in ('dead', 'thorns') else 0 if kind in ('crater', 'spire') else art_st(x, y)
    arts = ART[('dead', 2, rnd.randrange(2))] if kind == 'dead' else ART[(kind, st)]
    for (i, j), k in arts.items(): ART_PLACE[(x + i, y + j)] = k
for c in LAKE: del OCC[c]
for c in LAKE: claim(c[0], c[1], 1, 1, 'lac')
for c in LAKE: ART_PLACE[c] = ART[('lake', c)]
MTN = {"11111111": 113, "11111011": 178, "11011011": 121, "11011001": 121, "11011101": 121, "11111101": 179, "10111011": 114, "11101101": 179, "11111001": 121, "11011111": 121, "10110011": 114, "11101100": 112, "10101001": 133, "11001101": 120, "10011011": 122, "11101001": 133, "10011001": 122, "10010001": 122, "10100000": 133, "10101000": 133, "10001001": 159, "11001100": 120, "10100100": 133, "10100010": 134, "00000000": 159, "11000000": 141, "01010001": 135, "00010000": 177, "01000000": 176, "01011000": 135, "10010000": 142, "01010000": 135, "00010001": 177, "11110011": 498, "01010011": 135, "01010101": 135, "00110100": 111, "11000001": 141, "10110111": 114, "11110111": 186, "01110111": 105, "01110110": 105, "00110110": 106, "00110010": 106, "01110010": 106, "01010010": 176, "01100110": 104, "01111110": 105, "11111110": 187}
D8 = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
def is_m(c): return c in RIDGE or c[0] < 2 or c[0] >= W - 2 or c[1] < 2 or c[1] >= H - 2
def mtn_id(x, y):
    sig = ''.join('1' if is_m((x + dx, y + dy)) else '0' for dx, dy in D8)
    if sig == '11111111': return (113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 108, 108, 187)[((x * 73856093) ^ (y * 19349663)) % 25]
    if sig in MTN: return MTN[sig]
    return MTN[min(MTN, key=lambda k: sum((a_ != b_) * (4 if i_ < 4 else 1) for i_, (a_, b_) in enumerate(zip(k, sig))))]
# ---- montagne et Centre : metatuiles d'ORIGINE de FireRed (le tileset primaire du hack est celui d'Emeraude : on recopie les images en tuiles d'art,
#      couche haute transparente la ou l'original montre de l'herbe, couche basse = herbe du degrade). Roche : rampe ardoise (emplacement 10) ; Centre : couleurs d'origine (emplacement 12).
sys.path.insert(0, 'tools/topaze/maps')
import mapkit
_FP = mapkit.Tileset('gTileset_General'); _FS = mapkit.Tileset('gTileset_CeruleanCity')
def fr_img(m):
    ts_m = _FP.metatiles if m < 640 else _FS.metatiles
    e = struct.unpack('<8H', ts_m[(m if m < 640 else m - 640) * 16:][:16])
    out = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); op = out.load()
    for layer in range(2):
        for q in range(4):
            v = e[layer * 4 + q]; tid, hf, vf, pn = v & 0x3ff, (v >> 10) & 1, (v >> 11) & 1, v >> 12
            src = _FP if tid < 640 else _FS; t = tid if tid < 640 else tid - 640; tw = src.img.width // 8
            tile = src.img.crop(((t % tw) * 8, (t // tw) * 8, (t % tw) * 8 + 8, (t // tw) * 8 + 8))
            if hf: tile = tile.transpose(Image.FLIP_LEFT_RIGHT)
            if vf: tile = tile.transpose(Image.FLIP_TOP_BOTTOM)
            pl = (_FP if pn < 7 else _FS).pals[pn]; px = tile.load()
            for yy in range(8):
                for xx in range(8):
                    c = px[xx, yy]
                    if c: op[(q % 2) * 8 + xx, (q // 2) * 8 + yy] = pl[c] + (255,)
    for y_ in range(16):
        for x_ in range(16):
            r_, g_, b_, a_ = op[x_, y_]
            if a_:
                h_, l_, s_ = colorsys.rgb_to_hls(r_ / 255, g_ / 255, b_ / 255)
                if 70 <= h_ * 360 <= 190 and s_ > 0.22: op[x_, y_] = (0, 0, 0, 0)          # herbe d'origine -> transparent (la couche basse montre l'herbe du degrade)
    return out
LAY = []; LAY_KEY = {}; LPLACE = {}
def grass_bottom(st):
    e = struct.unpack('<8H', mt[GRASS_M * 16:GRASS_M * 16 + 16])
    return [(q & 0xfff) | (SLOT[st].get(q >> 12, q >> 12) << 12) for q in e[:4]]
def lay_meta(tiles4, slot, st, att=0):
    key = (tuple(tiles4), slot, st, att)
    if key not in LAY_KEY: LAY.append((grass_bottom(st), list(tiles4), slot, att)); LAY_KEY[key] = len(LAY) - 1
    return LAY_KEY[key]
def put_lay(x, y, raw, tiles4, slot):
    G[(x, y)] = raw; LPLACE[(x, y)] = lay_meta(tiles4, slot, stage_at(x, y))
def slice4(im):
    px = im.load(); out = []
    for q in range(4):
        out.append(add_tile([px[(q % 2) * 8 + i, (q // 2) * 8 + j] for j in range(8) for i in range(8)]))
    return out
def lum(c): return (0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255.0
# ilots : on ne garde que des blocs gras (chaque case dans un 2x2 plein) dont la signature existe dans la table d'origine
def _fat(c):
    for ox in (0, -1):
        for oy in (0, -1):
            if all(((c[0] + ox + i, c[1] + oy + j) in RIDGE) for i in (0, 1) for j in (0, 1)): return True
    return False
def _sig(c): return ''.join('1' if is_m((c[0] + dx, c[1] + dy)) else '0' for dx, dy in D8)
_ch = True
while _ch:
    _ch = False
    for c in sorted(k for k, v in OCC.items() if v == 'ilot'):
        if c in RIDGE and not _fat(c):
            RIDGE.discard(c); del OCC[c]; _ch = True
print('ilots restants', sum(1 for v in OCC.values() if v == 'ilot'))
MTN_IDS = sorted(set(MTN.values()) | {113, 108, 187, 169})
_mimg = {m: fr_img(m) for m in MTN_IDS}
_ls = [lum(p[:3]) for im in _mimg.values() for p in im.getdata() if p[3]]
_lo, _hi = sorted(_ls)[len(_ls) // 50], sorted(_ls)[-len(_ls) // 50]
RAMP = [lerp((12, 14, 32), (150, 158, 190), (k / 14.0) ** 1.1) for k in range(15)]
PALS[10] = [(0, 0, 0)] + RAMP
def mtn_tiles(m):
    im = _mimg[m]; px = im.load(); o = Image.new('P', (16, 16), 0); op = o.load()
    lo_, hi_ = _lo, _hi
    if m == 169:
        l_ = sorted(lum(q[:3]) for q in im.getdata() if q[3]); lo_, hi_ = l_[0], l_[-1] + 1e-6
    for y_ in range(16):
        for x_ in range(16):
            p = px[x_, y_]
            if p[3]: op[x_, y_] = 1 + max(0, min(14, int(round((lum(p[:3]) - lo_) / (hi_ - lo_) * 14))))
    return slice4(o)
MT_T = {m: mtn_tiles(m) for m in MTN_IDS}
# Centre : 25 metatuiles, couleurs d'origine quantifiees sur 15 teintes
CM = [[640, 641, 642, 643, 644], [72, 73, 74, 75, 391], [80, 81, 82, 83, 399], [88, 89, 90, 91, 407], [96, 97, 98, 390, 415]]
_cimg = {m: fr_img(m) for r_ in CM for m in r_}
_cp = [p[:3] for im in _cimg.values() for p in im.getdata() if p[3]]
_qi = Image.new('RGB', (len(_cp), 1)); _qi.putdata(_cp); _qq = _qi.quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
_qp = _qq.getpalette()[:45]; PALS[12] = [(0, 0, 0)] + [tuple(_qp[3 * k:3 * k + 3]) for k in range(15)]
def nearest12(c): return 1 + min(range(15), key=lambda k: sum((PALS[12][k + 1][i] - c[i]) ** 2 for i in range(3)))
CEN_T = {}
for m, im in _cimg.items():
    px = im.load(); o = Image.new('P', (16, 16), 0); op = o.load()
    for y_ in range(16):
        for x_ in range(16):
            if px[x_, y_][3]: op[x_, y_] = nearest12(px[x_, y_][:3])
    CEN_T[m] = slice4(o)
for _j, _row in enumerate(CM):
    for _i, _m in enumerate(_row):
        _door = (_i, _j) == (2, 4)
        put_lay(CENTER[0] + _i, CENTER[1] + _j, 0x3000 if _door else 0x400, CEN_T[_m], 12)
for (x, y) in sorted(RIDGE):
    if (x, y) in DOORS: put_lay(x, y, 0x3000, MT_T[169], 10); continue
    put_lay(x, y, 0x400, MT_T[mtn_id(x, y)], 10)
# la breche : herbe haute sur toute la zone
for c in GAPC: put(c[0], c[1], 0x3000, TALL_M, st=1)
PATH_D = dil(PATH, 1)
# ---- cases isolees (ou la grille d'arbres ne tient pas) : plus de sol nu
for y in range(2, H - 2):
    for x in range(2, W - 2):
        c = (x, y)
        if c in OCC or c in PATH_D or c in RES or c in LAKE_Z or c in ASH or c in ART_PLACE or (G[c] & 0xc00): continue
        if rnd.random() < (0.8 if y >= 52 else 0.4):
            nm = rnd.choice(['sm0', 'sm1', 'stump', 'sm0', 'sm1']) if y >= 52 else rnd.choice(['pit', 'sm0', 'sm1', 'pit', None, None])
            if nm is None: continue
            claim(x, y, 1, 1, 'rocaille'); ART_PLACE[c] = ART[(nm, art_st(x, y))]
OPEN = sorted(c for c in CORR if c not in OCC and c not in RES and c not in PATH_D and c not in LINE and c not in ASH and c not in LAKE_Z and 2 <= c[0] <= W - 3 and 2 <= c[1] <= H - 4)
def scatter(n, fn):
    k = tries = 0
    while k < n and tries < 3000:
        tries += 1
        if not OPEN: return
        c = rnd.choice(OPEN)
        if fn(c): k += 1
def one(name):
    def f(c):
        if near(c[0], c[1], 1) or c in ART_PLACE or c[1] < 52: return False
        claim(c[0], c[1], 1, 1, name); ART_PLACE[c] = ART[(name_map[name], 2)]; return True
    return f
name_map = {'vent': 'vent', 'souche': 'stump', 'cendre': 'ash'}
for nm, n in (('vent', 12), ('souche', 8), ('cendre', 8)): scatter(n, one(nm))
# ---- accessibilite
ART_RAW_BLOCK = set(ART_PLACE) - DOORS
def blocked(c):
    return c in ART_RAW_BLOCK or bool(G[c] & 0xc00)
def flood(s0, extra=()):
    seen_ = {s0}; q_ = collections.deque([s0])
    while q_:
        c = q_.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n_ = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n_[0] < W and 0 <= n_[1] < H and n_ not in seen_ and n_ not in extra and not blocked(n_): seen_.add(n_); q_.append(n_)
    return seen_
START = (19, H - 1); EXIT = (W - 1, 35)
seen = flood(START) | flood((ARCH2[0] + 1, ARCH2[1] + 2))
assert EXIT not in flood(START), 'la sortie est atteignable sans passer par le Mont Selenite'
assert (ARCH1[0] + 1, ARCH1[1] + 2) in flood(START) and (ARCH2[0] + 1, ARCH2[1] + 2) not in flood(START)
for c in [EXIT] + [(x, H - 1) for x in range(SOUTH_COLS[0], SOUTH_COLS[1] + 1)] + [(W - 1, y) for y in range(EAST_ROWS[0], EAST_ROWS[1] + 1)] + list(OBJ.values()) + list(HID.values()) + sorted(DOORS): assert c in seen, ('inaccessible', c)
for (x0, y0, x1, y1) in TALL: assert (x0, y0) in seen, ('herbe inaccessible', x0, y0)
for c in SIGNS.values(): assert any((c[0] + dx, c[1] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), ('panneau inaccessible', c)
assert (ARCH1[0] + 1, ARCH1[1] + 2) not in flood(START, extra=GAPC), 'la grotte est atteignable sans traverser la breche en herbe'
for k in FACE:
    x, y = OBJ[k]; d_ = DIRS[FACE[k]]
    for j in range(1, SIGHT[k] + 1):
        c = (x + d_[0] * j, y + d_[1] * j)
        assert not blocked(c) or c in PATH, ('ligne de vue coupee', k, c)
print('regards', FACE)

# ------------------------------------------------------------------ ecriture
for _m in (468, 469, 476, 477): variant(_m, 1)
NT = 0
ART_ID = {}
for k, ents in enumerate(ART_E):
    SEC_ENT.append([(640 + t) | (slot << 12) for (_, t, slot) in ents] + [0, 0, 0, 0]); SEC_ATT.append(0)
    ART_ID[k] = 640 + len(SEC_ENT) - 1
LAY_ID = {}
for k, (bot, tops, slot, att) in enumerate(LAY):
    SEC_ENT.append(bot + [(640 + t) | (slot << 12) for t in tops]); SEC_ATT.append(att); LAY_ID[k] = 640 + len(SEC_ENT) - 1
for c, k in LPLACE.items(): G[c] |= LAY_ID[k]
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
def add(path, text):
    s = open(path).read()
    if 'GeneralMoon' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralMoon[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralMoon[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_MoonRoad[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_MoonRoad[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralMoon[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralMoon[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_MoonRoad[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_MoonRoad[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralMoon =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralMoon,
    .palettes = gTilesetPalettes_GeneralMoon,
    .metatiles = gMetatiles_GeneralMoon,
    .metatileAttributes = gMetatileAttributes_GeneralMoon,
    .callback = NULL,
};

const struct Tileset gTileset_MoonRoad =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MoonRoad,
    .palettes = gTilesetPalettes_MoonRoad,
    .metatiles = gMetatiles_MoonRoad,
    .metatileAttributes = gMetatileAttributes_MoonRoad,
    .callback = NULL,
};
''')
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/Route4/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/Route4/border.bin', 'wb').write(struct.pack('<4H', *[0x400 | variant(m, 1) for m in (468, 469, 476, 477)]))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_ROUTE4': l.update(width=W, height=H, primary_tileset='gTileset_GeneralMoon', secondary_tileset='gTileset_MoonRoad')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'w': W, 'h': H, 'obj': OBJ, 'hid': HID, 'signs': SIGNS, 'face': FACE, 'sight': SIGHT, 'tall': TALL, 'gap': sorted(GAPC), 'center': CENTER, 'arch1': ARCH1, 'arch2': ARCH2, 'doors': sorted(DOORS), 'south_cols': SOUTH_COLS, 'east_rows': EAST_ROWS}, open('/tmp/route4_info.json', 'w'))
blk = sorted([x, y] for (x, y) in ((x, y) for y in range(H) for x in range(W)) if blocked((x, y)))
json.dump({'w': W, 'h': H, 'blocked': blk}, open('/tmp/route4_col.json', 'w'))
print('route 4 : metatuiles', len(SEC_ENT), 'tuiles art', len(ART_T))
