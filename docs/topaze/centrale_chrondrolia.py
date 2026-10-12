#!/usr/bin/env python3
"""Centrale de Chrondrolia (ex-Manoir Pokemon, 1F/2F/3F/B1F) : recoloration.
Murs roses/bruns -> acier bleu-gris, tapis rose -> bleu clair. Palettes d'origine embarquees (idempotent).
Tileset secondaire pokemon_mansion (utilise uniquement par PokemonMansion_*). Cartes inchangees."""
import colorsys
D = 'data/tilesets/secondary/pokemon_mansion/palettes/'
ORIG = {
 7: '949494 52836a 83b49c b4e6cd b40000 ff0000 94949c acacac 000000 000000 000000 000000 52526a 7b7b8b cdcdc5 ffffff',
 8: '949494 a4624a de947b ffbda4 8b5239 acc5e6 d5deee 000000 000000 bda473 000000 ffeebd 52526a 7b7b8b cdcdc5 ffffff',
 12: '949494 a4624a de947b ffbda4 8b5239 bd839c f6cdee 8b7331 9c835a bda473 decd9c ffeebd 52526a 7b7b8b cdcdc5 ffffff',
}
def conv(c, i, k):
    r, g, b = [x / 255 for x in c]
    h, s, v = colorsys.rgb_to_hsv(r, g, b); h *= 360
    if s > 0.15:
        if h < 35 or h > 300:
            if False: h, s, v = 48, min(1, s * 1.3), min(1, v * 1.05)   # (inutilise)
            else: h, s, v = 208, s * 0.38, v * 0.95                                       # murs -> acier
        elif 80 <= h <= 170: h, s, v = 195, s * 0.6, v                                    # vert -> bleu-gris
    r, g, b = colorsys.hsv_to_rgb((h % 360) / 360, s, v)
    return tuple(int(round(x * 255)) for x in (r, g, b))
for i, row in ORIG.items():
    cols = [tuple(int(x[k:k + 2], 16) for k in (0, 2, 4)) for x in row.split()]
    out = [conv(c, i, k) for k, c in enumerate(cols)]
    open(D + '%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
print('ok')
