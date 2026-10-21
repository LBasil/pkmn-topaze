#!/usr/bin/env python3
"""Retours Basil 21/10 : la Tour Hematek (Silph Co) prend l'ambiance de Hematown (ardoise sombre + braise rouge) et le repaire de Bourg Quartz
(Rocket Hideout) l'ambiance glacee de la ville (acier bleute, glace). Deux copies recolorees du secondaire SilphCo (tuiles/palettes de
'condominiums' + metatuiles de 'silph_co') : gTileset_SilphCoHematek et gTileset_SilphCoQuartz. Idempotent."""
import os, shutil, json, colorsys
SRC = 'data/tilesets/secondary/'
def ramp(stops):
    def f(v):
        v = max(0, min(1, v)) * (len(stops) - 1); i = min(int(v), len(stops) - 2); t = v - i
        return tuple(int(round(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * t)) for k in range(3))
    return f
def hsv(c): return colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
def lum(c): return (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255
SLATE = ramp([(14, 12, 26), (36, 40, 62), (70, 74, 100), (112, 116, 142), (168, 176, 198), (226, 232, 242)])
EMBER = ramp([(34, 8, 14), (76, 16, 26), (122, 28, 38), (176, 54, 52), (232, 120, 84)])
ICE = ramp([(26, 44, 70), (60, 96, 130), (110, 156, 190), (168, 208, 232), (222, 240, 250), (250, 254, 255)])
DEEP = ramp([(18, 30, 58), (44, 70, 112), (80, 118, 168), (130, 172, 214)])
def hematek(c):
    h, s, v = hsv(c); h *= 360
    if c == (255, 0, 255) or v < 0.05: return c
    if s > 0.35 and (h >= 330 or h <= 25): return EMBER(lum(c) * 0.95)      # rouges/oranges -> braise
    if s > 0.2 and 70 <= h <= 190: return EMBER(lum(c) * 0.9)               # verts -> braise sombre (moquette)
    return SLATE(lum(c) * 0.88)                                            # le reste (gris, bleus, blancs) -> ardoise
def quartz(c):
    h, s, v = hsv(c); h *= 360
    if c == (255, 0, 255) or v < 0.05: return c
    if s > 0.35 and (h >= 330 or h <= 25): return DEEP(lum(c) * 1.2)       # rouges -> bleu profond
    if s > 0.2 and 70 <= h <= 190: return DEEP(lum(c) * 1.1)
    return ICE(lum(c) * 1.02)
def rp(path):
    L = open(path).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
def make(name, const, fn, anim=True):
    d = SRC + name + '/'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d + 'palettes')
    for f in ('tiles.png',): shutil.copy(SRC + 'condominiums/' + f, d + f)
    for f in ('metatiles.bin', 'metatile_attributes.bin'): shutil.copy(SRC + 'silph_co/' + f, d + f)
    for i in range(16):
        cols = rp(SRC + 'condominiums/palettes/%02d.pal' % i)
        out = [cols[0]] + [fn(c) for c in cols[1:]]
        open(d + 'palettes/%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
    pals = ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
    def sub(path, text):
        s = open(path).read()
        if text.split('\n')[0] in s: return
        open(path, 'w').write(s + '\n' + text)
    sub('src/data/tilesets/graphics.h', 'const u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (const, d, const, pals))
    sub('src/data/tilesets/metatiles.h', 'const u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (const, d, const, d))
    sub('src/data/tilesets/headers.h', 'const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = InitTilesetAnim_SilphCo,\n};\n' % ((const,) * 5))
make('silph_co_hematek', 'SilphCoHematek', hematek)
make('silph_co_quartz', 'SilphCoQuartz', quartz)
f = 'data/layouts/layouts.json'; j = json.load(open(f))
for l in j['layouts']:
    i = l.get('id', '')
    if i.startswith('LAYOUT_SILPH_CO_') and l['secondary_tileset'] in ('gTileset_SilphCo', 'gTileset_SilphCoHematek') and i != 'LAYOUT_SILPH_CO_ELEVATOR' or i == 'LAYOUT_SILPH_CO_ELEVATOR':
        l['secondary_tileset'] = 'gTileset_SilphCoHematek'
    if i.startswith('LAYOUT_ROCKET_HIDEOUT_'): l['secondary_tileset'] = 'gTileset_SilphCoQuartz'
json.dump(j, open(f, 'w'), indent=2); open(f, 'a').write('\n')
print('ok')
