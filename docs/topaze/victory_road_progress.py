#!/usr/bin/env python3
"""Route Victoire : vraie progression (23/10). Idempotent.
- 1F : l'eboulis ONYBRIS scelle le couloir menant a l'echelle de la 2F (barriere de rochers en (4..5, 8..9)) tant que
  FLAG_VR_BOSS_DONE n'est pas pose ; une echelle visible (18,1), dans l'alcove nord-est, mene au repaire (infirmiere a cote).
- 2F : plus d'echelle du repaire, plus de mur de brume a la sortie, infirmiere deplacee en 1F.
- Repaire 1F : les entrees ramenent a la 1F."""
import json, struct, copy
def jl(p): return json.load(open(p))
def js(p, d): json.dump(d, open(p, 'w'), indent=2); open(p, 'a').write('\n')
def words(p): d = open(p, 'rb').read(); return list(struct.unpack('<%dH' % (len(d) // 2), d))
def put(p, w): open(p, 'wb').write(struct.pack('<%dH' % len(w), *w))
# ---- layouts
p1 = 'data/layouts/VictoryRoad_1F/map.bin'; w1 = words(p1); W1 = 48
w1[0 * W1 + 18] = 0x068e; w1[1 * W1 + 18] = 0x3297          # echelle du repaire (haut collision + case de warp)
put(p1, w1)
p2 = 'data/layouts/VictoryRoad_2F/map.bin'; w2 = words(p2); W2 = 51
if w2[0 * W2 + 30] == 0x068e:                               # retire l'echelle du repaire (copie les cases voisines)
    w2[0 * W2 + 30] = w2[0 * W2 + 29]; w2[1 * W2 + 30] = w2[1 * W2 + 29]
put(p2, w2)
# ---- 2F
m2 = jl('data/maps/VictoryRoad_2F/map.json')
nurse = [o for o in m2['object_events'] if o['script'] == 'VictoryRoad_2F_EventScript_Nurse']
m2['object_events'] = [o for o in m2['object_events'] if o['script'] != 'VictoryRoad_2F_EventScript_Nurse']
m2['warp_events'] = [w for w in m2['warp_events'] if w['dest_map'] != 'MAP_VICTORY_ROAD_LAIR_1F']
m2['coord_events'] = [c for c in m2['coord_events'] if 'ExitBlocked' not in c['script']]
js('data/maps/VictoryRoad_2F/map.json', m2)
# ---- 1F
m1 = jl('data/maps/VictoryRoad_1F/map.json')
if not any(o['script'] == 'VictoryRoad_1F_EventScript_Nurse' for o in m1['object_events']):
    n = nurse[0] if nurse else None
    n = copy.deepcopy(n) if n else {'type': 'object', 'graphics_id': 'OBJ_EVENT_GFX_NURSE', 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0', 'flag': '0'}
    n.update(x=19, y=2, elevation=3, movement_type='MOVEMENT_TYPE_FACE_LEFT', script='VictoryRoad_1F_EventScript_Nurse'); n.pop('local_id', None)
    m1['object_events'].append(n)
if not any(w['dest_map'] == 'MAP_VICTORY_ROAD_LAIR_1F' for w in m1['warp_events']):
    m1['warp_events'].append({'x': 18, 'y': 1, 'elevation': 3, 'dest_map': 'MAP_VICTORY_ROAD_LAIR_1F', 'dest_warp_id': '0'})
if not any(c['script'] == 'VictoryRoad_1F_EventScript_Rubble' for c in m1['coord_events']):
    m1['coord_events'].append({'type': 'trigger', 'x': 5, 'y': 10, 'elevation': 3, 'var': 'VAR_TEMP_0', 'var_value': '0', 'script': 'VictoryRoad_1F_EventScript_Rubble'})
js('data/maps/VictoryRoad_1F/map.json', m1)
# ---- repaire 1F : entrees -> 1F de la route
ml = jl('data/maps/VictoryRoadLair_1F/map.json')
for w in ml['warp_events']:
    if w['dest_map'] == 'MAP_VICTORY_ROAD_2F': w['dest_map'] = 'MAP_VICTORY_ROAD_1F'; w['dest_warp_id'] = '2'
js('data/maps/VictoryRoadLair_1F/map.json', ml)
print('ok')
