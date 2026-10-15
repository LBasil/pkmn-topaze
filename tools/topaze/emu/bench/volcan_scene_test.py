import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('SeafoamIslands_B4F', 13, 12, nocombat=False, pre=['FLAG_SEAFOAM_ALLIES_MET'])
t.e.run(60,0)
n=0; calm=0
while n<400:
    if t.idle():
        calm+=1
        if calm>=3: break
        t.e.run(20,0); continue
    calm=0
    t.press('A' if t.inbattle() else 'A',4,30); n+=1
    t.shot('v_%03d'%n)
print('n',n,t.getflag('FLAG_SEAFOAM_BOSS_DONE'))
