import sys
from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
info = json.load(open('/tmp/route4_info.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/route4_col.json'))['blocked']}
P.B |= {tuple(c) for c in info['obj'].values()}
start('r4_0')
sh(['writepb 03005008 1040 ff', 'writepb 03005008 1041 0f'])
which = sys.argv[1]
sh(['writepb 03005008 f8e 80'])
PL = {'center': ([(14, 72), (24, 64)], 'UP'), 'cave1': ([(14, 72), (24, 64), (31, 58), (20, 53)], 'UP'), 'cave2': ([(25, 21)], 'UP'), 'cer': ([(25, 21), (24, 33), (37, 34)], 'RIGHT')}
tg, key = PL[which]
for t in tg: goto(t, maxit=40)
print(which, sh(['key %s 20' % key, 'run 120', 'key %s 20' % key, 'run 120', 'shot r4_%s.ppm' % which]))
