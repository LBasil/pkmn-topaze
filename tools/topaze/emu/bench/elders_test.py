import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('PokemonLeague_LoreleisRoom', 6, 10, nocombat=True, prevars={'VAR_TOURNAMENT_ROUND':9,'VAR_ELDERS_ROUND':0,'VAR_MAP_SCENE_POKEMON_LEAGUE':1}, pre=['FLAG_DEFEATED_LORELEI','FLAG_TOPAZE_POSTGAME'])
print('start', t.where())
t.scene()
for r in range(21):
    ok = t.walk_to((6,6)); t.face('UP')
    t.press('A',4,30)
    n = t.scene(maxn=900)
    print('elder', r, ok, n, t.getvar('VAR_ELDERS_ROUND'), t.where(), 'item' , t.getflag('FLAG_TOPAZE_POSTGAME'))
    t.shot('E_%d'%r)
    t.e.run(120,0); t.scene(maxn=60)
