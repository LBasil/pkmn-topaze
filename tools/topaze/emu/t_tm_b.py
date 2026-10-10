from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
N = json.load(open('/tmp/tourmalia_npc.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/tourmalia_col.json'))['blocked']} | {tuple(v) for k, v in N.items() if k in ('policeman', 'grunt', 'slowbro', 'lass', 'guard', 'cuttree', 'boy', 'balding', 'youngster', 'woman')}
start('tm_0')
sh(['writepb 03005008 1040 ff', 'writepb 03005008 1041 0f', 'writepb 03005008 f8e 80'])
for name, tgt, face in (('center', (13, 17), 'UP'), ('gym', (30, 17), 'UP'), ('mart', (34, 24), 'UP')):
    print(name, goto(tgt, maxit=40))
    print(sh(['shot tm_%s.ppm' % name, 'key UP 20', 'run 120', 'shot tm_%s_in.ppm' % name]))
    print(sh(['key DOWN 20', 'run 120']))
