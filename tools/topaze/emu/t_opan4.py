# etape 5 : arene deverrouillee : les deux portes de la fonderie, sortie, PNJ
from play import run
from base import *
from townlib import *
start('opan3')
print(sh(['writepb 03005008 10b4 01']))
goto((16, 21)); sh(['key UP 34', 'run 90'])
for i in range(5):
    r = sh(['key DOWN 30', 'run 70'])
    if r[1] == (3, 1): break
print('recharge', r)
for door, front in (('gauche', (8, 12)), ('droite', (9, 12))):
    goto((front[0] + 2, 12)); 
    r = sh(['key %s 34' % ('LEFT' if front[0] == 9 else 'LEFT')] * 1 + ['run 10']) if False else None
    goto(front) if False else None
    # on marche jusqu'a la case devant la porte puis vers le haut
    pos, mp = where()
    d = 'LEFT'
    n = pos[0] - front[0]
    sh(walk(d, n)); r = sh(['key UP 40', 'run 90', 'shot gym_in_%s.ppm' % door]); print('arene', door, r)
    for i in range(6):
        r = sh(['key DOWN 30', 'run 70'])
        if r[1] == (3, 1): break
    print('sortie', door, r)
for k, (tgt, face, nm) in {'fatman': ((14, 26), 'UP', 'fat'), 'oldman': ((11, 15), 'UP', 'oldm'), 'woman': ((17, 13), 'UP', 'wom'), 'boy': ((26, 25), 'UP', 'boy')}.items():
    try:
        r = visit(tgt, face, 'op_' + nm, 3); print(k, r)
    except AssertionError as e: print(k, 'KO', e)
