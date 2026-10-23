#!/usr/bin/env python3
"""Arene de GRIM (Bourg Quartz, GLACE) redessinee : palais de glace, lac gele central avec sentier circulaire, cristaux, fresque de flocon.
Ecrase gym_sootopolis_sec + layout GymEmSootopolis. Idempotent."""
import sys, math, json, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gym_art import *
P7 = Pal('kabcdewsnNgpPyt', [(14, 24, 46), (40, 70, 120), (70, 120, 176), (120, 174, 222), (170, 214, 242), (214, 238, 252), (252, 254, 255), (90, 150, 210), (24, 40, 90), (40, 80, 150), (150, 196, 236), (150, 110, 220), (216, 170, 255), (255, 226, 120), (110, 230, 230)])
ts = TS({7: P7, 8: P7})
def ice(seed, kind=0):
    s = Spr('d'); s.rect(0, 15, 15, 15, 'c'); s.rect(15, 0, 15, 15, 'c'); s.rect(0, 0, 14, 0, 'e'); s.rect(0, 0, 0, 14, 'e')
    s.noise(['e', 'g', 'd', 'd'], 0.1, seed, only=['d'])
    r = random.Random(seed)
    if kind == 1:
        x, y = r.randint(2, 5), r.randint(2, 4)
        for _ in range(9):
            s.px(x, y, 'c'); x += r.choice((0, 1, 1)); y += r.choice((1, 1, 0))
            if x > 14 or y > 14: break
    if kind == 2:
        for _ in range(4): s.px(r.randint(2, 13), r.randint(2, 13), 'w')
        s.px(r.randint(2, 13), r.randint(2, 13), 't')
    return s
def snow(seed):
    s = Spr('w'); s.rect(0, 15, 15, 15, 'e'); s.rect(15, 0, 15, 15, 'e'); s.noise(['e', 'd', 'e', 'w'], 0.18, seed, only=['w'])
    return s
_f = None
def lake():
    s = Spr('n')
    for y in range(16):
        for x in range(16):
            v = math.sin(2 * math.pi * (x / 16 + 0.2 * math.sin(2 * math.pi * y / 16))) + math.sin(2 * math.pi * (y / 16 + 0.15 * math.sin(2 * math.pi * x / 8)))
            s.g[y][x] = 'n' if v < 0.2 else ('N' if v < 1.5 else 'a')
    for x, y in ((3, 4), (11, 11)): s.px(x, y, 't')
    return s
def pool(t, b, l, r):
    s = lake()
    if t: s.rect(0, 0, 15, 2, 'd'); s.rect(0, 0, 15, 0, 'w'); s.rect(0, 1, 15, 1, 'e'); s.rect(0, 2, 15, 2, 'c'); s.rect(0, 3, 15, 3, 'k')
    if b: s.rect(0, 13, 15, 15, 'd'); s.rect(0, 13, 15, 13, 'c'); s.rect(0, 12, 15, 12, 'k'); s.rect(0, 14, 15, 14, 'e'); s.rect(0, 15, 15, 15, 'c')
    if l: s.rect(0, 0, 2, 15, 'd'); s.rect(0, 0, 0, 15, 'w'); s.rect(1, 0, 1, 15, 'e'); s.rect(2, 0, 2, 15, 'c'); s.rect(3, 0, 3, 15, 'k')
    if r: s.rect(13, 0, 15, 15, 'd'); s.rect(13, 0, 13, 15, 'c'); s.rect(12, 0, 12, 15, 'k'); s.rect(14, 0, 14, 15, 'e'); s.rect(15, 0, 15, 15, 'c')
    return s
def wall_cap():
    s = Spr('b'); s.rect(0, 0, 15, 0, 'e'); s.rect(0, 1, 15, 1, 'd'); s.rect(0, 13, 15, 13, 'a'); s.rect(0, 14, 15, 14, 'k'); s.rect(0, 15, 15, 15, 'k')
    s.noise(['c', 'a', 'b'], 0.1, 3, only=['b'])
    for x in (2, 6, 10, 14):
        for y in range(2, 5 + x % 5): s.px(x, y, 'w' if y < 4 else 'e')
    return s
def wall_face(kind, seed):
    s = Spr('c'); s.rect(0, 0, 15, 0, 'w'); s.rect(0, 1, 15, 1, 'e'); s.rect(0, 15, 15, 15, 'k'); s.rect(0, 14, 15, 14, 'b')
    for y in (6, 11): s.rect(0, y, 15, y, 'b')
    for y, off in ((2, 5), (7, 0), (12, 9)): s.rect(off, y, off, y + 3, 'b') if False else None
    for y, off in ((2, 5), (7, 0), (7, 10), (12, 8)): s.rect(off, y, off, min(y + 3, 14), 'b')
    s.noise(['b', 'd', 'c'], 0.1, seed, only=['c'])
    if kind == 'frost':
        for x, y in ((3, 3), (4, 4), (5, 3), (4, 2), (4, 5), (3, 5), (5, 5), (12, 8), (11, 9), (13, 9), (12, 7), (12, 10)): s.px(x, y, 'w')
    if kind == 'rune':
        s.rect(5, 3, 10, 12, 'a'); s.rect(6, 4, 9, 11, 'n')
        for x, y in ((7, 5), (8, 5), (7, 6), (8, 7), (7, 8), (8, 8), (7, 9), (8, 10)): s.px(x, y, 't')
    return s
def side(left, seed):
    s = wall_face('plain', seed); s.rect(0, 0, 15, 1, 'c'); s.rect(0, 14, 15, 14, 'c'); s.rect(0, 15, 15, 15, 'b')
    for y in range(16):
        for x in range(16):
            if s.g[y][x] in 'we': s.g[y][x] = 'd'
    e = 15 if left else 0; s.rect(e, 0, e, 15, 'k'); i = 14 if left else 1; s.rect(i, 0, i, 15, 'e')
    return s
def dais(emblem=False, step=False):
    s = Spr('s')
    s.rect(0, 0, 15, 0, 'w'); s.rect(0, 0, 0, 15, 'w'); s.rect(0, 15, 15, 15, 'a'); s.rect(15, 0, 15, 15, 'a'); s.rect(1, 1, 14, 1, 'e'); s.rect(1, 1, 1, 14, 'e')
    s.noise(['c', 'g', 's'], 0.1, 31, only=['s'])
    for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)): s.px(x, y, 'y')
    if step:
        s = Spr('d'); s.rect(0, 0, 15, 3, 'w'); s.rect(0, 4, 15, 4, 'k'); s.rect(0, 5, 15, 8, 'e'); s.rect(0, 9, 15, 9, 'k'); s.rect(0, 10, 15, 13, 'd'); s.rect(0, 14, 15, 14, 'k'); s.rect(0, 15, 15, 15, 'c')
    if emblem: flake(s, 8, 8, 5.2, 'w', 'e')
    return s
def flake(s, cx, cy, R, c, c2, ys=1.0):
    for a in range(6):
        th = a * math.pi / 3
        for k in range(0, int(R * 4) + 1):
            d = k / 4.0
            x = cx + d * math.cos(th) - 0.5; y = cy + d * math.sin(th) * ys - 0.5
            xi, yi = int(round(x)), int(round(y))
            if 0 <= xi < 16 and 0 <= yi < 16: s.g[yi][xi] = c
            if d > R * 0.55 and d < R * 0.8:
                for sg in (-1, 1):
                    th2 = th + sg * math.pi / 3
                    for j in range(1, 3):
                        xx = int(round(x + j * 0.8 * math.cos(th2))); yy = int(round(y + j * 0.8 * math.sin(th2) * ys))
                        if 0 <= xx < 16 and 0 <= yy < 16: s.g[yy][xx] = c2
def on_floor(rows, seed):
    f = ice(seed); f.over(Spr.parse(rows)); return f
CRYST_T = ['................', '.......kk.......', '......kwwk......', '.....kweewk.....', '....kwedeewk....', '....kedddewk....', '...kwedddddek...', '...kededcdddk...', '..kwedddcdddek..', '..kededcccddek..', '..kedddcccddek..', '..kdddccbcddck..', '..kddccbbbcdck..', '..kdccbbabbcck..', '..kccbbaaabcck..', '..kcbbaaaaabck..']
CRYST_B = ['..kcbbaaaaabck..', '..kcbbaaaaabck..', '...kbbaaaaabk...', '...kkbbaaabkk...', '....kkbbbbkk....', '.....kkkkkk.....', '................', '................', '................', '................', '................', '................', '................', '................', '................', '................']
STATUE = ['................', '.......kk.......', '......kwwk......', '.....kwddwk.....', '....kwdtedwk....', '.....kwddwk.....', '......kwwk......', '.....kkddkk.....', '....kdeeeedk....', '....kdecceek....', '..kkkkkkkkkkkk..', '..kdddddddddck..', '..kccppPPcccbk..', '..kbbbbbbbbbbk..', '..kkkkkkkkkkkk..', '................']
PIL_T = ['................', '...kkkkkkkkkk...', '..kwwwwwwwwwwk..', '..kddddddddddck.', '...kkcceeccckk..', '....kcdwdcck....', '....kcdwdcck....', '....kcdwdcck....', '....kcdedcck....', '....kcdwdcck....', '....kcdedcck....', '....kcdwdcck....', '....kcdwdcck....', '....kcdedcck....', '....kcdwdcck....', '....kcdwdcck....']
CRYST_T, CRYST_B, STATUE, PIL_T = [[r[:16].ljust(16, '.') for r in L] for L in (CRYST_T, CRYST_B, STATUE, PIL_T)]
PIL_B = ['....kcdwdcck....'] * 10 + ['...kkcdwdckk...', '..kwwwwwwwwwwk..', '..kkkkkkkkkkkk..', '................', '................', '................']
PIL_B = [r[:16].ljust(16, '.') for r in PIL_B]
MAT = ['kkkkkkkkkkkkkkkk', 'kyyyyyyyyyyyyyyk'] + ['ky' + 'e' * 12 + 'yk'] * 12 + ['kyyyyyyyyyyyyyyk', 'kkkkkkkkkkkkkkkk']
def mural():
    W3 = 48; g = [['b'] * W3 for _ in range(32)]
    rr = random.Random(8)
    for y in range(32):
        for x in range(W3):
            if y < 16: g[y][x] = 'a'
            if y == 0: g[y][x] = 'e'
            elif y == 15: g[y][x] = 'b'
            elif y == 16: g[y][x] = 'w'
            elif y == 17: g[y][x] = 'e'
            elif y == 31: g[y][x] = 'k'
            elif y == 30: g[y][x] = 'b'
            elif rr.random() < 0.08: g[y][x] = 'b' if y > 17 else 'c'
    for y in range(4, 29):
        for x in range(8, 40):
            dx = (x - 24) / 16.0; dy = (y - 16) / 12.5
            d = dx * dx + dy * dy
            if d < 1.0: g[y][x] = 'n' if d > 0.45 else 'N'
            elif d < 1.12: g[y][x] = 'w' if d < 1.06 else 'e'
    cx, cy = 24, 16
    for a in range(6):
        th = a * math.pi / 3 + math.pi / 6 * 0
        for k in range(0, 14 * 4):
            d = k / 4.0
            x = cx + d * math.cos(th); y = cy + d * math.sin(th) / 1.12
            xi, yi = int(round(x)), int(round(y))
            if 4 <= yi < 29 and 8 <= xi < 40: g[yi][xi] = 'w'
            if d > 6 and d < 11 and (k % 8 < 4):
                for sg in (-1, 1):
                    th2 = th + sg * math.pi / 3
                    for j in range(1, 4):
                        xx = int(round(x + j * math.cos(th2))); yy = int(round(y + j * math.sin(th2) / 1.12))
                        if 4 <= yy < 29 and 8 <= xx < 40: g[yy][xx] = 'e'
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1): g[cy + dy][cx + dx] = 't' if (dx or dy) else 'w'
    out = []
    for k in range(3):
        for r in range(2):
            sp = Spr()
            for y in range(16):
                for x in range(16): sp.g[y][x] = g[r * 16 + y][k * 16 + x]
            out.append(sp)
    return out
ts.add('i1', ice(1), 7); ts.add('i2', ice(2), 7); ts.add('i3', ice(3), 7); ts.add('ic', ice(4, 1), 7); ts.add('ic2', ice(8, 1), 7); ts.add('isp', ice(5, 2), 7)
ts.add('sn1', snow(1), 7); ts.add('sn2', snow(2), 7)
ts.add('cap', wall_cap(), 7); ts.add('w1', wall_face('plain', 1), 7); ts.add('w2', wall_face('frost', 2), 7); ts.add('w3', wall_face('rune', 3), 7)
ts.add('sl', side(True, 2), 7); ts.add('sr', side(False, 4), 7)
ts.add('da', dais(), 7); ts.add('de', dais(True), 7); ts.add('ds', dais(step=True), 7)
ts.add('ct', on_floor(CRYST_T, 21), 7); ts.add('cb', on_floor(CRYST_B, 22), 7); ts.add('statue', on_floor(STATUE, 24), 7)
ts.add('pt', on_floor(PIL_T, 25), 7); ts.add('pb', on_floor(PIL_B, 26), 7)
ts.add('mat', Spr.parse(MAT), 7, beh=0x65)
for k, sp in enumerate(mural()): ts.add('mu%d%d' % (k // 2 + 1, k % 2), sp, 7)
LEG = {'#': 'black', 'T': 'cap', 'F': 'w1', 'G': 'w3', 'H': 'w2', 'L': 'sl', 'Z': 'sr', 'f': 'i1', 'h': 'i2', 'i': 'i3', 'g': 'ic', 'j': 'ic2', 'k': 'isp', 'n': 'sn1', 'o': 'sn2', 'D': 'da', 'E': 'de', 's': 'ds',
       'C': 'ct', 'c': 'cb', 'p': 'pt', 'q': 'pb', 'S': 'statue', 'm': 'mat', '1': 'mu10', '2': 'mu20', '3': 'mu30', '4': 'mu11', '5': 'mu21', '6': 'mu31'}
W, H = 17, 26
LAKE = [(x, y) for x in range(4, 13) for y in range(11, 17) if (x, y) not in ((4, 11), (12, 11), (4, 16), (12, 16))]
PS = set(LAKE)
def pooltile(x, y): return 'pool%d%d%d%d' % tuple(int((x + dx, y + dy) not in PS) for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)))
for (x, y) in PS:
    n = pooltile(x, y)
    if n not in ts.names: ts.add(n, pool(*[int(c) for c in n[4:]]), 7)
def build():
    g = [['#'] * W for _ in range(H)]
    rr = random.Random(5)
    for y in range(3, H - 1):
        for x in range(2, W - 2): g[y][x] = rr.choice('ffffhhigj' if rr.random() < 0.9 else 'kkn')
    for x in range(1, W - 1):
        g[1][x] = 'T'; g[2][x] = 'FFHFGFFHFFFFHFGFF'[x - 1] if x - 1 < 17 else 'F'
        g[H - 1][x] = 'T'
    for y in range(2, H - 1): g[y][1] = 'L'; g[y][W - 2] = 'Z'
    def put(x, y, c): g[y][x] = c
    for x in range(6, 11):
        for y in (3, 4): put(x, y, 'D')
        if x in (7, 8, 9): put(x, 5, 's')
    put(8, 4, 'E')
    for k, x in enumerate((7, 8, 9)): put(x, 1, '123'[k]); put(x, 2, '456'[k])
    for x in (3, 13): put(x, 3, 'p'); put(x, 4, 'q')
    for (x, y) in ((2, 8), (14, 8), (2, 18), (14, 18), (8, 20), (3, 22), (13, 22)): put(x, y, 'C') if y < H - 2 else None
    for (x, y) in ((4, 7), (12, 7), (6, 9), (10, 9), (3, 20), (13, 20), (8, 18)): put(x, y, 'n')
    for (x, y) in ((5, 7), (11, 7), (2, 12), (14, 14)): put(x, y, 'o')
    put(6, H - 2, 'S'); put(10, H - 2, 'S'); put(8, H - 1, 'm'); put(9, H - 1, 'm') if False else None
    put(8, H - 1, 'm'); put(9, H - 1, 'm')
    rows = [list(r) for r in g]
    # cristaux : tuile haute + basse
    for (x, y) in ((2, 8), (14, 8), (2, 18), (14, 18), (8, 20), (3, 22), (13, 22)):
        if y + 1 < H - 1: rows[y][x] = 'C'; rows[y + 1][x] = 'c'
    chars = {}; leg = dict(LEG); block = set('#TFGHLZCcpqS123456')
    for (x, y) in PS:
        n = pooltile(x, y)
        if n not in chars: chars[n] = chr(0x100 + len(chars)); leg[chars[n]] = n; block.add(chars[n])
        rows[y][x] = chars[n]
    return [''.join(r) for r in rows], leg, block
RR, LEGF, BLOCK = build()
if __name__ == '__main__':
    for r in RR: assert len(r) == W, (len(r), r)
    assert len(RR) == H
    preview(ts, RR, LEGF, '/tmp/gx/ice_gym.png', scale=2)
    if '--write' in sys.argv:
        ts.write('gym_sootopolis_sec')
        words = build_map(ts, RR, LEGF, BLOCK)
        write_layout('GymEmSootopolis', W, H, words, ts.id('black'))
        lj = json.load(open(ROOT + '/data/layouts/layouts.json'))
        for l in lj['layouts']:
            if l.get('id') == 'LAYOUT_GYM_EM_SOOTOPOLIS': l['width'], l['height'] = W, H
        json.dump(lj, open(ROOT + '/data/layouts/layouts.json', 'w'), indent=2); open(ROOT + '/data/layouts/layouts.json', 'a').write('\n')
        os.chdir(ROOT); from gym_lib import apply_gym
        apply_gym('CeladonCity_Gym', 'LAYOUT_GYM_EM_SOOTOPOLIS',
                  objs={0: (10, 9, 'FACE_LEFT', 3), 1: (14, 13, 'FACE_UP', 3), 2: (5, 6, 'FACE_RIGHT', 3), 3: (11, 6, 'FACE_LEFT', 3), 4: (2, 13, 'FACE_DOWN', 3), 5: (6, 18, 'FACE_RIGHT', 3),
                        6: (8, 3, 'FACE_DOWN'), 7: (10, 22, 'FACE_LEFT', 3)},
                  warps=[(8, 25), (9, 25), (9, 25)], bg=[(6, 24), (10, 24)])
