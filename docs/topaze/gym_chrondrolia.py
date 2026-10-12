#!/usr/bin/env python3
"""Arene d'Eddie (Chrondrolia, ex-arene de Cramois'ile) : recoloration electrique.
Murs/tuyaux verts -> jaune topaze, sol brun -> acier bleu-gris, violets -> cyan electrique. Palettes d'origine embarquees (idempotent).
Tileset secondaire cinnabar_gym (utilise uniquement par CinnabarIsland_Gym). Carte inchangee."""
import colorsys
D = 'data/tilesets/secondary/cinnabar_gym/palettes/'
ORIG = {
 7: 'ff00ff 52526a 8b8b94 b49cac cdbdbd e6debd 5a735a 83c573 cdee73 7b524a b46262 ff8b4a eef6ac ffe64a 6a5a52 ff00ff',
 8: 'ff00ff 52526a 8b8b94 cdbdbd f6f6ff 9483b4 cdbde6 7b62ff 52ac94 ff6262 5a735a 83c573 cdee73 ff00ff ff00ff ff00ff',
 12: 'ff00ff 52526a 7b7b7b 6a5a52 947352 ac835a d5ac5a e6b45a a45aac c573cd e694ff ff00ff ff00ff ff00ff ff00ff ff00ff',
}
def conv(c):
    if c == (255, 0, 255): return c
    r, g, b = [x / 255 for x in c]
    h, s, v = colorsys.rgb_to_hsv(r, g, b); h *= 360
    if s > 0.12:
        if 60 <= h <= 170:   h, s, v = 46 + (h - 100) * 0.1, min(1, s * 1.15), min(1, v * 1.02)   # vert -> topaze
        elif 15 <= h < 60:   h, s, v = 212, s * 0.28, v * 0.95                                   # brun -> acier
        elif 230 <= h <= 330: h, s, v = 188 + (h - 280) * 0.1, min(1, s * 1.1), v                # violet -> cyan electrique
    r, g, b = colorsys.hsv_to_rgb((h % 360) / 360, s, v)
    return tuple(int(round(x * 255)) for x in (r, g, b))
for i, row in ORIG.items():
    cols = [tuple(int(x[k:k + 2], 16) for k in (0, 2, 4)) for x in row.split()]
    open(D + '%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % conv(c) for c in cols))
print('ok')
