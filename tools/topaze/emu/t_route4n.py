from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
start('r4n_0')
info = json.load(open('/tmp/route4_info.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/route4_col.json'))['blocked']}
P.B |= {tuple(c) for c in info['obj'].values()}
sh(['writepb 03005008 1040 ff', 'writepb 03005008 1041 0f', 'writepb 03005008 f8e 80'])
for t in ((25, 21), (24, 33), (37, 34)): print(t, goto(t, maxit=40))
print(sh(['key RIGHT 20', 'run 120', 'key RIGHT 20', 'run 120', 'shot r4n_cer.ppm']))
