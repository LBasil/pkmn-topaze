import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
st=int(sys.argv[1])
t = T('FourIsland_LoreleisHouse', 7, 6, nocombat=True, prevars={'VAR_ECHO_STAGE':st}, pre=['FLAG_TOPAZE_POSTGAME'])
t.hold('UP', 12); print(t.where())
t.press('A',4,30); n=t.scene(maxn=600); print('lorelei', st, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_HIDE_ECHO_BEAST4'))
