#!/usr/bin/env python3
"""Arene d'ACHLYS (Amethiolite/Parmanie, POISON) redessinee : laboratoire-grotte aux bassins toxiques, sentier en S entre deux grands bassins,
estrade sous une fresque de goutte. Ecrase gym_fortree_sec + layout GymEmFortree. Idempotent."""
import sys, math, json, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gym_art import *
P7 = Pal('kabcdegGhpPnmwy', [(24, 14, 34), (48, 34, 68), (72, 54, 96), (100, 78, 128), (132, 108, 158), (176, 152, 198), (34, 104, 52), (84, 186, 62), (170, 240, 92), (140, 56, 168), (206, 118, 218), (60, 90, 58), (92, 126, 68), (232, 232, 208), (232, 208, 72)])
ts = TS({7: P7, 8: P7})
def floor(seed, stain=False):
    s = Spr('c'); s.rect(0, 15, 15, 15, 'b'); s.rect(15, 0, 15, 15, 'b'); s.rect(0, 0, 14, 0, 'd'); s.rect(0, 0, 0, 14, 'd')
    s.noise(['b', 'd', 'b'], 0.07, seed, only=['c'])
    if stain:
        r = random.Random(seed)
        for _ in range(9): s.px(r.randint(3, 12), r.randint(3, 12), 'g')
        for _ in range(3): s.px(r.randint(3, 12), r.randint(3, 12), 'G')
    return s
def goo(seed=0):
    s = Spr('g')
    for y in range(16):
        for x in range(16):
            v = math.sin(2 * math.pi * (x / 16 + 0.2 * math.sin(2 * math.pi * y / 16))) + math.sin(2 * math.pi * (y / 16 + 0.15 * math.sin(2 * math.pi * x / 8)))
            s.g[y][x] = 'g' if v < 0.1 else ('G' if v < 1.5 else 'h')
    for x, y in ((3, 4), (11, 11), (7, 14)): s.px(x, y, 'w')
    for x, y in ((12, 3), (4, 10)): s.px(x, y, 'P')
    return s
_pool = {}
def pool(t, b, l, r):
    s = goo()
    if t: s.rect(0, 0, 15, 2, 'c'); s.rect(0, 0, 15, 0, 'd'); s.rect(0, 2, 15, 2, 'k'); s.rect(0, 3, 15, 3, 'a')
    if b: s.rect(0, 13, 15, 15, 'c'); s.rect(0, 13, 15, 13, 'k'); s.rect(0, 14, 15, 14, 'd'); s.rect(0, 15, 15, 15, 'b'); s.rect(0, 12, 15, 12, 'a')
    if l: s.rect(0, 0, 2, 15, 'c'); s.rect(2, 0, 2, 15, 'k'); s.rect(0, 0, 0, 15, 'd'); s.rect(3, 0, 3, 15, 'a')
    if r: s.rect(13, 0, 15, 15, 'c'); s.rect(13, 0, 13, 15, 'k'); s.rect(15, 0, 15, 15, 'b'); s.rect(12, 0, 12, 15, 'a')
    return s
def wall_cap():
    s = Spr('a'); s.rect(0, 0, 15, 0, 'b'); s.rect(0, 15, 15, 15, 'k'); s.rect(0, 14, 15, 14, 'b')
    s.noise(['b', 'k'], 0.1, 3, only=['a'])
    for x in (2, 7, 12): s.rect(x, 1, x, 1 + (x % 3), 'k')
    return s
def wall_face(drip, seed):
    s = Spr('b'); s.rect(0, 0, 15, 0, 'e'); s.rect(0, 1, 15, 1, 'd'); s.rect(0, 15, 15, 15, 'k'); s.rect(0, 14, 15, 14, 'a')
    for y in (5, 10): s.rect(0, y, 15, y, 'a')
    for y, off in ((2, 4), (6, 0), (11, 8)): s.rect(off, y, off, y + 3, 'a')
    s.noise(['a', 'c'], 0.1, seed, only=['b'])
    if drip:
        for x, L in ((3, 9), (9, 6), (13, 11)):
            for y in range(2, 2 + L): s.px(x, y, 'G')
            s.px(x, 2 + L, 'h')
            for y in range(2, 2 + L // 2): s.px(x - 1, y, 'g')
    return s
def side(left, seed):
    s = wall_face(False, seed); s.rect(0, 0, 15, 1, 'b'); s.rect(0, 14, 15, 14, 'b'); s.rect(0, 15, 15, 15, 'a')
    for y in range(16):
        for x in range(16):
            if s.g[y][x] in 'ed': s.g[y][x] = 'c'
    e = 15 if left else 0; s.rect(e, 0, e, 15, 'k'); i = 14 if left else 1; s.rect(i, 0, i, 15, 'd')
    for y in (4, 5, 6, 7, 8): s.px(i + (-1 if left else 1), y, 'g')
    return s
def dais(emblem=False, step=False):
    s = Spr('a')
    s.rect(0, 0, 15, 0, 'p'); s.rect(0, 0, 0, 15, 'p'); s.rect(0, 15, 15, 15, 'k'); s.rect(15, 0, 15, 15, 'k'); s.rect(1, 1, 14, 1, 'b'); s.rect(1, 1, 1, 14, 'b')
    s.noise(['b', 'c', 'b'], 0.1, 31, only=['a'])
    for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)): s.px(x, y, 'G')
    if step:
        s = Spr('c'); s.rect(0, 0, 15, 3, 'e'); s.rect(0, 4, 15, 4, 'k'); s.rect(0, 5, 15, 8, 'd'); s.rect(0, 9, 15, 9, 'k'); s.rect(0, 10, 15, 13, 'c'); s.rect(0, 14, 15, 14, 'k'); s.rect(0, 15, 15, 15, 'b')
        s.noise(['d', 'e'], 0.08, 4, only=['c'])
    if emblem:
        for a in range(0, 360, 5):
            x = 8 + 5.6 * math.cos(math.radians(a)); y = 8 + 5.6 * math.sin(math.radians(a)); s.px(int(round(x)), int(round(y)), 'P')
        for a in range(0, 360, 10):
            x = 8 + 4.6 * math.cos(math.radians(a)); y = 8 + 4.6 * math.sin(math.radians(a)); s.px(int(round(x)), int(round(y)), 'p')
        for pt in ((8, 3), (8, 4), (7, 5), (9, 5), (7, 6), (8, 6), (9, 6), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (7, 9), (8, 9), (9, 9)): s.px(pt[0], pt[1], 'G')
        for pt in ((7, 7), (7, 8), (8, 6)): s.px(pt[0], pt[1], 'h')
        s.px(7, 6, 'w')
    return s
def on_floor(rows, seed):
    f = floor(seed); f.over(Spr.parse(rows)); return f
CAULD = ['................', '................', '...h..G.h.......', '..G.hG..G.h.....', '..kGGhGGhGGk....', '.kkGGGGGGGGkk...', '.kdkkkkkkkkdk...', '.kcdddddddddck..', '.kccccccccccck..', '.kcbccccccbcck..', '..kkbbbbbbbkk...', '...kk.kk.kk.....', '...kk.kk.kk.....', '................', '................', '................']
CAULD = [r[:16].ljust(16, '.') for r in CAULD]
STATUE = ['................', '......kkkk......', '.....kwwwwk.....', '.....kwkkwk.....', '.....kwwwwk.....', '......kwwk......', '.....kkGGkk.....', '....kGGhhGGk....', '....kGhGGhGk....', '.....kGGGGk.....', '..kkkkkkkkkkkk..', '..kdddddddddck..', '..kccppPPcccbk..', '..kbbbbbbbbbbk..', '..kkkkkkkkkkkk..', '................']
PIL_T = ['................', '...kkkkkkkkkk...', '..kddddddddddk..', '..kccccccccccck.', '...kkcceeccckk..', '....kccbbcck....', '....kccGbcck....', '....kccGbcck....', '....kccgbcck....', '....kccbbcck....', '....kccbbcck....', '....kccbbcck....', '....kccbbcck....', '....kccbbcck....', '....kccbbcck....', '....kccbbcck....']
PIL_T = [r[:16].ljust(16, '.') for r in PIL_T]
PIL_B = ['....kccbbcck....'] * 10 + ['...kkccbbcckk...', '..kddddddddddk..', '..kkkkkkkkkkkk..', '................', '................', '................']
MAT = ['kkkkkkkkkkkkkkkk'] + ['ke' + 'g' * 12 + 'ek'] * 14 + ['kkkkkkkkkkkkkkkk']
MAT = ['kkkkkkkkkkkkkkkk', 'kppppppppppppppk'] + ['kp' + 'c' * 12 + 'pk'] * 12 + ['kppppppppppppppk', 'kkkkkkkkkkkkkkkk']
def mural():
    W3 = 48; g = [['b'] * W3 for _ in range(32)]
    rr = random.Random(8)
    for y in range(32):
        for x in range(W3):
            if y < 16: g[y][x] = 'a'
            if y == 0: g[y][x] = 'b'
            elif y == 15: g[y][x] = 'b'
            elif y == 16: g[y][x] = 'e'
            elif y == 17: g[y][x] = 'd'
            elif y == 31: g[y][x] = 'k'
            elif y == 30: g[y][x] = 'a'
            elif rr.random() < 0.08: g[y][x] = 'a' if y > 17 else 'b'
    for y in range(4, 29):
        for x in range(8, 40):
            dx = (x - 24) / 16.0; dy = (y - 16) / 12.5
            d = dx * dx + dy * dy
            if d < 1.0: g[y][x] = 'g'
            elif d < 1.12: g[y][x] = 'P' if d < 1.06 else 'p'
    # goutte toxique
    for y in range(7, 27):
        t = (y - 7) / 19.0
        hw = int(1 + 8 * math.sin(min(1.0, t * 1.15) * math.pi / 2.1) ** 1.2) if t < 0.9 else 3
        if y > 20: hw = int(9 * math.sqrt(max(0.0, 1 - ((y - 20) / 7.0) ** 2)))
        for x in range(24 - hw, 24 + hw): g[y][x] = 'G'
        for x in range(24 - hw + 2, 24 + hw - 2): g[y][x] = 'h' if y > 15 else 'G'
    for y in range(17, 23):
        g[y][19] = 'w'
        if y < 20: g[y][20] = 'w'
    for (x, y) in ((12, 22), (35, 20), (13, 12), (36, 11), (33, 25), (15, 25)):
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)): g[y + dy][x + dx] = 'h'
        g[y][x] = 'w'
    out = []
    for k in range(3):
        for r in range(2):
            sp = Spr()
            for y in range(16):
                for x in range(16): sp.g[y][x] = g[r * 16 + y][k * 16 + x]
            out.append(sp)
    return out
ts.add('f1', floor(1), 7); ts.add('f2', floor(2), 7); ts.add('f3', floor(3), 7); ts.add('fs', floor(4, True), 7); ts.add('fs2', floor(5, True), 7)
LEG = {'#': 'black', 'T': 'cap', 'F': 'w1', 'G': 'wd', 'H': 'w2', 'L': 'sl', 'Z': 'sr', 'f': 'f1', 'h': 'f2', 'i': 'f3', 'g': 'fs', 'j': 'fs2', 'D': 'da', 'E': 'de', 's': 'ds',
       'C': 'cauld', 'p': 'pt', 'q': 'pb', 'S': 'statue', 'm': 'mat', '1': 'mu10', '2': 'mu20', '3': 'mu30', '4': 'mu11', '5': 'mu21', '6': 'mu31'}
ts.add('w1', wall_face(False, 1), 7); ts.add('wd', wall_face(True, 3), 7); ts.add('w2', wall_face(False, 7), 7); ts.add('cap', wall_cap(), 7)
ts.add('sl', side(True, 2), 7); ts.add('sr', side(False, 4), 7)
ts.add('da', dais(), 7); ts.add('de', dais(True), 7); ts.add('ds', dais(step=True), 7)
ts.add('cauld', on_floor(CAULD, 21), 7); ts.add('statue', on_floor(STATUE, 24), 7)
ts.add('pt', on_floor(PIL_T, 22), 7); ts.add('pb', on_floor(PIL_B, 23), 7)
ts.add('mat', Spr.parse(MAT), 7, beh=0x65)
for k, sp in enumerate(mural()): ts.add('mu%d%d' % (k // 2 + 1, k % 2), sp, 7)
W, H = 20, 25
POOLS = [(2, 8, 13, 11), (6, 14, 17, 17), (3, 20, 5, 21), (14, 20, 16, 21)]
def pooled():
    s = set()
    for x0, y0, x1, y1 in POOLS:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.add((x, y))
    return s
def build():
    PS = pooled()
    g = [['f'] * W for _ in range(H)]
    rr = random.Random(5)
    for y in range(H):
        for x in range(W): g[y][x] = '#'
    for y in range(3, H - 1):
        for x in range(2, W - 2): g[y][x] = rr.choice('fffffhhij' if rr.random() < 0.06 else 'fffffhhi')
    for x in range(1, W - 1):
        g[1][x] = 'T'; g[2][x] = 'FFHFGFFHFFFFGFHFFFF'[x - 1] if x - 1 < 19 else 'F'
        g[H - 1][x] = 'T'
    for y in range(2, H - 1): g[y][1] = 'L'; g[y][W - 2] = 'Z'
    def put(x, y, c): g[y][x] = c
    for x in range(7, 12):
        for y in (3, 4): put(x, y, 'D')
        if x in (8, 9, 10): put(x, 5, 's')
    put(9, 4, 'E')
    for k, x in enumerate((8, 9, 10)): put(x, 1, '123'[k]); put(x, 2, '456'[k])
    for x in (3, 15): put(x, 3, 'p'); put(x, 4, 'q')
    put(16, 7, 'C'); put(3, 7, 'C'); put(2, 13, 'C'); put(17, 13, 'C'); put(11, 18, 'C')
    put(6, H - 2, 'S'); put(12, H - 2, 'S'); put(8, H - 1, 'm'); put(9, H - 1, 'm')
    return [''.join(r) for r in g], PS
ROWS, PS = build()
def pooltile(x, y):
    return 'pool%d%d%d%d' % tuple(int((x + dx, y + dy) not in PS) for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)))
for (x, y) in PS:
    n = pooltile(x, y)
    if n not in ts.names:
        flags = [int(c) for c in n[4:]]
        ts.add(n, pool(*flags), 7)
def grid():
    out = [list(r) for r in ROWS]
    return out
LEG2 = dict(LEG)
for (x, y) in PS: LEG2['~' + pooltile(x, y)[4:]] = pooltile(x, y)
def rows_for_map():
    # on encode les bassins par un caractere propre a chaque variante
    chars = {}
    base = 0x100
    g = [list(r) for r in ROWS]
    leg = dict(LEG)
    block = set('#TFGHLZCpqS123456')
    for (x, y) in PS:
        n = pooltile(x, y)
        if n not in chars: chars[n] = chr(0x100 + len(chars)); leg[chars[n]] = n; block.add(chars[n])
        g[y][x] = chars[n]
    return [''.join(r) for r in g], leg, block
RR, LEGF, BLOCK = rows_for_map()
if __name__ == '__main__':
    for r in RR: assert len(r) == W, (len(r), r)
    assert len(RR) == H
    preview(ts, RR, LEGF, '/tmp/gx/toxic_gym.png', scale=2)
    if '--write' in sys.argv:
        ts.write('gym_fortree_sec')
        words = build_map(ts, RR, LEGF, BLOCK)
        write_layout('GymEmFortree', W, H, words, ts.id('black'))
        lj = json.load(open(ROOT + '/data/layouts/layouts.json'))
        for l in lj['layouts']:
            if l.get('id') == 'LAYOUT_GYM_EM_FORTREE': l['width'], l['height'] = W, H
        json.dump(lj, open(ROOT + '/data/layouts/layouts.json', 'w'), indent=2); open(ROOT + '/data/layouts/layouts.json', 'a').write('\n')
        os.chdir(ROOT); from gym_lib import apply_gym
        apply_gym('FuchsiaCity_Gym', 'LAYOUT_GYM_EM_FORTREE',
                  objs={0: (3, 15, 'FACE_DOWN', 3), 1: (16, 9, 'FACE_DOWN', 3), 2: (12, 19, 'FACE_LEFT', 3), 3: (13, 6, 'FACE_LEFT', 3), 4: (3, 12, 'FACE_RIGHT', 3), 5: (6, 4, 'FACE_RIGHT', 3), 6: (9, 3, 'FACE_DOWN'), 7: (15, 22, 'FACE_DOWN')},
                  warps=[(8, 24), (9, 24), (9, 24)], bg=[(6, 23), (12, 23)])
