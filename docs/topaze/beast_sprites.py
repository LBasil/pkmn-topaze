#!/usr/bin/env python3
"""Sprites overworld 32x32 de Raikou / Entei / Suicune : le sprite EXACT du Pokedex (graphics/pokemon/<x>/front.png, 64x64) reduit a la taille de Sulfura (~22 px),
sans melange de couleurs : on garde la palette d'origine du Pokedex ; pour chaque bloc 2x2 on prend la couleur dominante (le contour sombre l'emporte
des qu'il est present, pour garder les traits). Ecrit le PNG indexe (index 0 = transparent) et la palette .pal."""
import os, sys
from collections import Counter
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
TRANSP = (115, 197, 164)

def lum(pal, c): return sum(pal[c * 3:c * 3 + 3])

FIT = 22      # meme encombrement que Sulfura (22 x 20 dans le cadre 32x32)

def build(name):
    fr = Image.open(R + f'graphics/pokemon/{name}/front.png'); pal = fr.getpalette()
    bb = fr.convert('RGBA').getbbox(); x0, y0, x1, y1 = bb
    # transparence : indice 0 du Pokedex
    mask = fr.point(lambda v: 0 if v == 0 else 255)
    bb = mask.getbbox(); x0, y0, x1, y1 = bb; w, h = x1 - x0, y1 - y0
    sc = max(w, h) / FIT; nw, nh = max(1, round(w / sc)), max(1, round(h / sc))
    out = Image.new('P', (32, 32), 0); op = out.load()
    ox = (32 - nw) // 2; oy = 31 - nh
    for y in range(nh):
        for x in range(nw):
            sx0, sx1 = x0 + int(x * w / nw), x0 + max(int((x + 1) * w / nw), int(x * w / nw) + 1)
            sy0, sy1 = y0 + int(y * h / nh), y0 + max(int((y + 1) * h / nh), int(y * h / nh) + 1)
            px = [fr.getpixel((i, j)) for i in range(sx0, sx1) for j in range(sy0, sy1)]
            op_ = [c for c in px if c != 0]
            if len(op_) < 0.45 * len(px): continue
            cnt = Counter(op_); dk = [c for c in op_ if lum(pal, c) < 90]
            op[ox + x, oy + y] = Counter(dk).most_common(1)[0][0] if len(dk) >= 0.25 * len(op_) else cnt.most_common(1)[0][0]
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
