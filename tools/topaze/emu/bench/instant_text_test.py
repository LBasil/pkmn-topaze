import sys; sys.path.insert(0,'/tmp/gx')
from tz import *
fl=['FLAG_TOPAZE_COUNCIL','FLAG_DEFEATED_CHAMP','FLAG_REBEL_KAY','FLAG_REBEL_SYLVESTRE','FLAG_REBEL_HERA','FLAG_REBEL_GRIM','FLAG_REBEL_ACHLYS','FLAG_REBEL_NOX','FLAG_REBEL_EDDIE']
t = T('IndigoPlateau_PokemonCenter_1F', 11, 13, nocombat=True, prevars={'VAR_TOPAZE_ENDING':3,'VAR_REBELS_ROUND':0}, pre=fl)
sb2 = t.e.u32(0x0300504c); b = t.e.peek(sb2 + 0x14, 1)[0]; t.e.cmd('poke8 %x %x' % (sb2 + 0x14, (b & ~7) | 3))
print('speed', t.e.peek(sb2 + 0x14, 1)[0] & 7)
t.face('DOWN'); t.press('A', 4, 1)
for k in range(12):
    t.e.run(3, 0); t.shot('inst_%02d' % k)
