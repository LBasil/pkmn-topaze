import sys, os
sys.path.insert(0,'/tmp/gx')
from play import *
os.chdir('/home/claude/pkmn-topaze')
t=Player.resume('refuge_king'); RF.R.SURF=True
sb2=t.e.u32(0x0300510c)
for _ in range(12): t.press('B',4,30)      # l'etat sauve est dans le menu du marche
t.scene(maxn=200)
for f in ('FLAG_SYS_NATIONAL_DEX','FLAG_SYS_POKEDEX_GET'):
    try: t.flag(f)
    except Exception as ex: log('flag?',f,ex)
for stage_need in (200, 300):
    nb = (stage_need + 7)//8 + 1
    sb1 = t.e.u32(0x03005108)
    for i in range(nb):      # possedes = vus dans les 3 copies (anti-triche du jeu)
        for a in (sb2 + 0x28 + i, sb2 + 0x5c + i, sb1 + 0x5F8 + i, sb1 + 0x3A18 + i): t.e.cmd('poke8 %x ff' % a)
    for k in range(3):
        if t.sync()!='FuchsiaCity_SafariZone_Entrance': assert t.go('FuchsiaCity_SafariZone_Entrance')
        t.walk_to((3,6)); t.face('LEFT'); t.press('A',4,40); 
        for i in range(18):
            t.e.run(40, 0)
            if i % 2 == 1: t.press('A', 4, 10)
        t.scene(maxn=300)
        for _ in range(10): t.press('B',4,30)
        log('stage', t.getvar('VAR_REFUGE_STAGE'), [q['species'] for q in t.party()])
        if t.getvar('VAR_REFUGE_STAGE') >= (18 if stage_need == 200 else 19): break
log('RESULTAT fin 2 chaine : stage', t.getvar('VAR_REFUGE_STAGE'))
t.save('end2_chain_done')
