from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
N = json.load(open('/tmp/tourmalia_npc.json')); D = json.load(open('/tmp/tourmalia_doors.json')); M = json.load(open('/tmp/tourmalia_misc.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/tourmalia_col.json'))['blocked']} | {tuple(N[k]) for k in ('policeman_block', 'grunt', 'slowbro_block', 'lass_block', 'guard', 'cuttree', 'boy', 'balding', 'youngster', 'woman')}
start('tm_0')
sh(['writepb 03005008 1040 ff', 'writepb 03005008 1041 0f', 'writepb 03005008 f8e 80'])
back = (0, 19)
for name in ('th1', 'th2', 'th3', 'th4', 'th5', 'th6'):
    t = tuple(D[name][0])
    try: print(name, goto(t, maxit=60))
    except AssertionError as e: print(name, 'FAIL', e)
    print(sh(['run 100']))
    print(sh(['shot tm_%s.ppm' % name, 'key DOWN 20', 'run 120']))
