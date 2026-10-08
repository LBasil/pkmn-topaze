# Importe les tilesets de Pokemon Emeraude (pret/pokeemerald, clone dans ../pokeemerald) comme nouveaux tilesets FireRed :
#   data/tilesets/primary/general_emerald   (gTileset_GeneralEmerald, sans animation)
#   data/tilesets/secondary/petalburg_emerald (gTileset_PetalburgEmerald)
# Conversions : ids de tuiles/metatuiles du secondaire 512 -> 640, attributs 16 bits -> 32 bits, palette 6 du
# secondaire deplacee dans le primaire (FireRed a 7 palettes primaires, Emeraude 6).
import os, re, shutil, struct
from PIL import Image
EM = '../pokeemerald/data/tilesets/'
FR = 'data/tilesets/'
PRI, SEC = FR + 'primary/general_emerald/', FR + 'secondary/petalburg_emerald/'
for d in (PRI, SEC):
    os.makedirs(d + 'palettes', exist_ok=True)
shutil.copy(EM + 'primary/general/tiles.png', PRI + 'tiles.png')
shutil.copy(EM + 'secondary/petalburg/tiles.png', SEC + 'tiles.png')
for i in range(16):
    shutil.copy(EM + 'primary/general/palettes/%02d.pal' % i, PRI + 'palettes/%02d.pal' % i)
    shutil.copy(EM + 'secondary/petalburg/palettes/%02d.pal' % i, SEC + 'palettes/%02d.pal' % i)
shutil.copy(EM + 'secondary/petalburg/palettes/06.pal', PRI + 'palettes/06.pal')
# comportements connus de FireRed
hdr = open('include/constants/metatile_behaviors.h').read()
OK = {int(m, 16) for m in re.findall(r'#define MB_\w+\s+(0x[0-9A-Fa-f]+)', hdr)}
WATER = {0x10, 0x11, 0x12, 0x15}
def conv_attr(path, sec):
    raw = open(path, 'rb').read(); out = bytearray()
    for i in range(len(raw) // 2):
        v = struct.unpack('<H', raw[i * 2:i * 2 + 2])[0]
        b, layer = v & 0xff, v >> 12
        if b not in OK: b = 0
        a = b | (layer << 29)
        if b == 0x02: a |= 0x1000200
        elif b in WATER: a |= 0x22000400
        elif b == 0x13: a |= 0x2000600
        out += struct.pack('<I', a)
    return out
open(PRI + 'metatile_attributes.bin', 'wb').write(conv_attr(EM + 'primary/general/metatile_attributes.bin', False))
open(SEC + 'metatile_attributes.bin', 'wb').write(conv_attr(EM + 'secondary/petalburg/metatile_attributes.bin', True))
shutil.copy(EM + 'primary/general/metatiles.bin', PRI + 'metatiles.bin')
raw = open(EM + 'secondary/petalburg/metatiles.bin', 'rb').read(); out = bytearray()
for i in range(len(raw) // 2):
    e = struct.unpack('<H', raw[i * 2:i * 2 + 2])[0]
    t = e & 0x3ff
    if t >= 512: e = (e & ~0x3ff) | (t - 512 + 640)
    out += struct.pack('<H', e)
open(SEC + 'metatiles.bin', 'wb').write(out)
# declarations C
def add(path, text):
    s = open(path).read()
    if 'GeneralEmerald' not in s: open(path, 'a').write(text)
pal = lambda d, n: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
add('src/data/tilesets/graphics.h',
 '\nconst u32 gTilesetTiles_GeneralEmerald[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_GeneralEmerald[][16] =\n{\n%s};\n' % (PRI, pal(PRI, 0)) +
 '\nconst u32 gTilesetTiles_PetalburgEmerald[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_PetalburgEmerald[][16] =\n{\n%s};\n' % (SEC, pal(SEC, 0)))
add('src/data/tilesets/metatiles.h',
 '\nconst u16 gMetatiles_GeneralEmerald[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_GeneralEmerald[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (PRI, PRI) +
 'const u16 gMetatiles_PetalburgEmerald[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_PetalburgEmerald[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (SEC, SEC))
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_GeneralEmerald =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralEmerald,
    .palettes = gTilesetPalettes_GeneralEmerald,
    .metatiles = gMetatiles_GeneralEmerald,
    .metatileAttributes = gMetatileAttributes_GeneralEmerald,
    .callback = NULL,
};

const struct Tileset gTileset_PetalburgEmerald =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PetalburgEmerald,
    .palettes = gTilesetPalettes_PetalburgEmerald,
    .metatiles = gMetatiles_PetalburgEmerald,
    .metatileAttributes = gMetatileAttributes_PetalburgEmerald,
    .callback = NULL,
};
''')
print('ok', len(OK), 'comportements FR connus')
