# Grenalux v6 : la ville vivable, aux couleurs du GRENAT (44x36). Evolution de grenalux_big.py (v5, conservee dans
# docs/topaze/reference/ et branche grenalux-v5-reference). Nouveautes : plan d'occupation avec verifications (plus de
# chevauchements), variantes de palette pour les toits (ardoise-violet, ocre), lampadaires de cristal, carriere + mine,
# bassin avec promenade, bosquets, chemins de portes calcules (BFS), controle d'accessibilite.
# Ordre : import_emerald_tiles.py -> grenat_palette.py -> (layouts.json remis a fa8f0d0) -> grenalux_town.py -> grenalux_events.py
import struct, json, random, sys, colorsys, collections
sys.path.insert(0, 'docs/topaze')
_L = json.load(open('data/layouts/layouts.json'))
for _l in _L['layouts']:
    if _l.get('id') == 'LAYOUT_PALLET_TOWN':
        _l['primary_tileset'] = 'gTileset_GeneralEmerald'; _l['secondary_tileset'] = 'gTileset_PetalburgEmerald'
json.dump(_L, open('data/layouts/layouts.json', 'w'), indent=2)
open('data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<480H', *([0x3001] * 480)))
import grenalux_crystals as C
PD = 'data/tilesets/primary/general_emerald/'; SD = 'data/tilesets/secondary/petalburg_emerald/'
EMD = '../pokeemerald/data/layouts/'
def src(name, w, h): return struct.unpack('<%dH' % (w * h), open(EMD + '%s/map.bin' % name, 'rb').read())
LR = src('LittlerootTown', 20, 20); PB = src('PetalburgCity', 30, 30)
def remap(v):
    m = v & 0x3ff
    return (v & ~0x3ff) | (m + 128 if m >= 512 else m)
W, H = 44, 36
G = {}; OCC = {}
def walk(m): return 0x3000 | m
def water(m): return 0x1000 | m
GRASS, FLOWER = walk(1), walk(4)
TREE_RAW = [[0x5d4, 0x5d5], [0x5dc, 0x5dd]]
for y in range(H):
    for x in range(W): G[(x, y)] = GRASS
def put(x, y, v): G[(x, y)] = v
def claim(x, y, w, h, name):
    for j in range(h):
        for i in range(w):
            if OCC.get((x + i, y + j)) == 'enclos' and name in ('foin', 'abreuvoir', 'baie'): continue     # objets poses dans un enclos
            assert (x + i, y + j) not in OCC, 'chevauchement %s avec %s en %s' % (name, OCC[(x + i, y + j)], (x + i, y + j))
            assert 1 <= x + i <= W - 2 and 0 <= y + j <= H - 3, (name, x + i, y + j)
            OCC[(x + i, y + j)] = name
def tree(x, y):
    for j in range(2):
        for i in range(2): put(x + i, y + j, TREE_RAW[j][i])
GATE_X, WATER_X = 22, 21
# ---- variantes de palette (toits) : on duplique les metatuiles de maison avec la palette 11 / 12
mt = bytearray(open(SD + 'metatiles.bin', 'rb').read()); att = bytearray(open(SD + 'metatile_attributes.bin', 'rb').read())
pmt = open(PD + 'metatiles.bin', 'rb').read(); patt = open(PD + 'metatile_attributes.bin', 'rb').read()
def mt_ent(i): return list(struct.unpack('<8H', (mt[(i - 640) * 16:(i - 640) * 16 + 16] if i >= 640 else pmt[i * 16:i * 16 + 16])))
def mt_att(i): return (att[(i - 640) * 4:(i - 640) * 4 + 4] if i >= 640 else patt[i * 4:i * 4 + 4])
VAR = {}
def variant(i, pf, pt):
    key = (i, pf, pt)
    if key in VAR: return VAR[key]
    e = mt_ent(i)
    if not any((v >> 12) == pf for v in e): VAR[key] = i; return i
    e = [((v & 0xfff) | (pt << 12)) if (v >> 12) == pf else v for v in e]
    mt.extend(struct.pack('<8H', *e)); att.extend(mt_att(i))
    VAR[key] = 640 + len(mt) // 16 - 1; return VAR[key]
def shift_pal(srcfile, dst, hue, ls=1.0, ss=1.0):
    L = open(srcfile).read().split(); n = int(L[2]); cols = [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
    out = [cols[0]]
    for (r, g, b) in cols[1:]:
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if s > 0.25 and (h * 360 >= 300 or h * 360 <= 45): h = hue / 360; l = min(1, l * ls); s = min(1, s * ss)
        r, g, b = colorsys.hls_to_rgb(h, l, s); out.append((int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)))
    open(dst, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
shift_pal(PD + 'palettes/01.pal', SD + 'palettes/11.pal', 258, 1.25, 0.7)    # toit ardoise-violet (maisons Petalburg)
shift_pal(SD + 'palettes/10.pal', SD + 'palettes/12.pal', 38, 1.0, 1.5)      # toit ocre dore (maisons Littleroot)
def chunk(srcmap, sw, x0, y0, cw, ch, dx, dy, name, pal=None):
    claim(dx, dy, cw, ch, name)
    door = None
    for j in range(ch):
        for i in range(cw):
            v = remap(srcmap[(y0 + j) * sw + x0 + i]); m = v & 0x3ff
            if pal: m = variant(m, *pal)
            put(dx + i, dy + j, (v & ~0x3ff) | m)
            if int.from_bytes(mt_att(m), 'little') & 0x1ff == 0x69: door = (dx + i, dy + j)
    return door
PBP, LRP = (1, 11), (10, 12)
# ---- cadre d'arbres
for x in range(0, W, 2):
    if x != GATE_X: tree(x, 0)
for y in range(2, H - 2, 2):
    tree(0, y)
    if y != 6: tree(W - 2, y)                  # ouverture vers le grand ranch (x=42..43, y=6..7)
for x in range(0, W - 1, 2):
    if x not in (20, 22): tree(x, H - 2)
for y in (H - 2, H - 1):
    put(20, y, 0x400 | 53); put(24, y, 0x400 | 53)
    for x in (21, 22, 23): put(x, y, water(209))
# ---- batiments (le plan d'occupation refuse tout chevauchement)
D = {}
D['player'] = chunk(LR, 20, 2, 4, 5, 5, 5, 5, 'maison joueur')
D['ranch'] = chunk(PB, 30, 5, 2, 5, 4, 34, 5, 'ranch')
D['museum'] = chunk(PB, 30, 12, 4, 6, 5, 5, 17, 'musee')
D['lab'] = chunk(LR, 20, 3, 12, 7, 5, 31, 17, 'labo')
D['hA'] = chunk(PB, 30, 5, 2, 5, 4, 12, 6, 'maison A ardoise', PBP)
D['hC'] = chunk(PB, 30, 5, 2, 5, 4, 12, 14, 'maison C', None)
D['hD'] = chunk(PB, 30, 9, 16, 4, 4, 11, 27, 'maison D ardoise', PBP)
D['hE'] = chunk(LR, 20, 2, 4, 5, 5, 3, 27, 'maison E ocre', LRP)
D['garden'] = chunk(PB, 30, 18, 20, 8, 7, 34, 27, 'maison jardin', None)
for k, v in D.items(): assert v, 'porte introuvable ' + k
assert D['player'] == (8, 9) and D['ranch'] == (36, 8) and D['museum'] == (8, 21) and D['lab'] == (35, 21), D
open('/tmp/grenalux_doors.json', 'w').write(json.dumps(D))
# ---- decors a emprise
def place_sm(sm, x0, y0, w, h, name):
    claim(x0, y0, w, h, name)
    for (i, j), m in sm.items(): put(x0 + i, y0 + j, 0x400 | m)
place_sm(C.BIG, 21, 21, 3, 3, 'monument')
place_sm(C.BIG, 18, 8, 3, 3, 'cristal garde O'); place_sm(C.BIG, 25, 8, 3, 3, 'cristal garde E')
place_sm(C.MINE, 38, 22, 3, 3, 'mine')
for k, (x, y, v) in enumerate(((38, 14, 0), (40, 16, 1), (38, 18, 1), (40, 20, 0))): place_sm(C.BOUL[v], x, y, 2, 2, 'bloc%d' % k)
def one(x, y, v, name): claim(x, y, 1, 1, name); put(x, y, 0x400 | v)
for (x, y) in ((21, 3), (24, 3), (21, 7), (24, 7), (10, 11), (18, 11), (26, 11), (34, 11), (10, 14), (18, 14), (30, 14), (38, 11),
               (15, 19), (30, 19), (15, 25), (30, 25), (10, 31), (16, 26)):
    if (x, y) in OCC: continue
    one(x, y, C.LAMP, 'lampe')
for (x, y) in ((38, 17), (41, 14), (41, 19), (38, 21), (41, 22), (37, 24), (41, 11), (41, 18)): one(x, y, C.ROCK, 'rocher')
for (x, y) in ((10, 9), (37, 9), (36, 22), (11, 21), (21, 10), (10, 15)): one(x, y, 3, 'panneau')
# ---- jardin de baies du ranch (decoratif, baies non recoltables) a l'ouest du ranch
def pen(x0, y0, x1, y1, gaps, name):
    for x in range(x0, x1 + 1):
        for y in (y0, y1):
            if (x, y) not in gaps: one(x, y, C.FENCE_H, name)
    for y in range(y0 + 1, y1):
        for x in (x0, x1):
            if (x, y) not in gaps: one(x, y, C.FENCE_V, name)
    claim(x0 + 1, y0 + 1, x1 - x0 - 1, y1 - y0 - 1, 'enclos')
pen(28, 3, 33, 9, {(30, 9), (31, 9)}, 'cloture jardin')
for y in range(4, 9):
    for x in range(29, 33): put(x, y, walk(C.SOIL))
for k, x in enumerate(range(29, 33)):
    one(x, 5, C.BUSH[(0, 1, 2, 0)[k]], 'baie'); one(x, 7, C.BUSH[(2, 0, 1, 2)[k]], 'baie')
for _x in range(20, 25):
    for _y in range(20, 25):
        if (_x, _y) not in OCC: claim(_x, _y, 1, 1, 'ilot')
for y in range(20, 25):
    for x in range(20, 25):
        if OCC[(x, y)] == 'ilot': put(x, y, FLOWER if (x in (20, 24) or y in (20, 24)) else GRASS)
# bassin (eau) : x18..27, y29..32 + canal vers la route 21
claim(18, 29, 10, 4, 'bassin'); claim(21, 33, 3, 1, 'canal')
for x in range(18, 28):
    for y in range(29, 33):
        base = 200 if y == 29 else 216 if y == 32 else 208
        put(x, y, water(base + (0 if x == 18 else 2 if x == 27 else 1)))
for y in range(32, H - 2):
    for x in (21, 22, 23): put(x, y, water(209))
# ---- chemins
PATH = set()
def rect(x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x, y) in OCC: continue
            PATH.add((x, y))
rect(GATE_X, 0, GATE_X + 1, 19)
rect(7, 12, 40, 13)
rect(7, 10, 8, 11); rect(35, 9, 36, 11); rect(30, 9, 31, 11); rect(39, 6, 43, 7)
rect(16, 18, 29, 26)
rect(7, 22, 8, 25); rect(7, 24, 15, 25)
rect(34, 22, 35, 25); rect(30, 24, 35, 25); rect(36, 25, 41, 26)
rect(17, 27, 28, 28); rect(16, 27, 17, 33); rect(28, 27, 29, 33)
for k in ('hA', 'hC', 'hD', 'hE', 'garden'): pass
def passable(c):
    x, y = c
    return 2 <= x <= W - 3 and 1 <= y <= H - 4 and c not in OCC
def connect(start):
    """chemin le plus court depuis `start` jusqu'au reseau de chemins existant."""
    if start in PATH: return
    prev = {start: None}; q = collections.deque([start])
    while q:
        c = q.popleft()
        if c in PATH:
            while c is not None: PATH.add(c); c = prev[c]
            return
        for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + d[0], c[1] + d[1])
            if n not in prev and passable(n): prev[n] = c; q.append(n)
    raise AssertionError('porte isolee %s' % (start,))
for k in ('hA', 'hC', 'hD', 'hE'): connect((D[k][0], D[k][1] + 1))
connect((39, 8))                           # le chemin du grand ranch rejoint la grande rue
connect((33, 31))                          # le potager s'ouvre a l'ouest (rangee 4 du bloc)
connect((39, 25))
def path_id(x, y):
    N = (x, y - 1) in PATH or y == 0; S = (x, y + 1) in PATH; Wn = (x - 1, y) in PATH; E = (x + 1, y) in PATH
    if N and S and Wn and E: return 289
    if not N and not Wn and S and E: return 280
    if not N and not E and S and Wn: return 282
    if not S and not Wn and N and E: return 296
    if not S and not E and N and Wn: return 298
    if not N and S and Wn and E: return 281
    if not S and N and Wn and E: return 297
    if not Wn and N and S and E: return 288
    if not E and N and S and Wn: return 290
    return 289
for (x, y) in PATH:
    assert (x, y) not in OCC, ("chemin sur", OCC.get((x, y)), x, y)
    put(x, y, walk(path_id(x, y)))
# ---- vegetation : bosquets, fleurs en massifs
rnd = random.Random(6061)
def near(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            c = (x + i, y + j)
            if c in PATH or c in OCC: return True
    return False
def free_tree(x, y): return 2 <= x <= W - 4 and 2 <= y <= H - 6 and all((x + i, y + j) not in OCC and not near(x + i, y + j, 1) for i in range(2) for j in range(2))
def grove(cx, cy, n, spread):
    k = 0; tries = 0
    while k < n and tries < 600:
        tries += 1
        x = int(rnd.gauss(cx, spread)); y = int(rnd.gauss(cy, spread))
        if free_tree(x, y):
            tree(x, y); claim(x, y, 2, 2, 'arbre'); k += 1
for (cx, cy, n, s) in ((3, 10, 5, 2.2), (3, 24, 4, 2), (13, 22, 3, 1.5), (31, 31, 5, 2), (41, 9, 4, 2), (26, 15, 3, 1.8), (6, 14, 2, 1.5),
                       (20, 14, 2, 1.5), (4, 4, 2, 1.5), (40, 31, 2, 1.5), (14, 31, 2, 1)): grove(cx, cy, n, s)
for _ in range(16):
    cx, cy = rnd.randint(3, W - 4), rnd.randint(3, H - 6)
    for _ in range(rnd.randint(4, 9)):
        x, y = cx + rnd.randint(-2, 2), cy + rnd.randint(-1, 1)
        if 2 <= x <= W - 3 and 2 <= y <= H - 5 and G[(x, y)] == GRASS and (x, y) not in OCC and (x, y) not in PATH: put(x, y, FLOWER)
placed = 0; tries = 0
while placed < 14 and tries < 3000:
    tries += 1
    x, y = rnd.randint(2, W - 3), rnd.randint(2, H - 5)
    if G[(x, y)] in (GRASS, FLOWER) and (x, y) not in OCC and (x, y) not in PATH and not near(x, y, 1):
        put(x, y, 0x400 | rnd.choice(C.SM)); claim(x, y, 1, 1, 'petit cristal'); placed += 1
# ---- PNJ d'ambiance (cases reservees) ; coordonnees reprises par grenalux_events.py
NPC = {'gardener': (31, 8), 'miner': (41, 26), 'oldman': (19, 22), 'girl': (17, 30), 'boy': (29, 31), 'scientist': (33, 23), 'lady': (36, 23)}
for k, c in NPC.items(): assert (c not in OCC or OCC[c] == 'enclos') and G[c] in (GRASS, FLOWER, walk(C.SOIL)) or c in PATH, (k, c, hex(G[c]))
json.dump(NPC, open('/tmp/grenalux_npc.json', 'w'))
# ---- ecriture
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/PalletTown/border.bin', 'wb').write(struct.pack('<4H', 0x5d4, 0x5d5, 0x5dc, 0x5dd))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_PALLET_TOWN':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralEmerald', secondary_tileset='gTileset_PetalburgEmerald')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
blocked = {(x, y) for y in range(H) for x in range(W) if (g[y * W + x] & 0xc00) or ((g[y * W + x] >> 12) == 1)}
json.dump({'w': W, 'h': H, 'blocked': [list(c) for c in sorted(blocked)]}, open('/tmp/grenalux_col.json', 'w'))
# ---- accessibilite : tout doit etre atteignable depuis l'avenue
seen = {(22, 5)}; q = collections.deque([(22, 5)])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in blocked and n not in seen: seen.add(n); q.append(n)
for k, (x, y) in D.items(): assert (x, y + 1) in seen or k == 'garden', 'porte inatteignable ' + k
for k, c in NPC.items(): assert c in seen, 'PNJ inatteignable ' + k
assert (39, 25 + 1) in seen and (22, 0) in seen
TOWN_NPC = NPC
print('Grenalux v6', W, 'x', H, '| metatuiles secondaires', len(mt) // 16, '| tuiles', len(C.tiles))

# ======================================================================================================
# LE GRAND RANCH (32x24) : la suite du ranch de Zephyr, visible a l'est de la ville par l'ouverture du cadre
# (connexion "droite" de Grenalux, decalage 0). Un domaine entier : ecurie, grange, trois enclos, bouveries, cristaux.
# ======================================================================================================
W, H = 32, 24
G = {(x, y): GRASS for y in range(H) for x in range(W)}; OCC = {}; PATH = set()
for x in range(0, W, 2): tree(x, 0)
for y in range(2, H - 2, 2):
    if y != 6: tree(0, y)
    tree(W - 2, y)
for x in range(0, W, 2): tree(x, H - 2)
R = {}
R['stable'] = chunk(PB, 30, 5, 2, 5, 4, 3, 2, 'ecurie', PBP)
assert R['stable']
place_sm(C.BARN, 22, 2, 5, 4, 'grange'); place_sm(C.SILO, 27, 2, 2, 4, 'silo')
R['barn'] = (24, 5)
def pen(x0, y0, x1, y1, gaps, name):
    for x in range(x0, x1 + 1):
        for y in (y0, y1):
            if (x, y) not in gaps: one(x, y, C.FENCE_H, name)
    for y in range(y0 + 1, y1):
        for x in (x0, x1):
            if (x, y) not in gaps: one(x, y, C.FENCE_V, name)
    claim(x0 + 1, y0 + 1, x1 - x0 - 1, y1 - y0 - 1, 'enclos')
pen(10, 2, 19, 5, {(14, 5), (15, 5)}, 'cloture C')
pen(3, 10, 12, 17, {(7, 10), (8, 10)}, 'cloture A')
pen(16, 10, 27, 17, {(21, 10), (22, 10)}, 'cloture B')      # (27,13..14) : coupee par Onybris apres l'attaque (map script)
place_sm(C.BIG, 5, 19, 3, 3, 'cristal SO'); place_sm(C.BIG, 22, 19, 3, 3, 'cristal SE')
place_sm(C.BOUL[0], 9, 19, 2, 2, 'bloc'); place_sm(C.BOUL[1], 27, 19, 2, 2, 'bloc')
for (x, y) in ((17, 20), (18, 20), (19, 20)): one(x, y, C.HAY, 'foin')
for (x, y) in ((4, 11), (5, 11), (17, 11), (11, 3), (11, 4)): one(x, y, C.HAY, 'foin')
for (x, y) in ((11, 16), (26, 16), (18, 3)): one(x, y, C.TROUGH, 'abreuvoir')
for (x, y) in ((3, 8), (11, 8), (17, 8), (25, 8), (9, 5), (20, 5), (12, 19), (20, 19), (15, 21)): one(x, y, C.LAMP, 'lampe')
for (x, y) in ((2, 9), (12, 20), (28, 16), (2, 18), (29, 9), (16, 19)): one(x, y, C.ROCK, 'rocher')
rect(0, 6, 29, 7); rect(7, 8, 8, 9); rect(21, 8, 22, 9); rect(13, 8, 14, 21)
connect((R['stable'][0], R['stable'][1] + 1)); connect((R['barn'][0], R['barn'][1] + 1))
for (x, y) in PATH:
    assert (x, y) not in OCC, ('chemin sur', OCC.get((x, y)), x, y)
    put(x, y, walk(path_id(x, y)))
rnd = random.Random(7733)
for (cx, cy, n, s_) in ((29, 20, 3, 1.5), (2, 14, 3, 1.5), (3, 20, 2, 1.2), (29, 3, 3, 1.5), (16, 3, 0, 1)): grove(cx, cy, n, s_)
for _ in range(14):
    cx, cy = rnd.randint(3, W - 4), rnd.randint(3, H - 4)
    for _ in range(rnd.randint(4, 8)):
        x, y = cx + rnd.randint(-2, 2), cy + rnd.randint(-1, 1)
        if 2 <= x <= W - 3 and 2 <= y <= H - 4 and G[(x, y)] == GRASS and (x, y) not in OCC and (x, y) not in PATH: put(x, y, FLOWER)
RNPC = {'r_hand1': (9, 7), 'r_hand2': (14, 12), 'r_girl': (24, 7), 'r_slowpoke': (6, 13), 'r_psyduck': (10, 15), 'r_doduo': (19, 13),
        'r_nidoranm': (24, 15), 'r_nidoranf': (18, 16), 'r_meowth': (13, 3), 'r_jigglypuff': (17, 4), 'r_hand3': (28, 13)}
rb = {(x, y) for y in range(H) for x in range(W) if (G[(x, y)] & 0xc00) or ((G[(x, y)] >> 12) == 1)}
seen = {(0, 6)}; q = collections.deque([(0, 6)])
while q:
    c = q.popleft()
    for d in ((0, 1), (1, 0), (-1, 0), (0, -1)):
        n = (c[0] + d[0], c[1] + d[1])
        if 0 <= n[0] < W and 0 <= n[1] < H and n not in rb and n not in seen: seen.add(n); q.append(n)
for k, c in RNPC.items(): assert c in seen and c not in rb, ('PNJ du ranch inatteignable', k, c)
for k in ('stable', 'barn'): assert (R[k][0], R[k][1] + 1) in seen, k
assert (1, 6) in seen and (1, 7) in seen
json.dump(RNPC, open('/tmp/grenalux_ranch_npc.json', 'w'))
g = [G[(x, y)] for y in range(H) for x in range(W)]
import os
os.makedirs('data/layouts/PalletTownRanch', exist_ok=True)
open('data/layouts/PalletTownRanch/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/PalletTownRanch/border.bin', 'wb').write(struct.pack('<4H', 0x5d4, 0x5d5, 0x5dc, 0x5dd))
L = json.load(open('data/layouts/layouts.json'))
L['layouts'] = [l for l in L['layouts'] if l.get('id') != 'LAYOUT_PALLET_TOWN_RANCH']
L['layouts'].append({"id": "LAYOUT_PALLET_TOWN_RANCH", "name": "PalletTownRanch_Layout", "width": W, "height": H, "border_width": 2, "border_height": 2,
    "primary_tileset": "gTileset_GeneralEmerald", "secondary_tileset": "gTileset_PetalburgEmerald",
    "border_filepath": "data/layouts/PalletTownRanch/border.bin", "blockdata_filepath": "data/layouts/PalletTownRanch/map.bin"})
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
open(SD + 'metatiles.bin', 'wb').write(mt); open(SD + 'metatile_attributes.bin', 'wb').write(att)
assert len(mt) // 16 <= 384, len(mt) // 16
print('Grand ranch', W, 'x', H, '| metatuiles secondaires', len(mt) // 16)
