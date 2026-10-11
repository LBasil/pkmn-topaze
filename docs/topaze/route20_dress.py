# ROUTE 20 (ex-Seafoam) : route maritime entre Route 19 et Chrondrolia, memes couleurs que Chrondrolia / Route 21 Sud (derive de route21_dress.py). Idempotent : part de docs/topaze/route21_src/*_orig.bin.
# Chaque moitie a ses propres tilesets (copies de General + CinnabarIsland, eau ANIMEE conservee) :
#   NORD  : couleurs de Grenalux (grenat / bordeaux, eau violet nuit), cristaux de grenat sur les bancs de sable
#   SUD   : couleurs de Chrondrolia (bancs de sable -> beton gris-beige, toits dores, eau bleue), pylones haute tension plantes dans la mer sur dalle de beton, eclats de topaze
# Les deux moities ne sont plus reliees par une connexion de carte (palettes differentes) : warps a pas simple sur la rangee de mer (route21_events.py).
# Lancer depuis la racine : python3 docs/topaze/route21_dress.py && python3 docs/topaze/route21_events.py && python3 docs/topaze/chrondrolia_events.py
import struct, json, random, sys, os, shutil, math, colorsys, collections
from PIL import Image, ImageDraw
SRC = 'docs/topaze/route21_src/'
FRP = 'data/tilesets/primary/general/'; FRS = 'data/tilesets/secondary/cinnabar_island/'
W_, H_ = 120, 20
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_grenat(c):          # meme teinte que Grenalux (grenat_palette.py)
    h, l, s = hls(c)
    if s < 0.08: return c
    if 60 <= h <= 180: return rgb(352 + (h - 120) * 0.12, l * 0.8, min(1, s * 0.9))
    if 25 <= h < 60: return rgb(14 + (h - 40) * 0.2, l, s * 0.75)
    if 180 < h <= 260: return rgb(262 + (h - 215) * 0.2, l * 0.5, s * 0.4)
    return rgb(350, l * 0.78, min(1, s * 1.05))
def tint_marine(c):          # meme teinte que Chrondrolia : sable -> beton gris-beige, rose -> or ; eau et reste inchanges
    h, l, s = hls(c)
    if 25 <= h < 65 and s > 0.15: return rgb(44, l * 0.97, s * 0.45)
    if 270 <= h <= 345 and s > 0.15: return rgb(42 + (h - 300) * 0.05, min(1, l * 1.02 + 0.02), min(0.95, s * 1.1))
    return c
ART_PAL = 9
PAL_N = [(0, 0, 0), (40, 6, 14), (120, 16, 40), (176, 34, 64), (228, 80, 100), (255, 170, 176), (255, 236, 236), (70, 20, 110), (130, 60, 170),
         (190, 120, 220), (230, 200, 250), (24, 10, 20), (92, 52, 60), (160, 130, 140), (90, 70, 84), (255, 230, 200)]
PAL_S = [(0, 0, 0), (52, 30, 0), (150, 88, 0), (226, 158, 14), (255, 208, 56), (255, 240, 150), (255, 252, 226), (20, 96, 190), (70, 186, 255),
         (150, 230, 255), (226, 250, 255), (36, 36, 44), (196, 32, 24), (150, 150, 158), (84, 86, 98), (255, 248, 190)]
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
    cfg = dict(lay='Route20', LID='LAYOUT_ROUTE20', orig='r20_orig.bin', np='data/tilesets/primary/general_route20/', ns='data/tilesets/secondary/cinnabar_route20/', cn='Route20', tint=tint_marine, pal=PAL_S, seed=2020, npyl=14, ncry=8)
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
    start = (0, 0)
    assert not blocked(G[0])
    R0 = reach(start)
    rnd = random.Random(cfg['seed'])
    # ---- art
    exec(ART_SRC, globals())
    PALX = cfg['pal']
    PY = pylon(); SMS = [small(0), small(1), small(2)]
    ART = {}                                              # cellule -> (tuiles4, metatuile de base)
    def free(c, r=1):
        for a in range(-r, r + 1):
            for b in range(-r, r + 1):
                n = (c[0] + a, c[1] + b)
                if n in EV or n in ART: return False
        return True
    def plain_water(c): return 0 <= c[0] < W_ and 0 <= c[1] < H_ and M(c) == 299 and not blocked(G[c[1] * W_ + c[0]])
    placed = []
    # pylones (Sud : lignes haute tension ; Nord : quelques pylones du meme reseau)
    cands = [(x, y) for y in range(3, H_ - 3) for x in range(3, W_ - 3) if plain_water((x, y)) and plain_water((x, y + 1))]
    rnd.shuffle(cands); npy = 0
    def dist_block(c):
        best = 99
        for a in range(-4, 5):
            for b in range(-4, 5):
                n = (c[0] + a, c[1] + b)
                if not (0 <= n[0] < W_ and 0 <= n[1] < H_) or blocked(G[n[1] * W_ + n[0]]) or M(n) != 299: best = min(best, max(abs(a), abs(b)))
        return best
    cands = [c for c in cands if 2 <= dist_block(c) <= 4 and free(c, 2) and free((c[0], c[1] + 1), 2)]
    for c in cands:
        if npy >= cfg['npyl']: break
        if any(abs(c[0] - p[0]) < 5 and abs(c[1] - p[1]) < 7 for p in placed): continue
        cells = [c, (c[0], c[1] + 1)]
        if not (reach(start, set(ART) | set(cells)) >= (R0 - set(ART) - set(cells))): continue
        ART[cells[0]] = (slice4(PY.crop((0, 0, 16, 16))), 299); ART[cells[1]] = (slice4(PY.crop((0, 16, 16, 32))), 299); placed.append(c); npy += 1
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
    R1 = reach(start); lost = {c for c in R0 if c not in R1 and c not in ART}
    assert not lost, ('cases perdues', sorted(lost)[:10])
    assert all(c in R1 for c in EV if c in R0), 'evenement inaccessible'
    # ---- ecriture
    assert NMT + len(NEWE) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(NEWE), NTL + len(NEWT))
    NEWE = [[((640 + 0 * 0 + NTL + q[1]) | (ART_PAL << 12)) if isinstance(q, tuple) else q for q in e] for e in NEWE]
    smt += b''.join(struct.pack('<8H', *e) for e in NEWE); satt += NEWA
    open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in satt))
    rows = (NTL + len(NEWT) + 15) // 16
    out = Image.new('P', (128, rows * 8), 0); out.putpalette(simg.getpalette()); out.paste(simg, (0, 0))
    for n, t in enumerate(NEWT):
        ti = Image.new('P', (8, 8)); ti.putdata(list(t)); out.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
    out.save(NS + 'tiles.png'); writepal(NS + 'palettes/%02d.pal' % ART_PAL, PALX)
    open('data/layouts/%s/map.bin' % cfg['lay'], 'wb').write(struct.pack('<%dH' % len(G), *G))
    return cfg, NP, NS
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
Lj = json.load(open('data/layouts/layouts.json'))
for half in ('R20',):
    cfg, NP, NS = dress(half); cn = cfg['cn']
    add('src/data/tilesets/graphics.h', 'GeneralRoute21%s' % half,
        '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
        '\nconst u32 gTilesetTiles_Cinnabar%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Cinnabar%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
    add('src/data/tilesets/metatiles.h', 'GeneralRoute21%s' % half,
        '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
        '\nconst u16 gMetatiles_Cinnabar%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Cinnabar%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
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
    add('src/data/tilesets/headers.h', 'GeneralRoute21%s' % half,
        tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Cinnabar', cn, 'TRUE', 'Cinnabar', cn, 'Cinnabar', cn, 'Cinnabar', cn, 'Cinnabar', cn, 'NULL'))
    for l in Lj['layouts']:
        if l.get('id') == cfg['LID']: l.update(primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Cinnabar%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('route 20 habillee')
