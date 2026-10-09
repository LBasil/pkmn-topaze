import sys
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
which = sys.argv[1]
sh(['writepb 03005008 f8e 80'])
if which == 'center': tgt, key = (24, 17), 'UP'
elif which == 'cave1': tgt, key = (40, 10), 'UP'
elif which == 'cave2': tgt, key = (68, 10), 'UP'
else: tgt, key = (94, 15), 'RIGHT'
for t in {'center': [(12, 12), (24, 17)], 'cave1': [(12, 12), (30, 16), (40, 10)], 'cave2': [(12, 12), (30, 16), (46, 11), (60, 15), (68, 10)], 'cer': [(12, 12), (30, 16), (46, 11), (60, 15), (72, 11), (90, 16), (94, 15)]}[which]:
    try: goto(t, maxit=40)
    except AssertionError as e:
        for _ in range(60): sh(['key A 4', 'run 70'])
        sh(['key B 4','run 30']); goto(t, maxit=40); continue
    except Exception as e: print(e); sh(['shot r4_dbg.ppm']); print(info['obj'], info['face'], info['sight']); raise
print(which, sh(['key %s 20' % key, 'run 120', 'key %s 20' % key, 'run 120', 'shot r4_%s.ppm' % which]))
