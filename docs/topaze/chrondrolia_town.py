# CHRONDROLIA (ex-Cinnabar) : la cite jaune du TOPAZE (arene Electrique d'Eddie), electrique : pylones, tour a eclairs, cristaux de topaze.
# Meme methode que Opanihrum / Tourmalia : decors d'Emeraude (ici MAUVILLE, la ville electrique) recopies dans un jeu de tuiles secondaire COMPACTE
# (FireRed : 384 tuiles max), recolores en jaune topaze, + art procedural. Le Manoir Pokemon (ex-salle de jeux de Mauville) est en ruine, envahi par la nature (10 ans).
# Lancer depuis la racine du depot :  python3 docs/topaze/chrondrolia_town.py  puis  chrondrolia_events.py
import struct, json, random, sys, collections, os, shutil, re, math, colorsys
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
EM = '../pokeemerald/data/'
PRI = 'data/tilesets/primary/general_topaze/'; SEC = 'data/tilesets/secondary/mauville_topaze/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
FT = struct.unpack('<800H', open(EM + 'layouts/MauvilleCity/map.bin', 'rb').read())      # 40 x 20
def fr(x, y): return FT[y * 40 + x]
rnd = random.Random(2026)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
PALS_P = [readpal(EM + 'tilesets/primary/general/palettes/%02d.pal' % i) for i in range(16)]
PALS_S = [readpal(EM + 'tilesets/secondary/mauville/palettes/%02d.pal' % i) for i in range(16)]
PALS_P[6] = PALS_S[6]                                       # FireRed : palette 6 = primaire
LD = E.load('general', 'mauville')

# ------------------------------------------------------------------ metatuiles : conversion attributs + compaction du secondaire
patt = open(EM + 'tilesets/primary/general/metatile_attributes.bin', 'rb').read()
satt = open(EM + 'tilesets/secondary/mauville/metatile_attributes.bin', 'rb').read()
smt = open(EM + 'tilesets/secondary/mauville/metatiles.bin', 'rb').read()
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

_PT = Image.open(EM + 'tilesets/primary/general/tiles.png'); _ST = Image.open(EM + 'tilesets/secondary/mauville/tiles.png')
def greenish(q):
    t = q & 0x3ff; pal = (q >> 12) & 15
    src, tt = (_PT, t) if t < 512 else (_ST, t - 512)
    pals = PALS_P if t < 512 else PALS_S
    tile = src.crop(((tt % 16) * 8, (tt // 16) * 8, (tt % 16) * 8 + 8, (tt // 16) * 8 + 8)); px = list(tile.getdata()); n = g = 0
    for i in px:
        if i == 0: continue
        n += 1; h, l, s_ = hls_(pals[pal][i])
        if 72 <= h <= 175 and s_ > 0.15: g += 1
    return n and g / 64.0 > 0.2
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
        GB = struct.unpack('<8H', pmt[16:32])[:4]; CB = struct.unpack('<8H', pmt[94 * 16:94 * 16 + 16])[:4]   # sol d'herbe -> beton
        for qd in range(4):
            if out[qd] == GB[qd] or greenish(out[qd]): out[qd] = CB[qd]
        SEC_ENT.append(out); SEC_ATT.append(conv(struct.unpack('<H', satt[(m - 512) * 2:(m - 512) * 2 + 2])[0]))
        SEC_MAP[m] = 640 + len(SEC_ENT) - 1
    return (v & ~0x3ff) | SEC_MAP[m]
PCOPY = {}
def remap_chunk(v):
    m = v & 0x3ff
    if m >= 512 or m in (94, 1): return remap(v)
    if m not in PCOPY:
        e = list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16])); CB = struct.unpack('<8H', pmt[94 * 16:94 * 16 + 16])[:4]
        ch = False
        for qd in range(4):
            if greenish(e[qd]): e[qd] = CB[qd]; ch = True
        if ch: SEC_ENT.append(e); SEC_ATT.append(conv(struct.unpack('<H', patt[m * 2:m * 2 + 2])[0])); PCOPY[m] = 640 + len(SEC_ENT) - 1
        else: PCOPY[m] = None
    return remap(v) if PCOPY[m] is None else (v & ~0x3ff) | PCOPY[m]
def ents_of(m):
    """8 entrees (tuiles deja remappees) d'une metatuile d'Emeraude"""
    if m < 512: return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16]))
    return list(SEC_ENT[(remap(0x3000 | m) & 0x3ff) - 640])

# ------------------------------------------------------------------ plan
W, H = 28, 20                        # hauteur d'origine (Cinnabar 24x20) ; +4 colonnes a l'est pour la maison des habitants (demande de Basil)
TX, TY = 9, 12                       # pylone-monument 3x3
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
FLOORS = (609, 617)                       # sol pointille de Vergazon (entierement pointille)
# ---- zones ouvertes (le reste = foret)
OPEN = set(); WAY = set()
def blob(cx, cy, rx, ry, seed, amp=0.18, way=False):
    r = random.Random(seed); ph = [r.uniform(0, 6.28) for _ in range(3)]
    for y in range(int(cy - ry) - 2, int(cy + ry) + 3):
        for x in range(int(cx - rx) - 2, int(cx + rx) + 3):
            a = math.atan2((y - cy) / ry, (x - cx) / rx)
            k = 1 + amp * (math.sin(2 * a + ph[0]) + 0.6 * math.sin(3 * a + ph[1]) + 0.4 * math.sin(5 * a + ph[2])) / 2
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= k * k and 1 <= x < W - 1 and 1 <= y < H - 1:
                OPEN.add((x, y))
                if way: WAY.add((x, y))
def rect(x0, y0, x1, y1, way=True):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < W and 0 <= y < H:
                OPEN.add((x, y))
                if way: WAY.add((x, y))
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
# ---- batiments (copie brute des morceaux de Vergazon)
def chunk(x0, y0, cw, ch, dx, dy, name):
    claim(dx, dy, cw, ch, name); doors = []
    for j in range(ch):
        for i in range(cw):
            v = fr(x0 + i, y0 + j)
            if 0x60 <= beh(v & 0x3ff) <= 0x6f: doors.append((dx + i, dy + j)); v &= ~0xc00
            if (v & 0x3ff) in (1, 4): v = (v & ~0x3ff) | 94
            put(dx + i, dy + j, remap_chunk(v)); OPEN.discard((dx + i, dy + j))
    return doors
D = {}
# ---- palette « topaze » : toits roses -> or, paves gris-bleu -> creme chaud (le rouge du Centre et le bleu de la Boutique restent)
def hls_(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb_(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def topaze(c):
    h, l, s = hls_(c)
    if 270 <= h <= 345 and s > 0.15: return rgb_(42 + (h - 300) * 0.05, min(1, l * 1.02 + 0.02), min(0.95, s * 1.1))      # rose / violet -> or / ambre
    if 190 <= h <= 255 and s < 0.40 and l > 0.45: return rgb_(44, min(1, l * 0.97), s * 0.45)              # paves bleutes -> creme
    if 75 <= h <= 165 and s > 0.2: return rgb_(h - 13, l, s)                                                          # verts -> verts dores (soleil d'or)
    return c
for P in (PALS_P, PALS_S):
    for i in range(16): P[i] = [P[i][0]] + [topaze(c) for c in P[i][1:]]


# ---- terre et mer : mer au nord (arrivee de la Route 21 par ponton), baie a l'est (la Route 20), cote au sud ; un peu de foret dans les coins
def nshore(x): return 2.7 + 0.5 * math.sin(x * 0.5 + 0.6)
def sshore(x): return 17.6 + 0.5 * math.sin(x * 0.45 + 1.0)
BAY = set()
for y in range(9, H):
    for x in range(19, W):
        a = math.atan2((y - 13.5) / 5.0, (x - 29.0) / 5.2)
        k = 1 + 0.10 * (math.sin(2 * a + 1.3) + 0.6 * math.sin(3 * a + 0.4)) / 2
        if ((x - 29.0) / 5.2) ** 2 + ((y - 13.5) / 5.0) ** 2 <= k * k: BAY.add((x, y))
LAND = {(x, y) for y in range(H) for x in range(W) if nshore(x) <= y <= sshore(x) and (x, y) not in BAY}
SEA = {(x, y) for y in range(H) for x in range(W)} - LAND
blob(12, 10.5, 10.3, 6.3, 51, amp=0.08)
rect(8, 3, 10, 9)
# ---- batiments (decors de Mauville : maison -> labo, salle de jeux -> manoir en ruine, arene, centre, boutique)
claim(1, 4, 7, 5, 'centrale'); D['mansion'] = [(4, 8)]            # le Manoir est devenu la centrale electrique de l'ile (warp 0 : interieur d'origine pour l'instant)
D['lab'] = chunk(18, 11, 4, 4, 11, 4, 'labo')
D['gym'] = chunk(5, 1, 6, 5, 16, 4, 'arene')
D['center'] = chunk(21, 2, 4, 4, 3, 11, 'centre')
D['mart'] = chunk(22, 11, 4, 4, 15, 11, 'boutique')
D['house'] = chunk(31, 11, 4, 4, 23, 4, 'maison')
for k, v in D.items(): print(k, v)
for c in OCC: assert c in LAND, ('batiment hors terre', c, OCC[c])
# ---- voies : avenue du ponton, rue des facades, promenade du rivage, liaisons, place du pylone
trail([(9, 3), (9, 8), (9, 10)], 0, 61)
trail([(1, 10), (6, 10), (11, 9), (17, 10), (24, 10), (24, 11)], 0, 62)
trail([(1, 16), (6, 16), (11, 16), (17, 16), (19, 16)], 0, 63)
trail([(7, 10), (7, 13), (7, 16)], 0, 65); trail([(13, 10), (14, 13), (14, 16)], 0, 66)
blob(TX + 1, TY + 1, 2.8, 2.8, 64, amp=0.05)
for k, ds in D.items():
    for (x, y) in ds:
        for a in (0,):
            for b in (1, 2, 3):
                if (x + a, y + b) not in OCC and (x + a, y + b) in LAND: OPEN.add((x + a, y + b)); WAY.add((x + a, y + b))
# pontons : nord (la Route 21 arrive par la mer), est (la Route 20)
PIER1 = []
for x in (9, 10):
    PIER1 += [(x, y) for y in range(1, 6) if (x, y) in SEA]
PIER2 = [(x, y) for y in (11, 12) for x in range(19, 28) if (x, y) in SEA]            # ponton de 2 de large
BRIDGEC = set(PIER1) | set(PIER2); PIER1_SET = set(PIER1)
for c in BRIDGEC: claim(c[0], c[1], 1, 1, 'ponton')
OPEN = {c for c in OPEN if c in LAND}
OPEN -= set(OCC); WAY &= OPEN

# ------------------------------------------------------------------ art : pylones et cristaux de topaze (couche haute transparente sur le sol)
ART_PAL = 8
used = {q >> 12 for e in SEC_ENT for q in e}
print('palettes utilisees par les decors', sorted(used))
assert ART_PAL not in used and 9 not in used, used
PAL = [(0, 0, 0), (52, 30, 0), (150, 88, 0), (226, 158, 14), (255, 208, 56), (255, 240, 150), (255, 252, 226), (20, 96, 190), (70, 186, 255),
       (150, 230, 255), (226, 250, 255), (36, 36, 44), (196, 32, 24), (150, 150, 158), (84, 86, 98), (255, 248, 190)]
# 1 contour | 2 ambre fonce | 3 ambre | 4 or | 5 or clair | 6 blanc chaud | 7 bleu electrique fonce | 8 bleu | 9 bleu clair | 10 bleu pale | 11 ombre | 12 braise cramoisie | 13 acier | 14 acier sombre | 15 etincelle
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
def small(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 1, 12, 15, 16)
    if var == 0: prism(d, 4, 14, 5, 9); prism(d, 9, 15, 7, 14); prism(d, 13, 14, 4, 7)
    elif var == 1: prism(d, 6, 15, 6, 11); prism(d, 12, 14, 5, 8); d.rectangle((1, 13, 3, 14), fill=13); d.point((2, 12), fill=14)
    else: prism(d, 8, 15, 8, 14); d.rectangle((2, 13, 4, 14), fill=13); d.rectangle((12, 12, 14, 14), fill=13); d.point((13, 11), fill=14)
    return im

def bolt(d, pts, col=15):
    d.line(pts, fill=col)
def tower():
    """pylone-monument : socle d'acier, mat en treillis, grande topaze au sommet, eclairs (48x48)"""
    im = newimg(48, 48); d = ImageDraw.Draw(im)
    shadow(d, 2, 38, 46, 48)
    d.rectangle((9, 40, 38, 46), fill=13, outline=1); d.rectangle((9, 40, 38, 41), fill=14); d.line([(10, 42), (37, 42)], fill=11)
    d.rectangle((13, 36, 34, 40), fill=14, outline=1)
    for (a, b) in ((14, 33), (33, 33)): d.line([(a, 36), (24, 17)], fill=1)
    d.polygon([(15, 37), (24, 16), (33, 37)], fill=13, outline=1)
    for yy in (22, 27, 32): d.line([(24 - (yy - 16) // 2 - 1, yy), (24 + (yy - 16) // 2 + 1, yy)], fill=14)
    for (a, b, c_, e) in ((24 - 2, 20, 24 + 2, 26), (24 - 4, 26, 24 + 4, 32)): d.line([(a, b), (c_, e)], fill=14)
    prism(d, 24, 22, 13, 20)
    prism(d, 10, 41, 7, 12); prism(d, 38, 41, 7, 14)
    d.rectangle((6, 28, 14, 29), fill=14); d.rectangle((34, 26, 42, 27), fill=14)
    for (x, y) in ((6, 28), (14, 28), (34, 26), (42, 26)): d.rectangle((x - 1, y - 2, x, y), fill=3, outline=1)
    bolt(d, [(6, 26), (8, 23), (7, 21), (10, 17), (9, 15)]); bolt(d, [(42, 24), (40, 21), (41, 19), (38, 15), (39, 13)])
    bolt(d, [(24, 6), (21, 3), (23, 1), (20, 0)]); bolt(d, [(26, 4), (29, 6), (28, 8)])
    for (x, y) in ((9, 14), (10, 15), (39, 12), (38, 11), (22, 2), (27, 3)): d.point((x, y), fill=6)
    return im

def ash(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im); r = random.Random(500 + var)
    for _ in range(26):
        x, y = r.randint(1, 14), r.randint(1, 14); w_, h_ = r.randint(2, 5), r.randint(1, 3)
        d.ellipse((x - w_ // 2, y - h_ // 2, x + w_ // 2, y + h_ // 2), fill=r.choice((11, 11, 14)))
    for _ in range(9): d.point((r.randint(0, 15), r.randint(0, 15)), fill=r.choice((14, 13)))
    x, y = r.randint(3, 11), r.randint(3, 11); d.line([(x, y), (x + r.randint(-3, 3), y + r.randint(1, 3))], fill=12)
    d.point((x, y), fill=12); d.point((r.randint(2, 13), r.randint(2, 13)), fill=12)
    return im
def stump(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 1, 11, 15, 16)
    d.polygon([(4, 14), (5, 4), (7, 2), (9, 4), (11, 14)], fill=11, outline=1)
    d.line([(6, 5), (6, 13)], fill=14); d.line([(9, 6), (9, 12)], fill=14)
    if var: d.line([(9, 4), (13, 1)], fill=11); d.point((13, 1), fill=1)
    else: d.line([(5, 6), (2, 3)], fill=11); d.point((2, 3), fill=1)
    d.point((7, 9), fill=12); d.point((8, 5), fill=12); d.point((7, 12), fill=12)
    return im
ASH = [ash(i) for i in range(4)]; STUMP = [stump(0), stump(1)]

def powerplant():
    """centrale electrique (7x5 cases = 112x80) : deux tours de refroidissement, passerelle de tuyaux, hall d'acier a lucarnes, grande porte a eclair, postes de transformation"""
    im = newimg(112, 80); d = ImageDraw.Draw(im)
    def half_at(y): t = (y - 2) / 60.0; return 9 + int(7 * (abs(t - 0.55) * 2) ** 2)
    for cx in (16, 96):
        for y in range(2, 63):
            h_ = half_at(y)
            d.line([(cx - h_, y), (cx + h_, y)], fill=13); d.point((cx - h_, y), fill=1); d.point((cx + h_, y), fill=1)
            d.line([(cx + h_ - 6, y), (cx + h_ - 1, y)], fill=14); d.line([(cx - h_ + 2, y), (cx - h_ + 4, y)], fill=6)
        for y in (14, 28, 42, 56):
            h_ = half_at(y); d.line([(cx - h_, y), (cx + h_, y)], fill=14)
        h_ = half_at(2); d.rectangle((cx - h_ - 1, 1, cx + h_ + 1, 3), fill=4, outline=1)
        d.line([(cx - 4, 62), (cx - 4, 63)], fill=1)
        for (dx, dy, r_) in ((-4, 1, 5), (3, 0, 4), (8, 2, 3)): d.ellipse((cx + dx - r_, dy - r_ + 3, cx + dx + r_, dy + r_ + 3), fill=6)
    # passerelle de tuyaux entre les tours + montants
    for (y0, col) in ((8, 13), (12, 14)): d.rectangle((30, y0, 82, y0 + 2), fill=col, outline=1)
    for x in (36, 56, 76): d.rectangle((x, 8, x + 3, 25), fill=14, outline=1); d.line([(x + 1, 9), (x + 1, 24)], fill=13)
    # hall : toit, lucarnes, facade
    d.rectangle((28, 24, 84, 41), fill=13, outline=1); d.rectangle((28, 24, 84, 26), fill=4, outline=1)
    for x in (34, 52, 70): d.rectangle((x, 29, x + 10, 37), fill=8, outline=1); d.line([(x + 1, 30), (x + 8, 30)], fill=10); d.line([(x + 1, 31), (x + 4, 31)], fill=9)
    d.rectangle((26, 41, 86, 79), fill=14, outline=1)
    for x in range(30, 84, 8): d.line([(x, 42), (x, 78)], fill=11)
    for k, x in enumerate(range(31, 82, 10)):
        d.rectangle((x, 46, x + 6, 54), fill=5 if k % 2 else 8, outline=1); d.line([(x + 1, 47), (x + 4, 47)], fill=6)
    for x in range(26, 86, 8): d.rectangle((x, 58, x + 3, 60), fill=4); d.rectangle((x + 4, 58, x + 7, 60), fill=1)
    d.rectangle((26, 58, 85, 60), outline=1)
    d.rectangle((44, 47, 68, 57), fill=11, outline=1); d.rectangle((45, 48, 67, 49), fill=4)
    d.line([(58, 49), (54, 53), (58, 53), (54, 56)], fill=15); d.line([(59, 49), (55, 53), (59, 53), (55, 56)], fill=15)
    d.rectangle((45, 61, 66, 79), fill=4, outline=1); d.rectangle((48, 63, 63, 79), fill=1)
    d.line([(49, 64), (49, 78)], fill=11); d.line([(62, 64), (62, 78)], fill=11); d.rectangle((51, 70, 60, 79), fill=11)
    d.line([(52, 66), (59, 66)], fill=8)
    # postes de transformation de chaque cote
    for (x0, x1) in ((1, 25), (87, 111)):
        d.rectangle((x0, 64, x1, 78), fill=14, outline=1); d.line([(x0 + 1, 65), (x1 - 1, 65)], fill=13)
        for xx in range(x0 + 3, x1 - 4, 8):
            d.rectangle((xx, 67, xx + 5, 75), fill=13, outline=1); d.line([(xx + 1, 68), (xx + 4, 68)], fill=6)
            for yy in (69, 72): d.line([(xx + 1, yy), (xx + 4, yy)], fill=4)
            d.rectangle((xx + 1, 63, xx + 2, 66), fill=4, outline=1); d.rectangle((xx + 3, 63, xx + 4, 66), fill=4, outline=1)
    d.rectangle((0, 76, 111, 79), fill=13, outline=1); d.line([(1, 77), (110, 77)], fill=6)
    shadow(d, 0, 78, 111, 79)
    return im
def pylon():
    """pylone a treillis ancre dans une dalle de beton (boulons), traverse a isolateurs et cables (16x32)"""
    im = newimg(16, 32); d = ImageDraw.Draw(im)
    d.rectangle((1, 25, 14, 31), fill=13, outline=1); d.line([(2, 26), (13, 26)], fill=6); d.rectangle((2, 29, 13, 30), fill=14)
    for x in (3, 12): d.point((x, 27), fill=11)
    d.polygon([(4, 26), (7, 5), (8, 5), (11, 26)], fill=None, outline=14)
    d.line([(4, 26), (7, 5)], fill=14); d.line([(11, 26), (8, 5)], fill=14); d.line([(5, 26), (7, 7)], fill=13); d.line([(10, 26), (8, 7)], fill=13)
    for yy in (10, 15, 20): d.line([(7 - (yy - 5) // 5 - 1, yy), (8 + (yy - 5) // 5 + 1, yy)], fill=14)
    for (a, b, c_, e) in ((5, 22, 10, 17), (10, 22, 5, 17), (6, 16, 9, 11)): d.line([(a, b), (c_, e)], fill=13)
    d.rectangle((0, 6, 15, 7), fill=14, outline=1)
    for x in (1, 7, 14): d.rectangle((x - 1, 3, x, 6), fill=4, outline=1)
    d.line([(0, 8), (0, 12)], fill=1); d.line([(15, 8), (15, 12)], fill=1)
    d.point((7, 2), fill=15); d.point((1, 2), fill=6); d.point((14, 2), fill=6)
    d.rectangle((6, 24, 9, 25), fill=4, outline=1)
    return im
ART_T = []
def add_tile(t):
    t = tuple(t)
    if t in ART_T: return ART_T.index(t)
    ART_T.append(t); return len(ART_T) - 1
def slice_tiles(block):
    return [add_tile(list(block.crop(((q % 2) * 8, (q // 2) * 8, (q % 2) * 8 + 8, (q // 2) * 8 + 8)).getdata())) for q in range(4)]
ART_META = {}
def art_meta(tiles4, gid):
    """metatuile a 2 couches : bas = sol d'Emeraude `gid` (4 premieres entrees), haut = art transparent"""
    key = (tuple(tiles4), gid)
    if key not in ART_META:
        base = ents_of(gid)[:4]
        SEC_ENT.append(base + [('A', t) for t in tiles4]); SEC_ATT.append(0)
        ART_META[key] = len(SEC_ENT) - 1
    return ART_META[key]
ARTPLACE = {}                  # (x,y) -> (tuiles4 | None, gid)
def art_block(im, bw, bh, x0, y0, name, gid=609):
    claim(x0, y0, bw, bh, name)
    for j in range(bh):
        for i in range(bw):
            ARTPLACE[(x0 + i, y0 + j)] = (slice_tiles(im.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))), gid)
            OPEN.discard((x0 + i, y0 + j))
SM = [small(0), small(1), small(2)]


# ------------------------------------------------------------------ EAU : mer (nord, sud, baie de l'est) ; pontons de planches
class Ext:
    def __contains__(self, c): return (min(max(c[0], 0), W - 1), min(max(c[1], 0), H - 1)) in WATC
WATC = set(SEA)                      # pontons compris : pas de rive autour des planches
WAT = Ext()
WATERONLY = SEA - BRIDGEC
for c in BRIDGEC: WAY.discard(c)
WATER_ATT = conv(struct.unpack('<H', patt[0xd1 * 2:0xd1 * 2 + 2])[0])
import numpy as np
from PIL import ImageFilter
WPAL_ID = 9
_g = E.metatile(LD, GRASS).convert('RGB'); GR = tuple(int(np.asarray(_g)[:, :, k].mean()) for k in range(3))
WPAL = [(0, 0, 0), (22, 78, 104), (44, 120, 190), (82, 162, 226), (130, 200, 246), (228, 246, 255),
        tuple(int(v * 0.70) for v in GR), tuple(int(v * 0.84) for v in GR),
        (70, 44, 24), (150, 104, 64), (206, 156, 96), (52, 36, 28), (30, 110, 70), (64, 164, 96), (255, 170, 200), (255, 232, 136)]
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
def lily(c):
    im = None
    return im
def plank_img(c):
    x, y = c
    top = (x, y - 1) not in BRIDGEC; bot = (x, y + 1) not in BRIDGEC
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    if c in PIER1_SET:                                   # ponton vertical : planches en travers (horizontales), rails sur les cotes
        d.rectangle((0, 0, 15, 15), fill=9)
        for k in range(0, 16, 4): d.line((0, k, 15, k), fill=10); d.line((0, k + 3, 15, k + 3), fill=11)
        lft = (x - 1, y) not in BRIDGEC; rgt = (x + 1, y) not in BRIDGEC
        if lft: d.rectangle((0, 0, 2, 15), fill=10); d.line((0, 0, 0, 15), fill=8); d.line((2, 0, 2, 15), fill=8)
        if rgt: d.rectangle((13, 0, 15, 15), fill=10); d.line((13, 0, 13, 15), fill=8); d.line((15, 0, 15, 15), fill=8)
        return im
    d.rectangle((0, 0, 15, 15), fill=9)
    for k in range(0, 16, 4): d.line((k, 0, k, 15), fill=10); d.line((k + 3, 0, k + 3, 15), fill=11)
    for (k, yy) in ((1, 5), (2, 11), (0, 2), (3, 9)): d.point(((k + 4 * ((x + yy) % 4)) % 16, yy), fill=8)
    if top: d.rectangle((0, 0, 15, 3), fill=10); d.line((0, 0, 15, 0), fill=8); d.line((0, 3, 15, 3), fill=8); d.line((0, 1, 15, 2), fill=9)
    if bot: d.rectangle((0, 12, 15, 15), fill=10); d.line((0, 12, 15, 12), fill=8); d.line((0, 15, 15, 15), fill=8); d.line((0, 13, 15, 14), fill=9)
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
for c in sorted(WATERONLY): G[c] = water_cell(c)
PCACHE = {}
for c in sorted(BRIDGEC):
    k = ((c[0], c[1] - 1) in BRIDGEC, (c[0], c[1] + 1) in BRIDGEC, c[0] % 4, (c[0] - 1, c[1]) in BRIDGEC, (c[0] + 1, c[1]) in BRIDGEC, c in PIER1_SET)
    if k not in PCACHE:
        t4 = slice_tiles(plank_img(c)); SEC_ENT.append([('B', t) for t in t4] + list(EMPTY_TOP)); SEC_ATT.append(0); PCACHE[k] = len(SEC_ENT) - 1
    G[c] = 0x3000 | (640 + PCACHE[k])

# ------------------------------------------------------------------ sol + foret definitifs
CONC = 94                                                       # betons de Mauville (pave plein)
BEACH = {(x, y) for (x, y) in LAND if (x, y) not in OCC and any((x + a, y + b) in SEA for a in range(-1, 2) for b in range(-1, 2)) and 0 <= x <= W - 1}
LANDING = {(x + a, y + b) for (x, y) in BRIDGEC for a in range(-1, 2) for b in range(-1, 2)}
RAIL = {c for c in BEACH if c not in LANDING}                   # garde-corps le long de la mer (sauf aux pontons)
OPEN = {c for c in LAND if c not in OCC}                        # tout est betonne : plus de foret
GROUND = {}
for (x, y) in sorted(OPEN):
    GROUND[(x, y)] = CONC; G[(x, y)] = remap(0x3000 | CONC)

# ------------------------------------------------------------------ placement de l'art
TOWER = tower(); PYL = pylon()
rect(TX - 1, TY - 1, TX + 3, TY + 3, False)
WALKART = set()
PP = powerplant()
for j in range(5):
    for i in range(7):
        blk = PP.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16)); assert sum(1 for p in blk.getdata() if p) >= 12, ('case de centrale vide', i, j)
        ARTPLACE[(1 + i, 4 + j)] = (slice_tiles(blk), CONC); OPEN.discard((1 + i, 4 + j))
WALKART.add((4, 8))
art_block(TOWER, 3, 3, TX, TY, 'pylone-monument', CONC)
KEEP = set()
for k, ds in D.items():
    for (x, y) in ds:
        for a in range(-2, 3):
            for b in range(-1, 3): KEEP.add((x + a, y + b))
for c in list(BRIDGEC):
    for a in range(-1, 2):
        for b in range(-1, 2): KEEP.add((c[0] + a, c[1] + b))
# pylones electriques (1x2) le long des rues
def crystals(cells, prob, tag):
    placed = []
    for c in cells:
        if c in OCC or c not in OPEN or c in WAY or c in KEEP or c in BEACH or rnd.random() > prob: continue
        if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 2 for q in placed): continue
        placed.append(c); claim(c[0], c[1], 1, 1, tag); ARTPLACE[c] = (slice_tiles(SM[rnd.randrange(3)]), GROUND[c])
    return placed
crystals([c for c in sorted(OPEN) if c in GROUND], 0.035, 'topaze')

def wall_img(sides):
    """mur de quai en beton : bordure surelevee du cote de la mer (clair dessus, face sombre, bande jaune/noire), bollards"""
    im = newimg(16, 16); d = ImageDraw.Draw(im)
    N, S_, Wd_, E_ = sides
    if S_:
        d.rectangle((0, 7, 15, 10), fill=13, outline=1); d.line([(1, 8), (14, 8)], fill=6)
        d.rectangle((0, 11, 15, 15), fill=14, outline=1)
        for k in range(0, 16, 4): d.line([(k, 12), (k, 14)], fill=11)
        for k in range(0, 16, 4): d.rectangle((k, 9, k + 1, 9), fill=4); d.rectangle((k + 2, 9, k + 3, 9), fill=1)
    if N:
        d.rectangle((0, 0, 15, 3), fill=14, outline=1)
        d.rectangle((0, 4, 15, 8), fill=13, outline=1); d.line([(1, 5), (14, 5)], fill=6)
        for k in range(0, 16, 4): d.rectangle((k, 7, k + 1, 7), fill=4); d.rectangle((k + 2, 7, k + 3, 7), fill=1)
    if Wd_:
        d.rectangle((0, 0, 4, 15), fill=13, outline=1); d.line([(1, 1), (1, 14)], fill=6); d.rectangle((5, 0, 6, 15), fill=14)
        for k in range(1, 16, 4): d.rectangle((3, k, 3, k + 1), fill=4)
    if E_:
        d.rectangle((11, 0, 15, 15), fill=13, outline=1); d.line([(12, 1), (12, 14)], fill=6); d.rectangle((9, 0, 10, 15), fill=14)
        for k in range(1, 16, 4): d.rectangle((14, k, 14, k + 1), fill=4)
    return im
for c in sorted(RAIL):
    sides = tuple((c[0] + dx, c[1] + dy) in SEA for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)))
    if not any(sides): sides = (False, True, False, False) if (c[0], c[1] + 1) in SEA or True else sides
    claim(c[0], c[1], 1, 1, 'mur de quai'); ARTPLACE[c] = (slice_tiles(wall_img(sides)), CONC)

# ------------------------------------------------------------------ l'ile a brule il y a dix ans : cendres, braises, souches calcinees (surtout autour du manoir)
rav = random.Random(404)
for c in sorted(OPEN):
    if c in OCC or c in ARTPLACE or c in KEEP or c in BEACH or c not in GROUND: continue
    dm = math.hypot(c[0] - 4.5, c[1] - 8.0)
    if False:
        ARTPLACE[c] = (slice_tiles(ASH[rav.randrange(4)]), CONC); WALKART.add(c)
ns = 0
print('souches', ns, 'cendres', len(WALKART))

# ------------------------------------------------------------------ PNJ, panneaux (positions verifiees)
USED = set()
def pick(target, prefer_way=False, r=8):
    best = None
    for pw in (prefer_way, not prefer_way):
        for c in sorted(OPEN):
            if c in OCC or c in KEEP or c in USED or c in ARTPLACE: continue
            if (c in WAY) != pw: continue
            d = abs(c[0] - target[0]) + abs(c[1] - target[1])
            if d <= r and (best is None or d < best[0]): best = (d, c)
        if best: break
    assert best, ('pas de case libre pres de', target)
    USED.add(best[1]); return best[1]
NPC = {}
NPC['woman'] = pick((14, 12)); NPC['oldman'] = pick((6, 13))
NPC['bill'] = (9, 2); NPC['gull'] = (12, 2)
gx, gy = D['gym'][0]; lx, ly = D['lab'][0]
SIGNS = {'city': pick((7, 5), r=6), 'lab': (lx - 1, ly + 1), 'gym': (gx + 2, gy + 2)}          # panneaux de part et d'autre des portes, pas des pick() qui derivent
for k in ('lab', 'gym'): assert SIGNS[k] in OPEN and SIGNS[k] not in OCC and SIGNS[k] not in ARTPLACE and SIGNS[k] not in USED, (k, SIGNS[k])
for k, c in SIGNS.items(): claim(c[0], c[1], 1, 1, 'panneau: ' + k)
def pylon_at(x, y):
    cells = [(x, y), (x, y + 1)]
    if any(OCC.get((x + a, y + b), 'mur de quai') in ('maison', 'labo', 'arene', 'centre', 'boutique', 'centrale', 'pylone-monument') for a in (-1, 0, 1) for b in (-1, 0, 1, 2)): return False
    if any(c in OCC or c not in OPEN or c in WAY or c in KEEP or c in BEACH or c in USED for c in cells): return False
    claim(x, y, 1, 2, 'pylone'); ARTPLACE[(x, y)] = (slice_tiles(PYL.crop((0, 0, 16, 16))), CONC); ARTPLACE[(x, y + 1)] = (slice_tiles(PYL.crop((0, 16, 16, 32))), CONC)
    OPEN.discard((x, y)); OPEN.discard((x, y + 1)); GROUND.pop((x, y), None); GROUND.pop((x, y + 1), None)
    return True
npl = 0
PYS = []
for (x, y) in sorted(OPEN, key=lambda c: (c[1] * 7 + c[0] * 3) % 11):
    if npl >= 9: break
    if any(max(abs(x - p[0]), abs(y - p[1])) < 5 for p in PYS): continue
    if pylon_at(x, y): npl += 1; PYS.append((x, y))
print('pylones', npl)

# ------------------------------------------------------------------ resolution art -> metatuiles, valeurs brutes
for c, (t4, gid) in sorted(ARTPLACE.items()):
    mid = 640 + art_meta(t4, gid)
    G[c] = (0x3000 if c in WALKART else 0x400) | mid
for k, c in SIGNS.items(): G[c] = remap(0x400 | 3)
# ---- sentiers : sable d'Emeraude (autotuile) ; ring de pelouse autour du pylone
PATHC = {c for c in WAY if c in OPEN and c not in OCC and c not in ARTPLACE and not (G[c] & 0xc00)}
RING = {(x, y) for x in range(TX - 1, TX + 4) for y in range(TY - 1, TY + 4)} - {(x, y) for x in range(TX, TX + 3) for y in range(TY, TY + 3)}
PATHC = set()
def _free(c):
    return (c not in RING and c in OPEN and c not in OCC and c not in ARTPLACE and not (G[c] & 0xc00) and 0 <= c[0] < W and 0 <= c[1] < H)
for _ in range(3):
    add = set()
    for (x, y) in PATHC:
        P_ = lambda c: c in PATHC or c in add
        if not P_((x - 1, y)) and not P_((x + 1, y)):
            for c in ((x + 1, y), (x - 1, y)):
                if _free(c): add.add(c); break
        if not P_((x, y - 1)) and not P_((x, y + 1)):
            for c in ((x, y + 1), (x, y - 1)):
                if _free(c): add.add(c); break
        for (dx, dy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            if P_((x + dx, y)) and P_((x, y + dy)) and not P_((x + dx, y + dy)) and _free((x + dx, y + dy)): add.add((x + dx, y + dy))
    if not add: break
    PATHC |= add
def path_id(x, y):
    f = lambda c: (c in PATHC) or c[0] < 0 or c[0] >= W or c[1] < 0 or c[1] >= H or c in BRIDGEC or (c in OCC and not (G.get(c, 0) & 0xc00) and c not in OPEN)
    N = f((x, y - 1)); S = f((x, y + 1)); Wn = f((x - 1, y)); E_ = f((x + 1, y))
    if N and S and Wn and E_: return 289
    if not N and not Wn and S and E_: return 280
    if not N and not E_ and S and Wn: return 282
    if not S and not Wn and N and E_: return 296
    if not S and not E_ and N and Wn: return 298
    if not N and S and Wn and E_: return 281
    if not S and N and Wn and E_: return 297
    if not Wn and N and S and E_: return 288
    if not E_ and N and S and Wn: return 290
    return 289
for (x, y) in PATHC:
    G[(x, y)] = remap(0x3000 | path_id(x, y))

for (x, y) in sorted(OPEN):
    c = (x, y)
    if c in PATHC or c in OCC or c in ARTPLACE or c in KEEP or (G[c] & 0xc00): continue
    if GROUND.get(c) == GRASS and c not in BEACH and rnd.random() < 0.10: G[c] = remap(0x3000 | 4)
# manoir : dix ans d'abandon, la nature a repris la facade (herbe haute, buissons, fleurs)
rv = random.Random(88)
for (x, y) in sorted(OPEN):
    c = (x, y)
    if True or c in BEACH or c in PATHC or c in OCC or c in ARTPLACE or c in KEEP or (G[c] & 0xc00): continue
    r_ = rv.random()
    if r_ < 0.50: G[c] = remap(0x3000 | 13)
    elif r_ < 0.62: G[c] = remap(0x400 | 5)
    elif r_ < 0.72: G[c] = remap(0x3000 | 4)
def raw_blocked(c): return bool(G[c] & 0xc00) or c in WATERONLY
# ------------------------------------------------------------------ accessibilite (depart : bout du ponton nord ; les pontons sont le point d'arrivee par mer)
START1 = PIER1[0]; START2 = PIER2[-1]
seen = {START1}; q = collections.deque([START1])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not raw_blocked(n): seen.add(n); q.append(n)
for k, ds in D.items():
    for c in ds: assert c in seen, ('porte inaccessible', k, c)
assert START2 in seen, 'ponton est inaccessible'
for k in ('woman', 'oldman'): assert NPC[k] in seen, ('PNJ inaccessible', k, NPC[k])
for k, c in SIGNS.items(): assert any(((c[0] + a, c[1] + b) in seen) for a, b in ((0, 1), (0, -1), (1, 0), (-1, 0))), ('panneau inaccessible', k)
# la porte doit avoir au moins une case voisine libre (approche) et la case sous la porte ne doit pas etre bloquee
for k, ds in D.items():
    x, y = ds[0]; assert (x, y + 1) in seen, ('approche de porte bloquee', k)
print('portes, PNJ, pontons OK ; cases accessibles', len(seen))
json.dump(D, open('/tmp/chrondrolia_doors.json', 'w')); json.dump(NPC, open('/tmp/chrondrolia_npc.json', 'w')); json.dump(SIGNS, open('/tmp/chrondrolia_signs.json', 'w'))
json.dump({'pier1': PIER1, 'pier2': PIER2}, open('/tmp/chrondrolia_misc.json', 'w'))
# ------------------------------------------------------------------ ecriture des tilesets
used2 = {q >> 12 for e in SEC_ENT for q in e if not isinstance(q, tuple)}
assert 8 not in used2 and 9 not in used2, used2
NT = len(CT)
assert NT + len(ART_T) <= 384, ('trop de tuiles', NT, len(ART_T))
assert len(SEC_ENT) <= 384, len(SEC_ENT)
SEC_ENT = [[((640 + NT + q[1]) | ((ART_PAL if q[0] == 'A' else WPAL_ID) << 12)) if isinstance(q, tuple) else q for q in e] for e in SEC_ENT]
src_png = Image.open(EM + 'tilesets/secondary/mauville/tiles.png')
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

SEAMETA = 0x1000 | (640 + WCACHE[tuple(True for _ in range(9))]) if tuple(True for _ in range(9)) in WCACHE else None
assert SEAMETA, 'pas de metatuile de mer pleine'
def add(path, text):
    s = open(path).read()
    if 'GeneralTopaze' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralTopaze[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralTopaze[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_MauvilleTopaze[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_MauvilleTopaze[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralTopaze[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralTopaze[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_MauvilleTopaze[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_MauvilleTopaze[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
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
add('src/data/tilesets/headers.h', tmpl % (('GeneralTopaze', 'FALSE') + ('GeneralTopaze',) * 4) + tmpl % (('MauvilleTopaze', 'TRUE') + ('MauvilleTopaze',) * 4))
# ------------------------------------------------------------------ carte
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/CinnabarIsland/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
sea = 0x400 | (SEAMETA & 0x3ff) | 0x0
open('data/layouts/CinnabarIsland/border.bin', 'wb').write(struct.pack('<4H', *([0x400 | (SEAMETA & 0x3ff)] * 4)))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') == 'LAYOUT_CINNABAR_ISLAND':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralTopaze', secondary_tileset='gTileset_MauvilleTopaze')
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('chrondrolia: tuiles', NT, '+', len(ART_T), 'art ; metatuiles', len(SEC_ENT))
