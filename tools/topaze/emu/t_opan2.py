# etape 3 : tutoriel du vieil homme (var=1), porte nord -> route 2 et retour
from play import run
from base import *
from townlib import *
start('opan1')
print(sh(['writepb 03005008 10a2 01']))
goto((16, 21)); print(sh(['key UP 34', 'run 90']))
for i in range(5):
    r = sh(['key DOWN 30', 'run 70'])
    if r[1] == (3, 1): break
print('recharge', r)
goto((21, 3)); print(sh(['key UP 20', 'run 60', 'shot tut_0.ppm']))
print(sh(['key A 4', 'run 60'] * 50 + ['run 200', 'shot tut_1.ppm']))
print('apres tuto', where())
shutil.copy(CUR, S + 'opan2.ss')
