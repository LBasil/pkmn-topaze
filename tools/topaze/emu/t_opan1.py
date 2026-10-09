# etape 2 : validation d'Opanihrum (lancer avec TOPAZE_COL=/tmp/opanihrum_col.json, ROM de test, etat opan0)
from play import run
from base import *
from townlib import *
import sys
start('opan0')
print('arrivee', where())
def enter(name, front, door_dir='UP', expect=None):
    goto(front)
    r = sh([('key %s 34' % door_dir), 'run 90', 'shot in_%s.ppm' % name])
    print(name, 'entre ->', r, 'attendu', expect)
    # sortie : marcher vers le bas jusqu'a revenir en ville
    sh(['key B 4', 'run 20'] * 12 + ['key A 4', 'run 60'] * 6 + ['key B 4', 'run 20'] * 6)
    for i in range(5):
        r2 = sh(['key DOWN 30', 'run 70'])
        if r2[1] == (3, 1): break
    print(name, 'sortie ->', r2)
    return r2
enter('center', (16, 21), expect=(14, 3))     # CENTRE
enter('mart', (27, 21), expect=None)
enter('school', (28, 9))
enter('house', (36, 9))
# arene verrouillee : declencheur devant la porte, puis repoussee
goto((10, 12)); r = sh(['key LEFT 18', 'run 20', 'shot gym_lock_0.ppm', 'key A 4', 'run 60', 'shot gym_lock_1.ppm'] + ['key A 4', 'run 40'] * 2 + ['run 60'])
print('arene verrouillee', r)
print(sh(['key B 4', 'run 40'] * 4 + ['run 100']))
goto((21, 3)); r = sh(['key UP 20', 'run 40', 'shot old_0.ppm', 'key A 4', 'run 60', 'shot old_1.ppm', 'key A 4', 'run 60', 'key A 4', 'run 60'])
print('vieil homme (route nord)', r)
shutil.copy(CUR, S + 'opan1.ss')
