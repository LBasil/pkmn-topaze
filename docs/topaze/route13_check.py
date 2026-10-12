# controle Route 13 : bord atteignable = sorties seules ; sans escaliers, plateau et sortie ouest inatteignables depuis l'embarcadere
import struct, collections
W, H = 72, 20
g = struct.unpack('<%dH' % (W * H), open('data/layouts/Route13/map.bin', 'rb').read())
rd = lambda f: struct.unpack('<%dI' % (len(open(f, 'rb').read()) // 4), open(f, 'rb').read())
att = rd('data/tilesets/primary/general_route13v2/metatile_attributes.bin'); satt = rd('data/tilesets/secondary/celadon_route13v2/metatile_attributes.bin')
A = lambda m: att[m] if m < 640 else satt[m - 640]
def blocked(c): v = g[c[1] * W + c[0]]; return bool(v & 0xc00) or (A(v & 0x3ff) & 0x1ff) in (0x10, 0x11, 0x12, 0x13, 0x15, 0x1b)
stairs = lambda c: (A(g[c[1] * W + c[0]] & 0x3ff) & 0x60000000) != 0 and c[1] >= 5
def reach(start, skip=lambda c: False):
    seen = {start}; q = collections.deque([start])
    while q:
        c = q.popleft()
        for a, b in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n = (c[0] + a, c[1] + b)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n) and not skip(n): seen.add(n); q.append(n)
    return seen
R = reach((62, 2)); edge = sorted(c for c in R if c[0] in (0, W - 1) or c[1] in (0, H - 1))
EXIT = {(62, 0), (63, 0)} | {(0, y) for y in range(16, 20)}
print('bord atteignable :', edge); print('hors sorties :', [c for c in edge if c not in EXIT])
R2 = reach((62, 2), stairs)
print('cases escalier', sum(stairs(c) for c in R), '; sans escaliers : sortie ouest atteignable', (1, 17) in R2, '(doit etre False) ; plateau', (36, 8) in R2, '(False)')
print('avec escaliers : sortie ouest', (1, 17) in R, ', plateau', (36, 8) in R, ', impasse', (12, 5) in R)
