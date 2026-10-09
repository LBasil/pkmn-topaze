# PYROPIA (ex-Argenta) v2 « retapee » : la cite du volcan, couleurs de BRAISE (cendre sombre, falaises rouges, lac de lave).
# Meme methode qu'Opanihrum : tuiles d'Emeraude importees (ici LAVARIDGE : falaises rouges, bassin, arene), recolorees, + art procedural
# (vents de braise, braseros, cairn de flamme). Secondaire COMPACTE (FireRed : 384 tuiles max).
# Lancer depuis la racine :  python3 docs/topaze/pyropia_town.py  puis  pyropia_events.py
import struct, json, random, sys, colorsys, collections, os, shutil, re
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
EM = '../pokeemerald/data/'
PRI = 'data/tilesets/primary/general_ember/'; SEC = 'data/tilesets/secondary/lavaridge_ember/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
LAV = struct.unpack('<400H', open(EM + 'layouts/LavaridgeTown/map.bin', 'rb').read())      # 20 x 20
def lv(x, y): return LAV[y * 20 + x]
rnd = random.Random(404)

# ------------------------------------------------------------------ palettes (teinte braise)
LAVA_PALS = {8}                                            # palette secondaire du bassin
def tint(pi, k, c):
    r, g, b = c
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.10 and l > 0.93: return c                    # blancs purs conserves
    if 190 <= h <= 260 and s > 0.25 and pi in LAVA_PALS:  # eau -> lave : sombre (rouge) -> clair (jaune)
        h = 2 + 34 * l; s = 1.0; l = min(0.58, 0.16 + l * 0.50)
    elif 190 <= h <= 260 and s > 0.3: return c            # toit bleu de la boutique
    elif 78 <= h <= 175:                                  # herbe / pins -> cendre sombre
        h = 20; s = min(0.20, s * 0.3); l = l * 0.55
    elif 25 <= h < 78 and s > 0.2:                        # sable -> terre brulee, un peu plus sombre et chaude
        h = max(16, h - 12); s = s * 0.72; l = l * 0.80
    rr, gg, bb = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
PALS_P = [[(c if k == 0 else tint(i, k, c)) for k, c in enumerate(readpal(EM + 'tilesets/primary/general/palettes/%02d.pal' % i))] for i in range(16)]
PALS_S = [[(c if k == 0 else tint(i, k, c)) for k, c in enumerate(readpal(EM + 'tilesets/secondary/lavaridge/palettes/%02d.pal' % i))] for i in range(16)]
PALS_P[6] = PALS_S[6]
LD = E.load('general', 'lavaridge')
LD = (LD[0], LD[1], [PALS_P[i] for i in range(6)] + [PALS_S[i] for i in range(6, 13)], LD[3], LD[4])

# ------------------------------------------------------------------ metatuiles : attributs + compaction du secondaire (+ variantes miroir)
patt = open(EM + 'tilesets/primary/general/metatile_attributes.bin', 'rb').read()
satt = open(EM + 'tilesets/secondary/lavaridge/metatile_attributes.bin', 'rb').read()
smt = open(EM + 'tilesets/secondary/lavaridge/metatiles.bin', 'rb').read()
hdr = open('include/constants/metatile_behaviors.h').read()
OKB = {int(m, 16) for m in re.findall(r'#define MB_\w+\s+(0x[0-9A-Fa-f]+)', hdr)}
WATER = {0x10, 0x11, 0x12, 0x15}
def conv(v, nowater=True):
    b, layer = v & 0xff, v >> 12
    if b not in OKB: b = 0
    if b in WATER and nowater: b = 0                       # le bassin est de la LAVE : pas de Surf
    a = b | (layer << 29)
    if b == 0x02: a |= 0x1000200
    elif b in WATER: a |= 0x22000400
    elif b == 0x13: a |= 0x2000600
    return a
def beh(m):
    a = patt[m * 2:m * 2 + 2] if m < 512 else satt[(m - 512) * 2:(m - 512) * 2 + 2]
    return struct.unpack('<H', a)[0] & 0xff
SEC_MAP = {}; SEC_ENT = []; SEC_ATT = []; CT = []
def ctile(t):
    if t not in CT: CT.append(t)
    return 640 + CT.index(t)
def remap(v, flip=False):
    m = v & 0x3ff
    if m < 512 and not flip: return v
    key = (m, flip)
    if key not in SEC_MAP:
        if m < 512:                                        # miroir d'une metatuile primaire : copie dans le secondaire
            e = list(struct.unpack('<8H', open(EM + 'tilesets/primary/general/metatiles.bin', 'rb').read()[m * 16:m * 16 + 16]))
            att = conv(struct.unpack('<H', patt[m * 2:m * 2 + 2])[0])
        else:
            e = list(struct.unpack('<8H', smt[(m - 512) * 16:(m - 512) * 16 + 16]))
            att = conv(struct.unpack('<H', satt[(m - 512) * 2:(m - 512) * 2 + 2])[0])
        out = []
        for q in e:
            t = q & 0x3ff
            nq = (q & ~0x3ff) | (ctile(t - 512) if t >= 512 else t)
            out.append(nq)
        if flip:
            for base in (0, 4):
                out[base], out[base + 1] = out[base + 1] ^ 0x400, out[base] ^ 0x400
                out[base + 2], out[base + 3] = out[base + 3] ^ 0x400, out[base + 2] ^ 0x400
        SEC_ENT.append(out); SEC_ATT.append(att); SEC_MAP[key] = 640 + len(SEC_ENT) - 1
    return (v & ~0x3ff) | SEC_MAP[key]

# ------------------------------------------------------------------ plan d'occupation
W, H = 48, 40
G = {}; OCC = {}
def walk(m): return 0x3000 | m
GRASS = 0x3000 | 1
for y in range(H):
    for x in range(W): G[(x, y)] = GRASS
def put(x, y, v): G[(x, y)] = v
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            assert 0 <= x + i <= W - 1 and 0 <= y + j <= H - 1, (name, x + i, y + j)
            assert (x + i, y + j) not in OCC, 'chevauchement %s avec %s en %s' % (name, OCC[(x + i, y + j)], (x + i, y + j))
            OCC[(x + i, y + j)] = name
# ---- cadre de falaises : nord (625 plateau / 628 front), ouest 626, est 626 en miroir, sud plateau ; portes sud x=22..23, est y=22..23
for x in range(W):
    put(x, 0, remap(0x400 | 625)); put(x, 1, remap(0x400 | 628))
    put(x, H - 1, remap(0x400 | 625)); put(x, H - 2, remap(0x400 | 625))
for y in range(2, H - 2):
    put(0, y, remap(0x400 | 626)); put(1, y, remap(0x400 | 626))
    put(W - 2, y, remap(0x400 | 626, True)); put(W - 1, y, remap(0x400 | 626, True))
for x in (22, 23):
    for y in (H - 2, H - 1): put(x, y, GRASS)
for y in (22, 23):
    for x in (W - 2, W - 1): put(x, y, GRASS)
for (x, y) in list(G):
    if x in (0, 1, W - 2, W - 1) or y in (0, 1, H - 2, H - 1): OCC[(x, y)] = 'cadre'
# ---- pins decoratifs (1 case, bloques) en bordure interieure
PINE = [198, 22, 14]
def pine(x, y): claim(x, y, 1, 1, 'pin'); put(x, y, remap(0x400 | PINE[(x * 3 + y) % 3]))

# ---- batiments : morceaux de Lavaridge poses au coin (dx, dy)
def chunk(x0, y0, cw, ch, dx, dy, name):
    claim(dx, dy, cw, ch, name); doors = []
    for j in range(ch):
        for i in range(cw):
            v = lv(x0 + i, y0 + j); put(dx + i, dy + j, remap(v))
            if 0x60 <= beh(v & 0x3ff) <= 0x6f: doors.append((dx + i, dy + j))
    return doors
D = {}
D['pool'] = chunk(2, 2, 6, 8, 4, 3, 'lac de lave')
D['gym'] = chunk(2, 11, 6, 5, 6, 14, 'arene')
D['center'] = chunk(8, 3, 4, 4, 14, 5, 'centre pokemon')
D['mart'] = chunk(14, 2, 4, 4, 36, 12, 'boutique')
D['museumA'] = chunk(11, 12, 4, 4, 27, 5, 'musee aile A')
D['museumB'] = chunk(15, 12, 4, 4, 31, 5, 'musee aile B')
D['house1'] = chunk(11, 12, 4, 4, 38, 29, 'maison 1')
D['house2'] = chunk(15, 12, 4, 4, 12, 29, 'maison 2')
D['hallE'] = chunk(11, 12, 4, 4, 28, 29, 'maison deco E')
D['hallW'] = chunk(15, 12, 4, 4, 5, 29, 'maison deco O')
D['hallN'] = chunk(11, 12, 4, 4, 38, 4, 'maison deco NE')
# maisons purement decoratives : la porte devient un mur (pas de warp -> pas de porte qui ne s'ouvre pas)
for k in ('hallE', 'hallW', 'hallN'):
    x, y = D[k][0]
    put(x, y - 1, remap(0x400 | 11)); put(x, y, remap(0x400 | 19)); D[k] = []
print('portes', {k: v for k, v in D.items() if k != 'pool'})
for k in ('pool',): D.pop(k)
DECO = ('hallE', 'hallW', 'hallN')
for k in list(D):
    assert D[k] or k in DECO, ('pas de porte', k)
DOORS = {k: v[0] for k, v in D.items() if v}
DECO_FRONT = {'hallE': (29, 32), 'hallW': (6, 32), 'hallN': (39, 7)}
json.dump(DOORS, open('/tmp/pyropia_doors.json', 'w'))

# ------------------------------------------------------------------ chemins (autotile du primaire 280..298), larges de 2 cases
PATH = set()
def pr(x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): PATH.add((x, y))
pr(22, 2, 23, H - 1)                    # avenue (sortie sud)
pr(3, 22, W - 1, 23)                    # rue est-ouest (sortie est)
pr(3, 33, 44, 34)                       # rue du sud
fr = lambda k: (DOORS[k][0], DOORS[k][1] + 1)
pr(fr('gym')[0], fr('gym')[1], fr('gym')[0] + 1, 21)
pr(fr('center')[0], fr('center')[1], fr('center')[0] + 1, 21)
pr(23, 10, 41, 11)                      # rue du musee
for k in ('museumA', 'museumB'): pr(fr(k)[0], fr(k)[1], fr(k)[0] + 1, 10)
pr(fr('mart')[0], fr('mart')[1], fr('mart')[0] + 1, 21)
for k in ('house1', 'house2'): pr(fr(k)[0], fr(k)[1], fr(k)[0] + 1, 33)
for (x, y) in PATH: assert (x, y) not in OCC or OCC[(x, y)] in ('cadre',), ('chemin sur un decor', (x, y), OCC.get((x, y)))
def path_id(x, y):
    N = (x, y - 1) in PATH or y == 0; S = (x, y + 1) in PATH or y == H - 1; Wn = (x - 1, y) in PATH or x == 0; E_ = (x + 1, y) in PATH or x == W - 1
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
for (x, y) in PATH:
    put(x, y, 0x3000 | path_id(x, y)); OCC[(x, y)] = 'chemin'
# les 4 cases d'angle de croisement internes : on garde 289 (centre) ; bord de carte ouvert aux portes

# ------------------------------------------------------------------ art procedural : vents de braise, braseros, cairn de flamme
used_pals = {q >> 12 for e in SEC_ENT for q in e}
FREE = [p for p in range(7, 13) if p not in used_pals]
print('palettes secondaires utilisees', sorted(used_pals), 'libres', FREE)
assert FREE, 'aucune palette libre pour l art'
ART_PAL = FREE[0]
gm = E.metatile(LD, 1).convert('RGB')
cnt = collections.Counter(gm.getdata()); gcols = [c for c, _ in cnt.most_common(4)]
while len(gcols) < 4: gcols.append(gcols[-1])
SH = tuple(int(c * 0.55) for c in min(gcols, key=sum))
PAL = [(0, 0, 0)] + gcols + [(22, 10, 12), (48, 36, 40), (84, 70, 70), (126, 108, 104), (150, 30, 14), (240, 100, 20), (255, 200, 60), (255, 244, 200), SH, (60, 40, 84), (206, 62, 18)]
# indices : 1-4 sol | 5 contour | 6 pierre sombre | 7 pierre | 8 pierre claire | 9 braise sombre | 10 orange | 11 jaune | 12 blanc chaud | 13 ombre | 14 obsidienne | 15 lueur
def newimg(w, h):
    im = Image.new('P', (w, h), 1); im.putpalette([c for p in PAL for c in p]); return im
def ground_bg(w, h):
    im = newimg(w, h); px = im.load(); g = gm.load()
    for y in range(h):
        for x in range(w):
            c = g[x % 16, y % 16]; px[x, y] = 1 + gcols.index(c) if c in gcols else 1
    return im
def flame(d, cx, base, h, w):
    d.polygon([(cx - w, base), (cx - w // 2, base - h // 2), (cx - 1, base - h), (cx + w // 3, base - h * 2 // 3), (cx + w, base)], fill=10)
    d.polygon([(cx - w // 2, base), (cx, base - h * 2 // 3), (cx + w // 2, base)], fill=11)
    d.polygon([(cx - 1, base), (cx, base - h // 3), (cx + 1, base)], fill=12)
def vent(var):
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    pts = [[(2, 12), (5, 9), (8, 10), (11, 6), (14, 4)], [(1, 5), (5, 7), (8, 6), (10, 10), (14, 12)]][var]
    d.line(pts, fill=5, width=3); d.line(pts, fill=9, width=1)
    for (x, y) in pts[1:-1]: d.point((x, y), fill=10)
    d.point(pts[2], fill=11); d.point((pts[2][0] + 1, pts[2][1] - 3), fill=15); d.point((pts[1][0] - 1, pts[1][1] - 2), fill=15)
    return im
def brazier():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((2, 11, 14, 15), fill=13)
    d.rectangle((7, 8, 8, 13), fill=6, outline=5); d.rectangle((4, 13, 11, 14), fill=7, outline=5)
    d.polygon([(3, 6), (12, 6), (10, 9), (5, 9)], fill=7, outline=5)
    flame(d, 7, 6, 6, 3)
    return im
def spire(var):
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((1, 11, 15, 15), fill=13)
    for (x, h) in ((4, 8), (8, 11), (11, 7)) if var == 0 else ((6, 10), (10, 6)):
        d.polygon([(x - 2, 13), (x, 13 - h), (x + 2, 13)], fill=14, outline=5); d.line([(x - 1, 12), (x, 14 - h)], fill=8)
    d.point((10, 7), fill=15)
    return im
def cairn():
    im = ground_bg(48, 48); d = ImageDraw.Draw(im)
    d.ellipse((1, 38, 47, 47), fill=13)
    d.rectangle((6, 34, 41, 44), fill=7, outline=5); d.rectangle((10, 28, 37, 34), fill=7, outline=5); d.rectangle((15, 23, 32, 28), fill=7, outline=5)
    d.line([(7, 35), (40, 35)], fill=8); d.line([(11, 29), (36, 29)], fill=8); d.line([(16, 24), (31, 24)], fill=8)
    for x in range(8, 40, 6): d.line([(x, 36), (x, 43)], fill=6)
    d.polygon([(12, 23), (24, 4), (36, 23)], fill=9, outline=5)
    flame(d, 24, 23, 20, 9)
    d.polygon([(18, 23), (24, 8), (30, 23)], fill=10); d.polygon([(21, 23), (24, 13), (27, 23)], fill=11); d.polygon([(23, 23), (24, 17), (25, 23)], fill=12)
    for (x, y) in ((8, 20), (38, 18), (14, 12), (34, 10), (20, 3), (30, 5)): d.point((x, y), fill=15)
    return im
ART_T = []
def add_tile(t):
    t = tuple(t)
    if t in ART_T: return ART_T.index(t)
    ART_T.append(t); return len(ART_T) - 1
ART_E = []
def meta(block):
    ents = []
    for q in range(4):
        x, y = (q % 2) * 8, (q // 2) * 8
        ents.append(('ART', add_tile(list(block.crop((x, y, x + 8, y + 8)).getdata()))))
    ART_E.append(ents); return ('ART_META', len(ART_E) - 1)
def slice_all(im, bw, bh): return {(i, j): meta(im.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))) for j in range(bh) for i in range(bw)}
CAIRN = slice_all(cairn(), 3, 3); VENT = [meta(vent(0)), meta(vent(1))]; BRAZ = meta(brazier()); SPIRE = [meta(spire(0)), meta(spire(1))]
def art1(x, y, m, name, blocked=True):
    claim(x, y, 1, 1, name); put(x, y, ('ARTRAW', m, 0x400 if blocked else 0x3000))
for (i, j), m in CAIRN.items():
    claim(18 + i, 16 + j, 1, 1, 'cairn'); put(18 + i, 16 + j, ('ARTRAW', m, 0x400))
for (x, y) in ((21, 4), (24, 4), (21, 8), (24, 8), (21, 14), (24, 14), (21, 19), (24, 19), (21, 26), (24, 26), (21, 30), (24, 30), (21, 36), (24, 36), (9, 21), (12, 21), (14, 24), (17, 24)):
    if (x, y) not in OCC: art1(x, y, BRAZ, 'brasero')
for (x, y, v) in ((6, 24, 0), (11, 26, 1), (17, 27, 0), (33, 17, 1), (30, 25, 0), (35, 24, 1), (42, 22 - 5, 0), (26, 14, 1), (17, 14, 0), (3, 12, 1), (44, 13, 0), (34, 36, 1), (8, 36, 0), (15, 36, 1), (41, 24, 0)):
    if not any((x + i, y + j) in OCC for i in (0,) for j in (0,)): art1(x, y, VENT[v], 'vent', blocked=False)
for (x, y, v) in ((3, 18, 0), (3, 25, 1), (44, 17, 0), (43, 24, 1), (20, 25, 0), (26, 24, 1), (44, 36, 0), (3, 36, 1), (20, 36, 1), (30, 36, 0)):
    if (x, y) not in OCC: art1(x, y, SPIRE[v], 'obsidienne')
# ---- pins en bordure
for (x, y) in [(2, yy) for yy in range(2, 12)] + [(45, yy) for yy in range(2, 21)] + [(xx, 37) for xx in range(2, 12)] + [(xx, 37) for xx in range(38, 46)] + [(45, yy) for yy in range(25, 38)] + [(2, yy) for yy in range(24, 37)]:
    if (x, y) not in OCC and (x, y) not in PATH: pine(x, y)
# ---- bosquets de pins calcines (hasard repete) dans les coins libres
def grove(x0, y0, x1, y1, n):
    k = 0; tries = 0
    while k < n and tries < 400:
        tries += 1; x = rnd.randint(x0, x1); y = rnd.randint(y0, y1)
        if all((x + i, y + j) not in OCC for i in (-1, 0, 1) for j in (-1, 0, 1)) and not any((x + i, y + j) in PATH for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2)): pine(x, y); k += 1
grove(3, 24, 11, 28, 7); grove(16, 25, 21, 28, 4); grove(3, 12, 5, 21, 4); grove(40, 16, 44, 21, 6); grove(40, 24, 44, 28, 5)
grove(14, 12, 21, 16, 4); grove(33, 24, 44, 27, 5); grove(24, 14, 34, 21, 5); grove(3, 35, 44, 36, 8); grove(24, 24, 27, 28, 3)
# ---- panneaux
SIGN = remap(0x400 | 3)
def sign(x, y): claim(x, y, 1, 1, 'panneau'); put(x, y, SIGN)
SIGNS = {'museum': (26, 9), 'police': (42, 24), 'gym': (7, 19), 'tips': (25, 35), 'city': (21, 35)}
for k, c in SIGNS.items(): sign(*c)

# ------------------------------------------------------------------ accessibilite / PNJ
NPC = {'lass': (13, 20), 'fatman': (26, 25), 'bugcatcher': (34, 19), 'hidden': (30, 20)}
def raw_blocked(c):
    v = G[c]
    if isinstance(v, tuple): return True
    return bool(v & 0xc00)
seen = {(22, 22)}; q = collections.deque([(22, 22)])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not raw_blocked(n): seen.add(n); q.append(n)
for k, c in NPC.items():
    assert c not in OCC or OCC[c] in ('chemin',), ('PNJ sur un decor', k, c, OCC.get(c))
    assert c in seen, ('PNJ inaccessible', k, c)
for k, (x, y) in DOORS.items(): assert (x, y + 1) in seen, ('porte inaccessible', k, (x, y))
for c in ((22, H - 1), (23, H - 1), (W - 1, 22), (W - 1, 23)): assert c in seen, c
for k, c in SIGNS.items(): assert (c[0], c[1] + 1) in seen or (c[0], c[1] - 1) in seen or (c[0] - 1, c[1]) in seen or (c[0] + 1, c[1]) in seen, ('panneau inaccessible', k)
json.dump(NPC, open('/tmp/pyropia_npc.json', 'w')); json.dump({k: list(v) for k, v in SIGNS.items()}, open('/tmp/pyropia_signs.json', 'w'))

# ------------------------------------------------------------------ ecriture des tilesets
NT = len(CT)
assert NT + len(ART_T) <= 384, ('trop de tuiles', NT, len(ART_T))
art_ids = {}
for k, ents in enumerate(ART_E):
    SEC_ENT.append([(640 + NT + t) | (ART_PAL << 12) for (_, t) in ents] + [0, 0, 0, 0]); SEC_ATT.append(0)
    art_ids[k] = 640 + len(SEC_ENT) - 1
assert len(SEC_ENT) <= 384, len(SEC_ENT)
for k, v in list(G.items()):
    if isinstance(v, tuple):
        assert v[1][0] == 'ART_META'; G[k] = v[2] | art_ids[v[1][1]]
src_png = Image.open(EM + 'tilesets/secondary/lavaridge/tiles.png')
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
writepal(SEC + 'palettes/%02d.pal' % ART_PAL, PAL)
shutil.copy(EM + 'tilesets/primary/general/tiles.png', PRI + 'tiles.png')
shutil.copy(EM + 'tilesets/primary/general/metatiles.bin', PRI + 'metatiles.bin')
open(PRI + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', conv(struct.unpack('<H', patt[i * 2:i * 2 + 2])[0])) for i in range(len(patt) // 2)))
def add(path, text):
    s_ = open(path).read()
    if 'GeneralEmber' not in s_: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralEmber[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralEmber[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_LavaridgeEmber[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_LavaridgeEmber[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralEmber[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralEmber[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_LavaridgeEmber[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_LavaridgeEmber[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
def hdr_(n, sec): return """
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
""" % (n, 'TRUE' if sec else 'FALSE', n, n, n, n)
add('src/data/tilesets/headers.h', hdr_('GeneralEmber', False) + hdr_('LavaridgeEmber', True))
# ------------------------------------------------------------------ carte
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/PewterCity/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
b = remap(0x400 | 625)
open('data/layouts/PewterCity/border.bin', 'wb').write(struct.pack('<4H', b, b, b, b))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_PEWTER_CITY':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralEmber', secondary_tileset='gTileset_LavaridgeEmber')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
blocked = {(x, y) for y in range(H) for x in range(W) if (g[y * W + x] & 0xc00) or ((g[y * W + x] >> 12) == 1)}
json.dump({'w': W, 'h': H, 'blocked': [list(c) for c in sorted(blocked)]}, open('/tmp/pyropia_col.json', 'w'))
print('pyropia: tuiles', NT, '+', len(ART_T), 'art ; metatuiles', len(SEC_ENT), '; palette art', ART_PAL)
