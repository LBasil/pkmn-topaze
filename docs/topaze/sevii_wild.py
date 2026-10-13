#!/usr/bin/env python3
"""Sevii : les 'echos' du temps ramenent des Pokemon de Johto/Hoenn. Remplace les 10 emplacements les plus frequents
(les 2 plus rares restent vanilla) de tables choisies par des especes de A[map], en gardant les niveaux d'origine. Idempotent."""
import json
LAND = {
 'ONE_ISLAND_KINDLE_ROAD': ['NUMEL','ZIGZAGOON','POOCHYENA','SPINDA','MAKUHITA','ELECTRIKE','SPOINK'],
 'TWO_ISLAND_CAPE_BRINK': ['HOOTHOOT','SUNKERN','SNUBBULL','GIRAFARIG','MILTANK','TYROGUE','SPOINK'],
 'THREE_ISLAND_BOND_BRIDGE': ['TAILLOW','WINGULL','SURSKIT','SKITTY','PLUSLE','MINUN','VOLBEAT'],
 'THREE_ISLAND_BERRY_FOREST': ['SHROOMISH','SEEDOT','LOTAD','WURMPLE','NINCADA','ROSELIA'],
 'FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE': ['SNORUNT','SPHEAL','SWABLU','MAWILE','SNEASEL','DELIBIRD'],
 'FOUR_ISLAND_ICEFALL_CAVE_1F': ['SNORUNT','SPHEAL','SWABLU','MEDITITE'],
 'FOUR_ISLAND_ICEFALL_CAVE_B1F': ['SNORUNT','SPHEAL','ARON','SABLEYE'],
 'SIX_ISLAND_PATTERN_BUSH': ['SLAKOTH','WHISMUR','GULPIN','TROPIUS','KECLEON','ZANGOOSE','SEVIPER'],
 'SIX_ISLAND_RUIN_VALLEY': ['CACNEA','BALTOY','NOSEPASS','TRAPINCH','ABSOL','CASTFORM'],
 'FIVE_ISLAND_MEMORIAL_PILLAR': ['DUSKULL','SHUPPET','SABLEYE','HOOTHOOT'],
 'FIVE_ISLAND_MEADOW': ['SUNKERN','SKITTY','SNUBBULL','CORSOLA','YANMA'],
 'SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE': ['GLIGAR','ARON','MEDITITE','SKARMORY'],
 'SEVEN_ISLAND_SEVAULT_CANYON': ['LUNATONE','SOLROCK','GLIGAR','SUDOWOODO','ARON'],
}
WATER = {  # water_mons ET fishing_mons
 'ONE_ISLAND_TREASURE_BEACH': ['WAILMER','LUVDISC','CORSOLA','CHINCHOU'],
 'THREE_ISLAND_BOND_BRIDGE': ['CARVANHA','CORPHISH','BARBOACH'],
 'FIVE_ISLAND_RESORT_GORGEOUS': ['CLAMPERL','LUVDISC','CORSOLA'],
 'FIVE_ISLAND_WATER_LABYRINTH': ['FEEBAS','CLAMPERL','RELICANTH','BARBOACH'],
 'SIX_ISLAND_WATER_PATH': ['CHINCHOU','WAILMER','CARVANHA'],
}
d = json.load(open('src/data/wild_encounters.json'))
g = d['wild_encounter_groups'][0]
n = 0
for e in g['encounters']:
    m = e['map'].replace('MAP_', '')
    for table, conf in (('land_mons', LAND), ('water_mons', WATER), ('fishing_mons', WATER)):
        if m in conf and table in e:
            mons = e[table]['mons']; keep = 2 if table == 'land_mons' else 1
            spl = conf[m]
            for i in range(len(mons) - keep):
                mons[i]['species'] = 'SPECIES_' + spl[i % len(spl)]
            n += 1
json.dump(d, open('src/data/wild_encounters.json', 'w'), indent=2); open('src/data/wild_encounters.json', 'a').write('\n')
print('tables modifiees', n)
