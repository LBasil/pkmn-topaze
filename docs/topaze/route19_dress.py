# ROUTE 19 (ex-Parmanie sud) : route cotiere sous Amethiolite, couleurs amethyste (sable lilas, pelouses lilas). V2 : la mer du sud a ete envahie par une eruption volcanique : l'eau est remplacee par de l'obsidienne (impassable, veines de lave, 2 cones fumants) ; seuls un chenal sinueux, des bassins et la baie ouest restent navigables (acces a la Route 20 / iles Ecume). Derive de route20_dress.py. Idempotent : part de route21_src/r19_orig.bin.
# Lancer depuis la racine : python3 docs/topaze/route19_dress.py
import struct, json, random, sys, os, shutil, math, colorsys, collections
from PIL import Image, ImageDraw
SRC = 'docs/topaze/route21_src/'
FRP = 'data/tilesets/primary/general/'; FRS = 'data/tilesets/secondary/fuchsia_city/'
W_, H_ = 24, 60
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_amethyst(c):
    h, l, s = hls(c)
    if s < 0.08: return c
    if 28 <= h < 70 and s > 0.1: return rgb(284, min(1, l * 1.0 + 0.02), min(0.5, s * 0.6 + 0.05))
    if 70 <= h <= 175: return rgb(274, min(1, l + 0.03), min(0.7, s * 0.6 + 0.05)) if l > 0.42 else rgb(258, min(1, l * 1.18), min(0.8, s * 0.9))
    if 180 <= h <= 235: return rgb(h + 8, l, s)
    return c
ART_PAL = 9; ART_PAL2 = 10
PAL_V = [(0, 0, 0), (14, 6, 20), (36, 22, 46), (58, 40, 74), (88, 66, 110), (140, 120, 160), (214, 196, 230), (120, 16, 10), (214, 52, 16),
         (255, 128, 24), (255, 204, 64), (255, 246, 190), (70, 64, 72), (110, 104, 114), (160, 154, 164), (24, 16, 30)]
PAL_A = [(0, 0, 0), (30, 10, 52), (94, 44, 142), (142, 84, 202), (188, 132, 236), (228, 200, 252), (252, 242, 255), (46, 36, 112), (84, 72, 172),
         (132, 122, 222), (198, 192, 250), (40, 30, 66), (214, 64, 152), (176, 168, 192), (96, 88, 118), (255, 246, 200)]
ART_SRC = '''
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


def obsidian(var):
    """obsidienne tuilable (16x16) : facettes sombres, eclats ; var 4/5 = veine de lave horizontale, 6/7 = verticale"""
    im = newimg(16, 16); d = ImageDraw.Draw(im); r = random.Random(var * 77 + 5)
    d.rectangle((0, 0, 15, 15), fill=2)
    for _ in range(6):
        cx, cy = r.randrange(16), r.randrange(16); pts = [(cx + r.randint(-6, 6), cy + r.randint(-6, 6)) for _ in range(3)]; col = r.choice((3, 3, 4, 15, 15))
        for ox in (-16, 0, 16):
            for oy in (-16, 0, 16): d.polygon([(px + ox, py + oy) for px, py in pts], fill=col)
    for _ in range(3):
        x, y = r.randrange(16), r.randrange(16); d.point((x, y), fill=5)
        if r.random() < .4: d.point((x, y), fill=6)
    if var in (4, 5):
        pts = [(0, 8), (3, 7), (6, 9), (9, 7), (12, 9), (15, 8)] if var == 4 else [(0, 8), (3, 9), (6, 7), (9, 9), (12, 7), (15, 8)]
        for dy in (-1, 0, 1): d.line([(x, y + dy) for x, y in pts], fill=7 if dy else 8)
        d.line(pts, fill=9)
        for x, y in pts[1:-1:2]: d.point((x, y), fill=10)
    if var in (6, 7):
        pts = [(8, 0), (7, 3), (9, 6), (7, 9), (9, 12), (8, 15)] if var == 6 else [(8, 0), (9, 3), (7, 6), (9, 9), (7, 12), (8, 15)]
        for dx in (-1, 1): d.line([(x + dx, y) for x, y in pts], fill=7)
        d.line(pts, fill=8)
        for x, y in pts[1:-1:2]: d.point((x, y), fill=9)
    return im
def cone(w, h):
    """volcan fumant (w x h px) : cone d'obsidienne, cratere incandescent, coulees de lave, panache de cendres"""
    im = newimg(w, h); d = ImageDraw.Draw(im); fx = lambda f: int(f * (w - 1)); fy = lambda f: int(f * (h - 1))
    cx = w // 2
    for (px, py, rr, col) in ((.42, .16, .13, 12), (.52, .1, .12, 13), (.62, .07, .1, 14), (.36, .22, .09, 13), (.7, .03, .08, 14)):
        d.ellipse((fx(px) - int(rr * w), fy(py) - int(rr * h * .6), fx(px) + int(rr * w), fy(py) + int(rr * h * .6)), fill=col, outline=12)
    d.polygon([(fx(.0), fy(.97)), (fx(.3), fy(.34)), (fx(.7), fy(.34)), (fx(1.), fy(.97))], fill=3, outline=1)
    d.polygon([(fx(.04), fy(.93)), (fx(.33), fy(.37)), (cx, fy(.37)), (cx, fy(.95))], fill=4)
    d.polygon([(cx, fy(.37)), (fx(.68), fy(.37)), (fx(.96), fy(.93)), (cx, fy(.95))], fill=2)
    for k in range(4):
        x0 = fx(.34 + .1 * k); d.line([(x0, fy(.4)), (x0 - int(w * (.1 + .02 * k)), fy(.92))], fill=15)
    d.ellipse((fx(.28), fy(.28), fx(.72), fy(.44)), fill=7, outline=1); d.ellipse((fx(.33), fy(.3), fx(.67), fy(.41)), fill=8)
    d.ellipse((fx(.4), fy(.32), fx(.6), fy(.39)), fill=9); d.ellipse((fx(.45), fy(.33), fx(.55), fy(.37)), fill=10)
    for (a, b) in ((.5, .38), (.58, .66), (.46, .34)):
        pts = [(fx(a), fy(.4)), (fx(a) + (fx(b) - fx(a)) // 2 + 1, fy(.55)), (fx(b), fy(.9))]
        d.line(pts, fill=8, width=2); d.line(pts, fill=9)
    d.ellipse((fx(.2), fy(.9), fx(.45), fy(.99)), fill=8); d.ellipse((fx(.25), fy(.92), fx(.4), fy(.97)), fill=9)
    for (a, b) in ((.05, .96), (.88, .97), (.7, .99)): d.ellipse((fx(a), fy(b) - 2, fx(a) + 4, fy(b) + 1), fill=15, outline=1)
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
'''
def p_att(m, P, S): return (P[m] if m < 640 else S[m - 640])
WATER_ATT_MASK = ~0x60000000
def dress(half):
    cfg = dict(lay='Route19', LID='LAYOUT_ROUTE19', orig='r19_orig.bin', np='data/tilesets/primary/general_route19/', ns='data/tilesets/secondary/fuchsia_route19/', cn='Route19', tint=tint_amethyst, pal=PAL_A, seed=1919, npyl=7, ncry=2)
    NP, NS = cfg['np'], cfg['ns']
    for src, dst in ((FRP, NP), (FRS, NS)):
        shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
        for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
        for i in range(16):
            pp = readpal(src + 'palettes/%02d.pal' % i); writepal(dst + 'palettes/%02d.pal' % i, [pp[0]] + [cfg['tint'](c) for c in pp[1:16]])
    pmt = open(FRP + 'metatiles.bin', 'rb').read(); patt = struct.unpack('<%dI' % (os.path.getsize(FRP + 'metatile_attributes.bin') // 4), open(FRP + 'metatile_attributes.bin', 'rb').read())
    smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = list(struct.unpack('<%dI' % (len(smt) // 16), open(NS + 'metatile_attributes.bin', 'rb').read()))
    NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
    def ents(m): return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
    def att(m): return patt[m] if m < 640 else satt[m - 640]
    NEWT = []; NEWE = []; NEWA = []
    def add_tile(t):
        t = tuple(t)
        if t in NEWT: return NEWT.index(t)
        NEWT.append(t); return len(NEWT) - 1
    def slice4(im): return [add_tile(list(im.crop(((q % 2) * 8, (q // 2) * 8, (q % 2) * 8 + 8, (q // 2) * 8 + 8)).getdata())) for q in range(4)]
    def art_meta(tiles4, base_m):
        e = ents(base_m)[:4] + [('A', t) for t in tiles4]; a = att(base_m) & WATER_ATT_MASK
        NEWE.append(e); NEWA.append(a); return 640 + NMT + len(NEWE) - 1
    def art_meta2(bot4, top4, pal2=True):
        zero = add_tile([0] * 64)
        e = [('B', t) for t in bot4] + [('B', t) for t in (top4 if top4 else [zero] * 4)]
        if e in NEWE: return 640 + NMT + NEWE.index(e)
        NEWE.append(e); NEWA.append(0); return 640 + NMT + len(NEWE) - 1
    G = list(struct.unpack('<%dH' % (W_ * H_), open(SRC + cfg['orig'], 'rb').read())); G0 = list(G)
    def xy(i): return (i % W_, i // W_)
    def blocked(v): return bool(v & 0xc00)
    M = lambda c: G[c[1] * W_ + c[0]] & 0x3ff
    # evenements de la carte (cases a ne jamais toucher)
    mj = json.load(open('data/maps/%s/map.json' % cfg['lay']))
    EV = {(o['x'], o['y']) for o in mj['object_events']} | {(w['x'], w['y']) for w in mj['warp_events']} | {(b['x'], b['y']) for b in mj['bg_events']}
    def nbrs(c):
        for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if 0 <= n[0] < W_ and 0 <= n[1] < H_: yield n
    def reach(start, extra=frozenset()):
        seen = {start}; q = collections.deque([start])
        while q:
            c = q.popleft()
            for n in nbrs(c):
                if n not in seen and not blocked(G[n[1] * W_ + n[0]]) and n not in extra: seen.add(n); q.append(n)
        return seen
    start = (10, 0)
    assert not blocked(G[10])
    R0 = reach(start)
    rnd = random.Random(cfg['seed'])
    # ---- art
    exec(ART_SRC, globals())
    PALX = cfg['pal']
    PY = pylon(); SMS = [small(0), small(1), small(2)]
    OBS = {}
    ART = {}                                              # cellule -> (tuiles4, metatuile de base)
    def free(c, r=1):
        for a in range(-r, r + 1):
            for b in range(-r, r + 1):
                n = (c[0] + a, c[1] + b)
                if n in EV or n in ART or n in OBS: return False
        return True
    def plain_water(c): return 0 <= c[0] < W_ and 0 <= c[1] < H_ and M(c) == 299 and not blocked(G[c[1] * W_ + c[0]])
    placed = []

    # ---- eruption : la mer du sud devient obsidienne
    ROCKS = {272, 273, 280, 281, 459, 460, 467, 468, 473, 464, 472, 480, 482, 466}
    def is_sea(c): return (M(c) == 299 and not blocked(G[c[1] * W_ + c[0]])) or M(c) in ROCKS
    KEEP = set()
    def stamp(cx, cy, r):
        for yy in range(int(cy - r - 1), int(cy + r + 2)):
            for xx in range(int(cx - r - 1), int(cx + r + 2)):
                if 0 <= xx < W_ and 0 <= yy < H_ and (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r: KEEP.add((xx, yy))
    def channel(pts, r0):
        for (a, b) in zip(pts, pts[1:]):
            n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) * 2) + 1
            for k in range(n + 1):
                t = k / n; stamp(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, r0 + .5 * math.sin(k * 1.7 + a[0]))
    for yy in range(13, 20):
        for xx in range(7, 18): KEEP.add((xx, yy))                       # bassin devant la plage
    for yy in range(42, 59):
        for xx in range(0, 3): KEEP.add((xx, yy))                         # baie ouest (vers la Route 20)
    channel([(12, 16), (12, 19), (16, 22), (13, 25), (8, 27), (12, 30), (18, 33), (14, 37), (9, 41), (10, 45), (6, 48), (2, 50)], 1.5)
    CL = [(12, 16), (12, 19), (16, 22), (13, 25), (8, 27), (12, 30), (18, 33), (14, 37), (9, 41), (10, 45), (6, 48), (2, 50)]
    for (px, py, pr) in ((12, 48, 3.0), (17, 26, 2.0), (5, 53, 2.2)):
        stamp(px, py, pr); tg = min(CL, key=lambda k: abs(k[0] - px) + abs(k[1] - py)); channel([(px, py), tg], 1.0)
    for c in sorted(EV):                                                       # evenements en mer : toujours accessibles
        if c[1] >= 14 and is_sea(c) and c not in KEEP:
            tgt = min(KEEP, key=lambda k: abs(k[0] - c[0]) + abs(k[1] - c[1])); channel([c, tgt], 1.0)
    for c in sorted(EV):
        if c[1] >= 14 and is_sea(c): stamp(c[0], c[1], 1.2)
    cand = {(x, y) for y in range(14, H_) for x in range(W_) if is_sea((x, y)) and (x, y) not in KEEP and (x, y) not in EV}
    # cones : 4x4 et 3x3 sur de l'obsidienne, loin du chenal
    CONES = []
    def near_keep(c): return any((c[0] + a, c[1] + b) in KEEP for a in (-1, 0, 1) for b in (-1, 0, 1))
    for (cw, ch, prefer) in ((5, 5, (14, 33)), (4, 4, (5, 22)), (4, 4, (16, 52))):
        best = None
        for y0 in range(14, H_ - ch):
            for x0 in range(W_ - cw):
                cells = [(x0 + i, y0 + j) for j in range(ch) for i in range(cw)]
                if all(c in cand and not near_keep(c) for c in cells) and all(not any(abs(c[0] - o[0]) < 7 and abs(c[1] - o[1]) < 7 for c in cells[:1]) for o in [k[:2] for k in CONES]):
                    dd = abs(x0 - prefer[0]) + abs(y0 - prefer[1])
                    if best is None or dd < best[0]: best = (dd, x0, y0)
        assert best, 'pas de place pour le cone'
        CONES.append((best[1], best[2], cw, ch))
    rv = random.Random(1999)
    VAR = {}
    for c in sorted(cand):
        v = rv.random(); VAR[c] = rv.randrange(4) if v < .8 else (4 + rv.randrange(4))
    TILES_OBS = [obsidian(v) for v in range(8)]
    for (x0, y0, cw, ch) in CONES:
        cim = cone(cw * 16, ch * 16)
        for j in range(ch):
            for i in range(cw):
                c = (x0 + i, y0 + j); VAR[c] = rv.randrange(4)
                OBS[c] = (slice4(TILES_OBS[VAR[c]]), slice4(cim.crop((i * 16, j * 16, i * 16 + 16, j * 16 + 16))))
    for c in sorted(cand):
        if c not in OBS: OBS[c] = (slice4(TILES_OBS[VAR[c]]), None)
    for c, (b4, t4) in OBS.items():
        mid = art_meta2(b4, t4); G[c[1] * W_ + c[0]] = (G[c[1] * W_ + c[0]] & 0xf000) | 0x400 | mid
    print('obsidienne', len(OBS), 'cases ; eau conservee', len(KEEP))
    # recifs d'amethyste dans le chenal (Sud : lignes haute tension ; Nord : quelques pylones du meme reseau)
    cands = [(x, y) for y in range(3, H_ - 3) for x in range(3, W_ - 3) if plain_water((x, y)) and plain_water((x, y + 1))]
    rnd.shuffle(cands); npy = 0
    def dist_block(c):
        best = 99
        for a in range(-4, 5):
            for b in range(-4, 5):
                n = (c[0] + a, c[1] + b)
                if not (0 <= n[0] < W_ and 0 <= n[1] < H_) or blocked(G[n[1] * W_ + n[0]]) or M(n) != 299: best = min(best, max(abs(a), abs(b)))
        return best
    cands = [c for c in cands if 1 <= dist_block(c) <= 4 and free(c, 2)]
    for c in cands:
        if npy >= cfg['npyl']: break
        if any(abs(c[0] - p[0]) < 4 and abs(c[1] - p[1]) < 5 for p in placed): continue
        cells = [c]
        if not (reach(start, set(ART) | set(cells)) >= (R0 - set(ART) - set(cells))): continue
        ART[cells[0]] = (slice4(SMS[rnd.randrange(3)]), 299); placed.append(c); npy += 1
    # cristaux sur les bancs de sable (cases de sable entourees de sable)
    sand = [(x, y) for y in range(2, H_ - 2) for x in range(1, W_ - 1) if M((x, y)) in (277, 269, 285, 284) and not blocked(G[y * W_ + x]) and free((x, y), 1)
            and all(M(n) in (277, 269, 285, 284) for n in nbrs((x, y)))]
    rnd.shuffle(sand); nc = 0
    for c in sand:
        if nc >= cfg['ncry']: break
        if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < 3 for q in ART): continue
        if not (reach(start, set(ART) | {c}) >= (R0 - set(ART) - {c})): continue
        ART[c] = (slice4(SMS[rnd.randrange(3)]), M(c)); nc += 1
    print(half, 'pylones', npy, 'cristaux', nc)
    for c, (t4, base) in ART.items():
        mid = art_meta(t4, base); G[c[1] * W_ + c[0]] = (G[c[1] * W_ + c[0]] & 0xf000) | 0xc00 & 0x400 | mid
    R1 = reach(start); lost = {c for c in R0 if c not in R1 and c not in ART and c not in OBS}
    assert not lost, ('cases perdues', sorted(lost)[:10])
    assert all(c in R1 for c in EV if c in R0), 'evenement inaccessible'
    # ---- ecriture
    assert NMT + len(NEWE) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(NEWE), NTL + len(NEWT))
    NEWE = [[((640 + NTL + q[1]) | ((ART_PAL2 if q[0] == 'B' else ART_PAL) << 12)) if isinstance(q, tuple) else q for q in e] for e in NEWE]
    smt += b''.join(struct.pack('<8H', *e) for e in NEWE); satt += NEWA
    open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in satt))
    rows = (NTL + len(NEWT) + 15) // 16
    out = Image.new('P', (128, rows * 8), 0); out.putpalette(simg.getpalette()); out.paste(simg, (0, 0))
    for n, t in enumerate(NEWT):
        ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
    out.save(NS + 'tiles.png'); writepal(NS + 'palettes/%02d.pal' % ART_PAL, PALX); writepal(NS + 'palettes/%02d.pal' % ART_PAL2, PAL_V)
    open('data/layouts/%s/map.bin' % cfg['lay'], 'wb').write(struct.pack('<%dH' % len(G), *G))
    return cfg, NP, NS
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
Lj = json.load(open('data/layouts/layouts.json'))
for half in ('R19',):
    cfg, NP, NS = dress(half); cn = cfg['cn']
    add('src/data/tilesets/graphics.h', 'GeneralRoute19',
        '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
        '\nconst u32 gTilesetTiles_Fuchsia%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Fuchsia%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
    add('src/data/tilesets/metatiles.h', 'GeneralRoute19',
        '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
        '\nconst u16 gMetatiles_Fuchsia%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Fuchsia%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
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
    add('src/data/tilesets/headers.h', 'GeneralRoute19',
        tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Fuchsia', cn, 'TRUE', 'Fuchsia', cn, 'Fuchsia', cn, 'Fuchsia', cn, 'Fuchsia', cn, 'NULL'))
    for l in Lj['layouts']:
        if l.get('id') == cfg['LID']: l.update(primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Fuchsia%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('route 19 habillee')
