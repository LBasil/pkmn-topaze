import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
t = T('VictoryRoadLair_3F', 6, 12, nocombat=True)
t.e.run(60,0)
print('start', t.where())
t.hold('UP', 40); t.e.run(40,0)
print('after walk', t.where(), t.idle())
n=0; calm=0
while n<200:
    if t.idle() and n>0 or (t.idle() and n==0 and t.getvar('VAR_TEMP_1')==1):
        calm+=1
        if calm>=3: break
        t.e.run(20,0); continue
    calm=0
    t.press('A',4,30); n+=1
    t.shot('l_%03d'%n)
print('n',n,'VR_BOSS_DONE',t.getflag('FLAG_VR_BOSS_DONE'), t.where())
