import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('FourIsland_IcefallCave_Back', 12, 18, nocombat=False, prevars={'VAR_ECHO_STAGE':10}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where(), t.getflag('FLAG_HIDE_ECHO_BEAST4')); t.shot('H2_a')
t.hold('UP', 2*16+10); print(t.where())
t.press('A',4,30); n=t.scene(maxn=700); print('regice', n, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_ECHO_BEAST4_DONE'), t.where())
