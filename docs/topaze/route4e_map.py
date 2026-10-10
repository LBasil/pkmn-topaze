# ROUTE 4 EST « le sentier de tourmaline » (sortie de la Route 4 -> Tourmalia), poussiere lunaire (ouest) -> foret naturelle a cristaux de tourmaline (est) ; derive de route4_map.py
# (en-tete herite) ROUTE 4 « le flanc de lune » (Route 3 -> Mont Selenite -> Azuria), cendre -> paysage lunaire ; base de route3_map.py (pyropia -> lune)
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
PRI = 'data/tilesets/primary/general_moonwood/'; SEC = 'data/tilesets/secondary/moonwood_road/'
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
def tint_opal(r, g, b):        # teinte d'arrivee = couleurs naturelles d'Emeraude (foret de Tourmalia)
    return r, g, b
def _tint_opal_old(r, g, b):
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
W, H = 72, 30
GRASS_M, FLOWER_M, TALL_M = 1, 4, 13
TREE = [[468, 469], [476, 477]]
G = {}; OCC = {}; STG = {}
rnd = random.Random(1011)
def _tg(x): return max(0.0, min(1.0, (x - 14) / 40.0))
def stage_at(x, y):
    if x <= 3 or x >= W - 4 or y <= 3 or y >= H - 4: return stage_smooth(x, y)
    n = 0.35 * math.sin(x * 0.55 + y * 0.21) + 0.25 * math.sin(y * 0.37 - x * 0.3) + 0.2 * math.sin(x * 0.23 + y * 0.6)
    j = ((x * 73856093) ^ (y * 19349663)) % 1000 / 1000.0 - 0.5
    return max(0, min(2, int(round(2 * _tg(x) + n * 0.45 + j * 0.5))))
def stage_smooth(x, y):
    n = 0.35 * math.sin(x * 0.55 + y * 0.21) + 0.25 * math.sin(y * 0.37 - x * 0.3) + 0.2 * math.sin(x * 0.23 + y * 0.6)
    return max(0, min(2, int(round(2 * _tg(x) + n * 0.3))))

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
# ======================================================================== ROUTE 4 EST « le sentier de tourmaline » : de la poussiere lunaire (ouest, Route 4) a la forêt de tourmaline (est, Tourmalia)
EXIT_ROWS = (14, 17)
for x in range(0, W - 2, 2):
    tree(x, 0); tree(x, H - 2)
for y in range(2, H - 2, 2):
    if not (EXIT_ROWS[0] <= y <= EXIT_ROWS[1]): tree(0, y); tree(W - 2, y)
KNOTS = [(0, 15.5), (9, 15.5), (15, 12.0), (22, 8.5), (30, 11.5), (37, 17.5), (45, 21.5), (53, 17.0), (60, 12.5), (66, 15.0), (W - 10, 15.5), (W - 1, 15.5)]
def cline(x):
    for (x0, y0), (x1, y1) in zip(KNOTS, KNOTS[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0); t = t * t * (3 - 2 * t); return y0 + (y1 - y0) * t
    return 15.5
def halfw(x):
    h = 4.6 + 1.5 * math.sin(0.19 * x + 1) + 0.9 * math.sin(0.43 * x + 2)
    return 3.0 if (x < 6 or x > W - 7) else h
PATH = set()
for x in range(0, W):
    yc = int(round(cline(x) - 0.5))
    PATH.add((x, yc)); PATH.add((x, yc + 1))
    if x + 1 < W: PATH.add((x + 1, yc))
for x in list(range(0, 5)) + list(range(W - 5, W)):
    for y in range(EXIT_ROWS[0], EXIT_ROWS[1] + 1): PATH.add((x, y))
OPEN = set()
for x in range(2, W - 2):
    for y in range(2, H - 2):
        if abs(y - cline(x)) <= halfw(x): OPEN.add((x, y))
POCKETS = []
for x0, side in ((13, -1), (26, 1), (39, -1), (49, 1), (58, -1), (31, 1)):
    cy = cline(x0) + side * (halfw(x0) + 2.5); rx, ry = 5.0, 3.6
    POCKETS.append((x0, int(round(cy))))
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(x0 - rx) - 1, int(x0 + rx) + 2):
            if ((x - x0) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.15 * math.sin(x * 1.9 + y * 2.3) <= 1 and 4 <= y <= H - 5 and 3 <= x <= W - 4: OPEN.add((x, y))
for x in range(0, 6):
    for y in range(EXIT_ROWS[0] - 1, EXIT_ROWS[1] + 2): OPEN.add((x, y))
for x in range(W - 6, W):
    for y in range(EXIT_ROWS[0] - 1, EXIT_ROWS[1] + 2): OPEN.add((x, y))
def nz(x, y): return 0.5 * math.sin(x * 0.31 + y * 0.17) + 0.35 * math.sin(y * 0.43 - x * 0.12 + 1) + 0.3 * math.sin(x * 0.11 + y * 0.52 + 2)
def thr(x): return -2.0 if x < 8 else -0.9 + 1.9 * min(1.0, (x - 8) / (W - 12.0))
RIDGE = set(); BLOB = {}
for x in range(2, W - 2):
    for y in range(2, H - 2):
        if (x, y) in OPEN or (x, y) in PATH: continue
        if nz(x, y) > thr(x): RIDGE.add((x, y)); BLOB[(x, y)] = (x, y)
def _fat0(c, S):
    return any(all(((c[0] + ox + i, c[1] + oy + j) in S) for i in (0, 1) for j in (0, 1)) for ox in (0, -1) for oy in (0, -1))
_chh = True
while _chh:
    _chh = False
    for c in sorted(RIDGE):
        if not _fat0(c, RIDGE): RIDGE.discard(c); _chh = True
DOORS = set(); GAPC = set(); LAKE = set(); LAKE_Z = set(); LINE = set(); ASH = set()
for c in RIDGE: OCC[c] = 'roche'
def path_id(x, y):
    N = (x, y - 1) in PATH; S = (x, y + 1) in PATH; Wn = (x - 1, y) in PATH or x == 0; E = (x + 1, y) in PATH or x == W - 1
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
PATH = {c for c in PATH if c not in RIDGE}
for (x, y) in PATH: put(x, y, 0x3000, path_id(x, y), st=stage_at(x, y)); OCC[(x, y)] = 'chemin'
def dil(cells, r):
    return {(x + i, y + j) for (x, y) in cells for i in range(-r, r + 1) for j in range(-r, r + 1)}
PATH_D1 = dil(PATH, 1)
rnd = random.Random(4046)
def cands_in(xa, xb, d=(2, 2)):
    ring = dil(PATH, d[1]) - dil(PATH, d[0] - 1)
    return sorted(c for c in ring if xa <= c[0] <= xb and c in OPEN and c not in OCC and c not in RIDGE)
SIGNS = {'west': rnd.choice(cands_in(6, 12)), 'east': rnd.choice(cands_in(W - 14, W - 8))}
OBJ = {}; HID = {}; FACE = {}; SIGHT = {}
RES = dil(list(SIGNS.values()), 1)
CORR = set(OPEN)
for c in SIGNS.values(): OCC[c] = 'panneau'
# herbe haute : taches pres du chemin
PATCHZ = dil(PATH, 3) & OPEN
TALL = []
tries = 0
while len(TALL) < 12 and tries < 20000:
    tries += 1; x0 = rnd.randint(4, W - 9); y0 = rnd.randint(3, H - 6); w, h = rnd.choice([(2, 3), (3, 3), (4, 2), (3, 2), (2, 4)])
    cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    if any(c not in PATCHZ or c in OCC or c in RES or c in PATH_D1 for c in cells): continue
    TALL.append((x0, y0, x0 + w - 1, y0 + h - 1))
    for c in cells: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M, st=1)
# monolithe du degrade (3x3) : sur le site ou la poussiere lunaire devient verte
BIG = None
for _ in range(4000):
    x0 = rnd.randint(int(W * 0.40), int(W * 0.52)); y0 = rnd.randint(3, H - 6)
    cells = [(x0 + i, y0 + j) for i in range(3) for j in range(3)]
    if all(c in OPEN and c not in OCC and c not in RES and c not in PATH_D1 for c in cells) and any(abs(x0 + 1 - px) + abs(y0 + 1 - py) <= 6 for (px, py) in PATH):
        BIG = (x0, y0); break
assert BIG, 'pas de place pour le monolithe'
claim(BIG[0], BIG[1], 3, 3, 'monolithe')
# arbres : grille 2x2 ; dense hors de l'ouverture, clairseme dedans
DEAD = []
def tree_p(x, inside): return (0.10 + 0.16 * x / W) if inside else 0.82
for (ox, oy) in ((0, 0), (1, 1), (1, 0), (0, 1)):
    for y in range(2 + oy, H - 3, 2):
        for x in range(2 + ox, W - 3, 2):
            cells = [(x + i, y + j) for i in range(2) for j in range(2)]
            if any(c in PATH_D1 or c in OCC or c in RES or c in RIDGE for c in cells): continue
            inside = all(c in OPEN for c in cells)
            if any(c in OPEN for c in cells) and not inside: continue
            if rnd.random() < tree_p(x, inside): tree(x, y); claim(x, y, 2, 2, 'arbre')
            elif not inside:
                kind = rnd.choice(['boulder', 'spire', 'spire'] if x > W * 0.35 else ['crater', 'boulder', 'spire'])
                DEAD.append((x, y, kind)); claim(x, y, 2, 2, kind)

# ---- art : cristaux (prismes de grenat -> domes d'opale), pierre du degrade
LG = E.load('general', 'petalburg')
def grass_cols(st):
    L = (LG[0], LG[1], [stage_pal(i, TS_[st]) for i in range(6)] + LG[2][6:], LG[3], LG[4])
    cnt = collections.Counter(E.metatile(L, GRASS_M).convert('RGB').getdata()); cols = [c for c, _ in cnt.most_common(4)]
    while len(cols) < 4: cols.append(cols[-1])
    return cols
GARNET = [(14, 18, 40), (40, 50, 86), (104, 118, 160), (186, 198, 230), (244, 248, 255), (255, 150, 176), (150, 236, 255), (104, 150, 255)]      # opale (depart)
OPAL = [(8, 40, 28), (24, 104, 72), (60, 176, 112), (150, 236, 172), (240, 255, 244), (255, 112, 168), (120, 255, 190), (255, 160, 208)]                # braise / obsidienne (arrivee)
def art_pal(st):
    g = grass_cols(st); t = TS_[st]
    cols = [lerp(GARNET[i], OPAL[i], t) for i in range(8)]
    sh = tuple(int(c * 0.55) for c in min(g, key=sum))
    return [(0, 0, 0)] + g + cols + [sh, lerp((74, 84, 116), (86, 70, 72), t), lerp((138, 150, 184), (146, 120, 116), t)], g
for st in (0, 1, 2):
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
# ---- enregistrement de l'art (3 etages : poussiere lunaire / melange / tourmaline)
def art_st(x, y): return stage_at(x, y)
def crop4(b, st): return {(i, j): meta(b.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), st) for j in range(2) for i in range(2)}
for st in (0, 1, 2):
    ART[('sm0', st)] = meta(small(st, 0), st); ART[('sm1', st)] = meta(small(st, 1), st)
    ART[('sign', st)] = meta(sign_art(st), st)
    ART[('boulder', st)] = crop4(boulder_img(st), st)
    ART[('spire', st)] = crop4(spire_img(st), st)
for st in (0, 1):
    ART[('crater', st)] = crop4(crater_small(st), st); ART[('pit', st)] = meta(pit_img(st), st)
for st in (1, 2):
    ART[('stump', st)] = meta(stump_img(st), st)
_bst = stage_at(BIG[0] + 1, BIG[1] + 1)
_bi = big(_bst)
ART[('big', _bst)] = {(i, j): meta(_bi.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)), _bst) for j in range(3) for i in range(3)}
ART_PLACE = {}
def near(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if (x + i, y + j) in OCC or (x + i, y + j) in ART_PLACE: return True
    return False
for c in SIGNS.values(): ART_PLACE[c] = ART[('sign', art_st(*c))]
for (i, j), k in ART[('big', _bst)].items(): ART_PLACE[(BIG[0] + i, BIG[1] + j)] = k
for (x, y, kind) in DEAD:
    st = art_st(x, y)
    if kind == 'crater' and st > 1: kind = 'boulder'
    for (i, j), k in ART[(kind, st)].items(): ART_PLACE[(x + i, y + j)] = k

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
RAMP = [lerp((12, 16, 30), (158, 166, 182), (k / 14.0) ** 1.1) for k in range(15)]
PALS[12] = [(0, 0, 0)] + RAMP
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
# ---- cases isolees : plus de sol nu ; cristaux, cailloux, fleurs
for y in range(2, H - 2):
    for x in range(2, W - 2):
        c = (x, y)
        if c in OCC or c in PATH_D1 or c in RES or c in ART_PLACE or (G[c] & 0xc00) or c in RIDGE: continue
        inside = c in OPEN
        st = art_st(x, y)
        p = (0.05 + 0.12 * x / W) if inside else 0.45
        if rnd.random() < p:
            if st == 0: nm = rnd.choice(['pit', 'sm0', 'sm1', 'pit', 'sm0'])
            elif st == 1: nm = rnd.choice(['pit', 'sm0', 'sm1', 'stump', 'sm1'])
            else: nm = rnd.choice(['sm0', 'sm1', 'sm1', 'stump', 'sm0', 'sm1'])
            claim(x, y, 1, 1, 'rocaille'); ART_PLACE[c] = ART[(nm, st)]
        elif st >= 1 and inside and rnd.random() < 0.18:
            put(x, y, 0x3000, FLOWER_M, st=st)
# ---- accessibilite
ART_RAW_BLOCK = set(ART_PLACE)
def blocked(c):
    return c in ART_RAW_BLOCK or c in RIDGE or bool(G[c] & 0xc00)
def flood(s0, extra=()):
    seen_ = {s0}; q_ = collections.deque([s0])
    while q_:
        c = q_.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n_ = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n_[0] < W and 0 <= n_[1] < H and n_ not in seen_ and n_ not in extra and not blocked(n_): seen_.add(n_); q_.append(n_)
    return seen_
START = (0, 15); EXIT = (W - 1, 15)
seen = flood(START)
for y in range(EXIT_ROWS[0], EXIT_ROWS[1] + 1):
    for x_ in (0, W - 1): assert (x_, y) in seen, ('sortie inaccessible', x_, y)
for (x0, y0, x1, y1) in TALL: assert (x0, y0) in seen, ('herbe inaccessible', x0, y0)
for c in SIGNS.values(): assert any((c[0] + dx, c[1] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), ('panneau inaccessible', c)
_cut = sorted(c for c in OPEN if not blocked(c) and c not in seen)
print('cases d ouverture coupees du chemin :', len(_cut), _cut[:12])
for c in _cut:                                       # case libre isolee : on la comble (relief) plutot que de la laisser inatteignable
    nm = 'sm0' if art_st(*c) < 2 else 'sm1'; ART_PLACE[c] = ART[(nm, art_st(*c))]


for (x, y) in sorted(RIDGE):
    put_lay(x, y, 0x400, MT_T[mtn_id(x, y)], 12)

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
for (x, y), v in {(W - 2, 0): G[(W - 4, 0)], (W - 1, 0): G[(W - 3, 0)], (W - 2, 1): G[(W - 4, 1)], (W - 1, 1): G[(W - 3, 1)], (W - 2, H - 2): G[(W - 4, H - 2)], (W - 1, H - 2): G[(W - 3, H - 2)], (W - 2, H - 1): G[(W - 4, H - 1)], (W - 1, H - 1): G[(W - 3, H - 1)]}.items(): G[(x, y)] = v

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
    if 'GeneralMoonwood' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralMoonwood[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralMoonwood[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_MoonwoodRoad[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_MoonwoodRoad[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralMoonwood[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralMoonwood[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_MoonwoodRoad[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_MoonwoodRoad[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralMoonwood =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralMoonwood,
    .palettes = gTilesetPalettes_GeneralMoonwood,
    .metatiles = gMetatiles_GeneralMoonwood,
    .metatileAttributes = gMetatileAttributes_GeneralMoonwood,
    .callback = NULL,
};

const struct Tileset gTileset_MoonwoodRoad =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MoonwoodRoad,
    .palettes = gTilesetPalettes_MoonwoodRoad,
    .metatiles = gMetatiles_MoonwoodRoad,
    .metatileAttributes = gMetatileAttributes_MoonwoodRoad,
    .callback = NULL,
};
''')
g = [G[(x, y)] for y in range(H) for x in range(W)]
os.makedirs('data/layouts/Route4East', exist_ok=True)
open('data/layouts/Route4East/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/Route4East/border.bin', 'wb').write(struct.pack('<4H', *[0x400 | variant(m, 1) for m in (468, 469, 476, 477)]))
L = json.load(open('data/layouts/layouts.json'))
if not any(l.get('id') == 'LAYOUT_ROUTE4_EAST' for l in L['layouts']):
    L['layouts'].append({"id": "LAYOUT_ROUTE4_EAST", "name": "Route4East_Layout", "width": W, "height": H, "border_width": 2, "border_height": 2,
                         "primary_tileset": "gTileset_GeneralMoonwood", "secondary_tileset": "gTileset_MoonwoodRoad",
                         "border_filepath": "data/layouts/Route4East/border.bin", "blockdata_filepath": "data/layouts/Route4East/map.bin"})
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_ROUTE4_EAST': l.update(width=W, height=H, primary_tileset='gTileset_GeneralMoonwood', secondary_tileset='gTileset_MoonwoodRoad')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'w': W, 'h': H, 'signs': SIGNS, 'exit_rows': EXIT_ROWS, 'tall': TALL, 'big': BIG}, open('/tmp/route4e_info.json', 'w'))
blk = sorted([x, y] for (x, y) in ((x, y) for y in range(H) for x in range(W)) if blocked((x, y)))
json.dump({'w': W, 'h': H, 'blocked': blk}, open('/tmp/route4e_col.json', 'w'))
print('route 4 est : metatuiles', len(SEC_ENT), 'tuiles art', len(ART_T))
