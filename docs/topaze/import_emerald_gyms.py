#!/usr/bin/env python3
"""Importe les decors d'arenes d'Emeraude (../pokeemerald) : un couple (primaire, secondaire) FireRed par arene.
Reprend les conversions de import_emerald_tiles.py (secondaire 512 -> 640, attributs 16 -> 32 bits, palette 6 -> primaire).
Idempotent. Ecrit : data/tilesets/{primary,secondary}/gym_<x>_{pri,sec}, declarations C, et data/layouts/Gym<X>Em/map.bin converti."""
import os, re, shutil, struct, json
EM = '../pokeemerald/data/'
FR = 'data/tilesets/'
GYMS = {  # cle: (secondaire Emeraude, carte Emeraude, id layout Emeraude)
 'lavaridge': ('lavaridge_gym', 'LavaridgeTown_Gym_1F'), 'fortree': ('fortree_gym', 'FortreeCity_Gym'),
 'sootopolis': ('sootopolis_gym', 'SootopolisCity_Gym_1F'), 'dewford': ('dewford_gym', 'DewfordTown_Gym'),
 'mossdeep': ('mossdeep_gym', 'MossdeepCity_Gym'), 'mauville': ('mauville_gym', 'MauvilleCity_Gym'),
 'rustboro': ('rustboro_gym', 'RustboroCity_Gym'),
}
hdr = open('include/constants/metatile_behaviors.h').read()
OK = {int(m, 16) for m in re.findall(r'#define MB_\w+\s+(0x[0-9A-Fa-f]+)', hdr)}
WATER = {0x10, 0x11, 0x12, 0x15}
def conv_attr(path):
    raw = open(path, 'rb').read(); out = bytearray()
    for i in range(len(raw) // 2):
        v = struct.unpack('<H', raw[i * 2:i * 2 + 2])[0]
        b, layer = v & 0xff, v >> 12
        if b not in OK: b = 0
        if 0x44 <= b <= 0x47: b = 0   # Emerald: pas une glissade (en FireRed 0x44-0x47 = SLIDE_*, bloque la passerelle de Sootopolis)
        a = b | (layer << 29)
        if b == 0x02: a |= 0x1000200
        elif b in WATER: a |= 0x22000400
        out += struct.pack('<I', a)
    return out
def cam(k): return k.capitalize()
def add(path, text, marker):
    s = open(path).read()
    if marker not in s: open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
for key, (sec, emmap) in GYMS.items():
    PRI, SEC = FR + 'primary/gym_%s_pri/' % key, FR + 'secondary/gym_%s_sec/' % key
    for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
    shutil.copy(EM + 'tilesets/primary/building/tiles.png', PRI + 'tiles.png')
    shutil.copy(EM + 'tilesets/secondary/%s/tiles.png' % sec, SEC + 'tiles.png')
    for i in range(16):
        shutil.copy(EM + 'tilesets/primary/building/palettes/%02d.pal' % i, PRI + 'palettes/%02d.pal' % i)
        shutil.copy(EM + 'tilesets/secondary/%s/palettes/%02d.pal' % (sec, i), SEC + 'palettes/%02d.pal' % i)
    shutil.copy(EM + 'tilesets/secondary/%s/palettes/06.pal' % sec, PRI + 'palettes/06.pal')
    open(PRI + 'metatile_attributes.bin', 'wb').write(conv_attr(EM + 'tilesets/primary/building/metatile_attributes.bin'))
    open(SEC + 'metatile_attributes.bin', 'wb').write(conv_attr(EM + 'tilesets/secondary/%s/metatile_attributes.bin' % sec))
    shutil.copy(EM + 'tilesets/primary/building/metatiles.bin', PRI + 'metatiles.bin')
    raw = open(EM + 'tilesets/secondary/%s/metatiles.bin' % sec, 'rb').read(); out = bytearray()
    for i in range(len(raw) // 2):
        e = struct.unpack('<H', raw[i * 2:i * 2 + 2])[0]
        t = e & 0x3ff
        if t >= 512: e = (e & ~0x3ff) | (t - 512 + 640)
        out += struct.pack('<H', e)
    open(SEC + 'metatiles.bin', 'wb').write(out)
    # carte Emeraude convertie (ids >= 512 -> +128)
    mb = open(EM + 'layouts/%s/map.bin' % emmap, 'rb').read(); o = bytearray()
    for i in range(len(mb) // 2):
        v = struct.unpack('<H', mb[i * 2:i * 2 + 2])[0]
        mid = v & 0x3ff
        if mid >= 512: v = (v & ~0x3ff) | (mid - 512 + 640)
        o += struct.pack('<H', v)
    os.makedirs('docs/topaze/gym_src', exist_ok=True)
    open('docs/topaze/gym_src/%s.bin' % key, 'wb').write(o)
    N = cam(key)
    add('src/data/tilesets/graphics.h',
        '\nconst u32 gTilesetTiles_Gym%sPri[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Gym%sPri[][16] =\n{\n%s};\n' % (N, PRI, N, pal(PRI)) +
        '\nconst u32 gTilesetTiles_Gym%sSec[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_Gym%sSec[][16] =\n{\n%s};\n' % (N, SEC, N, pal(SEC)), 'gTilesetTiles_Gym%sPri' % N)
    add('src/data/tilesets/metatiles.h',
        '\nconst u16 gMetatiles_Gym%sPri[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Gym%sPri[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (N, PRI, N, PRI) +
        'const u16 gMetatiles_Gym%sSec[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_Gym%sSec[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (N, SEC, N, SEC), 'gMetatiles_Gym%sPri' % N)
    tpl = '''
const struct Tileset gTileset_Gym%(N)s%(S)s =
{
    .isCompressed = TRUE,
    .isSecondary = %(sec)s,
    .tiles = gTilesetTiles_Gym%(N)s%(S)s,
    .palettes = gTilesetPalettes_Gym%(N)s%(S)s,
    .metatiles = gMetatiles_Gym%(N)s%(S)s,
    .metatileAttributes = gMetatileAttributes_Gym%(N)s%(S)s,
    .callback = NULL,
};
'''
    add('src/data/tilesets/headers.h', tpl % dict(N=N, S='Pri', sec='FALSE') + tpl % dict(N=N, S='Sec', sec='TRUE'), 'gTileset_Gym%sPri' % N)
    print(key, len(o) // 2, 'cases')

# --- enregistrement des layouts (map.bin copie seulement s'il n'existe pas : les retouches ulterieures sont conservees)
DIMS = {'lavaridge': (17, 19), 'fortree': (20, 25), 'sootopolis': (17, 26), 'dewford': (18, 28), 'mossdeep': (26, 36), 'mauville': (10, 21), 'rustboro': (11, 20)}
J = json.load(open('data/layouts/layouts.json'))
have = {l.get('id') for l in J['layouts']}
for key, (w, h) in DIMS.items():
    lid = 'LAYOUT_GYM_EM_%s' % key.upper()
    D = 'data/layouts/GymEm%s/' % cam(key); os.makedirs(D, exist_ok=True)
    if not os.path.exists(D + 'map.bin'): shutil.copy('docs/topaze/gym_src/%s.bin' % key, D + 'map.bin')
    open(D + 'border.bin', 'wb').write(struct.pack('<4H', 1, 1, 1, 1))
    if lid in have: continue
    J['layouts'].append({'id': lid, 'name': 'GymEm%s_Layout' % cam(key), 'width': w, 'height': h, 'border_width': 2, 'border_height': 2,
        'primary_tileset': 'gTileset_Gym%sPri' % cam(key), 'secondary_tileset': 'gTileset_Gym%sSec' % cam(key),
        'border_filepath': D + 'border.bin', 'blockdata_filepath': D + 'map.bin'})
open('data/layouts/layouts.json', 'w').write(json.dumps(J, indent=2) + '\n')
