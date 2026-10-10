# ROUTE 24 « le pont des pepites » (et Route 25, meme jeu de tuiles pour la continuite des couleurs) : habillage aux couleurs de Tourmalia.
# La carte d'origine (pont, riviere, lac, dresseurs) est conservee ; on copie les tilesets de FireRed (general / cerulean_city) en
# `general_pepite` / `cerulean_pepite` : falaises recolorees en mauve (couleur de tourmaline), + art ajoute au secondaire (cristaux, grands arbres d'Emeraude),
# + vegetation et cristaux poses sur les cases libres (parcours verifie par BFS). Lancer depuis la racine : python3 docs/topaze/route24_dress.py
import struct, json, random, sys, os, shutil, math, colorsys, collections
from PIL import Image, ImageDraw
sys.path.insert(0, 'docs/topaze')
import emrender as E
FRP = 'data/tilesets/primary/general/'; FRS = 'data/tilesets/secondary/cerulean_city/'
NP = 'data/tilesets/primary/general_pepite/'; NS = 'data/tilesets/secondary/cerulean_pepite/'
for src, dst in ((FRP, NP), (FRS, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16): shutil.copy(src + 'palettes/%02d.pal' % i, dst + 'palettes/%02d.pal' % i)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
# ------------------------------------------------------------------ couleurs : falaises rosees -> mauve de tourmaline
def mauve(c):
    r, g, b = c; h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s > 0.12 and (h < 50 or h > 330):
        r, g, b = colorsys.hls_to_rgb(312 / 360, l, min(0.5, s * 0.8)); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
    return c
p1 = readpal(NP + 'palettes/01.pal'); writepal(NP + 'palettes/01.pal', [p1[0]] + [mauve(c) for c in p1[1:15]] + [p1[15]])
# ------------------------------------------------------------------ art
ART_PAL, TREE_PAL = 7, 8
PAL = [(0, 0, 0), (8, 24, 20), (18, 84, 60), (34, 140, 92), (100, 208, 140), (188, 246, 208), (250, 255, 250), (140, 30, 86), (222, 72, 138),
       (255, 146, 194), (255, 214, 232), (22, 60, 44), (92, 64, 40), (126, 130, 126), (70, 76, 74), (255, 232, 136)]
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
    im = newimg(16, 16); d = ImageDraw.Draw(im); shadow(d, 1, 12, 15, 16)
    if var == 0: prism(d, 4, 14, 5, 9); prism(d, 9, 15, 7, 14); prism(d, 13, 14, 4, 7)
    elif var == 1: prism(d, 6, 15, 6, 11); prism(d, 12, 14, 5, 8); d.rectangle((1, 13, 3, 14), fill=13); d.point((2, 12), fill=14)
    else: prism(d, 8, 15, 8, 14); d.rectangle((2, 13, 4, 14), fill=13); d.rectangle((12, 12, 14, 14), fill=13); d.point((13, 11), fill=14)
    return im
def cluster():       # 2x2 : grand amas de cristaux
    im = newimg(32, 32); d = ImageDraw.Draw(im); shadow(d, 1, 25, 31, 32)
    prism(d, 8, 29, 7, 17); prism(d, 24, 30, 8, 21); prism(d, 15, 31, 11, 28); d.rectangle((2, 27, 5, 29), fill=13)
    return im
# arbres d'Emeraude (468/469/476/477) en art transparent, palette propre (quantifiee sur 15 teintes)
LG = E.load('general', 'petalburg')
def rgba(m):
    pt, st, pals, mp, ms = LG; e = mp[m * 8:m * 8 + 8]; im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for layer in (0, 1):
        for k in range(4):
            v = e[layer * 4 + k]; im.alpha_composite(E.tile(pt, st, pals, v & 0x3ff, v >> 12, v & 0x400, v & 0x800), ((k % 2) * 8, (k // 2) * 8))
    return im
TREE = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
for k, m in enumerate((468, 469, 476, 477)): TREE.alpha_composite(rgba(m), ((k % 2) * 16, (k // 2) * 16))
tp = TREE.load()
for y in range(32):
    for x in range(32):
        r, g, b, a = tp[x, y]
        if a:
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if 135 <= h * 360 <= 205 and s > 0.2 and l > 0.5: tp[x, y] = (0, 0, 0, 0)
cols = [tp[x, y][:3] for y in range(32) for x in range(32) if tp[x, y][3]]
qi = Image.new('RGB', (len(cols), 1)); qi.putdata(cols); qq = qi.quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE); qpal = (qq.getpalette() or [])[:45]; qpal = list(qpal) + [qpal[-3], qpal[-2], qpal[-1]] * ((45 - len(qpal)) // 3) if len(qpal) >= 3 else [0]*45
TPAL = [(0, 0, 0)] + [tuple(qpal[3 * k:3 * k + 3]) for k in range(15)]
def near_idx(c): return 1 + min(range(15), key=lambda k: sum((TPAL[k + 1][i] - c[i]) ** 2 for i in range(3)))
TREE_P = newimg(32, 32); tq = TREE_P.load()
for y in range(32):
    for x in range(32):
        if tp[x, y][3]: tq[x, y] = near_idx(tp[x, y][:3])
# ------------------------------------------------------------------ tilesets : ajout au secondaire
smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = bytearray(open(NS + 'metatile_attributes.bin', 'rb').read())
NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
pmt = open(NP + 'metatiles.bin', 'rb').read(); patt = open(NP + 'metatile_attributes.bin', 'rb').read()
NEWT = []
def add_tile(t):
    t = tuple(t)
    if t in NEWT: return NEWT.index(t)
    NEWT.append(t); return len(NEWT) - 1
def slice4(im): return [add_tile([im.getpixel((((q % 2) * 8 + i), (q // 2) * 8 + j)) for j in range(8) for i in range(8)]) for q in range(4)]
NEWM = {}; ENTS = []
def art_meta(tiles4, slot, bottom):
    key = (tuple(tiles4), slot, tuple(bottom))
    if key not in NEWM: ENTS.append(list(bottom) + [(640 + NTL + t) | (slot << 12) for t in tiles4]); NEWM[key] = 640 + NMT + len(ENTS) - 1
    return NEWM[key]
def bottom_of(m):
    e = struct.unpack('<8H', pmt[m * 16:m * 16 + 16]) if m < 640 else struct.unpack('<8H', bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16]))
    return e[:4]
# ------------------------------------------------------------------ carte
W, H = 24, 40
mp_ = 'data/layouts/Route24/map.bin'
G = {(x, y): v for (x, y), v in zip(((x, y) for y in range(H) for x in range(W)), struct.unpack('<%dH' % (W * H), open(mp_, 'rb').read()))}
G0 = dict(G)
def beh(m):
    a = struct.unpack('<I', (patt[m * 4:m * 4 + 4] if m < 640 else bytes(satt[(m - 640) * 4:(m - 640) * 4 + 4])))[0]; return a & 0x1ff
WATER = {0x10, 0x11, 0x12, 0x15}
def blocked(c, g=None):
    v = (g or G)[c]; return bool(v & 0xc00) or beh(v & 0x3ff) in WATER
obj = json.load(open('data/maps/Route24/map.json'))
RES = set()
for o in obj['object_events']:
    for a in range(-1, 2):
        for b in range(-1, 2): RES.add((o['x'] + a, o['y'] + b))
for w in obj['warp_events']:
    for a in range(-1, 2):
        for b in range(-1, 2): RES.add((w['x'] + a, w['y'] + b))
for b_ in obj['bg_events']: RES.add((b_['x'], b_['y']))
for c_ in obj['coord_events']: RES.add((c_['x'], c_['y']))
def flood(g, s0):
    seen = {s0}; q = collections.deque([s0])
    while q:
        c = q.popleft()
        for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n, g): seen.add(n); q.append(n)
    return seen
START = (11, 38)
R0 = flood(G0, START)
GRASSM = {1, 4, 8, 9, 16, 17}
def mid(c): return G[c] & 0x3ff
def grass(c): return mid(c) in GRASSM and not blocked(c) and c not in RES
rnd = random.Random(2401)
GRS = {8: (0, 0), 9: (1, 0), 16: (0, 1), 17: (1, 1)}
def gm(x, y): return 8 + (x % 2) + 8 * (y % 2)
# prairie sur le plateau nord (a la place du sable) : deux pans a l'ouest et a l'est de la 1ere moitie
def meadow(x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if mid((x, y)) == 217 and (x, y) not in RES: G[(x, y)] = (G[(x, y)] & 0xfc00) | gm(x, y)
meadow(4, 3, 8, 5); meadow(14, 3, 16, 5); meadow(3, 7, 6, 8)
for y in range(7, 9):
    for x in range(15, 23): pass
ARTP = {}                            # cellule -> (tuiles4, slot, metatuile de base, bloque)
def put_tree(x, y):
    cells = [(x + i, y + j) for j in range(2) for i in range(2)]
    if not all(grass(c) for c in cells): return False
    ring = {(x + i, y + j) for i in range(-1, 3) for j in range(-1, 3)} - set(cells)
    if any(c in ARTP for c in ring) or sum(1 for c in ring if 0 <= c[0] < W and 0 <= c[1] < H and not blocked(c)) < 5: return False
    t4s = {(i, j): slice4(TREE_P.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))) for j in range(2) for i in range(2)}
    for (i, j), t4 in t4s.items(): ARTP[(x + i, y + j)] = (t4, TREE_PAL, mid((x + i, y + j)), True)
    return True
def put_small(c, var, walk=False):
    if not grass(c) or c in ARTP: return False
    ARTP[c] = (slice4(small(var)), ART_PAL, mid(c), True); return True
def put_cluster(x, y):
    cells = [(x + i, y + j) for j in range(2) for i in range(2)]
    if not all(grass(c) and c not in ARTP for c in cells): return False
    im = cluster()
    for j in range(2):
        for i in range(2): ARTP[(x + i, y + j)] = (slice4(im.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))), ART_PAL, mid((x + i, y + j)), True)
    return True
# arbres : berge ouest (nord), plateau, bande est
for (x, y) in ((3, 10), (8, 12), (4, 13), (14, 11), (14, 15), (14, 19), (14, 23), (15, 3), (3, 7)):
    put_tree(x, y)
for (x, y) in ((6, 10), (9, 14), (15, 13), (15, 17), (15, 21), (16, 4)): put_cluster(x, y)
cand = [c for c in sorted(G) if grass(c) and c not in ARTP and (c[0] <= 9 or c[0] in (14, 15, 16))]
for c in cand:
    if rnd.random() < 0.10 and not any((c[0] + a, c[1] + b) in ARTP for a in (-1, 0, 1) for b in (-1, 0, 1)): put_small(c, rnd.randrange(3))
# verification : tout ce qui etait atteignable (hors cases couvertes) le reste
for c, (t4, slot, m, blk) in ARTP.items(): G[c] = (G0[c] & 0xf000) | (0x400 if blk else 0) | art_meta(t4, slot, bottom_of(m))
R1 = flood(G, START)
lost = {c for c in R0 if c not in R1 and c not in ARTP}
assert not lost, ('cases devenues inatteignables', sorted(lost)[:10])
print('arbres/cristaux poses :', len(ARTP), '; atteignable', len(R0), '->', len(R1))
# ------------------------------------------------------------------ ecriture
smt += b''.join(struct.pack('<8H', *e) for e in ENTS); satt += b'\0\0\0\0' * len(ENTS)
assert NMT + len(ENTS) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(ENTS), NTL + len(NEWT))
open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(satt)
rows = (NTL + len(NEWT) + 15) // 16
out = Image.new('P', (128, rows * 8), 0); out.putpalette(simg.getpalette()); out.paste(simg, (0, 0))
for n, t in enumerate(NEWT):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
out.save(NS + 'tiles.png')
writepal(NS + 'palettes/%02d.pal' % ART_PAL, PAL); writepal(NS + 'palettes/%02d.pal' % TREE_PAL, TPAL)
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/Route24/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
def add(path, text):
    s = open(path).read()
    if 'GeneralPepite' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralPepite[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralPepite[][16] =\n{\n%s};\n' % (NP, pal(NP)) +
    '\nconst u32 gTilesetTiles_CeruleanPepite[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_CeruleanPepite[][16] =\n{\n%s};\n' % (NS, pal(NS)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralPepite[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralPepite[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (NP, NP) +
    'const u16 gMetatiles_CeruleanPepite[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_CeruleanPepite[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (NS, NS))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralPepite =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralPepite,
    .palettes = gTilesetPalettes_GeneralPepite,
    .metatiles = gMetatiles_GeneralPepite,
    .metatileAttributes = gMetatileAttributes_GeneralPepite,
    .callback = InitTilesetAnim_General,
};

const struct Tileset gTileset_CeruleanPepite =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CeruleanPepite,
    .palettes = gTilesetPalettes_CeruleanPepite,
    .metatiles = gMetatiles_CeruleanPepite,
    .metatileAttributes = gMetatileAttributes_CeruleanPepite,
    .callback = NULL,
};
''')
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') in ('LAYOUT_ROUTE24', 'LAYOUT_ROUTE25'): l.update(primary_tileset='gTileset_GeneralPepite', secondary_tileset='gTileset_CeruleanPepite')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'w': W, 'h': H, 'blocked': sorted([x, y] for (x, y) in G if blocked((x, y)))}, open('/tmp/route24_col.json', 'w'))
print('route 24 habillee : metatuiles', NMT + len(ENTS), 'tuiles', NTL + len(NEWT))
