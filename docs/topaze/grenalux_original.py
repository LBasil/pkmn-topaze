# Grenalux 100 % original : nouveau plan, nouvelles maisons (dessinees par code), moulin, ruisseau, pont,
# puits, arbres, haies, parterres. Ajoute des tuiles/metatuiles au tileset PalletTown (palette 7, libre).
# A lancer UNE fois depuis la racine du depot, sur un depot propre (voir tools/topaze/maps/README.md).
import struct, math, sys, os, random
from PIL import Image, ImageDraw
sys.path.insert(0, 'tools/topaze/maps')
from mapkit import Layout
D = 'data/tilesets/secondary/pallet_town/'
LID = 'LAYOUT_PALLET_TOWN'
orig = Layout(LID)
ORIG = list(orig.g)                     # carte d'origine (cadre d'arbres conserve)
W_, H_ = orig.w, orig.h

# ------------------------------------------------------------------ palette 7 (16 couleurs)
PAL = [(255, 0, 255),                    # 0 transparent
       (189, 238, 213), (139, 213, 189), # 1 pelouse, 2 pelouse (tache)
       (115, 205, 164), (65, 180, 139), (30, 120, 90),      # 3-5 verts
       (240, 236, 228), (190, 184, 180), (48, 44, 66),      # 6 pierre claire, 7 pierre, 8 contour
       (214, 160, 96), (130, 82, 52), (232, 204, 120),      # 9 bois clair, 10 bois sombre, 11 chaume / sable
       (88, 152, 224), (44, 92, 168),                       # 12 bleu, 13 bleu fonce (toit, eau)
       (216, 76, 60), (150, 44, 48)]                        # 14 rouge, 15 rouge fonce
def newimg(w, h, fill=1):
    im = Image.new('P', (w, h), fill); im.putpalette([c for p in PAL for c in p]); return im
GRASS_PAT = []
_g = orig.metatile_img(662).convert('RGB')
for y in range(16):
    GRASS_PAT.append([1 if _g.getpixel((x, y)) == (189, 238, 213) else 2 for x in range(16)])
def lawn(w, h):
    im = newimg(w, h); px = im.load()
    for y in range(h):
        for x in range(w): px[x, y] = GRASS_PAT[y % 16][x % 16]
    return im

# ------------------------------------------------------------------ registre de tuiles / metatuiles
mt = bytearray(open(D + 'metatiles.bin', 'rb').read()); NMT0 = len(mt) // 16
att = bytearray(open(D + 'metatile_attributes.bin', 'rb').read())
assert NMT0 == 89, 'deja applique ?'
png = Image.open(D + 'tiles.png'); NT0 = (png.size[1] // 8) * 16
assert NT0 == 80
tiles = []
def add_tile(t):
    t = tuple(t)
    if t in tiles: return tiles.index(t)
    tiles.append(t); return len(tiles) - 1
_meta = {}
def meta(block, behavior=0):
    """block : image P 16x16 (couche basse). retourne l'id global du metatuile (>=640)."""
    px = list(block.getdata())
    key = (tuple(px), behavior)
    if key in _meta: return _meta[key]
    ents = []
    for q in range(4):
        x, y = (q % 2) * 8, (q // 2) * 8
        t = block.crop((x, y, x + 8, y + 8))
        ents.append((640 + NT0 + add_tile(list(t.getdata()))) | (7 << 12))
    ents += [0, 0, 0, 0]
    mt.extend(struct.pack('<8H', *ents)); att.extend(struct.pack('<I', behavior))
    _meta[key] = 640 + len(mt) // 16 - 1
    return _meta[key]
def slice_meta(im, bw, bh, behaviors=None):
    out = {}
    for by in range(bh):
        for bx in range(bw):
            b = im.crop((bx * 16, by * 16, bx * 16 + 16, by * 16 + 16))
            out[(bx, by)] = meta(b, (behaviors or {}).get((bx, by), 0))
    return out

# ------------------------------------------------------------------ dessins
def shingles(d, box, c1, c2):
    x0, y0, x1, y1 = box
    for y in range(y0, y1 + 1):
        if (y - y0) % 4 == 3: d.line([(x0, y), (x1, y)], fill=c2)
    for y in range(y0, y1 + 1):
        r = (y - y0) // 4
        for x in range(x0 + (r % 2) * 3, x1 + 1, 6):
            if (y - y0) % 4 < 3: d.point((x, y), fill=c2)
def house(W, R, H, roof, door_col, win_row0=(), planters=(), chimney=None, lamp=True, shutters=True):
    w, h = W * 16, (R + H) * 16
    im = lawn(w, h); d = ImageDraw.Draw(im)
    rl, rd = roof
    rh = R * 16
    # toit en croupe
    pts = [(6, 1), (w - 7, 1), (w - 1, rh - 3), (0, rh - 3)]
    d.polygon(pts, fill=rl, outline=8)
    shingles(d, (3, 3, w - 4, rh - 5), rl, rd)
    d.line([(7, 2), (w - 8, 2)], fill=rd)
    # rebord de toit / ombre
    d.rectangle((0, rh - 3, w - 1, rh - 1), fill=rd, outline=8)
    if chimney is not None:
        cx = chimney * 16 + 9
        d.rectangle((cx, 0, cx + 5, 12), fill=7, outline=8); d.rectangle((cx - 1, 0, cx + 6, 2), fill=6, outline=8)
    # mur
    d.rectangle((2, rh, w - 3, h - 1), fill=6, outline=8)
    d.rectangle((3, h - 3, w - 4, h - 2), fill=7)
    for y in range(rh + 4, h - 3, 4): d.line([(3, y), (w - 4, y)], fill=7)
    for c in win_row0:
        x0 = c * 16 + 3; y0 = rh + 3
        d.rectangle((x0, y0, x0 + 9, y0 + 9), fill=12, outline=8)
        d.line([(x0 + 5, y0 + 1), (x0 + 5, y0 + 8)], fill=6); d.line([(x0 + 1, y0 + 5), (x0 + 8, y0 + 5)], fill=6)
        d.rectangle((x0 - 1, y0 + 10, x0 + 10, y0 + 11), fill=9, outline=8)
        if shutters:
            d.rectangle((x0 - 3, y0, x0 - 2, y0 + 9), fill=rd); d.rectangle((x0 + 11, y0, x0 + 12, y0 + 9), fill=rd)
    for c in planters:
        x0 = c * 16 + 2; y0 = h - 9
        d.rectangle((x0, y0, x0 + 11, y0 + 5), fill=10, outline=8)
        for i, col in enumerate((14, 11, 14, 12, 14, 11)):
            d.point((x0 + 1 + i * 2, y0 - 1), fill=col); d.point((x0 + 1 + i * 2, y0), fill=4)
        d.rectangle((x0 - 1, y0 - 4, x0 + 12, y0 - 3), fill=4) if False else None
    # porte
    dx = door_col * 16
    d.rectangle((dx + 2, h - 16, dx + 13, h - 1), fill=10, outline=8)
    d.rectangle((dx + 4, h - 14, dx + 11, h - 3), fill=9)
    d.line([(dx + 8, h - 14), (dx + 8, h - 3)], fill=10); d.point((dx + 10, h - 8), fill=11)
    d.line([(dx + 3, h - 2), (dx + 12, h - 2)], fill=7); d.rectangle((dx + 1, h - 2, dx + 14, h - 1), fill=7, outline=8)
    if lamp:
        d.rectangle((dx + 6, rh + 3, dx + 9, rh + 8), fill=11, outline=8); d.line([(dx + 7, rh + 1), (dx + 8, rh + 1)], fill=8)
    return im

def museum():
    W, R, H = 5, 2, 2; w, h = W * 16, (R + H) * 16
    im = lawn(w, h); d = ImageDraw.Draw(im)
    d.polygon([(40, 0), (w - 1, 28), (0, 28)], fill=6, outline=8)
    d.polygon([(40, 7), (w - 9, 25), (8, 25)], fill=7)
    d.ellipse((32, 12, 48, 28), fill=13, outline=8); d.ellipse((35, 15, 45, 25), fill=12)
    d.polygon([(40, 15), (42, 20), (39, 18), (41, 22), (38, 22)], fill=6) if False else None
    d.line([(40, 16), (40, 24)], fill=6); d.line([(36, 20), (44, 20)], fill=6)
    d.rectangle((0, 28, w - 1, 33), fill=6, outline=8); d.line([(1, 31), (w - 2, 31)], fill=7)
    d.rectangle((2, 34, w - 3, h - 1), fill=6, outline=8)
    for cx in (6, 22, 58, 74):
        d.rectangle((cx, 34, cx + 7, h - 4), fill=6, outline=8); d.line([(cx + 5, 35), (cx + 5, h - 5)], fill=7)
        d.rectangle((cx - 1, 34, cx + 8, 36), fill=7, outline=8); d.rectangle((cx - 1, h - 5, cx + 8, h - 4), fill=7, outline=8)
    d.rectangle((34, 38, 45, h - 1), fill=8)
    d.rectangle((32, 36, 47, 40), fill=7, outline=8)
    d.rectangle((35, 42, 44, h - 1), fill=10)
    d.line([(40, 42), (40, h - 1)], fill=8); d.point((38, h - 8), fill=11); d.point((42, h - 8), fill=11)
    d.rectangle((26, 40, 29, 52), fill=14, outline=8); d.rectangle((51, 40, 54, 52), fill=14, outline=8)  # bannieres
    d.rectangle((4, h - 3, w - 5, h - 1), fill=7, outline=8); d.rectangle((10, h - 1, w - 11, h - 1), fill=6)
    return im, 5, 4

def windmill():
    w, h = 48, 64
    im = lawn(w, h); d = ImageDraw.Draw(im)
    # ombre
    d.ellipse((4, 56, 44, 63), fill=2)
    # tour (tronc de cone)
    d.polygon([(14, 24), (34, 24), (40, 60), (8, 60)], fill=6, outline=8)
    for y in range(28, 60, 6):
        d.line([(10 + (y - 28) // 8, y), (38 - (y - 28) // 8, y)], fill=7)
        off = 4 if (y // 6) % 2 else 0
        for x in range(14 + off, 36, 8): d.line([(x, y), (x, y + 5)], fill=7)
    d.polygon([(21, 60), (27, 60), (27, 50), (24, 47), (21, 50)], fill=10, outline=8)
    d.polygon([(22, 39), (26, 39), (26, 44), (22, 44)], fill=12, outline=8)
    # toit conique rouge
    d.polygon([(12, 25), (36, 25), (24, 6)], fill=14, outline=8)
    d.polygon([(24, 8), (36, 25), (28, 25)], fill=15)
    d.line([(24, 2), (24, 7)], fill=8)
    # pales (croix)
    hx, hy = 24, 27
    ang = math.radians(20)
    for k in range(4):
        a = ang + k * math.pi / 2
        ex, ey = hx + 22 * math.cos(a), hy + 22 * math.sin(a)
        d.line([(hx, hy), (ex, ey)], fill=10, width=2)
        # voile
        px_, py_ = -math.sin(a), math.cos(a)
        p0 = (hx + 6 * math.cos(a), hy + 6 * math.sin(a))
        p1 = (ex, ey)
        p2 = (ex + 6 * px_, ey + 6 * py_); p3 = (p0[0] + 6 * px_, p0[1] + 6 * py_)
        d.polygon([p0, p1, p2, p3], fill=6, outline=8)
        d.line([p0, p1], fill=10, width=2)
    d.ellipse((hx - 3, hy - 3, hx + 3, hy + 3), fill=9, outline=8)
    return im, 3, 4

def tree():
    w = h = 32
    im = lawn(w, h); d = ImageDraw.Draw(im)
    d.ellipse((3, 22, 29, 31), fill=2)
    d.rectangle((13, 20, 18, 30), fill=10, outline=8); d.line([(15, 22), (15, 29)], fill=9)
    d.ellipse((1, 1, 30, 24), fill=4, outline=5)
    d.ellipse((4, 3, 22, 17), fill=3)
    for (x, y) in ((8, 6), (12, 4), (17, 8), (7, 11), (14, 12)): d.ellipse((x, y, x + 3, y + 2), fill=1)
    for (x, y) in ((20, 17), (13, 19), (24, 12), (6, 18)): d.point((x, y), fill=5); d.point((x + 1, y), fill=5)
    return im, 2, 2

def well():
    w = h = 32
    im = lawn(w, h); d = ImageDraw.Draw(im)
    d.ellipse((2, 14, 29, 30), fill=7, outline=8)
    d.ellipse((5, 16, 26, 27), fill=6, outline=8)
    d.ellipse((8, 18, 23, 25), fill=13); d.ellipse((10, 19, 21, 23), fill=12)
    d.line([(12, 20), (16, 20)], fill=6)
    d.rectangle((4, 4, 6, 24), fill=10, outline=8); d.rectangle((25, 4, 27, 24), fill=10, outline=8)
    d.polygon([(1, 8), (16, 0), (30, 8)], fill=14, outline=8)
    d.line([(4, 6), (16, 2)], fill=15)
    d.line([(16, 8), (16, 15)], fill=10); d.rectangle((14, 14, 18, 17), fill=9, outline=8)
    return im, 2, 2

def lamp():
    im = lawn(16, 16); d = ImageDraw.Draw(im)
    d.ellipse((4, 13, 11, 15), fill=2)
    d.rectangle((7, 5, 8, 14), fill=8)
    d.rectangle((4, 0, 11, 6), fill=11, outline=8); d.rectangle((6, 1, 9, 5), fill=1)
    d.rectangle((3, 12, 12, 14), fill=7, outline=8)
    return im

def hedge(kind):
    im = lawn(16, 16); d = ImageDraw.Draw(im)
    if kind == 'M':   d.rounded_rectangle((0, 3, 15, 14), 3, fill=4, outline=5)
    if kind == 'L':   d.rounded_rectangle((2, 3, 20, 14), 3, fill=4, outline=5)
    if kind == 'R':   d.rounded_rectangle((-5, 3, 13, 14), 3, fill=4, outline=5)
    if kind == 'S':   d.rounded_rectangle((2, 3, 13, 14), 3, fill=4, outline=5)
    for (x, y) in ((3, 5), (7, 7), (11, 5), (5, 10), (10, 10)):
        d.point((x, y), fill=3); d.point((x + 1, y), fill=3)
    if kind == 'M':   d.line([(0, 3), (0, 14)], fill=5); d.line([(15, 3), (15, 14)], fill=5)
    return im

def flowers(seed):
    r = random.Random(seed % 3)
    im = lawn(16, 16); d = ImageDraw.Draw(im)
    for _ in range(5):
        x, y = r.randint(1, 13), r.randint(2, 13)
        c = r.choice([14, 11, 12, 6, 14])
        d.point((x, y + 1), fill=4); d.point((x + 1, y + 1), fill=4)
        for (dx, dy) in ((0, 0), (1, -1), (-1, -1), (0, -2)) if False else ((0, 0), (1, 0), (0, -1), (1, -1)):
            d.point((x + dx, y + dy), fill=c)
        d.point((x, y - 1), fill=c)
        d.point((x, y), fill=11 if c != 11 else 14)
    return im

def fence(kind):
    im = lawn(16, 16); d = ImageDraw.Draw(im)
    if kind == 'H':
        d.rectangle((0, 5, 15, 6), fill=9, outline=None); d.rectangle((0, 10, 15, 11), fill=9)
        d.line([(0, 7), (15, 7)], fill=10); d.line([(0, 12), (15, 12)], fill=10)
        d.rectangle((6, 3, 9, 14), fill=9, outline=8); d.line([(8, 4), (8, 13)], fill=10)
    elif kind == 'V':
        d.rectangle((6, 0, 9, 15), fill=9); d.line([(6, 0), (6, 15)], fill=8); d.line([(9, 0), (9, 15)], fill=8)
        d.rectangle((2, 4, 13, 6), fill=10, outline=8); d.rectangle((2, 10, 13, 12), fill=10, outline=8)
    elif kind == 'E':  # extremite gauche (poteau)
        d.rectangle((3, 3, 6, 14), fill=9, outline=8)
        d.rectangle((7, 5, 15, 6), fill=9); d.rectangle((7, 10, 15, 11), fill=9)
        d.line([(7, 7), (15, 7)], fill=10); d.line([(7, 12), (15, 12)], fill=10)
    elif kind == 'F':  # extremite droite
        d.rectangle((9, 3, 12, 14), fill=9, outline=8)
        d.rectangle((0, 5, 8, 6), fill=9); d.rectangle((0, 10, 8, 11), fill=9)
        d.line([(0, 7), (8, 7)], fill=10); d.line([(0, 12), (8, 12)], fill=10)
    return im

def garden(var):
    im = lawn(16, 16); d = ImageDraw.Draw(im)
    d.rectangle((0, 1, 15, 14), fill=10, outline=8)
    for y in (3, 7, 11): d.line([(1, y), (14, y)], fill=9)
    for y in (4, 8, 12):
        for x in range(2 + (var % 2), 14, 4):
            d.rectangle((x, y - 1, x + 1, y), fill=3 if var < 2 else 14); d.point((x, y - 2), fill=4)
    return im

def sign_board(post=True):
    im = lawn(16, 16); d = ImageDraw.Draw(im)
    d.rectangle((7, 8, 8, 14), fill=10, outline=8)
    d.rectangle((2, 2, 13, 9), fill=9, outline=8); d.line([(4, 5), (11, 5)], fill=10); d.line([(4, 7), (11, 7)], fill=10)
    return im

# ----- cobble (autotile par voisinage)
def cobble_block(pathset, cx, cy):
    """cx, cy : coord. de bloc ; pathset : ensemble des blocs 'chemin' (pour les bords)."""
    im = newimg(16, 16, 6); d = ImageDraw.Draw(im)
    # pavage regulier (periodique)
    for row in range(3):
        y0 = row * 5 + (1 if row else 0)
        d.line([(0, row * 5 + 0), (15, row * 5 + 0)], fill=7)
        off = 4 if row % 2 else 0
        for x in range(off, 16, 8): d.line([(x, row * 5), (x, row * 5 + 4)], fill=7)
        for x in range(off + 1, 16, 8): d.point((x + 2, row * 5 + 2), fill=1)
    d.line([(0, 15), (15, 15)], fill=7)
    N = (cx, cy - 1) in pathset; S = (cx, cy + 1) in pathset; E = (cx + 1, cy) in pathset; Wn = (cx - 1, cy) in pathset
    px = im.load()
    def lip(x, y, depth):  # bord : herbe + ombre
        px[x, y] = 3 if depth == 0 else 7 if depth == 1 else px[x, y]
    for i in range(16):
        if not N:  px[i, 0] = 3; px[i, 1] = 7 if i % 2 else 7
        if not S:  px[i, 15] = 3; px[i, 14] = 7
        if not Wn: px[0, i] = 3; px[1, i] = 7
        if not E:  px[15, i] = 3; px[14, i] = 7
    # coins arrondis
    for (cond, pts) in (((not N) and (not Wn), [(0, 0), (1, 0), (0, 1)]), ((not N) and (not E), [(15, 0), (14, 0), (15, 1)]),
                        ((not S) and (not Wn), [(0, 15), (1, 15), (0, 14)]), ((not S) and (not E), [(15, 15), (14, 15), (15, 14)])):
        if cond:
            for (x, y) in pts: px[x, y] = 1
    return im

# ----- ruisseau (periode 4 blocs) + pont
def brook_canvas(blocks_w=4):
    w, h = blocks_w * 16, 32
    im = lawn(w, h); px = im.load()
    for x in range(w):
        cy = 16 + 3.2 * math.sin(2 * math.pi * x / 64.0)
        for y in range(h):
            dd = abs(y + 0.5 - cy)
            if dd < 6.4: px[x, y] = 12
            if 6.4 <= dd < 7.8: px[x, y] = 11 if (x + y) % 5 else 9      # berge sablonneuse
            elif 7.8 <= dd < 8.6: px[x, y] = 3
        # reflets
    d = ImageDraw.Draw(im)
    for (x, y, l) in ((5, 0, 6), (24, -2, 5), (40, 2, 7), (55, -1, 4), (14, 3, 3), (48, -3, 4)):
        cy = int(16 + 3.2 * math.sin(2 * math.pi * x / 64.0))
        d.line([(x, cy + y), (x + l, cy + y)], fill=6)
        d.line([(x + 2, cy + y + 3), (x + 2 + l, cy + y + 3)], fill=13)
    return im
def bridge_canvas(base):
    im = base.copy(); d = ImageDraw.Draw(im)
    d.rectangle((3, 0, 28, 31), fill=9)
    for y in range(0, 32, 4):
        d.line([(3, y + 3), (28, y + 3)], fill=10)
        d.line([(3, y), (28, y)], fill=11 if (y // 4) % 2 else 9)
    for x in (0, 28):
        d.rectangle((x, 0, x + 3, 31), fill=10, outline=8)
        for y in (3, 15, 27): d.rectangle((x - 0, y, x + 3, y + 3), fill=9, outline=8)
    return im

# ------------------------------------------------------------------ plan de la carte
G = {}                   # (x,y) -> (metatile, collision)  collision = 1 -> infranchissable
LAWN = 662
TOUCH = set()
def put(x, y, m, col=0): G[(x, y)] = (m, col); TOUCH.add((x, y))
for y in range(H_):
    for x in range(W_):
        v = ORIG[y * W_ + x]
        G[(x, y)] = (v & 0x3ff, 1 if (v & 0xc00) else 0)
# zone interieure a repeindre : x 3..20, y 3..16
for y in range(3, 17):
    for x in range(3, 21): put(x, y, LAWN)
for y in range(3, 17):               # colonnes d'ombre laterales
    put(2, y, 686); put(21, y, 663)

PATH = set()
for y in range(0, 9): PATH |= {(12, y), (13, y)}
for x in range(5, 18): PATH.add((x, 8))
for y in range(11, 15):
    for x in range(10, 15): PATH.add((x, y))
for x in range(5, 19): PATH.add((x, 15))
PATH.add((11, 15)); PATH.add((12, 15))
WELL = {(12, 12), (13, 12), (12, 13), (13, 13)}
BRIDGE = {(12, 9), (13, 9), (12, 10), (13, 10)}
PATHALL = PATH | BRIDGE
for (x, y) in PATH:
    if (x, y) in WELL: continue
    # voisins hors-carte (haut) considérés comme chemin
    ps = set(PATHALL)
    ps |= {(12, -1), (13, -1)}
    put(x, y, meta(cobble_block(ps | WELL, x, y)))

def place(im, bx, by, bw, bh, collide=True, behaviors=None, skip=()):
    sm = slice_meta(im, bw, bh, behaviors)
    for (i, j), m in sm.items():
        if (i, j) in skip: continue
        put(bx + i, by + j, m, 1 if collide else 0)

# brook
bk = brook_canvas(); BR = {}
for ty in range(2):
    for tx in range(4):
        BR[(tx, ty)] = meta(bk.crop((tx * 16, ty * 16, tx * 16 + 16, ty * 16 + 16)))
for x in range(2, 22):
    for ty in range(2):
        put(x, 9 + ty, BR[((x - 2) % 4, ty)], 1)
# pont : 2x2 sur le fond du ruisseau
bg = Image.new('P', (32, 32)); bg.putpalette(bk.getpalette())
bg.paste(bk.crop((((12 - 2) % 4) * 16, 0, ((12 - 2) % 4) * 16 + 16, 32)), (0, 0))
bg.paste(bk.crop((((13 - 2) % 4) * 16, 0, ((13 - 2) % 4) * 16 + 16, 32)), (16, 0))
place(bridge_canvas(bg), 12, 9, 2, 2, collide=False)

# batiments
# maison du joueur (toit bleu)
place(house(5, 2, 2, (12, 13), 2, win_row0=(1, 3), planters=(1, 3), chimney=3), 3, 4, 5, 4, behaviors={(2, 3): 0x69})
# ranch (toit rouge, 6 de large)
place(house(6, 2, 2, (14, 15), 2, win_row0=(1, 4), planters=(1, 3, 4), chimney=4), 15, 4, 6, 4, behaviors={(2, 3): 0x69})
# musee
mim, mw, mh = museum()
place(mim, 3, 11, mw, mh, behaviors={(2, 3): 0x69})
# moulin
wim, ww, wh = windmill()
place(wim, 9, 3, ww, wh)
# laboratoire d'origine (decale) : copie des blocs de l'ancienne carte
LABX, LABY = 15, 11
for j in range(4):
    for i in range(7):
        v = ORIG[(10 + j) * W_ + 13 + i]
        put(LABX + i, LABY + j, v & 0x3ff, 1 if (v & 0xc00) else 0)
# puits
wl, _, _ = well()
place(wl, 12, 12, 2, 2)
# arbres (2x2)
tim, _, _ = tree()
TREES = [(8, 12)]
for (tx, ty) in TREES:
    place(tim, tx, ty, 2, 2)
# haies, lampadaires, parterres, cloture, potager
for (x, y) in ((10, 11), (14, 11), (11, 5), (14, 5)): put(x, y, meta(lamp()), 1)
for x in range(3, 9): put(x, 3, meta(flowers(x)), 0)
for x in range(15, 21): put(x, 3, meta(flowers(x + 10)), 0)
for x in (8,): put(x, 4, meta(flowers(40)), 0)
for x in range(9, 12): put(x, 7, meta(flowers(50 + x)), 0)
for (x, y) in ((3, 8), (4, 8), (3, 9 - 1)):
    pass
for x in range(15, 21):
    if (x, 8) not in PATH: put(x, 8, meta(flowers(60 + x)), 0)
for x in range(3, 5): put(x, 8, meta(flowers(70 + x)), 0)
# chemin: les cellules (5..17, 8) sont deja chemin ; fleurs a l'est du ranch
# potager au sud-est (derriere le labo), entoure de cloture
put(19, 16, meta(fence('F')), 1)
for x in range(15, 19): put(x, 16, meta(fence('H')), 1)
put(14, 16, meta(fence('E')), 1)
put(20, 16, meta(garden(2)), 0)
# haies sud-ouest
for x in range(3, 8): put(x, 16, meta(flowers(80 + x)), 0)
# enseignes
put(11, 7, 2, 1)        # panneau de ville (bloc d'origine)
put(8, 7, 685, 1)       # boite aux lettres (maison du joueur)
put(14, 7, 685, 1)      # boite aux lettres (ranch)
put(19, 15, 2, 1)       # panneau du labo
put(4, 15, 3, 1)        # panneau "conseils dresseur"
put(8, 14, 2, 1)        # panneau musee
# bas : ombre et pelouse (cadre d'origine) deja en place; la rangee 16 devant le bassin
for x in range(10, 14): put(x, 16, LAWN, 0)

# ------------------------------------------------------------------ ecriture
rows = (NT0 + len(tiles) + 15) // 16
assert NT0 + len(tiles) <= 384, 'trop de tuiles: %d' % (NT0 + len(tiles))
assert len(mt) // 16 <= 384 + 0, 'trop de metatuiles'
open(D + 'metatiles.bin', 'wb').write(mt); open(D + 'metatile_attributes.bin', 'wb').write(att)
out = Image.new('P', (128, rows * 8), 0); out.putpalette(png.getpalette()); out.paste(png, (0, 0))
for i, t in enumerate(tiles):
    n = NT0 + i; ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, ((n % 16) * 8, (n // 16) * 8))
out.save(D + 'tiles.png')
open(D + 'palettes/07.pal', 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in PAL))
g = []
for y in range(H_):
    for x in range(W_):
        if (x, y) in TOUCH:
            m, col = G[(x, y)]
            g.append(m | (0x400 if col else 0) | (3 << 12))
        else:
            g.append(ORIG[y * W_ + x])
open('data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
print('tuiles ajoutees', len(tiles), 'metatuiles', len(mt) // 16 - NMT0)
# grille de collision pour le calcul des trajets
import json
json.dump({'w': W_, 'h': H_, 'blocked': [[x, y] for y in range(H_) for x in range(W_) if (g[y * W_ + x] & 0xc00) or ((g[y * W_ + x] >> 12) == 1)]},
          open('/tmp/grenalux_col.json', 'w'))
