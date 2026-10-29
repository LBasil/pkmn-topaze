#!/usr/bin/env python3
"""LOT 27 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'BuzzingMeadow' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='BuzzingMeadow', tpl='Route25', badge=1, lv=(5, 10), land=['CATERPIE', 'WEEDLE', 'LEDYBA', 'SPINARAK', 'WURMPLE', 'SILCOON', 'CASCOON', 'PARAS', 'VENONAT', 'NINCADA', 'PIDGEY', 'RATTATA'],
      ask='The BUZZING MEADOW: wings everywhere. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('BUG_CATCHER', 'I counted a hundred wings. Then I lost count.'), ('LASS', 'LEDYBA sleeps all day. Lucky.')], hidden=[], quests=[]),
 dict(map='PuddleLane', tpl='Route22', badge=2, lv=(12, 18), land=['PSYDUCK', 'POLIWAG', 'LOTAD', 'SURSKIT', 'WOOPER', 'MARILL', 'GOLDEEN', 'SLOWPOKE', 'RATTATA', 'PIDGEY', 'ZIGZAGOON', 'SENTRET'],
      ask='The PUDDLE LANE: it rained. It always rains. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('LITTLE_GIRL', 'I jump in every puddle. Every single one.'), ('OLD_MAN_1', 'Bring a coat. Or a POLIWAG.')], hidden=[], quests=[]),
 dict(map='GraniteBluff', tpl='Route4', badge=4, lv=(24, 30), land=['GEODUDE', 'GRAVELER', 'ONIX', 'MACHOP', 'MACHOKE', 'RHYHORN', 'ARON', 'LAIRON', 'NOSEPASS', 'SKARMORY', 'SANDSLASH', 'TRAPINCH'],
      ask='The GRANITE BLUFF: heavy stone and heavy boots. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('HIKER', 'The rock is solid. So am I.'), ('YOUNGSTER', 'I tried to climb. I tried twice.')], hidden=[], quests=[]),
 dict(map='ElectricAvenue', tpl='SafariZone_Center', badge=5, lv=(30, 36), land=['MAGNETON', 'ELECTABUZZ', 'ELECTRODE', 'MANECTRIC', 'AMPHAROS', 'RAICHU', 'PIKACHU', 'VOLTORB', 'JOLTEON', 'LANTURN', 'ELECTRIKE', 'MAREEP'],
      ask='The ELECTRIC AVENUE: street lights that bite. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SCIENTIST', 'Every pole here is a free charger.'), ('YOUNGSTER', 'VOLTORB rolls into the road. Watch out.')], hidden=[], quests=[]),
 dict(map='SpiritFalls', tpl='SafariZone_West', badge=7, lv=(44, 50), land=['GYARADOS', 'MILOTIC', 'LAPRAS', 'KINGDRA', 'SLOWKING', 'STARMIE', 'WALREIN', 'ALAKAZAM', 'XATU', 'ESPEON', 'UMBREON', 'HAUNTER'],
      ask='The SPIRIT FALLS: a waterfall with a voice. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('OLD_WOMAN', 'The waterfall sings. Listen at dusk.'), ('GENTLEMAN', 'They say the spirits bathe here.')], hidden=[], quests=[]),
 dict(map='FinalGate', tpl='SafariZone_East', badge=8, lv=(60, 66), land=['DRAGONITE', 'SALAMENCE', 'TYRANITAR', 'METAGROSS', 'FLYGON', 'KINGDRA', 'MILOTIC', 'GENGAR', 'ALAKAZAM', 'MACHAMP', 'STEELIX', 'BLISSEY'],
      ask='The FINAL GATE: beyond it, only legends. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('GENTLEMAN', 'No one has walked past this gate. Yet.'), ('OLD_MAN_1', 'I stopped here. Wisely.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
