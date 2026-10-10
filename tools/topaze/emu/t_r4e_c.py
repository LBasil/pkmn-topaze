from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
P.B = {tuple(c) for c in json.load(open('/tmp/route4e_col.json'))['blocked']}
start('r4e_0')
goto((70, 15), maxit=80)
print(sh(['key RIGHT 20', 'run 100']))
print(sh(['key RIGHT 30', 'run 40', 'shot r4e_tm.ppm']))
print(sh(['key LEFT 40', 'run 100', 'shot r4e_back.ppm']))
print(sh(['key LEFT 30', 'run 40']))
