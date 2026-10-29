#!/usr/bin/env python3
"""LOT 21 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'DaisyHill' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='DaisyHill', tpl='Route25', badge=1, lv=(5, 10), land=['HOPPIP', 'SUNKERN', 'ODDISH', 'BELLSPROUT', 'PIDGEY', 'RATTATA', 'SENTRET', 'HOOTHOOT', 'WURMPLE', 'CATERPIE', 'AZURILL', 'MARILL'],
      ask='The DAISY HILL: flowers all the way up. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('LASS', 'I pick one daisy a day. One only.'), ('LITTLE_BOY', 'SUNKERN is just a seed with legs.')], hidden=[], quests=[]),
 dict(map='MuddyCreek', tpl='SafariZone_West', badge=2, lv=(12, 18), land=['WOOPER', 'BARBOACH', 'GOLDEEN', 'POLIWAG', 'PSYDUCK', 'LOTAD', 'SURSKIT', 'MARILL', 'DIGLETT', 'GEODUDE', 'ZUBAT', 'RATTATA'],
      ask='The MUDDY CREEK: brown water and slippery friends. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('FAT_MAN', 'Mud is good for the skin. And for WOOPER.'), ('YOUNGSTER', 'BARBOACH hides in the mud. Dig!')], hidden=[], quests=[]),
 dict(map='CrystalGrotto', tpl='SafariZone_Center', badge=4, lv=(24, 30), land=['SHUPPET', 'GOLBAT', 'ONIX', 'GEODUDE', 'GRAVELER', 'CLEFAIRY', 'CLEFABLE', 'NOSEPASS', 'SABLEYE', 'MAWILE', 'ARON', 'LUNATONE'],
      ask='The CRYSTAL GROTTO: gems in every wall. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('HIKER', 'Do not touch the crystals. They hum.'), ('GENTLEMAN', 'CLEFAIRY dances here under the moon.')], hidden=[], quests=[]),
 dict(map='SunsetRoad', tpl='Route22', badge=5, lv=(30, 36), land=['PERSIAN', 'RAPIDASH', 'NINETALES', 'ARCANINE', 'FEAROW', 'DODRIO', 'SANDSLASH', 'PIDGEOTTO', 'GIRAFARIG', 'STANTLER', 'NOCTOWL', 'LINOONE'],
      ask='The SUNSET ROAD: a long walk toward the red sky. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('OLD_MAN_1', 'I walk here every evening. It never ends.'), ('LASS', 'ARCANINE glows in the setting sun.')], hidden=[], quests=[]),
 dict(map='ThunderPlain', tpl='Route4', badge=6, lv=(36, 42), land=['RAICHU', 'ELECTABUZZ', 'MAGNETON', 'MANECTRIC', 'ELECTRODE', 'PLUSLE', 'MINUN', 'JOLTEON', 'AMPHAROS', 'LANTURN', 'PIKACHU', 'ELEKID'],
      ask='The THUNDER PLAIN: static in the air. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('SCIENTIST', 'Do not wear metal. I learned that the hard way.'), ('YOUNGSTER', 'My hair is standing up. Is it normal?')], hidden=[], quests=[]),
 dict(map='AncientLibrary', tpl='SafariZone_East', badge=8, lv=(52, 58), land=['ALAKAZAM', 'XATU', 'ESPEON', 'GARDEVOIR', 'HYPNO', 'MR_MIME', 'WOBBUFFET', 'CLAYDOL', 'MEDICHAM', 'SLOWKING', 'UNOWN', 'GIRAFARIG'],
      ask='The ANCIENT LIBRARY: old books and older minds. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('GENTLEMAN', 'Silence, please. The books are thinking.'), ('OLD_WOMAN', 'UNOWN writes on the pages. No one reads it.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
