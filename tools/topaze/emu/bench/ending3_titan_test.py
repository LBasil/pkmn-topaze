import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
for m, x, y, f in (('SeafoamIslands_B4F', 19, 11, 'FLAG_FOUGHT_TITAN_KYOGRE'), ('MtEmber_RubyPath_1F', 22, 15, 'FLAG_FOUGHT_TITAN_GROUDON'), ('IndigoPlateau_Exterior', 9, 10, 'FLAG_FOUGHT_TITAN_RAYQUAZA')):
    t = T(m, x, y, nocombat=True, prevars={'VAR_TOPAZE_ENDING':3,'VAR_REBELS_ROUND':9}, pre=['FLAG_TOPAZE_COUNCIL'])
    t.shot('titan_' + m); t.face('UP'); t.press('A',4,30); n=t.scene(maxn=900, shot='titan2_'+m)
    for k in range(6):
        if t.inbattle(): t.finish_battle(maxn=900)
        t.scene(maxn=300)
    print(m, n, t.sync(), t.pos(), 'fought', t.getflag(f))
