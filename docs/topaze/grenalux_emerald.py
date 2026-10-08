# Grenalux v3 : meme plan "village de campagne" mais avec les vrais decors GBA (tilesets Emeraude importes par
# import_emerald_tiles.py). Les batiments sont copies des cartes d'Emeraude (Littleroot, Petalburg) puis assembles
# selon NOTRE plan. A lancer apres import_emerald_tiles.py, depuis la racine du depot, avec ../pokeemerald clone.
import struct, json, sys
EMD = '../pokeemerald/data/layouts/'
def src(name, w, h):
    return struct.unpack('<%dH' % (w * h), open(EMD + '%s/map.bin' % name, 'rb').read())
LR = src('LittlerootTown', 20, 20); PB = src('PetalburgCity', 30, 30)
def remap(v):
    m = v & 0x3ff
    return (v & ~0x3ff) | (m + 128 if m >= 512 else m)
W, H = 24, 20
G = {}
def walk(m): return 0x3000 | m
def water(m): return 0x1000 | m
TOUCH = set()
def put(x, y, v): G[(x, y)] = v; TOUCH.add((x, y))
def chunk(srcmap, sw, x0, y0, cw, ch, dx, dy):
    for j in range(ch):
        for i in range(cw):
            put(dx + i, dy + j, remap(srcmap[(y0 + j) * sw + x0 + i]))
GRASS, FLOWER = walk(1), walk(4)
for y in range(H):
    for x in range(W): put(x, y, GRASS)
# ---- cadre d'arbres (2x2) : [468 469 / 476 477]
TREE = [[468 | 0x400 & 0, 469], [476, 477]]
TREE_RAW = [[0x5d4, 0x5d5], [0x5dc, 0x5dd]]
def tree(x, y):
    for j in range(2):
        for i in range(2): put(x + i, y + j, TREE_RAW[j][i])
def border():
    for x in range(0, W, 2):
        if x in (12,): continue
        for y in (0,): tree(x, y)
    # le haut : on laisse l'ouverture x=12..13 pour la route 1 (x=12 est pair : on saute cette colonne)
    for y in range(2, H - 2, 2):
        tree(0, y); tree(22, y)
    for x in (0, 2, 4):
        tree(x, 18)
    for x in (11, 13, 15, 17, 19):
        tree(x, 18)
    tree(22, 18)
border()
for y in (18, 19):                     # buissons de part et d'autre de l'entree d'eau
    for x in (6, 10, 21):
        put(x, y, 0x400 | 53)
# ---- chemins (autotuile en sable)
PATH = set()
for y in range(0, 18): PATH |= {(12, y), (13, y)}
for y in (8, 9):
    for x in range(5, 20): PATH.add((x, y))
for x in (17, 18): PATH.add((x, 7))
PATH |= {(5, 15), (6, 15), (5, 16), (6, 16)}        # parvis du musee
PATH |= {(17, 15), (18, 15), (17, 16), (18, 16)}    # parvis du labo
def path_id(x, y):
    N, S, Wn, E = ((x, y - 1) in PATH or y == 0), ((x, y + 1) in PATH), ((x - 1, y) in PATH), ((x + 1, y) in PATH)
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
# ---- batiments (copies d'Emeraude)
chunk(LR, 20, 2, 4, 5, 5, 3, 3)        # maison du joueur : porte (6,7)
chunk(PB, 30, 5, 2, 5, 4, 16, 3)       # ranch du rival   : porte (18,6)
chunk(PB, 30, 12, 4, 6, 5, 3, 10)      # musee (ex-arene Petalburg) : porte (6,14)
chunk(LR, 20, 3, 12, 7, 5, 14, 10)     # laboratoire (ex-labo Birch) : porte (18,14)
# ---- bassin du sud (entree d'eau vers la route 21 en x=7..9)
POND = {(7, 16): 200, (8, 16): 201, (9, 16): 201, (10, 16): 201, (11, 16): 202,
        (7, 17): 208, (8, 17): 209, (9, 17): 209, (10, 17): 209, (11, 17): 210}
for (x, y), m in POND.items(): put(x, y, water(m))
for y in (18, 19):
    for x in (7, 8, 9): put(x, y, water(209))
# ---- decor : arbres isoles, fleurs, panneaux
for (x, y) in ((9, 3), (9, 5), (14, 4), (9, 12), (10, 14), (20, 17)):
    for j in range(2):
        for i in range(2):
            if (x + i, y + j) not in PATH: put(x + i, y + j, TREE_RAW[j][i])
for (x, y) in ((4, 8), (8, 8), (11, 7), (10, 9), (3, 9), (15, 12), (14, 7), (16, 9), (20, 8), (19, 16), (12, 3)):
    pass
for (x, y) in ((4, 8), (8, 7), (3, 9), (11, 7), (11, 9), (20, 8), (15, 7), (15, 16), (14, 17), (9, 15), (10, 13), (3, 15), (19, 9)):
    if (x, y) not in PATH and G[(x, y)] == GRASS: put(x, y, FLOWER)
for (x, y) in ((8, 3), (8, 8)): pass
# panneaux (bloc 3 d'Emeraude = panneau, infranchissable)
SIGN = 0x400 | 3
for (x, y) in ((8, 7), (15, 7), (19, 15), (11, 7), (9, 10), (4, 15)):
    if G[(x, y)] in (GRASS, FLOWER): put(x, y, SIGN)
# ---- ecriture
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/PalletTown/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/PalletTown/border.bin', 'wb').write(struct.pack('<4H', 0x5d4, 0x5d5, 0x5dc, 0x5dd))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_PALLET_TOWN':
        l['primary_tileset'] = 'gTileset_GeneralEmerald'; l['secondary_tileset'] = 'gTileset_PetalburgEmerald'
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'w': W, 'h': H, 'blocked': [[x, y] for y in range(H) for x in range(W) if (g[y * W + x] & 0xc00) or ((g[y * W + x] >> 12) == 1)]},
          open('/tmp/grenalux_col.json', 'w'))
print('ok')
