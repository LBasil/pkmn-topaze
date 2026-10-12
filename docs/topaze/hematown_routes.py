# ROUTES 5 / 6 / 7 (voisines de Hematown) : habillage v1 (recoloration, une ambiance par route selon la ville a l'autre bout).
#   Route 5 (Tourmalia)  : falaises mauves (palette primaire 1, comme Route 24), verts FireRed conserves.
#   Route 6 (Apatia)     : tilesets d'Apatia (GeneralApatia / VermilionApatia : tint_sunset, memes numeros de metatuiles que Vermilion) ; decor dans hematown_routes_decor.py.
#   Route 7 (Bourg Quartz): tilesets de Bourg Quartz (GeneralCeladopole / CeladonCeladopole : tint_snow) ; decor dans hematown_routes_decor.py.
# Tilesets copies de general / cerulean_city / vermilion_city / celadon_city (memes numeros de metatuiles : les cartes restent valables telles quelles).
# Les connexions vers MAP_SAFFRON_CITY_CONNECTION (bande dessinee avec d'autres tilesets) sont retirees des routes 5/6/7 (on y entre par les portes, des warps).
# Idempotent. Lancer depuis la racine : PYTHONDONTWRITEBYTECODE=1 python3 docs/topaze/hematown_routes.py
import json, os, shutil, colorsys
P = 'data/tilesets/'
def readpal(p):
    L = open(p).read().split(); n = int(L[2]); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(n)]
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
def hls(c): h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255); return h * 360, l, s
def rgb(h, l, s): r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s))); return int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5)
def tint_sunset(c):
    h, l, s = hls(c)
    if s < 0.08: return c
    if 28 <= h < 70 and s > 0.1: return rgb(24, min(0.9, l * 0.9 + 0.08), min(0.75, s * 0.9 + 0.1))
    if 70 <= h <= 175:
        if l > 0.44: return rgb(44, min(0.78, l * 0.95 + 0.04), min(0.62, s * 0.8 + 0.1))
        return rgb(176, l * 0.95, min(0.7, s * 0.9 + 0.08))
    if 180 <= h <= 250: return rgb(h + 14, l * 0.84, min(0.9, s * 0.72))
    return c
def tint_snow(c):
    h, l, s = hls(c)
    if s < 0.08: return c
    if 28 <= h < 70 and s > 0.1: return rgb(208, min(0.96, l * 0.55 + 0.45), 0.28)
    if 70 <= h <= 175:
        if l > 0.5: return rgb(206, min(0.97, 0.80 + (l - 0.5) * 0.35), 0.45)
        if l > 0.34: return rgb(204, 0.62 + (l - 0.34) * 0.9, 0.34)
        return rgb(212, min(0.5, l * 1.35), 0.38)
    if 180 <= h <= 235: return rgb(h - 4, min(0.92, l + 0.1), s * 0.8)
    return c
def mauve(c):
    h, l, s = hls(c)
    if s > 0.12 and (h < 50 or h > 330): return rgb(312, l, min(0.5, s * 0.8))
    return c
ident = lambda c: c
# nom, couche, tileset secondaire d'origine, callback secondaire, teinte primaire par palette, teinte secondaire par palette
CITY = {'LAYOUT_ROUTE6': ('gTileset_GeneralApatia', 'gTileset_VermilionApatia'), 'LAYOUT_ROUTE7': ('gTileset_GeneralCeladopole', 'gTileset_CeladonCeladopole')}
ROUTES = [('Route5', 'LAYOUT_ROUTE5', 'route5', 'cerulean_pepite', 'CeruleanCity', 'Cerulean', 'NULL', {1: mauve}, {}),
          ('Route6', 'LAYOUT_ROUTE6', 'route6', 'vermilion_apatia', 'Vermilion', 'Vermilion', 'NULL', None, {}),
          ('Route7', 'LAYOUT_ROUTE7', None, None, None, None, None, None, None)]
def add(path, marker, text):
    if marker not in open(path).read(): open(path, 'a').write(text)
pal = lambda d: ''.join('\tINCBIN_U16("%spalettes/%02d.gbapal"),\n' % (d, i) for i in range(16))
tm = '''
const struct Tileset gTileset_%s =
{
    .isCompressed = TRUE,
    .isSecondary = %s,
    .tiles = gTilesetTiles_%s,
    .palettes = gTilesetPalettes_%s,
    .metatiles = gMetatiles_%s,
    .metatileAttributes = gMetatileAttributes_%s,
    .callback = %s,
};
'''
Lj = json.load(open('data/layouts/layouts.json'))
def dress(name, lid, key, sdir, sprefix, scb, tp, ts):
    """Route 5 : copie des tilesets FireRed recolores (tilesets dedies)"""
    cn = 'Route' + key[-1]
    NP = P + 'primary/general_%s/' % key; NS = P + 'secondary/%s_%s/' % (sdir.split('_')[0], key)
    pairs = [(P + 'secondary/%s/' % sdir, NS, ts)]
    if tp is not None: pairs.insert(0, (P + 'primary/general/', NP, tp))
    for src, dst, spec in pairs:
        shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst + 'palettes')
        for f in ('metatiles.bin', 'metatile_attributes.bin', 'tiles.png'): shutil.copy(src + f, dst + f)
        for i in range(16):
            pp = readpal(src + 'palettes/%02d.pal' % i)
            out = [pp[0]] + [spec[i](c) for c in pp[1:15]] + [pp[15]] if i in spec else pp
            writepal(dst + 'palettes/%02d.pal' % i, out)
    if sdir == 'cerulean_pepite':     # tuiles de decor de la Route 24 (arbres, cristaux : palettes 7 et 8) ; palettes 9..12 (maison de Bill delabree) remises d'origine
        for i in range(9, 13): shutil.copy(P + 'secondary/cerulean_city/palettes/%02d.pal' % i, NS + 'palettes/%02d.pal' % i)
    G_, S_ = 'General' + cn, sprefix + cn
    if tp is None:     # Route 6 : primaire = celui d'Apatia, seul le secondaire est une copie (murets et escaliers ajoutes par hematown_routes_decor.py)
        add('src/data/tilesets/graphics.h', 'gTilesetTiles_%s[]' % S_,
            '\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (S_, NS, S_, pal(NS)))
        add('src/data/tilesets/metatiles.h', 'gMetatiles_%s[]' % S_,
            '\nconst u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (S_, NS, S_, NS))
        add('src/data/tilesets/headers.h', 'gTileset_%s =' % S_, tm % (S_, 'TRUE', S_, S_, S_, S_, scb))
        return 'gTileset_GeneralApatia', 'gTileset_' + S_
    add('src/data/tilesets/graphics.h', 'gTilesetTiles_%s[]' % G_,
        '\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (G_, NP, G_, pal(NP)) +
        '\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%stiles.4bpp.lz");\nconst u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (S_, NS, S_, pal(NS)))
    add('src/data/tilesets/metatiles.h', 'gMetatiles_%s[]' % G_,
        '\nconst u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (G_, NP, G_, NP) +
        '\nconst u16 gMetatiles_%s[] = INCBIN_U16("%smetatiles.bin");\nconst u32 gMetatileAttributes_%s[] = INCBIN_U32("%smetatile_attributes.bin");\n' % (S_, NS, S_, NS))
    add('src/data/tilesets/headers.h', 'gTileset_%s =' % G_,
        tm % (G_, 'FALSE', G_, G_, G_, G_, 'InitTilesetAnim_General') + tm % (S_, 'TRUE', S_, S_, S_, S_, scb))
    return 'gTileset_' + G_, 'gTileset_' + S_
Lj = json.load(open('data/layouts/layouts.json'))
for name, lid, key, sdir, sname, sprefix, scb, tp, ts in ROUTES:
    pt, st = dress(name, lid, key, sdir, sprefix, scb, tp, ts) if key else CITY[lid]
    for l in Lj['layouts']:
        if l.get('id') == lid: l.update(primary_tileset=pt, secondary_tileset=st)
    f = 'data/maps/%s/map.json' % name; m = json.load(open(f))
    m['connections'] = [c for c in (m.get('connections') or []) if c['map'] != 'MAP_SAFFRON_CITY_CONNECTION'] or None
    json.dump(m, open(f, 'w'), indent=2); open(f, 'a').write('\n')
json.dump(Lj, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
print('routes 5/6/7 habillees')
