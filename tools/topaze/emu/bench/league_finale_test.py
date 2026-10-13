import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('PokemonLeague_LoreleisRoom', 6, 10, nocombat=True, prevars={'VAR_TOURNAMENT_ROUND':9,'VAR_MAP_SCENE_POKEMON_LEAGUE':1}, pre=['FLAG_DEFEATED_LORELEI'])
t.e.run(60,0)
t.walk_to((6,3)); t.hold('UP', 12); t.e.run(60,0)
import os
for f in os.listdir('/tmp/gx/out'):
    if f.startswith('Z_'): os.remove('/tmp/gx/out/'+f)
n=0; i=0; calm=0
while n<900:
    if t.idle():
        calm+=1
        if calm>=3: break
        t.e.run(20,0); continue
    calm=0
    k='DOWN' if (t.inbattle() and (i:=i+1)%9==0) else 'A'
    t.press(k,4,30); n+=1
    if n%6==0: t.shot('Z_%03d'%n)
print('n',n,t.where(), t.getvar('VAR_TOPAZE_ENDING'))
for tr,name in ((752,'chen'),(753,'boss')):
    print(name, t.getflag(0x500+tr) if False else '')
