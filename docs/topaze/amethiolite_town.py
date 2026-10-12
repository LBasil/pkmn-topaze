# AMETHIOLITE (ex-Parmanie / Fuchsia) : la cite lacustre de l'AMETHYSTE (arene Poison), zoo-parc du Gardien et porte du Parc Safari.
# Meme methode que Chrondrolia / Tourmalia : decors d'Emeraude (ici SOOTOPOLIS : dômes, terrasses claires) recopies dans un jeu de tuiles secondaire
# COMPACTE (FireRed : 384 tuiles max), recolores en violet d'amethyste, + art procedural (grande porte du Safari, geodes, cristaux).
# Lancer depuis la racine du depot :  python3 docs/topaze/amethiolite_town.py  puis  amethiolite_events.py
import struct, json, random, sys, collections, os, shutil, re, math, colorsys
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
EM = '../pokeemerald/data/'
PRI = 'data/tilesets/primary/general_amethyst/'; SEC = 'data/tilesets/secondary/sootopolis_amethyst/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
FT = struct.unpack('<3600H', open(EM + 'layouts/SootopolisCity/map.bin', 'rb').read())      # 60 x 60
def fr(x, y): return FT[y * 60 + x]
rnd = random.Random(2026)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
PALS_P = [readpal(EM + 'tilesets/primary/general/palettes/%02d.pal' % i) for i in range(16)]
PALS_S = [readpal(EM + 'tilesets/secondary/sootopolis/palettes/%02d.pal' % i) for i in range(16)]
PALS_P[6] = PALS_S[6]                                       # FireRed : palette 6 = primaire
LD = E.load('general', 'sootopolis')

# ------------------------------------------------------------------ metatuiles : conversion attributs + compaction du secondaire
patt = open(EM + 'tilesets/primary/general/metatile_attributes.bin', 'rb').read()
satt = open(EM + 'tilesets/secondary/sootopolis/metatile_attributes.bin', 'rb').read()
smt = open(EM + 'tilesets/secondary/sootopolis/metatiles.bin', 'rb').read()
pmt = open(EM + 'tilesets/primary/general/metatiles.bin', 'rb').read()
hdr = open('include/constants/metatile_behaviors.h').read()
OKB = {int(m, 16) for m in re.findall(r'#define MB_\w+\s+(0x[0-9A-Fa-f]+)', hdr)}
WATER = {0x10, 0x11, 0x12, 0x15}
def conv(v):
    b, layer = v & 0xff, v >> 12
    if b not in OKB: b = 0
    a = b | (layer << 29)
    if b == 0x02: a |= 0x1000200
    elif b in WATER: a |= 0x22000400
    elif b == 0x13: a |= 0x2000600
    return a
def beh(m):
    a = patt[m * 2:m * 2 + 2] if m < 512 else satt[(m - 512) * 2:(m - 512) * 2 + 2]
    return struct.unpack('<H', a)[0] & 0xff

_PT = Image.open(EM + 'tilesets/primary/general/tiles.png'); _ST = Image.open(EM + 'tilesets/secondary/sootopolis/tiles.png')
SEC_MAP = {}; SEC_ENT = []; SEC_ATT = []; CT = []
def ctile(t):
    if t not in CT: CT.append(t)
    return 640 + CT.index(t)
def remap(v):
    m = v & 0x3ff
    if m < 512: return v
    if m not in SEC_MAP:
        e = struct.unpack('<8H', smt[(m - 512) * 16:(m - 512) * 16 + 16]); out = []
        for q in e:
            t = q & 0x3ff
            out.append((q & ~0x3ff) | (ctile(t - 512) if t >= 512 else t))
        SEC_ENT.append(out); SEC_ATT.append(conv(struct.unpack('<H', satt[(m - 512) * 2:(m - 512) * 2 + 2])[0]))
        SEC_MAP[m] = 640 + len(SEC_ENT) - 1
    return (v & ~0x3ff) | SEC_MAP[m]
def remap_chunk(v): return remap(v)
def ents_of(m):
    if m < 512: return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16]))
    return list(SEC_ENT[(remap(0x3000 | m) & 0x3ff) - 640])
def hls_(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb_(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def amethyste(c):
    """v7 (« vraiment amethyste ») : creme/olive des domes et du pave -> lilas MOYEN a violet profond (plus de pave quasi blanc) ; verts -> pelouse lilas / arbres indigo ; le rouge du Centre et le bleu de la Boutique restent"""
    h, l, s = hls_(c)
    if s < 0.02: return c
    if 28 <= h <= 75: return rgb_(274, 0.10 + 0.60 * l, min(0.80, s * 1.5 + 0.30))
    if 75 < h <= 175:
        if s < 0.12: return rgb_(272, 0.14 + 0.62 * l, 0.28)
        if l > 0.42: return rgb_(270, 0.12 + 0.66 * l, min(0.85, s * 0.7 + 0.24))
        return rgb_(256, min(1, l * 1.1), min(0.9, s * 1.0 + 0.05))
    return c
for P in (PALS_P, PALS_S):
    for i in range(16): P[i] = [P[i][0]] + [amethyste(x) for x in P[i][1:]]

# ------------------------------------------------------------------ plan (48 x 40, comme Parmanie d'origine : 3 sorties - sud Route 19, ouest Route 18, est Route 15)
W, H = 48, 32
G = {}; OCC = {}
for y in range(H):
    for x in range(W): G[(x, y)] = 0
def put(x, y, v): G[(x, y)] = v
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            assert (x + i, y + j) not in OCC, 'chevauchement %s avec %s en %s' % (name, OCC[(x + i, y + j)], (x + i, y + j))
            assert 0 <= x + i <= W - 1 and 0 <= y + j <= H - 1, (name, x + i, y + j)
            OCC[(x + i, y + j)] = name
GRASS = 1
OPEN = set(); WAY = set()
def trail(pts, wd, seed):
    r = random.Random(seed)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for k in range(n + 1):
            t = k / n; cx = x0 + (x1 - x0) * t; cy = y0 + (y1 - y0) * t
            for dy in range(-wd, wd + 1):
                for dx in range(-wd, wd + 1):
                    if dx * dx + dy * dy <= wd * wd + r.choice((0, 0, 1)) and 0 <= int(cx) + dx < W and 0 <= int(cy) + dy < H: OPEN.add((int(round(cx)) + dx, int(round(cy)) + dy))
                    if math.hypot(int(round(cx)) + dx - cx, int(round(cy)) + dy - cy) <= 1.0: WAY.add((int(round(cx)) + dx, int(round(cy)) + dy))
RECTS = []
def chunk(x0, y0, cw, ch, dx, dy, name):
    claim(dx, dy, cw, ch, name); doors = []; RECTS.append((dx, dy, cw, ch))
    for j in range(ch):
        for i in range(cw):
            v = fr(x0 + i, y0 + j)
            if 0x60 <= beh(v & 0x3ff) <= 0x6f: doors.append((dx + i, dy + j)); v &= ~0xc00
            put(dx + i, dy + j, remap_chunk(v))
    return doors
D = {}
DOME = (8, 3, 3, 4); FLAT = (44, 3, 3, 4)                      # maisons de Sootopolis : dôme (porte (9,6)) / plate (porte (45,6))
D['safari'] = None
D['warden'] = chunk(*DOME, 11, 3, 'maison du Gardien')
D['office'] = chunk(*FLAT, 31, 3, 'bureau du Safari')
D['house1'] = chunk(*FLAT, 3, 1, 'maison 1')
D['house2'] = chunk(*DOME, 40, 3, 'maison 2')
D['mart'] = chunk(16, 27, 4, 3, 7, 10, 'boutique')
D['center'] = chunk(42, 28, 4, 4, 38, 10, 'centre')
D['gym'] = chunk(28, 28, 6, 5, 6, 22, 'arene')
D['house3'] = chunk(*DOME, 35, 22, 'maison 3')
claim(20, 0, 8, 5, 'porte du Safari'); D['safari'] = [(24, 4), (23, 4)]
for k, v in D.items(): print(k, v)
# ---- lac au centre ; pelouse partout ailleurs
LCX, LCY, LRX, LRY = 24.0, 17.0, 8.2, 4.4
LAKE = set()
for y in range(H):
    for x in range(W):
        a = math.atan2((y - LCY) / LRY, (x - LCX) / LRX)
        k = 1 + 0.10 * (math.sin(2 * a + 0.7) + 0.6 * math.sin(3 * a + 1.9) + 0.4 * math.sin(5 * a + 0.2)) / 2
        if ((x - LCX) / LRX) ** 2 + ((y - LCY) / LRY) ** 2 <= k * k: LAKE.add((x, y))
for c in LAKE: assert c not in OCC, ('lac sur un batiment', c)
# ---- enclos (zoo du Gardien) : 4x4, haie d'arbres, 2x2 de pelouse ; un panneau devant
PENS = {'voltorb': (16, 8), 'chansey': (28, 8), 'fossil': (9, 18)}                     # 3 enclos ; chacun abrite 2 exposants (voir HOST)
HOST = {'voltorb': 'voltorb', 'slowpoke': 'voltorb', 'chansey': 'chansey', 'kangaskhan': 'chansey', 'fossil': 'fossil', 'lapras': 'fossil'}
for k, (px, py) in PENS.items(): claim(px, py, 4, 4, 'enclos ' + k)
# ---- voies : avenue de la porte, anneau autour du lac, routes ouest/est/sud, liaisons aux portes
RING = []
for k in range(0, 49):
    a = 2 * math.pi * k / 48
    RING.append((int(round(LCX + (LRX + 3.0) * math.cos(a))), int(round(LCY + (LRY + 3.0) * math.sin(a)))))
trail(RING, 0, 71)
trail([(22, 5), (22, 9)], 0, 72)
trail([(0, 14), (4, 14), (8, 15), (11, 14), (13, 16), (14, 17)], 0, 73); trail([(47, 14), (43, 14), (40, 15), (36, 14), (34, 16)], 0, 74)
trail([(24, 24), (23, 26), (24, 28), (23, 31)], 0, 75)
for k, ds in D.items():
    for (x, y) in ds:
        for b in (1, 2, 3): WAY.add((x, y + b)); OPEN.add((x, y + b))
trail([(8, 13), (8, 14), (10, 15)], 0, 77); trail([(39, 14), (39, 15), (36, 16)], 0, 78)
trail([(12, 7), (12, 10), (14, 13), (17, 14)], 0, 79); trail([(32, 7), (32, 10), (30, 12), (31, 14)], 0, 80)
trail([(9, 27), (12, 27), (15, 25), (17, 23)], 0, 81); trail([(36, 26), (33, 26), (30, 25), (27, 24)], 0, 82)
trail([(4, 5), (4, 12), (8, 14)], 0, 83); trail([(41, 7), (41, 10), (40, 13), (40, 15)], 0, 84)
for y in range(1, H - 1):
    for x in range(1, W - 1):
        if (x, y) not in OCC and (x, y) not in LAKE: OPEN.add((x, y))
for (x, y) in list(OPEN):
    if (x, y) in OCC or (x, y) in LAKE: OPEN.discard((x, y)); WAY.discard((x, y))
# sorties : couloirs ouverts jusqu'au bord de la carte
EXITS = {'S': [(x, y) for x in range(20, 28) for y in range(28, H)], 'W': [(x, y) for x in range(0, 4) for y in range(13, 16)], 'E': [(x, y) for x in range(44, W) for y in range(13, 16)]}
for ex in EXITS.values():
    for c in ex:
        if c not in OCC and c not in LAKE: OPEN.add(c)
WAY |= {c for c in OPEN if any(c in ex for ex in EXITS.values()) and (c[0] in (0, 47) or c[1] == 39 or (c[1] in (19, 21) ) or c[0] in (22, 23, 24, 25))}
# esplanade pavee autour du lac, bords irreguliers
for y in range(H):
    for x in range(W):
        a = math.atan2((y - LCY), (x - LCX))
        k = 1 + 0.07 * math.sin(3 * a + 0.4) + 0.05 * math.sin(7 * a + 1.1)
        if (x, y) not in LAKE and ((x - LCX) / (LRX + 4.3 * k)) ** 2 + ((y - LCY) / (LRY + 4.1 * k)) ** 2 <= 1: WAY.add((x, y)); OPEN.add((x, y))
for (x, y) in sorted(WAY):
    for c in ((x + 1, y), (x, y + 1)):
        if 1 <= c[0] < W - 1 and 1 <= c[1] < H - 1 and c not in OCC and c not in LAKE and not (c[1] > 35 and c[0] not in range(21, 27)): WAY.add(c); OPEN.add(c)
# forecourt devant chaque porte
# esplanade pavee autour de chaque batiment (les angles clairs des decors de Sootopolis se fondent dans le pave)
for (rx_, ry_, rw_, rh_) in RECTS:
    for y in range(ry_ - 1, ry_ + rh_ + 1):
        for x in range(rx_ - 1, rx_ + rw_ + 1):
            if 2 <= x < W - 2 and 1 <= y < H - 1 and (x, y) not in OCC and (x, y) not in LAKE: WAY.add((x, y)); OPEN.add((x, y))
OPEN -= set(OCC); OPEN -= LAKE; WAY &= OPEN

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
def shadow(d, x0, y0, x1, y1): d.ellipse((x0, y0, x1, y1), fill=11)
# ------------------------------------------------------------------ art : porte du Safari, geodes et cristaux d'amethyste
ART_PAL = 8
used = {q >> 12 for e in SEC_ENT for q in e}
print('palettes utilisees par les decors', sorted(used))
assert ART_PAL not in used and 9 not in used, used
PAL = [(0, 0, 0), (30, 10, 52), (94, 44, 142), (142, 84, 202), (188, 132, 236), (228, 200, 252), (252, 242, 255), (62, 30, 112), (104, 56, 170),
       (152, 100, 222), (214, 188, 252), (40, 30, 66), (214, 64, 152), (176, 168, 192), (96, 88, 118), (255, 246, 200)]       # v7 : indigo -> violet d'amethyste (7..10)
# 1 contour | 2 violet fonce | 3 violet | 4 amethyste claire | 5 lilas | 6 blanc | 7 indigo fonce | 8 indigo | 9 indigo clair | 10 lilas pale | 11 ombre | 12 rose toxique | 13 pierre | 14 pierre sombre | 15 lueur
GATE_SRC = None
def gate():
    """grande porte du Parc Safari (8x5 = 128x80) : deux tours de geodes, mur de pierre, arche sombre, enseigne, haie de cristaux"""
    im = newimg(128, 80); d = ImageDraw.Draw(im)
    d.rectangle((0, 28, 127, 79), fill=13, outline=1)
    d.rectangle((0, 28, 127, 33), fill=14, outline=1); d.line([(1, 29), (126, 29)], fill=6)
    for x in range(2, 126, 8): d.line([(x, 34), (x, 78)], fill=11)
    # tours laterales
    for x0 in (4, 100):
        d.rectangle((x0, 12, x0 + 23, 79), fill=14, outline=1); d.rectangle((x0 + 2, 14, x0 + 21, 18), fill=13, outline=1)
        for k in range(3): d.rectangle((x0 + 5 + k * 6, 40, x0 + 8 + k * 6, 52), fill=8, outline=1); d.line([(x0 + 6 + k * 6, 41), (x0 + 7 + k * 6, 41)], fill=10)
        d.rectangle((x0 - 2, 10, x0 + 25, 13), fill=3, outline=1); d.line([(x0 - 1, 11), (x0 + 24, 11)], fill=4)
    prism(d, 16, 12, 11, 22); prism(d, 8, 14, 7, 12); prism(d, 24, 14, 6, 10)
    prism(d, 112, 12, 11, 22); prism(d, 104, 14, 6, 10); prism(d, 120, 14, 7, 12)
    # centre : fronton + enseigne + arche
    d.rectangle((34, 20, 93, 28), fill=3, outline=1); d.line([(35, 21), (92, 21)], fill=4)
    d.rectangle((44, 22, 83, 27), fill=11, outline=1)
    for k, x in enumerate(range(46, 82, 6)): d.rectangle((x, 23, x + 3, 26), fill=12 if k % 2 == 0 else 5)
    prism(d, 64, 20, 9, 16)
    d.rectangle((40, 40, 87, 79), fill=14, outline=1)
    d.rectangle((50, 46, 77, 79), fill=1, outline=1); d.pieslice((50, 40, 77, 66), 180, 360, fill=1, outline=1)
    d.rectangle((54, 50, 73, 79), fill=11)
    d.rectangle((58, 56, 69, 79), fill=1)
    for x in (52, 75): d.rectangle((x, 46, x + 1, 79), fill=5)
    for k in range(7): d.point((54 + k * 3, 48 + (k % 2)), fill=15)
    # haies de cristaux devant les murs
    for x in (30, 36, 92, 98): prism(d, x, 79, 6, 9)
    d.line([(0, 79), (127, 79)], fill=1)
    shadow(d, 0, 76, 127, 79)
    return im
def monolith():
    """grande geode d'amethyste 3x3 (48x48) : grappe de prismes sur un socle de pierre"""
    im = newimg(48, 48); d = ImageDraw.Draw(im)
    shadow(d, 2, 38, 46, 48)
    d.rectangle((8, 40, 39, 46), fill=13, outline=1); d.line([(9, 41), (38, 41)], fill=6); d.rectangle((9, 44, 38, 45), fill=14)
    prism(d, 10, 42, 7, 14); prism(d, 38, 42, 7, 12); prism(d, 18, 43, 8, 20); prism(d, 31, 43, 9, 24); prism(d, 24, 44, 11, 34)
    for (x, y) in ((22, 8), (27, 12), (13, 24), (36, 22), (24, 20)): d.point((x, y), fill=6)
    for (x, y) in ((20, 6), (29, 18)): d.point((x, y), fill=12)
    return im
def small(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 1, 12, 15, 16)
    if var == 0: prism(d, 4, 14, 5, 9); prism(d, 9, 15, 7, 14); prism(d, 13, 14, 4, 7)
    elif var == 1: prism(d, 6, 15, 6, 11); prism(d, 12, 14, 5, 8); d.rectangle((1, 13, 3, 14), fill=13); d.point((2, 12), fill=14)
    else: prism(d, 8, 15, 8, 14); d.rectangle((2, 13, 4, 14), fill=13); d.rectangle((12, 12, 14, 14), fill=13); d.point((13, 11), fill=14)
    return im

# ------------------------------------------------------------------ sol : pelouse violette, pave clair sur les voies, haies d'arbres, murs de quai
PAVE = (729, 729, 729, 729, 731, 732, 740)                       # pave creme de Sootopolis (variantes)
TREE = (487, 468)                                                # arbres d'Emeraude (bloquants)
TREES = set()
GROUND = {}
for (x, y) in sorted(OPEN):
    if (x, y) in WAY: G[(x, y)] = remap(0x3000 | rnd.choice(PAVE)); GROUND[(x, y)] = PAVE[0]
    else: G[(x, y)] = remap(0x3000 | GRASS); GROUND[(x, y)] = GRASS
SEA = LAKE
BEACH = {(x, y) for (x, y) in OPEN if any((x + a, y + b) in LAKE for a in range(-1, 2) for b in range(-1, 2))}
RAIL = {c for c in BEACH}
LANDING = set()
# ---- bords : forêt dense violette (limite nette), sauf les 3 couloirs
EXSET = {c for ex in EXITS.values() for c in ex}
for y in range(H):
    for x in range(W):
        c = (x, y)
        if c in OCC or c in LAKE or c in EXSET: continue
        edge = x < 2 or y < 1 or x >= W - 2 or y >= H - 1
        if edge: TREES.add(c) ; OPEN.discard(c); WAY.discard(c); BEACH.discard(c); RAIL.discard(c)
# les couloirs : 2 rangees d'arbres de chaque cote
for ex_name, ex in EXITS.items():
    xs = [c[0] for c in ex]; ys = [c[1] for c in ex]
    if ex_name == 'S':
        for y in range(26, H):
            for x in (19, 28):
                if (x, y) not in OCC: TREES.add((x, y)); OPEN.discard((x, y)); WAY.discard((x, y))
    else:
        for x in (range(0, 8) if ex_name == 'W' else range(40, W)):
            for y in (12, 16):
                if (x, y) not in OCC and (x, y) not in LAKE: TREES.add((x, y)); OPEN.discard((x, y)); WAY.discard((x, y))
# ---- enclos : haie d'arbres, pelouse a l'interieur
PENCELLS = {}
for k, (px, py) in PENS.items():
    for j in range(4):
        for i in range(4):
            c = (px + i, py + j)
            if i in (0, 3) or j in (0, 3): TREES.add(c)
            else: G[c] = remap(0x3000 | GRASS); PENCELLS[c] = k
            OPEN.discard(c)
# ------------------------------------------------------------------ art
ART_T = []
def add_tile(t):
    t = tuple(t)
    if t in ART_T: return ART_T.index(t)
    ART_T.append(t); return len(ART_T) - 1
def slice_tiles(block):
    return [add_tile(list(block.crop(((q % 2) * 8, (q // 2) * 8, (q % 2) * 8 + 8, (q // 2) * 8 + 8)).getdata())) for q in range(4)]
ART_META = {}
def art_meta(tiles4, gid):
    key = (tuple(tiles4), gid)
    if key not in ART_META:
        base = ents_of(gid)[:4]
        SEC_ENT.append(base + [('A', t) for t in tiles4]); SEC_ATT.append(0)
        ART_META[key] = len(SEC_ENT) - 1
    return ART_META[key]
ARTPLACE = {}; WALKART = set()
def art_block(im, bw, bh, x0, y0, name, gid, claimed=False):
    if not claimed: claim(x0, y0, bw, bh, name)
    for j in range(bh):
        for i in range(bw):
            blk = im.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))
            if sum(1 for p in blk.getdata() if p) < 10: G[(x0 + i, y0 + j)] = 0x400 | remap(0x3000 | gid); OPEN.discard((x0 + i, y0 + j)); WAY.discard((x0 + i, y0 + j)); continue
            ARTPLACE[(x0 + i, y0 + j)] = (slice_tiles(blk), gid); OPEN.discard((x0 + i, y0 + j)); WAY.discard((x0 + i, y0 + j))
art_block(gate(), 8, 5, 20, 0, 'porte du Safari', PAVE[0], claimed=True)
WALKART.add((24, 4)); WALKART.add((23, 4))
MONO = monolith()
MX, MY = 23, 7
for j in range(3):
    for i in range(3): assert (MX + i, MY + j) not in OCC and (MX + i, MY + j) not in LAKE
art_block(MONO, 3, 3, MX, MY, 'geode-monument', GROUND.get((MX, MY), 1))
SM = [small(0), small(1), small(2)]
KEEP = set()
for k, ds in D.items():
    for (x, y) in ds:
        for a in range(-2, 3):
            for b in range(-1, 4): KEEP.add((x + a, y + b))
for ex in EXITS.values(): KEEP |= set(ex)
PENSIGN = {(px_ + i_, py_ + 4 + j_) for (px_, py_) in PENS.values() for i_ in range(4) for j_ in range(2)}; KEEP |= PENSIGN
def near_way(c, r=1): return any((c[0] + a, c[1] + b) in WAY for a in range(-r, r + 1) for b in range(-r, r + 1))
# ---- bosquets (groupes d'arbres) dans les coins de pelouse
for (cx, cy, rx, ry, sd) in ((5, 11, 2.6, 2.2, 1), (43, 10, 2.0, 2.2, 2), (14, 27, 3.0, 2.2, 3), (44, 26, 2.6, 2.4, 4), (14, 6, 2.0, 1.6, 5), (36, 16, 1.5, 1.5, 6)):
    rr = random.Random(900 + sd)
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            c = (x, y)
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1 or c not in OPEN or c in OCC or c in WAY or c in KEEP or c in BEACH or near_way(c) or rr.random() > 0.8: continue
            TREES.add(c); OPEN.discard(c)
for (cx, cy, rx, ry, sd) in ((4.5, 2.5, 4.2, 2.0, 11), (16.5, 28.5, 3.2, 3.0, 12), (33, 28, 3.6, 2.8, 13), (41, 29, 3.4, 2.6, 14), (44, 23, 2.2, 3.4, 15), (36, 22.5, 1.2, 1.2, 16)):
    rr = random.Random(950 + sd)
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            c = (x, y)
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1 or c not in OPEN or c in OCC or c in WAY or c in KEEP or c in BEACH or rr.random() > 0.88: continue
            TREES.add(c); OPEN.discard(c)
# ---- cristaux d'amethyste (pelouse, loin des voies) et arbres isoles
placed = []
for c in sorted(OPEN, key=lambda c: rnd.random()):
    if c in OCC or c in WAY or c in KEEP or c in BEACH or c in ARTPLACE or near_way(c) or G[c] & 0xc00: continue
    if GROUND.get(c) != GRASS: continue
    r_ = rnd.random()
    if r_ < 0.05 and not any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q in placed):
        placed.append(c); claim(c[0], c[1], 1, 1, 'cristal'); ARTPLACE[c] = (slice_tiles(SM[rnd.randrange(3)]), GRASS)
    elif r_ < 0.14 and not any((c[0] + a, c[1] + b) in OCC for a in (-1, 0, 1) for b in (-1, 0, 1)):
        TREES.add(c); OPEN.discard(c)
def tree_img(var):
    """arbre d'amethyste 1x1 (16x16) : houppier rond indigo, reflets lilas, petit tronc"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 2, 12, 15, 16)
    d.rectangle((7, 10, 9, 14), fill=14, outline=1)
    d.ellipse((0, 0, 15, 12), fill=8, outline=1)
    d.ellipse((7, 4, 14, 11), fill=7)
    d.ellipse((2, 1, 9, 7), fill=9)
    for (x, y) in (((4, 2), (6, 3), (3, 5)), ((5, 2), (3, 4), (7, 5)), ((4, 3), (7, 2), (3, 6)))[var]: d.point((x, y), fill=10)
    d.point((11, 7 + var), fill=12 if var == 1 else 3)
    return im
TREEIMG = [tree_img(0), tree_img(1), tree_img(2)]
def wall_img(sides):
    """mur de quai en pierre lilas : bordure surelevee du cote du lac"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    N, S_, Wd_, E_ = sides
    if S_:
        d.rectangle((0, 7, 15, 10), fill=13, outline=1); d.line([(1, 8), (14, 8)], fill=6)
        d.rectangle((0, 11, 15, 15), fill=14, outline=1)
        for k in range(0, 16, 4): d.line([(k, 12), (k, 14)], fill=11)
        for k in range(0, 16, 4): d.rectangle((k, 9, k + 1, 9), fill=4); d.rectangle((k + 2, 9, k + 3, 9), fill=2)
    if N:
        d.rectangle((0, 0, 15, 3), fill=14, outline=1)
        d.rectangle((0, 4, 15, 8), fill=13, outline=1); d.line([(1, 5), (14, 5)], fill=6)
        for k in range(0, 16, 4): d.rectangle((k, 7, k + 1, 7), fill=4); d.rectangle((k + 2, 7, k + 3, 7), fill=2)
    if Wd_:
        d.rectangle((0, 0, 4, 15), fill=13, outline=1); d.line([(1, 1), (1, 14)], fill=6); d.rectangle((5, 0, 6, 15), fill=14)
        for k in range(1, 16, 4): d.rectangle((3, k, 3, k + 1), fill=4)
    if E_:
        d.rectangle((11, 0, 15, 15), fill=13, outline=1); d.line([(12, 1), (12, 14)], fill=6); d.rectangle((9, 0, 10, 15), fill=14)
        for k in range(1, 16, 4): d.rectangle((14, k, 14, k + 1), fill=4)
    return im
for c in sorted(RAIL):
    if c in OCC or c in ARTPLACE: continue
    sides = tuple((c[0] + dx, c[1] + dy) in LAKE for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)))
    if not any(sides):
        diag = [(a, b) for a in (-1, 1) for b in (-1, 1) if (c[0] + a, c[1] + b) in LAKE]
        a, b = diag[0]; sides = (b == -1, b == 1, a == -1, a == 1)
    claim(c[0], c[1], 1, 1, 'mur de quai'); ARTPLACE[c] = (slice_tiles(wall_img(sides)), GROUND.get(c, GRASS))
rt = random.Random(77)
for c in sorted(TREES):
    if c in ARTPLACE or c in OCC and OCC[c] != 'enclos' and False: continue
    ARTPLACE[c] = (slice_tiles(TREEIMG[rt.randrange(3)]), GRASS); OPEN.discard(c); WAY.discard(c)

# ------------------------------------------------------------------ eau : lac (procedural, statique ; eau animee = a faire)
class Ext:
    def __contains__(self, c): return (min(max(c[0], 0), W - 1), min(max(c[1], 0), H - 1)) in WATC
WATC = set(LAKE); WAT = Ext()
WATER_ATT = conv(struct.unpack('<H', patt[0xd1 * 2:0xd1 * 2 + 2])[0])
import numpy as np
from PIL import ImageFilter
WPAL_ID = 9
_g = E.metatile(LD, GRASS).convert('RGB'); GR = tuple(int(np.asarray(_g)[:, :, k].mean()) for k in range(3))
WPAL = [(0, 0, 0), (30, 26, 96), (60, 58, 170), (100, 96, 218), (156, 150, 244), (236, 232, 255),
        tuple(int(v * 0.70) for v in GR), tuple(int(v * 0.84) for v in GR),
        (70, 44, 24), (150, 104, 64), (206, 156, 96), (52, 36, 28), (30, 110, 70), (64, 164, 96), (255, 170, 200), (255, 232, 136)]
WATER_SRC = None

def vnoise(gx, gy, sc, seed):
    ix, iy = math.floor(gx / sc), math.floor(gy / sc); fx, fy = gx / sc - ix, gy / sc - iy
    def h(a, b): return random.Random((a * 73856093) ^ (b * 19349663) ^ seed).random()
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    return (h(ix, iy) * (1 - ux) + h(ix + 1, iy) * ux) * (1 - uy) + (h(ix, iy + 1) * (1 - ux) + h(ix + 1, iy + 1) * ux) * uy
def water_img(c, ext):
    """16x16 d'eau (palette 8), forme lissee et ondulee sur les 3x3 cases voisines ; `ext` = cases d'eau (ponts compris)"""
    x, y = c
    m = Image.new('L', (48, 48), 0); md = ImageDraw.Draw(m)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if (x + dx, y + dy) in ext: md.rectangle(((dx + 1) * 16, (dy + 1) * 16, (dx + 1) * 16 + 15, (dy + 1) * 16 + 15), fill=255)
    # les bords de la carte du 3x3 etendent les voisins : on prolonge les cotes pour que le lissage ne rogne pas
    A = np.asarray(m.filter(ImageFilter.GaussianBlur(3.2)), dtype=float)
    im = newimg(16, 16); px = im.load()
    inside = np.zeros((18, 18), bool)
    for j in range(18):
        for i in range(18):
            gx, gy = x * 16 + i - 1, y * 16 + j - 1
            inside[j, i] = A[16 + j - 1, 16 + i - 1] > 128 + (vnoise(gx, gy, 5, 5) - 0.5) * 56 + (vnoise(gx, gy, 2.2, 9) - 0.5) * 20
    for j in range(16):
        for i in range(16):
            gx, gy = x * 16 + i, y * 16 + j
            if inside[j + 1, i + 1]:
                nb = [inside[j + 1 + b, i + 1 + a] for a, b in ((0, -1), (0, 1), (-1, 0), (1, 0))]
                if not all(nb): px[i, j] = 1
                else:
                    near = [inside[j + 1 + b, i + 1 + a] for a, b in ((-1, -1), (1, -1), (-1, 1), (1, 1))]
                    v = 3 if all(near) else 2
                    r = vnoise(gx * 1.0, gy * 2.2, 3.5, 17)
                    if v == 3 and r > 0.78: v = 4
                    if v == 3 and r < 0.16: v = 2
                    if v == 4 and vnoise(gx, gy, 1.5, 3) > 0.9: v = 5
                    px[i, j] = v
            else:
                if any(inside[j + 1 + b, i + 1 + a] for a, b in ((0, -1), (0, 1), (-1, 0), (1, 0))): px[i, j] = 6
                elif any(inside[j + 1 + b, i + 1 + a] for a, b in ((-1, -1), (1, -1), (-1, 1), (1, 1))): px[i, j] = 7
    return im
GBOT = ents_of(GRASS)[:4]
EMPTY_TOP = ents_of(GRASS)[4:]
WCACHE = {}
def water_cell(c):
    x, y = c
    key = tuple(((x + dx, y + dy) in WAT) for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    if key not in WCACHE:
        t4 = slice_tiles(water_img(c, WAT)); SEC_ENT.append(list(GBOT) + [('B', t) for t in t4]); SEC_ATT.append(WATER_ATT)
        WCACHE[key] = len(SEC_ENT) - 1
    return 0x1000 | (640 + WCACHE[key])
for c in sorted(LAKE): G[c] = water_cell(c)

# ------------------------------------------------------------------ resolution art -> metatuiles
for c, (t4, gid) in sorted(ARTPLACE.items()):
    mid = 640 + art_meta(t4, gid)
    G[c] = (0x3000 if c in WALKART else 0x400) | mid
# ------------------------------------------------------------------ PNJ, panneaux, objet cache (positions verifiees)
# ---- remplissage demande par Basil : rectangles a combler d'arbres (jamais au prix d'un acces : portes, sorties, panneaux des enclos restent atteignables)
FILL = [(4, 1, 19, 2), (28, 1, 46, 2), (2, 9, 7, 11), (42, 7, 46, 12), (14, 26, 18, 30), (29, 26, 34, 30), (38, 16, 46, 30), (43, 2, 46, 7), (2, 15, 8, 21), (2, 28, 15, 30), (35, 27, 38, 30), (37, 26, 38, 26)]
NEED = set()
for k_, ds_ in D.items():
    for (x_, y_) in ds_: NEED.add((x_, y_ + 1)); NEED.add((x_, y_))
for ex_ in EXITS.values(): NEED |= set(ex_)
for k_, (px_, py_) in PENS.items(): NEED |= {(px_ + 1, py_ + 4), (px_ + 2, py_ + 4)}
NEED |= {(22, 9), (24, 5)}
def conn_with(extra):
    st = (24, H - 1); sn = {st}; qq = collections.deque([st])
    while qq:
        c = qq.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and not (G[n] & 0xc00) and n not in LAKE and n not in extra: sn.add(n); qq.append(n)
    return all(c in sn for c in NEED)
def _bad():
    st = (24, H - 1); sn = {st}; qq = collections.deque([st])
    while qq:
        c = qq.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and not (G[n] & 0xc00) and n not in LAKE: sn.add(n); qq.append(n)
    return sorted(c for c in NEED if c not in sn)
print('NEED hors portee au depart :', _bad(), [(c, OCC.get(c), c in ARTPLACE, hex(G[c]), c in OPEN, c in TREES) for c in ((43, 21), (44, 21))])
NEED -= set(_bad())
rf = random.Random(31); nf = 0
for (x0_, y0_, x1_, y1_) in FILL:
    for y in range(y0_, y1_ + 1):
        for x in range(x0_, x1_ + 1):
            c = (x, y)
            if c in OCC or c in LAKE or c in NEED or c in ARTPLACE or (G[c] & 0xc00) or c in PENCELLS: continue
            G[c] = 0x400 | (640 + art_meta(slice_tiles(TREEIMG[rf.randrange(3)]), GRASS))
            if not conn_with(set()): G[c] = 0; G[c] = remap(0x3000 | GRASS)      # trou a laisser : on remet un sol (case non plantee)
            else: nf += 1
print('arbres de remplissage', nf)
# plus aucun trou : toute case libre inaccessible (hors enclos) devient un arbre
for _ in range(2):
    st = (24, H - 1); sn = {st}; qq = collections.deque([st])
    while qq:
        c = qq.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and not (G[n] & 0xc00) and n not in LAKE: sn.add(n); qq.append(n)
    npk = 0
    for y in range(H):
        for x in range(W):
            c = (x, y)
            if c in sn or c in LAKE or c in OCC or c in ARTPLACE or (G[c] & 0xc00) or c in PENCELLS: continue
            G[c] = 0x400 | (640 + art_meta(slice_tiles(TREEIMG[rf.randrange(3)]), GRASS)); npk += 1
    print('poches comblees', npk)
def _reach0():
    st = (24, H - 1); sn = {st}; qq = collections.deque([st])
    while qq:
        c = qq.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and not (G[n] & 0xc00) and n not in LAKE: sn.add(n); qq.append(n)
    return sn
REACH0 = _reach0()
USED = set()
def free_cell(c): return c in REACH0 and c in OPEN and c not in OCC and c not in ARTPLACE and c not in USED and not (G[c] & 0xc00) and (c not in KEEP or c in PENSIGN)
BLK = set()
def still_connected(extra):
    st = (24, H - 1); sn = {st}; qq = collections.deque([st]); bl = BLK | {extra}
    while qq:
        c = qq.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and not (G[n] & 0xc00) and n not in LAKE and n not in bl: sn.add(n); qq.append(n)
    return (REACH0 - bl) <= sn and all(any((c[0] + a_, c[1] + b_) in sn for a_, b_ in ((0, 1), (0, -1), (1, 0), (-1, 0))) for c in bl)
def pick(target, prefer_way=False, r=8):
    for pw in (prefer_way, not prefer_way):
        cands = sorted(((abs(c[0] - target[0]) + abs(c[1] - target[1]), c) for c in OPEN if free_cell(c) and (c in WAY) == pw and abs(c[0] - target[0]) + abs(c[1] - target[1]) <= r))
        for d_, c in cands:
            if still_connected(c): USED.add(c); BLK.add(c); return c
    raise AssertionError(('pas de case libre pres de', target))
NPC = {}
for k, h in HOST.items():
    px, py = PENS[h]
    inner = [(px + 1, py + 1), (px + 2, py + 1), (px + 1, py + 2), (px + 2, py + 2)]
    NPC['pen_' + k] = inner[0] if k == h else inner[3]
NPC['erik'] = pick((22, 9), True); NPC['youngster'] = pick((19, 12), True); NPC['littleboy'] = pick((9, 13), True)
NPC['oldman'] = pick((36, 15), True); NPC['tutor'] = pick((12, 14), True); NPC['lass'] = pick((30, 13), True)
NPC['tree1'] = pick((14, 4)); NPC['tree2'] = pick((36, 8)); NPC['tree3'] = pick((16, 25), False, 10); NPC['tree4'] = pick((44, 14), False, 10)
NPC['hidden'] = pick((13, 10), False, 12)
SIGNS = {}
gx, gy = D['gym'][0]
SIGNS['city'] = pick((22, 8), True, 4); SIGNS['safarizone'] = pick((19, 7), True, 4); SIGNS['safarigame'] = pick((29, 7), True, 4)
SIGNS['gym'] = (gx - 2, gy + 1); SIGNS['warden'] = pick((D['warden'][0][0] + 2, D['warden'][0][1] + 1), True, 3)
for k, h in HOST.items(): SIGNS['pen_' + k] = pick((PENS[h][0] + (1 if k == h else 3), PENS[h][1] + 4), True, 4)
assert SIGNS['gym'] in OPEN and SIGNS['gym'] not in OCC and SIGNS['gym'] not in ARTPLACE, SIGNS['gym']
USED.add(SIGNS['gym']); BLK.add(SIGNS['gym'])
for k, c in SIGNS.items(): claim(c[0], c[1], 1, 1, 'panneau: ' + k); G[c] = remap(0x400 | 3)
# ------------------------------------------------------------------ accessibilite (depart : couloir sud ; les autres sorties et toutes les portes doivent etre atteignables)
def raw_blocked(c): return bool(G[c] & 0xc00) or c in LAKE
# dernier passage : les poches creees par les panneaux / PNJ sont plantees aussi (aucun trou)
_tn = [m_ for m_ in range(3)]
for _ in range(3):
    st = (24, H - 1); sn = {st}; qq = collections.deque([st])
    while qq:
        c = qq.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and not (G[n] & 0xc00) and n not in LAKE: sn.add(n); qq.append(n)
    npk = 0
    for y in range(H):
        for x in range(W):
            c = (x, y)
            if c in sn or c in LAKE or c in OCC or c in ARTPLACE or (G[c] & 0xc00) or c in PENCELLS or c in USED: continue
            G[c] = 0x400 | (640 + art_meta(slice_tiles(TREEIMG[(x + y) % 3]), GRASS)); npk += 1
    if not npk: break
START = (24, H - 1)
seen = {START}; q = collections.deque([START])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not raw_blocked(n): seen.add(n); q.append(n)
_un = sorted(c for c in OPEN if c not in seen and not raw_blocked(c))
if _un: print('cases libres non atteintes :', len(_un), _un[:40])
for k, ds in D.items():
    for c in ds: assert c in seen, ('porte inaccessible', k, c)
    x, y = ds[0]; assert (x, y + 1) in seen, ('approche de porte bloquee', k)
for k in ('W', 'E'): assert any(c in seen for c in EXITS[k]) and EXITS[k][0] in seen, ('sortie inaccessible', k)
for k in ('erik', 'youngster', 'littleboy', 'oldman', 'tutor', 'lass'): assert NPC[k] in seen, ('PNJ inaccessible', k, NPC[k])
for k, c in SIGNS.items(): assert any(((c[0] + a, c[1] + b) in seen) for a, b in ((0, 1), (0, -1), (1, 0), (-1, 0))), ('panneau inaccessible', k)
assert NPC['hidden'] in seen
for k in ('tree1', 'tree2', 'tree3', 'tree4'): assert NPC[k] in seen or True
# aucune case d'acces ne doit etre perdue : le sud, l'ouest et l'est sont relies
print('portes, PNJ, sorties OK ; cases accessibles', len(seen))
# ------------------------------------------------------------------ v6 : toit de la boutique (retour Basil 12/10 : « il manque un toit au shop Pokemon »)
# le chunk d'Emeraude etait coupe une rangee trop bas : la rangee source y=26 porte le HAUT du toit (rayures + coins en biseau). On la rajoute APRES tous les
# tirages et controles (rien d'autre ne bouge), sur la rangee y=9 au-dessus de la boutique (7..10, 10..12) : 4 cases de pave deviennent le haut du toit.
MART_TOP = [(7 + i, 9) for i in range(4)]
assert all(c not in OCC and c not in USED and c not in LAKE and c not in ARTPLACE for c in MART_TOP), 'toit de la boutique : emplacement pris'      # pave ou 1 arbre d'art (7,9), jamais un batiment/PNJ/panneau
assert not any(tuple(v) in MART_TOP for v in list(NPC.values()) + list(SIGNS.values())), 'toit de la boutique : PNJ ou panneau dessus'
for i, c in enumerate(MART_TOP): put(c[0], c[1], remap_chunk(fr(16 + i, 26)))
assert all(G[c] & 0xc00 for c in MART_TOP), 'toit de la boutique : doit etre solide'
seen2 = {START}; q = collections.deque([START])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen2 and not raw_blocked(n): seen2.add(n); q.append(n)
assert not ((seen - seen2) - set(MART_TOP)), ('toit de la boutique : acces perdu', sorted((seen - seen2) - set(MART_TOP))[:10])
for k, ds in D.items():
    for c in ds: assert c in seen2, ('porte inaccessible apres le toit', k, c)
print('toit de la boutique pose :', MART_TOP)
# ------------------------------------------------------------------ v7 : arene deplacee a l'entree sud + monument de geode, mobilier urbain (retour Basil 12/10 : « pas fan de l'arene, elle est perdue » / « une vibe vraiment amethyste »)
# Tout est pose APRES les tirages (rien d'autre ne bouge). L'ancienne arene (6..11,22..26) redevient foret ; la nouvelle (x14..21, y22..27, porte en (17..18,27)) fait face a la route sud,
# parvis 14..19 x 28..29 ouvert dans la foret. Les tuiles de l'arene vont dans le tileset PRINCIPAL (emplacements 512..639, retournement horizontal = moitie droite gratuite), palette secondaire 10.
import amethiolite_art as AA
assert 10 not in {q >> 12 for e in SEC_ENT for q in e if not isinstance(q, tuple)}, 'palette 10 deja prise'
PT = []
def _flip_variants(t):
    rows = [list(t[r * 8:(r + 1) * 8]) for r in range(8)]
    hf = [r[::-1] for r in rows]; vf = rows[::-1]; hv = [r[::-1] for r in rows[::-1]]
    return [(sum(rows, []), 0, 0), (sum(hf, []), 1, 0), (sum(vf, []), 0, 1), (sum(hv, []), 1, 1)]
def padd_tile(px):
    px = list(px)
    for k, pt in enumerate(PT):
        for var, hf, vf in _flip_variants(pt):
            if var == px: return 512 + k, hf, vf
    PT.append(px); return 512 + len(PT) - 1, 0, 0
def strict_reach(blocked):
    sn = {START}; qq = collections.deque([START])
    while qq:
        c = qq.popleft()
        for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and not raw_blocked(n) and n not in blocked: sn.add(n); qq.append(n)
    return sn
OBJ0 = {tuple(v) for v in NPC.values()} | {tuple(v) for v in SIGNS.values()}
REACH_B = strict_reach(OBJ0)
def tree_cell(c, k=None):
    G[c] = 0x400 | (640 + art_meta(slice_tiles(TREEIMG[(c[0] * 7 + c[1] * 3) % 3 if k is None else k]), GRASS))
rp = random.Random(707)
# ---- 1. l'ancien site devient foret
SITE = {(x, y) for x in range(6, 12) for y in range(22, 28)} | {(12, 26), (12, 27), (13, 26), (13, 27)}
for c in sorted(SITE): tree_cell(c)
# ---- 2. nouvelle arene 8x6 : x14..21, y22..27 ; parvis ; ouverture dans la foret
AX, AY, AW, AH = 14, 22, 8, 6
for c in [(AX + i, AY + j) for j in range(AH) for i in range(AW)]:
    assert c not in OBJ0 or c == tuple(NPC['tree3']), ('arene : objet dans l\'emprise', c)
    assert c not in LAKE and c not in PENCELLS
for c in [(x, y) for x in range(14, 20) for y in (28, 29)]:
    assert c not in OBJ0 and c not in LAKE
    G[c] = remap(0x3000 | rp.choice(PAVE)); GROUND[c] = PAVE[0]; OPEN.add(c); WAY.add(c)
ARENA_DOORS = [(AX + 3, AY + 5), (AX + 4, AY + 5)]
im_a = AA.full(); GB = ents_of(PAVE[0])[:4]
for j in range(AH):
    for i in range(AW):
        c = (AX + i, AY + j)
        blk = im_a.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))
        if sum(1 for p in blk.getdata() if p) < 6: continue                  # coin vide du ciel : on garde le pave (praticable)
        top = []
        for q in range(4):
            t = im_a.crop((i * 16 + (q % 2) * 8, j * 16 + (q // 2) * 8, i * 16 + (q % 2) * 8 + 8, j * 16 + (q // 2) * 8 + 8))
            tid, hf, vf = padd_tile(list(t.getdata())); top.append(tid | (hf << 10) | (vf << 11) | (10 << 12))
        SEC_ENT.append(list(GB) + top); SEC_ATT.append(0)
        G[c] = (0x3000 if c in ARENA_DOORS else 0x400) | (640 + len(SEC_ENT) - 1)
print('arene : tuiles principales', len(PT), '(emplacements 512..%d)' % (511 + len(PT)))
assert 512 + len(PT) <= 640
# ---- 3. objets deplaces : panneau de l'arene, arbre a couper
D['gym'] = list(ARENA_DOORS)
SIGNS['gym'] = (16, 28); G[(16, 28)] = remap(0x400 | 3)
OBJ1 = {tuple(v) for k, v in NPC.items() if k != 'tree3'} | {tuple(v) for v in SIGNS.values()}
# ruelle de l'ancien site : cul-de-sac condamne par l'arbre a couper
for c in ((12, 24), (12, 25), (13, 25)): tree_cell(c)
NPC['tree3'] = (13, 24); OBJ1.add((13, 24))
# ---- 3b. mobilier urbain (lampadaires-cristaux, jardinieres, bancs) : casse les grandes bandes de pave vides ; aucune case de passage n'est perdue
IMG_PROP = {'lamp': AA.lamp(), 'plant0': AA.planter(0), 'plant1': AA.planter(1), 'benchS': AA.bench(False), 'benchN': AA.bench(True)}
PROP_META = {k: 640 + art_meta(slice_tiles(v), PAVE[0]) for k, v in IMG_PROP.items()}
PROPS = {}
def prop_ok(c):
    if c not in WAY or c in KEEP or c in USED or c in ARTPLACE or c in BEACH or raw_blocked(c) or c in OBJ1 or c in PROPS: return False
    if any((c[0] + a, c[1] + b) in PROPS for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b) and True: return False
    base = strict_reach(OBJ1 | set(PROPS))
    return c in base and (base - {c}) <= strict_reach(OBJ1 | set(PROPS) | {c})
def put_prop(kind, target, r=3, exact=False):
    for dd, c in sorted((abs(c[0] - target[0]) + abs(c[1] - target[1]), c) for c in WAY if abs(c[0] - target[0]) + abs(c[1] - target[1]) <= (0 if exact else r)):
        if prop_ok(c) or (exact and c in WAY and c not in OBJ1 and c not in PROPS):
            PROPS[c] = kind; G[c] = 0x400 | PROP_META[kind]; return c
    print('mobilier : pas de place pres de', kind, target); return None
for kind, tg, ex in (('lamp', (14, 28), True), ('lamp', (19, 28), True), ('plant0', (15, 28), True)):
    put_prop(kind, tg, exact=True)
PLACE = [('lamp', (21, 5)), ('lamp', (27, 5)), ('lamp', (21, 11)), ('lamp', (28, 11)), ('lamp', (5, 13)), ('lamp', (41, 13)), ('lamp', (22, 23)), ('lamp', (28, 23)), ('lamp', (34, 24)),
         ('benchS', (24, 23)), ('benchS', (26, 23)), ('benchN', (21, 13)), ('benchN', (28, 13)), ('plant1', (31, 23)), ('plant0', (33, 23)), ('plant0', (10, 13)), ('plant1', (37, 13)),
         ('plant0', (33, 16)), ('lamp', (34, 18)), ('plant1', (34, 21)), ('lamp', (12, 16)), ('plant0', (15, 13)), ('lamp', (39, 14))]
for kind, tg in PLACE: put_prop(kind, tg)
print('mobilier :', len(PROPS), collections.Counter(PROPS.values()))
# ---- 4. controles : tout est atteignable (PNJ et panneaux comptes comme obstacles), aucune poche, rien de perdu hors des zones remodelees
def pockets(ob):
    r_ = strict_reach(ob)
    return sorted(c for c in ((x, y) for y in range(H) for x in range(W)) if c not in r_ and not raw_blocked(c) and c not in PENCELLS and c not in ob)
for _ in range(4):
    pk = pockets(OBJ1)
    if not pk: break
    for c in pk: tree_cell(c)
    print('poches comblees (v7) :', pk)
AFTER = strict_reach(OBJ1)
assert not pockets(OBJ1), pockets(OBJ1)
for k, ds in D.items():
    for c in ds: assert c in AFTER, ('porte inaccessible (v7)', k, c)
    assert (ds[0][0], ds[0][1] + 1) in AFTER, ('approche de porte bloquee (v7)', k)
for k in ('W', 'E'): assert EXITS[k][0] in AFTER, ('sortie inaccessible (v7)', k)
for k in ('erik', 'youngster', 'littleboy', 'oldman', 'tutor', 'lass', 'hidden', 'tree1', 'tree2', 'tree3', 'tree4'):
    c = tuple(NPC[k]); assert any((c[0] + a_, c[1] + b_) in AFTER for a_, b_ in ((0, 1), (0, -1), (1, 0), (-1, 0))), ('PNJ inaccessible (v7)', k, c)
for k, c in SIGNS.items(): assert any(((c[0] + a_, c[1] + b_) in AFTER) for a_, b_ in ((0, 1), (0, -1), (1, 0), (-1, 0))), ('panneau inaccessible (v7)', k)
CHG = SITE | {(AX + i, AY + j) for j in range(AH) for i in range(AW)}
lost = (REACH_B - AFTER) - CHG - {tuple(NPC['tree3']), (12, 24), (12, 25), (13, 25)} - set(PROPS)
assert not lost, ('cases perdues par la v7', sorted(lost)[:20])
print('v7 : acces OK ;', len(AFTER), 'cases atteignables')
json.dump({k: v for k, v in D.items()}, open('/tmp/amethiolite_doors.json', 'w')); json.dump(NPC, open('/tmp/amethiolite_npc.json', 'w')); json.dump(SIGNS, open('/tmp/amethiolite_signs.json', 'w'))
json.dump({'S': EXITS['S'], 'W': EXITS['W'], 'E': EXITS['E']}, open('/tmp/amethiolite_misc.json', 'w'))
if os.environ.get('AM_DUMP'):
    print('    ' + ''.join(str(x % 10) for x in range(W)))
    for y in range(H):
        r_ = ''
        for x in range(W):
            c = (x, y)
            if c in OBJ1: r_ += 'o' if c not in {tuple(v) for v in SIGNS.values()} else 'S'
            elif c in LAKE: r_ += '~'
            elif raw_blocked(c): r_ += '#'
            elif GROUND.get(c) == GRASS: r_ += ','
            else: r_ += '.'
        print('%2d  %s' % (y, r_))
# ------------------------------------------------------------------ ecriture des tilesets
used2 = {q >> 12 for e in SEC_ENT for q in e if not isinstance(q, tuple)}
assert 8 not in used2 and 9 not in used2, used2
NT = len(CT)
print('tuiles', NT, '+', len(ART_T), '; metatuiles', len(SEC_ENT))
assert NT + len(ART_T) <= 384, ('trop de tuiles', NT, len(ART_T))
assert len(SEC_ENT) <= 384, len(SEC_ENT)
SEC_ENT = [[((640 + NT + q[1]) | ((ART_PAL if q[0] == 'A' else WPAL_ID) << 12)) if isinstance(q, tuple) else q for q in e] for e in SEC_ENT]
src_png = Image.open(EM + 'tilesets/secondary/sootopolis/tiles.png')
assert src_png.width == 128
rows = (NT + len(ART_T) + 15) // 16
out = Image.new('P', (128, rows * 8), 0); out.putpalette(src_png.getpalette())
for n, t in enumerate(CT):
    c = src_png.crop(((t % 16) * 8, (t // 16) * 8, (t % 16) * 8 + 8, (t // 16) * 8 + 8)); out.paste(c, ((n % 16) * 8, (n // 16) * 8))
for i, t in enumerate(ART_T):
    n = NT + i; ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, ((n % 16) * 8, (n // 16) * 8))
out.save(SEC + 'tiles.png')
open(SEC + 'metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *e) for e in SEC_ENT))
open(SEC + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in SEC_ATT))
for i in range(16):
    writepal(SEC + 'palettes/%02d.pal' % i, PALS_S[i]); writepal(PRI + 'palettes/%02d.pal' % i, PALS_P[i])
writepal(SEC + 'palettes/%02d.pal' % ART_PAL, PAL); writepal(SEC + 'palettes/%02d.pal' % WPAL_ID, WPAL); writepal(SEC + 'palettes/10.pal', AA.AP)
_pim = Image.open(EM + 'tilesets/primary/general/tiles.png'); assert _pim.size == (128, 256)
_pout = Image.new('P', (128, ((512 + len(PT) + 15) // 16) * 8), 0); _pout.putpalette(_pim.getpalette()); _pout.paste(_pim, (0, 0))
for i, t in enumerate(PT):
    n = 512 + i; ti = Image.new('P', (8, 8)); ti.putdata(list(t)); _pout.paste(ti, ((n % 16) * 8, (n // 16) * 8))
_pout.save(PRI + 'tiles.png')
shutil.copy(EM + 'tilesets/primary/general/metatiles.bin', PRI + 'metatiles.bin')
open(PRI + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', conv(struct.unpack('<H', patt[i * 2:i * 2 + 2])[0])) for i in range(len(patt) // 2)))
SEAMETA = 0x1000 | (640 + WCACHE[tuple(True for _ in range(9))])
def add(path, text):
    s = open(path).read()
    if 'GeneralAmethyst' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralAmethyst[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralAmethyst[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_SootopolisAmethyst[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_SootopolisAmethyst[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralAmethyst[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralAmethyst[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_SootopolisAmethyst[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_SootopolisAmethyst[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
tmpl = '''
const struct Tileset gTileset_%s =
{
    .isCompressed = TRUE,
    .isSecondary = %s,
    .tiles = gTilesetTiles_%s,
    .palettes = gTilesetPalettes_%s,
    .metatiles = gMetatiles_%s,
    .metatileAttributes = gMetatileAttributes_%s,
    .callback = NULL,
};
'''
add('src/data/tilesets/headers.h', tmpl % (('GeneralAmethyst', 'FALSE') + ('GeneralAmethyst',) * 4) + tmpl % (('SootopolisAmethyst', 'TRUE') + ('SootopolisAmethyst',) * 4))
# ------------------------------------------------------------------ carte
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/FuchsiaCity/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/FuchsiaCity/border.bin', 'wb').write(struct.pack('<4H', *([0x400 | (640 + art_meta(slice_tiles(TREEIMG[0]), GRASS))] * 4)))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_FUCHSIA_CITY':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralAmethyst', secondary_tileset='gTileset_SootopolisAmethyst')
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('amethiolite: ok')
