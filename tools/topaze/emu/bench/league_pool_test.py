import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('PokemonLeague_LoreleisRoom', 6, 10, nocombat=True, prevars={'VAR_TOURNAMENT_ROUND':0})
print('start', t.where(), t.getvar('VAR_TOURNAMENT_ROUND'))
t.scene(); t.shot('L_enter')
for r in range(9):
    ok = t.walk_to((6,6)); t.face('UP'); t.shot('L_r%d_face' % r)
    t.press('A',4,30)
    n = t.scene(maxn=900)
    print('round', r, 'ok', ok, 'presses', n, 'var', t.getvar('VAR_TOURNAMENT_ROUND'), t.where())
    t.shot('L_r%d_done' % r)
    t.e.run(120,0)
    t.scene(maxn=60)
print('end', t.where(), t.getflag('FLAG_DEFEATED_LORELEI'))
