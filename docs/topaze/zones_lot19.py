#!/usr/bin/env python3
"""LOT 19 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'LanternMeadow' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='LanternMeadow', tpl='Route25', badge=2, lv=(10, 16), land=['ODDISH', 'BELLSPROUT', 'GLOOM', 'WEEPINBELL', 'MARILL', 'AZURILL', 'HOPPIP', 'SUNKERN', 'PLUSLE', 'MINUN', 'PIKACHU', 'JIGGLYPUFF'],
      ask='The LANTERN MEADOW: glowing flowers at dusk. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('LASS', 'The flowers glow when the sun goes down.'), ('LITTLE_GIRL', 'PLUSLE and MINUN cheer for each other.')], hidden=[], quests=[]),
 dict(map='RustyYard', tpl='Route22', badge=3, lv=(18, 24), land=['MAGNEMITE', 'VOLTORB', 'GRIMER', 'KOFFING', 'MACHOP', 'GEODUDE', 'ZUBAT', 'RATTATA', 'RATICATE', 'ELECTRIKE', 'SKITTY', 'MEOWTH'],
      ask='The RUSTY YARD: old scrap and new friends. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('WORKER_M'.replace('WORKER_M', 'MAN'), 'Everything here is rust. Even the birds.'), ('YOUNGSTER', 'VOLTORB looks like a BALL. Do not touch it.')], hidden=[], quests=[]),
 dict(map='WillowBank', tpl='SafariZone_East', badge=4, lv=(24, 30), land=['LOTAD', 'LOMBRE', 'SEEDOT', 'NUZLEAF', 'POLIWAG', 'POLIWHIRL', 'PSYDUCK', 'GOLDUCK', 'MARILL', 'WOOPER', 'QUAGSIRE', 'SURSKIT'],
      ask='The WILLOW BANK: a slow river and calm shade. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('OLD_MAN_1', 'I fish here every day. I catch memories.'), ('LASS', 'LOMBRE laughs when you lose. Rude.')], hidden=[], quests=[]),
 dict(map='EmberRidge', tpl='Route4', badge=6, lv=(36, 42), land=['GROWLITHE', 'PONYTA', 'VULPIX', 'NINETALES', 'MAGMAR', 'TORKOAL', 'NUMEL', 'SLUGMA', 'CYNDAQUIL', 'MAGBY', 'FLAREON', 'HOUNDOUR'],
      ask='The EMBER RIDGE: warm rocks and red sparks. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('HIKER', 'The ridge is warm even in winter.'), ('SCIENTIST', 'HOUNDOUR howls before every eruption.')], hidden=[], quests=[]),
 dict(map='GlassCavern', tpl='SafariZone_Center', badge=7, lv=(42, 48), land=['SABLEYE', 'MAWILE', 'GOLBAT', 'CROBAT', 'ONIX', 'STEELIX', 'LAIRON', 'ARON', 'NOSEPASS', 'SKARMORY', 'MAGNETON', 'FORRETRESS'],
      ask='The GLASS CAVERN: shining walls and sharp echoes. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('HIKER', 'The walls shine. Do not lick them.'), ('GENTLEMAN', 'SABLEYE loves gems. So do I.')], hidden=[], quests=[]),
 dict(map='DawnSummit', tpl='Route22', badge=8, lv=(54, 60), land=['ARTICUNO'.replace('ARTICUNO', 'ALTARIA'), 'DRAGONITE', 'SALAMENCE', 'FLYGON', 'TOGETIC', 'XATU', 'ESPEON', 'UMBREON', 'GARDEVOIR', 'ABSOL', 'MILOTIC', 'KINGDRA'],
      ask='The DAWN SUMMIT: the first light of the region. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('OLD_WOMAN', 'The sun rises here first. It is worth the climb.'), ('GENTLEMAN', 'Only the strongest reach the summit.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
