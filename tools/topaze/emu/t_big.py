# Test grande Grenalux : sortie de la maison -> avenue -> declencheur du rival -> ranch
from play import run
from base import *
L = OUT + ['key DOWN 40', 'run 120', 'readp 03005008 0 6', 'shot a0.ppm']
# de (8,10) : droite jusqu'a x=22 (grande rue y=12), puis haut jusqu'a y=1
L += walk('DOWN', 2) + walk('RIGHT', 14) + walk('UP', 11)
for i in range(6): L += ['run 60', 'shot s%d.ppm' % i, 'readp 03005008 0 6']
M = []
for i in range(16): M += ['key A 4', 'run 90']
M += ['run 300', 'shot end.ppm', 'readp 03005008 0 6']
run(L + M)
