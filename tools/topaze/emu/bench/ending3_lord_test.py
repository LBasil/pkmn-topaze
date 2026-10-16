import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('OneIsland', 13, 9, nocombat=True, prevars={'VAR_TOPAZE_ENDING':3,'VAR_REBELS_ROUND':8}, pre=['FLAG_TOPAZE_COUNCIL','FLAG_SYS_GAME_CLEAR'])
t.face('UP'); t.press('A',4,30); n=t.scene(maxn=900, shot='lord1'); print('lord', n, t.sync(), 'flag', t.getflag('FLAG_LORD_ONE'), 'boost', t.getvar('VAR_TOPAZE_BOOST'))
