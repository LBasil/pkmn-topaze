import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('OneIsland_KindleRoad', 12, 124, nocombat=False, prevars={'VAR_ECHO_STAGE':1}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where(), t.getflag('FLAG_HIDE_ECHO_BEAST'))
t.hold('UP', 4*16-6); print(t.where()); t.shot('E2_b')
t.press('A',4,30); n=t.scene(maxn=700); print('raikou', n, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_ECHO_BEAST_DONE'), t.where()); t.shot('E2_c')
