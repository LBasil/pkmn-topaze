from play import run
from base import *
from townlib import *
import json
P.B = {tuple(c) for c in json.load(open('/tmp/pyropia_col.json'))['blocked']}
NP = json.load(open('/tmp/pyropia_npc.json')); DR = json.load(open('/tmp/pyropia_doors.json'))
P.B |= {tuple(c) for k, c in NP.items() if k != 'hidden'}
P.B |= {(22, 39), (23, 39)} | {(47, 25), (47, 26)}
start('py_0')
sh(['key UP 18', 'run 20'])
for k, (x, y) in DR.items():
    goto((x, y + 1))
    r = sh(['key UP 40', 'run 100', 'shot py_in_%s.ppm' % k]); print(k, 'entre ->', r)
    r = sh(['key DOWN 40', 'run 100']); print('   sortie ->', r)
    sh(['key B 4', 'run 20'] * 4)
shutil.copy(CUR, S + 'py_1.ss')
