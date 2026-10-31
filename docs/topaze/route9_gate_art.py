# v32 : cabane-portail cote ROUTE 9 : copie de la cabane sur arbre de Tourmalia (5 x 8 cases) injectee dans le tileset de la Route 9
# (nouvelles tuiles + 2 palettes libres 6 (primaire, propre a la Route 9) et 8 (secondaire) de gTileset_GeneralRoute9V2/CeladonRoute9V2 + nouvelles metatuiles), posee a l'extremite ouest de la Route 9.
# Porte (2,4), echelle (2,7). Rejouable : repart toujours des fichiers d'origine sauvegardes dans docs/topaze/route9_gate/orig_*.
import pickle, struct, os, shutil
import numpy as np
from PIL import Image
SEC = 'data/tilesets/secondary/celadon_route9v2/'; PRI = 'data/tilesets/primary/general_route9v2/'; OD = 'docs/topaze/route9_gate/'; MAPBIN = 'data/layouts/Route9/map.bin'
FILES = {'tiles.png': SEC + 'tiles.png', 'metatiles.bin': SEC + 'metatiles.bin', 'metatile_attributes.bin': SEC + 'metatile_attributes.bin', '06.pal': PRI + 'palettes/06.pal', '08.pal': SEC + 'palettes/08.pal', 'map.bin': MAPBIN}
os.makedirs(OD, exist_ok=True)
for k, p in FILES.items():
    o = OD + 'orig_' + k
    if not os.path.exists(o): shutil.copy(p, o)
    else: shutil.copy(o, p)
grid, mts = pickle.load(open('docs/topaze/tourmalia_copy/grid.pkl', 'rb'))
X0 = 22; BX, BY, BW, BH = 29, 28, 5, 8                       # bloc (coordonnees ville) : x 29..33, y 28..35
block = [[grid[BY + j][X0 + BX + i] for i in range(BW)] for j in range(BH)]
EXT = [11, 37, 7, 64, 70, 53, 77, 16]                       # v33 : cabane longue vers la GAUCHE depuis la route (porte a l'est de la cabane, corps etire vers l'ouest)
block = [r[:1] + [EXT[_j]] * 4 + r[1:] for _j, r in enumerate(block)]; BW = 9; DOORX = 6
uniq = sorted({v for r in block for v in r})
subs = {(m, q): mts[m][(q // 2) * 8:(q // 2) * 8 + 8, (q % 2) * 8:(q % 2) * 8 + 8].astype(np.uint8) for m in uniq for q in range(4)}
def is_green(t): p = t.reshape(-1, 3).astype(int); return bool(((p[:, 1] > p[:, 0] + 8) & (p[:, 1] >= p[:, 2])).mean() > 0.5)
grp = {k: (0 if is_green(v) else 1) for k, v in subs.items()}
pals = []
for g in (0, 1):
    px = np.concatenate([v.reshape(-1, 3) for k, v in subs.items() if grp[k] == g])
    im = Image.fromarray(px.reshape(-1, 1, 3)).quantize(colors=15, method=Image.MEDIANCUT, dither=Image.NONE)
    pl = np.array(im.getpalette()[:45]).reshape(-1, 3).astype(int)
    pals.append(np.vstack([pl, np.zeros((15 - len(pl), 3), int)]) if len(pl) < 15 else pl)
BANK = (6, 8)
for g, b in enumerate(BANK):
    cols = [(0, 0, 0)] + [tuple((int(c) & 0xf8) | (int(c) >> 5) for c in p) for p in pals[g]]
    open((PRI if b < 7 else SEC) + 'palettes/%02d.pal' % b, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in cols))
timg = Image.open(SEC + 'tiles.png'); tw = timg.width // 8; nt0 = tw * (timg.height // 8)
TL = {}; newt = []
def tile_for(k):
    g = grp[k]; p = subs[k].reshape(-1, 3).astype(int); d = ((p[:, None, :] - pals[g][None, :, :]) ** 2).sum(-1)
    key = (g, tuple(int(i) + 1 for i in d.argmin(1)))
    if key not in TL: TL[key] = nt0 + len(newt); newt.append(key[1])
    return (640 + TL[key]) | (BANK[g] << 12)
mb = open(SEC + 'metatiles.bin', 'rb').read(); nm0 = len(mb) // 16; ab = open(SEC + 'metatile_attributes.bin', 'rb').read()
newid = {}; mbn = b''; abn = b''
for m in uniq:
    newid[m] = 640 + nm0 + len(newid)
    mbn += struct.pack('<8H', *([tile_for((m, q)) for q in range(4)] + [0, 0, 0, 0]))
    abn += struct.pack('<I', 0x69 if m == 70 else 0)                       # 70 = porte de cabane (comportement de porte)
assert nt0 + len(newt) <= 384 and nm0 + len(uniq) <= 384, ('trop de tuiles', nt0 + len(newt))
open(SEC + 'metatiles.bin', 'wb').write(mb + mbn); open(SEC + 'metatile_attributes.bin', 'wb').write(ab + abn)
rows = (nt0 + len(newt) + tw - 1) // tw; out = Image.new('P', (128, rows * 8), 0); out.putpalette(timg.getpalette()); out.paste(timg, (0, 0)); px = out.load()
for n, idx in enumerate(newt):
    t = nt0 + n; ox, oy = (t % tw) * 8, (t // tw) * 8
    for j, v in enumerate(idx): px[ox + j % 8, oy + j // 8] = v
out.save(SEC + 'tiles.png')
# --- carte : bloc pose en (0,0) de la Route 9
W9, H9 = 72, 20; g9 = list(struct.unpack('<%dH' % (W9 * H9), open(MAPBIN, 'rb').read()))
WALKB = {53, 62, 78, 97, 70}
for j in range(BH):
    for i in range(BW):
        v = block[j][i]; g9[j * W9 + i] = ((0x3000 if v in WALKB and not (v == 70 and i != DOORX) else 0x400) | newid[v])
open(MAPBIN, 'wb').write(struct.pack('<%dH' % len(g9), *g9))
print('cabane Route 9 : %d metatuiles, %d tuiles, porte (6,4), echelle (6,7)' % (len(uniq), len(newt)))
