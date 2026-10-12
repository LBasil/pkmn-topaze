# ROUTES 16 + 17 v3 : « du quartz a l'ametyste » (v1 = habillage : branche route16-v1-reference ; v2d = cartes sinueuses sans relief : branche route16-v2-reference).
# Route 16 (depart : Bourg Quartz, neige qui tombe, a l'EST) -> Route 17 (160 cases, vers le SUD) -> Route 18 (arrivee : Amethiolite, lilas). Cartes NOUVELLES, relief et eau :
#   - terrasses : murets de pierre (autotuile par quarts de 8x8) coupes par des escaliers ; la Route 17 descend de palier en palier vers la mer,
#   - eau : etangs gelés / bassins et ruisseaux dessines par un autotuile maison (par quarts, forme libre), pont de planches (cases praticables) la ou le chemin traverse,
#   - jardin de cristaux secret sur un plateau (Route 16), cercle d'amethyste (Route 17), ile de cristal dans un bassin, portail de cristaux a la jonction 16/17,
#   - une seule famille de tilesets (`general_route16` / `celadon_route16`) : etage 0 = neige de Bourg Quartz, etage 1 = lilas d'amethyste (palettes de la Route 18), fonte progressive ;
#     palettes 4/6 = bleu de la Route 18 partout ; 10 = art amethyste, 12 = art quartz, 11 = pierre / bois (muret, escalier, pont).
# Le secondaire est COMPACTE (seules les metatuiles et tuiles reellement utilisees sont gardees) pour liberer de la place.
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
# pierre / bois : 1 trait sombre, 2 ombre portee (gris-lilas, vaut sur neige et sur lilas), 3 joint, 4 pierre, 5 chapeau clair, 6/7 pied, 8/9 neige, 10-13 bois, 14 mousse, 15 reflet
PAL_S = [(0, 0, 0), (62, 56, 96), (172, 176, 208), (112, 108, 148), (158, 156, 190), (232, 238, 252), (104, 98, 138), (80, 74, 114), (248, 251, 255), (208, 222, 242),
         (124, 92, 72), (172, 132, 100), (214, 180, 140), (72, 52, 50), (150, 124, 196), (210, 230, 250)]
ART_AME, ART_QTZ, WALLP, SHIFT = 10, 12, 11, {0: 7, 3: 8, 5: 9}        # emplacements : art amethyste, art quartz, pierre/bois ; palette d'origine -> emplacement lilas
for src, dst in ((GEN, NP), (SEC, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    shutil.copytree(src + 'anim', dst + 'anim') if os.path.isdir(src + 'anim') else None
    for i in range(16): shutil.copy(src + 'palettes/%02d.pal' % i, dst + 'palettes/%02d.pal' % i)
for i in range(7): shutil.copy('data/tilesets/primary/general_celadopole/palettes/%02d.pal' % i, NP + 'palettes/%02d.pal' % i)
for i in (4, 6): shutil.copy('data/tilesets/primary/general_route18/palettes/%02d.pal' % i, NP + 'palettes/%02d.pal' % i)      # palettes 4 et 6 = eau (mer, rivages, etangs) : bleu profond de la Route 18 partout
p0 = readpal(NP + 'palettes/00.pal'); p0[1], p0[2], p0[3], p0[12] = (247, 251, 255), (229, 240, 251), (186, 208, 230), (218, 232, 245)      # neige plus blanche (sol, cimes des arbres)
writepal(NP + 'palettes/00.pal', p0)
p5 = readpal(NP + 'palettes/05.pal'); p5[10], p5[11], p5[12] = (178, 192, 210), (170, 185, 204), (150, 168, 190)       # chemin de neige tassee : plus fonce que la neige (lisibilite)
writepal(NP + 'palettes/05.pal', p5)
for o, sl in SHIFT.items(): writepal(NS + 'palettes/%02d.pal' % sl, readpal('data/tilesets/primary/general_route18/palettes/%02d.pal' % o))
writepal(NS + 'palettes/%02d.pal' % ART_AME, PAL_A); writepal(NS + 'palettes/%02d.pal' % ART_QTZ, PAL_Q); writepal(NS + 'palettes/%02d.pal' % WALLP, PAL_S)
WATP = readpal(NP + 'palettes/04.pal')

# ------------------------------------------------------------------ metatuiles (secondaire COMPACTE : on ne garde que ce que les cartes d'origine utilisent)
pmt = open(GEN + 'metatiles.bin', 'rb').read(); patt = struct.unpack('<%dI' % (os.path.getsize(GEN + 'metatile_attributes.bin') // 4), open(GEN + 'metatile_attributes.bin', 'rb').read())
smt0 = open(NS + 'metatiles.bin', 'rb').read(); satt0 = struct.unpack('<%dI' % (len(smt0) // 16), open(NS + 'metatile_attributes.bin', 'rb').read())
ORIG = {L: list(struct.unpack('<%dH' % (w * h * (2 if L == 'Route17' else 1)), open(SRC + ('r16_orig.bin' if L == 'Route16' else 'r17_orig.bin'), 'rb').read())) for L, (w, h) in DIMS.items()}
KEEPM = sorted({v & 0x3ff for g in ORIG.values() for v in g if (v & 0x3ff) >= 640})
RM = {old: 640 + i for i, old in enumerate(KEEPM)}
def rm(v): return (v & 0xfc00) | RM.get(v & 0x3ff, v & 0x3ff)           # id d'origine -> id compacte (primaire : inchange)
simg0 = Image.open(NS + 'tiles.png'); tw0 = simg0.width // 8
rawm = [list(struct.unpack('<8H', smt0[(o - 640) * 16:(o - 640) * 16 + 16])) for o in KEEPM]
KEEPT = sorted({(e & 0x3ff) - 640 for es in rawm for e in es if (e & 0x3ff) >= 640}); RT = {old: i for i, old in enumerate(KEEPT)}
smt = bytearray(b''.join(struct.pack('<8H', *[((e & 0xfc00) | (640 + RT[(e & 0x3ff) - 640])) if (e & 0x3ff) >= 640 else e for e in es]) for es in rawm))
satt = [satt0[o - 640] for o in KEEPM]
simg = Image.new('P', (128, ((len(KEEPT) + 15) // 16) * 8), 0); simg.putpalette(simg0.getpalette())
for old, new in RT.items(): simg.paste(simg0.crop(((old % tw0) * 8, (old // tw0) * 8, (old % tw0) * 8 + 8, (old // tw0) * 8 + 8)), ((new % 16) * 8, (new // 16) * 8))
NMT = len(smt) // 16; NTL = len(KEEPT)
NEWE, NEWA, VAR, NEWT = [], [], {}, []
def ents(m):
    if m >= 640 + NMT: return list(NEWE[m - 640 - NMT])
    return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
def att(m):
    if m >= 640 + NMT: return NEWA[m - 640 - NMT]
    return patt[m] if m < 640 else satt[m - 640]
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


# ------------------------------------------------------------------ art v3 : murets, escaliers, eau (autotuile par quarts de 8x8), pont. Indices : voir PAL_S (pierre/bois) et WATP (palette 4 = eau de la Route 18)
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

# ------------------------------------------------------------------ sol de neige (palette 0 : 1 blanc, 2 bleu tres pale, 12 / 13 ombres de congere, 5 caillou) : 7 variantes 16x16 qui se raccordent en largeur
def snow_pat(var):
    r = random.Random(4400 + var * 37); g = [[1] * 16 for _ in range(16)]
    spark = {0: (0.05, 0.015), 6: (0.06, 0.02), 4: (0.12, 0.04)}.get(var, (0.04, 0.012))
    for y in range(16):
        for x in range(16):
            u = r.random()
            if u < spark[0]: g[y][x] = 2
            elif u < spark[0] + spark[1]: g[y][x] = 12
    if var == 1:
        for x in range(16):
            y0 = 5 + int(round(1.6 * math.sin(2 * math.pi * x / 16)))
            g[y0][x] = 1; g[y0 + 1][x] = 12; g[y0 + 2][x] = 2 if x % 3 else 12
    elif var == 2:
        for x in range(16):
            y0 = 11 + int(round(1.2 * math.sin(2 * math.pi * x / 16 + 1.5)))
            g[y0][x] = 1; g[y0 + 1][x] = 12; g[(y0 + 2) % 16][x] = 2
        for x in range(3, 12):
            y0 = 2 + int(round(0.9 * math.sin(2 * math.pi * x / 9)))
            g[y0][x] = 12 if x % 2 else 2
    elif var == 3:
        for x in range(3, 13):
            cr = 5 + int(round(((x - 8) / 5.0) ** 2 * 2.6))
            g[cr][x] = 1; g[cr + 1][x] = 12; g[cr + 2][x] = 13 if 4 < x < 11 else 12; g[cr + 3][x] = 2
    elif var == 5:
        for (px, py) in ((4, 5), (11, 10)):
            g[py][px] = 5; g[py][px + 1] = 5; g[py + 1][px] = 13; g[py + 1][px + 1] = 5; g[py - 1][px] = 1
    return g
def snow_tiles(var):
    g = snow_pat(var); return [add_tile([g[(q // 2) * 8 + j][(q % 2) * 8 + i] for j in range(8) for i in range(8)]) for q in range(4)]
SNOWM = {}
def snow_meta(var):
    """metatuile de sol : 4 quarts bas dessines (palette 0), calque haut vide ; comportement normal."""
    if var not in SNOWM: SNOWM[var] = new_meta([('T', t, 0) for t in snow_tiles(var)] + [0, 0, 0, 0], 0)
    return SNOWM[var]
def snow_var(x, y):
    n = noise(x * 0.9 + 3, y * 0.9 + 1); h = (x * 73856093 ^ y * 19349663) % 1000
    if n > 0.42: return 1 if (x + y) % 2 else 2
    if n < -0.50: return 3
    if h < 45: return 5
    if h < 200: return 4
    return 0 if (x + y) % 2 else 6

# ================================================================== CARTES v3
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

def build(L, rnd):
    W, H = DIMS[L]; orig = ORIG[L]
    SEA, FIXED, WALLU, WROWS, WATER, BRIDGES, HOLES, CLEAR, MEAD, GATES, PONDS = {}, {}, [], {}, {}, {}, set(), set(), set(), [], []
    def pond(cells, style): PONDS.append((cells, style)); [WATER.__setitem__(c, style) for c in cells]
    if L == 'Route17':
        pts = [(9.5, 0), (9.5, 2.5), (11.5, 5), (14, 7.5), (16, 9.5), (15, 11), (15, 13), (15, 15), (13, 17.5), (10, 19.5), (7, 21), (6, 23), (6, 25), (7.5, 27.5), (8.5, 29), (8.5, 31), (8.5, 33),
               (11, 35.5), (14.5, 37.5), (17, 40.5), (16, 43), (14.5, 45), (14.5, 47), (14.5, 49), (13, 51), (10.5, 52), (9, 54), (10, 56.5), (12.5, 58.5), (12.5, 60), (12.5, 62), (13, 64), (14, 68), (13, 72), (12, 76), (12, 79)]
        PATH = disc_path(pts, lambda x, y: 1.1 + 0.25 * math.sin(y * 0.7), W, H)
        PATH |= {(x, y) for y in (0, 1) for x in range(8, 12)} | {(x, y) for y in (H - 2, H - 1) for x in range(8, 17)}
        for y in range(H - 14, H):
            for x in list(range(0, 8)) + list(range(17, 24)): SEA[(x, y)] = rm(orig[(y + 80) * 24 + x])
        for yw in (13, 31, 47, 61): WROWS[yw] = (0, W - 1)
        pond(blob(4.2, 6.4, 3.4, 2.8, 3, W, H), 'ice')                       # lac gele de la plaine
        pond(blob(19.3, 22.9, 3.0, 2.4, 11, W, H), 'water')                  # bassin source
        pond(hstream(lambda x: 23.0 + 1.0 * math.sin(x / 3.0 + 0.6), 0, 17, W, H), 'water')     # ruisseau vers l'ouest, jusque sous les arbres
        island = {(3, 39), (4, 39), (3, 40), (4, 40)}
        pb = blob(4.4, 40.0, 3.8, 2.9, 23, W, H) | island
        pond(pb, 'water'); HOLES |= island
        pond(blob(3.0, 57.2, 2.6, 2.1, 31, W, H), 'water')
        BRIDGES = {'S1': ('V', {c for c in hstream(lambda x: 23.0 + 1.0 * math.sin(x / 3.0 + 0.6), 0, 17, W, H) if c in PATH})}
        MEAD = {(x, y) for x in range(W) for y in range(H) if noise(x * 1.35 + 7, y * 1.35 + 3) > 0.34} | ell(19, 52, 5, 3.6, W, H)
        CLEAR = set()
        GATES = [(6, 1), (12, 1)]
    else:
        # COL ENNEIGE : Bourg Quartz est en haut ; plateau d'altitude (est -> ouest), gorge du Ronflex, puis descente par un escalier vers le palier du bas et la Route 17
        pts = [(47, 13), (45.5, 13), (44, 12.5), (42.5, 12), (41, 10.5), (39, 9.5), (37.2, 10.5), (36, 12), (35, 12.5)]
        PATH = disc_path(pts, 1.1, W, H) | {(x, y) for x in range(29, 36) for y in (12, 13)}
        PATH |= disc_path([(29, 12.5), (27, 12), (24.5, 11.3), (21.8, 11.8), (20.8, 12.6)], 1.1, W, H)
        PATH |= disc_path([(21.5, 11.8), (18.5, 11), (15.5, 10.2), (13, 9.2), (11.5, 8), (10.6, 6.6)], 1.1, W, H)          # branche vers la maison (en haut)
        PATH |= disc_path([(20.8, 12.6), (20.6, 13.5), (20.6, 15), (20.6, 16.4)], 1.0, W, H)                              # vers l'escalier de la descente
        PATH |= disc_path([(20.6, 16.4), (18, 17.3), (15, 17.8), (12.5, 18.0), (10.5, 18.5), (9.5, 19)], 1.0, W, H)         # palier du bas
        PATH |= {(x, y) for y in (18, 19) for x in range(8, 12)} | {(x, 12) for x in (45, 46, 47)} | {(x, 14) for x in (45, 46, 47)}
        for y in (3, 4, 5):
            for x in range(9, 14): FIXED[(x, y)] = rm(orig[y * 48 + x])
        PATH -= set(FIXED)
        WALLU = [(x, y) for x in (30, 32) for y in list(range(0, 12, 2)) + [14, 16, 18]]
        WROWS[14] = (0, 28)                                                                                                   # falaise de la descente (2 cases), escalier au passage du chemin
        lake = blob(41.5, 4.4, 4.6, 2.9, 5, W, H); pond(lake, 'ice')
        st16 = vstream(lambda y: 42.3 + 0.9 * math.sin(y / 2.3), 7, 19, W, H) - lake; pond(st16, 'water')
        BRIDGES = {'S1': ('H', {c for c in st16 if c in PATH})}
        pond(blob(4.4, 10.0, 3.0, 2.2, 17, W, H), 'ice')                      # etang gele de l'ouest
        MEAD = {(x, y) for x in range(W) for y in range(H) if noise(x * 1.35 + 2, y * 1.35 + 9) > 0.45}
        CLEAR = set()
        GATES = [(6, 17), (12, 17)]
    WSET = set(WATER) - HOLES
    BR = set(); BRO = {}
    for k, (o, cells) in BRIDGES.items():
        xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
        if o == 'V':        # chemin nord-sud : pont rectangulaire sur toute la largeur du chemin, du bord nord au bord sud du ruisseau
            xa, xb = min(xs), max(xs); yy = [c[1] for c in WSET if xa <= c[0] <= xb and abs(c[1] - ys[0]) <= 3]
            rect = {(x, y) for x in range(xa, xb + 1) for y in range(min(yy), max(yy) + 1)}
        else:
            ya, yb = min(ys), max(ys); xx = [c[0] for c in WSET if ya <= c[1] <= yb and abs(c[0] - xs[0]) <= 3]
            rect = {(x, y) for y in range(ya, yb + 1) for x in range(min(xx), max(xx) + 1)}
        for c in rect: BR.add(c); BRO[c] = o; WSET.add(c)
    PATH_SAND = PATH - WSET
    PATH |= BR
    # ---- murets : les cases du chemin sur la rangee deviennent des marches (si le chemin existe au nord ET au sud), le reste est mur
    WALL, STAIR = set(), set()
    for yw, (xa, xb) in WROWS.items():
        st = {x for x in range(xa, xb + 1) if all((x, yw + k) in PATH for k in (-1, 0, 1, 2))}
        assert len(st) >= 2, ('escalier', L, yw)
        for x in range(xa, xb + 1):
            for k in (0, 1):
                if x in st: STAIR.add((x, yw + k))
                else: WALL.add((x, yw + k))
    ICE = set()
    for yw, (xa, xb) in WROWS.items():
        last = -9
        for x in range(xa + 2, xb - 1):
            if all((x + d, yw + k) in WALL for d in (-1, 0, 1) for k in (0, 1)) and (x * 5 + yw * 3) % 7 in (0, 1) and x - last >= 6: ICE |= {(x, yw), (x, yw + 1)}; last = x
    PATH_SAND -= WALL | STAIR | set(HOLES)
    PATH -= WALL
    FEAT = WSET | WALL | STAIR | BR
    PATH_ALL = PATH_SAND | STAIR | BR
    BUF = dil(PATH_ALL, 1) | dil(set(FIXED), 1)
    DM = distmap(PATH_ALL, W, H)
    nofor = PATH_ALL | BUF | set(FIXED) | set(SEA) | dil(WSET, 1) | WALL | dil(STAIR, 1) | CLEAR
    if L == 'Route17':
        FOREST = {(x, y) for y in range(H) for x in range(W) if (x, y) not in nofor | MEAD and DM[(x, y)] >= 2 + ((x * 7 + y * 13) % 5 == 0)}
    else:
        WALLC = set()
        for (x, y) in WALLU: WALLC |= {(x + i, y + j) for i in range(2) for j in range(2)}
        edge = lambda x, y: y <= 1 or y >= 18 or x <= 2 or x >= 44
        FOREST = {(x, y) for y in range(H) for x in range(W) if (x, y) not in nofor and (edge(x, y) or ((x, y) not in MEAD and DM[(x, y)] >= 2 + ((x * 7 + y * 13) % 5 == 0)))}
        FOREST |= WALLC
        FOREST -= PATH_ALL | set(FIXED) | WSET | WALL | STAIR | CLEAR
    FOREST -= set(SEA)
    # ---- bosquets isoles (arbres entiers 2x2, jamais contre le chemin)
    gr = []; blockd = PATH_ALL | BUF | set(FIXED) | set(SEA) | FEAT | dil(WSET, 1)
    cands = [(x, y) for y in range(3, H - 3, 2) for x in range(3, W - 3, 2) if all((x + i, y + j) not in FOREST and (x + i, y + j) not in blockd and DM[(x + i, y + j)] >= 3 for i in range(2) for j in range(2)) and (x, y) not in CLEAR]
    rnd.shuffle(cands)
    for (x, y) in cands:
        if len(gr) >= (26 if L == 'Route16' else 30): break
        if any(max(abs(x - a), abs(y - b)) < 4 for (a, b) in gr): continue
        gr.append((x, y)); FOREST |= {(x + i, y + j) for i in range(2) for j in range(2)}
        for (dx, dy) in rnd.sample([(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2), (2, -2), (-2, 2)], 3):
            cs2 = {(x + dx + i, y + dy + j) for i in range(2) for j in range(2)}
            if rnd.random() < 0.55 and all(c in G_ok(W, H) and c not in FOREST and c not in blockd and DM[c] >= 3 for c in cs2): FOREST |= cs2
    G = {(x, y): (0x3000, 8 + (x & 1) + 8 * (y & 1)) for y in range(H) for x in range(W)}
    for c in PATH_SAND: G[c] = (0x3000, sand_id(lambda dx, dy, c=c: (c[0] + dx, c[1] + dy) in PATH_ALL or not (0 <= c[0] + dx < W and 0 <= c[1] + dy < H)))
    SPEC = {}
    for c in WSET - BR: SPEC[c] = ('pond', WATER[c]); G[c] = (0x400, 8)
    for c in HOLES: SPEC.pop(c, None); G[c] = (0x3000, 8 + (c[0] & 1) + 8 * (c[1] & 1))
    for c in BR: SPEC[c] = ('bridge', BRO[c]); G[c] = (0x3000, 8)
    for c in WALL: SPEC[c] = ('wall', int(c in ICE)); G[c] = (0x400, 8)
    for c in STAIR: SPEC[c] = ('stair',); G[c] = (0x3000, 8)
    TREEO, TREES = {}, []
    def put_tree(x, y):
        cs = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        for c, m in zip(cs, (28, 29, 20, 21)): G[c] = (0x400, m); TREEO[c] = (x, y)
        TREES.append((x, y))
    if L == 'Route16':
        for (x, y) in WALLU: put_tree(x, y)
    nofor2 = PATH_ALL | BUF | set(FIXED) | set(SEA) | FEAT | dil(WSET, 1) | CLEAR
    for (ox, oy) in ((0, 0), (1, 0), (0, 1), (1, 1)):             # reseau aligne d'abord, puis reseaux decales pour combler les trous (arbres toujours entiers)
        for uy in range(oy, H - 1, 2):
            for ux in range(ox, W - 1, 2):
                cs = [(ux, uy), (ux + 1, uy), (ux, uy + 1), (ux + 1, uy + 1)]
                if sum(c in FOREST for c in cs) >= (3 if (ox, oy) == (0, 0) else 4) and not any(c in nofor2 or c in TREEO for c in cs): put_tree(ux, uy)
    for c, v in FIXED.items(): G[c] = (v & 0xfc00, v & 0x3ff)
    for c, v in SEA.items(): G[c] = (v & 0xfc00, v & 0x3ff)
    return dict(W=W, H=H, G=G, SPEC=SPEC, PATH=PATH_ALL, BUF=BUF, MEAD=MEAD, TREEO=TREEO, FIXED=FIXED, SEA=SEA, FOREST=FOREST, WSET=WSET, BR=BR, WALL=WALL, STAIR=STAIR, GATES=GATES, CLEAR=CLEAR, PONDS=PONDS, FEAT=FEAT)

def decorate(L, B, rnd):
    W, H, G, PATH, BUF, SPEC = B['W'], B['H'], B['G'], B['PATH'], B['BUF'], B['SPEC']
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
    def plain(c): return c in G and c not in SPEC and G[c][0] == 0x3000 and G[c][1] in GRASS_B
    TALL = [c for c in B['MEAD'] if plain(c) and c not in BUF and noise(c[0] * 1.7, c[1] * 1.3) > -0.05]
    for c in TALL: G[c] = (0x3000, 13)
    EV = {}
    def near_path(c, dmin, dmax):
        ds = [max(abs(c[0] - p[0]), abs(c[1] - p[1])) for p in PATH if abs(p[0] - c[0]) <= dmax and abs(p[1] - c[1]) <= dmax]
        return bool(ds) and dmin <= min(ds) <= dmax
    def pick(target, dmin=2, dmax=2, avoid=(), rad=99):
        cand = [c for c in G if plain(c) and G[c][1] in GRASS_B and c not in EV.values() and 2 <= c[0] < W - 2 and 2 <= c[1] < H - 2 and near_path(c, dmin, dmax) and c in R0
                and all(max(abs(c[0] - a[0]), abs(c[1] - a[1])) >= 4 for a in avoid) and max(abs(c[0] - target[0]), abs(c[1] - target[1])) <= rad]
        if not cand: return None
        return min(cand, key=lambda c: (c[0] - target[0]) ** 2 + (c[1] - target[1]) ** 2 + rnd.random())
    return dict(R0=R0, reach=reach, blocked=blocked, plain=plain, pick=pick, EV=EV, start=start, nbs=nbs)

def place_all(L, B, D, rnd):
    W, H, G, PATH, BUF, MEAD, SPEC = B['W'], B['H'], B['G'], B['PATH'], B['BUF'], B['MEAD'], B['SPEC']
    R0, reach, blocked, plain, pick, EV, start = D['R0'], D['reach'], D['blocked'], D['plain'], D['pick'], D['EV'], D['start']
    mj = json.load(open('data/maps/%s/map.json' % L))
    def face(c):
        p = min(PATH, key=lambda q: (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2)
        dx, dy = p[0] - c[0], p[1] - c[1]
        return ('RIGHT' if dx > 0 else 'LEFT') if abs(dx) >= abs(dy) else ('DOWN' if dy > 0 else 'UP')
    placed = []
    trainers = [o for o in mj['object_events'] if o.get('trainer_type') == 'TRAINER_TYPE_NORMAL']
    if L == 'Route16':
        tg = [(43, 9), (38, 15), (26, 10), (18, 9), (14, 12), (24, 17), (15, 16), (11, 11)]
    else:
        tg = [(12, 8), (17, 12), (8, 19), (12, 28), (12, 36), (17, 43), (12, 49), (8, 56), (14, 61), (11, 65)]
    for o, t in zip(trainers, tg):
        c = pick(t, 2, 2, avoid=placed, rad=8)
        if c is None: c = pick(t, 2, 3, avoid=placed, rad=12)
        assert c, ('dresseur', o['script'], t)
        placed.append(c); EV[o['script']] = c
        o['x'], o['y'] = c; o['movement_type'] = 'MOVEMENT_TYPE_FACE_' + face(c); o['movement_range_x'] = 0; o['movement_range_y'] = 0
        o['trainer_sight_or_berry_tree_id'] = '2'
    keep_bg, signs = [], [b for b in mj['bg_events'] if b['type'] == 'sign']
    want = {'Route16_EventScript_RouteSign': (7, 16)} if L == 'Route16' else {'Route17_EventScript_RouteSign': (11, 70), 'Route17_EventScript_TrainerTips1': (10, 20), 'Route17_EventScript_TrainerTips2': (12, 40)}
    for b in signs:
        if b['script'] not in want: continue
        c = pick(want[b['script']], 2, 2, avoid=placed + list(EV.values()), rad=10) or pick(want[b['script']], 2, 4, avoid=placed + list(EV.values()), rad=16) or pick(want[b['script']], 1, 5, avoid=placed + list(EV.values()))
        assert c, b['script']
        G[c] = (0x400, 2); EV[b['script']] = c; b['x'], b['y'] = c; keep_bg.append(b)
    ART = {}
    # ---- cristaux voulus : bloc de la gorge, portail, ile, cercle d'amethyste
    def try_big(x, y, v, need_reach=True):
        cs = [(x + i, y + j) for j in range(2) for i in range(2)]
        if not all(plain(c) and c not in placed and c not in PATH and c not in ART for c in cs): return False
        if any(max(abs(c[0] - p[0]), abs(c[1] - p[1])) < 2 for c in cs for p in placed): return False
        sv = {c: G[c] for c in cs}
        for c in cs: G[c] = (0x400, G[c][1])
        if need_reach and not (reach(start, set(ART) | set(cs)) >= (R0 - set(ART) - set(cs) - {c for c in R0 if blocked(c)})):
            for c in cs: G[c] = sv[c]
            return False
        for q, c in enumerate(cs): ART[c] = (('b', v, q), sv[c][1])
        return True
    if L == 'Route16':
        ART[(31, 12)] = (('s', 1), G[(31, 12)][1]); G[(31, 12)] = (0x400, G[(31, 12)][1])
    nb = 0
    for k, (x, y) in enumerate(B['GATES']): nb += try_big(x, y, k % 3)
    if L == 'Route17':
        try_big(3, 39, 1, need_reach=False)                               # ile de cristal
        for k, th in enumerate((20, 80, 140, 200, 260, 320)):             # cercle d'amethyste autour de (18, 54)
            x = int(round(18 + 3.9 * math.cos(math.radians(th)))) - 1; y = int(round(54 + 3.0 * math.sin(math.radians(th)))) - 1
            try_big(x, y, k % 3)
    # ---- objets caches
    def secret(t, dmin=2):
        cand = [c for c in G if plain(c) and c in R0 and c not in ART and c not in placed and 2 <= c[0] < W - 2 and c not in PATH and min([99] + [max(abs(c[0] - p[0]), abs(c[1] - p[1])) for p in PATH if abs(p[0] - c[0]) <= 4 and abs(p[1] - c[1]) <= 4]) >= dmin]
        return min(cand, key=lambda c: (c[0] - t[0]) ** 2 + (c[1] - t[1]) ** 2)
    for b in mj['bg_events']:
        if b['type'] != 'hidden_item': continue
        if L == 'Route16': keep_bg.append(b); continue
        t = {'ITEM_RARE_CANDY': (18, 54), 'ITEM_FULL_RESTORE': (9, 40), 'ITEM_PP_UP': (9, 9), 'ITEM_MAX_REVIVE': (3, 27), 'ITEM_MAX_ELIXIR': (5, 61)}[b['item']]
        c = secret(t); placed.append(c); b['x'], b['y'] = c; keep_bg.append(b); EV[b['item']] = c
    mj['bg_events'] = keep_bg
    def dpath(c, lim=7):
        ds = [max(abs(c[0] - p[0]), abs(c[1] - p[1])) for p in PATH if abs(p[0] - c[0]) <= lim and abs(p[1] - c[1]) <= lim]
        return min(ds) if ds else 99
    BIGO = []
    nbig = 2 if L == 'Route16' else 5
    bc = [(x, y) for y in range(3, H - 4) for x in range(3, W - 5) if all(plain((x + i, y + j)) and (x + i, y + j) in R0 and (x + i, y + j) not in placed for i in range(2) for j in range(2))]
    rnd.shuffle(bc)
    for (x, y) in bc:
        if len(BIGO) >= nbig: break
        cs = [(x + i, y + j) for j in range(2) for i in range(2)]
        if not (2 <= min(dpath(c) for c in cs) and max(dpath(c) for c in cs) <= 6): continue
        if any(max(abs(x - o[0]), abs(y - o[1])) < 6 for o in BIGO) or any(max(abs(x - q[0]), abs(y - q[1])) < 3 for q in list(ART) + placed): continue
        if try_big(x, y, rnd.randrange(3)): BIGO.append((x, y))
    cand = [c for c in G if plain(c) and c in R0 and 2 <= c[0] < W - 2 and 2 <= c[1] < H - 2 and c not in PATH and c not in placed and c not in ART]
    rnd.shuffle(cand); lim = 22 if L == 'Route16' else 60; ncry = 0
    pts = placed + list(EV.values())
    for c in cand:
        if ncry >= lim: break
        d = dpath(c, 6)
        if d < 2 or d > 5: continue
        if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q in list(ART) + pts): continue
        ART[c] = (('s', rnd.randrange(3)), G[c][1]); G[c] = (0x400, G[c][1])
        if not (reach(start, set(ART)) >= (R0 - set(ART) - {c for c in R0 if blocked(c)})): del ART[c]; G[c] = (0x3000, G[c][1]); continue
        ncry += 1
    return mj, ART, EV, placed

def finalize(L, B, ART):
    W, H, G, TREEO, SPEC, WSET, WALL, STAIR, BR = B['W'], B['H'], B['G'], B['TREEO'], B['SPEC'], B['WSET'], B['WALL'], B['STAIR'], B['BR']
    ST = {(x, y): stage(L, x, y) for y in range(H) for x in range(W)}
    cl = lambda c: (min(max(c[0], 0), W - 1), min(max(c[1], 0), H - 1))
    isW = lambda c: cl(c) in WSET or cl(c) in BR
    out = []
    for y in range(H):
        for x in range(W):
            c = (x, y); fl, m = G[c]; st = ST[c]; base = 8 + (x & 1) + 8 * (y & 1); fb = snow_meta(0) if st == 0 else 8
            if c in ART:
                v, b0 = ART[c]; out.append((0x400) | art_meta(v, st, snow_meta(0 if (x + y) % 2 else 6) if st == 0 else b0)); continue
            if c in SPEC:
                sp = SPEC[c]; f = lambda dx, dy: (x + dx, y + dy)
                if sp[0] == 'pond':
                    qs = []
                    for q, (a, b, dg) in enumerate(((f(-1, 0), f(0, -1), f(-1, -1)), (f(1, 0), f(0, -1), f(1, -1)), (f(-1, 0), f(0, 1), f(-1, 1)), (f(1, 0), f(0, 1), f(1, 1)))):
                        ah, av, d2 = int(isW(a)), int(isW(b)), int(isW(dg))
                        qs.append(pond_q(q, ah, av, d2 if (ah and av) else 0, sp[1], (x * 3 + y * 5) % 3))
                    out.append(0x400 | mk(qs, 4, st, fb, 0)); continue
                if sp[0] == 'bridge':
                    o = sp[1]
                    if o == 'V': rA, rB = (x - 1, y) not in BR, (x + 1, y) not in BR
                    else: rA, rB = (x, y - 1) not in BR, (x, y + 1) not in BR
                    out.append(0x3000 | mk([bridge_q(q, o, rA, rB, (x + y) % 3) for q in range(4)], WALLP, st, fb, 0x20000000)); continue
                if sp[0] == 'stair':
                    eL, eR = (x - 1, y) not in STAIR, (x + 1, y) not in STAIR
                    out.append(0x3000 | mk([stair_q(q, eL, eR, 0 if (x, y - 1) not in STAIR else 1) for q in range(4)], WALLP, st, fb, 0x20000000)); continue
                if sp[0] == 'wall':
                    wl = cl((x - 1, y)) in WALL and (x - 1 >= 0 or True); wr = cl((x + 1, y)) in WALL
                    part = 0 if (x, y - 1) not in WALL else 1
                    out.append(0x400 | mk([wall_q(q, int(wl if q % 2 == 0 else wr), (x // 2) % 2, part, sp[1]) for q in range(4)], WALLP, st, fb, 0)); continue
            wat = (att(m) & 0x1ff) in WATER_B
            sto = ST[TREEO[c]] if c in TREEO else (1 if wat else st)
            if fl == 0x3000 and m in GRASS_B and sto == 0 and c not in TREEO: out.append(0x3000 | snow_meta(snow_var(x, y))); continue
            out.append(fl | variant(m, sto))
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
m16 = MJ['Route16']; m16['weather'] = 'WEATHER_SNOW'
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
for Lb in ('Route16', 'Route17'): open('data/layouts/%s/border.bin' % Lb, 'wb').write(struct.pack('<4H', 28, 29, 20, 21))      # hors carte : foret (et non plus la mer)
print('dont originales %d, variantes %d, art %d' % (NMT, len(VAR), len(ARTM))); print('metatuiles %d/384, tuiles %d/384' % (NMT + len(NEWE), NTL + len(NEWT)))

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
