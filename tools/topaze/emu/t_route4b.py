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
def walk(t):
    for k in range(8):
        try: return goto(t, maxit=40)
        except AssertionError as e:
            print('interrompu', e)
            sh(['key A 4', 'run 90', 'key A 4', 'run 90', 'key DOWN 4', 'run 12', 'key RIGHT 4', 'run 12', 'key A 4', 'run 160', 'key A 4', 'run 60', 'key B 4', 'run 30'])
    raise AssertionError(('abandon', t))
def nb(t):
    for r in range(0,6):
        for dx in range(-r,r+1):
            for dy in range(-r,r+1):
                c=(t[0]+dx,t[1]+dy)
                if c not in P.B and 0<=c[0]<40 and 0<=c[1]<84: return c
for tgt in map(nb, ((19, 78), (14, 72), (16, 66), (24, 64), (30, 64), (31, 58), (22, 54), (20, 53))):
    print(tgt, walk(tgt))
print(sh(['shot r4_end.ppm']))
