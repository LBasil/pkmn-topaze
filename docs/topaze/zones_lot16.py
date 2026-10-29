#!/usr/bin/env python3
"""LOT 16 : 6 zones sauvages sans drapeau (WeedPatch, SkyPerch, SandboxGrove, IvyMaze, NorthWind, StoneCircle). Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'WeedPatch' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='WeedPatch', tpl='Route25', badge=1, lv=(5, 10), land=['CATERPIE', 'WEEDLE', 'METAPOD', 'KAKUNA', 'WURMPLE', 'SILCOON', 'CASCOON', 'LEDYBA', 'SPINARAK', 'PIDGEY', 'RATTATA', 'ZIGZAGOON'],
      water=['PSYDUCK', 'MAGIKARP', 'POLIWAG', 'GOLDEEN', 'LOTAD'], fish=['MAGIKARP', 'GOLDEEN', 'POLIWAG', 'LOTAD', 'BARBOACH', 'PSYDUCK', 'MARILL', 'CORPHISH', 'WOOPER', 'FEEBAS'],
      ask='The WEED PATCH: tall grass and tiny bugs. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('BUG_CATCHER', 'Bugs grow fast. Catch two of each, just in case.'), ('YOUNGSTER', 'CASCOON and SILCOON both end up flying.')], hidden=[], quests=[]),
 dict(map='SkyPerch', tpl='Route22', badge=5, lv=(30, 36), land=['FEAROW', 'SKARMORY', 'PIDGEOTTO', 'SWELLOW', 'ALTARIA', 'SWABLU', 'DODUO', 'DODRIO', 'MURKROW', 'DELIBIRD', 'TAILLOW', 'NATU'],
      ask='The SKY PERCH: cliffs for birds and wind riders. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('HIKER', 'Look up. Half the sky here is a POKéMON.'), ('LASS', 'SWABLU loves clouds. ALTARIA is its song.')], hidden=[], quests=[]),
 dict(map='SandboxGrove', tpl='SafariZone_West', badge=3, lv=(18, 24), land=['DIGLETT', 'SANDSHREW', 'TRAPINCH', 'CACNEA', 'BALTOY', 'GEODUDE', 'ONIX', 'CUBONE', 'PHANPY', 'NUMEL', 'ZIGZAGOON', 'SLAKOTH'],
      ask='The SANDBOX GROVE: a sandy playground for ground types. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('LITTLE_BOY', 'I dig and dig. Look what came up!'), ('HIKER', 'Ground types dislike the rain. Keep that in mind.')], hidden=[], quests=[]),
 dict(map='IvyMaze', tpl='ViridianForest', badge=2, lv=(12, 18), land=['PARAS', 'PARASECT', 'VENONAT', 'KAKUNA', 'BEEDRILL', 'SPINARAK', 'LEDYBA', 'SEEDOT', 'SHROOMISH', 'ODDISH', 'BELLSPROUT', 'PINECO'],
      ask='The IVY MAZE: twisting paths of green. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('BUG_CATCHER', 'Lost twice already. Worth it for PARAS.'), ('LASS', 'SHROOMISH is shy, so stay still.')], hidden=[], quests=[]),
 dict(map='NorthWind', tpl='Route4', badge=7, lv=(46, 52), land=['DELIBIRD', 'SNEASEL', 'PILOSWINE', 'DEWGONG', 'LAPRAS', 'GLALIE', 'SNORUNT', 'SPHEAL', 'SEALEO', 'JYNX', 'SWINUB', 'SMOOCHUM'],
      ask='The NORTH WIND: bitter gusts and cold fur. Visit?', gt='Come back with 7 BADGES.',
      npcs=[('HIKER', 'My ears hurt. My team loves it.'), ('OLD_MAN_1', 'LAPRAS comes by when the wind is right.')], hidden=[], quests=[]),
 dict(map='StoneCircle', tpl='Route22', badge=8, lv=(52, 58), land=['DRAGONAIR', 'ALTARIA', 'FLYGON', 'VIBRAVA', 'SHELGON', 'BAGON', 'GIBLE'.replace('GIBLE', 'KINGDRA'), 'DRATINI', 'SWABLU', 'TRAPINCH', 'DRAGONITE', 'SALAMENCE'],
      ask='The STONE CIRCLE: dragons gather under standing stones. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('OLD_WOMAN', 'The circle calls the dragons. Not the other way.'), ('GENTLEMAN', 'Even SALAMENCE comes here, once in a long while.')], hidden=[], quests=[]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
