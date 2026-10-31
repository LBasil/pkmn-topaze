# TOURMALIA v18 (ville fluviale) : repositionne les evenements de la carte existante (portes, PNJ, panneaux, grotte) sur la nouvelle geometrie.
# A lancer apres tourmalia_river.py (lit /tmp/tourmalia_*.json). Rejouable : on retrouve chaque element par sa cle (script / local_id / destination).
import json, re
D = json.load(open('/tmp/tourmalia_doors.json')); N = json.load(open('/tmp/tourmalia_npc.json'))
S = json.load(open('/tmp/tourmalia_signs.json')); M = json.load(open('/tmp/tourmalia_misc.json'))
door = lambda k: D[k][0]
f = 'data/maps/CeruleanCity/map.json'; d = json.load(open(f))
# portes : (index, batiment) ; 8..11 = portes de secours garees dans la foret (indices stables), non touchees
WARP = {0: 'th1', 1: 'th4', 2: 'th3', 3: 'center', 4: 'gym', 5: 'th5', 6: 'mart', 12: 'th6', 13: 'th2'}
for i, k in WARP.items(): d['warp_events'][i]['x'], d['warp_events'][i]['y'] = door(k)
assert d['warp_events'][7]['dest_map'] in ('MAP_CERULEAN_CAVE_1F', 'MAP_CERULEAN_CITY_GLASS_HALL')
d['warp_events'][7]['x'], d['warp_events'][7]['y'] = M['grot_door']
POS = {'LOCALID_CERULEAN_POLICEMAN': N['policeman'], 'LOCALID_CERULEAN_SLOWBRO': N['slowbro'], 'LOCALID_CERULEAN_LASS': N['lass'], 'LOCALID_CERULEAN_RIVAL': N['rival'], 'LOCALID_CERULEAN_WOMAN': N['woman']}
GFX = {'OBJ_EVENT_GFX_LITTLE_BOY': 'boy', 'OBJ_EVENT_GFX_BALDING_MAN': 'balding', 'OBJ_EVENT_GFX_YOUNGSTER': 'youngster', 'OBJ_EVENT_GFX_CAMPER': 'camper', 'OBJ_EVENT_GFX_OLD_MAN_1': 'oldman'}
for o in d['object_events']:
    p = POS.get(o.get('local_id')) or (N[GFX[o['graphics_id']]] if o['graphics_id'] in GFX else None)
    if p: o['x'], o['y'] = p
d['coord_events'] = [c for c in d['coord_events'] if 'CaveSealed' not in c['script']]      # v28 : plus de message 'grotte scellee' (le dome est un vrai batiment visitable)
SG = {'CitySign': 'city', 'GymSign': 'gym', 'BikeShopSign': 'bike', 'TrainerTips': 'tips'}
for b in d['bg_events']:
    if b['type'] == 'sign': b['x'], b['y'] = S[SG[b['script'].split('_')[-1]]]
    elif b['type'] == 'hidden_item': b['x'], b['y'] = N['hidden']
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# barrages (apres le billet) : memes coordonnees de couloir
f = 'data/maps/CeruleanCity/scripts.inc'; s = open(f).read()
for k, key in (('POLICEMAN', 'policeman_block'), ('SLOWBRO', 'slowbro_block'), ('LASS', 'lass_block')):
    s = re.sub(r'(setobjectxyperm LOCALID_CERULEAN_%s, )\d+, \d+' % k, r'\g<1>%d, %d' % tuple(N[key]), s)
open(f, 'w').write(s)
# soin / reapparition : devant la porte du Centre (src/data/heal_locations.json ; le .h est genere)
f = 'src/data/heal_locations.json'; h = json.load(open(f)); x, y = door('center')
for l in h['heal_locations']:
    if l['id'] == 'HEAL_LOCATION_CERULEAN_CITY': l['x'], l['y'] = x, y + 1
json.dump(h, open(f, 'w'), indent=2); open(f, 'a').write('\n')
print('evenements Tourmalia v18 ecrits')

# v25 : le panneau du pied du pont indique les 4 sorties
_t = open('data/maps/CeruleanCity/text.inc').read()
_t = re.sub(r'(CeruleanCity_Text_CitySign::\n).*?\$"', lambda m: m.group(1) + '    .string "TOURMALIA CITY\\n"\n    .string "Where the forest grows crystal\\p"\n    .string "WEST:  ROUTE 4 (this road)\\n"\n    .string "SOUTH: ROUTE 5 (ladder below)\\p"\n    .string "EAST:  ROUTE 9 (past the dome)\\n"\n    .string "NORTH: ROUTE 24 (the hillside)$"', _t, count=1, flags=re.S)
open('data/maps/CeruleanCity/text.inc', 'w').write(_t)
_t = open('data/maps/CeruleanCity/text.inc').read()
_t = re.sub(r'(CeruleanCity_Text_TrainerTipsHeldItems::\n)(?:    \.string ".*"\n)*?    \.string ".*\$"', lambda m: m.group(1) + '    .string "TRAINER TIPS\\p"\n    .string "A POKéMON can be made to hold\\n"\n    .string "an item.\\p"\n    .string "Some items can even be used by\\n"\n    .string "the holding POKéMON in battle.$"', _t, count=1)
_t = re.sub(r'(CeruleanCity_Text_BikeShopSign::\n)(?:    \.string ".*"\n)*?    \.string ".*\$"', lambda m: m.group(1) + '    .string "GLASS HALL\\n"\n    .string "Open to visitors.$"', _t, count=1)
_t = _t.replace('NORTH: ROUTE 24 (the hillside)', 'NORTH: ROUTE 24 (hill path)')
open('data/maps/CeruleanCity/text.inc', 'w').write(_t)
# v28 : le dome est une vraie salle (CeruleanCity_GlassHall, cree par tourmalia_hall.py)
