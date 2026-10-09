from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
info = json.load(open('/tmp/route3_info.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/route3_col.json'))['blocked']}
P.B |= {tuple(c) for c in info['obj'].values()}
start('r3_0')
for tgt in ((6, 12), (12, 13), (15, 14), (18, 14)):
    print(tgt, goto(tgt, maxit=40))
print(sh(['shot r3_gap1.ppm']))
