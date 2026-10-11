# ROUTE 22 « la route de la Ligue » : meme principe que les Routes 24/25 (generateur route24_dress.py) : falaises mauves, 10 ans d'abandon -> foret dense,
# sentier sinueux (Dijkstra a couts aleatoires) vers chaque evenement, arbres d'Emeraude 2x3 + buissons + herbe haute + cristaux ; portail de la Ligue delabre.
# Idempotent : part de docs/topaze/route22_src/map22_orig.bin. Lancer depuis la racine : python3 docs/topaze/route22_dress.py
import struct, json, random, sys, os, shutil, math, colorsys, collections, heapq
from PIL import Image, ImageDraw
sys.path.insert(0, 'tools/topaze/maps')
import mapkit
SRC = 'docs/topaze/route22_src/'
FRP = 'data/tilesets/primary/general/'; FRS = 'data/tilesets/secondary/viridian_city/'
NP = 'data/tilesets/primary/general_opalroad/'; NS = 'data/tilesets/secondary/viridian_pepite/'
for src, dst in ((FRP, NP), (FRS, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16): shutil.copy(src + 'palettes/%02d.pal' % i, dst + 'palettes/%02d.pal' % i)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
# ------------------------------------------------------------------ couleurs : falaises rosees -> mauve de tourmaline
def tint_opal(c):      # meme teinte que la Route 1 -> Opanihrum : verts -> sarcelle sombre, le reste -> ardoise bleu-nuit ; rouges/violets vifs conserves
    r, g, b = c; h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.10 and l > 0.93: return c
    if s > 0.45 and (h >= 180 or h < 25): return c
    if 78 <= h <= 175: h = 168 + (h - 120) * 0.12; s = min(1, s * 0.5); l = l * 0.8
    else: h = 232; s = min(0.42, s * 0.55 + 0.10); l = min(1, l * 0.72)
    return rgb(h, l, s)
for i in range(6):     # palettes primaires 0..5 (sol, arbres, falaises, eau, ...) -> opale
    pp = readpal(NP + 'palettes/%02d.pal' % i); writepal(NP + 'palettes/%02d.pal' % i, [pp[0]] + [tint_opal(c) for c in pp[1:16]])
def decay(c):
    h, l, s = hls(c)
    if s < 0.05 and l > 0.93: return (176, 172, 150)        # blanc -> crepi sale
    return rgb(h, l * 0.72, s * 0.6)                        # reste : ternes, fanes
for i in (9, 12):      # portail de la Ligue (palettes secondaires 9 et 12, seulement le portail) : delabre par 10 ans d'abandon
    pp = readpal(NS + 'palettes/%02d.pal' % i); writepal(NS + 'palettes/%02d.pal' % i, [pp[0]] + [decay(tint_opal(c)) for c in pp[1:15]] + [pp[15]])
# ------------------------------------------------------------------ tilesets : etat de depart (le secondaire recoit l'art + le pont)
smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = bytearray(open(NS + 'metatile_attributes.bin', 'rb').read())
NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
pmt = open(NP + 'metatiles.bin', 'rb').read(); patt = open(NP + 'metatile_attributes.bin', 'rb').read()
NEWT = []; ENTS = []; ENTATT = []
def add_tile(t):
    t = tuple(t)
    if t in NEWT: return NEWT.index(t)
    NEWT.append(t); return len(NEWT) - 1
def slice4(im): return [add_tile([im.getpixel((((q % 2) * 8 + i), (q // 2) * 8 + j)) for j in range(8) for i in range(8)]) for q in range(4)]
NEWM = {}
def new_meta(entries, att=0, key=None):
    if key is not None and key in NEWM: return NEWM[key]
    ENTS.append(list(entries)); ENTATT.append(att); m = 640 + NMT + len(ENTS) - 1
    if key is not None: NEWM[key] = m
    return m
def raw_entries(m):
    if m >= 640 + NMT: return list(ENTS[m - 640 - NMT])
    return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
def raw_attr(m):
    if m >= 640 + NMT: return ENTATT[m - 640 - NMT]
    return struct.unpack('<I', patt[m * 4:m * 4 + 4] if m < 640 else bytes(satt[(m - 640) * 4:(m - 640) * 4 + 4]))[0]
def bottom_of(m): return raw_entries(m)[:4]
ART_PAL, MIX_PAL = 7, 8      # 7 : cristaux ; 8 : arbres (idx 1..6) + pont (idx 7..15)
# ------------------------------------------------------------------ SPRITES
GRASS_BG = (115, 205, 164)
def clean_specks(im, passes=2):
    px = im.load(); w, h = im.size
    for _ in range(passes):
        kill = []
        for y in range(h):
            for x in range(w):
                if px[x, y][3] == 0: continue
                n = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3])
                if n <= 1: kill.append((x, y))
        for c in kill: px[c] = (0, 0, 0, 0)
    return im
TREE_OUT = (57, 82, 0, 255)
DOME = [6, 9, 12, 14, 16, 18, 19, 20]          # largeurs des 8 rangs de la cime arrondie (du sommet vers le corps)
def make_tree():
    """Arbre d'Emeraude entier, 32x48 = 2 cases de large x 3 de haut (la cime deborde sur la case du dessus, comme dans Emeraude).
    Le 2x2 d'origine (468/469/476/477) est un arbre EMPILE : haut de cime coupe, 3 derniers rangs = pic de l'arbre suivant, halo turquoise.
    On garde le corps (rangs 0..28), on retire halo + pixels isoles, et on dessine un dome arrondi (texture echantillonnee sur le corps) au-dessus."""
    T = Image.open(SRC + 'tree_emerald_raw.png').convert('RGBA'); tp = T.load()
    for y in range(32):
        for x in range(32):
            if tp[x, y][3]:
                h, l, s = hls(tp[x, y][:3])
                if 140 <= h <= 170 and s > 0.3: tp[x, y] = (0, 0, 0, 0)
    body = T.crop((0, 0, 32, 29)); bp = body.load()
    R = Image.new('RGBA', (32, 48), (0, 0, 0, 0)); R.paste(body, (0, 16)); rp = R.load(); top = 16 - len(DOME)
    for r, w in enumerate(DOME):
        x0 = 16 - w // 2; x1 = x0 + w - 1
        for x in range(x0, x1 + 1):
            c = bp[x, 1 + ((r * 3 + x // 2) % 9)]
            rp[x, top + r] = c if c[3] else bp[16, 5]
        rp[x0, top + r] = TREE_OUT; rp[x1, top + r] = TREE_OUT
    for x in range(32):
        if rp[x, top][3]: rp[x, top] = TREE_OUT
    return clean_specks(R)
PAL_C = [(0, 0, 0), (6, 8, 20), (18, 22, 46), (36, 44, 86), (80, 96, 160), (150, 170, 230), (236, 242, 255), (120, 70, 200), (255, 104, 186),
         (70, 240, 218), (236, 255, 250), (14, 22, 36), (40, 32, 50), (70, 76, 98), (40, 44, 66), (255, 232, 136)]
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
def cluster(var=0):     # 2x2 : grand amas de cristaux, TOUT le 32x32 occupe (haut ET bas ; plus de sprite « seulement en bas »)
    im = newimg(32, 32); d = ImageDraw.Draw(im); shadow(d, 1, 26, 31, 32)
    if var == 0: prism(d, 6, 29, 7, 20); prism(d, 26, 30, 8, 23); prism(d, 16, 31, 12, 29); d.rectangle((1, 28, 4, 30), fill=13); d.point((2, 27), fill=14)
    else: prism(d, 6, 30, 7, 21); prism(d, 15, 31, 10, 29); prism(d, 26, 29, 7, 19); d.rectangle((26, 28, 30, 30), fill=13); d.point((28, 27), fill=14)
    return im
TREE_RGBA = make_tree()
_px = TREE_RGBA.load()
for _y in range(TREE_RGBA.height):
    for _x in range(TREE_RGBA.width):
        if _px[_x, _y][3]: _px[_x, _y] = tint_opal(_px[_x, _y][:3]) + (255,)
tcols = collections.Counter(p[:3] for p in TREE_RGBA.getdata() if p[3])
TREE_COLS = [c for c, n in tcols.most_common()]
assert len(TREE_COLS) <= 6, ('arbre : trop de teintes', len(TREE_COLS))
MIXP = [GRASS_BG] + TREE_COLS + [(0, 0, 0)] * (15 - len(TREE_COLS))
assert len(MIXP) == 16
def idx_of(c, lo, hi): return min(range(lo, hi), key=lambda k: sum((MIXP[k][i] - c[i]) ** 2 for i in range(3)))
TREE_P = newimg(32, 48); tq = TREE_P.load(); tpx = TREE_RGBA.load()
for y in range(48):
    for x in range(32):
        if tpx[x, y][3]: tq[x, y] = idx_of(tpx[x, y][:3], 1, 1 + len(TREE_COLS))
TREE_PF = TREE_P.transpose(Image.FLIP_LEFT_RIGHT)
MAPS = [dict(name='Route22', W=48, H=24, src=SRC + 'map22_orig.bin', start=(46, 7), seed=2207, ntree=60, nclus=7, clus_gap=6, xmax=99, plain={1, 8, 9, 16, 17}, bg_ring=0, align=0)]
OUT = {}
for CFG in MAPS:
    # ------------------------------------------------------------------ carte
    W, H = CFG['W'], CFG['H']
    G = {(x, y): v for (x, y), v in zip(((x, y) for y in range(H) for x in range(W)), struct.unpack('<%dH' % (W * H), open(CFG['src'], 'rb').read()))}
    G0 = dict(G)
    def beh(m): return raw_attr(m) & 0x1ff
    WATER = {0x10, 0x11, 0x12, 0x15}
    def blocked(c, g=None):
        v = (g or G)[c]; return bool(v & 0xc00) or beh(v & 0x3ff) in WATER
    obj = json.load(open('data/maps/%s/map.json' % CFG['name']))
    RES = set(); EVC = []
    for o in obj['object_events']: EVC.append((o['x'], o['y']))
    for w_ in obj['warp_events']: EVC.append((w_['x'], w_['y']))
    BGC = {(b_['x'], b_['y']) for b_ in obj['bg_events']}
    for b_ in obj['bg_events']: EVC.append((b_['x'], b_['y']))
    for c_ in obj['coord_events']: EVC.append((c_['x'], c_['y']))
    for (ex, ey) in EVC:
        r_ = CFG['bg_ring'] if (ex, ey) in BGC else 1
        for a in range(-r_, r_ + 1):
            for b in range(-r_, r_ + 1):
                if (a != 0 and b != 0): continue     # foret dense : croix seulement
                RES.add((ex + a, ey + b))
    def flood(g, s0):
        seen = {s0}; q = collections.deque([s0])
        while q:
            c = q.popleft()
            for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n, g): seen.add(n); q.append(n)
        return seen
    START = CFG['start']
    R0 = flood(G0, START)
    GRASSM = {1, 4, 8, 9, 16, 17}
    def mid(c): return G[c] & 0x3ff
    def gm(x, y): return 8 + (x % 2) + 8 * (y % 2)
    CONV = set()                         # cases volontairement converties (eau, etc.)
    def setm(c, m, flags=None):
        G[c] = ((G0[c] & 0xf000) if flags is None else flags) | m
    # --- ancien sable (routes de gravier) -> herbe : 10 ans d'abandon, le chemin a disparu sous la vegetation
    SAND = {354, 355, 356, 362, 363, 364, 370, 371, 372, 211, 212, 213, 219, 220, 221, 227, 228, 229, 261}
    for c in sorted(G0):
        if G0[c] & 0x3ff in SAND: setm(c, gm(*c))
    PLAIN = CFG['plain']; PLAIN.update({4, 13})
    # ------------------------------------------------------------------ vegetation par bruit de densite
    def lattice(seed, n=64):
        r = random.Random(seed); return [[r.random() for _ in range(n)] for _ in range(n)]
    LA, LB = lattice(51), lattice(52)
    def sm(t): return t * t * (3 - 2 * t)
    def vn(L, x, y):
        x0, y0 = int(math.floor(x)), int(math.floor(y)); fx, fy = sm(x - x0), sm(y - y0)
        a = L[y0 % 64][x0 % 64]; b = L[y0 % 64][(x0 + 1) % 64]; c = L[(y0 + 1) % 64][x0 % 64]; d = L[(y0 + 1) % 64][(x0 + 1) % 64]
        return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy
    def dens(x, y): return 0.62 * vn(LA, x / 4.5, y / 4.5) + 0.38 * vn(LB, x / 2.2 + 9, y / 2.2 + 4)
    PLAIN = CFG['plain']
    KEEPS = set()          # sentier a garder libre (foret dense)
    def grass(c): return c in G and c[0] <= CFG['xmax'] and mid(c) in PLAIN and not blocked(c) and c not in RES and c not in CONV and c not in OVER and c not in KEEPS
    def edgeness(c):       # proximite d'une falaise / eau / haie : les arbres aiment les lisieres
        n = 0
        for a in range(-2, 3):
            for b in range(-2, 3):
                k = (c[0] + a, c[1] + b)
                if k in G and k != c and (blocked(k) or mid(k) in (113, 114, 117, 112, 115, 343, 318)): n += 1
        return min(1.0, n / 9.0)
    ARTP = {}; OVER = {}; TREES = []; CLUS = []; SHARDS = []     # OVER : cimes qui debordent sur la case du dessus (calque haut, case praticable)
    def reach_ok(new, relax=False):       # poser ces cases bloquees ne doit isoler aucune case d'origine encore praticable (verifie a chaque pose)
        seen = {START}; q = collections.deque([START]); nb = set(new)
        while q:
            c = q.popleft()
            for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if n in G and n not in seen and not blocked(n) and n not in ARTP and n not in nb: seen.add(n); q.append(n)
        return all(c in seen for c in (EVC if relax else R0) if c not in CONV and c not in ARTP and c not in nb and c in R0 and not blocked(c))
    def tile_ent(t4, slot): return [(640 + NTL + t) | (slot << 12) for t in t4]
    def art_meta(tiles4, slot, bottom):
        key = (tuple(tiles4), slot, tuple(bottom)); return new_meta(list(bottom) + tile_ent(tiles4, slot), 0, key)
    def free_ring(cells, r=1):
        xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
        return {(x, y) for x in range(min(xs) - r, max(xs) + r + 1) for y in range(min(ys) - r, max(ys) + r + 1)} - set(cells)
    ABOVE_OK = {113, 121, 122, 123, 124, 125, 105, 106, 107, 108, 109, 112, 114, 115, 117, 120, 178, 179, 186, 187, 4, 13}
    def put_big(x, y, img, kind, relax=False):
        cells = [(x + i, y + j) for j in range(2) for i in range(2)]
        if not all(grass(c) and c not in ARTP for c in cells): return False
        tall = img.height == 48                      # arbre : la cime deborde sur la case du dessus (herbe libre exigee)
        above = [(x + i, y - 1) for i in range(2)]
        if tall and not all(c in G and (mid(c) in (PLAIN | {1, 4, 217}) and not blocked(c) or (relax and mid(c) in ABOVE_OK)) and c not in RES and c not in CONV and c not in ARTP and c not in OVER for c in above): return False
        ring = free_ring(cells)
        if not relax and (sum(1 for c in ring if c in ARTP) > (3 if kind == 'tree' else 0) or sum(1 for c in ring if c in G and not blocked(c) and c not in ARTP) < 3): return False
        if not reach_ok(cells): return False
        off = 16 if tall else 0
        for j in range(2):
            for i in range(2):
                ARTP[(x + i, y + j)] = (slice4(img.crop((i * 16, off + j * 16, i * 16 + 16, off + j * 16 + 16))), MIX_PAL if kind == 'tree' else ART_PAL, mid((x + i, y + j)))
        if tall:
            for i in range(2): OVER[above[i]] = (slice4(img.crop((i * 16, 0, i * 16 + 16, 16))), MIX_PAL)
        (TREES if kind == 'tree' else CLUS).append((x, y)); return True
    def put_small(c, var):
        if not grass(c) or c in ARTP or not reach_ok([c]): return False
        ARTP[c] = (slice4(small(var)), ART_PAL, mid(c)); SHARDS.append(c); return True
    rnd = random.Random(CFG['seed'])
    if True:       # foret abandonnee : reseau de sentiers sinueux (Dijkstra a couts bruites) libre, tout le reste envahi d'arbres
        cost = {c: 1.0 + 5.0 * dens(c[0] * 1.2 + 3, c[1] * 1.2 + 8) for c in G}
        dist = {START: 0.0}; prev = {}; pq = [(0.0, START)]
        while pq:
            d_, c = heapq.heappop(pq)
            if d_ > dist.get(c, 1e9): continue
            for dx, dy in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                n = (c[0] + dx, c[1] + dy)
                if n in G and not blocked(n):
                    nd = d_ + cost[n]
                    if nd < dist.get(n, 1e9): dist[n] = nd; prev[n] = c; heapq.heappush(pq, (nd, n))
        tg = [c for c in EVC if c in dist]
        rk = random.Random(2214); KEEPS.update(tg)
        for t in tg:
            c = t
            while c in prev:
                KEEPS.add(c)
                for dx, dy in ((0, 1), (1, 0)):
                    n = (c[0] + dx, c[1] + dy)
                    if n in G and not blocked(n) and rk.random() < 0.6: KEEPS.add(n)
                c = prev[c]
    # amas de cristaux : au pied des falaises / de l'eau, hors des cases d'arbre
    ccand = []
    for y in range(H - 1):
        for x in range(W - 1):
            cs = [(x + i, y + j) for j in range(2) for i in range(2)]
            if all(grass(c) and c not in ARTP for c in cs):
                ccand.append((0.7 * edgeness((x, y)) + 0.3 * rnd.random(), x, y))
    ccand.sort(reverse=True)
    for sc, x, y in ccand:
        if len(CLUS) >= CFG['nclus']: break
        if all(max(abs(cx - x), abs(cy - y)) >= CFG['clus_gap'] for cx, cy in CLUS) and True:
            put_big(x, y, cluster(len(CLUS) % 2), 'crystal')
    if True:
        rf = random.Random(2512); fc = [(x, y) for y in range(1, H - 1) for x in range(0, W - 1)]; nf = 0
        for _pass in range(4):
            rf.shuffle(fc)
            for (x, y) in fc:
                if rf.random() < 0.05: continue
                if any(abs(ty - y) <= 1 and abs(tx - x) in (3, 4, 5) for tx, ty in TREES) or any(abs(tx - x) <= 1 and abs(ty - y) in (3, 4, 5) for tx, ty in TREES): continue
                if put_big(x, y, TREE_P if rf.random() < 0.5 else TREE_PF, 'tree', relax=True): nf += 1
        BUSH = set(); rb = random.Random(2513)
        for (x, y) in sorted(fc):
            c = (x, y)
            if grass(c) and c not in ARTP and rb.random() < 0.4 + 0.6 * dens(x * 1.5, y * 1.5) and reach_ok([c]):
                BUSH.add(c); G[c] = (G0[c] & 0xf000) | 0x400 | 5
        print('foret', nf, 'sentier', len(KEEPS), 'buissons', len(BUSH))
    # arbres : meilleurs scores d'abord, quinconce (jamais alignes en ligne/colonne), bosquets la ou le bruit est fort
    cand = []
    for y in range(H - 1):
        for x in range(W - 1):
            cs = [(x + i, y + j) for j in range(2) for i in range(2)]
            if all(grass(c) for c in cs):
                sc = dens(x + 1, y + 1) + 0.45 * edgeness((x, y)) + 0.1 * rnd.random()
                cand.append((sc, x, y))
    cand.sort(reverse=True)
    def tree_ok(x, y):
        for (tx, ty) in TREES:
            dx, dy = abs(tx - x), abs(ty - y)
            if max(dx, dy) < 2: return False
            if (dx == 0 or dy == 0) and max(dx, dy) <= 3: return False          # pas d'alignement
            al = CFG['align']
            if al and ((dy <= 1 and dx <= al) or (dx <= 1 and dy <= al)): return False   # ni rangees ni files quasi alignees
        return True
    NTREE = CFG['ntree']; REJ = collections.Counter()
    for sc, x, y in cand:
        if len(TREES) >= NTREE or sc < 0.3: break
        if tree_ok(x, y):
            if not put_big(x, y, TREE_P if rnd.random() < 0.5 else TREE_PF, 'tree'): REJ['put_big'] += 1
        else: REJ['tree_ok'] += 1
    # colonies : quelques eclats autour des amas (1 a 3), plus de rares eclats isoles
    for (cx, cy) in CLUS:
        spots = [(cx + a, cy + b) for a in range(-2, 4) for b in range(-2, 4) if (a, b) not in ((0, 0), (1, 0), (0, 1), (1, 1))]
        rnd.shuffle(spots)
        for c in spots[:rnd.randint(1, 3)]: put_small(c, rnd.randrange(3))
    for c in sorted(G):
        if grass(c) and c not in ARTP and rnd.random() < 0.07 and not any((c[0] + a, c[1] + b) in ARTP for a in (-1, 0, 1) for b in (-1, 0, 1)): put_small(c, rnd.randrange(3))
    for c in sorted(G):
        if grass(c) and c not in ARTP and dens(c[0] * 1.7 + 30, c[1] * 1.7 + 7) > 0.64 and rnd.random() < 0.75: setm(c, 4)
    if True:       # herbe haute en nappes, fleurs, eclats : jamais de bande propre
        ra = random.Random(2510)
        def old(c): return c in G and mid(c) in (PLAIN | {1}) and not blocked(c) and c not in RES and c not in CONV and c not in ARTP and c not in OVER
        for c in sorted(G):
            if not old(c): continue
            r = ra.random(); dn = dens(c[0] * 1.3 + 5, c[1] * 1.3 + 11)
            if dn > 0.47 and r < 0.72: setm(c, 13)
            elif r < 0.22: setm(c, 4)
        for c in sorted(G):
            if old(c) and ra.random() < 0.06 and reach_ok([c]) and not any((c[0] + a, c[1] + b) in ARTP for a in (-1, 0, 1) for b in (-1, 0, 1)):
                ARTP[c] = (slice4(small(ra.randrange(3))), ART_PAL, mid(c)); SHARDS.append(c)
    # pose finale des metatuiles d'art (collision : tout bloque ; les cimes qui debordent restent praticables)
    for c, (t4, slot) in OVER.items(): G[c] = (G[c] & 0xfc00) | art_meta(t4, slot, bottom_of(mid(c)))
    for c, (t4, slot, m) in ARTP.items(): G[c] = (G0[c] & 0xf000) | 0x400 | art_meta(t4, slot, bottom_of(m))
    # ------------------------------------------------------------------ verifications
    R1 = flood(G, START)
    lost = {c for c in R0 if c not in R1 and c not in ARTP and c not in CONV and c not in BUSH}
    if lost: print('LOST', sorted(lost)[:10], [(n, hex(G[n]), n in ARTP, n in R1, n in R0) for n in ((7,15),(7,17),(6,16),(8,16),(7,16))])
    assert not lost, ('cases devenues inatteignables', sorted(lost)[:10])
    for ev in EVC: assert ev not in ARTP and ev not in CONV, ('evenement recouvert', ev)
    print(CFG['name'], 'herbe', sum(1 for c in G if c in G and mid(c) in CFG['plain']), sum(1 for c in G if c in RES and mid(c) in CFG['plain']), 'cand', len(cand), dict(REJ), 'arbres', len(TREES), 'amas', len(CLUS), 'eclats', len(SHARDS), '; atteignable', len(R0), '->', len(R1))
    OUT[CFG['name']] = (dict(G), W, H)
    json.dump({'w': W, 'h': H, 'blocked': sorted([x, y] for (x, y) in G if blocked((x, y)))}, open('/tmp/%s_col.json' % CFG['name'].lower(), 'w'))
# ------------------------------------------------------------------ controle des sprites (planche + assertions)
def qa_sprite(name, rgba, big=True):
    w, h = rgba.size; px = rgba.load(); ok = True; msgs = []
    if big:
        for qy in range(0, h, 16):
            for qx in range(0, w, 16):
                n = sum(1 for j in range(16) for i in range(16) if px[qx + i, qy + j][3])
                if n < 40: ok = False; msgs.append('case (%d,%d) presque vide (%d)' % (qx // 16, qy // 16, n))
        bb = rgba.getbbox(); top = sum(1 for x in range(w) for y in range(bb[1], bb[1] + 4) if px[x, y][3]); bot = sum(1 for x in range(w) for y in range(bb[3] - 4, bb[3]) if px[x, y][3])
        if top == 0 or bot == 0: ok = False; msgs.append('haut ou bas vide')
        if bot > 0 and top > 0 and not (0.1 < top / float(bot) < 4): msgs.append('haut/bas desequilibres %d/%d' % (top, bot))
    iso = sum(1 for y in range(h) for x in range(w) if px[x, y][3] and sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3]) == 0)
    if iso: ok = False; msgs.append('%d pixel(s) isole(s)' % iso)
    assert ok, (name, msgs)
    return msgs
def p_to_rgba(im, pal):
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); o = out.load(); p = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y]: o[x, y] = pal[p[x, y]] + (255,)
    return out
SPR = [('arbre', TREE_RGBA, True), ('arbre_miroir', p_to_rgba(TREE_PF, MIXP), True), ('amas0', p_to_rgba(cluster(0), PAL_C), True), ('amas1', p_to_rgba(cluster(1), PAL_C), True)] + \
      [('eclat%d' % v, p_to_rgba(small(v), PAL_C), False) for v in range(3)]
sheet = Image.new('RGBA', (len(SPR) * 200, 260), (115, 205, 164, 255))
for i, (n, im, big) in enumerate(SPR):
    m = qa_sprite(n, im, big)
    if m: print('sprite', n, ':', '; '.join(m))
    sheet.alpha_composite(im.resize((im.width * 5, im.height * 5), 0), (i * 200 + 10, 10))
sheet.save('docs/topaze/reference/route22_sprites_qa.png')
# ------------------------------------------------------------------ ecriture
smt += b''.join(struct.pack('<8H', *e) for e in ENTS); satt += b''.join(struct.pack('<I', a) for a in ENTATT)
assert NMT + len(ENTS) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(ENTS), NTL + len(NEWT))
open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(satt)
rows = (NTL + len(NEWT) + 15) // 16
out = Image.new('P', (128, rows * 8), 0); out.putpalette(simg.getpalette()); out.paste(simg, (0, 0))
for n, t in enumerate(NEWT):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
out.save(NS + 'tiles.png')
writepal(NS + 'palettes/%02d.pal' % ART_PAL, PAL_C); writepal(NS + 'palettes/%02d.pal' % MIX_PAL, MIXP)
for nm, (GG, WW, HH) in OUT.items():
    g = [GG[(x, y)] for y in range(HH) for x in range(WW)]
    open('data/layouts/%s/map.bin' % nm, 'wb').write(struct.pack('<%dH' % len(g), *g))
def add(path, text):
    s = open(path).read()
    if 'GeneralOpalroad' not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
    '\nconst u32 gTilesetTiles_GeneralOpalroad[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralOpalroad[][16] =\n{\n%s};\n' % (NP, pal(NP)) +
    '\nconst u32 gTilesetTiles_ViridianPepite[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_ViridianPepite[][16] =\n{\n%s};\n' % (NS, pal(NS)))
add('src/data/tilesets/metatiles.h',
    '\nconst u16 gMetatiles_GeneralOpalroad[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralOpalroad[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (NP, NP) +
    '\nconst u16 gMetatiles_ViridianPepite[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_ViridianPepite[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (NS, NS))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralOpalroad =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralOpalroad,
    .palettes = gTilesetPalettes_GeneralOpalroad,
    .metatiles = gMetatiles_GeneralOpalroad,
    .metatileAttributes = gMetatileAttributes_GeneralOpalroad,
    .callback = InitTilesetAnim_General,
};

const struct Tileset gTileset_ViridianPepite =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ViridianPepite,
    .palettes = gTilesetPalettes_ViridianPepite,
    .metatiles = gMetatiles_ViridianPepite,
    .metatileAttributes = gMetatileAttributes_ViridianPepite,
    .callback = NULL,
};
''')
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_ROUTE22': l.update(primary_tileset='gTileset_GeneralOpalroad', secondary_tileset='gTileset_ViridianPepite')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('route 22 habillee : metatuiles', NMT + len(ENTS), 'tuiles', NTL + len(NEWT))
