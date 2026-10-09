# FORET CALCINEE (ex Foret de Jade / Viridian Forest) : memes cartes, tilesets recopies avec des palettes de cendre et de charbon.
# Lancer depuis la racine : python3 docs/topaze/forest_cinder.py   (idempotent)
import os, shutil, json, colorsys, re
SRC = [('data/tilesets/primary/general', 'data/tilesets/primary/general_cinder', 'GeneralCinder', 'gTileset_General', False),
       ('data/tilesets/secondary/viridian_forest', 'data/tilesets/secondary/cinder_forest', 'CinderForest', 'gTileset_ViridianForest', True)]
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def char(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if s < 0.08 and (l > 0.9 or l < 0.12): return r, g, b             # blanc / noir : inchanges (texte, contours)
    if 60 <= h <= 180:                                                 # feuillage et herbe -> charbon et cendre
        h = 12; s = min(0.12, s * 0.25); l = l * 0.45
    elif 20 <= h < 60: h = 16 + (h - 40) * 0.15; s = min(0.4, s * 0.55); l = l * 0.55     # sable, troncs -> terre brulee
    elif 180 < h <= 260: h = 10; s = 0.3; l = l * 0.55
    else: h = 10; s = min(0.7, s * 0.8); l = l * 0.65
    r, g, b = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
for src, dst, cname, orig, sec in SRC:
    os.makedirs(dst + '/palettes', exist_ok=True)
    for f in ('tiles.png', 'metatiles.bin', 'metatile_attributes.bin'): shutil.copy(src + '/' + f, dst + '/' + f)
    for i in range(16):
        c = readpal('%s/palettes/%02d.pal' % (src, i)); writepal('%s/palettes/%02d.pal' % (dst, i), [c[0]] + [char(*x) for x in c[1:]] if 0 <= i <= 12 else c)
def add(path, marker, text):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
txt = ''
for src, dst, cname, orig, sec in SRC:
    txt += '\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (cname, dst, cname, pal(dst))
add('src/data/tilesets/graphics.h', 'GeneralCinder', txt)
txt = ''
for src, dst, cname, orig, sec in SRC:
    txt += '\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%s/metatile_attributes.bin");\n' % (cname, dst, cname, dst)
add('src/data/tilesets/metatiles.h', 'GeneralCinder', txt)
txt = ''
for src, dst, cname, orig, sec in SRC:
    txt += '''
const struct Tileset gTileset_%s =
{
    .isCompressed = TRUE,
    .isSecondary = %s,
    .tiles = gTilesetTiles_%s,
    .palettes = gTilesetPalettes_%s,
    .metatiles = gMetatiles_%s,
    .metatileAttributes = gMetatileAttributes_%s,
    .callback = NULL,
};
''' % (cname, 'TRUE' if sec else 'FALSE', cname, cname, cname, cname)
add('src/data/tilesets/headers.h', 'gTileset_GeneralCinder', txt)
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_VIRIDIAN_FOREST': l.update(primary_tileset='gTileset_GeneralCinder', secondary_tileset='gTileset_CinderForest')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
# nom : VIRIDIAN FOREST -> CINDER FOREST
f = 'src/data/region_map/region_map_entry_strings.h'; s = open(f).read(); s = s.replace('_("VIRIDIAN FOREST")', '_("CINDER FOREST")'); open(f, 'w').write(s)
f = 'data/maps/Route2/text.inc'; s = open(f).read(); s = s.replace('VIRIDIAN FOREST\\n"\n    .string "The old wood runs under the cliff.$"', 'CINDER FOREST\\n"\n    .string "Nothing grows there anymore...$"'); open(f, 'w').write(s)
print('foret calcinee ecrite')
# image de presentation de la carte (ecran d'intro) : meme image, palette de cendre (depart toujours de l'original sauvegarde)
from PIL import Image
im = Image.open('docs/topaze/reference/forest_preview_orig.png'); pl = im.getpalette()
new = []
for k in range(0, len(pl), 3):
    r, g, b = pl[k:k + 3]
    if k == 0: new += [r, g, b]; continue
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    rr, gg, bb = colorsys.hls_to_rgb(12 / 360, l * 0.85 if l < 0.9 else l * 0.95, min(0.16, s * 0.3))
    new += [int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5)]
im.putpalette(new); im.save('graphics/map_preview/viridian_forest/tiles.png')
