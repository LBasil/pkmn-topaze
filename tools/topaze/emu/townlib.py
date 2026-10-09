# Aides de test pour Grenalux : planificateur de trajet avec relecture de la position (replanification) + dialogues
import sys, json, subprocess, shutil, os
sys.path.insert(0, '/home/claude/pkmn-topaze/docs/topaze')
import grenalux_paths as P
from pl import *
STATIC = {(10, 16), (22, 6), (22, 11), (19, 22), (33, 23), (36, 23), (41, 26), (31, 8)}
if os.environ.get('TOPAZE_COL'):
    STATIC = {tuple(c) for c in json.load(open('/tmp/opanihrum_npc.json')).values()} | {(18, 6), (20, 2), (8, 12), (9, 12)}
P.B |= STATIC
CUR = S + 'cur.ss'
def sh(L):
    out = run(['run 2', 'ls ' + CUR, 'run 2'] + L + ['run 4', 'readp 03005008 0 6', 'ss ' + CUR], show=False)
    last = out[-1].split(':')[-1].split()
    v = [int(x, 16) for x in last]
    return (v[0], v[2]), (v[4], v[5])        # (x, y), (groupe, carte)
def start(state):
    shutil.copy(S + state + '.ss', CUR)
def where():
    return sh([])
def leg(pos, tgt):
    t = P.path(pos, tgt)
    if not t: return None
    d0 = (t[1][0] - t[0][0], t[1][1] - t[0][1]); n = 1
    while n + 1 < len(t) and (t[n + 1][0] - t[n][0], t[n + 1][1] - t[n][1]) == d0: n += 1
    return {(1, 0): 'RIGHT', (-1, 0): 'LEFT', (0, 1): 'DOWN', (0, -1): 'UP'}[d0], n
def goto(tgt, maxit=14):
    pos, mp = where()
    for _ in range(maxit):
        if pos == tgt: return pos
        d, n = leg(pos, tgt)
        pos, mp = sh(walk(d, n))
    raise AssertionError(('inatteignable', tgt, pos))
def talk(face, shot, n=3):
    L = ['key %s 4' % face, 'run 14', 'key A 4', 'run 50', 'shot %s_0.ppm' % shot]
    for i in range(1, n): L += ['key A 4', 'run 50', 'shot %s_%d.ppm' % (shot, i)]
    for i in range(6): L += ['key B 4', 'run 24']
    return L
def visit(tgt, face, name, n=3):
    goto(tgt); r = sh(talk(face, name, n)); return r
