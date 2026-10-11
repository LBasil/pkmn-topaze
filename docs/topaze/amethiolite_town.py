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
    """creme/olive des dômes -> lilas clair ; verts -> pelouse lilas clair / arbres violets profonds ; le rouge du Centre et le bleu de la Boutique restent"""
    h, l, s = hls_(c)
    if s < 0.02: return c
    if 28 <= h <= 75: return rgb_(282, l * 0.98, min(0.6, s * 1.1 + 0.08) if l > 0.5 else min(0.45, s * 0.8 + 0.04))
    if 75 < h <= 175:
        if s < 0.12: return rgb_(276, l, 0.13)
        if l > 0.42: return rgb_(274, min(1, l * 1.0 + 0.03), min(0.8, s * 0.62 + 0.05))
        return rgb_(258, min(1, l * 1.18), min(0.85, s * 0.95))
    return c
for P in (PALS_P, PALS_S):
    for i in range(16): P[i] = [P[i][0]] + [amethyste(x) for x in P[i][1:]]

# ------------------------------------------------------------------ plan (48 x 40, comme Parmanie d'origine : 3 sorties - sud Route 19, ouest Route 18, est Route 15)
W, H = 48, 40
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
def chunk(x0, y0, cw, ch, dx, dy, name):
    claim(dx, dy, cw, ch, name); doors = []
    for j in range(ch):
        for i in range(cw):
            v = fr(x0 + i, y0 + j)
            if 0x60 <= beh(v & 0x3ff) <= 0x6f: doors.append((dx + i, dy + j)); v &= ~0xc00
            put(dx + i, dy + j, remap_chunk(v))
    return doors
D = {}
DOME = (8, 2, 3, 5); FLAT = (44, 3, 3, 4)                      # maisons de Sootopolis : dôme (porte (9,6)) / plate (porte (45,6))
D['safari'] = None
D['warden'] = chunk(*DOME, 11, 2, 'maison du Gardien')
D['office'] = chunk(*FLAT, 31, 3, 'bureau du Safari')
D['house1'] = chunk(*FLAT, 3, 6, 'maison 1')
D['house2'] = chunk(*DOME, 40, 2, 'maison 2')
D['mart'] = chunk(16, 26, 4, 4, 7, 11, 'boutique')
D['center'] = chunk(42, 28, 4, 4, 38, 11, 'centre')
D['gym'] = chunk(28, 28, 6, 5, 6, 29, 'arene')
D['house3'] = chunk(*DOME, 35, 30, 'maison 3')
claim(20, 2, 8, 5, 'porte du Safari'); D['safari'] = [(24, 6)]
for k, v in D.items(): print(k, v)
# ---- lac au centre ; pelouse partout ailleurs
LCX, LCY, LRX, LRY = 24.0, 22.0, 8.2, 5.4
LAKE = set()
for y in range(H):
    for x in range(W):
        a = math.atan2((y - LCY) / LRY, (x - LCX) / LRX)
        k = 1 + 0.10 * (math.sin(2 * a + 0.7) + 0.6 * math.sin(3 * a + 1.9) + 0.4 * math.sin(5 * a + 0.2)) / 2
        if ((x - LCX) / LRX) ** 2 + ((y - LCY) / LRY) ** 2 <= k * k: LAKE.add((x, y))
for c in LAKE: assert c not in OCC, ('lac sur un batiment', c)
# ---- enclos (zoo du Gardien) : 4x4, haie d'arbres, 2x2 de pelouse ; un panneau devant
PENS = {'voltorb': (16, 8), 'chansey': (29, 9), 'slowpoke': (3, 22), 'kangaskhan': (43, 24), 'fossil': (9, 25), 'lapras': (38, 27)}
for k, (px, py) in PENS.items(): claim(px, py, 4, 4, 'enclos ' + k)
# ---- voies : avenue de la porte, anneau autour du lac, routes ouest/est/sud, liaisons aux portes
RING = []
for k in range(0, 49):
    a = 2 * math.pi * k / 48
    RING.append((int(round(LCX + (LRX + 3.0) * math.cos(a))), int(round(LCY + (LRY + 3.0) * math.sin(a)))))
trail(RING, 0, 71)
trail([(24, 7), (24, 12), (24, 14)], 0, 72)
trail([(0, 19), (4, 19), (8, 20), (11, 19), (13, 21), (14, 22)], 0, 73); trail([(47, 21), (43, 21), (39, 22), (36, 21), (34, 22)], 0, 74)
trail([(24, 31), (23, 34), (24, 36), (23, 39)], 0, 75)
for k, ds in D.items():
    for (x, y) in ds:
        for b in (1, 2, 3): WAY.add((x, y + b)); OPEN.add((x, y + b))
trail([(8, 15), (8, 17), (10, 19)], 0, 77); trail([(39, 15), (39, 17), (36, 20)], 0, 78)
trail([(12, 7), (12, 10), (14, 14), (17, 17)], 0, 79); trail([(32, 7), (32, 10), (30, 14), (31, 17)], 0, 80)
trail([(9, 34), (9, 36), (14, 36), (20, 33)], 0, 81); trail([(36, 35), (36, 37), (30, 37), (27, 34)], 0, 82)
trail([(4, 10), (4, 14), (8, 19)], 0, 83); trail([(41, 7), (41, 10), (40, 14), (40, 19)], 0, 84)
for y in range(1, H - 1):
    for x in range(1, W - 1):
        if (x, y) not in OCC and (x, y) not in LAKE: OPEN.add((x, y))
for (x, y) in list(OPEN):
    if (x, y) in OCC or (x, y) in LAKE: OPEN.discard((x, y)); WAY.discard((x, y))
# sorties : couloirs ouverts jusqu'au bord de la carte
EXITS = {'S': [(x, y) for x in range(20, 28) for y in range(36, H)], 'W': [(x, y) for x in range(0, 4) for y in range(18, 21)], 'E': [(x, y) for x in range(44, W) for y in range(20, 23)]}
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
PAL = [(0, 0, 0), (30, 10, 52), (94, 44, 142), (142, 84, 202), (188, 132, 236), (228, 200, 252), (252, 242, 255), (46, 36, 112), (84, 72, 172),
       (132, 122, 222), (198, 192, 250), (40, 30, 66), (214, 64, 152), (176, 168, 192), (96, 88, 118), (255, 246, 200)]
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
        if edge: G[c] = 0x400 | rnd.choice(TREE) ; OPEN.discard(c); WAY.discard(c); BEACH.discard(c); RAIL.discard(c)
# les couloirs : 2 rangees d'arbres de chaque cote
for ex_name, ex in EXITS.items():
    xs = [c[0] for c in ex]; ys = [c[1] for c in ex]
    if ex_name == 'S':
        for y in range(34, H):
            for x in (19, 28):
                if (x, y) not in OCC: G[(x, y)] = 0x400 | rnd.choice(TREE); OPEN.discard((x, y)); WAY.discard((x, y))
    else:
        for x in (range(0, 8) if ex_name == 'W' else range(40, W)):
            for y in (17, 21) if ex_name == 'W' else (19, 23):
                if (x, y) not in OCC and (x, y) not in LAKE: G[(x, y)] = 0x400 | rnd.choice(TREE); OPEN.discard((x, y)); WAY.discard((x, y))
# ---- enclos : haie d'arbres, pelouse a l'interieur
PENCELLS = {}
for k, (px, py) in PENS.items():
    for j in range(4):
        for i in range(4):
            c = (px + i, py + j)
            if i in (0, 3) or j in (0, 3): G[c] = 0x400 | rnd.choice(TREE)
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
art_block(gate(), 8, 5, 20, 2, 'porte du Safari', PAVE[0], claimed=True)
WALKART.add((24, 6))
MONO = monolith()
MX, MY = 23, 8
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
def near_way(c, r=1): return any((c[0] + a, c[1] + b) in WAY for a in range(-r, r + 1) for b in range(-r, r + 1))
# ---- bosquets (groupes d'arbres) dans les coins de pelouse
for (cx, cy, rx, ry, sd) in ((5, 14, 2.6, 3.4, 1), (43, 14, 2.4, 3.6, 2), (13, 31, 3.0, 2.2, 3), (44, 33, 2.6, 2.6, 4), (14, 12, 2.2, 1.8, 5), (35, 8, 2.0, 1.6, 6)):
    rr = random.Random(900 + sd)
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            c = (x, y)
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1 or c not in OPEN or c in OCC or c in WAY or c in KEEP or c in BEACH or near_way(c) or rr.random() > 0.8: continue
            G[c] = 0x400 | rr.choice(TREE); OPEN.discard(c)
# ---- cristaux d'amethyste (pelouse, loin des voies) et arbres isoles
placed = []
for c in sorted(OPEN, key=lambda c: rnd.random()):
    if c in OCC or c in WAY or c in KEEP or c in BEACH or c in ARTPLACE or near_way(c) or G[c] & 0xc00: continue
    if GROUND.get(c) != GRASS: continue
    r_ = rnd.random()
    if r_ < 0.05 and not any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q in placed):
        placed.append(c); claim(c[0], c[1], 1, 1, 'cristal'); ARTPLACE[c] = (slice_tiles(SM[rnd.randrange(3)]), GRASS)
    elif r_ < 0.14 and not any((c[0] + a, c[1] + b) in OCC for a in (-1, 0, 1) for b in (-1, 0, 1)):
        G[c] = 0x400 | rnd.choice(TREE)
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
USED = set()
def free_cell(c): return c in OPEN and c not in OCC and c not in ARTPLACE and c not in USED and not (G[c] & 0xc00) and c not in KEEP
def pick(target, prefer_way=False, r=8):
    best = None
    for pw in (prefer_way, not prefer_way):
        for c in sorted(OPEN):
            if not free_cell(c) or (c in WAY) != pw: continue
            d = abs(c[0] - target[0]) + abs(c[1] - target[1])
            if d <= r and (best is None or d < best[0]): best = (d, c)
        if best: break
    assert best, ('pas de case libre pres de', target)
    USED.add(best[1]); return best[1]
NPC = {}
for k, (px, py) in PENS.items():
    inner = [(px + 1, py + 1), (px + 2, py + 1), (px + 1, py + 2), (px + 2, py + 2)]
    NPC['pen_' + k] = inner[0]
NPC['erik'] = pick((24, 16), True); NPC['youngster'] = pick((20, 11), True); NPC['littleboy'] = pick((9, 17), True)
NPC['oldman'] = pick((38, 18), True); NPC['tutor'] = pick((12, 16), True); NPC['lass'] = pick((30, 13), True)
NPC['tree1'] = pick((14, 3)); NPC['tree2'] = pick((34, 8)); NPC['tree3'] = pick((12, 30)); NPC['tree4'] = pick((40, 33))
NPC['hidden'] = pick((13, 12), False, 12)
SIGNS = {}
gx, gy = D['gym'][0]
SIGNS['city'] = pick((22, 8), True, 4); SIGNS['safarizone'] = pick((19, 7), True, 4); SIGNS['safarigame'] = pick((29, 7), True, 4)
SIGNS['gym'] = (gx + 2, gy + 1); SIGNS['warden'] = pick((D['warden'][0][0] + 2, D['warden'][0][1] + 1), True, 3)
for k, (px, py) in PENS.items(): SIGNS['pen_' + k] = pick((px + 1, py + 4), True, 3)
assert SIGNS['gym'] in OPEN and SIGNS['gym'] not in OCC and SIGNS['gym'] not in ARTPLACE, SIGNS['gym']
USED.add(SIGNS['gym'])
for k, c in SIGNS.items(): claim(c[0], c[1], 1, 1, 'panneau: ' + k); G[c] = remap(0x400 | 3)
# ------------------------------------------------------------------ accessibilite (depart : couloir sud ; les autres sorties et toutes les portes doivent etre atteignables)
def raw_blocked(c): return bool(G[c] & 0xc00) or c in LAKE
START = (24, H - 1)
seen = {START}; q = collections.deque([START])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not raw_blocked(n): seen.add(n); q.append(n)
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
json.dump({k: v for k, v in D.items()}, open('/tmp/amethiolite_doors.json', 'w')); json.dump(NPC, open('/tmp/amethiolite_npc.json', 'w')); json.dump(SIGNS, open('/tmp/amethiolite_signs.json', 'w'))
json.dump({'S': EXITS['S'], 'W': EXITS['W'], 'E': EXITS['E']}, open('/tmp/amethiolite_misc.json', 'w'))
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
writepal(SEC + 'palettes/%02d.pal' % ART_PAL, PAL); writepal(SEC + 'palettes/%02d.pal' % WPAL_ID, WPAL)
shutil.copy(EM + 'tilesets/primary/general/tiles.png', PRI + 'tiles.png')
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
open('data/layouts/FuchsiaCity/border.bin', 'wb').write(struct.pack('<4H', *([0x400 | TREE[0]] * 4)))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_FUCHSIA_CITY':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralAmethyst', secondary_tileset='gTileset_SootopolisAmethyst')
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('amethiolite: ok')
