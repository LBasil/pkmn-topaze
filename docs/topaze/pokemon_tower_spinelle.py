#!/usr/bin/env python3
"""Tour Spinelle (interieur de la Tour Pokemon) : recoloration Spinellia.
Sol vert -> ardoise bleu-vert, murs/stèles violets -> gris-violet froid, or -> rouge spinelle.
Les palettes d'origine sont embarquees (idempotent). Tileset secondaire pokemon_tower
(utilise uniquement par PokemonTower_1F..7F). Carte et tuiles inchangees."""
import colorsys, os
D = 'data/tilesets/secondary/pokemon_tower/palettes/'
ORIG = {
 7: 'ff00ff 52526a 737373 b4b4a4 eeeef6 527b52 5a835a 6a9c6a 83ac83 b49cde 6a529c 8b73bd d5bdff ff00ff 416a41 ffffff',
 8: 'ff00ff 52526a 737373 b4b4a4 eeeef6 628b62 6a9c6a 83ac83 94bd94 b49cde cd8b20 deac39 f6eea4 ff00ff 527b52 ffffff',
 9: 'ff00ff 52526a 737373 b4b4a4 eeeef6 ff00ff ff00ff ff00ff ff00ff ff00ff ff00ff ac7b20 eebd4a 4acdcd a4ffff ffffff',
 12: 'ff00ff 52526a 836abd 9c7bcd e6e6ff 73737b 6a9c6a ff00ff ff00ff ff00ff ff00ff 6a529c 9c83cd cdacf6 bda4e6 73737b',
}
def conv(c):
    if c == (255, 0, 255): return c
    r, g, b = [x / 255 for x in c]
    h, s, v = colorsys.rgb_to_hsv(r, g, b); h *= 360
    if s > 0.12:
        if 80 <= h <= 170:   h, s, v = 188 + (h - 125) * 0.2, s * 0.75, v * 0.86      # vert -> ardoise
        elif 230 <= h <= 300: h, s, v = 252 + (h - 265) * 0.25, s * 0.5, v * 0.95      # violet -> gris-violet
        elif 25 <= h <= 65:  h, s, v = 350 + (h - 45) * 0.2, min(1, s * 0.9), v * 0.92 # or -> spinelle
    r, g, b = colorsys.hsv_to_rgb((h % 360) / 360, s, v)
    return tuple(int(round(x * 255)) for x in (r, g, b))
for i, row in ORIG.items():
    cols = [tuple(int(x[k:k + 2], 16) for k in (0, 2, 4)) for x in row.split()]
    out = [conv(c) for c in cols]
    open(D + '%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in out))
print('ok')
