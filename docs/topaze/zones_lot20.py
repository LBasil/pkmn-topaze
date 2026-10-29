#!/usr/bin/env python3
"""LOT 20 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'CrickPond' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='CrickPond', tpl='Route25', badge=1, lv=(4, 9), land=['POLIWAG', 'GOLDEEN', 'LOTAD', 'WOOPER', 'MARILL', 'PSYDUCK', 'SURSKIT', 'RATTATA', 'PIDGEY', 'CATERPIE', 'ZIGZAGOON', 'AZURILL'],
      ask='The CRICK POND: small ripples, small friends. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('LITTLE_BOY', 'I heard a splash. Then nothing. Spooky.'), ('LASS', 'MARILL floats like a ball. Cute.')], hidden=[], quests=[]),
 dict(map='PineRow', tpl='ViridianForest', badge=2, lv=(12, 18), land=['PINECO', 'SPINARAK', 'HOOTHOOT', 'SENTRET', 'EKANS', 'ODDISH', 'SEEDOT', 'NINCADA', 'SHROOMISH', 'PARAS', 'WEEDLE', 'KAKUNA'],
      ask='The PINE ROW: tall trunks and quiet needles. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('BUG_CATCHER', 'PINECO hangs from the trunks. Shake gently.'), ('OLD_MAN_1', 'These trees are older than the town.')], hidden=[], quests=[]),
 dict(map='SaltyDunes', tpl='SafariZone_West', badge=3, lv=(18, 24), land=['SANDSHREW', 'SANDSLASH', 'TRAPINCH', 'CACNEA', 'BALTOY', 'DIGLETT', 'KRABBY', 'WINGULL', 'SKIPLOOM', 'MEOWTH', 'CUBONE', 'GEODUDE'],
      ask='The SALTY DUNES: sand, wind and sea spray. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('SAILOR', 'The sea is just beyond. The sand tells me so.'), ('LITTLE_BOY', 'I built a castle. A TRAPINCH ate it.')], hidden=[], quests=[]),
 dict(map='TwilightGlen', tpl='Route22', badge=5, lv=(30, 36), land=['MURKROW', 'MISDREAVUS', 'HAUNTER', 'GASTLY', 'DUSKULL', 'SHUPPET', 'UMBREON', 'NOCTOWL', 'GLIGAR', 'SABLEYE', 'MIGHTYENA', 'HOUNDOUR'],
      ask='The TWILIGHT GLEN: everything is a shade of blue. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('OLD_WOMAN', 'It is always dusk here. Do not ask me why.'), ('LASS', 'MISDREAVUS whispers my name. I am leaving.')], hidden=[], quests=[]),
 dict(map='SteelGarden', tpl='SafariZone_East', badge=6, lv=(36, 42), land=['SKARMORY', 'STEELIX', 'MAGNETON', 'FORRETRESS', 'MAWILE', 'ARON', 'LAIRON', 'NOSEPASS', 'ONIX', 'GRAVELER', 'PINSIR', 'SCIZOR'],
      ask='The STEEL GARDEN: metal flowers that never wilt. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('SCIENTIST', 'Magnetic fields everywhere. My watch is dead.'), ('GENTLEMAN', 'A garden that needs no water. Practical.')], hidden=[], quests=[]),
 dict(map='RainbowFalls', tpl='Route4', badge=8, lv=(50, 56), land=['MILOTIC', 'GYARADOS', 'KINGDRA', 'SEADRA', 'LAPRAS', 'VAPOREON', 'SUICUNE'.replace('SUICUNE', 'GOLDUCK'), 'STARMIE', 'POLIWRATH', 'WALREIN', 'LUDICOLO', 'SWAMPERT'],
      ask='The RAINBOW FALLS: a rainbow, a waterfall and big splashes. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('OLD_MAN_1', 'A rainbow every morning. I never get tired.'), ('LASS', 'MILOTIC is the most beautiful thing I have seen.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
