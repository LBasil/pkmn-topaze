#!/usr/bin/env python3
"""SEAFOAM volcano: GeneralSeafoam = copy of primary General with blue (water) hues -> lava; switches the 7 Seafoam layouts. Idempotent."""
import os, shutil, colorsys, json, re
SRC='data/tilesets/primary/general/'; DST='data/tilesets/primary/general_seafoam/'
shutil.rmtree(DST, ignore_errors=True); os.makedirs(DST+'palettes')
for f in ('metatiles.bin','metatile_attributes.bin','tiles.png'): shutil.copy(SRC+f, DST+f)
def lava(c):
    r,g,b=c; h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
    if s<0.18 or not (0.5<=h<=0.75): return c
    # darker = crust red, lighter = bright orange/yellow
    L=l
    ramp=[(0.0,(70,10,6)),(0.35,(150,30,8)),(0.55,(220,70,10)),(0.75,(255,140,30)),(1.0,(255,230,120))]
    for (a,ca),(bb,cb) in zip(ramp,ramp[1:]):
        if L<=bb:
            t=(L-a)/(bb-a); return tuple(int(round(ca[i]+(cb[i]-ca[i])*t)) for i in range(3))
    return ramp[-1][1]
for i in range(16):
    L=open(SRC+'palettes/%02d.pal'%i).read().split(); n=int(L[2])
    cols=[tuple(int(x) for x in L[3+3*k:6+3*k]) for k in range(n)]
    out=[cols[0]]+[lava(c) for c in cols[1:]]
    open(DST+'palettes/%02d.pal'%i,'w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in out))
def sub(path, anchor, text):
    s=open(path).read()
    if text.split('\n')[0] in s: return
    open(path,'w').write(s+'\n'+text)
pals=''.join('\tINCBIN_U16("data/tilesets/primary/general_seafoam/palettes/%02d.gbapal"),\n'%i for i in range(16))
sub('src/data/tilesets/graphics.h',None,'const u32 gTilesetTiles_GeneralSeafoam[] = INCBIN_U32("data/tilesets/primary/general_seafoam/tiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralSeafoam[][16] =\n{\n'+pals+'};\n')
sub('src/data/tilesets/metatiles.h',None,'const u16 gMetatiles_GeneralSeafoam[] = INCBIN_U16("data/tilesets/primary/general_seafoam/metatiles.bin");\nconst u32 gMetatileAttributes_GeneralSeafoam[] = INCBIN_U32("data/tilesets/primary/general_seafoam/metatile_attributes.bin");\n')
sub('src/data/tilesets/headers.h',None,'const struct Tileset gTileset_GeneralSeafoam =\n{\n    .isCompressed = TRUE,\n    .isSecondary = FALSE,\n    .tiles = gTilesetTiles_GeneralSeafoam,\n    .palettes = gTilesetPalettes_GeneralSeafoam,\n    .metatiles = gMetatiles_GeneralSeafoam,\n    .metatileAttributes = gMetatileAttributes_GeneralSeafoam,\n    .callback = InitTilesetAnim_General,\n};\n')
p='data/layouts/layouts.json'; j=json.load(open(p))
for e in j['layouts']:
    if e.get('id','').startswith('LAYOUT_SEAFOAM_ISLANDS'): e['primary_tileset']='gTileset_GeneralSeafoam'
json.dump(j,open(p,'w'),indent=2); open(p,'a').write('\n')
print('ok')
