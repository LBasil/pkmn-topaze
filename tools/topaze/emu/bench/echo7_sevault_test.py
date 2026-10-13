import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
st=int(sys.argv[1]); up=int(sys.argv[2]); left=int(sys.argv[3]); fl=sys.argv[4]
t = T('SevenIsland_SevaultCanyon', 17, 7, nocombat=False, prevars={'VAR_ECHO_STAGE':st}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where(), t.getflag('FLAG_HIDE_ECHO_'+fl)); 
t.hold('UP', up); t.hold('LEFT', left); print(t.where()); t.shot('J2_'+fl)
t.press('A',4,30); n=t.scene(maxn=700); print('beast', n, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_DONE_ECHO_'+fl))
