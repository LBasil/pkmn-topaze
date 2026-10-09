# ======================================================================== ROUTE 3 « la coulee » : crêtes de roche verticales percees d'une breche en herbe haute, salles de braise, lacs de lave
S_DOOR, N_DOOR = (-5, -5), (-5, -5)
WEST_ROWS = (10, 13); EAST_ROWS = (14, 17)
for x in range(0, W - 2, 2):
    tree(x, 0); tree(x, H - 2)
for y in range(2, H - 2, 2):
    if not (WEST_ROWS[0] <= y <= WEST_ROWS[1]): tree(0, y)
    if not (EAST_ROWS[0] <= y <= EAST_ROWS[1]): tree(W - 2, y)
PATH = set()
RIDGES = [(15, 12, 16), (32, 3, 7), (49, 17, 21), (66, 6, 10)]     # (x gauche, breche haut, breche bas)
WAY = [(1, 11), (6, 12), (11, 13), (15, 14), (21, 12), (24, 8), (29, 5), (32, 5), (38, 8), (41, 14), (44, 19), (49, 19),
       (55, 15), (58, 10), (62, 8), (66, 8), (71, 11), (73, 15), (76, 16), (78, 15)]
def seg(a, b):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        t = k / max(1, n); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        for i in (0, 1): PATH.add((int(round(x)) + i, int(round(y))))
        PATH.add((int(round(x)) + 1, int(round(y)) + 1))
for a_, b_ in zip(WAY, WAY[1:]): seg(a_, b_)
def wob(seed_, n=H):
    r = random.Random(seed_); v = 0; out = []
    for _ in range(n):
        if r.random() < 0.3: v = max(-1, min(1, v + r.choice((-1, 1))))
        out.append(v)
    return out
RIDGE = set(); GAPC = set(); BLOB = {}
for k, (x0, g0, g1) in enumerate(RIDGES):
    wl, wr = wob(100 + k), wob(200 + k)
    for y in range(2, H - 2):
        if g0 <= y <= g1:
            for x in range(x0 - 3, x0 + 7): GAPC.add((x, y))
            continue
        sh = int(round(2 * math.sin(y * 0.38 + k * 1.7)))
        for x in range(x0 + sh + wl[y], x0 + sh + 3 + wr[y]): RIDGE.add((x, y)); BLOB[(x, y)] = (x0, y)
# la breche est pleine d'herbe haute : on ne dessine pas de chemin dessous, on ne laisse pas de roche
PATH -= GAPC
RIDGE -= GAPC
PATH = {c for c in PATH if 0 <= c[0] < W and 0 <= c[1] < H and c not in RIDGE}
def path_id(x, y):
    N = (x, y - 1) in PATH; S = (x, y + 1) in PATH; Wn = (x - 1, y) in PATH or x == 0; E = (x + 1, y) in PATH or x == W - 1
    if N and S and Wn and E: return 289
    if not N and not Wn and S and E: return 280
    if not N and not E and S and Wn: return 282
    if not S and not Wn and N and E: return 296
    if not S and not E and N and Wn: return 298
    if not N and S and Wn and E: return 281
    if not S and N and Wn and E: return 297
    if not Wn and N and S and E: return 288
    if not E and N and S and Wn: return 290
    return 289
for (x, y) in PATH: put(x, y, 0x3000, path_id(x, y)); OCC[(x, y)] = 'chemin'
for c in RIDGE: OCC[c] = 'roche'
for c in GAPC: OCC[c] = 'herbe'
def dil(cells, r):
    return {(x + i, y + j) for (x, y) in cells for i in range(-r, r + 1) for j in range(-r, r + 1)}
PATH_D1 = dil(PATH, 1)
rnd = random.Random(3033)
# ---- lacs de lave (cases isolees d'autotile) : deux dans les salles 2 et 4
LAKE = set()
def lake_shape(cx, cy, rx, ry):
    return {(x, y) for y in range(int(cy - ry) - 1, int(cy + ry) + 2) for x in range(int(cx - rx) - 1, int(cx + rx) + 2)
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.2 * math.sin(x * 1.7 + y * 2.3) <= 1}
_busy = dil(PATH, 2) | dil(RIDGE, 1) | dil(GAPC, 1)
_all = []
for cy in range(5, H - 6):
    for cx in range(16, W - 12):
        cells = lake_shape(cx, cy, 2.6, 3.0)
        if len(cells) >= 18 and not any(c in _busy for c in cells) and all(2 <= c[0] < W - 2 and 2 <= c[1] < H - 3 for c in cells): _all.append((cx, cy, cells))
print('lacs possibles', len(_all))
rnd.shuffle(_all); _chosen = []
for (cx, cy, cells) in _all:
    if len(_chosen) >= 3: break
    if all(abs(cx - a_) + abs(cy - b_) >= 18 for (a_, b_) in _chosen): _chosen.append((cx, cy)); LAKE |= cells
for c in LAKE: OCC[c] = 'lac'
LAKE_Z = dil(LAKE, 1)
# ---- ilots de roche (plateaux compacts) : relief dans les salles
def free_cell(c, r=2):
    return 3 <= c[0] <= W - 4 and 3 <= c[1] <= H - 4 and c not in OCC and c not in GAPC and c not in LAKE_Z and not any((c[0] + i, c[1] + j) in PATH or (c[0] + i, c[1] + j) in RIDGE or (c[0] + i, c[1] + j) in GAPC for i in range(-r, r + 1) for j in range(-r, r + 1))
for _ in range(60):
    if len([1 for v in OCC.values() if v == 'ilot']) > 150: break
    c0 = (rnd.randint(4, W - 5), rnd.randint(4, H - 5))
    if not free_cell(c0): continue
    blob = {c0}; n_ = rnd.randint(6, 12)
    for _t in range(80):
        if len(blob) >= n_: break
        p = rnd.choice(sorted(blob)); q = (p[0] + rnd.choice((-1, 0, 1)), p[1] + rnd.choice((-1, 0, 1)))
        if q not in blob and free_cell(q) and sum(((q[0] + a, q[1] + b) in blob) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 1: blob.add(q)
    if len(blob) < 5: continue
    for c in blob: RIDGE.add(c); OCC[c] = 'ilot'; BLOB[c] = c0
# ---- panneaux, PNJ, objets caches
_sc = sorted(c for c in dil(PATH, 2) - PATH_D1 if 68 <= c[0] <= 75 and 8 <= c[1] <= 18 and c not in OCC and c not in RIDGE and c not in GAPC and c not in LAKE_Z)
SIGNS = {'sign': _sc[len(_sc) // 2]}
OBJ = {}
def clear_line(c, d, n):
    return all(((c[0] + d[0] * k, c[1] + d[1] * k) not in OCC or (c[0] + d[0] * k, c[1] + d[1] * k) in PATH) and 1 <= c[0] + d[0] * k < W - 1 and 1 <= c[1] + d[1] * k < H - 1 for k in range(1, n + 1))
DIRS = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}
TR = [('colton', (19, 28)), ('ben', (22, 30)), ('janice', (36, 46)), ('greg', (37, 47)), ('calvin', (53, 63)), ('sally', (54, 62)), ('james', (70, 76)), ('robin', (57, 64))]
FACE = {}; SIGHT = {}; LINE = set()
for name, (xa, xb) in TR:
    cands = []
    for y in range(3, H - 3):
        for x in range(xa, xb + 1):
            c = (x, y)
            if c in OCC or c in PATH_D1 or c in LAKE_Z or c in GAPC or any(dil({c}, 2) & set(OBJ.values())): continue
            for dn, d in DIRS.items():
                for k in range(2, 5):
                    p = (x + d[0] * k, y + d[1] * k)
                    if not (1 <= p[0] < W - 1 and 1 <= p[1] < H - 1): break
                    if p in PATH and all(((x + d[0] * j, y + d[1] * j) not in OCC) for j in range(1, k)):
                        cands.append((c, dn, k)); break
    assert cands, ('pas de place pour', name)
    c, dn, k = rnd.choice(cands)
    OBJ[name] = c; FACE[name] = dn; SIGHT[name] = k
    d = DIRS[dn]
    for j in range(1, k + 1): LINE.add((c[0] + d[0] * j, c[1] + d[1] * j))
    OCC[c] = 'pnj'
OBJ['youngster'] = (11, 16); OCC[(11, 16)] = 'pnj'
_hc = sorted(c for c in dil(PATH, 2) - PATH_D1 if 36 <= c[0] <= 60 and c not in OCC and c not in RIDGE and c not in LAKE_Z and c not in GAPC and c not in LINE and not any((c[0] + i, c[1] + j) in OCC and OCC[(c[0] + i, c[1] + j)] != 'chemin' for i in (-1, 0, 1) for j in (-1, 0, 1)))
HID = {'oran': rnd.choice(_hc)}
RES = dil(list(OBJ.values()) + list(SIGNS.values()) + list(HID.values()), 1) | LINE
CORR = dil(PATH, 1) | LAKE_Z | LINE | dil(list(OBJ.values()) + list(SIGNS.values()) + list(HID.values()), 2)
CORR -= RIDGE | GAPC
PATCHZ = dil(PATH, 3)
# ---- herbes hautes : quelques parcelles dans les salles, jamais sur le chemin
TALL = []
tries = 0
while len(TALL) < 10 and tries < 20000:
    tries += 1; x0 = rnd.randint(3, W - 8); y0 = rnd.randint(3, H - 7); w, h = rnd.choice([(2, 3), (3, 3), (4, 2), (3, 2), (2, 4)])
    cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    if any(c not in PATCHZ or c in OCC or c in RES or c in PATH_D1 or c in LAKE_Z for c in cells): continue
    TALL.append((x0, y0, x0 + w - 1, y0 + h - 1))
    for c in cells: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M, st=1)
# ---- foret : arbres (reseau 2x2) partout ou ce n'est ni couloir, ni roche, ni breche
DEAD = []
for (ox, oy) in ((0, 0), (1, 1), (1, 0), (0, 1)):
    for y in range(2 + oy, H - 3, 2):
        for x in range(2 + ox, W - 3, 2):
            cells = [(x + i, y + j) for i in range(2) for j in range(2)]
            if any(c in PATH_D1 or c in OCC or c in RES or c in LAKE_Z or c in RIDGE or c in GAPC for c in cells): continue
            if rnd.random() < 0.55: tree(x, y); claim(x, y, 2, 2, 'arbre')
            else:
                kind = rnd.choice(['dead', 'dead', 'boulder', 'thorns', 'spire']); DEAD.append((x, y, kind)); claim(x, y, 2, 2, kind)
ASH = set()
for y in range(2, H - 2):
    for x in range(2, W - 2):
        c = (x, y)
        if c in OCC or c in RES: continue
        n = math.sin(x * 0.45 + y * 0.3) + math.sin(y * 0.6 - x * 0.2) + math.sin(x * 0.17 + y * 0.5)
        if n > 0.5: put(x, y, 0x3000, GRASS_M, st=1); ASH.add(c)
