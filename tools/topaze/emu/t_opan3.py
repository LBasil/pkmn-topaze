# etape 4 : sorties : nord (route 2) et retour ; ouest (route 22) et retour ; sud (route 1) et retour
from play import run
from base import *
from townlib import *
start('opan2')
print(sh(['key B 4', 'run 40'] * 14 + ['run 60']))
r = sh(['key UP 50', 'run 120', 'shot rt2_arrive.ppm']); print('nord ->', r)
r = sh(['key UP 18', 'run 20', 'key DOWN 40', 'run 120', 'shot rt2_back.ppm']); print('retour route2 ->', r)
goto((3, 22)); r = sh(['key LEFT 70', 'run 120', 'shot rt22_arrive.ppm']); print('ouest ->', r)
r = sh(['key LEFT 18', 'run 20', 'key RIGHT 50', 'run 120', 'shot rt22_back.ppm']); print('retour route22 ->', r)
goto((21, 37)); r = sh(['key DOWN 70', 'run 120', 'shot rt1_arrive.ppm']); print('sud ->', r)
r = sh(['key DOWN 18', 'run 20', 'key UP 50', 'run 120', 'shot rt1_back.ppm']); print('retour route1 ->', r)
shutil.copy(CUR, S + 'opan3.ss')
