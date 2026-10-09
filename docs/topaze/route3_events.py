# ROUTE 3 : evenements (warps Pyropia <-> Route 3 <-> Route 4, dresseurs, panneau, objet cache, cendres). A lancer apres route3_map.py. Idempotent.
import json
info = json.load(open('/tmp/route3_info.json'))
W, H = info['w'], info['h']
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
f = 'data/maps/Route3/map.json'; d = json.load(open(f))
# Pyropia : warps 9 et 10 -> Route 3 warps 0 et 1 ; Route 4 : warps 3..10 (x=8..15, y=19) <-> Route 3 est
d['warp_events'] = [warp(0, 11, 'MAP_PEWTER_CITY', 9), warp(0, 12, 'MAP_PEWTER_CITY', 10), warp(0, 10, 'MAP_PEWTER_CITY', 9), warp(0, 13, 'MAP_PEWTER_CITY', 10)] + \
                   [warp(W - 1, y, 'MAP_ROUTE4', 7) for y in (14, 15, 16, 17)]
d['connections'] = []
POS = {'Route3_EventScript_Youngster': 'youngster', 'Route3_EventScript_Colton': 'colton', 'Route3_EventScript_Ben': 'ben', 'Route3_EventScript_Janice': 'janice',
       'Route3_EventScript_Greg': 'greg', 'Route3_EventScript_Calvin': 'calvin', 'Route3_EventScript_Sally': 'sally', 'Route3_EventScript_James': 'james', 'Route3_EventScript_Robin': 'robin'}
for o in d['object_events']:
    k = POS[o['script']]; o['x'], o['y'] = info['obj'][k]
    if k in info['face']:
        o['movement_type'] = 'MOVEMENT_TYPE_FACE_' + info['face'][k]; o['trainer_sight_or_berry_tree_id'] = str(info['sight'][k])
for b in d['bg_events']:
    if b['type'] == 'sign': b['x'], b['y'] = info['signs']['sign']
    elif b['type'] == 'hidden_item': b['x'], b['y'] = info['hid']['oran']
d['weather'] = 'WEATHER_VOLCANIC_ASH'
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# Route 4 : plus de connexion vers la Route 3 (tilesets differents) : warps a pas simple a la place
f = 'data/maps/Route4/map.json'; d = json.load(open(f))
d['connections'] = [c for c in d.get('connections', []) if c['map'] != 'MAP_ROUTE3']
d['warp_events'] = d['warp_events'][:3] + [warp(x, 19, 'MAP_ROUTE3', 5) for x in range(8, 16)]
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
print('evenements route 3 ecrits')
