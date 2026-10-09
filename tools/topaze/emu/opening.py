# Rejoue l'ouverture complete de Grenalux (v6) et enregistre l'etat "free2" : dehors, devant le labo, starter + rival battu
# (a relancer apres chaque changement de ROM : les etats ne survivent pas a une recompilation)
from play import run
from base import *
from townlib import *
print(run(OUT+['key DOWN 40','run 120','readp 03005008 0 6','ss ' + S + 'town1.ss'], show=False)[-1])
start('town1')
goto((22,3)); print(sh(['key UP 40','run 60']))
print(sh(['key A 4','run 50']*40))
print(sh(['key A 4','run 70']*40))
print(sh(['key B 4','run 20']*4+walk('RIGHT',1)+['key RIGHT 4','run 20']))
print(sh(['key A 4','run 90']*3+['key DOWN 4','run 10','key A 4','run 100']+['key A 4','run 80']*4+['run 100']))
print(sh(['key B 4','run 12']*3+['key START 4','run 80']+['key A 4','run 80']*6+['run 100']))
print(sh(walk('DOWN',8)+['run 60']))
print(sh(['key A 4','run 60']*60+['run 200']))
print(sh(['key A 4','run 80']*25+['run 150']))
print(sh(walk('DOWN',4)+['run 100']))
print(sh(walk('LEFT',1)+['key DOWN 30','run 120']))
print(where())
shutil.copy(CUR, S + 'free2.ss')
