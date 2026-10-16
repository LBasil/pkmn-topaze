import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('IndigoPlateau_PokemonCenter_1F', 11, 13, nocombat=True, prevars={'VAR_TOPAZE_ENDING':3,'VAR_REBELS_ROUND':8}, pre=['FLAG_TOPAZE_COUNCIL','FLAG_DEFEATED_CHAMP'])
t.face('DOWN'); t.press('A',4,30); n=t.scene(maxn=900, shot='reb'); print('scene', n, t.sync(), 'round', t.getvar('VAR_REBELS_ROUND'), 'boost', t.getvar('VAR_TOPAZE_BOOST'))
for k in range(8):
    if t.inbattle(): t.finish_battle()
    t.scene(maxn=400)
print('after', t.sync(), 'round', t.getvar('VAR_REBELS_ROUND'), 'boost', t.getvar('VAR_TOPAZE_BOOST'))
