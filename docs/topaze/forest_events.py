# FORET CALCINEE : evenements (warps, dresseurs, objets, panneaux, meteo de cendres). A lancer apres forest_map.py. Idempotent.
import json
info = json.load(open('/tmp/forest_info.json'))
f = 'data/maps/ViridianForest/map.json'; d = json.load(open(f))
def warp(c, dest, wid): return {"x": c[0], "y": c[1], "elevation": 3, "dest_map": dest, "dest_warp_id": str(wid)}
sd, nd = info['sdoor'], info['ndoor']
# les interieurs renvoient aux warps 0 (sud) et 2 (nord) : les indices 1 et 3 sont des doublons
d['warp_events'] = [warp(sd, 'MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE', 3), warp(sd, 'MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE', 3),
                    warp(nd, 'MAP_ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE', 1), warp(nd, 'MAP_ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE', 1)]
POS = {'ViridianForest_EventScript_Youngster': 'youngster', 'ViridianForest_EventScript_Boy': 'boy', 'ViridianForest_EventScript_Rick': 'rick',
       'ViridianForest_EventScript_Doug': 'doug', 'ViridianForest_EventScript_Sammy': 'sammy', 'ViridianForest_EventScript_Anthony': 'anthony',
       'ViridianForest_EventScript_Charlie': 'charlie', 'ViridianForest_EventScript_ItemPokeBall': 'ball_pokeball', 'ViridianForest_EventScript_ItemAntidote': 'ball_antidote',
       'ViridianForest_EventScript_ItemPotion': 'ball_potion', 'ViridianForest_EventScript_ItemPotion2': 'ball_potion2'}
for o in d['object_events']:
    k = POS[o['script']]; o['x'], o['y'] = info['obj'][k]
    if k in info['face']:
        o['movement_type'] = 'MOVEMENT_TYPE_FACE_' + info['face'][k]; o['trainer_sight_or_berry_tree_id'] = str(info['sight'][k])
SG = {'ViridianForest_EventScript_TrainerTips1': 'tips1', 'ViridianForest_EventScript_TrainerTips2': 'tips2', 'ViridianForest_EventScript_TrainerTips3': 'tips3',
      'ViridianForest_EventScript_TrainerTips4': 'tips4', 'ViridianForest_EventScript_TrainerTips5': 'tips5', 'ViridianForest_EventScript_ExitSign': 'exit'}
for b in d['bg_events']:
    if b['type'] == 'sign': b['x'], b['y'] = info['signs'][SG[b['script']]]
    elif b['item'] == 'ITEM_POTION': b['x'], b['y'] = info['hid']['potion']
    elif b['item'] == 'ITEM_ANTIDOTE': b['x'], b['y'] = info['hid']['antidote']
d['weather'] = 'WEATHER_VOLCANIC_ASH'
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
f = 'data/maps/ViridianForest/text.inc'; s = open(f).read()
s = s.replace('"LEAVING OPANIHRUM FOREST\\n"', '"LEAVING CINDER FOREST\\n"')
open(f, 'w').write(s)
print('evenements foret ecrits')
