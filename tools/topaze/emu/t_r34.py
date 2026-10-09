from play import run
from base import *
from townlib import *
start('r4_0')
print(sh(['shot r34_a.ppm']))
print(sh(['key LEFT 16', 'run 30', 'key LEFT 16', 'run 30', 'shot r34_b.ppm']))
print(sh(['key RIGHT 16', 'run 14', 'key RIGHT 16', 'run 14', 'key RIGHT 16', 'run 14', 'shot r34_c.ppm', 'run 30', 'shot r34_d.ppm', 'run 60', 'shot r34_e.ppm']))
print(sh(['key UP 40', 'run 40', 'key UP 40', 'run 40', 'shot r34_f.ppm']))
