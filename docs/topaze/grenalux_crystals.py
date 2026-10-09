# Cristaux de grenat de Grenalux (dessines par code) : grappe geante, grappe moyenne, petits cristaux.
# Ajoute des tuiles/metatuiles au tileset PetalburgEmerald (palette secondaire 7, libre) et les pose dans map.bin.
# Ordre de regeneration : import_emerald_tiles.py -> grenat_palette.py -> grenalux_emerald.py -> grenalux_crystals.py
import struct, sys, math, collections
from PIL import Image, ImageDraw
sys.path.insert(0, 'tools/topaze/maps')
from mapkit import Layout
D = 'data/tilesets/secondary/petalburg_emerald/'
lay = Layout('LAYOUT_PALLET_TOWN')
ground = lay.metatile_img(1).convert('RGB')
cnt = collections.Counter(ground.getdata())
gcols = [c for c, _ in cnt.most_common(4)]
while len(gcols) < 4: gcols.append(gcols[-1])
PAL = [(0, 0, 0)] + gcols + [(48, 6, 26), (112, 14, 44), (176, 28, 62), (226, 70, 96), (255, 176, 196),
                              (255, 255, 255), (90, 40, 84), (60, 20, 50), (150, 52, 120), (20, 4, 14), (255, 120, 150)]
# indices : 1-4 sol | 5 contour | 6 grenat sombre | 7 grenat | 8 clair | 9 reflet | 10 blanc | 11 ombre | 12 prune | 13 violet | 14 noir
def newimg(w, h):
    im = Image.new('P', (w, h), 1); im.putpalette([c for p in PAL for c in p]); return im
def ground_bg(w, h):
    im = newimg(w, h); px = im.load(); g = ground.load()
    for y in range(h):
        for x in range(w):
            c = g[x % 16, y % 16]; px[x, y] = 1 + gcols.index(c) if c in gcols else 1
    return im
def prism(d, cx, base, hw, h, tilt=0):
    """cristal hexagonal : facette gauche (7), droite (6), pointe claire (8)."""
    top = base - h
    L, R = cx - hw, cx + hw
    tx = cx + tilt
    d.polygon([(L, base), (L, top + hw), (tx, top), (R, top + hw), (R, base), (cx, base + hw // 2)], fill=7, outline=5)
    d.polygon([(cx, base + hw // 2), (cx, top + 3), (R, top + hw), (R, base)], fill=6)
    d.polygon([(L + 1, top + hw), (tx, top + 1), (cx, top + 3), (cx - 1, base - 1), (L + 1, base - 1)], fill=7)
    d.polygon([(tx, top + 1), (tx + 3 + hw // 2, top + hw - 1), (cx, top + hw + 2)], fill=8)
    d.line([(L + 2, top + hw + 2), (L + 2, base - 4)], fill=9)
    d.point((tx, top + 2), fill=10)
def shadow(d, x0, y0, x1, y1): d.ellipse((x0, y0, x1, y1), fill=11)
def big():
    w, h = 48, 48
    im = ground_bg(w, h); d = ImageDraw.Draw(im)
    shadow(d, 1, 36, 47, 47)
    prism(d, 10, 42, 6, 20, -2); prism(d, 38, 43, 6, 18, 2)
    prism(d, 24, 44, 9, 40, 1)
    prism(d, 15, 44, 5, 28, -1); prism(d, 33, 45, 5, 26, 1)
    for (x, y) in ((22, 14), (30, 22), (12, 26), (36, 28)): d.point((x, y), fill=10); d.point((x + 1, y), fill=9)
    return im, 3, 3
def mid():
    w, h = 32, 32
    im = ground_bg(w, h); d = ImageDraw.Draw(im)
    shadow(d, 1, 24, 31, 31)
    prism(d, 9, 29, 5, 14, -1); prism(d, 23, 29, 5, 12, 1); prism(d, 16, 30, 7, 25)
    d.point((15, 8), fill=10); d.point((20, 16), fill=9)
    return im, 2, 2
def small(var):
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 2, 11, 14, 15)
    if var == 0: prism(d, 8, 13, 4, 10)
    else: prism(d, 5, 13, 3, 7, -1); prism(d, 11, 13, 3, 9, 1)
    return im

def lamp():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 3, 12, 13, 15)
    d.rectangle((7, 7, 8, 14), fill=12); d.rectangle((5, 13, 10, 14), fill=14)
    d.polygon([(8, 0), (11, 3), (11, 7), (8, 9), (5, 7), (5, 3)], fill=7, outline=5)
    d.polygon([(8, 1), (10, 3), (8, 5), (6, 3)], fill=8); d.point((7, 3), fill=10)
    d.point((3, 4), fill=15); d.point((13, 5), fill=15); d.point((8, 11), fill=11)
    return im
def boulder(var):
    w = h = 32
    im = ground_bg(w, h); d = ImageDraw.Draw(im)
    shadow(d, 2, 24, 31, 31)
    d.ellipse((1, 5, 30, 29), fill=11, outline=14)
    d.pieslice((3, 7, 28, 27), 200, 330, fill=13)
    d.ellipse((6, 12, 27, 27), fill=11)
    d.arc((2, 6, 29, 28), 150, 300, fill=13)
    d.arc((4, 12, 29, 29), 20, 130, fill=12)
    if var == 0: veins = [(9, 13), (12, 16), (10, 18), (21, 20)]
    else: veins = [(20, 11), (22, 14), (18, 16), (9, 21)]
    for (x, y) in veins:
        d.polygon([(x, y - 3), (x + 2, y - 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y - 1)], fill=7, outline=5)
        d.point((x, y - 1), fill=9)
    return im, 2, 2
def rock():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 1, 11, 15, 15)
    d.ellipse((1, 4, 14, 14), fill=11, outline=14); d.arc((2, 5, 13, 13), 180, 300, fill=13)
    d.point((9, 9), fill=8)
    return im
def mine():
    w, h = 48, 48
    im = ground_bg(w, h); d = ImageDraw.Draw(im)
    d.polygon([(0, 47), (0, 24), (7, 12), (18, 5), (30, 5), (41, 12), (47, 24), (47, 47)], fill=11, outline=14)
    d.polygon([(4, 24), (10, 14), (19, 8), (28, 8)], fill=13)
    for (x, y) in ((8, 20), (13, 10), (36, 16), (40, 28), (6, 34), (42, 38)):
        d.polygon([(x, y - 3), (x + 2, y - 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y - 1)], fill=7, outline=5); d.point((x, y - 1), fill=9)
    for y in (30, 38): d.line([(2, y), (14, y + 2)], fill=12); d.line([(34, y + 2), (45, y)], fill=12)
    d.rectangle((13, 20, 34, 47), fill=12, outline=14)                 # cadre en bois sombre
    d.rectangle((16, 24, 31, 47), fill=14)                              # ouverture
    d.pieslice((16, 20, 31, 32), 180, 360, fill=14)
    d.rectangle((13, 20, 34, 23), fill=6, outline=14)                   # linteau
    d.line([(14, 21), (33, 21)], fill=7)
    d.rectangle((13, 24, 15, 47), fill=6, outline=14); d.rectangle((32, 24, 34, 47), fill=6, outline=14)
    d.rectangle((22, 14, 25, 19), fill=11); d.polygon([(23, 9), (26, 12), (23, 15), (20, 12)], fill=8, outline=5)   # cristal-enseigne
    d.line([(17, 44), (30, 44)], fill=13); d.line([(17, 47), (30, 47)], fill=13)
    return im, 3, 3

def fence_h():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 0, 12, 15, 15)
    for y in (5, 9): d.rectangle((0, y, 15, y + 1), fill=13, outline=14); d.line([(0, y), (15, y)], fill=15)
    for x in (0, 7, 14): d.rectangle((x, 2, x + 1, 13), fill=12, outline=14); d.point((x, 3), fill=13)
    return im
def fence_v():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 4, 12, 12, 15)
    d.rectangle((6, 0, 9, 15), fill=12, outline=14); d.line([(7, 0), (7, 15)], fill=13)
    d.rectangle((3, 3, 12, 4), fill=13, outline=14); d.rectangle((3, 9, 12, 10), fill=13, outline=14)
    return im
def hay():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 0, 11, 15, 15)
    d.rectangle((1, 4, 14, 13), fill=8, outline=14)
    for y in (6, 8, 10, 12): d.line([(2, y), (13, y)], fill=15)
    d.line([(5, 4), (5, 13)], fill=12); d.line([(10, 4), (10, 13)], fill=12)
    return im
def trough():
    im = ground_bg(16, 16); d = ImageDraw.Draw(im)
    shadow(d, 0, 11, 15, 15)
    d.rectangle((1, 6, 14, 12), fill=12, outline=14); d.rectangle((3, 7, 12, 9), fill=13); d.line([(4, 8), (7, 8)], fill=9)
    d.line([(2, 13), (2, 14)], fill=14); d.line([(13, 13), (13, 14)], fill=14)
    return im
# ---- registre
mt = bytearray(open(D + 'metatiles.bin', 'rb').read()); att = bytearray(open(D + 'metatile_attributes.bin', 'rb').read())
NMT = len(mt) // 16
png = Image.open(D + 'tiles.png'); NT = (png.size[1] // 8) * 16
tiles = []
def add_tile(t):
    t = tuple(t)
    if t in tiles: return tiles.index(t)
    tiles.append(t); return len(tiles) - 1
def meta(block):
    ents = []
    for q in range(4):
        x, y = (q % 2) * 8, (q // 2) * 8
        ents.append((640 + NT + add_tile(list(block.crop((x, y, x + 8, y + 8)).getdata()))) | (7 << 12))
    ents += [0, 0, 0, 0]
    mt.extend(struct.pack('<8H', *ents)); att.extend(struct.pack('<I', 0))
    return 640 + len(mt) // 16 - 1
def slice_all(im, bw, bh): return {(i, j): meta(im.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))) for j in range(bh) for i in range(bw)}
BIG = slice_all(*big()); MID = slice_all(*mid()); SM = [meta(small(0)), meta(small(1))]
LAMP = meta(lamp()); BOUL = [slice_all(*boulder(0)), slice_all(*boulder(1))]; ROCK = meta(rock()); MINE = slice_all(*mine())
FENCE_H = meta(fence_h()); FENCE_V = meta(fence_v()); HAY = meta(hay()); TROUGH = meta(trough())
assert NT + len(tiles) <= 384, NT + len(tiles)
open(D + 'metatiles.bin', 'wb').write(mt); open(D + 'metatile_attributes.bin', 'wb').write(att)
rows = (NT + len(tiles) + 15) // 16
out = Image.new('P', (128, rows * 8), 0); out.putpalette(png.getpalette()); out.paste(png, (0, 0))
for i, t in enumerate(tiles):
    n = NT + i; ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, ((n % 16) * 8, (n // 16) * 8))
out.save(D + 'tiles.png')
open(D + 'palettes/07.pal', 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in PAL))
if __name__ == '__main__':
    # ---- carte
    W = lay.w
    g = list(lay.g)
    GR = 0x3000 | 1
    def setc(x, y, v): g[y * W + x] = v
    def clear(x, y, w, h):
        for j in range(h):
            for i in range(w): setc(x + i, y + j, GR)
    def place(sm, x, y, bw, bh):
        for (i, j), m in sm.items(): setc(x + i, y + j, 0x400 | m)
    clear(9, 3, 2, 4); clear(14, 4, 2, 2); clear(9, 12, 2, 2); clear(10, 14, 2, 2)           # ancien arbres remplaces
    place(BIG, 9, 3, 3, 3)
    place(BIG, 9, 11, 3, 3)
    place(MID, 14, 4, 2, 2)
    for (x, y, v) in ((3, 9, 0), (11, 9, 1), (20, 8, 0), (15, 16, 1), (8, 16, 0), (4, 12, 1)):
        if g[y * W + x] & 0xff == 0 or True: setc(x, y, 0x400 | SM[v])
    open('data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
    print('tuiles', len(tiles), 'metatuiles', len(mt) // 16 - NMT)
