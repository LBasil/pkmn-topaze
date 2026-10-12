# TOURMALIA : interieur de l'arene = creux de l'ARBRE GEANT. Meme carte que l'arene de Azuria, mais un tileset secondaire copie
# (cerulean_gym_tree) dont les PALETTES sont recolorees : murs -> ecorce, sol/estrade -> bois, bassin -> seve verte lumineuse.
# 0 tuile en plus. Les quelques metatuiles du tileset primaire (Building) utilisees par la carte sont copiees dans le secondaire
# avec des palettes libres (8..11) pour pouvoir etre recolorees sans toucher aux autres interieurs.
# Lancer depuis la racine :  python3 docs/topaze/tourmalia_gym_tree.py   (idempotent ; puis supprimer build/firered/data/maps.o ; make)
import struct, json, os, shutil, colorsys
SRC = 'data/tilesets/secondary/cerulean_gym/'; DST = 'data/tilesets/secondary/cerulean_gym_tree/'; PRIM = 'data/tilesets/primary/building/'
LAY = 'data/layouts/CeruleanCity_Gym/'
os.makedirs(DST + 'palettes', exist_ok=True)
for f in ('tiles.png',): shutil.copy(SRC + f, DST + f)
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def tr(c):
    r, g, b = c
    if (r, g, b) == (255, 0, 255): return c
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); h *= 360
    if 175 <= h <= 265 and s > 0.28: h = 150 + 25 * (1 - l); s = min(0.6, s * 0.8 + 0.1); l = min(0.36, 0.08 + l * 0.30)     # eau -> seve verte lumineuse
    elif s > 0.55 and (h < 25 or h > 330): pass                                                                              # rouges (statues) gardes
    else: h = 24 + 8 * l; s = 0.25 + 0.15 * (1 - abs(l - 0.5)); l = 0.06 + 0.34 * l ** 1.2                                  # pierre/creme -> bois et ecorce
    rr, gg, bb = colorsys.hls_to_rgb(h / 360, max(0, min(1, l)), max(0, min(1, s)))
    return int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5)
mt = [list(struct.unpack('<8H', open(SRC + 'metatiles.bin', 'rb').read()[i * 16:i * 16 + 16])) for i in range(len(open(SRC + 'metatiles.bin', 'rb').read()) // 16)]
at = list(struct.unpack('<%dI' % (len(open(SRC + 'metatile_attributes.bin', 'rb').read()) // 4), open(SRC + 'metatile_attributes.bin', 'rb').read()))
pm = open(PRIM + 'metatiles.bin', 'rb').read(); pa = open(PRIM + 'metatile_attributes.bin', 'rb').read()
cells = list(struct.unpack('<%dH' % (len(open(LAY + 'map.bin', 'rb').read()) // 2), open(LAY + 'map.bin', 'rb').read()))
PRI_USED = sorted({c & 0x3ff for c in cells if (c & 0x3ff) < 640})
SEC0 = 640
# palettes : primaires utilisees par les metatuiles copiees
pal_used = set()
for m in PRI_USED: pal_used |= {q >> 12 for q in struct.unpack('<8H', pm[m * 16:m * 16 + 16])}
free = [p for p in (8, 9, 10, 11) if all(q >> 12 != p for e in mt for q in e)]
pmap = {p: free[k] for k, p in enumerate(sorted(x for x in pal_used if x < 7))}
assert len(pmap) <= len(free), (pmap, free)
PRI_PAL = {p: readpal(PRIM + 'palettes/%02d.pal' % p) for p in range(7)}
SEC_PAL = [readpal(SRC + 'palettes/%02d.pal' % p) for p in range(13)]
OUT = [[(c if k == 0 else tr(c)) for k, c in enumerate(SEC_PAL[p])] for p in range(13)]
for p, slot in pmap.items(): OUT[slot] = [(c if k == 0 else tr(c)) for k, c in enumerate(PRI_PAL[p])]
for i in range(16):
    writepal(DST + 'palettes/%02d.pal' % i, OUT[i] if i < 13 else [(0, 0, 0)] * 16)
newmt = list(mt); newat = list(at); NEWID = {}
for m in PRI_USED:
    e = list(struct.unpack('<8H', pm[m * 16:m * 16 + 16])); e = [(q & 0xfff) | (pmap.get(q >> 12, q >> 12) << 12) for q in e]
    newmt.append(e); newat.append(struct.unpack('<I', pa[m * 4:m * 4 + 4])[0]); NEWID[m] = SEC0 + len(newmt) - 1
assert len(newmt) <= 384
open(DST + 'metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *e) for e in newmt))
open(DST + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in newat))
cells = [((c & ~0x3ff) | NEWID[c & 0x3ff]) if (c & 0x3ff) in NEWID else c for c in cells]
open(LAY + 'map.bin', 'wb').write(struct.pack('<%dH' % len(cells), *cells))
print('interieur de l arbre : metatuiles primaires copiees', len(PRI_USED), ', palettes remappees', pmap)
def add(path, text, key):
    s = open(path).read()
    if key not in s: open(path, 'a').write(text)
pal = ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (DST, i) for i in range(16))
add('src/data/tilesets/graphics.h', '\nconst u32 gTilesetTiles_CeruleanGymTree[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_CeruleanGymTree[][16] =\n{\n%s};\n' % (DST, pal), 'CeruleanGymTree')
add('src/data/tilesets/metatiles.h', '\nconst u16 gMetatiles_CeruleanGymTree[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_CeruleanGymTree[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (DST, DST), 'CeruleanGymTree')
add('src/data/tilesets/headers.h', '''
const struct Tileset gTileset_CeruleanGymTree =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CeruleanGymTree,
    .palettes = gTilesetPalettes_CeruleanGymTree,
    .metatiles = gMetatiles_CeruleanGymTree,
    .metatileAttributes = gMetatileAttributes_CeruleanGymTree,
    .callback = NULL,
};
''', 'CeruleanGymTree')
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_CERULEAN_CITY_GYM': l['secondary_tileset'] = 'gTileset_CeruleanGymTree'
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
