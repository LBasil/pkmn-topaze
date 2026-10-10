from play import run
from base import *
from townlib import *
start('free2')
sh(['writepb 03005008 f74 80', 'writepb 03005008 f75 07', 'writepb 03005008 10e0 02'])
goto((35, 21)); sh(['key UP 30', 'run 100']); sh(['key DOWN 30', 'run 100'])
goto((22, 3)); print(sh(['key UP 70', 'run 90', 'shot tm_start.ppm']))
print(sh(['key RIGHT 30', 'run 40']))
shutil.copy(CUR, S + 'tm_0.ss')
