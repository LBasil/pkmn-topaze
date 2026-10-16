import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('Route25_SeaCottage', 6, 8, nocombat=True, prevars={'VAR_ROUTE25_MISTY':2,'VAR_TOPAZE_ENDING':2}, pre=['FLAG_TOPAZE_COUNCIL'])
print('start', t.where()); t.shot('misty0')
t.face('RIGHT'); t.press('A',4,30); n=t.scene(maxn=500, shot='misty'); print('misty', n, 'gift flag', t.getflag('FLAG_QUEST_MISTY_VISIT'))
