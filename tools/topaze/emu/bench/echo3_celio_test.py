import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
st=int(sys.argv[1])
t = T('OneIsland_PokemonCenter_1F', 9, 8, nocombat=True, prevars={'VAR_ECHO_STAGE':st,'VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F':7}, pre=['FLAG_TOPAZE_POSTGAME'])
ok = t.walk_to((15,7)); t.face('UP'); t.press('A',4,30); n=t.scene(maxn=600); print('bill', st, ok, t.getvar('VAR_ECHO_STAGE'), t.getflag('FLAG_HIDE_ECHO_BEAST3'))
