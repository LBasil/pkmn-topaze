#!/usr/bin/env python3
"""LOT 24 : 6 zones sauvages sans drapeau. Idempotent."""
import sys, re; sys.path.insert(0, 'docs/topaze')
from zonelib import *
if 'FernGully' in rd('data/event_scripts.s'): print('deja applique'); raise SystemExit
Z = [
 dict(map='FernGully', tpl='ViridianForest', badge=1, lv=(5, 10), land=['CATERPIE', 'WEEDLE', 'PIDGEY', 'RATTATA', 'ODDISH', 'BELLSPROUT', 'WURMPLE', 'LEDYBA', 'SENTRET', 'HOOTHOOT', 'NINCADA', 'SEEDOT'],
      ask='The FERN GULLY: a green dip full of tiny wings. Visit?', gt='Come back with 1 BADGE.',
      npcs=[('BUG_CATCHER', 'Ferns hide everything. Even my net.'), ('LITTLE_BOY', 'I found a WEEDLE. It found me back.')], hidden=[], quests=[]),
 dict(map='CliffsideCove', tpl='Route22', badge=3, lv=(18, 24), land=['WINGULL', 'PELIPPER', 'KRABBY', 'SHELLDER', 'STARYU', 'TENTACOOL', 'CORSOLA', 'SLOWPOKE', 'PSYDUCK', 'GEODUDE', 'ZUBAT', 'SPEAROW'],
      ask='The CLIFFSIDE COVE: a hidden beach under the rocks. Visit?', gt='Come back with 3 BADGES.',
      npcs=[('SAILOR', 'Nobody comes here. Except me and WINGULL.'), ('LASS', 'The tide covers the path at night.')], hidden=[], quests=[]),
 dict(map='MeteorField', tpl='SafariZone_East', badge=5, lv=(30, 36), land=['SOLROCK', 'LUNATONE', 'CLEFAIRY', 'CLEFABLE', 'STARYU', 'STARMIE', 'BALTOY', 'CLAYDOL', 'MAGNEMITE', 'MAGNETON', 'NATU', 'XATU'],
      ask='The METEOR FIELD: craters and star dust. Visit?', gt='Come back with 5 BADGES.',
      npcs=[('SCIENTIST', 'A rock fell here. It was not a rock.'), ('GENTLEMAN', 'CLEFAIRY came from the stars. Or so they say.')], hidden=[], quests=[]),
 dict(map='VenomSwamp', tpl='SafariZone_West', badge=6, lv=(36, 42), land=['MUK', 'WEEZING', 'ARBOK', 'VENOMOTH', 'TENTACRUEL', 'GLOOM', 'VILEPLUME', 'ARIADOS', 'SWALOT', 'SEVIPER', 'QUAGSIRE', 'GRIMER'],
      ask='The VENOM SWAMP: the air itself bites. Visit?', gt='Come back with 6 BADGES.',
      npcs=[('SCIENTIST', 'Wear a mask. Wear two.'), ('HIKER', 'Everything here is purple. Even me.')], hidden=[], quests=[]),
 dict(map='WindmillFlats', tpl='Route25', badge=4, lv=(24, 30), land=['PIDGEOTTO', 'FEAROW', 'DODUO', 'DODRIO', 'AMPHAROS', 'MAREEP', 'FLAAFFY', 'MILTANK', 'TAUROS', 'PONYTA', 'GIRAFARIG', 'STANTLER'],
      ask='The WINDMILL FLATS: wide fields and slow blades. Visit?', gt='Come back with 4 BADGES.',
      npcs=[('OLD_MAN_1', 'The windmill turns. So do the years.'), ('LITTLE_GIRL', 'MILTANK gives the best milk. Ask nicely.')], hidden=[], quests=[]),
 dict(map='RoyalGarden', tpl='SafariZone_Center', badge=8, lv=(56, 62), land=['ROSELIA', 'BELLOSSOM', 'VILEPLUME', 'VICTREEBEL', 'TANGELA', 'EXEGGUTOR', 'SCEPTILE', 'LUDICOLO', 'BUTTERFREE', 'BEAUTIFLY', 'VENUSAUR', 'MEGANIUM'],
      ask='The ROYAL GARDEN: the most perfect hedges you will see. Visit?', gt='Come back with all 8 BADGES.',
      npcs=[('GENTLEMAN', 'The gardener has not slept in a week.'), ('OLD_WOMAN', 'The roses here bloom out of season.')], hidden=[], quests=[]),
]
SPX = rd('include/constants/species.h')
bad = [(z['map'], n) for z in Z for n in z['land'] if not re.search(r'#define SPECIES_%s\b' % n, SPX)]
EVO = rd('include/constants/event_objects.h'); badg = [g for z in Z for g in [x[0] for x in z['npcs']] if not re.search(r'OBJ_EVENT_GFX_%s\b' % g, EVO)]
if bad or badg: print('INVALIDE', bad, set(badg)); raise SystemExit(1)
WE = json.load(open('src/data/wild_encounters.json')); grp = WE['wild_encounter_groups'][0]['encounters']; journal = []; arr = {}
for z in Z: arr[z['map']] = make_zone(z, grp, journal)
N.jdump(WE, 'src/data/wild_encounters.json')
for z, f in zip(Z, ['Apprentice', 'ScribeFerryman', 'SeasonsFerryman', 'DuskFerrywoman', 'ScribeFerryman', 'DuskFerrywoman']): ferry_add(f, z['map'], arr[z['map']], z['badge'], z['ask'], z['gt'])
