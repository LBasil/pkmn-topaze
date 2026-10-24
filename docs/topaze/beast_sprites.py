#!/usr/bin/env python3
"""Sprites overworld 32x32 de Raikou / Entei / Suicune : le sprite EXACT du Pokedex (graphics/pokemon/<x>/front.png, 64x64) reduit de moitie,
sans melange de couleurs : on garde la palette d'origine du Pokedex ; pour chaque bloc 2x2 on prend la couleur dominante (le contour sombre l'emporte
des qu'il est present, pour garder les traits). Ecrit le PNG indexe (index 0 = transparent) et la palette .pal."""
import os, sys
from collections import Counter
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
TRANSP = (115, 197, 164)

def lum(pal, c): return sum(pal[c * 3:c * 3 + 3])

def build(name):
    fr = Image.open(R + f'graphics/pokemon/{name}/front.png'); pal = fr.getpalette()
    out = Image.new('P', (32, 32), 0); op = out.load()
    for y in range(32):
        for x in range(32):
            cnt = Counter(c for c in (fr.getpixel((2 * x + i, 2 * y + j)) for i in (0, 1) for j in (0, 1)) if c != 0)
            if sum(cnt.values()) < 2: continue
            dark = min(cnt, key=lambda c: lum(pal, c))
            op[x, y] = dark if lum(pal, dark) < 90 else cnt.most_common(1)[0][0]
    cols = [TRANSP] + [tuple(pal[i * 3:i * 3 + 3]) for i in range(1, 16)]
    out.putpalette([v for c in cols for v in c] + [0] * (768 - 48))
    return out, cols

if __name__ == '__main__':
    for n in sys.argv[1:] or ('raikou', 'entei', 'suicune'):
        img, cols = build(n)
        img.save(R + f'graphics/object_events/pics/pokemon/{n}.png')
        with open(R + f'graphics/object_events/palettes/{n}.pal', 'w') as f:
            f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in cols))
        print(n)
