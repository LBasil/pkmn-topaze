#!/usr/bin/env python3
"""Mont Selenite : refonte visuelle de l'interieur (1F, B1F, B2F).

- nouveau tileset secondaire `mt_moon` (copie de `cave`) dont les palettes sont reteintees "clair de lune" (violet/bleu ardoise,
  poussiere lunaire argentee a la place du sable jaune) ;
- palette 7 (libre dans `cave`) : sol + cristaux de pierre lunaire (dessines par code, comme les grenats de Grenalux) ;
- nouveaux metatuiles : petits/moyens/grands cristaux (solides), variantes de sol scintillantes (praticables, meme comportement
  que le sol d'origine : les rencontres sauvages sont conservees) ;
- pose automatique dans les trois cartes, avec verification qu'aucun chemin / PNJ / objet / warp n'est bloque.

Usage (depuis la racine du depot, idempotent) : python3 docs/topaze/moon_cave.py
"""
import os, sys, json, shutil, struct, colorsys, random, collections
from PIL import Image, ImageDraw
sys.path.insert(0, 'tools/topaze/maps')

SRC = 'data/tilesets/secondary/cave/'
D = 'data/tilesets/secondary/mt_moon/'
FLOORS = ('1F', 'B1F', 'B2F')

# ------------------------------------------------------------------ 1. tileset
if os.path.isdir(D): shutil.rmtree(D)
os.makedirs(D + 'palettes')
for f in ('tiles.png', 'metatiles.bin', 'metatile_attributes.bin'): shutil.copy(SRC + f, D + f)
for i in range(16): shutil.copy(SRC + 'palettes/%02d.pal' % i, D + 'palettes/%02d.pal' % i)

def read_pal(p):
    L = open(p).read().split(); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(int(L[2]))]
def write_pal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in cols))

def moon(c):
    r, g, b = c
    if c in ((255, 0, 255), (0, 0, 0)): return c
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if 0.5 < h < 0.75 and s > 0.3: return c                      # bleus d'origine (eau, echelles) : inchanges
    rose = h > 0.9 or h < 0.06
    nh = 0.72 if rose else 0.63                                    # roche rosee -> violet ; sable/ardoise -> bleu gris
    ns = min(0.42, s * 0.8 + 0.16)
    nl = l * 0.9 if l < 0.55 else min(0.95, l * 0.97 + 0.02)
    rr, gg, bb = colorsys.hls_to_rgb(nh, nl, ns)
    return (round(rr * 255), round(gg * 255), round(bb * 255))

for i in (8, 9, 10, 11, 12):
    p = D + 'palettes/%02d.pal' % i
    cols = read_pal(p); write_pal(p, [cols[0]] + [moon(c) for c in cols[1:]])

# ------------------------------------------------------------------ 2. layouts -> nouveau tileset
LJ = 'data/layouts/layouts.json'
txt = open(LJ).read()
for f in FLOORS:
    i = txt.index('"id": "LAYOUT_MT_MOON_%s"' % f); j = txt.index('"secondary_tileset": "', i)
    k = txt.index('"', j + 22)
    txt = txt[:j + 22] + 'gTileset_MtMoon' + txt[k:]
open(LJ, 'w').write(txt)

# enregistrement C (idempotent)
def append_once(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal_lines = ''.join('\tINCBIN_U16("data/tilesets/secondary/mt_moon/palettes/%02d.gbapal"),\n' % i for i in range(16))
append_once('src/data/tilesets/graphics.h', 'gTilesetTiles_MtMoon',
            '\nconst u32 gTilesetTiles_MtMoon[] = INCBIN_U32("data/tilesets/secondary/mt_moon/tiles.4bpp.lz");\n\n'
            'const u16 gTilesetPalettes_MtMoon[][16] =\n{\n' + pal_lines + '};\n')
append_once('src/data/tilesets/metatiles.h', 'gMetatiles_MtMoon',
            'const u16 gMetatiles_MtMoon[] = INCBIN_U16("data/tilesets/secondary/mt_moon/metatiles.bin");\n'
            'const u32 gMetatileAttributes_MtMoon[] = INCBIN_U32("data/tilesets/secondary/mt_moon/metatile_attributes.bin");\n')
append_once('src/data/tilesets/headers.h', 'gTileset_MtMoon',
            '\nconst struct Tileset gTileset_MtMoon =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
            '    .tiles = gTilesetTiles_MtMoon,\n    .palettes = gTilesetPalettes_MtMoon,\n    .metatiles = gMetatiles_MtMoon,\n'
            '    .metatileAttributes = gMetatileAttributes_MtMoon,\n    .callback = NULL,\n};\n')

from mapkit import Layout
lay = Layout('LAYOUT_MT_MOON_1F')
FLOOR = 641
ground = lay.metatile_img(FLOOR).convert('RGB')
cnt = collections.Counter(ground.getdata())
gcols = [c for c, _ in cnt.most_common(4)]
while len(gcols) < 4: gcols.append(gcols[-1])
gcols.sort(key=lambda c: sum(c))                                  # du plus sombre au plus clair
PAL = [(0, 0, 0)] + gcols + [(30, 30, 78), (84, 104, 190), (138, 170, 236), (196, 224, 255), (236, 250, 255),
                              (255, 255, 255), (28, 30, 64), (66, 58, 128), (118, 104, 176), (12, 12, 34), (150, 244, 244)]
# indices : 1-4 sol | 5 contour | 6 cristal sombre | 7 cristal | 8 clair | 9 reflet | 10 blanc | 11 ombre | 12 violet | 13 violet clair | 14 noir | 15 lueur

def newimg(w, h):
    im = Image.new('P', (w, h), 1); im.putpalette([c for p in PAL for c in p]); return im
def ground_bg(w, h):
    im = newimg(w, h); px = im.load(); g = ground.load()
    for y in range(h):
        for x in range(w):
            c = g[x % 16, y % 16]; px[x, y] = 1 + gcols.index(c) if c in gcols else 1
    return im
def prism(d, cx, base, hw, h, tilt=0):
    top = base - h; L, R = cx - hw, cx + hw; tx = cx + tilt
    d.polygon([(L, base), (L, top + hw), (tx, top), (R, top + hw), (R, base), (cx, base + hw // 2)], fill=7, outline=5)
    d.polygon([(cx, base + hw // 2), (cx, top + 3), (R, top + hw), (R, base)], fill=6)
    d.polygon([(L + 1, top + hw), (tx, top + 1), (cx, top + 3), (cx - 1, base - 1), (L + 1, base - 1)], fill=7)
    d.polygon([(tx, top + 1), (tx + 3 + hw // 2, top + hw - 1), (cx, top + hw + 2)], fill=8)
    d.line([(L + 2, top + hw + 2), (L + 2, base - 4)], fill=9)
    d.point((tx, top + 2), fill=10)
def shadow(d, x0, y0, x1, y1): d.ellipse((x0, y0, x1, y1), fill=11)
def glow(d, x0, y0, x1, y1): d.ellipse((x0, y0, x1, y1), fill=13)
def big():
    im = ground_bg(48, 48); d = ImageDraw.Draw(im)
    shadow(d, 1, 36, 47, 47); glow(d, 5, 40, 43, 47)
    prism(d, 10, 42, 6, 20, -2); prism(d, 38, 43, 6, 18, 2)
    prism(d, 24, 44, 9, 40, 1)
    prism(d, 15, 44, 5, 28, -1); prism(d, 33, 45, 5, 26, 1)
    for (x, y) in ((22, 14), (30, 22), (12, 26), (36, 28)): d.point((x, y), fill=10); d.point((x + 1, y), fill=15)
    return im, 3, 3
def mid():
    im = ground_bg(32, 32); d = ImageDraw.Draw(im)
    shadow(d, 1, 24, 31, 31); glow(d, 4, 27, 28, 31)
    prism(d, 9, 29, 5, 14, -1); prism(d, 23, 29, 5, 12, 1); prism(d, 16, 30, 7, 25)
    d.point((15, 8), fill=10); d.point((20, 16), fill=15)
    return im, 2, 2
def small(var):
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 2, 11, 14, 15)
    if var == 0: prism(d, 8, 13, 4, 10)
    else: prism(d, 5, 13, 3, 7, -1); prism(d, 11, 13, 3, 9, 1)
    return im
def sparkle(var):
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    pts = [[(3, 4), (11, 9), (6, 12)], [(12, 3), (4, 8), (9, 13)], [(7, 3), (13, 11), (2, 12)]][var]
    for (x, y) in pts:
        d.point((x, y), fill=10); d.point((x - 1, y), fill=15); d.point((x + 1, y), fill=15); d.point((x, y - 1), fill=15); d.point((x, y + 1), fill=15)
    return im

# ------------------------------------------------------------------ 3. metatuiles
mt = bytearray(open(D + 'metatiles.bin', 'rb').read()); att = bytearray(open(D + 'metatile_attributes.bin', 'rb').read())
NMT = len(mt) // 16
png = Image.open(D + 'tiles.png'); NT = (png.size[1] // 8) * 16
tiles = []
def add_tile(t):
    t = tuple(t)
    if t in tiles: return tiles.index(t)
    tiles.append(t); return len(tiles) - 1
def meta(block, attr=0):
    ents = []
    for q in range(4):
        x, y = (q % 2) * 8, (q // 2) * 8
        ents.append((640 + NT + add_tile(list(block.crop((x, y, x + 8, y + 8)).getdata()))) | (7 << 12))
    ents += [0, 0, 0, 0]
    mt.extend(struct.pack('<8H', *ents)); att.extend(struct.pack('<I', attr))
    return 640 + len(mt) // 16 - 1
def slice_all(im, bw, bh): return {(i, j): meta(im.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))) for j in range(bh) for i in range(bw)}
BIG = slice_all(*big()); MID = slice_all(*mid()); SM = [meta(small(0)), meta(small(1))]
FLOOR_ATTR = struct.unpack('<I', att[4:8])[0]                    # attribut du sol d'origine (comportement + rencontres)
SPK = [meta(sparkle(v), FLOOR_ATTR) for v in range(3)]
assert NT + len(tiles) <= 384 + 256 - 128 + 128, len(tiles)
assert 640 + NT + len(tiles) <= 1024, len(tiles)
open(D + 'metatiles.bin', 'wb').write(mt); open(D + 'metatile_attributes.bin', 'wb').write(att)
out = Image.new('P', (128, ((NT + len(tiles) + 15) // 16) * 8), 0); out.putpalette(png.getpalette()); out.paste(png, (0, 0))
for i, t in enumerate(tiles):
    n = NT + i; ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, ((n % 16) * 8, (n // 16) * 8))
out.save(D + 'tiles.png')
write_pal(D + 'palettes/07.pal', PAL)

# ------------------------------------------------------------------ 4. pose dans les cartes
def walk_cells(g, w, h, blocked):
    """cases praticables (collision 0) hors `blocked`."""
    return {(x, y) for y in range(h) for x in range(w) if not (g[y * w + x] >> 10 & 3) and (x, y) not in blocked}
def reach(cells, starts):
    seen = set(); st = [s for s in starts if s in cells]
    seen.update(st)
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in cells and n not in seen: seen.add(n); st.append(n)
    return seen

for fl in FLOORS:
    name = 'MtMoon_' + fl
    mj = json.load(open('data/maps/%s/map.json' % name))
    L = Layout('LAYOUT_MT_MOON_' + fl); w, h = L.w, L.h; g = list(L.g)
    pts = [(e['x'], e['y']) for e in mj.get('warp_events', [])] + [(e['x'], e['y']) for e in mj.get('object_events', [])] \
        + [(e['x'], e['y']) for e in mj.get('bg_events', [])] + [(e['x'], e['y']) for e in mj.get('coord_events', [])]
    keep = set(pts)
    cells0 = walk_cells(g, w, h, set())
    starts = [(e['x'], e['y']) for e in mj.get('warp_events', [])]
    base = reach(cells0, starts)
    rnd = random.Random(hash(fl) & 0xffff if False else {'1F': 11, 'B1F': 23, 'B2F': 37}[fl])
    want = {'1F': [(MID, 2, 4), (SM, 1, 10)], 'B1F': [(MID, 2, 3), (SM, 1, 9)], 'B2F': [(BIG, 3, 1), (MID, 2, 3), (SM, 1, 8)]}[fl]
    placed = []
    taken = set()
    def free_zone(x, y, s):
        for j in range(-1, s + 1):
            for i in range(-1, s + 1):
                cx, cy = x + i, y + j
                if not (0 <= cx < w and 0 <= cy < h): return False
        for j in range(s):
            for i in range(s):
                cx, cy = x + i, y + j
                if g[cy * w + cx] & 0x3ff != FLOOR or g[cy * w + cx] >> 10 & 3: return False
                if (cx, cy) in taken: return False
        for (px, py) in keep:                                        # marge de 2 cases autour des PNJ / warps / objets
            if x - 2 <= px <= x + s + 1 and y - 2 <= py <= y + s + 1: return False
        for (px, py, ps) in placed:
            if abs(px - x) < s + ps + 3 and abs(py - y) < s + ps + 3: return False
        return True
    for (kind, size, count) in want:
        n = 0; tries = 0
        while n < count and tries < 4000:
            tries += 1
            x = rnd.randrange(2, w - 2 - size); y = rnd.randrange(2, h - 2 - size)
            if not free_zone(x, y, size): continue
            fp = {(x + i, y + j) for j in range(size) for i in range(size)}
            cells1 = walk_cells(g, w, h, taken | fp)
            if reach(cells1, starts) != (base - taken - fp):       # un chemin serait coupe ou une poche isolee creee
                continue
            if any(p not in cells1 for p in ()): continue
            v = kind if isinstance(kind, dict) else None
            if v is not None:
                for (i, j), m in v.items(): g[(y + j) * w + x + i] = 0x400 | m
            else:
                g[y * w + x] = 0x400 | kind[rnd.randrange(2)]
            taken |= fp; placed.append((x, y, size)); n += 1
        print(fl, 'taille', size, 'poses', n, '/', count)
    # sol scintillant : ~7 % du sol plat, hors zones occupees
    ns = 0
    for y in range(h):
        for x in range(w):
            if (x, y) in taken: continue
            v = g[y * w + x]
            if v & 0x3ff == FLOOR and not (v >> 10 & 3) and rnd.random() < 0.07:
                g[y * w + x] = (v & 0xfc00) | SPK[rnd.randrange(3)]; ns += 1
    print(fl, 'scintillements', ns)
    # verification finale : toutes les cases utiles restent accessibles
    cells2 = walk_cells(g, w, h, set())
    after = reach(cells2, starts)
    useful = {p for p in keep if p in base}
    assert useful <= after or all(p in cells2 or p not in cells0 for p in useful), 'chemin coupe'
    assert (base - taken) <= after, 'zone coupee sur ' + fl
    open(L.path, 'wb').write(struct.pack('<%dH' % len(g), *g))
print('tuiles ajoutees', len(tiles), 'metatuiles ajoutes', len(mt) // 16 - NMT)
