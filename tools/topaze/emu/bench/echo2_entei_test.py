import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('TwoIsland_CapeBrink', 12, 33, nocombat=False, prevars={'VAR_ECHO_STAGE':4}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where(), t.getflag('FLAG_HIDE_ECHO_BEAST2'))
t.hold('UP', 3*16+8); print(t.where()); t.shot('F2_b')
t.press('A',4,30); n=t.scene(maxn=700); print('entei', n, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_ECHO_BEAST2_DONE'), t.where())
