import sys, os
sys.path.insert(0,'/tmp/gx')
from play import *
w=int(sys.argv[1]); RF.WISH=w
t=Player.resume('league_won')
log('=== FIN', w+1, 'depuis league_won', [(q['level'],q['hp']) for q in t.party()])
orig = t.press
state = {'in': False}
def press(k, *a, **kw):
    if k == 'A':
        act = RF.multichoice_active(t)
        if act and not state['in']:
            state['in'] = True; log('  menu des voeux : choix', w)
            for _ in range(w): orig('DOWN', 4, 20)
        if not act: state['in'] = False
    return orig(k, *a, **kw)
t.press = press
RF.WISH = 0
RF.league_finale(t)
log('RESULTAT fin', t.getvar('VAR_TOPAZE_ENDING'), 'postgame', t.getflag('FLAG_TOPAZE_POSTGAME'), t.sync(), t.pos()[2:])
t.save('end%d_done' % (w+1))
