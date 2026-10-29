#!/usr/bin/env python3
"""LOT 25 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'LilyLagoon' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='LilyLagoon', tpl='Route25', badge=1, lv=(5, 10), land=['LOTAD', 'POLIWAG', 'PSYDUCK', 'MARILL', 'AZURILL', 'GOLDEEN', 'SURSKIT', 'WOOPER', 'HOPPIP', 'CATERPIE', 'PIDGEY', 'RATTATA'],
      ask='The LILY LAGOON: pads to hop and tiny frogs. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('LITTLE_GIRL', 'I hopped across all the pads. Almost.'), ('LASS', 'LOTAD wears a lily as a hat.')], hidden=[], quests=[]),
 dict(map='PrairieDusk', tpl='Route22', badge=2, lv=(12, 18), land=['TAUROS', 'MILTANK', 'PONYTA', 'DODUO', 'SENTRET', 'FURRET', 'MAREEP', 'RATTATA', 'RATICATE', 'SPEAROW', 'PIDGEOTTO', 'GIRAFARIG'],
      ask='The PRAIRIE DUSK: tall grass, orange sky. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('OLD_MAN_1', 'TAUROS stampedes at sunset. Stay behind a tree.'), ('YOUNGSTER', 'I race PONYTA. I lose. Every time.')], hidden=[], quests=[]),
 dict(map='CoralTerrace', tpl='SafariZone_West', badge=4, lv=(24, 30), land=['CORSOLA', 'STARYU', 'STARMIE', 'KRABBY', 'KINGLER', 'SEADRA', 'HORSEA', 'CLAMPERL', 'LUVDISC', 'CHINCHOU', 'SHELLDER', 'REMORAID'],
      ask='The CORAL TERRACE: stone steps built by the tide. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('SAILOR', 'The steps are coral. Mind your feet.'), ('LASS', 'CORSOLA is a tiny reef that walks.')], hidden=[], quests=[]),
 dict(map='SpireYard', tpl='SafariZone_East', badge=6, lv=(38, 44), land=['HAUNTER', 'GENGAR', 'MISDREAVUS', 'DUSKULL', 'BANETTE', 'SHUPPET', 'SABLEYE', 'MURKROW', 'GOLBAT', 'CROBAT', 'NOCTOWL', 'HOUNDOOM'],
      ask='The SPIRE YARD: a graveyard around a tall tower. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('OLD_WOMAN', 'The tower bell rings. No one rings it.'), ('HIKER', 'The ghosts are polite. Mostly.')], hidden=[], quests=[]),
 dict(map='QuartzQuarry', tpl='Route4', badge=5, lv=(30, 36), land=['GRAVELER', 'GOLEM', 'ONIX', 'STEELIX', 'MACHOKE', 'MACHAMP', 'RHYHORN', 'RHYDON', 'NOSEPASS', 'LAIRON', 'SKARMORY', 'SANDSLASH'],
      ask='The QUARTZ QUARRY: pale rock and loud hammers. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('HIKER', 'I mine all day. My team smashes all night.'), ('MAN', 'Clear stone. Clear mind.')], hidden=[], quests=[]),
 dict(map='EdgeOfTheWorld', tpl='SafariZone_Center', badge=8, lv=(60, 66), land=['DRAGONITE', 'SALAMENCE', 'METAGROSS', 'TYRANITAR', 'FLYGON', 'KINGDRA', 'MILOTIC', 'GENGAR', 'ALAKAZAM', 'STEELIX', 'BLISSEY', 'SNORLAX'],
      ask='The EDGE OF THE WORLD: the last cliff. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('OLD_MAN_1', 'Beyond is just sea. And rumors.'), ('GENTLEMAN', 'Only the bold stand here.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
