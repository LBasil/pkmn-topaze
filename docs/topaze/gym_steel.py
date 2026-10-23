#!/usr/bin/env python3
"""Arene d'HEPHA (Opanihrum, ACIER) redessinee : fonderie a cloisons en zigzag, sol de tole, bandes de securite, fresque d'engrenage.
Ecrase gym_dewford_sec + layout GymEmDewford. Idempotent."""
import sys, math, json, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gym_art import *
P7 = Pal('kabcdewyYrotnsh', [(18, 20, 28), (44, 52, 66), (70, 80, 98), (100, 112, 132), (140, 152, 172), (190, 200, 216), (240, 244, 250), (240, 200, 40), (160, 120, 20), (200, 50, 40), (250, 140, 40), (60, 160, 170), (30, 40, 70), (120, 150, 190), (255, 224, 130)])
ts = TS({7: P7, 8: P7})
def plate(seed, kind=0):
    s = Spr('c'); s.rect(0, 0, 15, 0, 'd'); s.rect(0, 0, 0, 15, 'd'); s.rect(0, 15, 15, 15, 'b'); s.rect(15, 0, 15, 15, 'b')
    s.noise(['b', 'd', 'c', 'c'], 0.06, seed, only=['c'])
    for x, y in ((2, 2), (13, 2), (2, 13), (13, 13)): s.px(x, y, 'e'); s.px(x + 1 if x < 8 else x - 1, y, 'a') if False else None
    if kind == 1:
        for y in range(2, 14, 3): s.rect(2, y, 13, y, 'b')
    if kind == 2:
        s = Spr('a'); s.rect(0, 0, 15, 0, 'c'); s.rect(0, 15, 15, 15, 'k')
        for y in range(1, 15, 2):
            s.rect(0, y, 15, y, 'b')
        for x in range(0, 16, 4): s.rect(x, 1, x, 14, 'k')
        s.noise(['k', 'b'], 0.08, seed, only=['a'])
    return s
def hazard(seed):
    s = Spr('a'); s.rect(0, 0, 15, 15, 'a')
    for y in range(16):
        for x in range(16):
            if ((x + y) // 4) % 2 == 0: s.g[y][x] = 'y'
            else: s.g[y][x] = 'k'
    s.rect(0, 0, 15, 0, 'Y'); s.rect(0, 15, 15, 15, 'k')
    return s
def wall_cap():
    s = Spr('d'); s.rect(0, 0, 15, 0, 'e'); s.rect(0, 1, 15, 1, 'd'); s.rect(0, 13, 15, 13, 'b'); s.rect(0, 14, 15, 14, 'a'); s.rect(0, 15, 15, 15, 'k')
    s.noise(['c', 'e'], 0.08, 3, only=['d'])
    for x in (2, 7, 12): s.px(x, 7, 'a'); s.px(x, 6, 'e')
    return s
def wall_face(kind, seed):
    s = Spr('b'); s.rect(0, 0, 15, 0, 'e'); s.rect(0, 1, 15, 1, 'd'); s.rect(0, 15, 15, 15, 'k'); s.rect(0, 14, 15, 14, 'a')
    s.noise(['a', 'c'], 0.07, seed, only=['b'])
    s.rect(0, 7, 15, 7, 'a'); s.rect(0, 8, 15, 8, 'c')
    for x in (1, 14):
        for y in (3, 11): s.px(x, y, 'e'); s.px(x, y + 1, 'a')
    if kind == 'pipe':
        s.rect(0, 3, 15, 5, 'c'); s.rect(0, 3, 15, 3, 'e'); s.rect(0, 5, 15, 5, 'a')
        for x in (4, 11): s.rect(x, 2, x + 1, 6, 'd'); s.rect(x, 2, x, 6, 'e')
    if kind == 'vent':
        s.rect(3, 3, 12, 12, 'a')
        for y in range(4, 12, 2): s.rect(4, y, 11, y, 'k')
        s.rect(3, 3, 12, 3, 'd'); s.rect(3, 12, 12, 12, 'd')
    if kind == 'glow':
        s.rect(4, 3, 11, 12, 'k'); s.rect(5, 4, 10, 11, 'r'); s.rect(6, 5, 9, 10, 'o'); s.rect(7, 6, 8, 9, 'h')
    return s
def side(left, seed):
    s = wall_face('plain', seed); s.rect(0, 0, 15, 1, 'b'); s.rect(0, 14, 15, 14, 'b'); s.rect(0, 15, 15, 15, 'a')
    for y in range(16):
        for x in range(16):
            if s.g[y][x] in 'e': s.g[y][x] = 'd'
    e = 15 if left else 0; s.rect(e, 0, e, 15, 'k'); i = 14 if left else 1; s.rect(i, 0, i, 15, 'e')
    return s
def dais(emblem=False, step=False):
    s = Spr('b')
    s.rect(0, 0, 15, 0, 'e'); s.rect(0, 0, 0, 15, 'e'); s.rect(0, 15, 15, 15, 'k'); s.rect(15, 0, 15, 15, 'k'); s.rect(1, 1, 14, 1, 'd'); s.rect(1, 1, 1, 14, 'd')
    s.noise(['a', 'c', 'b'], 0.09, 31, only=['b'])
    for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)): s.px(x, y, 'o')
    if step:
        s = Spr('c'); s.rect(0, 0, 15, 3, 'e'); s.rect(0, 4, 15, 4, 'k'); s.rect(0, 5, 15, 8, 'd'); s.rect(0, 9, 15, 9, 'k'); s.rect(0, 10, 15, 13, 'c'); s.rect(0, 14, 15, 14, 'k'); s.rect(0, 15, 15, 15, 'b')
        for x in (0, 15): s.px(x, 6, 'y')
    if emblem:
        cog(s, 8, 8, 5.5, 3.2, 'o', 'h')
    return s
def cog(s, cx, cy, R, r, c, c2):
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - cx + 0.0, y - cy + 0.0); a = math.atan2(y - cy, x - cx)
            tooth = R if math.cos(a * 8) > 0.2 else R - 1.6
            if d <= tooth and d >= r: s.g[y][x] = c
            elif d < r - 0.5 and d >= r - 1.6: s.g[y][x] = c2
def on_floor(rows, seed):
    f = plate(seed); f.over(Spr.parse(rows)); return f
CRATE = ['................', '................', '................', '.kkkkkkkkkkkkk..', '.kddddddddddck..', '.kdYyYyYyYyYck..', '.kdyYyYyYyYyck..', '.kdYyYkkYyYyck..', '.kdyYyYkkyYyck..', '.kdYyYyYyYyYck..', '.kdyYyYyYyYyck..', '.kccccccccccck..', '.kbbbbbbbbbbbk..', '..kkkkkkkkkkk...', '................', '................']
CRATE = [r[:16].ljust(16, '.') for r in CRATE]
PRESS = ['................', '..kkkkkkkkkkkk..', '..keeeeeeeeeck..', '..kdddddddddck..', '...kkkkkkkkkk...', '....kccbbcck....', '....kccbbcck....', '....kddddddk....', '...kccccccccck..', '...kyyyyyyyyyk..', '...kkkkkkkkkkk..', '..keeeeeeeeeeek.', '..kccccccccccck.', '..kbbbbbbbbbbbk.', '..kkkkkkkkkkkkk.', '................']
PRESS = [r[:16].ljust(16, '.') for r in PRESS]
STATUE = ['................', '......kkkk......', '....kkddddkk....', '...kdddkkdddk...', '...kdkdddkdk....', '...kddkeekddk...', '...kdkdddkdk....', '...kdddkkdddk...', '....kkddddkk....', '......kkkk......', '..kkkkkkkkkkkk..', '..kdddddddddck..', '..kccoohhccccbk..', '..kbbbbbbbbbbk..', '..kkkkkkkkkkkk..', '................']
PIL_T = ['................', '...kkkkkkkkkk...', '..keeeeeeeeeek..', '..kddddddddddck.', '...kkcceeccckk..', '....kccdbcck....', '....kccdbcck....', '....kccdbcck....', '....kyYdbYyk....', '....kccdbcck....', '....kccdbcck....', '....kccdbcck....', '....kccdbcck....', '....kccdbcck....', '....kccdbcck....', '....kccdbcck....']
PIL_T = [r[:16].ljust(16, '.') for r in PIL_T]
PIL_B = ['....kccdbcck....'] * 10 + ['...kkccdbcckk...', '..keeeeeeeeeek..', '..kkkkkkkkkkkk..', '................', '................', '................']
MAT = ['kkkkkkkkkkkkkkkk', 'kyyyyyyyyyyyyyyk'] + ['ky' + 'c' * 12 + 'yk'] * 12 + ['kyyyyyyyyyyyyyyk', 'kkkkkkkkkkkkkkkk']
def mural():
    W3 = 48; g = [['b'] * W3 for _ in range(32)]
    rr = random.Random(8)
    for y in range(32):
        for x in range(W3):
            if y < 16: g[y][x] = 'a'
            if y == 0: g[y][x] = 'd'
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
            if d < 1.0: g[y][x] = 'n' if d > 0.55 else 'a'
            elif d < 1.12: g[y][x] = 'e' if d < 1.06 else 'd'
    cx, cy = 24, 16
    for y in range(32):
        for x in range(48):
            d = math.hypot(x - cx, (y - cy) * 1.15); a = math.atan2((y - cy) * 1.15, x - cx)
            R = 11.2 if math.cos(a * 9) > 0.1 else 9.2
            if d <= R and d >= 4.2: g[y][x] = 'd'
            if d <= R and d >= R - 1: g[y][x] = 'e' if g[y][x] == 'd' else g[y][x]
            if d < 4.2 and d >= 2.4: g[y][x] = 'o'
            if d < 2.4: g[y][x] = 'h'
            if 5.0 <= d < 6.0 and g[y][x] == 'd': g[y][x] = 'c'
    out = []
    for k in range(3):
        for r in range(2):
            sp = Spr()
            for y in range(16):
                for x in range(16): sp.g[y][x] = g[r * 16 + y][k * 16 + x]
            out.append(sp)
    return out
ts.add('p1', plate(1), 7); ts.add('p2', plate(2), 7); ts.add('p3', plate(3), 7); ts.add('pg', plate(4, 1), 7); ts.add('gr', plate(5, 2), 7)
ts.add('hz', hazard(1), 7)
ts.add('cap', wall_cap(), 7); ts.add('w1', wall_face('plain', 1), 7); ts.add('w2', wall_face('pipe', 2), 7); ts.add('w3', wall_face('vent', 3), 7); ts.add('wg', wall_face('glow', 4), 7)
ts.add('sl', side(True, 2), 7); ts.add('sr', side(False, 4), 7)
ts.add('da', dais(), 7); ts.add('de', dais(True), 7); ts.add('ds', dais(step=True), 7)
ts.add('crate', on_floor(CRATE, 21), 7); ts.add('press', on_floor(PRESS, 25), 7); ts.add('statue', on_floor(STATUE, 24), 7)
ts.add('pt', on_floor(PIL_T, 22), 7); ts.add('pb', on_floor(PIL_B, 23), 7)
ts.add('mat', Spr.parse(MAT), 7, beh=0x65)
for k, sp in enumerate(mural()): ts.add('mu%d%d' % (k // 2 + 1, k % 2), sp, 7)
LEG = {'#': 'black', 'T': 'cap', 'F': 'w1', 'G': 'wg', 'H': 'w2', 'V': 'w3', 'L': 'sl', 'Z': 'sr', 'f': 'p1', 'h': 'p2', 'i': 'p3', 'g': 'pg', 'r': 'gr', 'x': 'hz', 'D': 'da', 'E': 'de', 's': 'ds',
       'C': 'crate', 'P': 'press', 'p': 'pt', 'q': 'pb', 'S': 'statue', 'm': 'mat', '1': 'mu10', '2': 'mu20', '3': 'mu30', '4': 'mu11', '5': 'mu21', '6': 'mu31'}
BLOCK = set('#TFGHVLZCPpqS123456')
W, H = 18, 29
def build():
    g = [['#'] * W for _ in range(H)]
    rr = random.Random(5)
    for y in range(3, H - 1):
        for x in range(2, W - 2): g[y][x] = rr.choice('ffffhhig')
    for x in range(1, W - 1):
        g[1][x] = 'T'; g[2][x] = 'FFVFHFFGFFHFFVFF'[x - 1] if x - 1 < 16 else 'F'
        g[H - 1][x] = 'T'
    for y in range(2, H - 1): g[y][1] = 'L'; g[y][W - 2] = 'Z'
    def put(x, y, c): g[y][x] = c
    # cloisons : (rang du haut, x0, x1)
    parts = [(23, 6, 15), (18, 2, 11), (13, 6, 15), (8, 2, 11)]  # gaps: G, D, G, D
    for k, (y0, x0, x1) in enumerate(parts):
        for x in range(x0, x1 + 1):
            put(x, y0, 'T'); put(x, y0 + 1, 'FHVFGFHFFV'[(x * 3 + k) % 10])
            if y0 + 2 < H - 1 and g[y0 + 2][x] in 'fhig': put(x, y0 + 2, 'x')
    for x in range(7, 12):
        for y in (3, 4): put(x, y, 'D')
        if x in (8, 9, 10): put(x, 5, 's')
    put(9, 4, 'E')
    for k, x in enumerate((8, 9, 10)): put(x, 1, '123'[k]); put(x, 2, '456'[k])
    for x in (3, 15): put(x, 3, 'p'); put(x, 4, 'q')
    for (x, y) in ((15, 22), (2, 17), (15, 12), (2, 6), (15, 26), (11, 26)): put(x, y, 'C')
    put(2, 4, 'P'); put(15, 10, 'P') if False else None
    for (x, y) in ((3, 11), (12, 21), (3, 25)): put(x, y, 'r')
    put(5, H - 2, 'S'); put(11, H - 2, 'S'); put(7, H - 1, 'm'); put(8, H - 1, 'm')
    return [''.join(r) for r in g]
ROWS = build()
if __name__ == '__main__':
    for r in ROWS: assert len(r) == W, (len(r), r)
    assert len(ROWS) == H
    preview(ts, ROWS, LEG, '/tmp/gx/steel_gym.png', scale=2)
    if '--write' in sys.argv:
        ts.write('gym_dewford_sec')
        words = build_map(ts, ROWS, LEG, BLOCK)
        write_layout('GymEmDewford', W, H, words, ts.id('black'))
        lj = json.load(open(ROOT + '/data/layouts/layouts.json'))
        for l in lj['layouts']:
            if l.get('id') == 'LAYOUT_GYM_EM_DEWFORD': l['width'], l['height'] = W, H
        json.dump(lj, open(ROOT + '/data/layouts/layouts.json', 'w'), indent=2); open(ROOT + '/data/layouts/layouts.json', 'a').write('\n')
        os.chdir(ROOT); from gym_lib import apply_gym
        apply_gym('ViridianCity_Gym', 'LAYOUT_GYM_EM_DEWFORD',
                  objs={0: (14, 5, 'FACE_DOWN', 3), 1: (9, 11, 'FACE_LEFT', 3), 2: (13, 11, 'FACE_UP', 2), 3: (9, 16, 'FACE_RIGHT', 3), 4: (4, 16, 'FACE_UP', 2), 5: (9, 26, 'FACE_LEFT', 4),
                        6: (8, 21, 'FACE_LEFT', 3), 7: (8, 3, 'FACE_DOWN'), 8: (13, 21, 'FACE_UP', 2), 9: (3, 26, 'FACE_DOWN')},
                  warps=[(7, 28), (8, 28), (8, 28)], bg=[(5, 27), (11, 27), (15, 27)])
