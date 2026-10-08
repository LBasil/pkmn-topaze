# Test : sortie de la maison -> trajet nord -> cinematique du rival (Grenalux v2)
from play import run
from base import *
L = OUT + ['key DOWN 40', 'run 120'] + walk('RIGHT', 7) + walk('UP', 6)
for i in range(8):
    L += ['run 60', 'shot s%d.ppm' % i, 'readp 03005008 0 6']
run(L)
