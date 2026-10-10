from play import run
from base import *
from townlib import *
start('free2')
sh(['writepb 03005008 f74 80', 'writepb 03005008 f75 07', 'writepb 03005008 10e0 02'])
goto((23, 3))
print(sh(['key UP 20', 'run 60'] + ['key A 4', 'run 60'] * 12 + ['key B 4', 'run 30'] * 3))
print(sh(['key UP 70', 'run 90', 'shot r4e_start.ppm']))
print(sh(['key RIGHT 30', 'run 40', 'shot r4e_a.ppm']))
shutil.copy(CUR, S + 'r4e_0.ss')
