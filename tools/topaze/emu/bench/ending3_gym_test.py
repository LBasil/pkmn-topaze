import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('PewterCity_Gym', 6, 6, nocombat=True, prevars={'VAR_TOPAZE_ENDING':3}, pre=['FLAG_TOPAZE_COUNCIL','FLAG_DEFEATED_BROCK','FLAG_GOT_TM39_FROM_BROCK'])
t.flag(0x500+414)
t.face('UP'); t.press('A',4,30); n=t.scene(maxn=900, shot='kay'); print('kay', n, t.sync(), 'flag', t.getflag('FLAG_REBEL_KAY'), 'boost', t.getvar('VAR_TOPAZE_BOOST'))
