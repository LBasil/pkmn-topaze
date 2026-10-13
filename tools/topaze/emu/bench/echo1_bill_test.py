import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('OneIsland_PokemonCenter_1F', 9, 8, nocombat=True, prevars={'VAR_ECHO_STAGE':0,'VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F':7}, pre=['FLAG_TOPAZE_POSTGAME'])
print('start', t.where())
ok = t.walk_to((14,7)); print('walk', ok, t.where()); t.face('UP'); t.press('A',4,30); n=t.scene(maxn=700); print('bill', n, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_HIDE_ECHO_BEAST')); t.shot('E1_bill')
ok = t.walk_to((15,7)); t.face('UP'); t.press('A',4,30); n=t.scene(maxn=300); print('celio wait', n, t.getvar('VAR_ECHO_STAGE')); t.shot('E1_celio')
