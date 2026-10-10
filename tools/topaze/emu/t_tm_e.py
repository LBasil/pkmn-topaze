from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
N = json.load(open('/tmp/tourmalia_npc.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/tourmalia_col.json'))['blocked']} | {tuple(N[k]) for k in ('policeman_block', 'grunt', 'slowbro_block', 'lass_block', 'guard', 'cuttree', 'boy', 'balding', 'youngster', 'woman')}
start('tm_0')
sh(['writepb 03005008 1040 ff', 'writepb 03005008 1041 0f', 'writepb 03005008 f8e 80'])
print(goto((6, 20), maxit=40))
print(sh(['key RIGHT 30', 'run 40', 'shot tm_bridge.ppm']))      # pont de planches
print(sh(['key RIGHT 30', 'run 40']))
print(goto((8, 34), maxit=60)); print(sh(['key RIGHT 40', 'run 60', 'shot tm_bridge2.ppm']))
print(goto((9, 12), maxit=60)); print(sh(['key LEFT 20', 'run 40']))   # contre l'eau
