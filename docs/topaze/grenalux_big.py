# Grenalux v5 : grande ville (44x36) aux couleurs du grenat. Meme pipeline que la v4 (reference conservee sur la
# branche grenalux-v4-reference et dans docs/topaze/reference/) mais avec un vrai plan de ville :
# avenue nord-sud, grande rue est-ouest, place centrale a monument de cristal, bassin sud relie a la route 21,
# quartiers de maisons, labo, musee, ranch, jardins, arbres, cristaux.
# Ordre : import_emerald_tiles.py -> grenat_palette.py -> grenalux_big.py   (depuis la racine, ../pokeemerald clone)
import struct, json, random, sys
sys.path.insert(0, 'docs/topaze')
# le calque des cristaux emprunte les couleurs du sol : le layout doit deja utiliser les tilesets d'Emeraude
_L = json.load(open('data/layouts/layouts.json'))
for _l in _L['layouts']:
    if _l.get('id') == 'LAYOUT_PALLET_TOWN':
        _l['primary_tileset'] = 'gTileset_GeneralEmerald'; _l['secondary_tileset'] = 'gTileset_PetalburgEmerald'
json.dump(_L, open('data/layouts/layouts.json', 'w'), indent=2)
open('data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<480H', *([0x3001] * 480)))   # carte provisoire 24x20 (lecture des couleurs)
import grenalux_crystals as C            # dessine/enregistre les cristaux (tuiles + palette 7) a l'import
EMD = '../pokeemerald/data/layouts/'
def src(name, w, h): return struct.unpack('<%dH' % (w * h), open(EMD + '%s/map.bin' % name, 'rb').read())
LR = src('LittlerootTown', 20, 20); PB = src('PetalburgCity', 30, 30)
def remap(v):
    m = v & 0x3ff
    return (v & ~0x3ff) | (m + 128 if m >= 512 else m)
W, H = 44, 36
G = {}
def walk(m): return 0x3000 | m
def water(m): return 0x1000 | m
GRASS, FLOWER = walk(1), walk(4)
TREE_RAW = [[0x5d4, 0x5d5], [0x5dc, 0x5dd]]
for y in range(H):
    for x in range(W): G[(x, y)] = GRASS
def put(x, y, v): G[(x, y)] = v
def chunk(srcmap, sw, x0, y0, cw, ch, dx, dy):
    for j in range(ch):
        for i in range(cw): put(dx + i, dy + j, remap(srcmap[(y0 + j) * sw + x0 + i]))
def tree(x, y):
    for j in range(2):
        for i in range(2): put(x + i, y + j, TREE_RAW[j][i])
GATE_X = 22                              # ouverture nord (route 1) en x=22..23
WATER_X = 21                             # entree d'eau sud (route 21) en x=21..23
# ---- cadre d'arbres
for x in range(0, W, 2):
    if x != GATE_X: tree(x, 0)
for y in range(2, H - 2, 2): tree(0, y); tree(W - 2, y)
for x in range(0, W - 1, 2):
    if x not in (20, 22): tree(x, H - 2)           # 20..21 / 22..23 : entree d'eau
for y in (H - 2, H - 1):
    put(20, y, 0x400 | 53); put(24, y, 0x400 | 53)
    for x in (21, 22, 23): put(x, y, water(209))
for x in range(W - 2, 0, -2): pass
# ---- reseau de chemins (sable auto-tuile)
PATH = set()
def rect(x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): PATH.add((x, y))
rect(GATE_X, 0, GATE_X + 1, 17)          # avenue nord-sud
rect(7, 12, 37, 13)                      # grande rue est-ouest
rect(7, 10, 8, 11)                       # perron maison du joueur
rect(35, 9, 36, 11)                      # perron du ranch
rect(16, 18, 29, 26)                     # place centrale
rect(7, 22, 8, 25); rect(7, 24, 15, 25)  # chemin du musee vers la place
rect(34, 22, 35, 25); rect(30, 24, 35, 25)   # chemin du labo vers la place
rect(21, 27, 24, 28)                     # promenade vers le bassin
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
for (x, y) in PATH: put(x, y, walk(path_id(x, y)))
# ---- batiments
chunk(LR, 20, 2, 4, 5, 5, 5, 5)          # maison du joueur : porte (8,9)
chunk(PB, 30, 5, 2, 5, 4, 34, 5)         # ranch du rival   : porte (36,8)
chunk(PB, 30, 12, 4, 6, 5, 5, 17)        # musee            : porte (8,21)
chunk(LR, 20, 3, 12, 7, 5, 31, 17)       # laboratoire      : porte (35,21)
chunk(PB, 30, 5, 2, 5, 4, 12, 6)         # maisons du village (decor)
chunk(LR, 20, 2, 4, 5, 5, 28, 5)
chunk(PB, 30, 9, 16, 4, 4, 11, 27)
chunk(PB, 30, 9, 16, 4, 4, 30, 28)
chunk(PB, 30, 18, 20, 8, 7, 34, 29)      # maison a potager
chunk(LR, 20, 2, 4, 5, 5, 3, 28)
# ---- bassin sud et entree d'eau
for x in range(18, 28):
    for y in range(29, 33):
        top, bot = (y == 29), (y == 32)
        L, R = (x == 18), (x == 27)
        base = 200 if top else 216 if bot else 208
        m = base + (0 if L else 2 if R else 1)
        put(x, y, water(m))
for x in (21, 22, 23): put(x, 32, water(209))
for y in range(33, H - 2):
    for x in (21, 22, 23): put(x, y, water(209))
# ---- decor : monument central (cristal geant), cristaux, arbres, fleurs
def blocked(x, y): return G[(x, y)] != GRASS and G[(x, y)] != FLOWER
def place_sm(sm, x0, y0):
    for (i, j), m in sm.items(): put(x0 + i, y0 + j, 0x400 | m)
for y in range(20, 25):                  # ilot d'herbe fleuri autour du monument (sinon fond d'herbe sur le sable)
    for x in range(20, 25): PATH.discard((x, y)); put(x, y, FLOWER if (x in (20, 24) or y in (20, 24)) else GRASS)
place_sm(C.BIG, 21, 21); place_sm(C.BIG, 17, 8); place_sm(C.BIG, 28, 8)
def near_blocked(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if 0 <= x + i < W and 0 <= y + j < H and ((x + i, y + j) in PATH or blocked(x + i, y + j)): return True
    return False
rnd = random.Random(2077)
def margin_ok(x, y): return 3 <= x <= W - 4 and 3 <= y <= H - 5
placed = 0; tries = 0
while placed < 34 and tries < 4000:
    tries += 1
    x, y = rnd.randint(2, W - 4), rnd.randint(2, H - 5)
    if all(not blocked(x + i, y + j) and not near_blocked(x + i, y + j, 1) for i in range(2) for j in range(2)):
        tree(x, y); placed += 1
placed = 0; tries = 0
while placed < 22 and tries < 4000:
    tries += 1
    x, y = rnd.randint(2, W - 3), rnd.randint(2, H - 5)
    if not blocked(x, y) and (x, y) not in PATH and not near_blocked(x, y, 1):
        put(x, y, 0x400 | rnd.choice(C.SM)); placed += 1
for _ in range(140):
    x, y = rnd.randint(2, W - 3), rnd.randint(2, H - 5)
    if G[(x, y)] == GRASS and (x, y) not in PATH: put(x, y, FLOWER)
SIGN = 0x400 | 3
for (x, y) in ((10, 9), (33, 8), (38, 22), (11, 21), (21, 10), (10, 15)):
    if G[(x, y)] in (GRASS, FLOWER): put(x, y, SIGN)
# ---- ecriture
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/PalletTown/border.bin', 'wb').write(struct.pack('<4H', 0x5d4, 0x5d5, 0x5dc, 0x5dd))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_PALLET_TOWN':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralEmerald', secondary_tileset='gTileset_PetalburgEmerald')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'w': W, 'h': H, 'blocked': [[x, y] for y in range(H) for x in range(W) if (g[y * W + x] & 0xc00) or ((g[y * W + x] >> 12) == 1)]},
          open('/tmp/grenalux_col.json', 'w'))
print('grande Grenalux', W, 'x', H)
