# Pyropia v2 : arrivee (ROM de test : sortie nord de Grenalux -> sud de Pyropia)
from play import run
from base import *
from townlib import *
start('free2')
sh(['writepb 03005008 f74 80', 'writepb 03005008 f75 07', 'writepb 03005008 10e0 02'])
goto((35, 21)); sh(['key UP 30', 'run 100']); sh(['key DOWN 30', 'run 100'])
goto((22, 3)); print(sh(['key UP 70', 'run 90', 'shot py_arrive.ppm']))
shutil.copy(CUR, S + 'py_0.ss')
