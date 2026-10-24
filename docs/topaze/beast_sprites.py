#!/usr/bin/env python3
"""Sprites overworld 32x32 de Raikou / Entei / Suicune, derives des vrais sprites de face (graphics/pokemon/<x>/front.png) :
reduction x2 (moyenne par bloc), alpha seuille, quantification a 15 couleurs + index 0 transparent. Palette dediee par bete."""
import os, sys
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
TRANSP = (115, 197, 164)

def build(name):
    fr = Image.open(R + f'graphics/pokemon/{name}/front.png').convert('RGBA')
    fp = fr.load(); W, H = fr.size
    out = Image.new('RGBA', (W // 2, H // 2)); op = out.load()
    for y in range(H // 2):
        for x in range(W // 2):
            blk = [fp[2 * x + i, 2 * y + j] for i in (0, 1) for j in (0, 1)]
            op_ = [p for p in blk if p[3] > 0]
            if len(op_) < 2: continue            # moins de la moitie opaque : transparent
            n = len(op_); op[x, y] = (sum(p[0] for p in op_) // n, sum(p[1] for p in op_) // n, sum(p[2] for p in op_) // n, 255)
    px = [out.getpixel((x, y))[:3] for y in range(out.size[1]) for x in range(out.size[0]) if out.getpixel((x, y))[3]]
    strip = Image.new('RGB', (len(px), 1)); strip.putdata(px)
    q = strip.quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:45]; cols = [tuple(pal[i * 3:i * 3 + 3]) for i in range(15)]
    def near(c): return min(range(15), key=lambda i: sum((a - b) ** 2 for a, b in zip(c, cols[i])))
    img = Image.new('P', out.size, 0)
    ip = img.load()
    for y in range(out.size[1]):
        for x in range(out.size[0]):
            p = out.getpixel((x, y))
            if p[3]: ip[x, y] = 1 + near(p[:3])
    full = [TRANSP] + cols
    img.putpalette([v for c in full for v in c] + [0] * (768 - 48))
    return img, full

if __name__ == '__main__':
    for n in sys.argv[1:] or ('raikou', 'entei', 'suicune'):
        img, full = build(n)
        img.save(R + f'graphics/object_events/pics/pokemon/{n}.png')
        with open(R + f'graphics/object_events/palettes/{n}.pal', 'w') as f:
            f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in full))
        print(n, img.size)
