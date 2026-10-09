from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
info = json.load(open('/tmp/route2_info.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/route2_col.json'))['blocked']}
P.B |= {(x, y) for (x0, y0, x1, y1) in info['tall'] for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}
P.B |= {tuple(c) for c in info['npc'].values()}
start('r2_0')
sh(['key UP 18', 'run 20'])
P.B |= {(12, 55), (13, 55)}
path = [tuple(c) for c in info['path']]
for y in (50, 44, 37):
    tgt = next(c for c in path if c[1] == y and tuple(c) not in P.B); print(tgt, goto(tgt, maxit=30))
print(sh(['shot r2_south.ppm']))
print('portail sud ->', goto((13, 34), maxit=30), sh(['key UP 40', 'run 120', 'shot r2_forest.ppm']))
print(sh(['key UP 40', 'run 60', 'key UP 40', 'run 60', 'shot r2_forest2.ppm']))
print(sh(['key UP 60', 'run 100', 'shot r2_forest3.ppm']))
