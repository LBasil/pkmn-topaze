# etape 1 : de Grenalux (etat free2) vers Opanihrum par la porte nord (ROM de test : warps Grenalux -> Opanihrum)
# On masque le grunt / le rival par les drapeaux puis on recharge la carte en entrant dans le labo et en ressortant.
from play import run
from base import *
from townlib import *
start('free2')
print(sh(['writepb 03005008 f74 80', 'writepb 03005008 f75 07', 'writepb 03005008 10e0 02']))
goto((35, 21)); print(sh(['key UP 30', 'run 100']))
print(sh(['key DOWN 30', 'run 100']))
goto((22, 3)); print(sh(['key UP 70', 'run 90', 'shot op_arrive.ppm']))
shutil.copy(CUR, S + 'opan0.ss')
