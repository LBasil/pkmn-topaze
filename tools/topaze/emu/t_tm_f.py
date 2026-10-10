from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
N = json.load(open('/tmp/tourmalia_npc.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/tourmalia_col.json'))['blocked']} | {tuple(N[k]) for k in ('policeman', 'grunt', 'slowbro', 'lass', 'guard', 'cuttree', 'boy', 'balding', 'youngster', 'woman')}
for name, tgt, key in (('nord', (23, 1), 'UP'), ('grove', (41, 32), 'UP'), ('sw', (5, 34), 'UP')):
    start('tm_0'); sh(['writepb 03005008 1040 ff', 'writepb 03005008 1041 0f', 'writepb 03005008 f8e 80'])
    try: print(name, goto(tgt, maxit=70), sh(['key %s 20' % key, 'run 100']))
    except AssertionError as e: print(name, 'FAIL', e)
