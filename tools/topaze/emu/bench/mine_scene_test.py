import sys,os; sys.path.insert(0,'/tmp/gx')
from tz import *
from mtest import plan
os.chdir('/home/claude/pkmn-topaze')
t=T('GrenaluxMine_1F',18,36,nocombat=True,pre=['FLAG_TOPAZE_POSTGAME'])
t.e.run(60,0); t.sync()
for st in plan('GrenaluxMine_1F',(18,37),'GrenaluxMine_3F',(14,12))[:-1]: t.chain([st])
t.chain([(14,12)]); print(t.where())
for f in os.listdir('/tmp/gx/out'):
    if f.startswith('V_'): os.remove('/tmp/gx/out/'+f)
t.e.run(16,KEYS['UP']); t.e.run(20,0)
for i in range(60):
    t.press('A',4,40); t.shot('V_%02d'%i)
    if t.idle() and t.getflag('FLAG_MEW_FLED'): break
print(i,t.getflag('FLAG_MEW_FLED'),t.where())
