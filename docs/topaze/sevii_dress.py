#!/usr/bin/env python3
"""Îles Sevii (post-game) : chaque groupe d'îles prend l'ambiance d'un Écho du Temps (22/10).
 123 = Écho de braise (îles volcaniques : herbe ocre-dorée, sable cendre, eau inchangée)
 45  = Écho d'automne (Johto : feuillages roux, eau violet-indigo)
 67  = Écho tropical (Hoenn : émeraude profond, sable corail, eau turquoise)
Copies du primaire General (animations conservées) + du secondaire SeviiIslandsXX ; layouts redirigés. Idempotent."""
import os, shutil, json, colorsys
P = 'data/tilesets/primary/general/'; S = 'data/tilesets/secondary/'
def rp(path):
    L = open(path).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * i:6 + 3 * i]) for i in range(n)]
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def ember(c):
    h, l, s = hls(c)
    if c == (255, 0, 255) or s < .1: return c
    if 70 <= h <= 170: return rgb(44 + (h - 110) * .12, l * .98, s * .72)     # verts -> ocre doré
    if 28 <= h < 70 and s > .2: return rgb(26, l * .9, s * .35)                  # sable -> cendre chaude
    return c
def autumn(c):
    h, l, s = hls(c)
    if c == (255, 0, 255) or s < .1: return c
    if 70 <= h <= 170: return rgb(18 + (h - 110) * .25, l * .95, min(1, s * 1.05))   # verts -> roux/orange
    if 180 <= h <= 250: return rgb(h + 30, l * .9, s * .95)                           # eau -> indigo
    return c
def tropic(c):
    h, l, s = hls(c)
    if c == (255, 0, 255) or s < .1: return c
    if 70 <= h <= 170: return rgb(152 + (h - 110) * .2, l * .78, min(1, s * 1.45))  # verts -> émeraude
    if 28 <= h < 70 and s > .2: return rgb(14, min(1, l * 1.03), s * .85)             # sable -> corail clair
    if 180 <= h <= 250: return rgb(180 + (h - 215) * .3, l * 1.02, min(1, s * 1.05))  # eau -> turquoise
    return c
GROUPS = {'123': ('Echo123', ember), '45': ('Echo45', autumn), '67': ('Echo67', tropic)}
def copy_ts(src, dst, fn):
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
    for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
    for i in range(16):
        cols = rp(src + 'palettes/%02d.pal' % i)
        out = [cols[0]] + [fn(c) for c in cols[1:16]]
        open(dst + 'palettes/%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
def sub(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write('\n' + text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
TM = 'const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n'
j = json.load(open('data/layouts/layouts.json'))
for g, (cn, fn) in GROUPS.items():
    sec_src = S + 'sevii_islands_%s/' % g
    NP = 'data/tilesets/primary/general_%s/' % cn.lower(); NS = S + 'sevii_%s/' % cn.lower()
    copy_ts(P, NP, fn); copy_ts(sec_src, NS, fn)
    for d, name in ((NP, 'General' + cn), (NS, 'Sevii' + cn)):
        sub('src/data/tilesets/graphics.h', 'gTilesetTiles_%s[]' % name, 'const u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (name, d, name, pal(d)))
        sub('src/data/tilesets/metatiles.h', 'gMetatiles_%s[]' % name, 'const u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (name, d, name, d))
    sub('src/data/tilesets/headers.h', 'gTileset_General%s =' % cn, TM % ('General' + cn, 'FALSE', 'General' + cn, 'General' + cn, 'General' + cn, 'General' + cn, 'InitTilesetAnim_General'))
    sub('src/data/tilesets/headers.h', 'gTileset_Sevii%s =' % cn, TM % ('Sevii' + cn, 'TRUE', 'Sevii' + cn, 'Sevii' + cn, 'Sevii' + cn, 'Sevii' + cn, 'NULL'))
    for l in j['layouts']:
        if l.get('secondary_tileset') in ('gTileset_SeviiIslands' + g, 'gTileset_Sevii' + cn):
            l['primary_tileset'] = 'gTileset_General' + cn; l['secondary_tileset'] = 'gTileset_Sevii' + cn
json.dump(j, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('sevii habillees')
