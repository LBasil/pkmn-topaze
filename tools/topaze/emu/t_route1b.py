from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
info = json.load(open('/tmp/route1_info.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/route1_col.json'))['blocked']}
P.B |= {(x, y) for (x0, y0, x1, y1) in info['tall'] for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}
P.B |= {tuple(c) for c in info['ledges']} | {tuple(c) for c in info['npc'].values()}
start('r1_0')
for tgt in ((12, 50), (14, 40), (9, 30), (11, 21), (13, 15), (9, 10), (15, 4)):
    print(tgt, goto(tgt, maxit=30))
print(sh(['shot r1_mid.ppm']))
print('nord ->', goto((15, 1), maxit=20), sh(['key UP 40', 'run 100', 'shot r1_op.ppm']))
print('retour ->', sh(['key DOWN 40', 'run 100', 'shot r1_back.ppm']))
print('retour 2 ->', sh(['key UP 18', 'run 20', 'key DOWN 40', 'run 100', 'shot r1_back.ppm']))
