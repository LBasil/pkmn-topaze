# controle Route 14 : fuites de falaise (cases « couvertes » sans collision retirees), bord atteignable = sorties seules
import struct, collections
W, H = 24, 60
g = struct.unpack('<%dH' % (W * H), open('data/layouts/Route14/map.bin', 'rb').read())
att = struct.unpack('<%dI' % (len(open('data/tilesets/primary/general_route14v2/metatile_attributes.bin', 'rb').read()) // 4), open('data/tilesets/primary/general_route14v2/metatile_attributes.bin', 'rb').read())
satt = struct.unpack('<%dI' % (len(open('data/tilesets/secondary/celadon_route14v2/metatile_attributes.bin', 'rb').read()) // 4), open('data/tilesets/secondary/celadon_route14v2/metatile_attributes.bin', 'rb').read())
A = lambda m: att[m] if m < 640 else satt[m - 640]
def blocked(c): v = g[c[1] * W + c[0]]; return bool(v & 0xc00) or (A(v & 0x3ff) & 0x1ff) in (0x10, 0x11, 0x12, 0x13, 0x15, 0x1b)
def covered(c): v = g[c[1] * W + c[0]]; return (A(v & 0x3ff) >> 29) & 3 == 1 or (A(v & 0x3ff) & 0x60000000) != 0
def reach(start, skip=lambda c: False):
    seen = {start}; q = collections.deque([start])
    while q:
        c = q.popleft()
        for a, b in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + a, c[1] + b)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n) and not skip(n): seen.add(n); q.append(n)
    return seen
R = reach((1, 51)); edge = sorted(c for c in R if c[0] in (0, W - 1) or c[1] in (0, H - 1))
print('bord atteignable :', edge)
EXIT = {(0, y) for y in range(47, 57)} | {(23, y) for y in range(16, 20)}
print('hors sorties :', [c for c in edge if c not in EXIT])
cov = {c for c in R if covered(c)}
R2 = reach((1, 51), lambda c: c in cov)
print('cases couvertes', len(cov), '; apres retrait, sortie est atteignable :', (22, 17) in R2, '(doit etre False)', '; sortie ouest :', (1, 51) in R2)
print('spur atteint avec escaliers :', (11, 10) in R)
