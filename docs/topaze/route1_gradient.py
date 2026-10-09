# ROUTE 1 « la route du dégradé » : relie Grenalux (grenat) à Opanihrum (opale noire) ; les couleurs glissent du grenat à l'opale
# du sud au nord. Carte entièrement nouvelle (26x54), chemin sinueux, herbes hautes, cristaux dont la nature change (prismes de
# grenat -> dômes d'opale), pierre du dégradé.
# Technique : 3 « étages » de palettes (t=0 grenat, 0.5 mélange, 1 opale). Les métatuiles d'Emeraude utilisées (herbe, arbres, sable...)
# sont recopiées dans le tileset secondaire avec des numéros de palette différents (variantes) ; l'étage de chaque case suit un champ
# lisse + le gradient sud->nord, ce qui donne un fondu progressif.
# Emplacements de palettes : étage0 = primaire 0,2,5 (+ art 6) ; étage1 = primaire 1,3,4 (+ art 10) ; étage2 = secondaire 7,8,9 (+ art 11) ; 12 = panneau.
# Lancer depuis la racine : python3 docs/topaze/route1_gradient.py  puis  route1_events.py
import struct, json, random, sys, colorsys, collections, os, re, math, shutil
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
EM = '../pokeemerald/data/'
PRI = 'data/tilesets/primary/general_gradient/'; SEC = 'data/tilesets/secondary/gradient_road/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
# ------------------------------------------------------------------ teintes : GRENAT (Grenalux) et OPALE NOIRE (Opanihrum)
def tint_garnet(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.08: return r, g, b
    if 60 <= h <= 180: h = 352 + (h - 120) * 0.12; s = min(1, s * 0.9); l = l * 0.8
    elif 25 <= h < 60: h = 14 + (h - 40) * 0.2; s *= 0.75
    elif 180 < h <= 260: h = 262 + (h - 215) * 0.2; s *= 0.4; l = l * 0.5
    else: h = 350; s = min(1, s * 1.05); l = l * 0.78
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_opal(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.10 and l > 0.93: return r, g, b
    if s > 0.45 and (h >= 180 or h < 25): return r, g, b
    if 78 <= h <= 175: h = 168 + (h - 120) * 0.12; s = min(1, s * 0.5); l = l * 0.8
    else: h = 232; s = min(0.42, s * 0.55 + 0.10); l = min(1, l * 0.72)
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t + .5) for i in range(3))
def hlerp(a, b, t):
    """melange en teinte (HLS), toujours par le violet : grenat (350) -> violet -> opale (170..230), au lieu d'un gris boueux en RVB."""
    ha, la, sa = colorsys.rgb_to_hls(*[c / 255 for c in a]); hb, lb, sb = colorsys.rgb_to_hls(*[c / 255 for c in b])
    if sa < 0.06 or sb < 0.06: return lerp(a, b, t)
    dh = hb - ha
    if dh > 0: dh -= 1
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
    out = [c if k == 0 else hlerp(tint_garnet(*c), tint_opal(*c), t) for k, c in enumerate(ORIG[i])]
    if i == 5: out = [out[0]] + [desat(c, 1 - 0.65 * t) for c in out[1:]]       # sable : la route reste pale vers le nord (comme l'avenue d'Opanihrum)
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
W, H = 26, 54
GRASS_M, FLOWER_M, TALL_M = 1, 4, 13
TREE = [[468, 469], [476, 477]]
G = {}; OCC = {}; STG = {}
rnd = random.Random(1010)
def stage_at(x, y):
    t = (H - 1 - y) / (H - 1)
    n = 0.35 * math.sin(x * 0.55 + y * 0.21) + 0.25 * math.sin(y * 0.37 - x * 0.3) + 0.2 * math.sin(x * 0.23 + y * 0.6)
    j = ((x * 73856093) ^ (y * 19349663)) % 1000 / 1000.0 - 0.5               # grain : fondu irregulier aux frontieres
    return max(0, min(2, int(round(2 * t + n * 0.45 + j * 0.5))))
def stage_smooth(x, y):
    t = (H - 1 - y) / (H - 1)
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
def tree(x, y):
    st = stage_at(x, y)
    for j in range(2):
        for i in range(2): put(x + i, y + j, 0x400, TREE[j][i], st=st)
# ---- portes : sud (Grenalux) x=12..13 ; nord (Opanihrum) x=14..17
S_GATE, N_GATE = (12, 13), (14, 15, 16, 17)
for x in range(0, W, 2):
    if x != 12: tree(x, H - 2)
    if x != 14 and x != 16: tree(x, 0)
for y in range(2, H - 2, 2):
    tree(0, y); tree(W - 2, y)
# ---- chemin : meandre continu (2 cases de large au minimum), rejoint les portes sud (x 12..13) et nord (x 14..17)
PATH = set()
def xc(y):
    d = H - 1 - y
    w = min(1.0, min(d, y) / 9.0)                                  # pres des portes le chemin va droit
    base = 13 + 5.5 * math.sin(d / 6.5) + 1.8 * math.sin(d / 3.4 + 0.8)
    return int(round(13 * (1 - w) + base * w)) if d > y else int(round(14 * (1 - w) + base * w))
X = {y: max(4, min(W - 6, xc(y))) for y in range(H)}
for y in range(H):
    a = X[y]; b = X[min(H - 1, y + 1)]
    for x in range(min(a, b), max(a, b) + 2): PATH.add((x, y))
PATH |= {(12, H - 1), (13, H - 1), (12, H - 2), (13, H - 2), (14, 0), (15, 0), (16, 0), (17, 0), (14, 1), (15, 1), (16, 1), (17, 1)}
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
# ---- herbes hautes (rencontres)
PATH_M = {(x + i, y + j) for (x, y) in PATH for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2)}
STONE = next((x, y) for y in range(4, 16) for x in range(W - 7, 3, -1) if all((x + i, y + j) not in PATH_M for i in range(3) for j in range(3)))
for j in range(3):
    for i in range(3): OCC[(STONE[0] + i, STONE[1] + j)] = 'reserve'
# ---- falaises / crêtes de roche : amas irreguliers (marche aleatoire allongee) separes du chemin d'une case d'herbe
def dil(cells, r):
    return {(x + i, y + j) for (x, y) in cells for i in range(-r, r + 1) for j in range(-r, r + 1)}
CLEAR = dil(PATH, 1)
SIGN = (11, 51); NPC = {'clerk': (14, 50), 'boy': (max(x for (x, y) in PATH if y == 29) + 3, 29)}
RES = dil([SIGN] + list(NPC.values()), 1)
RIDGE = set()
def ridge_ok(c):
    x, y = c
    return 2 <= x <= W - 3 and 3 <= y <= H - 5 and c not in OCC and c not in CLEAR and c not in RES and c not in RIDGE
def grow(seed, n):
    """amas compact : on prefere les cases voisines de plusieurs cases deja prises (bords arrondis, quelques bosses)."""
    cells = {seed}
    while len(cells) < n:
        cand = {}
        for (x, y) in cells:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (x + dx, y + dy)
                if nb in cells or not ridge_ok(nb): continue
                k = sum(((nb[0] + a, nb[1] + b) in cells) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                cand[nb] = 0.6 + 1.6 * (k - 1) + (0.5 if dy == 0 else 0)          # un peu plus large que haut
        if not cand: break
        cs = sorted(cand); w = [max(0.05, cand[c]) for c in cs]
        cells.add(rnd.choices(cs, w)[0])
    return cells
BLOB = {}; made = 0; tries = 0
while made < 11 and tries < 800:
    tries += 1
    side = rnd.random()
    sx = rnd.randint(3, 6) if side < 0.35 else (rnd.randint(W - 7, W - 4) if side < 0.7 else rnd.randint(3, W - 4))     # beaucoup d'amas s'adossent aux bords (falaises naturelles)
    seed = (sx, 6 + made * 4 + rnd.randint(-1, 1))
    if not ridge_ok(seed): continue
    cells = grow(seed, rnd.randint(14, 34))
    if len(cells) < 10: continue
    cy = sum(c[1] for c in cells) / len(cells); cx = sum(c[0] for c in cells) / len(cells)
    for c in cells: RIDGE.add(c); OCC[c] = 'roche'; BLOB[c] = (cx, cy)
    made += 1
print('amas de roche', made, 'cases', len(RIDGE))
LEDGES = []
# ---- herbes hautes (rencontres) : rectangles libres pres du chemin
TALL = []
tries = 0
while len(TALL) < 10 and tries < 3000:
    tries += 1; x0 = rnd.randint(2, W - 8); y0 = rnd.randint(3, H - 8); w = rnd.randint(3, 5); h = rnd.randint(3, 4)
    cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    if x0 + w > W - 3 or y0 + h > H - 4 or any(c in OCC for c in cells): continue
    if not any((x + dx, y + dy) in PATH for (x, y) in cells for dx in (-3, 3) for dy in (-3, 3)): continue
    if any((x, y) in OCC for (x, y) in [(x0 - 1, y0 + k) for k in range(h)] + [(x0 + w, y0 + k) for k in range(h)]) and False: continue
    TALL.append((x0, y0, x0 + w - 1, y0 + h - 1))
    for c in cells: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M)
# ---- art : cristaux (prismes de grenat -> domes d'opale), pierre du degrade
LG = E.load('general', 'petalburg')
def grass_cols(st):
    L = (LG[0], LG[1], [stage_pal(i, TS_[st]) for i in range(6)] + LG[2][6:], LG[3], LG[4])
    cnt = collections.Counter(E.metatile(L, GRASS_M).convert('RGB').getdata()); cols = [c for c, _ in cnt.most_common(4)]
    while len(cols) < 4: cols.append(cols[-1])
    return cols
GARNET = [(48, 6, 26), (112, 14, 44), (176, 28, 62), (226, 70, 96), (255, 176, 196), (255, 255, 255), (255, 120, 150), (255, 220, 230)]
OPAL = [(8, 10, 24), (22, 26, 52), (46, 54, 98), (92, 106, 168), (236, 242, 255), (255, 104, 186), (70, 240, 218), (186, 116, 255)]
def art_pal(st):
    g = grass_cols(st); t = TS_[st]
    cols = [hlerp(GARNET[i], OPAL[i], t) for i in range(8)]
    sh = tuple(int(c * 0.55) for c in min(g, key=sum))
    return [(0, 0, 0)] + g + cols + [sh, hlerp((112, 84, 92), (74, 82, 104), t), hlerp((166, 134, 132), (130, 142, 170), t)], g
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
    """etage 0 : prisme de grenat ; etage 2 : dome d'opale ; etage 1 : prisme a reflets (transition)."""
    if st == 2: dome(d, cx, base, rx, h)
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
    bx, by = BLOB[(x, y)]; ART_PLACE[(x, y)] = ROCK[(m, stage_smooth(bx, by), (x * 3 + y * 5) % 4 if m == 15 else (x + y) % 2)]                                  # la pierre du degrade, a l'est du chemin
# ---- panneau, PNJ
claim(*SIGN, 1, 1, 'panneau'); ART_PLACE[SIGN] = ART[('sign', 0)]
for c in NPC.values(): assert c not in OCC, ('PNJ sur un decor', c)
# ---- bosquets d'arbres (hors chemin, hors herbes, hors cases reservees ; marge de 1 case)
def near(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if (x + i, y + j) in OCC or (x + i, y + j) in ART_PLACE: return True
    return False
for c in NPC.values(): OCC[c] = 'pnj'
def free_tree(x, y): return 2 <= x <= W - 4 and 2 <= y <= H - 4 and all((x + i, y + j) not in OCC and not near(x + i, y + j, 1) for i in range(2) for j in range(2))
def grove(cx, cy, n, spread):
    k = tries = 0
    while k < n and tries < 800:
        tries += 1; x = int(rnd.gauss(cx, spread)); y = int(rnd.gauss(cy, spread))
        if free_tree(x, y): tree(x, y); claim(x, y, 2, 2, 'arbre'); k += 1
for (cx, cy, n, s) in ((4, 50, 5, 2.2), (20, 48, 5, 2.4), (22, 40, 4, 2), (3, 40, 3, 1.5), (10, 38, 4, 2.2), (22, 29, 4, 2), (3, 25, 5, 2), (13, 26, 3, 1.4),
                       (5, 18, 4, 2), (22, 18, 3, 1.5), (3, 6, 5, 2), (6, 12, 2, 1.5), (20, 6, 4, 2), (12, 3, 3, 1.5), (24, 24, 2, 1.5), (12, 14, 2, 1.5)):
    grove(cx, cy, n, s)
# ---- cristaux epars (de plus en plus d'opale vers le nord), fleurs
placed = tries = 0
while placed < 26 and tries < 4000:
    tries += 1; x, y = rnd.randint(2, W - 3), rnd.randint(2, H - 4)
    if (x, y) not in OCC and (x, y) not in ART_PLACE and not near(x, y, 1) and G[(x, y)] & 0x3ff in [variant(GRASS_M, s) for s in range(3)]:
        art1(x, y, rnd.choice(('sm0', 'sm1'))); placed += 1
for _ in range(34):
    cx, cy = rnd.randint(2, W - 3), rnd.randint(2, H - 4)
    for _ in range(rnd.randint(3, 7)):
        x, y = cx + rnd.randint(-2, 2), cy + rnd.randint(-1, 1)
        if 1 <= x < W - 1 and 1 <= y < H - 2 and (x, y) not in OCC and (x, y) not in ART_PLACE and G[(x, y)] & 0x3ff in [variant(GRASS_M, s) for s in range(3)]:
            put(x, y, 0x3000, FLOWER_M)
for c in NPC.values(): del OCC[c]
# ---- accessibilite
ART_RAW_BLOCK = set(ART_PLACE)
def blocked(c):
    return c in ART_RAW_BLOCK or bool(G[c] & 0xc00)
seen = {(12, H - 1)}; q = collections.deque([(12, H - 1)])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n): seen.add(n); q.append(n)
for c in [(x, 0) for x in N_GATE] + [(x, H - 1) for x in S_GATE] + list(NPC.values()) + [(SIGN[0] + 1, SIGN[1])]: assert c in seen, ('inaccessible', c)
for (x0, y0, x1, y1) in TALL: assert (x0, y0) in seen or (x1, y1) in seen, ('herbe inaccessible', x0, y0)
# ------------------------------------------------------------------ ecriture
for _m in (468, 469, 476, 477): variant(_m, 1)      # bord de carte : arbres du mélange (violet), neutre entre les deux villes
for k, ents in enumerate(ART_E): pass
NT = 0
ART_ID = {}
for k, ents in enumerate(ART_E):
    SEC_ENT.append([(640 + t) | (slot << 12) for (_, t, slot) in ents] + [0, 0, 0, 0]); SEC_ATT.append(0)
    ART_ID[k] = 640 + len(SEC_ENT) - 1
assert len(SEC_ENT) <= 384 and len(ART_T) <= 384, (len(SEC_ENT), len(ART_T))
for c, k in ART_PLACE.items(): G[c] = 0x400 | ART_ID[k]
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
    if 'GeneralGradient' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralGradient[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralGradient[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_GradientRoad[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GradientRoad[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralGradient[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralGradient[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_GradientRoad[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GradientRoad[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralGradient =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralGradient,
    .palettes = gTilesetPalettes_GeneralGradient,
    .metatiles = gMetatiles_GeneralGradient,
    .metatileAttributes = gMetatileAttributes_GeneralGradient,
    .callback = NULL,
};

const struct Tileset gTileset_GradientRoad =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GradientRoad,
    .palettes = gTilesetPalettes_GradientRoad,
    .metatiles = gMetatiles_GradientRoad,
    .metatileAttributes = gMetatileAttributes_GradientRoad,
    .callback = NULL,
};
''')
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/Route1/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/Route1/border.bin', 'wb').write(struct.pack('<4H', *[0x400 | variant(m, 1) for m in (468, 469, 476, 477)]))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_ROUTE1': l.update(width=W, height=H, primary_tileset='gTileset_GeneralGradient', secondary_tileset='gTileset_GradientRoad')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'sign': SIGN, 'npc': NPC, 'w': W, 'h': H, 'tall': TALL, 'ledges': LEDGES, 'path': sorted(PATH)}, open('/tmp/route1_info.json', 'w'))
blk = sorted([x, y] for (x, y) in ((x, y) for y in range(H) for x in range(W)) if blocked((x, y)))
json.dump({'w': W, 'h': H, 'blocked': blk}, open('/tmp/route1_col.json', 'w'))
print('route 1 : metatuiles', len(SEC_ENT), 'tuiles art', len(ART_T))
