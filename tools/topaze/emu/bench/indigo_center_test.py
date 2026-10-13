import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('IndigoPlateau_PokemonCenter_1F', 12, 16, nocombat=True)
t.e.run(60,0)
for nm,pos in (('brice',(10,15)),('flora',(11,15)),('misty',(12,15))):
    ok=t.walk_to(pos); t.face('UP'); t.press('A',4,30); t.shot('IC_'+nm); t.e.run(20,0)
    for _ in range(8): t.press('B',4,25)
    print(nm, ok, t.where())
