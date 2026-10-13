#!/usr/bin/env python3
"""Fonderie d'Opanihrum (arene d'Hepha, ex arene de Jadielle, tileset viridian_gym) : sol menthe -> acier sombre, fleches vertes -> braise orange, jaunes -> ambre.
Idempotent par fichier marqueur. Lancer depuis la racine."""
import colorsys, os
D = 'data/tilesets/secondary/viridian_gym/palettes/'
if os.path.exists(D + '.hepha_done'): print('already'); raise SystemExit
def rd(i):
    L = open(D + '%02d.pal' % i).read().split(); return [tuple(int(x) for x in L[3 + 3 * k:6 + 3 * k]) for k in range(16)]
def conv(c, i):
    if c in ((255, 0, 255), (0, 0, 0)): return c
    h, s, v = colorsys.rgb_to_hsv(*[x / 255 for x in c]); h *= 360
    if s > 0.15:
        if 90 <= h <= 200:                       # menthe / vert -> steel (pal 12 sol) ou braise (fleches)
            if i == 12: h, s, v = 214, s * 0.30, v * 0.52
            else: h, s, v = 22 + (h - 140) * 0.1, 0.92, max(v, 0.78)
        elif 45 <= h < 90: h, s, v = 32 + (h - 60) * 0.2, min(1, s * 1.05), v * 0.95   # jaune -> ambre
        elif 10 <= h < 45: h, s, v = 12, min(1, s * 1.1), v * 0.85                      # brun -> cuivre sombre
    elif i == 12: v *= 0.8
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb((h % 360) / 360, s, v))
for i in (7, 8, 12):
    cols = rd(i)
    open(D + '%02d.pal' % i, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % conv(c, i) for c in cols))
open(D + '.hepha_done', 'w').write('x')
print('ok')
