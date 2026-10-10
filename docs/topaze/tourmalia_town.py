# TOURMALIA (ex-Azuria) : la cite-foret du Gardien (arene Insecte/Plante de Sylvestre), couleurs de la TOURMALINE (vert profond, coeur rose).
# Meme methode que Opanihrum : decors d'Emeraude (ici Vergazon = FORTREE : cabanes sur pilotis, ponts de corde, grande foret) recopies
# dans un jeu de tuiles secondaire COMPACTE (FireRed : 384 tuiles max) + art procedural (cristaux de tourmaline, monolithe, terrier, grotte).
# Lancer depuis la racine du depot :  python3 docs/topaze/tourmalia_town.py  puis  tourmalia_events.py
import struct, json, random, sys, collections, os, shutil, re, math
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
EM = '../pokeemerald/data/'
PRI = 'data/tilesets/primary/general_tourmaline/'; SEC = 'data/tilesets/secondary/fortree_tourmaline/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
FT = struct.unpack('<800H', open(EM + 'layouts/FortreeCity/map.bin', 'rb').read())      # 40 x 20
def fr(x, y): return FT[y * 40 + x]
rnd = random.Random(2026)

def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
PALS_P = [readpal(EM + 'tilesets/primary/general/palettes/%02d.pal' % i) for i in range(16)]
PALS_S = [readpal(EM + 'tilesets/secondary/fortree/palettes/%02d.pal' % i) for i in range(16)]
PALS_P[6] = PALS_S[6]                                       # FireRed : palette 6 = primaire
LD = E.load('general', 'fortree')

# ------------------------------------------------------------------ metatuiles : conversion attributs + compaction du secondaire
patt = open(EM + 'tilesets/primary/general/metatile_attributes.bin', 'rb').read()
satt = open(EM + 'tilesets/secondary/fortree/metatile_attributes.bin', 'rb').read()
smt = open(EM + 'tilesets/secondary/fortree/metatiles.bin', 'rb').read()
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
def ents_of(m):
    """8 entrees (tuiles deja remappees) d'une metatuile d'Emeraude"""
    if m < 512: return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16]))
    return list(SEC_ENT[(remap(0x3000 | m) & 0x3ff) - 640])

# ------------------------------------------------------------------ plan
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
# l'allee du Gardien (rival : voie droite x 22..24, y 0..9)
rect(22, 0, 24, 13)
# clairieres (prairie) et sentiers (sol pointille) : la ville est faite de petites clairieres reliees par des sentiers, dans une grande foret
blob(24, 18, 6.8, 4.2, 11)                                  # place du monolithe
blob(30, 14, 5.4, 4.0, 31)                                  # parvis de l'arene
blob(14, 16, 4.6, 4.0, 32)                                  # clairiere du Centre
blob(35, 23, 4.6, 3.4, 33)                                  # clairiere de la boutique
trail([(0, 20), (4, 21), (9, 20), (14, 19), (18, 19)], 1, 12)         # sortie ouest (Route 4)
rect(0, 19, 2, 22)
trail([(14, 9), (18, 8), (21, 9)], 1, 15)
trail([(8, 8), (6, 12), (5, 16), (4, 20)], 1, 13)           # sentier de la berge ouest : pied de l'echelle de la cabane 1 -> entree ouest          # sous les cabanes (ouest)
trail([(25, 9), (29, 8), (34, 9), (41, 9)], 1, 16)          # sous les cabanes (est)
blob(40, 10, 3.2, 3.2, 17)                                  # recoin du terrier
rect(8, 7, 9, 7, False); rect(28, 7, 29, 7, False); rect(35, 7, 36, 7, False)  # pied des echelles
trail([(30, 19), (36, 19), (42, 18), (47, 18)], 1, 18); rect(36, 18, 40, 19); rect(42, 18, 47, 19)   # sortie est (Route 9) ; goulet en x=41 (y=19 seul)
trail([(24, 22), (25, 28), (24, 33)], 1, 19); rect(24, 30, 25, 31); rect(24, 32, 24, 35)
rect(22, 36, 27, 39); rect(22, 34, 26, 35)
for c in [(22, 34), (23, 34), (25, 34), (26, 34), (22, 35), (23, 35), (25, 35), (26, 35)]: OPEN.discard(c)          # goulet de l'arbre a couper : 1 case en (24,35)
trail([(30, 22), (34, 25)], 1, 20)
trail([(36, 26), (39, 29), (41, 31)], 1, 24); blob(41, 32, 4.2, 3.4, 25)      # bosquet de tourmaline (sud-est)
trail([(14, 20), (14, 25), (19, 27), (19, 33)], 1, 22); blob(10, 36, 9.5, 2.6, 23); trail([(19, 33), (18, 36), (14, 36)], 1, 26)       # sentier du sud-ouest + clairiere des cabanes basses
# ---- batiments (copie brute des morceaux de Vergazon)
def chunk(x0, y0, cw, ch, dx, dy, name):
    claim(dx, dy, cw, ch, name); doors = []
    for j in range(ch):
        for i in range(cw):
            v = fr(x0 + i, y0 + j)
            if 0x60 <= beh(v & 0x3ff) <= 0x6f: doors.append((dx + i, dy + j)); v &= ~0xc00
            put(dx + i, dy + j, remap(v)); OPEN.discard((dx + i, dy + j))
    return doors
D = {}
D['th1'] = chunk(8, 1, 5, 6, 6, 1, 'cabane 1')
D['th2'] = chunk(15, 1, 5, 6, 15, 1, 'cabane 2')
D['th3'] = chunk(23, 1, 5, 6, 27, 1, 'cabane 3')
D['th4'] = chunk(30, 0, 5, 7, 34, 0, 'cabane 4')
D['th5'] = chunk(10, 11, 5, 6, 3, 28, 'cabane 5')
D['th6'] = chunk(35, 11, 5, 6, 14, 28, 'cabane 6')
D['center'] = chunk(4, 3, 4, 4, 12, 13, 'centre')
D['mart'] = chunk(3, 11, 4, 4, 33, 20, 'boutique')
D['gym'] = chunk(19, 7, 6, 5, 27, 12, 'arene')
print('portes detectees', D)
# ponts de corde (rangee de plateforme = y 4 en haut, y 31 en bas)
def bridge(x0, x1, y):
    for x in range(x0, x1 + 1): claim(x, y, 1, 1, 'pont'); put(x, y, remap(fr(13, 4)))
bridge(11, 14, 4); bridge(32, 33, 4); bridge(8, 13, 31)
# ---- zones sous les batiments : les pieds des echelles / portes doivent etre ouverts
LADDER = {'th1': (8, 7), 'th3': (29, 7), 'th4': (36, 7), 'th5': (5, 34), 'th6': (16, 34)}
for k, c in LADDER.items(): OPEN.add(c); WAY.add(c)
for k in ('center', 'mart', 'gym'):
    for (x, y) in D[k]:
        for a in (-1, 0, 1):
            for b in (1, 2):
                if (x + a, y + b) not in OCC: OPEN.add((x + a, y + b)); WAY.add((x + a, y + b))
OPEN -= set(OCC)
json.dump({k: v for k, v in D.items()}, open('/tmp/tourmalia_doors.json', 'w'))
# ---- cases ouvertes : sol (sentiers = pointille ; prairie = herbe unie avec des plaques pointillees)
GROUND = {}
for (x, y) in sorted(OPEN):
    if (x, y) in OCC: continue
    gid = GRASS
    GROUND[(x, y)] = gid; G[(x, y)] = remap(0x3000 | gid)
# ---- foret : arbres de bordure (fond herbe) pres des zones ouvertes, grands arbres au coeur
def is_open(c): return c in OPEN or (c in OCC and not (G[c] & 0xc00))
for y in range(H):
    for x in range(W):
        c = (x, y)
        if c in OPEN or c in OCC: continue
        edge = any(((x + a, y + b) in OPEN) for a in (-1, 0, 1) for b in (-1, 0, 1))
        m = rnd.choice((587, 588, 14, 15)) if edge else rnd.choice((198, 199, 198, 199, 198))
        G[c] = remap(0x400 | m)

# ------------------------------------------------------------------ art : cristaux de tourmaline (couche haute transparente sur le sol)
ART_PAL = 7
used = {q >> 12 for e in SEC_ENT for q in e}
assert ART_PAL not in used and 8 not in used, used
PAL = [(0, 0, 0), (8, 24, 20), (18, 84, 60), (34, 140, 92), (100, 208, 140), (188, 246, 208), (250, 255, 250), (140, 30, 86), (222, 72, 138),
       (255, 146, 194), (255, 214, 232), (22, 60, 44), (92, 64, 40), (126, 130, 126), (70, 76, 74), (255, 232, 136)]
# 1 contour | 2 vert profond | 3 vert | 4 vert clair | 5 menthe | 6 blanc | 7 rose fonce | 8 rose | 9 rose clair | 10 rose pale | 11 ombre | 12 terre | 13 pierre | 14 pierre sombre | 15 or
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
def monolith():
    im = newimg(48, 48); d = ImageDraw.Draw(im)
    shadow(d, 2, 38, 46, 48)
    for (a, b, c, e) in ((6, 38, 12, 43), (33, 40, 41, 46), (14, 41, 22, 46), (27, 41, 35, 47)): d.rectangle((a, b, c, e), fill=13, outline=1)
    d.line([(7, 39), (11, 39)], fill=15); d.line([(34, 41), (40, 41)], fill=14)
    prism(d, 10, 42, 9, 22); prism(d, 38, 43, 9, 26); prism(d, 17, 43, 6, 14); prism(d, 31, 44, 7, 17)
    prism(d, 24, 44, 15, 41)
    for (x, y) in ((22, 6), (23, 5), (26, 12), (9, 24), (37, 22), (24, 20)): d.point((x, y), fill=15)
    return im
def hole():
    im = newimg(16, 32); d = ImageDraw.Draw(im)
    d.ellipse((0, 4, 15, 30), fill=12, outline=1); d.ellipse((2, 7, 13, 27), fill=14); d.ellipse((3, 9, 12, 25), fill=1)
    for (x, y) in ((1, 8), (14, 12), (0, 22), (15, 26)): d.rectangle((x, y, x + 1, y + 1), fill=13)
    for (x, y) in ((4, 5), (11, 6), (2, 17), (13, 20)): d.point((x, y), fill=2)
    d.point((8, 17), fill=8)
    return im
def grotto():
    im = newimg(48, 48); d = ImageDraw.Draw(im)
    shadow(d, 0, 41, 47, 48)
    d.polygon([(1, 46), (3, 24), (10, 11), (24, 6), (38, 11), (45, 24), (47, 46)], fill=14, outline=1)
    d.polygon([(4, 44), (6, 25), (12, 14), (24, 9), (24, 44)], fill=13)
    for (x, y, w_) in ((8, 20, 4), (14, 12, 5), (36, 16, 4), (40, 28, 3), (30, 10, 3), (6, 34, 3)): d.rectangle((x, y, x + w_, y + 1), fill=2)
    d.pieslice((17, 24, 31, 52), 180, 360, fill=1); d.rectangle((17, 38, 30, 47), fill=1)
    for (x, y) in ((16, 36), (31, 35)): d.rectangle((x, y, x + 1, y + 11), fill=13)
    d.point((24, 40), fill=8); d.point((23, 41), fill=9); d.point((25, 42), fill=7)
    prism(d, 7, 34, 6, 12); prism(d, 41, 36, 6, 14); prism(d, 13, 14, 5, 9); prism(d, 34, 12, 5, 8)
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

# ------------------------------------------------------------------ goulets exacts (forces de passage)
for y in (30, 31):
    for x in range(21, 31):
        if x not in (24, 25): OPEN.discard((x, y)); WAY.discard((x, y))
for x in range(21, 31):
    if x != 24: OPEN.discard((x, 35)); WAY.discard((x, 35))
for y in (32, 33, 34):
    for x in range(21, 29):
        if x not in (23, 24, 25) and (x, y) in OPEN and x >= 21: OPEN.discard((x, y)); WAY.discard((x, y))
rect(26, 29, 27, 29)                      # niche (Spectrum/Ronflex hors du passage)
for y in (40,):
    pass
for x in (40, 41, 42):                      # goulet de l'est : en x=41 seule la rangee y=19 reste ouverte
    for y in range(14, 25):
        if (x, y) not in ((40, 18), (40, 19), (41, 19), (42, 18), (42, 19)): OPEN.discard((x, y)); WAY.discard((x, y))
for c in list(OPEN):
    if c in OCC: OPEN.discard(c)
# ------------------------------------------------------------------ EAU : ruisseau venu du nord (sous le pont de corde des cabanes hautes) -> etang (le ruisseau passe sous le pont de corde)
def seg_r(px, py, a, b):
    ax, ay, ar = a; bx, by, br = b; dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / float(dx * dx + dy * dy or 1)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy)) - (ar + (br - ar) * t)
STREAM = [(12.5, -1.0, 1.9), (12.5, 2.5, 1.8), (12.5, 6.0, 1.7), (11.6, 9.0, 1.5), (10.0, 12.0, 1.4), (9.0, 15.0, 1.5), (8.8, 18.0, 1.5), (9.0, 21.5, 1.5), (8.0, 24.5, 1.4), (8.8, 27.0, 1.6), (10.4, 29.5, 1.6),
          (10.6, 32.0, 1.6), (11.4, 34.0, 1.7), (11, 35.5, 1.9)]
rw = random.Random(77)
WATERC = set()
for y in range(0, H - 1):
    for x in range(1, W - 1):
        d = min(seg_r(x, y, a, b) for a, b in zip(STREAM, STREAM[1:]))
        if d <= rw.uniform(-0.1, 0.12): WATERC.add((x, y))
for (cx, cy, rx, ry) in ((10, 37, 2.8, 1.7), (12.6, 36.6, 2.4, 1.5)):                # etang
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 and 1 <= x < W - 1 and 1 <= y < H - 1: WATERC.add((x, y))
ROPEC = {c for c in WATERC if OCC.get(c) == 'pont'}
WATERC = {c for c in WATERC if c not in OCC or c in ROPEC}
BRIDGEC = set()
for (r0, r1) in ((20, 21), (33, 34)):
    xs = [c[0] for c in WATERC if r0 <= c[1] <= r1 and c not in ROPEC]
    for y in range(r0, r1 + 1):
        for x in range(min(xs), max(xs) + 1):
            if (x, y) not in OCC: BRIDGEC.add((x, y)); WATERC.add((x, y))
WATERC = {c for c in WATERC if c in ROPEC or c in BRIDGEC or c not in WAY}      # un sentier ne finit pas dans l'eau (hors ponts)
WATERONLY = WATERC - ROPEC - BRIDGEC
WAT = WATERC
BANK = {(x + a, y + b) for (x, y) in WATERC for a in (-1, 0, 1) for b in (-1, 0, 1)} - WATERC
BANK = {c for c in BANK if c not in OCC and 1 <= c[0] < W - 1 and 1 <= c[1] < H - 1}
for c in WATERONLY | BRIDGEC: OPEN.discard(c)
for c in BANK: OPEN.add(c)
for x in range(8, 14):                              # le pont de corde (altitude 4) ne se rejoint que par les echelles : pas de sol libre contre lui
    for y in (30, 32):
        if (x, y) not in WATERC and (x, y) not in OCC: OPEN.discard((x, y)); WAY.discard((x, y))
for c in WATERONLY | BRIDGEC: claim(c[0], c[1], 1, 1, 'eau')
WATER_ATT = conv(struct.unpack('<H', patt[0xd1 * 2:0xd1 * 2 + 2])[0])             # comportement eau, couche 'couvrante' (on peut surfer, le sprite passe au-dessus)
import numpy as np
from PIL import ImageFilter
WPAL_ID = 8
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
    k = ((c[0], c[1] - 1) in BRIDGEC, (c[0], c[1] + 1) in BRIDGEC, c[0] % 4)
    if k not in PCACHE:
        t4 = slice_tiles(plank_img(c)); SEC_ENT.append([('B', t) for t in t4] + list(EMPTY_TOP)); SEC_ATT.append(0); PCACHE[k] = len(SEC_ENT) - 1
    G[c] = 0x3000 | (640 + PCACHE[k])
ALLW = {(i, j) for i in range(-2, 3) for j in range(-2, 3)}
WIMG_FULL = slice_tiles(water_img((100, 100), {(100 + i, 100 + j) for i, j in ALLW}))
for c in sorted(ROPEC):                                                                          # pont de corde au-dessus du ruisseau : fond = eau, haut = cordes
    base = G[c]; i = (base & 0x3ff) - 640
    SEC_ENT.append([('B', t) for t in WIMG_FULL] + list(SEC_ENT[i][4:])); SEC_ATT.append(SEC_ATT[i]); G[c] = (base & ~0x3ff) | (640 + len(SEC_ENT) - 1)
# ------------------------------------------------------------------ sol + foret definitifs (apres goulets)
for (x, y) in sorted(OPEN):
    if (x, y) in OCC: continue
    if (x, y) not in GROUND:
        gid = GRASS
        GROUND[(x, y)] = gid; G[(x, y)] = remap(0x3000 | gid)
for (x, y) in list(G):
    c = (x, y)
    if c in OPEN or c in OCC: continue
    edge = any(((x + a, y + b) in OPEN) for a in (-1, 0, 1) for b in (-1, 0, 1))
    m = rnd.choice((587, 588, 14, 15)) if edge else rnd.choice((198, 199, 198, 199, 198))
    G[c] = remap(0x400 | m)
for c in list(GROUND):
    if c not in OPEN: del GROUND[c]

# ------------------------------------------------------------------ placement de l'art
MONO = monolith(); HOLE = hole(); GROT = grotto()
rect(22, 18, 24, 20, False)
art_block(MONO, 3, 3, 22, 18, 'monolithe')
GROT_DOOR = (1, 1)                                     # grotte retiree (v6) : la porte de Cerulean Cave reste declaree mais hors d'atteinte
art_block(HOLE, 1, 2, 41, 10, 'terrier'); HOLE_CELLS = [(41, 10), (41, 11)]
for c in list(OPEN):
    pass
# cristaux le long de l'allee (a la place des arbres de bordure)
for k, y in enumerate((2, 4, 6, 8, 10)):
    for x in (21, 25):
        if (x, y) not in OCC and (x, y) not in OPEN:
            claim(x, y, 1, 1, 'cristal'); ARTPLACE[(x, y)] = (slice_tiles(SM[(k + x) % 3]), GRASS)
def crystals(cells, prob, tag):
    placed = []
    for c in cells:
        if c in OCC or c not in OPEN or c in WAY or rnd.random() > prob: continue
        if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 2 for q in placed): continue
        placed.append(c); claim(c[0], c[1], 1, 1, tag); ARTPLACE[c] = (slice_tiles(SM[rnd.randrange(3)]), GROUND[c])
    return placed
# cases a garder libres : abords de portes, goulets
KEEP = set()
for k, ds in D.items():
    for (x, y) in ds:
        for a in range(-2, 3):
            for b in range(-1, 3): KEEP.add((x + a, y + b))
for a in range(-2, 3):
    for b in range(1, 3): KEEP.add((4 + a, 9 + b))
for c in [(24, 30), (25, 30), (24, 31), (25, 31), (26, 29), (27, 29), (24, 32), (24, 33), (24, 34), (24, 35), (41, 19), (40, 18), (40, 17), (40, 19), (42, 19), (39, 9), (40, 9), (40, 10), (40, 11), (39, 11)]: KEEP.add(c)
GROVE = [c for c in sorted(OPEN) if c[0] >= 36 and c[1] >= 27]
crystals([c for c in sorted(OPEN) if c not in KEEP and c not in GROVE and 4 <= c[0] <= 45], 0.045, 'cristal')
crystals([c for c in GROVE if c not in KEEP], 0.22, 'cristal')
# palmiers (3x3, a l'orée de la foret)
def palm(x, y):
    cells = [(x + i, y + j) for i in range(3) for j in range(3)]
    if any(c in OCC or c in OPEN or c[0] < 1 or c[1] < 1 or c[0] > W - 2 or c[1] > H - 2 for c in cells): return False
    if not any(((x + i, y + j) in OPEN) for i in range(-1, 4) for j in range(-1, 4)): return False
    chunk(1, 1, 3, 3, x, y, 'palmier'); return True
n_ = 0
for _ in range(400):
    if n_ >= 9: break
    if palm(rnd.randint(2, W - 5), rnd.randint(2, H - 5)): n_ += 1
print('palmiers', n_)

# ------------------------------------------------------------------ PNJ, panneaux, objets (positions verifiees)
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
NPC['policeman'] = (40, 18); NPC['policeman_block'] = (41, 19)
NPC['grunt'] = (40, 10); NPC['gtop'] = (40, 9); NPC['gbottom'] = (40, 11)
NPC['slowbro'] = (26, 29); NPC['lass'] = (27, 29); NPC['slowbro_block'] = (24, 31); NPC['lass_block'] = (25, 31)
NPC['guard'] = (1, 2); NPC['cuttree'] = (24, 35); NPC['rival'] = (22, 0)
NPC['boy'] = pick((18, 21)); NPC['balding'] = pick((9, 21)); NPC['youngster'] = pick((35, 21)); NPC['woman'] = pick((7, 35))
NPC['hidden'] = pick((16, 9), r=12)
SIGNS = {'city': pick((3, 18)), 'gym': pick((33, 17)), 'bike': pick((7, 35)), 'tips': pick((21, 33), r=12)}
for k, c in SIGNS.items():
    claim(c[0], c[1], 1, 1, 'panneau: ' + k)
for k in ('policeman', 'policeman_block', 'grunt', 'gtop', 'gbottom', 'slowbro', 'lass', 'slowbro_block', 'lass_block', 'cuttree', 'rival'):
    assert NPC[k] not in ARTPLACE, (k, NPC[k])
# ------------------------------------------------------------------ resolution art -> metatuiles, valeurs brutes
for c, (t4, gid) in sorted(ARTPLACE.items()):
    mid = 640 + art_meta(t4, gid)
    walk = (c == GROT_DOOR) or (c in HOLE_CELLS)
    G[c] = (0x3000 if walk else 0x400) | mid
for k, c in SIGNS.items(): G[c] = remap(0x400 | 3)
# ---- sentiers : sable d'Emeraude (autotuile, comme la Route 4 Est) ; prairies : fleurs
PATHC = {c for c in WAY if c in OPEN and c not in OCC and c not in ARTPLACE and c not in WATERONLY and c not in BRIDGEC and not (G[c] & 0xc00)}
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
    if (x, y) in HOLE_CELLS: continue
    G[(x, y)] = remap(0x3000 | path_id(x, y))
for (x, y) in sorted(OPEN):
    c = (x, y)
    if c in PATHC or c in OCC or c in ARTPLACE or c in KEEP or c in WATERONLY or c in BRIDGEC or (G[c] & 0xc00): continue
    if GROUND.get(c) == GRASS and rnd.random() < 0.10: G[c] = remap(0x3000 | 4)

for c in HOLE_CELLS: GROUND[c] = 609
def raw_blocked(c): return bool(G[c] & 0xc00) or c in WATERONLY
# ------------------------------------------------------------------ accessibilite
seen = {(23, 0)}; q = collections.deque([(23, 0)])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not raw_blocked(n): seen.add(n); q.append(n)
for k, ds in D.items():
    for c in ds: assert c in seen, ('porte inaccessible', k, c)
for name, c in (('terrier1', HOLE_CELLS[0]), ('terrier2', HOLE_CELLS[1])): assert c in seen, (name, c)
for k in ('policeman', 'policeman_block', 'grunt', 'gtop', 'gbottom', 'slowbro', 'lass', 'slowbro_block', 'lass_block', 'cuttree', 'rival', 'boy', 'balding', 'youngster', 'woman', 'hidden'):
    assert NPC[k] in seen, ('PNJ inaccessible', k, NPC[k])
EXITS = {'west': [(0, y) for y in (19, 20, 21, 22)], 'north': [(x, 0) for x in (22, 23, 24)], 'east': [(47, 18), (47, 19)], 'south': [(x, H - 1) for x in (22, 23, 24, 25)]}
for k, cs in EXITS.items():
    for c in cs: assert c in seen, ('sortie inaccessible', k, c)
for k, c in SIGNS.items(): assert any(((c[0] + a, c[1] + b) in seen) for a, b in ((0, 1), (0, -1), (1, 0), (-1, 0))), ('panneau inaccessible', k)
# forces de passage : sans le policier / la cabane de Spectrum, pas d'acces a l'est / au sud
def flood_without(cells):
    sn = {(23, 0)}; qq = collections.deque([(23, 0)])
    while qq:
        c = qq.popleft()
        for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in sn and n not in cells and not raw_blocked(n): sn.add(n); qq.append(n)
    return sn
sn = flood_without({NPC['policeman_block']})
assert (47, 18) not in sn and (47, 19) not in sn, 'l est est atteignable sans passer le policier'
sn = flood_without({NPC['slowbro_block'], NPC['lass_block']})
assert (24, H - 1) not in sn, 'le sud est atteignable sans passer Spectrum/la fille'
sn = flood_without({NPC['cuttree']})
assert (24, H - 1) not in sn
print('portes, PNJ, sorties, goulets OK ; cases accessibles', len(seen))
json.dump(NPC, open('/tmp/tourmalia_npc.json', 'w')); json.dump(SIGNS, open('/tmp/tourmalia_signs.json', 'w'))
json.dump({'grot_door': GROT_DOOR, 'hole': HOLE_CELLS}, open('/tmp/tourmalia_misc.json', 'w'))
# ------------------------------------------------------------------ ecriture des tilesets
NT = len(CT)
assert NT + len(ART_T) <= 384, ('trop de tuiles', NT, len(ART_T))
assert len(SEC_ENT) <= 384, len(SEC_ENT)
SEC_ENT = [[((640 + NT + q[1]) | ((ART_PAL if q[0] == 'A' else WPAL_ID) << 12)) if isinstance(q, tuple) else q for q in e] for e in SEC_ENT]
src_png = Image.open(EM + 'tilesets/secondary/fortree/tiles.png')
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
def add(path, text):
    s = open(path).read()
    if 'GeneralTourmaline' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralTourmaline[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralTourmaline[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_FortreeTourmaline[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_FortreeTourmaline[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralTourmaline[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralTourmaline[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_FortreeTourmaline[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_FortreeTourmaline[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralTourmaline =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralTourmaline,
    .palettes = gTilesetPalettes_GeneralTourmaline,
    .metatiles = gMetatiles_GeneralTourmaline,
    .metatileAttributes = gMetatileAttributes_GeneralTourmaline,
    .callback = NULL,
};

const struct Tileset gTileset_FortreeTourmaline =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_FortreeTourmaline,
    .palettes = gTilesetPalettes_FortreeTourmaline,
    .metatiles = gMetatiles_FortreeTourmaline,
    .metatileAttributes = gMetatileAttributes_FortreeTourmaline,
    .callback = NULL,
};
''')
# ------------------------------------------------------------------ carte
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/CeruleanCity/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/CeruleanCity/border.bin', 'wb').write(struct.pack('<4H', 0x400 | 198, 0x400 | 199, 0x400 | 199, 0x400 | 198))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_CERULEAN_CITY':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralTourmaline', secondary_tileset='gTileset_FortreeTourmaline')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
blocked = {(x, y) for y in range(H) for x in range(W) if g[y * W + x] & 0xc00} | WATERONLY
json.dump({'w': W, 'h': H, 'blocked': [list(c) for c in sorted(blocked)]}, open('/tmp/tourmalia_col.json', 'w'))
print('tourmalia: tuiles', NT, '+', len(ART_T), 'art ; metatuiles', len(SEC_ENT), '; palette art', ART_PAL)
