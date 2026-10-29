#!/usr/bin/env python3
"""LOT 26 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'HarvestHollow' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='HarvestHollow', tpl='Route25', badge=1, lv=(5, 10), land=['RATTATA', 'PIDGEY', 'SENTRET', 'ZIGZAGOON', 'HOPPIP', 'SUNKERN', 'ODDISH', 'BELLSPROUT', 'MEOWTH', 'SPEAROW', 'AZURILL', 'SKITTY'],
      ask='The HARVEST HOLLOW: golden fields and scarecrows. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('OLD_WOMAN', 'The scarecrow moved last night. I swear.'), ('LITTLE_BOY', 'I hid in the corn. They never found me.')], hidden=[], quests=[]),
 dict(map='MirrorMarsh', tpl='SafariZone_West', badge=3, lv=(18, 24), land=['PSYDUCK', 'GOLDUCK', 'POLIWAG', 'POLIWHIRL', 'LOTAD', 'LOMBRE', 'WOOPER', 'QUAGSIRE', 'BARBOACH', 'SURSKIT', 'MARILL', 'SLOWPOKE'],
      ask='The MIRROR MARSH: still water that copies the sky. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('GENTLEMAN', 'Stand still. The sky will fall in the water.'), ('LASS', 'I saw myself wave. I did not wave.')], hidden=[], quests=[]),
 dict(map='HighPines', tpl='ViridianForest', badge=4, lv=(24, 30), land=['HERACROSS', 'PINSIR', 'SCYTHER', 'ARIADOS', 'BEEDRILL', 'GLIGAR', 'TEDDIURSA', 'URSARING', 'PIDGEOTTO', 'NOCTOWL', 'STANTLER', 'PINECO'],
      ask='The HIGH PINES: thin air and strong bugs. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('HIKER', 'The air is thin. My team is not.'), ('BUG_CATCHER', 'HERACROSS loves tree sap. So do I.')], hidden=[], quests=[]),
 dict(map='SeaGlassShore', tpl='Route22', badge=5, lv=(30, 36), land=['WINGULL', 'PELIPPER', 'CORSOLA', 'KINGLER', 'STARMIE', 'SEADRA', 'TENTACRUEL', 'LUVDISC', 'CLAMPERL', 'SHELLDER', 'LAPRAS', 'WAILMER'],
      ask='The SEA GLASS SHORE: green shards, soft waves. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('LASS', 'I collect sea glass. Each one is a story.'), ('SAILOR', 'Old bottles. Old storms.')], hidden=[], quests=[]),
 dict(map='DeepEmberCave', tpl='SafariZone_Center', badge=7, lv=(44, 50), land=['MAGMAR', 'MAGCARGO', 'CAMERUPT', 'TORKOAL', 'GOLBAT', 'CROBAT', 'STEELIX', 'ONIX', 'SLUGMA', 'NINETALES', 'ARCANINE', 'RAPIDASH'],
      ask='The DEEP EMBER CAVE: hot stone, hotter echoes. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('HIKER', 'Do not go any deeper. I mean it.'), ('SCIENTIST', 'The walls are warm. The floor is warmer.')], hidden=[], quests=[]),
 dict(map='SkyGarden', tpl='SafariZone_East', badge=8, lv=(56, 62), land=['ALTARIA', 'DRAGONITE', 'SALAMENCE', 'FLYGON', 'TOGETIC', 'XATU', 'SKARMORY', 'HOUNDOOM', 'MILOTIC', 'GARDEVOIR', 'ROSELIA', 'BELLOSSOM'],
      ask='The SKY GARDEN: flowers above the clouds. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('OLD_WOMAN', 'The gardener flies. I do not ask how.'), ('GENTLEMAN', 'The best view in the region. Do not tell.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
