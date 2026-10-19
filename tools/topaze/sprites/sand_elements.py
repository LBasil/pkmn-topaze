#!/usr/bin/env python3
"""Elements dessines en code pour les Bulbizarre "des sables" (etape 1 : les trois elements seuls).

Sortie : /tmp/sand/elem_<stade>.png (taille reelle, fond transparent) + /tmp/sand/preview_x8.png (agrandi x8 sur fond beige).
Meme palette (PAL) sur les trois stades. Le contour est ajoute automatiquement autour de l'union des pixels dessines.
"""
import os
from PIL import Image

OUT_DIR = '/tmp/sand'
os.makedirs(OUT_DIR, exist_ok=True)

PAL = {
    'out':  (16, 16, 16),        # contour des sprites d'origine
    'gd':   (41, 90, 49),        # cactus : vert fonce
    'gm':   (74, 140, 66),       # cactus : vert moyen
    'gl':   (139, 201, 98),      # cactus : vert clair
    'spine': (255, 244, 205),    # epines
    'pk_d': (205, 74, 115),      # fleur : rose fonce
    'pk':   (246, 131, 164),     # fleur : rose
    'pk_l': (255, 189, 205),     # fleur : rose clair
    'yel':  (255, 214, 74),      # coeur de fleur
    'tq_d': (24, 140, 156),      # eau : turquoise fonce
    'tq':   (65, 205, 213),      # eau : turquoise
    'tq_l': (189, 246, 246),     # eau : reflet
    'gr':   (98, 172, 57),       # herbe
    'gr_l': (164, 222, 90),      # herbe claire
    'tr':   (148, 98, 57),       # tronc de palmier
    'tr_d': (98, 57, 41),        # tronc : ombre
    'sd':   (230, 200, 140),     # bord d'oasis : sable clair
    'sd_d': (181, 140, 90),      # bord d'oasis : terre
}


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = {}                                   # (x, y) -> nom de couleur
    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h: self.p[(x, y)] = c
    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): self.px(x, y, c)
    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0: self.px(x, y, c)
    def line(self, pts, c):
        for (x, y) in pts: self.px(x, y, c)
    def outline(self):
        """un pixel de contour sur chaque case vide voisine (4-connexite) d'un pixel dessine."""
        add = {}
        for (x, y) in self.p:
            for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n not in self.p and 0 <= n[0] < self.w and 0 <= n[1] < self.h: add[n] = 'out'
        self.p.update(add)
    def image(self):
        im = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0))
        for (x, y), c in self.p.items(): im.putpixel((x, y), PAL[c] + (255,))
        return im


def flower(cv, cx, cy, r):
    """fleur ronde : petales roses autour d'un coeur jaune. r = 1 (minuscule) ou 2 (grande)."""
    if r == 1:
        for (dx, dy) in ((0, -1), (1, 0), (0, 1), (-1, 0)): cv.px(cx + dx, cy + dy, 'pk')
        cv.px(cx, cy, 'yel')
    else:
        for (dx, dy) in ((0, -2), (2, 0), (0, 2), (-2, 0), (1, -1), (-1, -1), (1, 1), (-1, 1), (0, -1), (1, 0), (0, 1), (-1, 0)):
            cv.px(cx + dx, cy + dy, 'pk')
        for (dx, dy) in ((0, -2), (-1, -1), (-2, 0)): cv.px(cx + dx, cy + dy, 'pk_l')
        for (dx, dy) in ((0, 2), (1, 1), (2, 0)): cv.px(cx + dx, cy + dy, 'pk_d')
        cv.px(cx, cy, 'yel'); cv.px(cx - 1, cy, 'yel'); cv.px(cx, cy - 1, 'yel')


def shade_cactus(cv, cells, ribs_every=3):
    """ombrage vertical : bord gauche clair, bord droit sombre, cotes sombres, epines creme au sommet des cotes."""
    xs = sorted({x for (x, y) in cells}); x0, x1 = xs[0], xs[-1]
    for (x, y) in cells:
        t = (x - x0) / max(1, (x1 - x0))
        cv.px(x, y, 'gl' if t < 0.22 else ('gm' if t < 0.7 else 'gd'))
    for (x, y) in cells:
        if (x - x0) % ribs_every == 1 and (x, y - 1) in cells and (x, y + 1) in cells:
            if (y % 3) == 0: cv.px(x, y, 'spine')
            else: cv.px(x, y, 'gd' if (x - x0) / max(1, (x1 - x0)) < 0.7 else 'out')


# ---------------------------------------------------------------------------------------- Bulbizarre
def bulbizarre():
    cv = Canvas(18, 17)
    cells = set()
    for y in range(17):
        for x in range(18):
            if ((x - 8.5) / 7.5) ** 2 + ((y - 10) / 6.0) ** 2 <= 1.0: cells.add((x, y))
    for c in cells: cv.px(c[0], c[1], 'gm')
    shade_cactus(cv, cells, 3)
    for (x, y) in ((4, 8), (8, 6), (12, 8), (6, 12), (11, 12), (9, 15)): cv.px(x, y, 'spine')    # quelques epines
    for (x, y) in ((4, 7), (8, 5), (13, 8), (5, 12), (12, 12)): cv.px(x, y, 'spine')
    flower(cv, 9, 3, 1)
    cv.outline()
    return cv.image()


# ---------------------------------------------------------------------------------------- Herbizarre
def herbizarre():
    cv = Canvas(24, 30)
    cells = set()
    def box(x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): cells.add((x, y))
    box(9, 9, 14, 28)                                   # tronc
    for (x, y) in ((9, 9), (14, 9)): cells.discard((x, y))
    box(1, 17, 8, 20); box(1, 11, 4, 17)                # bras gauche (horizontal puis vertical)
    box(15, 13, 22, 16); box(19, 7, 22, 13)             # bras droit
    for (x, y) in ((1, 11), (4, 11), (19, 7), (22, 7)): cells.discard((x, y))
    for c in cells: cv.px(c[0], c[1], 'gm')
    shade_cactus(cv, cells, 3)
    for (x, y) in ((11, 10), (12, 15), (11, 22), (13, 26), (2, 14), (3, 18), (20, 10), (21, 15)): cv.px(x, y, 'spine')
    flower(cv, 11, 5, 2)
    cv.outline()
    return cv.image()


# ---------------------------------------------------------------------------------------- Florizarre
def palm(cv, x, y_base, h, lean):
    """mini palmier : tronc brun legerement courbe + 5 palmes."""
    px = x
    for i in range(h):
        cv.px(px, y_base - i, 'tr' if i % 2 else 'tr_d')
        if lean and i in (h // 3, 2 * h // 3): px += lean
    top = y_base - h
    for (dx, dy, c) in ((0, -1, 'gr_l'), (-1, 0, 'gr'), (1, 0, 'gr'), (-2, 0, 'gr'), (2, 0, 'gr'), (-3, 1, 'gr_l'), (3, 1, 'gr_l'),
                        (-2, 1, 'gr_l'), (2, 1, 'gr_l'), (0, 0, 'gr_l'), (-1, -1, 'gr_l'), (1, -1, 'gr_l')):
        cv.px(px + dx, top + dy, c)

def florizarre():
    cv = Canvas(42, 32)
    # plateau (mamelon de terre) : bord sable clair, dessous plus sombre
    for y in range(18, 31):
        for x in range(42):
            if ((x - 20.5) / 20.5) ** 2 + ((y - 31) / 13.0) ** 2 <= 1.0 and y >= 19: cv.px(x, y, 'sd')
    for y in range(24, 31):
        for x in range(42):
            if (x, y) in cv.p: cv.px(x, y, 'sd_d')
    # surface d'oasis : herbe
    for y in range(19, 25):
        for x in range(42):
            if ((x - 20.5) / 19.0) ** 2 + ((y - 24.0) / 5.5) ** 2 <= 1.0: cv.px(x, y, 'gr')
    # mare turquoise
    for y in range(20, 26):
        for x in range(42):
            if ((x - 17.0) / 8.0) ** 2 + ((y - 23.0) / 3.0) ** 2 <= 1.0: cv.px(x, y, 'tq')
    for x in range(11, 22): cv.px(x, 21, 'tq_d')
    for (x, y) in ((13, 23), (14, 23), (15, 24), (19, 22)): cv.px(x, y, 'tq_l')
    for (x, y) in ((10, 20), (24, 20), (9, 23), (25, 23), (13, 26), (21, 26)): cv.px(x, y, 'gr_l')   # touffes d'herbe
    # palmiers
    palm(cv, 9, 21, 11, 1)
    palm(cv, 25, 21, 9, -1)
    # cactus sur le cote
    cc = set()
    for y in range(11, 24):
        for x in (34, 35, 36): cc.add((x, y))
    for y in range(15, 19): cc |= {(32, y), (33, y)}
    for y in range(13, 17): cc |= {(38, y), (37, y)}
    cc.discard((34, 11)); cc.discard((36, 11))
    for c in cc: cv.px(c[0], c[1], 'gm')
    for (x, y) in cc:
        if x in (32, 34): cv.px(x, y, 'gl')
        if x in (36, 38): cv.px(x, y, 'gd')
    for (x, y) in ((35, 13), (35, 18), (35, 22), (33, 16), (37, 14)): cv.px(x, y, 'spine')
    flower(cv, 35, 9, 1)
    cv.outline()
    return cv.image()


ELEMS = {'bulbizarre': bulbizarre, 'herbizarre': herbizarre, 'florizarre': florizarre}

if __name__ == '__main__':
    ims = {}
    for n, f in ELEMS.items():
        im = f(); im.save('%s/elem_%s.png' % (OUT_DIR, n)); ims[n] = im; print(n, im.size)
    S = 8; pad = 4
    W = sum(i.width for i in ims.values()) + pad * (len(ims) + 1); H = max(i.height for i in ims.values()) + 2 * pad
    sheet = Image.new('RGBA', (W * S, H * S), (206, 184, 140, 255))
    x = pad
    for n, im in ims.items():
        big = im.resize((im.width * S, im.height * S), Image.NEAREST)
        sheet.alpha_composite(big, (x * S, (H - im.height - pad) * S + pad * S // 2)); x += im.width + pad
    sheet.convert('RGB').save(OUT_DIR + '/preview_x8.png'); print(sheet.size)
