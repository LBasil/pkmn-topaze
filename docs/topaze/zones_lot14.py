#!/usr/bin/env python3
"""LOT 14 : 4 zones sauvages sans drapeau (BreezeHill, StarlitSteppe, SaltFlats, MistLake). Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'BreezeHill' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='BreezeHill', tpl='Route22', badge=1, lv=(6, 12), land=['PIDGEY', 'SPEAROW', 'MANKEY', 'NIDORAN_M', 'NIDORAN_F', 'EKANS', 'SANDSHREW', 'ZIGZAGOON', 'WURMPLE', 'TAILLOW', 'LOTAD', 'RALTS'],
      ask='The BREEZE HILL: wind, grass and first catches. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('YOUNGSTER', 'RALTS is shy. Be patient and be lucky.'), ('LASS', 'The wind here carries every early POKéMON to you.')], hidden=[], quests=[]),
 dict(map='StarlitSteppe', tpl='Route8', badge=6, lv=(40, 46), land=['STANTLER', 'GIRAFARIG', 'PHANPY', 'DONPHAN', 'TEDDIURSA', 'URSARING', 'HOUNDOUR', 'SNEASEL', 'MILTANK', 'SKARMORY', 'LARVITAR', 'DUNSPARCE'],
      ask='The STARLIT STEPPE: wide plains under a thousand stars. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('HIKER', 'LARVITAR hides in the tall grass at night.'), ('GENTLEMAN', 'Even DUNSPARCE shows up, if you are lucky.')], hidden=[], quests=[]),
 dict(map='SaltFlats', tpl='Route9', badge=4, lv=(24, 30), land=['WINGULL', 'PELIPPER', 'KRABBY', 'SANDSHREW', 'DUNSPARCE', 'DIGLETT', 'DUGTRIO', 'CACNEA', 'BALTOY', 'TRAPINCH', 'SKARMORY', 'NUMEL'],
      water=['WINGULL', 'PELIPPER', 'TENTACOOL', 'KRABBY', 'WAILMER'], fish=['MAGIKARP', 'KRABBY', 'KINGLER', 'WAILMER', 'CORSOLA', 'HORSEA', 'FEEBAS', 'TENTACOOL', 'STARYU', 'CHINCHOU'],
      ask='The SALT FLATS: dry crust and bright shores. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('SAILOR', 'Salt, sand and sea. A strange mix of POKéMON.'), ('HIKER', 'TRAPINCH digs where the sand is softest.')], hidden=[], quests=[]),
 dict(map='MistLake', tpl='Route10', badge=2, lv=(12, 18), land=['PSYDUCK', 'POLIWAG', 'GOLDEEN', 'LOTAD', 'MARILL', 'SURSKIT', 'ODDISH', 'BELLSPROUT', 'RATTATA', 'PIDGEY', 'VOLTORB', 'MAGNEMITE'],
      water=['PSYDUCK', 'GOLDEEN', 'POLIWAG', 'MARILL', 'MAGIKARP'], fish=['MAGIKARP', 'GOLDEEN', 'POLIWAG', 'MARILL', 'BARBOACH', 'CORPHISH', 'LOTAD', 'PSYDUCK', 'WOOPER', 'FEEBAS'],
      ask='The MIST LAKE: soft fog, calm water. Visit?', gt='Come back with 2 BADGES.',
      npcs=[('FISHER', 'The fog hides the best fishing spots.'), ('LITTLE_GIRL', 'MARILL bounces on the water. So cute!')], hidden=[], quests=[]),
]
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
