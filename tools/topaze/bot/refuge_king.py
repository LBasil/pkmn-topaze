import sys
sys.path.insert(0,'/tmp/gx')
from play import *
t=Player.resume('refuge_15'); RF.R.SURF=True
TRIES=5
BUFF = 'BUFF' in __import__('os').environ      # validation du SCRIPT seulement (niveau 100) : l'equilibrage est evalue a part
try: RF.sail_to(t, 0)
except AssertionError: pass
t.heal(True); assert t.go('FuchsiaCity_SafariZone_Entrance'); t.e.run(60,0)
log('stage', t.getvar('VAR_REFUGE_STAGE'), [(q['level'],q['hp']) for q in t.party()])
if BUFF: RF.Auto.buff(t); log('  (equipe gonflee : test du script, pas de l equilibrage)')
for k in range(TRIES):
    if t.sync()!='FuchsiaCity_SafariZone_Entrance': assert t.go('FuchsiaCity_SafariZone_Entrance'); t.e.run(60,0)
    t.walk_to((3,6)); t.face('LEFT'); t.press('A',4,40); t.mash(40); t.scene(900)

    for _ in range(8):
        if not t.inbattle(): break
        t.finish_battle(maxn=900); t.scene(maxn=300)
    t.scene(maxn=300)
    log('ROI stage', t.getvar('VAR_REFUGE_STAGE'), t.sync())
    if t.getvar('VAR_REFUGE_STAGE') >= 17: break
    top=max(q['level'] for q in t.party()); t.too_strong=top+5; log('  duel perdu : entrainement jusqu au niveau', top+5); t.use_candies(0, upto=top+5); t.ensure(top+5); t.heal(True)
t.save('refuge_king')
for pat in ('InfoAttendant','InfoAttendant'):
    try: t.walk_to((3,6)); t.face('LEFT'); t.press('A',4,40); t.mash(40); t.scene(maxn=300); log(pat, 'stage', t.getvar('VAR_REFUGE_STAGE'))
    except AssertionError as e: log('BLOCK', pat, e)
