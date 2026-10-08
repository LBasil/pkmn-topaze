import subprocess
from pl import *
subprocess.run(['python3','states.py','Charmander'],check=True)
M,k=mash(40,40,'f',gap=60)
fromstate('rivalbattle',['key A 4','run 70']*14+['run 120']+['key A 4','run 50','key A 4','run 30','key DOWN 4','run 12','key A 4','run 120']+M+['run 100']+['key A 4','run 60']*6+['run 200','ss '+S+'post2.ss'])
fromstate('post2',walk('DOWN',4)+['run 30']+walk('DOWN',2)+['run 90','key B 4','run 30']+walk('LEFT',6)+walk('UP',12)+walk('DOWN',1)+walk('RIGHT',3)+walk('UP',5)+['run 20','ss '+S+'rt1.ss'])
fromstate('rt1',['key A 4','run 40']*6+['key B 4','run 30']+walk('UP',5)+[pos(),'ss '+S+'rt1b.ss'])
