#!/usr/bin/env python3
"""Sprites overworld 32x32 de Raikou / Entei / Suicune, derives des vrais sprites de face (graphics/pokemon/<x>/front.png) :
reduction x2 (moyenne par bloc), alpha seuille, quantification a 15 couleurs + index 0 transparent. Palette dediee par bete."""
import os, sys
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
TRANSP = (115, 197, 164)

OUT = (28, 24, 40)        # contour sombre
FIT = 22                  # taille max de la bete dans le cadre de 32x32 (style des oiseaux / Pokemon du ranch : compact, aplats, contour)

def build(name, ncol=9):
    fr = Image.open(R + f'graphics/pokemon/{name}/front.png').convert('RGBA')
    bb = fr.getbbox(); fr = fr.crop(bb)
    w, h = fr.size; sc = FIT / max(w, h); nw, nh = max(1, round(w * sc)), max(1, round(h * sc))
    # reduction par moyenne ponderee par l'alpha
    big = fr.resize((nw * 4, nh * 4), Image.LANCZOS)
    sm = Image.new('RGBA', (nw, nh)); sp = sm.load(); bp = big.load()
    for y in range(nh):
        for x in range(nw):
            blk = [bp[x * 4 + i, y * 4 + j] for i in range(4) for j in range(4)]
            op = [p for p in blk if p[3] > 128]
            if len(op) < 9: continue
            n = len(op); sp[x, y] = (sum(p[0] for p in op) // n, sum(p[1] for p in op) // n, sum(p[2] for p in op) // n, 255)
    px = [sm.getpixel((x, y))[:3] for y in range(nh) for x in range(nw) if sm.getpixel((x, y))[3]]
    strip = Image.new('RGB', (len(px), 1)); strip.putdata(px)
    q = strip.quantize(colors=ncol, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:ncol * 3]; cols = [tuple(pal[i * 3:i * 3 + 3]) for i in range(ncol)]
    def near(c): return min(range(ncol), key=lambda i: sum((a - b) ** 2 for a, b in zip(c, cols[i])))
    # grille d'indices (0 = vide), 1..ncol = couleurs, ncol+1 = contour
    g = [[0] * nw for _ in range(nh)]
    for y in range(nh):
        for x in range(nw):
            p = sm.getpixel((x, y))
            if p[3]: g[y][x] = 1 + near(p[:3])
    # nettoyage : pixel isole -> couleur majoritaire des voisins
    for y in range(nh):
        for x in range(nw):
            if not g[y][x]: continue
            nb = [g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < nw and 0 <= y + dy < nh and g[y + dy][x + dx]]
            if nb and g[y][x] not in nb:
                g[y][x] = max(set(nb), key=nb.count)
    img = Image.new('P', (32, 32), 0); ip = img.load()
    ox = (32 - nw) // 2; oy = 30 - nh          # bas du cadre : pieds pres du bord inferieur
    oy = max(1, oy)
    occ = lambda x, y: 0 <= x < nw and 0 <= y < nh and g[y][x]
    for y in range(-1, nh + 1):
        for x in range(-1, nw + 1):
            X, Y = ox + x, oy + y
            if not (0 <= X < 32 and 0 <= Y < 32): continue
            if occ(x, y): ip[X, Y] = g[y][x]
            elif any(occ(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): ip[X, Y] = ncol + 1
    full = [TRANSP] + cols + [OUT] + [(0, 0, 0)] * (16 - ncol - 2)
    img.putpalette([v for c in full for v in c] + [0] * (768 - 48))
    return img, full

if __name__ == '__main__':
    for n in sys.argv[1:] or ('raikou', 'entei', 'suicune'):
        img, full = build(n)
        img.save(R + f'graphics/object_events/pics/pokemon/{n}.png')
        with open(R + f'graphics/object_events/palettes/{n}.pal', 'w') as f:
            f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in full))
        print(n, img.size)
