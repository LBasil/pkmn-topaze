import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('PokemonLeague_LoreleisRoom', 6, 10, nocombat=False, prevars={'VAR_TOURNAMENT_ROUND':6,'VAR_MAP_SCENE_POKEMON_LEAGUE':1})
t.e.run(60,0)
a=t.sb()+0x3A4C
for i,v in enumerate((0xBB,0xBC,0xBD,0xBE,0xBF,0xFF)): t.e.cmd('poke8 %x %x'%(a+i,v))
print('walk', t.walk_to((6,6)), t.where())
t.face('UP')
for n in range(1,90):
    t.press('A',4,30); t.shot('z_%03d'%n)
print(t.where(), t.getvar('VAR_TOURNAMENT_ROUND'))
