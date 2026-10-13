#!/usr/bin/env python3
"""LE REPAIRE d'Onybris : copie du tileset secondaire PokemonLeague recoloree (obsidienne : sol noir-violet, parois cramoisi sombre, emblemes = braise).
Enregistre gTileset_PokemonLeagueLair (secondaire). Idempotent."""
import os, shutil, colorsys
SRC='data/tilesets/secondary/pokemon_league/'; DST='data/tilesets/secondary/pokemon_league_lair/'
shutil.rmtree(DST, ignore_errors=True); os.makedirs(DST+'palettes')
for f in ('metatiles.bin','metatile_attributes.bin','tiles.png'): shutil.copy(SRC+f, DST+f)
def conv(c):
    if c in ((255,0,255),(0,0,0)): return c
    h,s,v=colorsys.rgb_to_hsv(*[x/255 for x in c]); h*=360
    if s>0.2 and 255<=h<=320: h,s,v=22,0.92,max(0.55,v)            # violet / emblem -> braise
    elif s>0.2 and 10<=h<70: h,s,v=352,min(1,s*0.9),v*0.5          # orange/brown -> crimson dark
    elif s>0.2 and (140<=h<255): h,s,v=268,0.45,v*0.33              # teal/blue -> obsidian violet
    elif s>0.2: h,s,v=h,s*0.7,v*0.5
    else: h,s,v=268,0.25,v*0.42                                      # greys/whites -> dark slate violet
    return tuple(int(round(x*255)) for x in colorsys.hsv_to_rgb((h%360)/360,s,v))
for i in range(16):
    L=open(SRC+'palettes/%02d.pal'%i).read().split(); n=int(L[2])
    cols=[tuple(int(x) for x in L[3+3*k:6+3*k]) for k in range(n)]
    out=[cols[0]]+[conv(c) for c in cols[1:]]
    open(DST+'palettes/%02d.pal'%i,'w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in out))
def sub(path,text):
    s=open(path).read()
    if text.split('\n')[0] in s: return
    open(path,'w').write(s+'\n'+text)
pals=''.join('\tINCBIN_U16("data/tilesets/secondary/pokemon_league_lair/palettes/%02d.gbapal"),\n'%i for i in range(16))
sub('src/data/tilesets/graphics.h','const u32 gTilesetTiles_PokemonLeagueLair[] = INCBIN_U32("data/tilesets/secondary/pokemon_league_lair/tiles.4bpp.lz");\nconst u16 gTilesetPalettes_PokemonLeagueLair[][16] =\n{\n'+pals+'};\n')
sub('src/data/tilesets/metatiles.h','const u16 gMetatiles_PokemonLeagueLair[] = INCBIN_U16("data/tilesets/secondary/pokemon_league_lair/metatiles.bin");\nconst u32 gMetatileAttributes_PokemonLeagueLair[] = INCBIN_U32("data/tilesets/secondary/pokemon_league_lair/metatile_attributes.bin");\n')
sub('src/data/tilesets/headers.h','const struct Tileset gTileset_PokemonLeagueLair =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_PokemonLeagueLair,\n    .palettes = gTilesetPalettes_PokemonLeagueLair,\n    .metatiles = gMetatiles_PokemonLeagueLair,\n    .metatileAttributes = gMetatileAttributes_PokemonLeagueLair,\n    .callback = NULL,\n};\n')
print('ok')
