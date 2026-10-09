from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
info = json.load(open('/tmp/route2_info.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/route2_col.json'))['blocked']}
P.B |= {(x, y) for (x0, y0, x1, y1) in info['tall'] for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}
P.B |= {tuple(c) for c in info['npc'].values()}
start('r2n_0')
sh(['key DOWN 18', 'run 20'])
P.B |= {(12, 0), (13, 0)}
path = [tuple(c) for c in info['path']]
for y in (6, 13, 19):
    tgt = next(c for c in path if c[1] == y and tuple(c) not in P.B); print(tgt, goto(tgt, maxit=30))
print(sh(['shot r2_north.ppm']))
print('portail nord ->', goto((13, 25), maxit=30), sh(['key DOWN 40', 'run 120', 'shot r2_forestN.ppm']))
