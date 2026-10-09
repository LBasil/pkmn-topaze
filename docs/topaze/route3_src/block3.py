# ---- placement
DOORS = set()
def near(x, y, r=1):
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if (x + i, y + j) in OCC or (x + i, y + j) in ART_PLACE: return True
    return False
for c in SIGNS.values(): claim(c[0], c[1], 1, 1, 'panneau'); ART_PLACE[c] = ART[('sign', 2)]
for (x, y, kind) in DEAD:
    arts = ART[('dead', 2, rnd.randrange(2))] if kind == 'dead' else ART[(kind, 2)]
    for (i, j), k in arts.items(): ART_PLACE[(x + i, y + j)] = k
for c in LAKE: del OCC[c]
for c in LAKE: claim(c[0], c[1], 1, 1, 'lac de lave')
for c, k in ART[('volcano', 2)].items(): ART_PLACE[c] = k
for (x, y) in sorted(RIDGE):
    m = (((x, y - 1) in RIDGE) * 1) | (((x + 1, y) in RIDGE) * 2) | (((x, y + 1) in RIDGE) * 4) | (((x - 1, y) in RIDGE) * 8)
    ART_PLACE[(x, y)] = ROCK[(m, 2, (x * 3 + y * 5) % 4 if m == 15 else (x + y) % 2)]
# la breche : herbe haute sur toute la zone
for c in GAPC: put(c[0], c[1], 0x3000, TALL_M, st=1)
PATH_D = dil(PATH, 1)
# ---- cases isolees (ou la grille d'arbres ne tient pas) : obsidienne, souches, braise : plus de sol nu
_FILL = ['sm0', 'sm1', 'stump', 'sm0', 'sm1']
for y in range(2, H - 2):
    for x in range(2, W - 2):
        c = (x, y)
        if c in OCC or c in PATH_D or c in RES or c in LAKE_Z or c in ASH or c in ART_PLACE or (G[c] & 0xc00): continue
        if rnd.random() < 0.8: claim(x, y, 1, 1, 'rocaille'); ART_PLACE[c] = ART[(rnd.choice(_FILL), 2)]
OPEN = sorted(c for c in CORR if c not in OCC and c not in RES and c not in PATH_D and c not in LINE and c not in ASH and c not in LAKE_Z and 2 <= c[0] <= W - 3 and 2 <= c[1] <= H - 4)
def scatter(n, fn):
    k = tries = 0
    while k < n and tries < 3000:
        tries += 1; c = rnd.choice(OPEN)
        if fn(c): k += 1
def one(name):
    def f(c):
        if near(c[0], c[1], 1) or c in ART_PLACE: return False
        claim(c[0], c[1], 1, 1, name); ART_PLACE[c] = ART[(name_map[name], 2)]; return True
    return f
name_map = {'vent': 'vent', 'souche': 'stump', 'cendre': 'ash', 'obsidienne0': 'sm0', 'obsidienne1': 'sm1'}
for nm, n in (('vent', 14), ('souche', 10), ('cendre', 8), ('obsidienne0', 6), ('obsidienne1', 5)): scatter(n, one(nm))
# ---- accessibilite
ART_RAW_BLOCK = set(ART_PLACE)
def blocked(c):
    return c in ART_RAW_BLOCK or bool(G[c] & 0xc00)
def flood(s0, extra=()):
    seen_ = {s0}; q_ = collections.deque([s0])
    while q_:
        c = q_.popleft()
        for d_ in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            n_ = (c[0] + d_[0], c[1] + d_[1])
            if 0 <= n_[0] < W and 0 <= n_[1] < H and n_ not in seen_ and n_ not in extra and not blocked(n_): seen_.add(n_); q_.append(n_)
    return seen_
START = (0, 11); EXIT = (W - 1, 15)
seen = flood(START)
for c in [EXIT] + [(0, y) for y in range(WEST_ROWS[0], WEST_ROWS[1] + 1)] + [(W - 1, y) for y in range(EAST_ROWS[0], EAST_ROWS[1] + 1)] + list(OBJ.values()) + list(HID.values()): assert c in seen, ('inaccessible', c)
for (x0, y0, x1, y1) in TALL: assert (x0, y0) in seen, ('herbe inaccessible', x0, y0)
for c in SIGNS.values(): assert any((c[0] + dx, c[1] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), ('panneau inaccessible', c)
assert EXIT not in flood(START, extra=GAPC), 'la sortie est atteignable sans traverser les breches en herbe'
# ---- dresseurs : ligne de vue sans obstacle vers le chemin (deja garantie par la geometrie) ; on verifie qu'aucun decor ne la coupe
for k in FACE:
    x, y = OBJ[k]; d_ = DIRS[FACE[k]]
    for j in range(1, SIGHT[k] + 1):
        c = (x + d_[0] * j, y + d_[1] * j)
        assert not blocked(c) or c in PATH, ('ligne de vue coupee', k, c)
print('regards', FACE)
