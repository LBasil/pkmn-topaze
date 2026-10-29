#!/usr/bin/env python3
"""LOT 23 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'TumbleweedTrail' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='TumbleweedTrail', tpl='Route22', badge=2, lv=(12, 18), land=['SANDSHREW', 'DIGLETT', 'MEOWTH', 'RATTATA', 'SPEAROW', 'EKANS', 'GEODUDE', 'ZIGZAGOON', 'SKITTY', 'PIDGEY', 'NINCADA', 'SENTRET'],
      ask='The TUMBLEWEED TRAIL: dry wind, rolling bushes. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('OLD_MAN_1', 'The tumbleweeds are faster than my knees.'), ('YOUNGSTER', 'I chased one for an hour. It won.')], hidden=[], quests=[]),
 dict(map='MarbleHall', tpl='SafariZone_Center', badge=3, lv=(18, 24), land=['CLEFAIRY', 'JIGGLYPUFF', 'SKITTY', 'MEOWTH', 'PERSIAN', 'SPOINK', 'NUMEL', 'ABRA', 'KADABRA', 'PIKACHU', 'CHANSEY', 'SNUBBULL'],
      ask='The MARBLE HALL: a quiet gallery open to the sky. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('GENTLEMAN', 'A fine hall. A little too many POKéMON.'), ('LASS', 'CHANSEY is lucky. And so am I.')], hidden=[], quests=[]),
 dict(map='BoneyardRise', tpl='Route4', badge=5, lv=(30, 36), land=['CUBONE', 'MAROWAK', 'GRAVELER', 'GOLEM', 'SKARMORY', 'ONIX', 'SANDSLASH', 'DUSKULL', 'GLIGAR', 'HOUNDOUR', 'MIGHTYENA', 'SABLEYE'],
      ask='The BONEYARD RISE: old bones, old stories. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('HIKER', 'CUBONE wears its mother skull. Respect.'), ('OLD_WOMAN', 'Do not take a bone. They remember.')], hidden=[], quests=[]),
 dict(map='LavaLagoon', tpl='SafariZone_West', badge=6, lv=(38, 44), land=['MAGCARGO', 'TORKOAL', 'CAMERUPT', 'MAGMAR', 'RAPIDASH', 'NINETALES', 'SLUGMA', 'NUMEL', 'WAILMER', 'KRABBY', 'KINGLER', 'OCTILLERY'],
      ask='The LAVA LAGOON: red water, hot air. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('SAILOR', 'Swimming here is a bad idea. I tried.'), ('SCIENTIST', 'Water and lava share one pool. Impossible!')], hidden=[], quests=[]),
 dict(map='DozyDell', tpl='ViridianForest', badge=2, lv=(12, 18), land=['SLAKOTH', 'HOOTHOOT', 'NOCTOWL', 'SNORLAX', 'HOUNDOUR', 'DROWZEE', 'SPINARAK', 'ODDISH', 'POOCHYENA', 'ZIGZAGOON', 'LEDYBA', 'SHROOMISH'],
      ask='The SLEEPY HOLLOW: naps are mandatory. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('FAT_MAN', 'I came for a walk. I took a nap.'), ('LITTLE_GIRL', 'Shh. Everything is sleeping.')], hidden=[], quests=[]),
 dict(map='ChampionsPath', tpl='Route22', badge=8, lv=(58, 64), land=['DRAGONITE', 'SALAMENCE', 'TYRANITAR', 'METAGROSS', 'FLYGON', 'MILOTIC', 'GYARADOS', 'ALAKAZAM', 'GENGAR', 'MACHAMP', 'STEELIX', 'BLISSEY'],
      ask='The CHAMPIONS PATH: only the best walk here. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('GENTLEMAN', 'Every champion has walked this path once.'), ('OLD_MAN_1', 'I was strong, once. Now I am wise.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
