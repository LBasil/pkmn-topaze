#!/usr/bin/env python3
"""Arene de KAY (Pyropia, FEU) redessinee de A a Z : caldeira de basalte, deux rivieres de lave a franchir sur des dalles, estrade du champion.
Tuiles dessinees en code (gym_art.py) ; ecrase gym_rustboro_sec + layout GymEmRustboro. Idempotent."""
import sys, math, json, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gym_art import *
P7 = Pal('kabcdeRroywnsNh'[:15], [(16, 10, 12), (34, 26, 30), (56, 42, 46), (82, 62, 64), (110, 84, 82), (144, 112, 104), (196, 52, 24), (118, 28, 18), (240, 116, 30), (255, 190, 60), (255, 236, 170), (30, 22, 36), (150, 120, 96), (92, 70, 104), (196, 176, 164)])
P8 = Pal('kbcdiIjuUVroywm', [(16, 10, 12), (56, 42, 46), (82, 62, 64), (110, 84, 82), (44, 44, 54), (82, 84, 98), (130, 134, 150), (122, 84, 24), (196, 142, 40), (246, 208, 96), (210, 50, 24), (248, 124, 28), (255, 204, 70), (255, 244, 214), (170, 30, 32)])
ts = TS({7: P7, 8: P8})
def floor(seed, k='k', a='b', b='c', c='d', glow=False):
    s = Spr(b)
    s.rect(0, 15, 15, 15, a); s.rect(15, 0, 15, 15, a); s.rect(0, 0, 14, 0, c); s.rect(0, 0, 0, 14, c)
    s.noise([a, c, a], 0.07, seed, only=[b])
    if glow:
        pts = [(2, 3), (3, 4), (4, 4), (5, 5), (6, 7), (7, 7), (8, 8), (9, 10), (10, 10), (11, 11), (12, 13)]
        R, o = ('R', 'o') if k == 'k' else ('r', 'o')
        for x, y in pts: s.px(x, y, 'r' if k == 'k' else 'r')
        for x, y in pts[::2]: s.px(x, y, 'R' if k == 'k' else 'o')
    return s
def lava(seed=0, y0=0, y1=16):
    s = Spr('r')
    for y in range(16):
        for x in range(16):
            v = math.sin(2 * math.pi * (x / 16 + 0.18 * math.sin(2 * math.pi * y / 16))) + math.sin(2 * math.pi * (y / 16 + 0.14 * math.sin(2 * math.pi * x / 16 * 2)))
            s.g[y][x] = 'r' if v < -0.9 else ('R' if v < 0.1 else ('o' if v < 1.1 else 'y'))
    for x, y in ((3, 5), (11, 12), (7, 1)): s.px(x, y, 'w')
    return s
def bank_top():
    s = lava(); s.rect(0, 0, 15, 4, 'c'); s.rect(0, 0, 15, 0, 'e'); s.rect(0, 1, 15, 2, 'd'); s.rect(0, 4, 15, 4, 'k'); s.rect(0, 5, 15, 5, 'r'); s.rect(0, 3, 15, 3, 'b')
    s.noise(['b', 'd'], 0.1, 5, only=['c', 'd']); return s
def bank_bot():
    s = lava(); s.rect(0, 11, 15, 15, 'c'); s.rect(0, 11, 15, 11, 'k'); s.rect(0, 12, 15, 12, 'e'); s.rect(0, 13, 15, 14, 'd'); s.rect(0, 15, 15, 15, 'b'); s.rect(0, 10, 15, 10, 'r')
    s.noise(['b', 'd'], 0.1, 6, only=['c', 'd']); return s
def bridge():
    s = lava()
    s.rect(2, 0, 13, 15, 'd'); s.rect(2, 0, 2, 15, 'k'); s.rect(13, 0, 13, 15, 'k'); s.rect(3, 0, 3, 15, 'e'); s.rect(12, 0, 12, 15, 'c')
    s.rect(4, 7, 11, 8, 'c'); s.rect(4, 7, 11, 7, 'e'); s.rect(3, 15, 12, 15, 'k')
    s.noise(['c', 'e'], 0.1, 9, only=['d']); s.rect(1, 0, 1, 15, 'r'); s.rect(14, 0, 14, 15, 'r'); return s
def wall_cap():
    s = Spr('a'); s.rect(0, 0, 15, 0, 'b'); s.rect(0, 15, 15, 15, 'k'); s.rect(0, 14, 15, 14, 'b')
    for x in (0, 8): s.rect(x, 1, x, 13, 'b')
    s.noise(['b', 'n'], 0.08, 3, only=['a']); return s
def wall_face(glow=False, seed=1):
    s = Spr('b'); s.rect(0, 0, 15, 0, 'e'); s.rect(0, 1, 15, 1, 'd'); s.rect(0, 15, 15, 15, 'k'); s.rect(0, 14, 15, 14, 'a')
    for y in (5, 10): s.rect(0, y, 15, y, 'a')
    for y, off in ((2, 4), (6, 0), (11, 8)):
        s.rect(off, y, off, y + 3, 'a')
    s.noise(['a', 'c'], 0.1, seed, only=['b'])
    if glow:
        for x, y in ((3, 3), (4, 4), (4, 5), (5, 6), (6, 7), (6, 8), (7, 9), (8, 10), (9, 11), (9, 12)):
            s.px(x, y, 'R')
        for x, y in ((4, 5), (6, 7), (8, 10)): s.px(x, y, 'o')
    return s
def side(left=True, seed=2):
    s = wall_face(False, seed); s.rect(0, 0, 15, 1, 'b'); s.rect(0, 14, 15, 14, 'b'); s.rect(0, 15, 15, 15, 'a')
    for y in range(16):
        for x in range(16): 
            if s.g[y][x] in 'ed': s.g[y][x] = 'c'
    e = 15 if left else 0; s.rect(e, 0, e, 15, 'k'); i = 14 if left else 1; s.rect(i, 0, i, 15, 'd'); return s
def dais(emblem=False):
    s = floor(11, 'k', 'c', 'd', 'e'); s.rect(0, 0, 15, 0, 'e'); s.rect(0, 0, 0, 15, 'e')
    if emblem:
        for a in range(0, 360, 6):
            x = 8 + 5.4 * math.cos(math.radians(a)); y = 8 + 5.4 * math.sin(math.radians(a)); s.px(int(round(x)), int(round(y)), 'R')
        for pt in ((8, 3), (7, 4), (9, 4), (8, 5), (8, 6), (7, 7), (9, 7), (8, 8), (7, 9), (9, 9), (8, 10), (8, 11)): s.px(pt[0], pt[1], 'o')
        for pt in ((8, 5), (8, 7), (8, 9)): s.px(pt[0], pt[1], 'y')
        s.px(8, 8, 'w')
    return s
def on_floor(sprite_rows, seed):
    f = floor(seed, 'k', 'b', 'c', 'd'); f.over(Spr.parse(sprite_rows)); return f
BRAZIER = ['................', '.......rr.......', '......rooy......', '.....royyyo.....', '.....royywo.....', '......ooyo......', '.....kkkkkk.....', '....kjjjjjjk....', '....kIIIIIIk....', '.....kIIIIk.....', '......kIIk......', '......kIIk......', '.....kiIIik.....', '....kiIIIIik....', '....kkkkkkkk....', '................']
PIL_TOP = ['................', '...kkkkkkkkkk...', '..kNNNNNNNNNNk..', '..knNNNNNNNnnk..', '...kknnNNnnkk...', '....knnNNnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....', '....knnNnnnk....']
STATUE = ['................', '.......kk.......', '......kjjk......', '.....kjIIjk.....', '.....kIkkIk.....', '....kjIIIIjk....', '....kIIiiIIk....', '....kIiyyiIk....', '.....kIiiIk.....', '....kjIIIIjk....', '...kIIIIIIIIk...', '..kkkkkkkkkkkk..', '..kjjjjjjjjjjk..', '..kIIUVUUIIIIk..', '..kiiiiiiiiiik..', '..kkkkkkkkkkkk..']
MAT = ['kkkkkkkkkkkkkkkk', 'kUUUUUUUUUUUUUUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUmmmmmmmmmmmmUk', 'kUUUUUUUUUUUUUUk', 'kkkkkkkkkkkkkkkk']
def pil_bot():
    r = list(PIL_TOP); r = r[:]; return ['....knnNnnnk....'] * 11 + ['...kknnNnnnkk...', '..kNNNNNNNNNNk..', '..kkkkkkkkkkkkk.', '................', '................'][:5]
ts.add('f1', floor(1), 7); ts.add('f2', floor(2), 7); ts.add('f3', floor(3), 7); ts.add('fg', floor(4, glow=True), 7)
ts.add('lava', lava(), 7); ts.add('bt', bank_top(), 7); ts.add('bb', bank_bot(), 7); ts.add('br', bridge(), 7)
ts.add('cap', wall_cap(), 7); ts.add('w1', wall_face(False, 1), 7); ts.add('w2', wall_face(False, 7), 7); ts.add('wg', wall_face(True, 3), 7)
ts.add('sl', side(True), 7); ts.add('sr', side(False), 7); ts.add('da', dais(), 7); ts.add('de', dais(True), 7)
ts.add('brazier', on_floor(BRAZIER, 21), 8); ts.add('pt', on_floor(PIL_TOP, 22), 8) if False else None
# colonnes d'obsidienne : lettres de P7 (n, N) -> palette 7 ; fond de sol en P7
def pillar(top):
    s = floor(23, 'k', 'b', 'c', 'd'); rows = PIL_TOP if top else ['....knnNnnnk....'] * 10 + ['...kknnNnnnkk...', '..kNNNNNNNNNNk..', '..kkkkkkkkkkkk..', '................', '................', '................']
    s.over(Spr.parse(rows)); return s
ts.add('pt', pillar(True), 7); ts.add('pb', pillar(False), 7)
ts.add('statue', on_floor(STATUE, 24), 8)
ts.add('mat', Spr.parse(MAT), 8, beh=0x65)
def floor_glow(top, seed):
    s = floor(seed)
    rows = (0, 1, 2) if top else (15, 14, 13)
    r = random.Random(seed)
    for k, y in enumerate(rows):
        for x in range(16):
            if r.random() < (0.45, 0.25, 0.1)[k]: s.px(x, y, 'r' if k < 2 else 'b')
    return s
def dais2(emblem=False, step=False):
    s = Spr('a')
    s.rect(0, 0, 15, 0, 'r'); s.rect(0, 0, 0, 15, 'r'); s.rect(0, 15, 15, 15, 'k'); s.rect(15, 0, 15, 15, 'k'); s.rect(1, 1, 14, 1, 'b'); s.rect(1, 1, 1, 14, 'b')
    s.noise(['b', 'n', 'b'], 0.08, 31, only=['a'])
    for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)): s.px(x, y, 'R')
    if step:
        s = Spr('c'); s.rect(0, 0, 15, 3, 'e'); s.rect(0, 4, 15, 4, 'k'); s.rect(0, 5, 15, 8, 'd'); s.rect(0, 9, 15, 9, 'k'); s.rect(0, 10, 15, 13, 'c'); s.rect(0, 14, 15, 14, 'k'); s.rect(0, 15, 15, 15, 'b')
        s.noise(['d', 'e'], 0.08, 4, only=['c'])
    if emblem:
        for a in range(0, 360, 5):
            x = 8 + 5.6 * math.cos(math.radians(a)); y = 8 + 5.6 * math.sin(math.radians(a)); s.px(int(round(x)), int(round(y)), 'R'); 
        for a in range(0, 360, 10):
            x = 8 + 4.6 * math.cos(math.radians(a)); y = 8 + 4.6 * math.sin(math.radians(a)); s.px(int(round(x)), int(round(y)), 'r')
        for pt in ((8, 3), (7, 4), (9, 4), (8, 4), (8, 5), (7, 6), (9, 6), (8, 6), (7, 7), (9, 7), (8, 7), (7, 8), (8, 8), (9, 8), (7, 9), (8, 9), (9, 9), (8, 10), (8, 11)): s.px(pt[0], pt[1], 'o')
        for pt in ((8, 6), (8, 7), (8, 8), (8, 9), (8, 5)): s.px(pt[0], pt[1], 'y')
        s.px(8, 8, 'w'); s.px(8, 9, 'w')
    return s
def mural():
    W3 = 48; g = [['b'] * W3 for _ in range(32)]
    import random as _r; rr = _r.Random(8)
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
    prof = [(3, 1), (4, 1), (5, 2), (6, 2), (7, 3), (8, 4), (9, 4), (10, 5), (11, 6), (12, 6), (13, 7), (14, 7), (15, 8), (16, 8), (17, 9), (18, 9), (19, 9), (20, 9), (21, 9), (22, 9), (23, 8), (24, 8), (25, 7), (26, 6), (27, 5), (28, 3)]
    for y, hw in prof:
        sh = (y - 3) // 6
        for x in range(24 - hw - (1 if y > 15 else 0), 24 + hw + 1):
            g[y][x] = 'R'
        inner = hw - 2
        if inner > 0:
            for x in range(24 - inner, 24 + inner): g[y][x] = 'o'
        core = hw - 5
        if core > 0:
            for x in range(24 - core, 24 + core - 1): g[y][x] = 'y'
    for y in range(18, 27): g[y][23] = 'w'; g[y][24] = 'w' if y > 20 else 'y'
    for y, x in ((9, 28), (10, 28), (11, 29), (12, 29), (13, 30)): g[y][x] = 'a'
    out = []
    for k in range(3):
        for r in range(2):
            sp = Spr()
            for y in range(16):
                for x in range(16): sp.g[y][x] = g[r * 16 + y][k * 16 + x]
            out.append(sp)
    return out
for k, sp in enumerate(mural()): ts.add('mu%d%d' % (k // 2 + 1, k % 2), sp, 7)
ts.add('ft', floor_glow(True, 41), 7); ts.add('fu', floor_glow(False, 42), 7)
ts.add('da2', dais2(), 7); ts.add('de2', dais2(True), 7); ts.add('ds', dais2(step=True), 7)
LEG = {'#': 'black', 'T': 'cap', '1': 'mu10', '2': 'mu20', '3': 'mu30', '4': 'mu11', '5': 'mu21', '6': 'mu31', 'F': 'w1', 'G': 'wg', 'H': 'w2', 'L': 'sl', 'Z': 'sr', 'f': 'f1', 'h': 'f2', 'i': 'f3', 'g': 'fg', 'A': 'bt', 'B': 'bb', 'X': 'br', 'D': 'da2', 'E': 'de2', 's': 'ds', 'u': 'fu', 't': 'ft', 'R': 'brazier', 'p': 'pt', 'q': 'pb', 'S': 'statue', 'm': 'mat'}
BLOCK = set('#TFGHLZABRpqS123456')
W, H = 17, 22
def build():
    g = [['f'] * W for _ in range(H)]
    for x in range(W): g[0][x] = 'T'; g[1][x] = 'FFHFGFFHFFFFGFHFF'[x]; g[H - 1][x] = 'T'
    for y in range(2, H - 1): g[y][0] = 'L'; g[y][W - 1] = 'Z'
    import random as _r; rr = _r.Random(5)
    for y in range(2, H - 1):
        for x in range(1, W - 1): g[y][x] = rr.choice('fffffhhi')
    def put(x, y, c): g[y][x] = c
    for x in range(6, 11):
        for y in (2, 3, 4): put(x, y, 'D')
        put(x, 5, 's') if x in (7, 8, 9) else None
    put(8, 4, 'E')
    for k, x in enumerate((7, 8, 9)): put(x, 0, '123'[k]); put(x, 1, '456'[k])
    for x in (3, 13): put(x, 2, 'R'); put(x, 15, 'R')
    for x in (5, 11): put(x, 3, 'p'); put(x, 4, 'q')
    for x in (4, 12): put(x, 9, 'p'); put(x, 10, 'q')
    for (y0, br) in ((6, (3, 13)), (12, (8, 9))):
        for x in range(1, W - 1):
            put(x, y0, 'A'); put(x, y0 + 1, 'B')
        for x in br: put(x, y0, 'X'); put(x, y0 + 1, 'X')
        for x in range(1, W - 1):
            put(x, y0 - 1, 'u') if g[y0 - 1][x] in 'fhi' else None
            put(x, y0 + 2, 't') if g[y0 + 2][x] in 'fhi' else None
    for x in (1, 15): put(x, 3, 'g')
    for (x, y) in ((2, 9), (14, 10), (5, 17), (12, 18), (9, 8)): put(x, y, 'g')
    put(4, H - 2, 'S'); put(11, H - 2, 'S'); put(7, H - 1, 'm'); put(8, H - 1, 'm')
    return [''.join(r) for r in g]
ROWS = build()
if __name__ == '__main__':
    for r in ROWS: assert len(r) == W, (len(r), r)
    assert len(ROWS) == H
    preview(ts, ROWS, LEG, '/tmp/gx/fire_gym.png', scale=2)
    if '--write' in sys.argv:
        ts.write('gym_rustboro_sec')
        words = build_map(ts, ROWS, LEG, BLOCK)
        write_layout('GymEmRustboro', W, H, words, ts.id('black'))
        lj = json.load(open(ROOT + '/data/layouts/layouts.json'))
        for l in lj['layouts']:
            if l.get('id') == 'LAYOUT_GYM_EM_RUSTBORO': l['width'], l['height'] = W, H
        json.dump(lj, open(ROOT + '/data/layouts/layouts.json', 'w'), indent=2); open(ROOT + '/data/layouts/layouts.json', 'a').write('\n')
        from gym_lib import apply_gym
        sys.path.insert(0, ROOT)
        os.chdir(ROOT)
        apply_gym('PewterCity_Gym', 'LAYOUT_GYM_EM_RUSTBORO',
                  objs={0: (8, 3, 'FACE_DOWN'), 1: (8, 10, 'FACE_DOWN', 3), 2: (6, 19, 'FACE_DOWN')},
                  warps=[(7, 21), (8, 21), (8, 21)], bg=[(4, 20), (11, 20)])
