import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('ThreeIsland_BondBridge', 34, 10, nocombat=False, prevars={'VAR_ECHO_STAGE':7}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where(), t.getflag('FLAG_HIDE_ECHO_BEAST3'))
t.hold('LEFT', 3*16+8); print(t.where()); t.shot('G2_b')
t.press('A',4,30); n=t.scene(maxn=700); print('suicune', n, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_ECHO_BEAST3_DONE'), t.where())
