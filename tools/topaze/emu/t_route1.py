# Route 1 (route du degrade) : Grenalux -> Route 1 -> Opanihrum et retour, en suivant le chemin (herbes hautes evitees)
from play import run
from base import *
from townlib import *
import json
import grenalux_paths as P
info = json.load(open('/tmp/route1_info.json'))
P.B |= {(x, y) for (x0, y0, x1, y1) in info['tall'] for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}
start('free2')
print(sh(['writepb 03005008 f74 80', 'writepb 03005008 f75 07', 'writepb 03005008 10e0 02']))
