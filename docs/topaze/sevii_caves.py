#!/usr/bin/env python3
"""Sevii : les grottes / forets suivent l'ambiance de leur ile (voir sevii_dress.py, a lancer avant). Clones teintes des secondaires vanilla
(Cave, NavelRock, RockTunnel, ViridianForest, BerryForest, DiglettsCave) ; layouts des cartes de l'ile redirigees. Idempotent."""
import os, json, shutil
src = open('docs/topaze/sevii_dress.py').read().split("j = json.load(open('data/layouts/layouts.json'))")[0]
exec(src)
def shift(hue, sm, lm, gray_s=0.07):
    def f(c):
        if c == (255, 0, 255): return c
        h, l, s = hls(c)
        if s < .10: return rgb(hue, l * lm, min(gray_s, .12) if 0.08 < l < 0.92 else 0)
        return rgb(hue + (h % 40) * 0.1, l * lm, min(1, s * sm))
    return f
# cn, secondaire source (dossier), teinte, primaire themed, prefixes de cartes
JOBS = [
 ('CaveSteel', 'cave', shift(212, .45, .92, .10), 'gTileset_GeneralEcho5', ('FiveIsland_LostCave',)),
 ('CaveTide', 'cave', shift(190, .8, 1.02, .08), 'gTileset_GeneralEcho3', ('ThreeIsland_DunsparceTunnel',)),
 ('NavelStone', 'navel_rock', shift(16, .85, .93, .08), 'gTileset_GeneralEcho6', ('SixIsland_DottedHole',)),
 ('RockStone', 'rock_tunnel', shift(16, .85, .93, .08), 'gTileset_GeneralEcho6', ('SixIsland_AlteringCave',)),
 ('ForestStone', 'viridian_forest', shift(52, .55, .96, .06), 'gTileset_GeneralEcho6', ('SixIsland_PatternBush',)),
 ('ForestTide', 'berry_forest', shift(168, .9, 1.0, .06), 'gTileset_GeneralEcho3', ('ThreeIsland_BerryForest',)),
 ('DigTropic', 'digletts_cave', shift(158, .7, 1.0, .06), 'gTileset_GeneralEcho67', ('SevenIsland_SevaultCanyon_TanobyKey',)),
]
j = json.load(open('data/layouts/layouts.json'))
maps = {}
for d in [x for x in os.listdir('data/maps') if os.path.exists('data/maps/%s/map.json' % x)]:
    mj = json.load(open('data/maps/%s/map.json' % d)); maps[d] = mj['layout']
for cn, sdir, fn, prim, prefixes in JOBS:
    NS = S + 'sevii_%s/' % cn.lower(); copy_ts(S + sdir + '/', NS, fn)
    name = 'Sevii' + cn
    sub('src/data/tilesets/graphics.h', 'gTilesetTiles_%s[]' % name, 'const u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (name, NS, name, pal(NS)))
    sub('src/data/tilesets/metatiles.h', 'gMetatiles_%s[]' % name, 'const u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (name, NS, name, NS))
    sub('src/data/tilesets/headers.h', 'gTileset_%s =' % name, TM % (name, 'TRUE', name, name, name, name, 'NULL'))
    lids = {maps[m] for m in maps if m.startswith(prefixes)}
    for l in j['layouts']:
        if l.get('id') in lids:
            l['primary_tileset'] = prim; l['secondary_tileset'] = 'gTileset_' + name
json.dump(j, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('grottes habillees')
