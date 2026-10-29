#!/usr/bin/env python3
"""LOT 5 : 6 zones de capture a theme (spectres, foudre, dragons, psy, plaine, dunes) + passeuse du crepuscule. Textes anglais PROVISOIRES. Idempotent."""
import sys; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'FuchsiaCity_EventScript_DuskFerrywoman' in rd('data/maps/FuchsiaCity/scripts.inc'): print('deja applique'); raise SystemExit
Z = [
 dict(map='WhisperGrove', tpl='SevenIsland_SevaultCanyon_Grove', badge=6, lv=(36, 42), land=['MISDREAVUS', 'GASTLY', 'HAUNTER', 'DUSKULL', 'SHUPPET', 'SABLEYE', 'MURKROW', 'HOUNDOUR', 'BANETTE', 'DUSCLOPS', 'SHEDINJA', 'ABSOL'],
      ask='The GROVE OF WHISPERS: spirits drift between the trees. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('OLD_WOMAN', 'Listen. The trees whisper names of those who passed.'), ('LASS', 'MISDREAVUS sings at night. Do not sing back.')], hidden=['ELIXIR', 'MAX_ETHER', 'NUGGET'],
      quests=[dict(g='OLD_MAN_1', want=('NUGGET', 1), rew=('SPELL_TAG', 1), ask='A NUGGET pays the ferryman for a lost soul. Bring me one.', done='The soul rests. Take this SPELL TAG.', after='The grove is quieter now.', miss='No NUGGET yet. Look on the routes.', j=('THE FERRYMAN FEE', 'WHISPER GROVE: bring a NUGGET.'))]),
 dict(map='SparkGlade', tpl='SevenIsland_SevaultCanyon_Glade', badge=5, lv=(32, 38), land=['MAGNEMITE', 'VOLTORB', 'ELECTRIKE', 'MAREEP', 'PIKACHU', 'PLUSLE', 'MINUN', 'CHINCHOU', 'MAGNETON', 'ELECTRODE', 'ELECTABUZZ', 'MANECTRIC'],
      ask='The SPARK GLADE hums with static. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SCIENTIST', 'The air here is full of charge. My hair stands up, even my POKeMON\'s.'), ('BUG_CATCHER', 'I touched a VOLTORB. It was a mistake.')], hidden=['MAX_ETHER', 'ELIXIR', 'REVIVE'],
      quests=[dict(g='SCIENTIST', want=('ELIXIR', 2), rew=('MAGNET', 1), ask='My coils drain fast. Bring me 2 ELIXIRS and I will give you a prototype.', done='Perfect! Take this MAGNET.', after='The glade hums happily.', miss='Two ELIXIRS. Check the grass.', j=('THE COIL KEEPER', 'SPARK GLADE: bring 2 ELIXIRS.'))]),
 dict(map='DragonPerch', tpl='SevenIsland_SevaultCanyon_Summit', badge=8, lv=(46, 52), land=['DRATINI', 'DRAGONAIR', 'BAGON', 'SWABLU', 'ALTARIA', 'LARVITAR', 'PUPITAR', 'VIBRAVA', 'HORSEA', 'SEADRA', 'SHELGON', 'FLYGON'],
      ask='The DRAGON PERCH: the air is thin and the wings are large. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('COOLTRAINER_M', 'Dragons come here to nest. Be respectful and be fast.')], hidden=['RARE_CANDY', 'PP_UP', 'MAX_REVIVE'],
      quests=[dict(g='OLD_MAN_1', want=('DRAGON_SCALE', 1), rew=('DRAGON_FANG', 1), ask='A DRAGON SCALE for the old nest. Bring me one.', done='It fits perfectly. Take this DRAGON FANG.', after='The nest is whole again.', miss='No DRAGON SCALE yet. The stone greenhouse sells them.', j=('THE OLD NEST', 'DRAGON PERCH: bring a DRAGON SCALE.'))]),
 dict(map='ZenGarden', tpl='SafariZone_North', badge=5, lv=(32, 38), land=['ABRA', 'KADABRA', 'RALTS', 'KIRLIA', 'NATU', 'XATU', 'SPOINK', 'GIRAFARIG', 'WOBBUFFET', 'CHIMECHO', 'BALTOY', 'MR_MIME'],
      ask='The ZEN GARDEN: still water, calm minds. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('WOMAN_3', 'Sit. Breathe. The POKeMON will come to you.'), ('MAN', 'ABRA teleports when it senses a fight. Be quick.')], hidden=['ELIXIR', 'REVIVAL_HERB', 'MENTAL_HERB'],
      quests=[dict(g='OLD_WOMAN', want=('LEMONADE', 2), rew=('TWISTED_SPOON', 1), ask='Tea time! Two LEMONADEs for the garden and a gift for you.', done='Delicious! Take this TWISTED SPOON.', after='The garden is at peace.', miss='Two LEMONADEs, please. The cafe sells them.', j=('TEA FOR TWO', 'ZEN GARDEN: bring 2 LEMONADES.'))]),
 dict(map='GiantsPlain', tpl='SafariZone_East', badge=4, lv=(26, 32), land=['TAUROS', 'MILTANK', 'KANGASKHAN', 'RHYHORN', 'GIRAFARIG', 'STANTLER', 'PONYTA', 'DODUO', 'DODRIO', 'PINSIR', 'HERACROSS', 'CHANSEY'],
      ask='The PLAIN OF GIANTS: wide grass and big POKeMON. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('HIKER', 'Big POKeMON need big space. Mind the herds.'), ('CAMPER', 'TAUROS charge when they see red. Wear green.')], hidden=['ULTRA_BALL', 'MAX_REPEL', 'HYPER_POTION'],
      gifts=[('PHANPY', 15, 'A baby PHANPY got separated from its herd. Can you look after it?')], gift_name='THE LOST CALF', gift_hint='GIANTS PLAIN: a baby needs a home.',
      quests=[dict(g='FAT_MAN', want=('SODA_POP', 2), rew=('BLACK_BELT', 1), ask='Two SODA POPs for the road, friend. I will make it worth it.', done='Fizzy! Take this BLACK BELT.', after='The plain is a good place.', miss='Two SODA POPs, please. The cafe sells them.', j=('FIZZY TRADE', 'GIANTS PLAIN: bring 2 SODA POPS.'))]),
 dict(map='DuneSea', tpl='SafariZone_West', badge=5, lv=(32, 38), land=['TRAPINCH', 'CACNEA', 'SANDSHREW', 'DIGLETT', 'BALTOY', 'GLIGAR', 'PHANPY', 'NUMEL', 'SKARMORY', 'LARVITAR', 'VIBRAVA', 'SANDSLASH'],
      ask='The DUNE SEA: sand as far as the eye can see. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('HIKER', 'Water is gold here. Watch your supplies.'), ('LITTLE_GIRL', 'TRAPINCH waits in a pit. Do not fall in.')], hidden=['STARDUST', 'STAR_PIECE', 'NUGGET'],
      quests=[dict(g='OLD_MAN_1', want=('FRESH_WATER', 2), rew=('SOFT_SAND', 1), ask='Two FRESH WATERs and I will give you the sand that sings.', done='Water! Take this SOFT SAND.', after='The dunes sing for you.', miss='Two FRESH WATERs, please. The cafe sells them.', j=('WATER FOR THE DUNES', 'DUNE SEA: bring 2 FRESH WATERS.'))]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = ['# ---- LOT 5 (zones a theme)']; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
ferry('DuskFerrywoman', 'WOMAN_1', (21, 22), 'At dusk the strangest places open, {PLAYER}.', 'The dusk is not ready. Come back when the clocks make sense.', 'Another time. Dusk will come again.',
      [(z['map'], arr[z['map']], z['badge'], z['ask'], z['gt']) for z in Z])
journal_add(journal); flush_flags()
