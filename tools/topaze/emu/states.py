from pl import *
from base import OUT
import sys
which=sys.argv[1] if len(sys.argv)>1 else 'Charmander'
ball={'Bulbasaur':2,'Squirtle':3,'Charmander':4}[which]   # RIGHT steps depuis (6,5)
run(OUT+walk('DOWN',2)+['run 200','ss '+S+'pallet.ss'])
fromstate('pallet',walk('RIGHT',5)+walk('UP',5)+walk('RIGHT',2)+['key UP 16','run 1','key UP 16','run 1','run 60']+['key A 4','run 90']*6+['ss '+S+'oak.ss'])
fromstate('oak',['key A 4','run 60']*20+['ss '+S+'lab.ss'])
fromstate('lab',['key A 4','run 70']*10+['run 60','ss '+S+'lab2.ss'])
fromstate('lab2',walk('DOWN',1)+walk('RIGHT',ball)+['key UP 4','run 20']+['key A 4','run 90']*4+['run 150','key A 4','run 120','ss '+S+'starter.ss'])
fromstate('starter',['key DOWN 4','run 10','key A 4','run 100']+['key A 4','run 80']*3+['run 100','ss '+S+'free.ss'])
fromstate('free',walk('DOWN',1)+walk('LEFT',ball)+walk('DOWN',7)+['run 100']+['key A 4','run 80']*7+['ss '+S+'rivalbattle.ss'])
print('ok')
