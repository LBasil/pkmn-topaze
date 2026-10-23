"""Bibliotheque de dessin du repaire de Bourg Quartz (tileset SilphCoQuartz). Les ids sont ceux des metatuiles d'origine."""
import struct, os, random
ORIGD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hideout_orig')
BLOCK = {8, 26, 27, 28, 153, 593, 594, 595, 596, 597, 598, 599, 601, 602, 603, 606, 607, 609, 610, 611, 614, 615, 616, 620, 622, 624, 632, 648, 649, 650, 651, 652, 653, 654, 656, 657, 658, 659, 660, 661, 662, 663, 664, 668, 669, 670, 671, 674, 675, 676, 677, 679, 682, 683, 684, 685, 686, 687, 693, 694, 695, 696, 697, 698, 699, 701, 702, 707, 708, 709, 713, 714, 715, 716, 717, 720, 721, 724, 725, 728, 729, 732, 733, 734, 735, 741, 742, 743, 744, 747, 748, 752, 755, 756, 760, 763, 764, 767, 770, 773, 774, 775, 776, 777, 784, 785, 787, 788, 789, 790, 791, 792, 793, 795, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 814, 815}
BLOCK |= {899, 900, 901, 913, 914, 915, 916, 917, 918, 919, 920, 933, 934, 935, 941, 942, 943, 944, 945, 949, 950, 951, 957, 958, 959, 936}
def blk(i): return i in BLOCK
def Wd(i): return i | (0x400 if blk(i) else 0x3000)
FL, SH, SHR = 641, 642, 643
def orig(name):
    d = open(os.path.join(ORIGD, name + '.bin'), 'rb').read(); return struct.unpack('<%dH' % (len(d) // 2), d)
OW = {'B1F': 28, 'B2F': 32, 'B3F': 22, 'B4F': 24}
def reg(name, x, y, w, h):
    g = orig(name); return [[g[(y + j) * OW[name] + x + i] for i in range(w)] for j in range(h)]
# motifs (ids, 0 = rien)
DESK = [[0, 688, 689, 690, 0], [0, 699, 697, 708, 643], [739, 707, 697, 698, 643], [0, 704, 705, 706, 643]]
DESK2 = [[688, 689, 690, 688, 689, 690], [699, 806, 807, 696, 697, 708], [707, 697, 698, 696, 697, 698], [704, 705, 706, 700, 705, 706]]
RACK = [[693, 694, 695], [701, 702, 703]]            # grosse machine adossee au mur (face + 1re rangee)
TERM = [[775, 773], [783, 781]]
MON = [[774, 774], [782, 782]]
SOFA = [[800, 801, 802], [808, 809, 810]]
GRAY = [[787, 788, 789, 787, 788, 789], [798, 799, 797, 795, 790, 791], [803, 804, 805, 803, 804, 805], [811, 812, 813, 1000, 812, 813]]
PLANT_A = [[769], [777]]
PLANT_B = [[768], [776]]
LOCKER = [[944, 945], [944, 945]]
SHELF = [[915, 916, 917]]
CRATE = [[914]]
TABLE_R = [[933, 934, 935], [941, 950, 943], [957, 958, 959]]
MAT = [[938, 939, 940]]
PAPERS = [[904, 905]]
BOARD = [[918, 919, 920]]
STAIR_UP = [[594, 595, 596], [602, 603, 604], [610, 611, 612]]       # a gauche : cellule praticable = (x+2, y+1)
STAIR_DN = [[597, 598, 599], [605, 606, 607], [613, 614, 615]]       # cellule praticable = (x, y+1)
ELEV = [[674, 675, 676], [682, 683, 684]]
class Cv:
    def __init__(s, w, h):
        s.w, s.h = w, h; s.g = [Wd(8)] * (w * h); s.z = [0] * (w * h)      # z : 1 = zone reprise par Onybris
        s.rnd = random.Random(7)
    def inb(s, x, y): return 0 <= x < s.w and 0 <= y < s.h
    def set(s, x, y, i, z=None):
        if s.inb(x, y):
            s.g[y * s.w + x] = Wd(i) if i < 0x400 else i
            if z is not None: s.z[y * s.w + x] = z
    def get(s, x, y): return s.g[y * s.w + x] & 0x3ff
    def zone(s, x0, y0, x1, y1, z=1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if s.inb(x, y): s.z[y * s.w + x] = z
    def fill(s, x0, y0, x1, y1, i):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.set(x, y, i)
    def put(s, rows, x, y):
        for j, r in enumerate(rows):
            for i, v in enumerate(r):
                if v: s.set(x + i, y + j, v)
    def room(s, x0, y0, x1, y1, z=0, deco=True):
        """interieur praticable x0..x1, y0..y1 ; murs autour (haut : 2 rangees, bas : 1)."""
        w = x1 - x0 + 1
        for x in range(x0 - 1, x1 + 2):
            e = 648 if x == x0 - 1 else 652 if x == x1 + 1 else (650 if deco and s.rnd.random() < .22 else 649)
            f = 656 if x == x0 - 1 else 660 if x == x1 + 1 else (658 if deco and s.rnd.random() < .22 else 657)
            b = 664 if x == x0 - 1 else 668 if x == x1 + 1 else (665 if x == x0 else 666)
            s.set(x, y0 - 2, e); s.set(x, y0 - 1, f); s.set(x, y1 + 1, b)
        for y in range(y0, y1 + 1):
            s.set(x0 - 1, y, 656); s.set(x1 + 1, y, 660)
            for x in range(x0, x1 + 1): s.set(x, y, SH if (y == y0 or x == x0) else FL)
        s.zone(x0 - 1, y0 - 2, x1 + 1, y1 + 1, z)
    def vdoor(s, x, yb, w=2):
        """passage entre la piece du dessus (bord bas = yb) et celle du dessous (bord haut = yb+1)."""
        for dx in range(w):
            for y in (yb, yb + 1, yb + 2): s.set(x + dx, y, FL)
    def hdoor(s, xr, yg, h=3):
        """piece a gauche (mur droit xr) et piece a droite (mur gauche xr+1), porte de hauteur h a partir de yg (jusqu'a la rangee du bas)."""
        for dy in range(h):
            s.set(xr, yg + dy, SH if dy == 0 else FL); s.set(xr + 1, yg + dy, SH if dy == 0 else FL)
        s.set(xr, yg - 2, 735); s.set(xr, yg - 1, 743); s.set(xr + 1, yg - 2, 734); s.set(xr + 1, yg - 1, 742)
    def stair_dn(s, x, y0):      # escalier 'bas' pose sur le mur du haut d'une piece dont la 1re rangee praticable est y0 ; renvoie la case de warp
        s.put(STAIR_DN, x, y0 - 1); return (x, y0)
    def stair_up(s, x, y0):
        s.put(STAIR_UP, x, y0 - 1); return (x + 2, y0)
    def save(s, path): open(path, 'wb').write(struct.pack('<%dH' % len(s.g), *s.g))
    def ascii(s):
        return '\n'.join(''.join('8' if (s.g[y * s.w + x] & 0x3ff) == 8 else ('#' if (s.g[y * s.w + x] >> 10) & 3 else '.') for x in range(s.w)) for y in range(s.h))
