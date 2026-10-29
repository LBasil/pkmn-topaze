#!/usr/bin/env python3
"""LOT 22 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'BerryBrook' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='BerryBrook', tpl='Route25', badge=1, lv=(4, 9), land=['ZIGZAGOON', 'LINOONE', 'PIDGEY', 'RATTATA', 'SENTRET', 'LOTAD', 'SEEDOT', 'TAILLOW', 'SURSKIT', 'HOPPIP', 'CATERPIE', 'WEEDLE'],
      ask='The BERRY BROOK: a sweet stream. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('LITTLE_GIRL', 'The berries here taste like candy.'), ('LASS', 'ZIGZAGOON steals them. Cute thief.')], hidden=[], quests=[]),
 dict(map='HauntedOrchard', tpl='ViridianForest', badge=3, lv=(18, 24), land=['GASTLY', 'HAUNTER', 'ODDISH', 'GLOOM', 'HOOTHOOT', 'MURKROW', 'SHUPPET', 'DUSKULL', 'PARAS', 'BELLSPROUT', 'SHROOMISH', 'MISDREAVUS'],
      ask='The HAUNTED ORCHARD: the apples whisper. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('OLD_WOMAN', 'Do not eat the apples. They talk back.'), ('BUG_CATCHER', 'GASTLY floats between the trees.')], hidden=[], quests=[]),
 dict(map='CopperCanyon', tpl='SafariZone_West', badge=4, lv=(24, 30), land=['ONIX', 'GEODUDE', 'GRAVELER', 'RHYHORN', 'RHYDON', 'MACHOP', 'MACHOKE', 'SANDSLASH', 'SKARMORY', 'TRAPINCH', 'NUMEL', 'CUBONE'],
      ask='The COPPER CANYON: red walls and echo. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('HIKER', 'Shout. The canyon will answer.'), ('YOUNGSTER', 'RHYHORN charged me. I ran very fast.')], hidden=[], quests=[]),
 dict(map='GlimmerBay', tpl='Route22', badge=5, lv=(30, 36), land=['WINGULL', 'PELIPPER', 'TENTACRUEL', 'CORSOLA', 'STARMIE', 'KRABBY', 'KINGLER', 'CLAMPERL', 'LUVDISC', 'HORSEA', 'SEADRA', 'WAILMER'],
      ask='The GLIMMER BAY: the sea sparkles at noon. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SAILOR', 'The bay glows. The fish glow. I glow.'), ('LASS', 'LUVDISC is a heart. Literally.')], hidden=[], quests=[]),
 dict(map='IronForest', tpl='ViridianForest', badge=6, lv=(36, 42), land=['SCIZOR', 'PINSIR', 'HERACROSS', 'FORRETRESS', 'SKARMORY', 'STEELIX', 'ARIADOS', 'VENOMOTH', 'BEEDRILL', 'LEDIAN', 'SHEDINJA', 'DUSTOX'],
      ask='The IRON FOREST: leaves like blades. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('HIKER', 'The leaves cut. Wear long sleeves.'), ('BUG_CATCHER', 'SCIZOR is my hero. It is also my nightmare.')], hidden=[], quests=[]),
 dict(map='MythicSpring', tpl='SafariZone_Center', badge=8, lv=(55, 62), land=['MILOTIC', 'VAPOREON', 'LAPRAS', 'SLOWKING', 'KINGDRA', 'STARMIE', 'WALREIN', 'POLITOED', 'AZUMARILL', 'LUDICOLO', 'SWAMPERT', 'GOLDUCK'],
      ask='The MYTHIC SPRING: a pool that grants wishes, they say. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('OLD_WOMAN', 'I made a wish here once. It is still coming.'), ('GENTLEMAN', 'The water is clear enough to see tomorrow.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
