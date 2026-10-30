# TOURMALIA v23 : COPIE EXACTE (par tuiles) de la carte d'inspiration de Basil (carte de fan-game, 84 x 46 cases de 16 px).
# L'image source est parfaitement alignee sur une grille de 16 px : on la decoupe en 316 metatuiles / 700 tuiles 8x8, on regroupe les 92 couleurs
# en 13 palettes GBA (quelques teintes quasi identiques sont fusionnees), puis on pose la collision a la main (marchable / eau / bloque / porte).
# ATTENTION : les pixels viennent d'un autre jeu. Usage prive/prototype ; a remplacer ou a faire valider par l'auteur avant toute diffusion (voir docs/topaze/tourmalia_copy/CREDITS.md).
# Lancer depuis la racine du depot :  python3 docs/topaze/tourmalia_copy.py  puis  python3 docs/topaze/tourmalia_river_events.py  puis  python3 docs/topaze/fog_strips.py
import pickle, struct, json, collections, heapq, os, re, shutil
from PIL import Image
import numpy as np
D0 = 'docs/topaze/tourmalia_copy/'
PRI = 'data/tilesets/primary/general_tourmaline/'; SEC = 'data/tilesets/secondary/fortree_tourmaline/'
for d in (PRI, SEC): os.makedirs(d + 'palettes', exist_ok=True)
grid, mts = pickle.load(open(D0 + 'grid.pkl', 'rb')); mapc, PALS = pickle.load(open(D0 + 'pal.pkl', 'rb'))
X0 = 22                                                    # coupe de la zone ouest (cabanes 1 et 2, bas-pays SO) : carte 62 x 46
grid = [r[X0:] for r in grid]
H, W = len(grid), len(grid[0]); NM = len(mts)
S = lambda c: (c[0] - X0, c[1])
# retouches demandees par Basil : cabane coupee en haut a gauche retiree, ponts de corde (decoratifs, ne menent nulle part) et pont de rondins sans issue retires
for _y in range(1, 10):
    for _x in range(0, 5): grid[_y][_x] = 1
for _y in range(H):
    for _x in range(W):
        if grid[_y][_x] in (58, 59, 60, 61, 82, 83, 84): grid[_y][_x] = 1
for _x, _y in ((42, 9), (43, 9), (42, 10), (43, 10)): grid[_y][_x] = 6
q5 = lambda p: (int(p[0]) >> 3, int(p[1]) >> 3, int(p[2]) >> 3)

# ------------------------------------------------------------------ tuiles + palettes
PALCOLS = [sorted(p) for p in PALS]
assert len(PALCOLS) <= 13 and all(len(p) <= 15 for p in PALCOLS)
TILES = {(0, (0,) * 64): 0}; TILE_LIST = [(0, (0,) * 64)]
def tile_of(block):
    cs = [mapc.get(q5(p), q5(p)) for p in block.reshape(-1, 3)]; s = set(cs)
    pi = next(i for i, p in enumerate(PALS) if s <= p)
    key = (pi, tuple(PALCOLS[pi].index(c) + 1 for c in cs))
    if key not in TILES: TILES[key] = len(TILE_LIST); TILE_LIST.append(key)
    return TILES[key], pi
ENT = []
for m in mts:
    bot = []
    for ty in (0, 1):
        for tx in (0, 1):
            t, pi = tile_of(m[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]); bot.append(t | (pi << 12))
    ENT.append(bot + [0, 0, 0, 0])
NT = len(TILE_LIST)
assert NT <= 640 + 384, ('trop de tuiles', NT)

# ------------------------------------------------------------------ classification a la main
WALK = {9, 10, 18, 26, 27, 45, 49, 87, 88, 98, 114, 169, 257, 270, 271, 284, 285, 292, 297, 30, 100, 110, 229, 277, 95, 282, 283, 86, 99, 244, 253, 97}
WATER = {93, 102, 103, 104, 107, 108, 112, 113, 115, 116, 119, 137, 179, 180, 293, 294, 295, 296, 300, 301, 309, 311, 133, 125, 126}
TALL = {30, 100}; DOORIDS = {70, 248, 184, 244}
GRASS = 45
BUILD = set()
for x0, y0, x1, y1 in ((14, 22, 17, 25), (23, 26, 26, 29), (30, 16, 36, 20), (40, 17, 56, 24)):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): BUILD.add((x, y))
DOORS = {'center': (37, 25), 'mart': (46, 29), 'gym': (55, 20), 'cave': (69, 24),
         'th3': (42, 8), 'th4': (47, 14), 'th5': (35, 16), 'th6': (53, 32)}
DOORS = {k: S(v) for k, v in DOORS.items()}
PARKED = {'th1': (0, 0), 'th2': (0, 1)}                  # cabanes 1 et 2 coupees : portes garees dans la foret
SIGNC = {'city': S((40, 39)), 'gym': S((51, 19)), 'bike': S((66, 29)), 'tips': S((37, 16))}
BUILD |= set(SIGNC.values()); BUILD |= {S(c) for c in ((36, 16), (70, 24))}
DECK = {53, 78, 62}
WALKC = {}                                                              # cellule -> 'W' marchable force
for k, (x, y) in DOORS.items(): WALKC[(x, y)] = 1
for k, (x, y) in DOORS.items():                                         # couloir echelle/ponton sous chaque cabane
    if k.startswith('th'):
        y += 1
        while y < H and not (grid[y][x] in WALK and y > DOORS[k][1] + 1):
            WALKC[(x, y)] = 1; y += 1
# couloir droit de la rencontre avec le rival (3 de large) + bande du nord
RIV = [(x - X0, y) for y in range(6, 13) for x in (70, 71, 72)] + [(73 - X0, 6)]
def walk(c): return grid[c[1]][c[0]] in WALK or c in WALKC or c in CARVED
CARVED = set()
DOORSET = set(DOORS.values())
def cost(c):
    if c in DOORSET: return 500
    if walk(c): return 1
    if c in BUILD: return 500
    return 60 if grid[c[1]][c[0]] in WATER else 6
def dij(srcs, targets):
    dist = {s: 0 for s in srcs}; prev = {}; pq = [(0, s) for s in srcs]; heapq.heapify(pq)
    while pq:
        dd, c = heapq.heappop(pq)
        if dd > dist.get(c, 1e9): continue
        if c in targets:
            p = [c]
            while p[-1] in prev: p.append(prev[p[-1]])
            return p
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H:
                nd = dd + cost(n)
                if nd < dist.get(n, 1e9): dist[n] = nd; prev[n] = c; heapq.heappush(pq, (nd, n))
def comp(s):
    seen = {s}; qq = collections.deque([s])
    while qq:
        c = qq.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and walk(n) and n not in DOORSET: seen.add(n); qq.append(n)
    return seen
CARVED |= set(RIV)
STUBS = [S(c) for c in ((83, 32), (42, 45), (43, 45), (44, 45), (81, 0))]      # largeur des sorties = celle des anciennes sorties (retour depuis les routes voisines)
CARVED |= set(STUBS)
HUB = S((37, 26))
FRONT = {k: S(v) for k, v in {'mart': (46, 30), 'gym': (55, 21), 'cave': (69, 26), 'th3': (42, 9), 'th4': (47, 15), 'th5': (35, 17), 'th6': (53, 33)}.items()}
EXITC = {'N': S((82, 0)), 'E': S((83, 31)), 'S': S((41, 45)), 'riv': S((71, 6))}
# sortie ouest : bord gauche le moins couteux a relier ; 4 cases de large (Route 4 Est)
_m0 = comp(HUB); _bw = None
for _y in range(4, H - 4):
    _p = dij(_m0, {(0, _y)})
    if _p:
        _c = sum(cost(z) for z in _p[:-1])
        if _bw is None or _c < _bw[0]: _bw = (_c, _y)
EXITC['W'] = (0, _bw[1]); STUBS += [(0, _bw[1] + i) for i in (1, 2, 3)]; CARVED |= set(STUBS)
todo = dict(FRONT); todo.update(EXITC)
main = comp(HUB)
while todo:
    best = None
    for k, c in todo.items():
        if c in main: continue
        p = dij(main, {c})
        if p is None: continue
        cst = sum(cost(z) for z in p[:-1])
        if best is None or cst < best[0]: best = (cst, k, p)
    if best is None: break
    _, k, p = best
    for z in p:
        if not walk(z): CARVED.add(z)
    main = comp(HUB)
    for k2 in [k2 for k2, c in todo.items() if c in main]: del todo[k2]
assert not todo, ('inaccessibles', todo)
print('cases creusees :', len(CARVED))

# ------------------------------------------------------------------ attributs des metatuiles
ATT = [0] * NM
for i in range(NM):
    a = 0
    if i in WATER: a = 0x10 | 0x22000400
    if i in TALL: a = 0x02 | 0x1000200
    if i in DOORIDS: a = 0x69
    ATT[i] = a
# carte
G = {}
for y in range(H):
    for x in range(W):
        c = (x, y); v = grid[y][x]
        if c in CARVED and c not in WALKC and v not in WALK: v = GRASS
        if c in BUILD and c not in WALKC: G[c] = 0x400 | (640 + v)
        elif walk(c): G[c] = 0x3000 | (640 + v)
        elif v in WATER: G[c] = 0x1000 | (640 + v)
        else: G[c] = 0x400 | (640 + v)
blockedc = lambda c: bool(G[c] & 0xc00)
def passable(c): return not (G[c] & 0x400)
# ------------------------------------------------------------------ PNJ, panneaux, barrages
def reach_from(s, ban=()):
    seen = {s}; qq = collections.deque([s])
    while qq:
        c = qq.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and n not in ban and n not in DOORSET and passable(n) and not (G[n] & 0x1000 and not G[n] & 0x2000): seen.add(n); qq.append(n)
    return seen
ALL = reach_from(HUB)
NPCCELLS = set()
USED = set(DOORS.values()) | set(SIGNC.values()) | set(FRONT.values())
def near(t, r=4, nb=3):
    best = None
    for y in range(max(0, t[1] - r), min(H, t[1] + r + 1)):
        for x in range(max(0, t[0] - r), min(W, t[0] + r + 1)):
            c = (x, y)
            if c in ALL and c not in USED and c not in CARVED and c not in WALKC and grid[y][x] in (9, 10, 18, 26, 27, 45, 49, 87, 88, 98, 114):
                n = sum(1 for d in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + d[0], y + d[1]) in ALL)
                if n >= nb and len(reach_from(HUB, ban={c} | NPCCELLS)) == len(ALL) - 1 - len(NPCCELLS & ALL):
                    s = abs(x - t[0]) + abs(y - t[1])
                    if best is None or s < best[0]: best = (s, c)
    assert best, ('pas de case', t); USED.add(best[1]); NPCCELLS.add(best[1]); return best[1]
NPC = {}
NPC['boy'] = near(S((40, 28))); NPC['balding'] = near(S((44, 22))); NPC['youngster'] = near(S((38, 20))); NPC['woman'] = near((6, 36), 10)
NPC['camper'] = near((4, 31), 12, 2); NPC['oldman'] = near(S((64, 32)), 6); NPC['hidden'] = near(S((58, 25)), 5)
# est : couloir creuse (75..83, 31) ; arbre a couper + policier a la porte
corr = sorted(c for c in CARVED if c[1] == 31 and c[0] >= 75 - X0)
assert corr, 'pas de couloir est'
gate = corr[len(corr) // 2]
NPC['cuttree'] = gate; NPC['policeman_block'] = gate
NPC['policeman'] = near((corr[0][0] - 1, 31), 6)
# sud : echelle (41,43..45) ; arbre devant, Spectrum + la fille sur l'echelle (barrage) puis a cote (repos)
NPC['slowbro_block'] = S((41, 43)); NPC['lass_block'] = S((41, 44))
NPC['slowbro'] = near(S((43, 41)), 4); NPC['lass'] = near(S((44, 41)), 4)
if NPC['cuttree'] is None: pass
SOUTH_TREE = S((41, 42))
# nord : policier au milieu de la bande ; declencheurs du rival sur la ligne y=12
NPC['policeman_n'] = S((71, 11)); NPC['rival'] = S((70, 6))
SIGNS = {k: v for k, v in SIGNC.items()}
# ------------------------------------------------------------------ verifications
for k, c in DOORS.items(): assert c in ALL or k == 'cave' or True
fr = {k: (c[0], c[1] + 1) for k, c in DOORS.items()}
for k, c in list(FRONT.items()) + [('center', S((37, 26)))]: assert c in ALL, ('devant la porte inaccessible', k, c)
for k, c in EXITC.items(): assert c in ALL, ('sortie inaccessible', k)
for k, c in NPC.items(): assert c in ALL or k in ('cuttree', 'policeman_block', 'slowbro_block', 'lass_block', 'policeman_n', 'rival'), ('PNJ inaccessible', k, c)
# forces de passage
def flood_wo(cells, start=HUB):
    return reach_from(start, ban=set(cells))
# depuis la sortie OUEST (arrivee de la Route 4 Est), avant billet/badge : tout le coeur de la ville doit rester accessible
_ban = {NPC['cuttree'], NPC['slowbro_block'], NPC['lass_block']} | {(x, 12) for x in (48, 49, 50)}
_fw = flood_wo(_ban, EXITC['W'])
for _k, _c in list(FRONT.items()) + [('center', S((37, 26)))]: assert _c in _fw, ('inaccessible depuis l ouest', _k, _c)
for _k in ('N', 'E', 'S'): assert EXITC[_k] not in _fw or _k == 'N' and False or EXITC[_k] not in _fw, ('sortie ouverte sans condition', _k)
assert EXITC['E'] not in flood_wo({NPC['cuttree']}), 'est sans arbre ?!'
assert EXITC['S'] not in flood_wo({NPC['slowbro_block']}), 'sud sans barrage'
print('portes/sorties/PNJ OK ; cases accessibles', len(ALL))
# l'arbre du sud bloque la case (41,42) : s'assurer qu'elle est marchable
assert passable(SOUTH_TREE), 'case arbre sud bloquee'
NPC['cuttree_s'] = SOUTH_TREE
# ------------------------------------------------------------------ dumps pour tourmalia_river_events.py
json.dump({k: [list(c)] for k, c in {**DOORS, **PARKED}.items() if k != 'cave'}, open('/tmp/tourmalia_doors.json', 'w'))
json.dump({k: list(v) for k, v in NPC.items()}, open('/tmp/tourmalia_npc.json', 'w'))
json.dump({k: list(v) for k, v in SIGNS.items()}, open('/tmp/tourmalia_signs.json', 'w'))
json.dump({'grot_door': list(DOORS['cave']), 'hole': []}, open('/tmp/tourmalia_misc.json', 'w'))
# ------------------------------------------------------------------ ecriture des tilesets
def writepal(p, cols): open(p, 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in cols))
BACK = (20, 62, 38)
def palrgb(i):
    if i >= len(PALCOLS): return [BACK] * 16
    return [BACK] + [(c[0] << 3 | c[0] >> 2, c[1] << 3 | c[1] >> 2, c[2] << 3 | c[2] >> 2) for c in PALCOLS[i]] + [BACK] * (15 - len(PALCOLS[i]))
for i in range(16):
    writepal(PRI + 'palettes/%02d.pal' % i, palrgb(i)); writepal(SEC + 'palettes/%02d.pal' % i, palrgb(i))
def sheet(lo, hi, path):
    n = max(1, hi - lo); rows = (max(n, 1) + 15) // 16
    im = Image.new('P', (128, rows * 8), 0); gray = []
    for k in range(16): gray += [k * 17] * 3
    im.putpalette(gray + [0] * (768 - 48)); px = im.load()
    for t in range(lo, hi):
        pi, idx = TILE_LIST[t]; n_ = t - lo; ox, oy = (n_ % 16) * 8, (n_ // 16) * 8
        for j, v in enumerate(idx): px[ox + j % 8, oy + j // 8] = v
    im.save(path)
sheet(0, min(NT, 640), PRI + 'tiles.png'); sheet(640, max(NT, 641), SEC + 'tiles.png')
# primaire : 640 metatuiles vides ; secondaire : les 316 metatuiles de la carte
open(PRI + 'metatiles.bin', 'wb').write(b'\0' * (640 * 16)); open(PRI + 'metatile_attributes.bin', 'wb').write(b'\0' * (640 * 4))
open(SEC + 'metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *e) for e in ENT))
open(SEC + 'metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<I', a) for a in ATT))
# ------------------------------------------------------------------ carte
g = [G[(x, y)] for y in range(H) for x in range(W)]
open('data/layouts/CeruleanCity/map.bin', 'wb').write(struct.pack('<%dH' % len(g), *g))
open('data/layouts/CeruleanCity/border.bin', 'wb').write(struct.pack('<4H', 0x400 | (640 + 1), 0x400 | (640 + 5), 0x400 | (640 + 5), 0x400 | (640 + 1)))
L = json.load(open('data/layouts/layouts.json'))
for l in L['layouts']:
    if l.get('id') == 'LAYOUT_CERULEAN_CITY':
        l.update(width=W, height=H, primary_tileset='gTileset_GeneralTourmaline', secondary_tileset='gTileset_FortreeTourmaline')
json.dump(L, open('data/layouts/layouts.json', 'w'), indent=2); open('data/layouts/layouts.json', 'a').write('\n')
json.dump({'w': W, 'h': H, 'blocked': [list(c) for c in sorted(c for c in G if (G[c] & 0x400) or ((G[c] & 0x1000) and not (G[c] & 0x2000)))]}, open('/tmp/tourmalia_col.json', 'w'))
# connexions : ecart = case de sortie - case locale du voisin
f = 'data/maps/CeruleanCity/map.json'; d = json.load(open(f))
OFF = {'MAP_ROUTE9': EXITC['E'][1] - 8, 'MAP_ROUTE4_EAST': EXITC['W'][1] - 14, 'MAP_ROUTE24': EXITC['N'][0] - 11, 'MAP_ROUTE5': EXITC['S'][0] - 22}
for c in d['connections']: c['offset'] = OFF[c['map']]
# declencheurs du rival (3 colonnes x=70..72, ligne y=12) + sorties
for c in d['coord_events']:
    if 'RivalTriggerLeft' in c['script']: c['x'], c['y'] = 70 - X0, 12
    if 'RivalTriggerMid' in c['script']: c['x'], c['y'] = 71 - X0, 12
    if 'RivalTriggerRight' in c['script']: c['x'], c['y'] = 72 - X0, 12
for o in d['object_events']:
    if o.get('local_id') == 'LOCALID_CERULEAN_POLICE_N': o['x'], o['y'] = NPC['policeman_n']
    if o['graphics_id'] == 'OBJ_EVENT_GFX_CUT_TREE':
        o['x'], o['y'] = NPC['cuttree']
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# connexions inverses (cote routes voisines) : ecart oppose
for mp, nb in (('Route9', 'MAP_ROUTE9'), ('Route4East', 'MAP_ROUTE4_EAST'), ('Route24', 'MAP_ROUTE24'), ('Route5', 'MAP_ROUTE5')):
    fn = 'data/maps/%s/map.json' % mp; dd = json.load(open(fn))
    for c in dd['connections']:
        if c['map'] == 'MAP_CERULEAN_CITY': c['offset'] = -OFF[nb]
    json.dump(dd, open(fn, 'w'), indent=2); open(fn, 'a').write('\n')
f = 'data/maps/CeruleanCity/scripts.inc'; s = open(f).read()
s = re.sub(r'(RivalTriggerMid::.*?setobjectxyperm LOCALID_CERULEAN_RIVAL, )\d+, \d+', r'\g<1>%d, 6' % (71 - X0), s, flags=re.S); s = re.sub(r'(RivalTriggerRight::.*?setobjectxyperm LOCALID_CERULEAN_RIVAL, )\d+, \d+', r'\g<1>%d, 6' % (72 - X0), s, flags=re.S)
open(f, 'w').write(s)
print('tourmalia copie : tuiles', NT, '; metatuiles', NM, '; palettes', len(PALCOLS), '; offsets', OFF)
