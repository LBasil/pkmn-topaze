# Route 4 nord (apres Mt Moon) : arrivee par la porte nord, puis jusqu'a la sortie est vers Azuria
from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
start('free2')
sh(['writepb 03005008 f74 80', 'writepb 03005008 f75 07', 'writepb 03005008 10e0 02'])
goto((35, 21)); sh(['key UP 30', 'run 100']); sh(['key DOWN 30', 'run 100'])
goto((22, 3)); print(sh(['key UP 70', 'run 90', 'shot r4n_start.ppm']))
shutil.copy(CUR, S + 'r4n_0.ss')
