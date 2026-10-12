# controle Route 11 : bord atteignable = sorties seules ; le poste de garde est le seul passage vers l'est ; escaliers obligatoires
import struct, collections
W, H = 72, 20
g = struct.unpack('<%dH' % (W * H), open('data/layouts/Route11/map.bin', 'rb').read())
rd = lambda f: struct.unpack('<%dI' % (len(open(f, 'rb').read()) // 4), open(f, 'rb').read())
att = rd('data/tilesets/primary/general_route11v2/metatile_attributes.bin'); satt = rd('data/tilesets/secondary/celadon_route11v2/metatile_attributes.bin')
A = lambda m: att[m] if m < 640 else satt[m - 640]
def blocked(c): v = g[c[1] * W + c[0]]; return bool(v & 0xc00) or (A(v & 0x3ff) & 0x1ff) in (0x10, 0x11, 0x12, 0x13, 0x15, 0x1b)
covered = lambda c: (A(g[c[1] * W + c[0]] & 0x3ff) & 0x60000000) != 0
LINK = {(58, 10): (65, 10), (65, 10): (58, 10)}
def reach(start, skip=lambda c: False, link=True):
    seen = {start}; q = collections.deque([start])
    while q:
        c = q.popleft()
        nb = [(c[0] + a, c[1] + b) for a, b in ((0, 1), (1, 0), (-1, 0), (0, -1))] + ([LINK[c]] if link and c in LINK else [])
        for n in nb:
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not blocked(n) and not skip(n): seen.add(n); q.append(n)
    return seen
R = reach((1, 9)); edge = sorted(c for c in R if c[0] in (0, W - 1) or c[1] in (0, H - 1))
EXIT = {(0, 8), (0, 9), (0, 10), (71, 9), (71, 10), (71, 11)}
print('bord atteignable :', edge); print('hors sorties :', [c for c in edge if c not in EXIT])
print('sans le poste de garde : sortie est atteignable', (70, 10) in reach((1, 9), link=False), '(doit etre False)')
cov = {c for c in R if covered(c)}
print('cases couvertes', len(cov), '; sans escaliers/pont : poste de garde atteignable', (57, 10) in reach((1, 9), lambda c: c in cov), '(False) ; plateau', (24, 6) in reach((1, 9), lambda c: c in cov), '(False)')
print('avec : plateau', (24, 6) in R, ', grotte (6,8)', (6, 8) in R, ', sortie est', (70, 10) in R, ', porte', (58, 10) in R, (65, 10) in R)
