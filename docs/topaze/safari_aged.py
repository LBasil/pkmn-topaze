#!/usr/bin/env python3
"""Retours Basil 21/10 : « il faut que le parc Safari prenne 10 ans visuellement ». Copies recolorees (herbe seche, vegetation sombre, eaux ternes)
du primaire General et du secondaire FuchsiaCity pour les 4 zones du Safari : gTileset_GeneralSafari + gTileset_FuchsiaSafari. Idempotent."""
import os, shutil, json, colorsys
P, S = 'data/tilesets/primary/', 'data/tilesets/secondary/'
def hsv(c): return colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
def aged(c):
    if c == (255, 0, 255): return c
    h, s, v = hsv(c); h *= 360
    if s < 0.1: s2, h2, v2 = 0.10, 50, v * 0.95
    elif 65 <= h <= 175: h2, s2, v2 = 52 + (h - 120) * 0.12, s * 0.5, v * 0.9      # verts -> olive / herbe seche
    elif 175 < h <= 265: h2, s2, v2 = 195, s * 0.45, v * 0.88                      # eaux -> ternes
    else: h2, s2, v2 = h, s * 0.6, v * 0.94
    r = colorsys.hsv_to_rgb((h2 % 360) / 360, min(1, s2), min(1, v2))
    return tuple(int(round(x * 255)) // 8 * 8 + (7 if x > 0.97 else 0) for x in r)
def rp(path):
    L = open(path).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
def sub(path, text):
    s = open(path).read()
    if text.split('\n')[0] in s: return
    open(path, 'w').write(s + '\n' + text)
def make(src, dst, const, secondary, cb):
    base = S if secondary else P
    sd, d = base + src + '/', base + dst + '/'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d + 'palettes')
    for f in ('tiles.png', 'metatiles.bin', 'metatile_attributes.bin'): shutil.copy(sd + f, d + f)
    for i in range(16):
        cols = rp(sd + 'palettes/%02d.pal' % i)
        out = [cols[0]] + [aged(c) for c in cols[1:]]
        open(d + 'palettes/%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
    pals = ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
    sub('src/data/tilesets/graphics.h', 'const u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (const, d, const, pals))
    sub('src/data/tilesets/metatiles.h', 'const u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (const, d, const, d))
    sub('src/data/tilesets/headers.h', 'const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n' % (const, 'TRUE' if secondary else 'FALSE', const, const, const, const, cb))
make('general', 'general_safari', 'GeneralSafari', False, 'InitTilesetAnim_General')
make('fuchsia_city', 'fuchsia_safari', 'FuchsiaSafari', True, 'NULL')
f = 'data/layouts/layouts.json'; j = json.load(open(f))
for l in j['layouts']:
    if l.get('id') in ('LAYOUT_SAFARI_ZONE_CENTER', 'LAYOUT_SAFARI_ZONE_EAST', 'LAYOUT_SAFARI_ZONE_NORTH', 'LAYOUT_SAFARI_ZONE_WEST'):
        l['primary_tileset'] = 'gTileset_GeneralSafari'; l['secondary_tileset'] = 'gTileset_FuchsiaSafari'
json.dump(j, open(f, 'w'), indent=2); open(f, 'a').write('\n')
print('ok')
