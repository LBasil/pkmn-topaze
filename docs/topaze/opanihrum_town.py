# OPANIHRUM (ex-Jadielle) : la cite de la forge et de l'acier, couleurs de l'OPALE (gris-bleu laiteux, reflets irises).
# Meme methode que Grenalux : tuiles d'Emeraude importees (ici Rustboro, la ville de pierre grise), recolorees, + art
# procedural (monument d'opale) ; plan d'occupation avec verifications ; accessibilite verifiee.
# Le jeu de tuiles secondaire est COMPACTE : on ne garde que les metatuiles utilisees (FireRed : 384 tuiles max).
# Lancer depuis la racine du depot :  python3 docs/topaze/opanihrum_town.py  puis  opanihrum_events.py
import struct, json, random, sys, colorsys, collections, os, shutil
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
EM = '../pokeemerald/data/'
PRI = 'data/tilesets/primary/general_opal/'; SEC = 'data/tilesets/secondary/rustboro_opal/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
RUST = struct.unpack('<2400H', open(EM + 'layouts/RustboroCity/map.bin', 'rb').read())      # 40 x 60
def rb(x, y): return RUST[y * 40 + x]

# ------------------------------------------------------------------ palettes (teinte opale/acier)
def tint(r, g, b):
    """OPALE NOIRE : pierre bleu-nuit presque noire, verdure sombre vert-de-gris ; les reflets viennent de l'art (feu de l'opale)."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.10 and l > 0.93: return r, g, b                  # blancs purs conserves
    if s > 0.45 and (h >= 180 or h < 25): return r, g, b      # rouges / bleus vifs (toits du CENTRE et de la BOUTIQUE)
    if 78 <= h <= 175:                    # vegetation : vert-de-gris sombre
        h = 168 + (h - 120) * 0.12; s = min(1, s * 0.5); l = l * 0.8
    else:                                 # pierre / sable / gris : ardoise bleu-nuit
        h = 232; s = min(0.42, s * 0.55 + 0.10); l = min(1, l * 0.72)
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
PALS_P = [[(c if k == 0 else tint(*c)) for k, c in enumerate(readpal(EM + 'tilesets/primary/general/palettes/%02d.pal' % i))] for i in range(16)]
PALS_S = [[(c if k == 0 else tint(*c)) for k, c in enumerate(readpal(EM + 'tilesets/secondary/rustboro/palettes/%02d.pal' % i))] for i in range(16)]
PALS_P[6] = PALS_S[6]                                       # FireRed : palette 6 = primaire
LD = E.load('general', 'rustboro')
LD = (LD[0], LD[1], [PALS_P[i] for i in range(6)] + [PALS_S[i] for i in range(6, 13)], LD[3], LD[4])   # rendu avec les palettes teintees

# ------------------------------------------------------------------ metatuiles : conversion attributs + compaction du secondaire
patt = open(EM + 'tilesets/primary/general/metatile_attributes.bin', 'rb').read()
satt = open(EM + 'tilesets/secondary/rustboro/metatile_attributes.bin', 'rb').read()
smt = open(EM + 'tilesets/secondary/rustboro/metatiles.bin', 'rb').read()
import re
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
SEC_MAP = {}            # id Emeraude (>=512) -> nouvel id FireRed (640+)
SEC_ENT = []            # entrees (8 u16) avec tuiles deja remappees
SEC_ATT = []
CT = []                 # tuiles secondaires conservees (indices dans le tiles.png d'Emeraude)
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

# ------------------------------------------------------------------ plan d'occupation
W, H = 42, 40
G = {}; OCC = {}
def walk(m): return 0x3000 | m
GRASS = 0x3000 | 1
COBBLE = remap(0x3000 | 699)
for y in range(H):
    for x in range(W): G[(x, y)] = GRASS
def put(x, y, v): G[(x, y)] = v
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            assert (x + i, y + j) not in OCC, 'chevauchement %s avec %s en %s' % (name, OCC[(x + i, y + j)], (x + i, y + j))
            assert 0 <= x + i <= W - 1 and 0 <= y + j <= H - 1, (name, x + i, y + j)
            OCC[(x + i, y + j)] = name
TREE_RAW = [[0x5d4, 0x5d5], [0x5dc, 0x5dd]]
def tree(x, y):
    for j in range(2):
        for i in range(2): put(x + i, y + j, TREE_RAW[j][i])
# sol pave interieur (x 3..38, y 3..36) ; cadre de grille de fer x=2/39, y=2/37
PX0, PX1, PY0, PY1 = 3, 38, 3, 36
for y in range(PY0, PY1 + 1):
    for x in range(PX0, PX1 + 1): put(x, y, COBBLE)
# ---- cadre d'arbres (portes : nord/sud x=20..21 ; ouest y=22..23)
for x in range(0, W, 2):
    if x != 20: tree(x, 0); tree(x, H - 2)
for y in range(2, H - 2, 2):
    if y != 22: tree(0, y)
    tree(W - 2, y)
# ---- grille de fer (cases bloquees) autour de la place, ouvertures aux portes
FH, FHB, FL, FR_, FTL, FTR, FBL, FBR = 679, 764, 789, 793, 702, 850, 812, 794
def fence(x, y, m): put(x, y, remap(0x400 | m))
for x in range(2, 40):
    if x in (20, 21): continue
    fence(x, 2, FH); fence(x, 37, FHB)
for y in range(3, 37):
    if y not in (22, 23): fence(2, y, FL)
    fence(39, y, FR_)
fence(2, 2, FTL); fence(39, 2, FTR); fence(2, 37, FBL); fence(39, 37, FBR)
# herbe entre la grille et les arbres : x=1/40 (deja herbe), y=1/38
# ---- avenue (2 cases : 768 gauche, 770 droite) et rues transversales
def street(y0, x0, x1, gaps=()):
    for x in range(x0, x1 + 1):
        top = 760 if x == x0 else 762 if x == x1 else 761
        bot = 776 if x == x0 else 778 if x == x1 else 777
        if x in (20, 21): top = bot = 94
        put(x, y0, remap(0x3000 | top)); put(x, y0 + 1, remap(0x3000 | bot))
for y in range(3, 37):
    if G[(20, y)] == COBBLE: put(20, y, remap(0x3000 | 768)); put(21, y, remap(0x3000 | 770))
street(12, 3, 38); street(22, 3, 38); street(35, 3, 38)
for y in (22, 23):                         # porte ouest : la rue sort de la place jusqu'au bord
    for x in (0, 1, 2): put(x, y, remap(0x3000 | (761 if y == 22 else 777)))
for y in (0, 1, 38, 39):                   # portes nord/sud : l'avenue sort
    put(20, y, remap(0x3000 | 768)); put(21, y, remap(0x3000 | 770))
for y in (2, 37): put(20, y, remap(0x3000 | 768)); put(21, y, remap(0x3000 | 770))
# case 20 des portes (arbres sautes en x=20 : 20..21 libres, 18..19 et 22..23 arbres) -> ok

# ---- batiments : (nom, x0 Rustboro, y0, largeur, hauteur) -> posés au coin (dx, dy)
def chunk(x0, y0, cw, ch, dx, dy, name):
    claim(dx, dy, cw, ch, name); doors = []
    for j in range(ch):
        for i in range(cw):
            v = rb(x0 + i, y0 + j); put(dx + i, dy + j, remap(v))
            if 0x60 <= beh(v & 0x3ff) <= 0x6f: doors.append((dx + i, dy + j))
    return doors
D = {}
D['foundry'] = chunk(7, 7, 10, 9, 4, 3, 'fonderie (arene)')
D['school'] = chunk(24, 30, 7, 5, 25, 4, 'ecole')
D['house'] = chunk(31, 15, 5, 5, 34, 4, 'maison')
D['center'] = chunk(15, 35, 4, 4, 15, 17, 'centre pokemon')
D['mart'] = chunk(15, 42, 4, 4, 26, 17, 'boutique')
D['tanL'] = chunk(9, 25, 9, 6, 4, 16, 'halle de forge')
D['grayB'] = chunk(28, 24, 5, 5, 33, 16, 'maison B')
D['grayBig'] = chunk(3, 43, 7, 9, 4, 26, 'residence')
D['tanS'] = chunk(7, 34, 5, 5, 12, 27, 'maison S')
D['tanBR'] = chunk(24, 42, 6, 5, 33, 27, 'atelier')
print('portes detectees', {k: v for k, v in D.items()})
open('/tmp/opanihrum_doors.json', 'w').write(json.dumps(D))

# ------------------------------------------------------------------ art procedural : monument d'opale, enclume, lingots
used_pals = {q >> 12 for e in SEC_ENT for q in e}
FREE = [p for p in range(7, 13) if p not in used_pals]
print('palettes secondaires utilisees', sorted(used_pals), 'libres', FREE)
assert FREE, 'aucune palette libre pour l art'
ART_PAL = FREE[0]
cob = metatile_img = E.metatile(LD, 699).convert('RGB')
cnt = collections.Counter(cob.getdata()); gcols = [c for c, _ in cnt.most_common(4)]
while len(gcols) < 4: gcols.append(gcols[-1])
SH = tuple(int(c * 0.55) for c in min(gcols, key=sum))
PAL = [(0, 0, 0)] + gcols + [(8, 10, 24), (22, 26, 52), (46, 54, 98), (92, 106, 168), (236, 242, 255), (255, 104, 186), (70, 240, 218),
                              (186, 116, 255), SH, (150, 158, 182), (255, 196, 80)]
# indices : 1-4 sol | 5 contour | 6 opale sombre | 7 opale | 8 clair | 9 blanc | 10 rose | 11 cyan | 12 violet | 13 ombre | 14 acier | 15 cuivre
def newimg(w, h):
    im = Image.new('P', (w, h), 1); im.putpalette([c for p in PAL for c in p]); return im
def ground_bg(w, h):
    im = newimg(w, h); px = im.load(); g = cob.load()
    for y in range(h):
        for x in range(w):
            c = g[x % 16, y % 16]; px[x, y] = 1 + gcols.index(c) if c in gcols else 1
    return im
def shadow(d, x0, y0, x1, y1): d.ellipse((x0, y0, x1, y1), fill=13)
def dome(d, cx, base, rx, ry):
    top = base - ry
    d.ellipse((cx - rx, top, cx + rx, base + ry // 4), fill=7, outline=5)
    d.pieslice((cx - rx + 1, top + 1, cx + rx - 1, base + ry // 4 - 1), 300, 80, fill=6)
    d.pieslice((cx - rx + 2, top + 2, max(cx - rx + 4, cx + rx - 5), max(top + 4, base - ry // 2)), 170, 290, fill=8)
    for k, c in enumerate((10, 11, 15, 12, 10, 11)):                          # feu de l'opale
        x = cx - rx + 2 + k * max(2, (2 * rx - 6) // 5); y = top + ry // 2 + (k % 3) * max(2, ry // 4)
        d.polygon([(x, y), (x + 2, y - 2), (x + 4, y + 1), (x + 2, y + 4)], fill=c)
    d.ellipse((cx - rx // 2, top + 3, cx - rx // 2 + 3, top + 6), fill=9)
def big():
    im = ground_bg(48, 48); d = ImageDraw.Draw(im)
    shadow(d, 1, 38, 47, 47)
    d.rectangle((5, 36, 42, 44), fill=14, outline=5); d.rectangle((8, 33, 39, 36), fill=14, outline=5)
    d.line([(6, 37), (41, 37)], fill=8); d.line([(9, 34), (38, 34)], fill=8)
    dome(d, 11, 34, 8, 12); dome(d, 36, 34, 8, 14)
    dome(d, 24, 34, 12, 30)
    return im, 3, 3
def small(var):
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 1, 11, 15, 15)
    if var == 0: dome(d, 8, 12, 5, 8)
    else: dome(d, 5, 12, 3, 5); dome(d, 11, 12, 4, 8)
    return im
def anvil():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 1, 11, 15, 15)
    d.rectangle((4, 11, 11, 13), fill=14, outline=5); d.rectangle((6, 8, 9, 11), fill=14, outline=5)
    d.polygon([(1, 5), (14, 5), (15, 8), (3, 8), (0, 6)], fill=14, outline=5); d.line([(2, 6), (12, 6)], fill=8)
    d.point((13, 3), fill=15); d.point((12, 2), fill=15); d.point((14, 4), fill=15)
    return im
def ingots():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 0, 11, 15, 15)
    for (x, y) in ((1, 9), (8, 9), (4, 5)):
        d.polygon([(x, y + 4), (x + 2, y), (x + 7, y), (x + 6, y + 4)], fill=14, outline=5); d.line([(x + 2, y + 1), (x + 6, y + 1)], fill=8)
    d.point((11, 6), fill=15)
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
BIG = slice_all(*big()); SM = [meta(small(0)), meta(small(1))]; ANVIL = meta(anvil()); INGOTS = meta(ingots())

# ------------------------------------------------------------------ decors : fontaine, monument, lampadaires, enseignes
FOUNTAIN = chunk(27, 38, 3, 3, 16, 24, 'fontaine')
def art_cells(sm, x0, y0, w, h, name):
    claim(x0, y0, w, h, name)
    for (i, j), m in sm.items(): put(x0 + i, y0 + j, ('ARTRAW', m, 0x400))
ART_PLACED = []
art_cells(BIG, 24, 25, 3, 3, 'monument opale')
def art1(x, y, m, name):
    claim(x, y, 1, 1, name); put(x, y, ('ARTRAW', m, 0x400))
LAMP_T, LAMP_B = 530, 538                  # lampadaire Emeraude : haut traversable (au-dessus du joueur), pied bloque
def lamp(x, y):
    claim(x, y, 1, 2, 'lampadaire')
    put(x, y, remap(0x3000 | LAMP_T)); put(x, y + 1, remap(0x400 | LAMP_B))
for (x, y) in ((19, 4), (22, 4), (19, 8), (22, 8), (19, 14), (22, 14), (19, 18), (22, 18), (19, 25), (22, 25), (19, 29), (22, 29), (19, 32), (22, 32)):
    lamp(x, y)
SIGN = remap(0x400 | 3)
def sign(x, y): claim(x, y, 1, 1, 'panneau'); put(x, y, SIGN)
SIGNS = {'tips1': (23, 3), 'gym': (11, 13), 'city': (23, 16), 'tips2': (23, 31), 'gymdoor': None}
for k, c in SIGNS.items():
    if c: sign(*c)
for (x, y, v) in ((14, 15, 0), (31, 15, 1), (16, 33, 0), (30, 33, 1), (8, 24, 0), (35, 25, 1)):
    art1(x, y, SM[v], 'opale')
for (x, y) in ((13, 19), (30, 19), (12, 33), (31, 25)): art1(x, y, ANVIL, 'enclume')
for (x, y) in ((14, 19), (31, 19), (13, 33)): art1(x, y, INGOTS, 'lingots')
# ilots de verdure : parc a droite de la fonderie, parterres sous l'ecole et la maison
FLOWER = walk(4)
def patch(x0, y0, x1, y1, name):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            claim(x, y, 1, 1, name); put(x, y, GRASS)
patch(14, 3, 17, 10, 'parc'); patch(26, 10, 32, 11, 'parterre ecole'); patch(33, 10, 38, 11, 'parterre maison')
patch(13, 34, 17, 34, 'parterre sud') if False else None
for (x, y) in ((14, 3), (16, 3), (14, 8), (16, 8)):
    for j in range(2):
        for i in range(2): put(x + i, y + j, TREE_RAW[j][i])
for y in (5, 6):
    for x in range(14, 18): put(x, y, FLOWER if (x + y) % 2 == 0 else GRASS)
for x in range(26, 39):
    if x != 33: put(x, 11, FLOWER if x % 2 == 0 else GRASS)
for (x, y) in ((4, 24), (5, 24), (6, 24), (7, 24)):
    pass

# ------------------------------------------------------------------ accessibilite / PNJ
NPC = {'fatman': (14, 25), 'oldman': (11, 14), 'woman': (17, 12), 'youngster': (31, 21), 'boy': (26, 24), 'tutorial': (20, 6), 'potion': (15, 5)}
BLOCK_RAW = lambda v: isinstance(v, tuple) or (v & 0xc00) or ((v >> 12) == 1)
def raw_blocked(c):
    v = G[c]
    if isinstance(v, tuple): return True
    return bool(v & 0xc00)
seen = {(20, 12)}; q = collections.deque([(20, 12)])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not raw_blocked(n): seen.add(n); q.append(n)
for k, c in NPC.items():
    assert OCC.get(c) in (None, 'parc') and c in seen, ('PNJ inaccessible ou sur un decor', k, c)
for k, ds in D.items():
    for (x, y) in ds: assert (x, y + 1) in seen, ('porte inaccessible', k, (x, y))
for c in ((20, 0), (21, 0), (20, 39), (21, 39), (0, 22), (0, 23)): assert c in seen, c
for k, c in SIGNS.items():
    if c: assert (c[0], c[1] + 1) in seen or (c[0], c[1] - 1) in seen or (c[0] - 1, c[1]) in seen, ('panneau inaccessible', k)
json.dump(NPC, open('/tmp/opanihrum_npc.json', 'w'))

# ------------------------------------------------------------------ ecriture des tilesets
NT = len(CT)
assert NT + len(ART_T) <= 384, ('trop de tuiles', NT, len(ART_T))
NART0 = 640 + len(SEC_ENT)
art_ids = {}
for k, ents in enumerate(ART_E):
    SEC_ENT.append([(640 + NT + t) | (ART_PAL << 12) for (_, t) in ents] + [0, 0, 0, 0]); SEC_ATT.append(0)
    art_ids[k] = 640 + len(SEC_ENT) - 1
assert len(SEC_ENT) <= 384, len(SEC_ENT)
for k, v in list(G.items()):
    if isinstance(v, tuple):
        assert v[1][0] == 'ART_META'; G[k] = v[2] | art_ids[v[1][1]]
# tiles.png secondaire
src_png = Image.open(EM + 'tilesets/secondary/rustboro/tiles.png')
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
# primaire : copie du primaire d'Emeraude (ids < 512)
shutil.copy(EM + 'tilesets/primary/general/tiles.png', PRI + 'tiles.png')
shutil.copy(EM + 'tilesets/primary/general/metatiles.bin', PRI + 'metatiles.bin')
open(PRI + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', conv(struct.unpack('<H', patt[i * 2:i * 2 + 2])[0])) for i in range(len(patt) // 2)))
# declarations C (idempotentes)
def add(path, text):
    s = open(path).read()
    if 'GeneralOpal' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralOpal[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralOpal[][16] =\n{\n%s};\n' % (PRI, pal(PRI)) +
    '\nconst u32 gTilesetTiles_RustboroOpal[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_RustboroOpal[][16] =\n{\n%s};\n' % (SEC, pal(SEC)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralOpal[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralOpal[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
    'const u16 gMetatiles_RustboroOpal[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_RustboroOpal[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralOpal =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralOpal,
    .palettes = gTilesetPalettes_GeneralOpal,
    .metatiles = gMetatiles_GeneralOpal,
    .metatileAttributes = gMetatileAttributes_GeneralOpal,
    .callback = NULL,
};

const struct Tileset gTileset_RustboroOpal =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RustboroOpal,
    .palettes = gTilesetPalettes_RustboroOpal,
    .metatiles = gMetatiles_RustboroOpal,
    .metatileAttributes = gMetatileAttributes_RustboroOpal,
    .callback = NULL,
};
''')
# ------------------------------------------------------------------ carte
g = [G[(x, y)] for y in range(H) for x in range(W)]
os.makedirs('data/layouts/ViridianCity', exist_ok=True)
open('data/layouts/ViridianCity/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/ViridianCity/border.bin', 'wb').write(struct.pack('<4H', 0x5d4, 0x5d5, 0x5dc, 0x5dd))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_VIRIDIAN_CITY':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralOpal', secondary_tileset='gTileset_RustboroOpal')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
blocked = {(x, y) for y in range(H) for x in range(W) if (g[y * W + x] & 0xc00) or ((g[y * W + x] >> 12) == 1)}
json.dump({'w': W, 'h': H, 'blocked': [list(c) for c in sorted(blocked)]}, open('/tmp/opanihrum_col.json', 'w'))
print('opanihrum: tuiles', NT, '+', len(ART_T), 'art ; metatuiles', len(SEC_ENT), '; palette art', ART_PAL)
