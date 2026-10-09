# ======================================================================== FORET CALCINEE : sentier tortueux (l'ancien coupe-feu), clairieres, cratere central
DY = 9
def FX(x): return x if x <= 6 else int(round(6 + (x - 6) * 38 / 46))
def FY(y): return y if y <= 12 else (y - DY if y >= 50 else int(round(12 + (y - 12) * (38 - DY) / 38)))
def P(c): return (FX(c[0]), FY(c[1]))
def PB(b): return (FX(b[0]), FY(b[1]), FX(b[2]), FY(b[3]))
S_DOOR, N_DOOR = P((29, 50)), (5, 9)
S_ROWS = [0, 1, 2, 3, 4, 5, 2]                       # lignes du tuyau (art) pour y=50..56 : on voit la face nord avec la porte, puis le tuyau qui part hors carte
N_ROWS = [2, 5, 2, 5, 3, 4, 2, 5, 6, 7]              # y=0..9 : le tuyau vient du haut de la carte, la porte est en bas (face sud)
BUILD = {(S_DOOR[0] - 1 + i, S_DOOR[1] + j) for i in range(3) for j in range(7)} | {(4 + i, j) for i in range(3) for j in range(10)}
for c in BUILD: OCC[c] = 'tuyau'
for x in list(range(0, 4, 2)) + [7] + list(range(8, W, 2)): tree(x, 0)
for x in list(range(0, S_DOOR[0] - 2, 2)) + list(range(S_DOOR[0] + 2, W - 2, 2)): tree(x, H - 2)
for y in range(2, H - 2, 2): tree(0, y); tree(W - 2, y)
PATH = set()
WAY = [P(c) for c in [(29, 49), (29, 44), (41, 42), (41, 36), (12, 35), (12, 28), (40, 27), (40, 19), (8, 17)]] + [(6, 12), (5, 10)]
SPURS = [(P(a), P(b)) for a, b in [((12, 28), (9, 25))]]
CLEARINGS = [PB(b) for b in [(14, 38, 28, 46), (21, 16, 25, 17), (35, 16, 39, 17), (13, 16, 16, 17)]]
VOLC = (2, 34)
LAKE = {(x, y) for x in range(2, 10) for y in range(34, 46) if ((x - 5.5) / 4.7) ** 2 + ((y - 39.5) / 7.2) ** 2 + 0.25 * math.sin(x * 1.7 + y * 2.3) <= 0.9 or (y >= 44 and x <= 9)}                                       # volcan (4x4), au nord-ouest de la clairiere sud-ouest
GIANT = P((7, 21))                                      # grand arbre calcine (3x4) qui barre la diagonale gauche
def seg(a, b):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        t = k / max(1, n); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        for i in (0, 1): PATH.add((int(round(x)) + i, int(round(y))))
        PATH.add((int(round(x)) + 1, int(round(y)) + 1))
for a_, b_ in zip(WAY, WAY[1:]): seg(a_, b_)
for a_, b_ in SPURS: seg(a_, b_)
PATH -= BUILD
def path_id(x, y):
    N = (x, y - 1) in PATH; S = (x, y + 1) in PATH; Wn = (x - 1, y) in PATH; E = (x + 1, y) in PATH
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
for (x, y) in PATH:
    if 0 <= x < W and 0 <= y < H: put(x, y, 0x3000, path_id(x, y)); OCC[(x, y)] = 'chemin'
def dil(cells, r):
    return {(x + i, y + j) for (x, y) in cells for i in range(-r, r + 1) for j in range(-r, r + 1)}
OBJ0 = {'youngster': (26, 47), 'boy': (33, 46), 'rick': (45, 38), 'doug': (17, 39), 'sammy': (22, 31), 'anthony': (23, 16), 'charlie': (20, 14),
       'ball_pokeball': (16, 46), 'ball_antidote': (37, 16), 'ball_potion': (24, 46), 'ball_potion2': (27, 44)}
HID0 = {'potion': (20, 45), 'antidote': (14, 16)}
SIGNS0 = {'tips1': (32, 47), 'tips2': (43, 39), 'tips3': (24, 38), 'tips4': (15, 31), 'tips5': (30, 31), 'exit': (9, 13)}
OBJ = {k: P(v) for k, v in OBJ0.items()}; HID = {k: P(v) for k, v in HID0.items()}; SIGNS = {k: P(v) for k, v in SIGNS0.items()}
RES = dil(list(OBJ.values()) + list(HID.values()) + list(SIGNS.values()), 1)
CORR = dil(PATH, 2)
NOGO = {(x, y) for x in range(3, FX(12)) for y in range(FY(18), FY(28))}      # la diagonale gauche est fermee : que des arbres autour de l'arbre geant
CORR -= (NOGO - PATH)
CORR -= {c for c in CORR if c[0] >= 38 and c not in dil(PATH, 2)}
for (x0, y0, x1, y1) in CLEARINGS: CORR |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
CR = P((20, 40))
for c in LAKE: OCC[c] = 'reserve-volcan'
for i in range(3):
    for j in range(3): OCC[(CR[0] + i, CR[1] + j)] = 'reserve'
for i in range(3):
    for j in range(4):
        if (GIANT[0] + i, GIANT[1] + j) not in OCC: OCC[(GIANT[0] + i, GIANT[1] + j)] = 'reserve-geant'
rnd = random.Random(3030)
bad_ = [c for c in list(OBJ.values()) + list(HID.values()) + list(SIGNS.values()) if c in OCC]
assert not bad_, ('cases deja prises', bad_, [(c, OCC[c]) for c in bad_])
# ---- herbes hautes : dans les couloirs et les clairieres, jamais sur le chemin
TALL = []
tries = 0
while len(TALL) < 14 and tries < 20000:
    tries += 1; x0 = rnd.randint(3, W - 8); y0 = rnd.randint(4, H - 8); w, h = rnd.choice([(2, 4), (2, 5), (3, 3), (4, 2), (5, 2), (6, 2), (3, 4), (2, 3)])
    cells = [(x, y) for y in range(y0, y0 + h) for x in range(x0, x0 + w)]
    if any(c not in CORR or c in OCC or c in RES for c in cells): continue
    if any(c in dil(PATH, 0) for c in cells): continue
    TALL.append((x0, y0, x0 + w - 1, y0 + h - 1))
    for c in cells: OCC[c] = 'herbe'; put(c[0], c[1], 0x3000, TALL_M, st=1)
# ---- foret : arbres sur un reseau 2x2 partout sauf couloirs/clairieres ; un tiers sont des squelettes calcines (art)
DEAD = []
for y in range(2, H - 2, 2):
    for x in range(2, W - 2, 2):
        cells = [(x + i, y + j) for i in range(2) for j in range(2)]
        if any(c in CORR or c in OCC or c in RES for c in cells): continue
        if rnd.random() < (0.0 if x >= 37 else 0.05): continue
        east = x >= W - 10
        if rnd.random() < (0.9 if east else 0.55): tree(x, y); claim(x, y, 2, 2, 'arbre')
        else:
            kind = rnd.choice(['boulder', 'thorns', 'spire', 'spire', 'dead'] if east else ['dead', 'dead', 'boulder', 'thorns', 'spire'])
            DEAD.append((x, y, kind)); claim(x, y, 2, 2, kind)
# ---- arbres serres de part et d'autre des deux entrees (tuyaux) : pas de sol nu colle au tuyau
for (x, y) in [(2, 2), (2, 4), (2, 6), (2, 8), (8, 2), (8, 4), (8, 6), (8, 8)] + [(S_DOOR[0] - 4, 40), (S_DOOR[0] - 4, 42), (S_DOOR[0] - 4, 44), (S_DOOR[0] - 2, 44), (S_DOOR[0] + 2, 44), (S_DOOR[0] + 2, 42)]:
    cells = [(x + i, y + j) for i in range(2) for j in range(2)]
    if any(c in OCC or c in RES or c in PATH or not (1 <= c[0] < W - 1 and 1 <= c[1] < H - 2) for c in cells): continue
    tree(x, y); claim(x, y, 2, 2, 'arbre')
# ---- trou a boucher : deux rochers a cote du rocher voisin
for (x, y) in ((28, 12), (30, 12)):
    cells = [(x + i, y + j) for i in range(2) for j in range(2)]
    assert not any(c in OCC or c in RES or c in PATH for c in cells), ('trou deja pris', x, y)
    DEAD.append((x, y, 'boulder')); claim(x, y, 2, 2, 'boulder')
# ---- herbe cendree : zones de sol gris clair (c'etait une foret), hors arbres, chemin et objets
ASH = set()
for y in range(2, H - 2):
    for x in range(2, W - 2):
        c = (x, y)
        if c in OCC or c in RES: continue
        n = math.sin(x * 0.45 + y * 0.3) + math.sin(y * 0.6 - x * 0.2) + math.sin(x * 0.17 + y * 0.5)
        if n > 0.5: put(x, y, 0x3000, GRASS_M, st=1); ASH.add(c)
RIDGE = set(); WALL = set(); BLOB = {}
