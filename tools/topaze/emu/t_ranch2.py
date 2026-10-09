# Grand ranch apres l'attaque : on pose FLAG_GRENALUX_ONYBRIS_STRIKE (0x4A9) puis on va a la cloture
from play import run
from base import *
L = OUT + ['writepb 03005008 f75 02', 'key DOWN 40', 'run 120']
L += walk('DOWN', 2) + walk('RIGHT', 32) + walk('UP', 5) + walk('RIGHT', 4) + walk('UP', 1) + walk('RIGHT', 22) + walk('DOWN', 6) + ['readp 03005008 0 6', 'shot q0.ppm']
run(L)
