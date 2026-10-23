"""Bibliotheque de dessin pour la centrale de Chrondrolia (tileset PowerPlant)."""
import struct, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools/topaze/maps'))
ORIG = os.path.join(os.path.dirname(__file__), 'centrale_orig')
def Wk(i): return i | 0x3000      # praticable
def Bl(i): return i | 0x0400      # bloquant
WALK = {710,668,669,671,674,690,705,706,707,716,720,721,758,759,771,772,773,792,667,670}
def T(i): return Wk(i) if i in WALK else Bl(i)
class Cv:
    def __init__(s, w, h, name=None):
        s.w, s.h = w, h; s.g = [Bl(645)] * (w * h)
        s.src = None
        if name:
            d = open(os.path.join(ORIG, name + '.bin'), 'rb').read()
            s.src = (w, struct.unpack('<%dH' % (len(d) // 2), d))
    def set(s, x, y, i):
        if 0 <= x < s.w and 0 <= y < s.h: s.g[y * s.w + x] = T(i) if i < 0x400 else i
    def get(s, x, y): return s.g[y * s.w + x]
    def fill(s, x0, y0, x1, y1, i):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.set(x, y, i)
    def stamp(s, sx, sy, sw, sh, dx, dy):
        w, g = s.src
        for j in range(sh):
            for i in range(sw): s.g[(dy + j) * s.w + dx + i] = g[(sy + j) * w + sx + i]
    def shell(s, doors=()):
        s.fill(1, 3, s.w - 2, s.h - 2, 671)
        for y in range(3, s.h): s.set(0, y, 659); s.set(s.w - 1, y, 663)
        for x in range(s.w): s.set(x, s.h - 1, 683)
        for c in doors: s.door(c)
    def door(s, c):
        h = s.h
        s.fill(c - 2, h - 3, c + 2, h - 3, 716); s.fill(c - 2, h - 2, c + 2, h - 2, 716)
        for k, i in enumerate((705, 706, 707)): s.set(c - 1 + k, h - 2, i)
        s.set(c - 2, h - 1, 682); s.set(c + 2, h - 1, 684)
        for k, i in enumerate((713, 714, 715)): s.set(c - 1 + k, h - 1, i)
    def topwall(s, x0, x1, piles=()):
        n = x1 - x0 + 1
        r1 = [652, 726, 742] + [653] * (n - 6) + [743, 727, 654]
        r2 = [660, 734] + [661] * (n - 4) + [735, 662]
        r3 = [668] + [669] * (n - 2) + [670]
        for k in range(n):
            s.set(x0 + k, 1, r1[k]); s.set(x0 + k, 2, r2[k]); s.set(x0 + k, 3, r3[k])
        for p in piles: s.set(p, 3, 693)
    def turbine(s, x, y): s.stamp_lit(TURB, x, y)
    def stamp_lit(s, rows, x, y):
        for j, r in enumerate(rows):
            for i, v in enumerate(r):
                if v: s.set(x + i, y + j, v)
    def save(s, path):
        open(path, 'wb').write(struct.pack('<%dH' % len(s.g), *s.g))
    def ascii(s):
        return '\n'.join(''.join('#' if (v >> 10) & 3 else '.' for v in s.g[y * s.w:(y + 1) * s.w]) for y in range(s.h))
# motifs (ids ; 0 = rien)
TURB = [[776, 653, 653, 653, 653], [784, 747, 748, 749, 661], [792, 755, 756, 757, 693], [0, 763, 764, 765, 694], [0, 771, 772, 773, 0]]
MACH = [[653, 653, 653], [744, 745, 746], [752, 753, 754], [760, 761, 762]]
BENCH = [[674, 674, 674, 674, 678], [697, 653, 653, 776, 664], [698, 751, 750, 784, 664], [669, 759, 758, 792, 664]]
SIDE = [[653, 658], [661, 666], [690, 669]]
BARREL = [[728], [729]]
