#!/usr/bin/env python3
"""Route 23 + Plateau Indigo : palette « aube » (24/10) : la route de la Ligue se leve apres la nuit bleue de la Route 22.
Copies du primaire General (animations conservees) et du secondaire IndigoPlateau, seulement pour LAYOUT_ROUTE23 et LAYOUT_INDIGO_PLATEAU_EXTERIOR. Idempotent."""
import os, shutil, json, colorsys
P = 'data/tilesets/primary/general/'; S = 'data/tilesets/secondary/indigo_plateau/'
def rp(path):
    L = open(path).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def dawn(c):
    h, l, s = hls(c)
    if c == (255, 0, 255): return c
    if s < .12:                                    # pierre / blanc : leger voile dore
        return rgb(32, min(1, l * 1.02), min(.22, s + .13)) if l > .45 else c
    if 70 <= h <= 170: return rgb(58 + (h - 110) * .12, l * 1.04, s * .72)   # verts -> olive dore
    if 180 <= h <= 250: return rgb(h - 28, l * 1.02, s * .85)               # eau -> turquoise tiede
    return c
def copy_ts(src, dst):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16):
        cols = rp(src + 'palettes/%02d.pal' % i)
        out = [cols[0]] + [dawn(c) for c in cols[1:16]]
        open(dst + 'palettes/%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
def sub(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write('\n' + text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
TM = 'const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n'
NP = 'data/tilesets/primary/general_dawn/'; NS = 'data/tilesets/secondary/indigo_dawn/'
copy_ts(P, NP); copy_ts(S, NS)
for d, name in ((NP, 'GeneralDawn'), (NS, 'IndigoDawn')):
    sub('src/data/tilesets/graphics.h', 'gTilesetTiles_%s[]' % name, 'const u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (name, d, name, pal(d)))
    sub('src/data/tilesets/metatiles.h', 'gMetatiles_%s[]' % name, 'const u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (name, d, name, d))
sub('src/data/tilesets/headers.h', 'gTileset_GeneralDawn =', TM % ('GeneralDawn', 'FALSE', 'GeneralDawn', 'GeneralDawn', 'GeneralDawn', 'GeneralDawn', 'InitTilesetAnim_General'))
sub('src/data/tilesets/headers.h', 'gTileset_IndigoDawn =', TM % ('IndigoDawn', 'TRUE', 'IndigoDawn', 'IndigoDawn', 'IndigoDawn', 'IndigoDawn', 'NULL'))
j = json.load(open('data/layouts/layouts.json'))
for l in j['layouts']:
    if l.get('id') in ('LAYOUT_ROUTE23', 'LAYOUT_INDIGO_PLATEAU_EXTERIOR'):
        l['primary_tileset'] = 'gTileset_GeneralDawn'; l['secondary_tileset'] = 'gTileset_IndigoDawn'
json.dump(j, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('route23 aube ok')
