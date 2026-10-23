#!/usr/bin/env python3
"""Arene de HERA (Apatia, VOL / DRAGON-FEE) redessinee de A a Z : terrasse de marbre suspendue dans le ciel, deux gouffres de ciel a franchir
sur des ponts a rambardes dorees, estrade sous une fresque d'ailes. Ecrase gym_mauville_sec + layout GymEmMauville. Idempotent."""
import sys, math, json, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gym_art import *
P7 = Pal('kSsqWcmlvgGpPtT', [(52, 44, 84), (190, 226, 250), (136, 190, 238), (92, 156, 224), (252, 252, 255), (206, 224, 244), (232, 232, 246), (208, 200, 238), (168, 160, 208), (236, 188, 70), (164, 116, 36), (244, 176, 204), (122, 98, 172), (98, 204, 198), (52, 140, 150)])
ts = TS({7: P7, 8: P7})
def sky(seed, puffs=0):
    s = Spr('S'); r = random.Random(seed)
    s.noise(['c', 'W'], 0.02, seed, only=['S'])
    for _ in range(puffs):
        cx, cy = r.randint(3, 12), r.randint(4, 11)
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, -1), (1, -1), (2, 0), (-2, 0), (0, 1)):
            s.px(cx + dx, cy + dy, 'W')
        for dx in (-2, -1, 0, 1, 2): s.px(cx + dx, cy + 1, 'c')
    return s
def marble(alt, seed, inlay=False):
    base, edge = ('m', 'l') if not alt else ('l', 'm')
    s = Spr(base); s.rect(0, 15, 15, 15, 'v'); s.rect(15, 0, 15, 15, 'v'); s.rect(0, 0, 14, 0, 'W'); s.rect(0, 0, 0, 14, 'W')
    s.noise(['W', 'c'] if not alt else ['m', 'v'], 0.05, seed, only=[base])
    if inlay:
        for (x, y) in ((8, 4), (7, 5), (9, 5), (6, 6), (10, 6), (7, 7), (9, 7), (8, 8), (7, 9), (9, 9), (6, 10), (10, 10), (7, 11), (9, 11), (8, 12)):
            pass
        for (x, y) in ((8, 5), (7, 6), (9, 6), (8, 7), (6, 8), (10, 8), (7, 9), (9, 9), (8, 10)): s.px(x, y, 'g')
        s.px(8, 8, 'G')
    return s
def chasm_top():
    s = sky(1); s.rect(0, 0, 15, 9, 'm'); s.rect(0, 0, 15, 0, 'W'); s.rect(0, 9, 15, 9, 'k'); s.rect(0, 10, 15, 10, 'g'); s.rect(0, 11, 15, 11, 'G'); s.rect(0, 12, 15, 12, 'k')
    s.noise(['W', 'v'], 0.05, 3, only=['m']); s.rect(0, 13, 15, 13, 'c'); return s
def chasm_bot():
    s = sky(2); s.rect(0, 6, 15, 15, 'm'); s.rect(0, 5, 15, 5, 'k'); s.rect(0, 4, 15, 4, 'g'); s.rect(0, 3, 15, 3, 'G'); s.rect(0, 2, 15, 2, 'k'); s.rect(0, 6, 15, 6, 'v')
    s.noise(['W', 'v'], 0.05, 4, only=['m']); return s
def chasm_mid():
    return sky(5, 1)
def bridge():
    s = sky(6)
    s.rect(2, 0, 13, 15, 'm'); s.rect(1, 0, 1, 15, 'k'); s.rect(14, 0, 14, 15, 'k'); s.rect(2, 0, 2, 15, 'g'); s.rect(13, 0, 13, 15, 'g'); s.rect(3, 0, 3, 15, 'G'); s.rect(12, 0, 12, 15, 'G')
    for y in (4, 9, 14): s.rect(4, y, 11, y, 'v')
    s.noise(['W', 'l'], 0.06, 7, only=['m'])
    for y in (0, 7, 15): s.px(2, y, 'W'); s.px(13, y, 'W')
    return s
def rail(left):
    s = Spr('m')
    s.rect(0, 15, 15, 15, 'v'); s.rect(0, 0, 15, 0, 'W')
    s.noise(['W', 'c'], 0.05, 9 if left else 10, only=['m'])
    a, b = (0, 5) if left else (10, 15)
    for y in range(16):
        for x in range(a, b + 1): s.px(x, y, 'S')
    e = 6 if left else 9
    s.rect(e, 0, e, 15, 'k'); s.rect(e + (1 if left else -1), 0, e + (1 if left else -1), 15, 'g')
    pe = 5 if left else 10
    for y in (2, 7, 12): s.rect(pe - (1 if left else -1), y, pe, y + 2, 'G')
    s.noise(['c', 'W'], 0.03, 11, only=['S'])
    return s
def wall_top():
    s = Spr('v'); s.rect(0, 0, 15, 0, 'k'); s.rect(0, 1, 15, 1, 'W'); s.rect(0, 2, 15, 3, 'l'); s.rect(0, 13, 15, 13, 'g'); s.rect(0, 14, 15, 14, 'G'); s.rect(0, 15, 15, 15, 'k')
    for x in (3, 11): s.rect(x, 4, x + 1, 12, 'm')
    s.noise(['W', 'm'], 0.05, 12, only=['v']); return s
def wall_face(kind, seed):
    s = Spr('l'); s.rect(0, 0, 15, 0, 'g'); s.rect(0, 1, 15, 1, 'G'); s.rect(0, 15, 15, 15, 'k'); s.rect(0, 14, 15, 14, 'v')
    s.noise(['m', 'v'], 0.06, seed, only=['l'])
    if kind == 'arch':
        for y in range(3, 14):
            hw = 5 if y > 6 else (2 + (y - 3))
            for x in range(8 - hw, 8 + hw): s.px(x, y, 'S' if y < 11 else 's')
        for y in range(3, 14):
            hw = 5 if y > 6 else (2 + (y - 3))
            s.px(8 - hw - 1, y, 'k'); s.px(8 + hw, y, 'k')
        s.rect(5, 13, 10, 13, 'k')
        s.noise(['W', 'c'], 0.06, 13, only=['S'])
    if kind == 'col':
        s.rect(6, 2, 9, 13, 'm'); s.rect(6, 2, 6, 13, 'W'); s.rect(9, 2, 9, 13, 'v'); s.rect(5, 2, 10, 3, 'g'); s.rect(5, 12, 10, 13, 'g')
    return s
def ledge():
    s = Spr('m'); s.rect(0, 0, 15, 0, 'W'); s.rect(0, 10, 15, 10, 'k'); s.rect(0, 11, 15, 12, 'g'); s.rect(0, 13, 15, 13, 'G'); s.rect(0, 14, 15, 14, 'k'); 
    for y in (15,): s.rect(0, y, 15, y, 'S')
    s.noise(['W', 'v'], 0.05, 14, only=['m']); return s
def dais(emblem=False, step=False):
    s = Spr('p'); s.rect(0, 0, 15, 0, 'W'); s.rect(0, 0, 0, 15, 'W'); s.rect(0, 15, 15, 15, 'P'); s.rect(15, 0, 15, 15, 'P'); s.rect(1, 1, 14, 1, 'l'); s.rect(1, 1, 1, 14, 'l')
    s.noise(['l', 'W'], 0.08, 15, only=['p'])
    if step:
        s = Spr('m'); s.rect(0, 0, 15, 3, 'W'); s.rect(0, 4, 15, 4, 'k'); s.rect(0, 5, 15, 8, 'm'); s.rect(0, 9, 15, 9, 'k'); s.rect(0, 10, 15, 13, 'l'); s.rect(0, 14, 15, 14, 'k'); s.rect(0, 15, 15, 15, 'v')
    if emblem:
        for a in range(0, 360, 6):
            x = 8 + 5.6 * math.cos(math.radians(a)); y = 8 + 5.6 * math.sin(math.radians(a)); s.px(int(round(x)), int(round(y)), 'g')
        wing = [(7, 4), (6, 5), (5, 6), (4, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 11)]
        for x, y in wing: s.px(x, y, 'T'); s.px(15 - x, y, 'T')
        for x, y in ((6, 6), (6, 8), (7, 9), (7, 7), (5, 8)): s.px(x, y, 't'); s.px(15 - x, y, 't')
        s.px(7, 8, 'g'); s.px(8, 8, 'g'); s.px(7, 7, 'W'); s.px(8, 7, 'W')
    return s
STATUE = ['................', '.....kk..kk.....', '....kttkktk.....', '...kttTttTtk....', '...kttkttktk....', '....ktttttk.....', '.....kktkk......', '....kmmmmmmk....', '...kmWmmmmvk....', '...kmmmmmmvk....', '..kkkkkkkkkkk...', '..kvvvvvvvvvvk..', '..kllggGGllllk..', '..kvvvvvvvvvvk..', '..kkkkkkkkkkkk..', '................']
PIL_T = ['................', '...kkkkkkkkkk...', '..kggggggggggk..', '..kGGGGGGGGGGk..', '...kmWmmmmvk....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....']
PIL_B = ['....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '....kmWmmvk.....', '...kgggggggk....', '..kGGGGGGGGGk...', '..kkkkkkkkkkk...', '................', '................', '................', '................', '................']
def on_floor(rows, seed):
    f = marble(False, seed); f.over(Spr.parse(rows)); return f
MAT = ['kkkkkkkkkkkkkkkk', 'kggggggggggggggk', 'kgppppppppppppgk', 'kgpppppppppppppk'.replace('p', 'p'), 'kgppppppppppppgk', 'kgppppPppppppppk', 'kgpppPpppppppppk', 'kgppppPppppppppk', 'kgppppppppppppgk', 'kgppppppppppppgk', 'kgppppppppppppgk', 'kgppppppppppppgk', 'kgppppppppppppgk', 'kgppppppppppppgk', 'kggggggggggggggk', 'kkkkkkkkkkkkkkkk']
MAT = ['kkkkkkkkkkkkkkkk'] + ['kg' + 'p' * 12 + 'gk'] * 14 + ['kkkkkkkkkkkkkkkk']
def mural():
    W3 = 48; g = [['l'] * W3 for _ in range(32)]
    rr = random.Random(21)
    for y in range(32):
        for x in range(W3):
            g[y][x] = 'v' if y < 16 else 'l'
            if y == 0: g[y][x] = 'k'
            elif y == 1: g[y][x] = 'W'
            elif y == 15: g[y][x] = 'g'
            elif y == 16: g[y][x] = 'g'
            elif y == 17: g[y][x] = 'G'
            elif y == 31: g[y][x] = 'k'
            elif y == 30: g[y][x] = 'v'
            elif rr.random() < 0.05: g[y][x] = 'm'
    # fond de ciel dans un cadre arrondi
    for y in range(4, 28):
        for x in range(6, 42):
            dx = (x - 24) / 18.0; dy = (y - 16) / 12.0
            if dx * dx + dy * dy < 1.0: g[y][x] = 'S' if y < 20 else 's'
    for y in range(3, 29):
        for x in range(5, 43):
            dx = (x - 24) / 19.0; dy = (y - 16) / 13.0
            if 1.0 <= dx * dx + dy * dy < 1.12: g[y][x] = 'g'
    # ailes : deux plumes etagees
    for side in (-1, 1):
        for k, (y, L) in enumerate(((10, 14), (13, 13), (16, 12), (19, 10), (22, 7))):
            for l in range(L):
                x = 24 + side * (3 + l)
                for t in range(3):
                    yy = y + t - (l // 5)
                    if 4 <= yy < 28: g[yy][x] = 'W' if t == 0 else ('t' if t == 1 else 'T')
    for y in range(12, 26):
        for x in (23, 24): g[y][x] = 'g' if y < 24 else 'G'
    g[11][23] = g[11][24] = 'g'
    out = []
    for k in range(3):
        for r in range(2):
            sp = Spr()
            for y in range(16):
                for x in range(16): sp.g[y][x] = g[r * 16 + y][k * 16 + x]
            out.append(sp)
    return out
for i, (nm, sp) in enumerate((('sk1', sky(1)), ('sk2', sky(2, 1)), ('sk3', sky(3, 1)), ('sk4', sky(4)))): ts.add(nm, sp, 7)
ts.add('m1', marble(False, 21), 7); ts.add('m2', marble(True, 22), 7); ts.add('m3', marble(False, 23, True), 7)
ts.add('ct', chasm_top(), 7); ts.add('cb', chasm_bot(), 7); ts.add('br', bridge(), 7)
ts.add('rl', rail(True), 7); ts.add('rr', rail(False), 7)
ts.add('wt', wall_top(), 7); ts.add('wf', wall_face('plain', 31), 7); ts.add('wa', wall_face('arch', 32), 7); ts.add('wc', wall_face('col', 33), 7)
ts.add('ledge', ledge(), 7)
ts.add('da', dais(), 7); ts.add('de', dais(True), 7); ts.add('ds', dais(step=True), 7)
ts.add('statue', on_floor(STATUE, 41), 7); ts.add('pt', on_floor(PIL_T, 42), 7); ts.add('pb', on_floor(PIL_B, 43), 7)
ts.add('mat', Spr.parse(MAT), 7, beh=0x65)
for k, sp in enumerate(mural()): ts.add('mu%d%d' % (k // 2 + 1, k % 2), sp, 7)
LEG = {'S': 'sk1', 's': 'sk2', 'z': 'sk3', 'y': 'sk4', 'a': 'm1', 'b': 'm2', 'c': 'm3', 'T': 'ct', 'B': 'cb', 'X': 'br', 'L': 'rl', 'R': 'rr', 't': 'wt', 'f': 'wf', 'A': 'wa', 'C': 'wc', 'e': 'ledge', 'D': 'da', 'E': 'de', 'p': 'ds', 'Q': 'statue', 'u': 'pt', 'v': 'pb', 'm': 'mat',
       '1': 'mu10', '2': 'mu20', '3': 'mu30', '4': 'mu11', '5': 'mu21', '6': 'mu31'}
BLOCK = set('SszyTBLRtfACeQuv123456')
W, H = 15, 23
def build():
    g = [['S'] * W for _ in range(H)]
    rr = random.Random(3)
    for y in range(H):
        for x in range(W): g[y][x] = rr.choice('SSSSSSsz' if rr.random() < 0.5 else 'SSSSSSSy')
    def put(x, y, c): g[y][x] = c
    for x in range(1, 14):
        put(x, 1, 't'); put(x, 2, rr.choice('fffAfCf'))
    for x in (2, 12): put(x, 2, 'C')
    put(1, 1, 't'); put(13, 1, 't')
    for y in range(3, H - 1):
        put(1, y, 'L'); put(13, y, 'R')
        for x in range(2, 13): put(x, y, 'a' if (x + y) % 2 == 0 else 'b')
    for x in range(1, 14): put(x, H - 1, 'e')
    # estrade
    for x in range(5, 10):
        for y in (3, 4, 5): put(x, y, 'D')
    put(7, 5, 'E')
    for x in (6, 7, 8): put(x, 6, 'p')
    # fresque d'ailes
    for k, x in enumerate((6, 7, 8)): put(x, 1, '123'[k]); put(x, 2, '456'[k])
    # gouffres
    for (y0, br) in ((9, 10), (15, 4)):
        for x in range(2, 13):
            put(x, y0, 'T'); put(x, y0 + 1, 'B')
        put(br, y0, 'X'); put(br, y0 + 1, 'X')
        for x in (1, 13): pass
    # marbre incruste + decor
    for (x, y) in ((3, 4), (11, 4), (7, 12), (3, 19), (11, 19), (7, 7)): put(x, y, 'c')
    for x in (3, 11): put(x, 3, 'u'); put(x, 4, 'v')
    put(7, 12, 'u'); put(7, 13, 'v')
    put(4, H - 2, 'Q'); put(10, H - 2, 'Q'); put(7, H - 1, 'm'); put(8, H - 1, 'm')
    return [''.join(r) for r in g]
ROWS = build()
if __name__ == '__main__':
    for r in ROWS: assert len(r) == W
    preview(ts, ROWS, LEG, '/tmp/gx/sky_gym.png', scale=2)
    if '--write' in sys.argv:
        ts.write('gym_mauville_sec')
        words = build_map(ts, ROWS, LEG, BLOCK)
        write_layout('GymEmMauville', W, H, words, ts.id('sk1'))
        lj = json.load(open(ROOT + '/data/layouts/layouts.json'))
        for l in lj['layouts']:
            if l.get('id') == 'LAYOUT_GYM_EM_MAUVILLE': l['width'], l['height'] = W, H
        json.dump(lj, open(ROOT + '/data/layouts/layouts.json', 'w'), indent=2); open(ROOT + '/data/layouts/layouts.json', 'a').write('\n')
        os.chdir(ROOT); from gym_lib import apply_gym
        apply_gym('VermilionCity_Gym', 'LAYOUT_GYM_EM_MAUVILLE',
                  objs={0: (7, 4, 'FACE_DOWN'), 1: (4, 7, 'FACE_RIGHT', 3), 2: (4, 12, 'FACE_DOWN', 3), 3: (6, 20, 'FACE_DOWN'), 4: (10, 13, 'FACE_UP', 3)},
                  warps=[(7, 22), (8, 22), (8, 22)], bg=[(4, 21), (10, 21)])
