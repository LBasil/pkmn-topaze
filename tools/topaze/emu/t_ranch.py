# Test grand ranch : maison -> grande rue -> ouverture est -> grand ranch (carte voisine)
from play import run
from base import *
L = OUT + ['key DOWN 40', 'run 120', 'readp 03005008 0 6']
L += walk('DOWN', 2) + walk('RIGHT', 32) + walk('UP', 5) + ['readp 03005008 0 6', 'shot r0.ppm']
L += walk('RIGHT', 8) + ['readp 03005008 0 6', 'shot r1.ppm'] + walk('RIGHT', 8) + ['readp 03005008 0 6', 'shot r2.ppm']
run(L)
