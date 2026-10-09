from play import run
from base import *
from townlib import *
import json
P.B = {tuple(c) for c in json.load(open('/tmp/pyropia_col.json'))['blocked']}
NP = json.load(open('/tmp/pyropia_npc.json')); SG = json.load(open('/tmp/pyropia_signs.json'))
P.B |= {tuple(c) for k, c in NP.items() if k != 'hidden'} | {(22, 39), (23, 39), (47, 25), (47, 26)}
start('py_0'); sh(['key UP 18', 'run 20'])
for n, face in (('lass', 'DOWN'), ('fatman', 'UP'), ('bugcatcher', 'UP')):
    x, y = NP[n]
    for tgt, f in (((x, y + 1), 'UP'), ((x, y - 1), 'DOWN'), ((x - 1, y), 'RIGHT'), ((x + 1, y), 'LEFT')):
        try: goto(tgt); break
        except Exception: continue
    print(n, tgt, sh(talk(f, 'py_npc_' + n, 2)))
for n, (x, y) in SG.items():
    for tgt, f in (((x, y + 1), 'UP'), ((x, y - 1), 'DOWN'), ((x - 1, y), 'RIGHT'), ((x + 1, y), 'LEFT')):
        try: goto(tgt); break
        except Exception: continue
    print(n, tgt, sh(talk(f, 'py_sgn_' + n, 2)))
goto((45, 25)); print('est ->', sh(['key RIGHT 70', 'run 120', 'shot py_r3.ppm']))
print('retour', sh(['key RIGHT 18', 'run 20', 'key LEFT 50', 'run 120']))
goto((22, 38)); print('sud ->', sh(['key DOWN 70', 'run 120', 'shot py_r2.ppm']))
print('retour', sh(['key DOWN 18', 'run 20', 'key UP 50', 'run 120']))
