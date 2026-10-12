# ROUTES 16 + 17 « du quartz a l'ametyste » : Route 16 (depart : Bourg Quartz, neige, a l'EST) puis Route 17 (voie cyclable, 160 cases, vers le SUD)
# jusqu'a la Route 18 (arrivee : Amethiolite, lilas). Une seule famille de tilesets (`general_route16` / `celadon_route16`) :
#   - etage 0 = neige de Bourg Quartz (palettes primaires 0..6 de `general_celadopole`),
#   - etage 1 = lilas d'amethyste (palettes de `general_route18` pour les palettes 0, 3, 5 d'origine, rangees dans les emplacements 7, 8, 9),
#   - 10 = palette d'art amethyste, 12 = palette d'art quartz, 11 = voie cyclable (melange).
# L'etage de chaque case suit la distance parcourue depuis Bourg Quartz (route 16 d'est en ouest puis route 17 du nord au sud) + un champ lisse :
# des plaques de lilas apparaissent dans la neige puis prennent le dessus (fonte progressive), la Route 17 finit entierement lilas comme la Route 18.
# Decor : bosquets d'arbres (arbres FR 2x2) et cristaux (quartz cote neige, amethyste cote lilas) dans les prairies, sans jamais couper un acces (BFS).
# Idempotent : part de route21_src/r16_orig.bin / r17_orig.bin. Lancer depuis la racine : python3 docs/topaze/route16_dress.py
import struct, json, random, os, shutil, math, colorsys, collections, sys
from PIL import Image, ImageDraw
SRC = 'docs/topaze/route21_src/'
GEN = 'data/tilesets/primary/general/'; SEC = 'data/tilesets/secondary/celadon_city/'
NP = 'data/tilesets/primary/general_route16/'; NS = 'data/tilesets/secondary/celadon_route16/'
DIMS = {'Route16': (48, 20), 'Route17': (24, 160)}
for n, f in (('Route16', 'r16_orig.bin'), ('Route17', 'r17_orig.bin')):
    if not os.path.exists(SRC + f): shutil.copy('data/layouts/%s/map.bin' % n, SRC + f)

def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t + .5) for i in range(3))
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s

# ------------------------------------------------------------------ palettes
PAL_A = [(0, 0, 0), (30, 10, 52), (94, 44, 142), (142, 84, 202), (188, 132, 236), (228, 200, 252), (252, 242, 255), (46, 36, 112), (84, 72, 172),
         (132, 122, 222), (198, 192, 250), (40, 30, 66), (214, 64, 152), (176, 168, 192), (96, 88, 118), (255, 246, 200)]
def quartz(c):
    if c == (0, 0, 0): return c
    h, l, s = hls(c); return rgb(196, min(0.97, 0.18 + l * 0.85), min(0.75, 0.25 + s * 0.4))
PAL_Q = [quartz(c) for c in PAL_A]
ART_AME, ART_QTZ, SHIFT = 10, 12, {0: 7, 3: 8, 5: 9}        # emplacements : art amethyste, art quartz ; palette d'origine -> emplacement lilas
for src, dst in ((GEN, NP), (SEC, NS)):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    shutil.copytree(src + 'anim', dst + 'anim') if os.path.isdir(src + 'anim') else None
    for i in range(16): shutil.copy(src + 'palettes/%02d.pal' % i, dst + 'palettes/%02d.pal' % i)
for i in range(7): shutil.copy('data/tilesets/primary/general_celadopole/palettes/%02d.pal' % i, NP + 'palettes/%02d.pal' % i)
for i in (4, 6): shutil.copy('data/tilesets/primary/general_route18/palettes/%02d.pal' % i, NP + 'palettes/%02d.pal' % i)      # palettes 4 et 6 = eau (mer, rivages) : bleu profond de la Route 18 partout
for o, sl in SHIFT.items(): writepal(NS + 'palettes/%02d.pal' % sl, readpal('data/tilesets/primary/general_route18/palettes/%02d.pal' % o))
pc, pa = readpal('data/tilesets/secondary/celadon_celadopole/palettes/11.pal'), readpal('data/tilesets/secondary/celadon_route18/palettes/11.pal')
writepal(NS + 'palettes/11.pal', [pc[0]] + [lerp(pc[k], pa[k], .5) for k in range(1, 16)])
writepal(NS + 'palettes/%02d.pal' % ART_AME, PAL_A); writepal(NS + 'palettes/%02d.pal' % ART_QTZ, PAL_Q)

# ------------------------------------------------------------------ metatuiles
pmt = open(GEN + 'metatiles.bin', 'rb').read(); patt = struct.unpack('<%dI' % (os.path.getsize(GEN + 'metatile_attributes.bin') // 4), open(GEN + 'metatile_attributes.bin', 'rb').read())
smt = bytearray(open(NS + 'metatiles.bin', 'rb').read()); satt = list(struct.unpack('<%dI' % (len(smt) // 16), open(NS + 'metatile_attributes.bin', 'rb').read()))
NMT = len(smt) // 16; simg = Image.open(NS + 'tiles.png'); NTL = (simg.width // 8) * (simg.height // 8)
def ents(m): return list(struct.unpack('<8H', pmt[m * 16:m * 16 + 16] if m < 640 else bytes(smt[(m - 640) * 16:(m - 640) * 16 + 16])))
def att(m): return patt[m] if m < 640 else satt[m - 640]
NEWE, NEWA, VAR, NEWT = [], [], {}, []
def new_meta(e, a):
    NEWE.append(e); NEWA.append(a); return 640 + NMT + len(NEWE) - 1
def variant(m, st):
    """metatuile m a l'etage st (0 = telle quelle, 1 = palettes 0/3/5 -> lilas)."""
    if st == 0: return m
    if (m, 1) in VAR: return VAR[(m, 1)]
    e = ents(m); out = [(q & 0xfff) | (SHIFT.get(q >> 12, q >> 12) << 12) for q in e]
    VAR[(m, 1)] = m if out == e else new_meta(out, att(m)); return VAR[(m, 1)]
def add_tile(t):
    t = tuple(t)
    if t in NEWT: return NEWT.index(t)
    NEWT.append(t); return len(NEWT) - 1

# ------------------------------------------------------------------ art : petits cristaux (prismes) 16x16
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
def small(var):
    im = newimg(16, 16); d = ImageDraw.Draw(im); d.ellipse((1, 12, 15, 16), fill=11)
    if var == 0: prism(d, 4, 14, 5, 9); prism(d, 9, 15, 7, 14); prism(d, 13, 14, 4, 7)
    elif var == 1: prism(d, 6, 15, 6, 11); prism(d, 12, 14, 5, 8); d.rectangle((1, 13, 3, 14), fill=13); d.point((2, 12), fill=14)
    else: prism(d, 8, 15, 8, 14); d.rectangle((2, 13, 4, 14), fill=13); d.rectangle((12, 12, 14, 14), fill=13); d.point((13, 11), fill=14)
    return im
def slice4(im): return [add_tile(list(im.crop(((q % 2) * 8, (q // 2) * 8, (q % 2) * 8 + 8, (q // 2) * 8 + 8)).getdata())) for q in range(4)]
SMT = [slice4(small(v)) for v in range(3)]
ARTM = {}
def art_meta(var, st, base):
    """case = fond d'herbe (variante d'etage) + cristal (calque haut) ; palette d'art selon l'etage."""
    k = (var, st, base)
    if k not in ARTM:
        sl = ART_AME if st else ART_QTZ; bot = ents(base)[:4]
        if st: bot = [(q & 0xfff) | (SHIFT.get(q >> 12, q >> 12) << 12) for q in bot]
        ARTM[k] = new_meta(bot + [('T', t, sl) for t in SMT[var]], att(base) & ~0x60000000)
    return ARTM[k]

# ------------------------------------------------------------------ etage (fonte neige -> lilas)
def noise(x, y): return 0.5 * math.sin(x * 0.35 + y * 0.11) + 0.3 * math.sin(y * 0.19 - x * 0.27 + 1.3) + 0.2 * math.sin(x * 0.13 + y * 0.43 + 2.1)
def stage(L, x, y):
    W, H = DIMS[L]
    s = (47 - x) / 47 * 0.44 if L == 'Route16' else 0.44 + 0.56 * y / (H - 1)
    j = ((x * 73856093) ^ (y * 19349663)) % 1000 / 1000.0 - 0.5
    return 1 if s + 0.16 * noise(x, y) > 0.60 else 0

GRASS = (8, 9, 16, 17, 830, 831, 838, 839, 835, 836, 837)
def dress(L):
    W, H = DIMS[L]
    G = list(struct.unpack('<%dH' % (W * H), open(SRC + ('r16_orig.bin' if L == 'Route16' else 'r17_orig.bin'), 'rb').read()))
    mj = json.load(open('data/maps/%s/map.json' % L))
    EV = {(o['x'], o['y']) for o in mj['object_events']} | {(w['x'], w['y']) for w in mj['warp_events']} | {(b['x'], b['y']) for b in mj['bg_events']}
    ST = {(x, y): stage(L, x, y) for y in range(H) for x in range(W)}
    blocked = lambda i: bool(G[i] & 0xc00)
    def nb(c):
        for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if 0 <= n[0] < W and 0 <= n[1] < H: yield n
    def reach(start, extra=frozenset()):
        seen = {start}; q = collections.deque([start])
        while q:
            c = q.popleft()
            for n in nb(c):
                if n not in seen and not blocked(n[1] * W + n[0]) and n not in extra: seen.add(n); q.append(n)
        return seen
    start = (47, 13) if L == 'Route16' else (12, 0)
    assert not blocked(start[1] * W + start[0]), start
    R0 = reach(start)
    def plain(c): return 0 <= c[0] < W and 0 <= c[1] < H and (G[c[1] * W + c[0]] & 0x3ff) in GRASS and not blocked(c[1] * W + c[0])
    def zone_ok(c, r):
        return all(plain((c[0] + a, c[1] + b)) and (c[0] + a, c[1] + b) not in EV for a in range(-r, r + 1) for b in range(-r, r + 1))
    rnd = random.Random(1616 if L == 'Route16' else 1717)
    BASE = {}                                              # cellule -> metatuile de base (sans etage) a poser
    ART = {}                                               # cellule -> (variante de cristal, base d'herbe)
    TREES = []
    # ---- bosquets : seeds espaces, 1..3 arbres 2x2 accoles, marge d'herbe tout autour
    cells = [(x, y) for y in range(2, H - 3) for x in range(2, W - 3)]
    rnd.shuffle(cells); seeds = []
    SP = 7 if L == 'Route17' else 6
    for c in cells:
        if any(max(abs(c[0] - s[0]), abs(c[1] - s[1])) < SP for s in seeds): continue
        # un arbre 2x2 : cases (x,y),(x+1,y),(x,y+1),(x+1,y+1) + 1 de marge
        def tree_ok(o):
            if any(max(abs(o[0] - t[0]), abs(o[1] - t[1])) < 2 for t in TREES if t != o) and False: return False
            for a in range(-1, 3):
                for b in range(-1, 3):
                    n = (o[0] + a, o[1] + b)
                    if n in EV or n in BASE: return False
                    if 0 <= a < 2 and 0 <= b < 2:
                        if not plain(n): return False
                    elif not (0 <= n[0] < W and 0 <= n[1] < H) or blocked(n[1] * W + n[0]): return False
            return True
        if not tree_ok(c): continue
        group = [c]
        for off in rnd.sample([(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, 2), (2, -1), (-2, 1)], 8):
            if len(group) >= rnd.choice((1, 2, 2, 3)): break
            o = (c[0] + off[0], c[1] + off[1])
            if o in group: continue
            for g in group + [o]:
                pass
            if tree_ok(o) and all(not ((o[0] + a, o[1] + b) in BASE) for a in range(2) for b in range(2)):
                # eviter le chevauchement avec les arbres du groupe
                if all(abs(o[0] - g[0]) >= 2 or abs(o[1] - g[1]) >= 2 for g in group): group.append(o)
        placed = []
        for o in group:
            cs = [(o[0] + a, o[1] + b) for b in range(2) for a in range(2)]
            if any(n in BASE for n in cs): continue
            for (n, m) in zip(cs, (20, 21, 28, 29)): BASE[n] = m
            if reach(start, set(BASE)) >= (R0 - set(BASE)): placed.append(o); TREES.append(o)
            else:
                for n in cs: BASE.pop(n, None)
        if placed: seeds.append(c)
    # ---- cristaux : cases d'herbe isolees, loin des arbres (un cristal bloque sa case)
    ncry = 0
    free = [(x, y) for y in range(2, H - 2) for x in range(2, W - 2) if plain((x, y)) and (x, y) not in BASE and (x, y) not in EV
            and all(n not in BASE and not blocked(n[1] * W + n[0]) for n in nb((x, y)))]
    rnd.shuffle(free); lim = 18 if L == 'Route16' else 46
    for c in free:
        if ncry >= lim: break
        if any(max(abs(c[0] - q[0]), abs(c[1] - q[1])) < (4 if L == 'Route17' else 3) for q in ART): continue
        if any(max(abs(c[0] - t[0]), abs(c[1] - t[1])) < 3 for t in TREES): continue
        if not (reach(start, set(BASE) | set(ART) | {c}) >= (R0 - set(BASE) - set(ART) - {c})): continue
        ART[c] = (rnd.randrange(3), G[c[1] * W + c[0]] & 0x3ff); ncry += 1
    # ---- ecriture de la carte
    out = list(G)
    for i in range(W * H):
        c = (i % W, i // W); fl = G[i] & 0xfc00
        if c in BASE:
            tr = [t for t in TREES if t[0] <= c[0] <= t[0] + 1 and t[1] <= c[1] <= t[1] + 1][0]
            st = ST[tr]; out[i] = 0x400 | variant(BASE[c], st)                    # tout l'arbre au meme etage
        elif c in ART:
            v, base = ART[c]; st = ST[c]; out[i] = (G[i] & 0xf000) | 0x400 | art_meta(v, st, base)
        else:
            m0 = G[i] & 0x3ff; wat = (att(m0) & 0x1ff) in (0x10, 0x11, 0x12, 0x13, 0x15, 0x1b)
            out[i] = fl | variant(m0, 1 if wat else ST[c])
    # verifications
    G2 = out
    blocked2 = lambda c: bool(G2[c[1] * W + c[0]] & 0xc00)
    seen = {start}; q = collections.deque([start])
    while q:
        c = q.popleft()
        for n in nb(c):
            if n not in seen and not blocked2(n): seen.add(n); q.append(n)
    lost = {c for c in R0 if c not in seen and c not in BASE and c not in ART}
    assert not lost, ('cases perdues', sorted(lost)[:10])
    assert all(c in seen for c in EV if c in R0), 'evenement inaccessible'
    nb1 = sum(ST.values()); print(L, 'arbres', len(TREES), 'cristaux', ncry, 'cases lilas %d/%d' % (nb1, W * H))
    return out

res = {L: dress(L) for L in DIMS}
# ---- ecriture des tilesets
assert NMT + len(NEWE) <= 384 and NTL + len(NEWT) <= 384, (NMT + len(NEWE), NTL + len(NEWT))
fin = [[((640 + NTL + q[1]) | (q[2] << 12)) if isinstance(q, tuple) else q for q in e] for e in NEWE]
smt += b''.join(struct.pack('<8H', *e) for e in fin); satt += NEWA
open(NS + 'metatiles.bin', 'wb').write(smt); open(NS + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in satt))
rows = (NTL + len(NEWT) + 15) // 16
tout = Image.new('P', (128, rows * 8), 0); tout.putpalette(simg.getpalette()); tout.paste(simg, (0, 0))
for n, t in enumerate(NEWT):
    ti = Image.new('P', (8, 8)); ti.putdata(list(t)); tout.paste(ti, (((NTL + n) % 16) * 8, ((NTL + n) // 16) * 8))
tout.save(NS + 'tiles.png')
for L, G in res.items(): open('data/layouts/%s/map.bin' % L, 'wb').write(struct.pack('<%dH' % len(G), *G))
print('metatuiles %d/384, tuiles %d/384' % (NMT + len(NEWE), NTL + len(NEWT)))

# ---- enregistrement des tilesets
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
cn = 'Route16'
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h', 'GeneralRoute16',
    '\nconst u32 gTilesetTiles_General%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_General%s[][16] =\n{\n%s};\n' % (cn, NP, cn, pal(NP)) +
    '\nconst u32 gTilesetTiles_Celadon%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Celadon%s[][16] =\n{\n%s};\n' % (cn, NS, cn, pal(NS)))
add('src/data/tilesets/metatiles.h', 'GeneralRoute16',
    '\nconst u16 gMetatiles_General%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_General%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NP, cn, NP) +
    '\nconst u16 gMetatiles_Celadon%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Celadon%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (cn, NS, cn, NS))
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
add('src/data/tilesets/headers.h', 'GeneralRoute16',
    tm % ('General', cn, 'FALSE', 'General', cn, 'General', cn, 'General', cn, 'General', cn, 'InitTilesetAnim_General') + tm % ('Celadon', cn, 'TRUE', 'Celadon', cn, 'Celadon', cn, 'Celadon', cn, 'Celadon', cn, 'NULL'))
Lj = json.load(open('data/layouts/layouts.json'))
for l in Lj['layouts']:
    if l.get('id') in ('LAYOUT_ROUTE16', 'LAYOUT_ROUTE17'): l.update(primary_tileset='gTileset_General%s' % cn, secondary_tileset='gTileset_Celadon%s' % cn)
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('routes 16 et 17 habillees')
