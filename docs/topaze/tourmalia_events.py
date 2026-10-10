# TOURMALIA (ex-Azuria, LAYOUT_CERULEAN_CITY) : evenements. A lancer apres tourmalia_town.py. Idempotent.
import json, re
D = json.load(open('/tmp/tourmalia_doors.json')); N = json.load(open('/tmp/tourmalia_npc.json'))
S = json.load(open('/tmp/tourmalia_signs.json')); M = json.load(open('/tmp/tourmalia_misc.json'))
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
def door(k): return D[k][0]
C = 'MAP_CERULEAN_CITY_'
W = [None] * 27
def put(i, xy, dest, wid): W[i] = warp(xy[0], xy[1], dest, wid)
put(0, door('th1'), C + 'HOUSE1', 1); put(1, door('th4'), C + 'HOUSE2', 1); put(2, door('th3'), C + 'HOUSE3', 1)
put(3, door('center'), C + 'POKEMON_CENTER_1F', 1); put(4, door('gym'), C + 'GYM', 1); put(5, door('th5'), C + 'BIKE_SHOP', 1)
put(6, door('mart'), C + 'MART', 1); put(7, M['grot_door'], 'MAP_CERULEAN_CAVE_1F', 0)
put(8, (0, 0), C + 'HOUSE1', 3)                                  # porte arriere inutilisee (case inaccessible)
put(9, M['hole'][0], C + 'HOUSE2', 3); put(10, M['hole'][1], C + 'HOUSE2', 3)
put(11, (0, 1), C + 'BIKE_SHOP', 1)
put(12, door('th6'), C + 'HOUSE4', 0); put(13, door('th2'), C + 'HOUSE5', 0)
for i, y in enumerate(range(19, 23)): put(14 + i, (0, y), 'MAP_ROUTE4', 11 + i)
for i, x in enumerate((22, 23, 24)): put(18 + i, (x, 0), 'MAP_ROUTE24', i)
for i, y in enumerate((18, 19)): put(21 + i, (47, y), 'MAP_ROUTE9', i)
for i, x in enumerate(range(22, 26)): put(23 + i, (x, 39), 'MAP_ROUTE5', 4 + i)
f = 'data/maps/CeruleanCity/map.json'; d = json.load(open(f))
d['warp_events'] = W; d['connections'] = []; d['weather'] = 'WEATHER_RAIN'
pos = {'LOCALID_CERULEAN_POLICEMAN': N['policeman'], 'LOCALID_CERULEAN_GRUNT': N['grunt'], 'LOCALID_CERULEAN_SLOWBRO': N['slowbro'],
       'LOCALID_CERULEAN_LASS': N['lass'], 'LOCALID_CERULEAN_RIVAL': N['rival'], 'LOCALID_CERULEAN_WOMAN': N['woman'], 'LOCALID_CERULEAN_CAVE_GUARD': N['guard']}
gfx = {'OBJ_EVENT_GFX_LITTLE_BOY': 'boy', 'OBJ_EVENT_GFX_BALDING_MAN': 'balding', 'OBJ_EVENT_GFX_YOUNGSTER': 'youngster', 'OBJ_EVENT_GFX_CUT_TREE': 'cuttree'}
objs = []
for o in d['object_events']:
    if o['type'] == 'clone': continue
    p = pos.get(o.get('local_id')) or N[gfx[o['graphics_id']]]
    o['x'], o['y'] = p; objs.append(o)
d['object_events'] = objs
for c in d['coord_events']:
    if 'Rival' in c['script']:
        c['y'] = 6
    else:
        c['x'] = N['gtop' if 'Top' in c['script'] else 'gbottom'][0]; c['y'] = N['gtop' if 'Top' in c['script'] else 'gbottom'][1]
SG = {'CitySign': 'city', 'GymSign': 'gym', 'BikeShopSign': 'bike', 'TrainerTips': 'tips'}
bg = []
for b in d['bg_events']:
    if b['type'] == 'sign':
        if 'Bicycle' in b['script']: continue
        b['x'], b['y'] = S[SG[b['script'].split('_')[-1]]]
    elif b['type'] == 'hidden_item': b['x'], b['y'] = N['hidden']
    bg.append(b)
d['bg_events'] = bg
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# retour : Route 4 (ids 14..17), Route 24 / 5 / 9 (plus de connexion Azuria)
f = 'data/maps/Route4/map.json'; r = json.load(open(f))
for w, i in zip(r['warp_events'][-4:], (14, 15, 16, 17)): w['dest_warp_id'] = str(i)
json.dump(r, open(f, 'w'), indent=2); open(f, 'a').write('\n')
def edit(name, newwarps, keep=0):
    f = f'data/maps/{name}/map.json'; r = json.load(open(f))
    r['connections'] = [c for c in r['connections'] if c['map'] != 'MAP_CERULEAN_CITY']
    r['warp_events'] = r['warp_events'][:keep] + newwarps
    json.dump(r, open(f, 'w'), indent=2); open(f, 'a').write('\n')
edit('Route24', [warp(10 + i, 39, 'MAP_CERULEAN_CITY', 18 + i) for i in range(3)])
edit('Route9', [warp(0, 8 + i, 'MAP_CERULEAN_CITY', 21 + i) for i in range(2)])
edit('Route5', [warp(22 + i, 0, 'MAP_CERULEAN_CITY', 23 + i) for i in range(4)], keep=4)
# scripts : barrages (apres le billet), texte du panneau
f = 'data/maps/CeruleanCity/scripts.inc'; s = open(f).read()
for k, key in (('POLICEMAN', 'policeman_block'), ('SLOWBRO', 'slowbro_block'), ('LASS', 'lass_block')):
    s = re.sub(r'(setobjectxyperm LOCALID_CERULEAN_%s, )\d+, \d+' % k, r'\g<1>%d, %d' % tuple(N[key]), s)
open(f, 'w').write(s)
f = 'data/maps/CeruleanCity/text.inc'; s = open(f).read()
s = re.sub(r'(CeruleanCity_Text_CitySign::\n).*?\$"', r'\1    .string "TOURMALIA CITY\\n"\n    .string "Where the forest grows crystal$"', s, count=1, flags=re.S)
open(f, 'w').write(s)
# soin / reapparition : porte du Centre + 1
f = 'src/data/heal_locations.h'; s = open(f).read()
x, y = door('center')
s = re.sub(r'(HEAL_LOCATION_CERULEAN_CITY - 1\] = \{.*?\.x = )\d+(,\s*\.y = )\d+', r'\g<1>%d\g<2>%d' % (x, y + 1), s, count=1, flags=re.S)
open(f, 'w').write(s)
# pas simples sur Routes 24 / 5 / 9
f = 'src/field_control_avatar.c'; s = open(f).read()
if 'LAYOUT_ROUTE24' not in s:
    s = s.replace('|| gMapHeader.mapLayoutId == LAYOUT_CERULEAN_CITY;', '|| gMapHeader.mapLayoutId == LAYOUT_CERULEAN_CITY\n        || gMapHeader.mapLayoutId == LAYOUT_ROUTE24 || gMapHeader.mapLayoutId == LAYOUT_ROUTE5 || gMapHeader.mapLayoutId == LAYOUT_ROUTE9;')
    open(f, 'w').write(s)
print('evenements Tourmalia ecrits')
