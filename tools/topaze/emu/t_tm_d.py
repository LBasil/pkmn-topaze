from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
N = json.load(open('/tmp/tourmalia_npc.json')); M = json.load(open('/tmp/tourmalia_misc.json'))
P.B = {tuple(c) for c in json.load(open('/tmp/tourmalia_col.json'))['blocked']} | {tuple(N[k]) for k in ('policeman_block', 'grunt', 'slowbro_block', 'lass_block', 'guard', 'cuttree', 'boy', 'balding', 'youngster', 'woman')}
start('tm_0')
sh(['writepb 03005008 1040 ff', 'writepb 03005008 1041 0f', 'writepb 03005008 f8e 80'])
print(goto((10, 5), maxit=60), sh(['shot tm_ladder0.ppm']))
print(sh(['key UP 12', 'run 30', 'shot tm_ladder1.ppm']))
print(sh(['key UP 12', 'run 30', 'shot tm_ladder2.ppm']))
print(sh(['key DOWN 40', 'run 60']))
# policeman : voie est
print(goto((40, 19), maxit=60))
print(sh(['key RIGHT 14', 'run 40', 'shot tm_police.ppm']))
print(goto((24, 30), maxit=60))
print(sh(['key DOWN 14', 'run 40', 'shot tm_slow.ppm']))
