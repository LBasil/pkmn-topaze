import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('SevenIsland_SevaultCanyon', 17, 10, nocombat=False, prevars={'VAR_ECHO_STAGE':21}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where(), t.getflag('FLAG_HIDE_ECHO_SCENE'))
t.hold('UP', 40)
n=t.scene(maxn=1500); print('scene', n, t.getvar('VAR_ECHO_STAGE'), t.where()); t.shot('K1_end')
