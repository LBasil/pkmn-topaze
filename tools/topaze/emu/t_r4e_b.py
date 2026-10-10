from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
P.B = {tuple(c) for c in json.load(open('/tmp/route4e_col.json'))['blocked']}
start('r4e_0')
print(where())
for t in ((14, 13), (30, 14), (45, 17), (60, 14), (70, 15)):
    print(t, goto(t, maxit=60))
print(sh(['key RIGHT 20', 'run 80', 'shot r4e_end.ppm']))
print(sh(['key RIGHT 20', 'run 80']))
print(sh(['key LEFT 30', 'run 80', 'shot r4e_back.ppm']))
