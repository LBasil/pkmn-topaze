#!/usr/bin/env python3
"""Arene de NOX v2 (retours Basil 21/10 : decor + mecanique des pastilles = non) : plus de pastilles. Salle droite de type Rustboro (couloirs en serpent,
aucun puzzle), tuiles Rustboro recolorees ténèbres/spectre (copie de gym_rustboro_pri/sec passee de la braise au violet nuit),
layout LAYOUT_GYM_NOX, 7 dresseurs + Nox. Idempotent."""
import os, shutil, json, colorsys, sys
sys.path.insert(0, 'docs/topaze'); from gym_lib import apply_gym
P, S = 'data/tilesets/primary/', 'data/tilesets/secondary/'
def rp(path):
    L = open(path).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
def ghost(c):
    h, s, v = colorsys.rgb_to_hsv(*[x / 255 for x in c]); h *= 360
    if v < 0.04: return c
    if s > 0.45 and (h < 50 or h >= 330) and v > 0.5: h, s, v = 275, 0.6, min(1, v * 0.78)       # braise vive -> violet spectral
    elif s > 0.25: h, s, v = 268, s * 0.7, v * 0.8
    else: h, s, v = 262, 0.30, v * 0.85
    r = colorsys.hsv_to_rgb((h % 360) / 360, min(1, s), min(1, v))
    return tuple(int(round(x * 255)) for x in r)
def sub(path, text):
    s = open(path).read()
    if text.split('\n')[0] in s: return
    open(path, 'w').write(s + '\n' + text)
def make(base, src, dst, const, secondary):
    sd, d = base + src + '/', base + dst + '/'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d + 'palettes')
    for f in ('tiles.png', 'metatiles.bin', 'metatile_attributes.bin'): shutil.copy(sd + f, d + f)
    for i in range(16):
        cols = rp(sd + 'palettes/%02d.pal' % i)
        out = [cols[0]] + [ghost(c) for c in cols[1:]]
        open(d + 'palettes/%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
    pals = ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
    sub('src/data/tilesets/graphics.h', 'const u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (const, d, const, pals))
    sub('src/data/tilesets/metatiles.h', 'const u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (const, d, const, d))
    sub('src/data/tilesets/headers.h', 'const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n' % (const, 'TRUE' if secondary else 'FALSE', const, const, const, const))
make(P, 'gym_rustboro_pri', 'gym_nox_pri', 'GymNoxPri', False)
make(S, 'gym_rustboro_sec', 'gym_nox_sec', 'GymNoxSec', True)
os.makedirs('data/layouts/GymNox', exist_ok=True)
for f in ('map.bin', 'border.bin'): shutil.copy('data/layouts/GymEmRustboro/' + f, 'data/layouts/GymNox/' + f)
jf = 'data/layouts/layouts.json'; j = json.load(open(jf))
if not any(l.get('id') == 'LAYOUT_GYM_NOX' for l in j['layouts']):
    src = [l for l in j['layouts'] if l.get('id') == 'LAYOUT_GYM_EM_RUSTBORO'][0]
    n = dict(src); n.update(id='LAYOUT_GYM_NOX', name='GymNox_Layout', primary_tileset='gTileset_GymNoxPri', secondary_tileset='gTileset_GymNoxSec',
                           border_filepath='data/layouts/GymNox/border.bin', blockdata_filepath='data/layouts/GymNox/map.bin')
    j['layouts'].append(n); json.dump(j, open(jf, 'w'), indent=2); open(jf, 'a').write('\n')
apply_gym('SaffronCity_Gym', 'LAYOUT_GYM_NOX',
    objs={0: (2, 17, 'FACE_RIGHT', 4), 1: (8, 16, 'FACE_LEFT', 4), 2: (5, 13, 'FACE_DOWN', 4), 3: (2, 6, 'FACE_DOWN', 3),
          4: (3, 4, 'FACE_RIGHT', 4), 5: (7, 4, 'FACE_LEFT', 4), 6: (5, 2, 'FACE_DOWN'), 7: (7, 14, 'FACE_LEFT', 3), 8: (3, 18, 'FACE_DOWN')},
    warps=[(5, 19), (6, 19), (6, 19)], bg=[(2, 18), (8, 18)])
print('ok')
