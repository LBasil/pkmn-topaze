#!/usr/bin/env python3
"""Layouts du REPAIRE (copies des salles de la Ligue, tileset PokemonLeagueLair). Idempotent."""
import json, shutil, os
SRC={'VictoryRoadLair_1F':('PokemonLeague_LancesRoom','LAYOUT_VICTORY_ROAD_LAIR_1F'),
     'VictoryRoadLair_2F':('PokemonLeague_ChampionsRoom','LAYOUT_VICTORY_ROAD_LAIR_2F'),
     'VictoryRoadLair_3F':('PokemonLeague_LoreleisRoom','LAYOUT_VICTORY_ROAD_LAIR_3F')}
p='data/layouts/layouts.json'; j=json.load(open(p)); ids={l.get('id') for l in j['layouts']}
for name,(src,lid) in SRC.items():
    os.makedirs('data/layouts/'+name,exist_ok=True)
    for f in ('map.bin','border.bin'): shutil.copy(f'data/layouts/{src}/{f}',f'data/layouts/{name}/{f}')
    if lid in ids: continue
    base=[l for l in j['layouts'] if l.get('blockdata_filepath')==f'data/layouts/{src}/map.bin'][0]
    e=dict(base); e['id']=lid; e['name']=name+'_Layout'; e['secondary_tileset']='gTileset_PokemonLeagueLair'
    e['border_filepath']=f'data/layouts/{name}/border.bin'; e['blockdata_filepath']=f'data/layouts/{name}/map.bin'
    j['layouts'].append(e)
json.dump(j,open(p,'w'),indent=2); open(p,'a').write('\n')
print('ok')
