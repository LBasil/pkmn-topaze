import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('ViridianCity', 15, 22, nocombat=True, prevars={'VAR_TOPAZE_ENDING':2,'VAR_REFUGE_STAGE':1}, pre=['FLAG_TOPAZE_COUNCIL'])
t.face('UP'); t.press('A',4,30); n=t.scene(maxn=1200, shot='ref1'); print('ranger', n, t.sync(), 'stage', t.getvar('VAR_REFUGE_STAGE'), 'boost', t.getvar('VAR_TOPAZE_BOOST'))
