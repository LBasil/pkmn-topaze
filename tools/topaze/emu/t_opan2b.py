from play import run
from base import *
from townlib import *
start('opan2')
for i in range(6):
    print(sh(['key A 4', 'run 100', 'shot tb_%d.ppm' % i]))
