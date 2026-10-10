# ROUTE 4 : evenements (grottes du Mont Selenite, Centre, warps Route 3 <-> Route 4 <-> Azuria, PNJ, panneaux, objets caches). A lancer apres route4_map.py. Idempotent.
import json
info = json.load(open('/tmp/route4_info.json'))
W, H = info['w'], info['h']
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
a1, a2, ce = info['arch1'], info['arch2'], info['center']
f = 'data/maps/Route4/map.json'; d = json.load(open(f))
d['warp_events'] = ([warp(a1[0] + 1, a1[1] + 2, 'MAP_MT_MOON_1F', 3), warp(a2[0] + 1, a2[1] + 2, 'MAP_MT_MOON_B1F', 7), warp(ce[0] + 2, ce[1] + 4, 'MAP_ROUTE4_POKEMON_CENTER_1F', 1)]
                    + [warp(x, H - 1, 'MAP_ROUTE3', 5) for x in (18, 19, 20, 21)] + [warp(x, H - 1, 'MAP_ROUTE3', 5) for x in (19, 18, 20, 21)]
                    + [warp(W - 1, y, 'MAP_ROUTE4_EAST', c) for y, c in zip(range(info['east_rows'][0], info['east_rows'][1] + 1), (0, 1, 2, 3))])
d['connections'] = []
d['weather'] = 'WEATHER_VOLCANIC_ASH'
POS = {'Route4_EventScript_Woman': 'woman', 'Route4_EventScript_Crissy': 'crissy', 'Route4_EventScript_ItemTM05': 'tm05', 'Route4_EventScript_Boy': 'boy',
       'Route4_EventScript_MegaPunchTutor': 'mpunch', 'Route4_EventScript_MegaKickTutor': 'mkick'}
objs = []
for o in d['object_events']:
    if o['type'] == 'clone': continue                      # le garde de la grotte Azuria n'est plus visible d'ici (plus de frontiere commune)
    k = POS[o['script']]; o['x'], o['y'] = info['obj'][k]
    if k in info['face']:
        o['movement_type'] = 'MOVEMENT_TYPE_FACE_' + info['face'][k]; o['trainer_sight_or_berry_tree_id'] = str(info['sight'][k])
    objs.append(o)
d['object_events'] = objs
HIDN = {'ITEM_GREAT_BALL': 'great', 'ITEM_PERSIM_BERRY': 'persim', 'ITEM_RAZZ_BERRY': 'razz'}
for b in d['bg_events']:
    if b['type'] == 'sign': b['x'], b['y'] = info['signs']['mtmoon' if 'MtMoon' in b['script'] else 'route']
    elif b['type'] == 'hidden_item': b['x'], b['y'] = info['hid'][HIDN[b['item']]]
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
print('evenements route 4 ecrits')
