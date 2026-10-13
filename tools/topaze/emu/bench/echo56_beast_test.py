import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
m,x,y,st,hold,fl=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
t = T(m, x, y, nocombat=False, prevars={'VAR_ECHO_STAGE':st}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where(), t.getflag('FLAG_HIDE_ECHO_BEAST'+fl)); t.shot('I2_'+fl)
t.hold('UP', hold); print(t.where()); t.press('A',4,30); n=t.scene(maxn=700); print('beast', n, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_ECHO_BEAST%s_DONE'%fl))
