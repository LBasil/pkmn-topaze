#!/usr/bin/env python3
"""Arene d'Amethiolite (ex-arene de Parmanie, champion Achlys) : recoloration amethyste.
Sol rose -> lilas d'ametyste, or -> argent-lilas, verts -> violet profond. Palettes d'origine embarquees (idempotent).
Tileset secondaire fuchsia_gym (utilise uniquement par FuchsiaCity_Gym). Carte inchangee."""
import colorsys
D = 'data/tilesets/secondary/fuchsia_gym/palettes/'
ORIG = {
 7: 'ff00ff 52526a 7b7b7b b4b4a4 ffffff 9c8339 d5c56a f6ee94 d5deee dee6ff 296a52 398373 ac8373 c59c94 eeb4a4 b48b7b',
 8: 'ff00ff 52526a 7b7b7b b4b4a4 ffffff 9c8339 d5c56a f6ee94 9ccdf6 73acde ff00ff ff00ff ff00ff ff00ff ff00ff ff00ff',
 12: 'ff00ff 52526a 838383 b4b4a4 ffffff ac8373 c59c94 eeb4a4 ffdec5 ffeeee e6a462 ffc562 cda49c b48b7b ff00ff ff00ff',
}
def conv(c):
    if c == (255, 0, 255): return c
    r, g, b = [x / 255 for x in c]
    h, s, v = colorsys.rgb_to_hsv(r, g, b); h *= 360
    if s > 0.08:
        if h < 60 or h > 330:   h, s, v = 272 + (h if h < 60 else h - 360) * 0.1, s * 0.75, v * 0.97   # rose/or -> lilas
        elif 120 <= h <= 190:   h, s, v = 268, min(1, s * 1.1), v * 0.8                                  # vert -> violet profond
    r, g, b = colorsys.hsv_to_rgb((h % 360) / 360, s, v)
    return tuple(int(round(x * 255)) for x in (r, g, b))
for i, row in ORIG.items():
    cols = [tuple(int(x[k:k + 2], 16) for k in (0, 2, 4)) for x in row.split()]
    open(D + '%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % conv(c) for c in cols))
print('ok')
