# ROUTE 1 (route du degrade) : evenements. A lancer apres route1_gradient.py. Idempotent.
import json, re
info = json.load(open('/tmp/route1_info.json')); H = info['h']
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
f = 'data/maps/Route1/map.json'; d = json.load(open(f))
d['warp_events'] = [warp(12, H - 1, 'MAP_PALLET_TOWN', 4), warp(13, H - 1, 'MAP_PALLET_TOWN', 5),                    # 0,1 : Grenalux
                    warp(14, 0, 'MAP_VIRIDIAN_CITY', 8), warp(15, 0, 'MAP_VIRIDIAN_CITY', 8), warp(16, 0, 'MAP_VIRIDIAN_CITY', 9), warp(17, 0, 'MAP_VIRIDIAN_CITY', 9)]
for o in d['object_events']:
    if o['script'] == 'Route1_EventScript_MartClerk': o['x'], o['y'] = info['npc']['clerk']; o['movement_type'] = 'MOVEMENT_TYPE_FACE_LEFT'; o['movement_range_x'] = 0; o['movement_range_y'] = 0
    if o['script'] == 'Route1_EventScript_Boy': o['x'], o['y'] = info['npc']['boy']; o['movement_range_x'] = 1; o['movement_range_y'] = 0
for b in d['bg_events']: b['x'], b['y'] = info['sign']
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
f = 'data/maps/Route1/text.inc'; s = open(f).read()
s = re.sub(r'(?s)Route1_Text_CanJumpFromLedges::\n.*?\n\n', lambda m: 'Route1_Text_CanJumpFromLedges::\n    .string "Notice how the grass changes color\\n"\n    .string "as you walk this road?\\p"\n    .string "Red near GRENALUX, black and teal\\n"\n    .string "near OPANIHRUM.\\p"\n    .string "Grown-ups say the crystals do it.$"\n\n', s)
open(f, 'w').write(s)
print('evenements Route 1 ecrits')
