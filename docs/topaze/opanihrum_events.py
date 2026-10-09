# OPANIHRUM : evenements de la ville (warps, PNJ, panneaux, declencheurs) + sorties vers les routes.
# A lancer apres opanihrum_town.py (lit /tmp/opanihrum_npc.json et /tmp/opanihrum_doors.json). Idempotent.
# Comme pour Grenalux, les liaisons avec les routes sont des WARPS (tilesets differents -> les connexions affichent des tuiles brouillees).
import json, re, copy
NPC = json.load(open('/tmp/opanihrum_npc.json')); DR = json.load(open('/tmp/opanihrum_doors.json'))
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
f = 'data/maps/ViridianCity/map.json'; d = json.load(open(f))
# ---- objets
where = {'ViridianCity_EventScript_DreamEaterTutor': 'fatman', 'ViridianCity_EventScript_OldMan': 'oldman', 'ViridianCity_EventScript_Woman': 'woman',
         'ViridianCity_EventScript_Youngster': 'youngster', 'ViridianCity_EventScript_Boy': 'boy', 'ViridianCity_EventScript_ItemPotion': 'potion'}
objs = []
for o in d['object_events']:
    if o['script'] == 'EventScript_CutTree': continue                       # plus d'arbres a couper : la place est dallee
    if o['script'] in where: o['x'], o['y'] = NPC[where[o['script']]]
    if o['script'] == 'ViridianCity_EventScript_TutorialOldMan':
        o['x'], o['y'] = 18, 6; o['movement_range_x'] = 0; o['movement_range_y'] = 0
    if o['script'] == 'ViridianCity_EventScript_Youngster': o['movement_range_y'] = 1
    if o['script'] == 'ViridianCity_EventScript_Boy': o['movement_range_x'] = 1; o['movement_range_y'] = 1
    objs.append(o)
d['object_events'] = objs
# ---- warps : 0 centre, 1 maison, 2 arene (porte gauche), 3 ecole, 4 boutique (ordre d'origine : les interieurs y renvoient), 5 arene (porte droite)
W = d['warp_events']
for w, (x, y) in zip(W[:5], [DR['center'][0], DR['house'][0], DR['foundry'][0], DR['school'][0], DR['mart'][0]]): w['x'] = x; w['y'] = y
W = W[:5] + [warp(DR['foundry'][1][0], DR['foundry'][1][1], 'MAP_VIRIDIAN_CITY_GYM', 1)]
W += [warp(20, 0, 'MAP_ROUTE2', 11), warp(21, 0, 'MAP_ROUTE2', 13),          # 6,7 : nord (route 2)
      warp(20, 39, 'MAP_ROUTE1', 3), warp(21, 39, 'MAP_ROUTE1', 4),          # 8,9 : sud (route 1)
      warp(0, 22, 'MAP_ROUTE22', 3), warp(0, 23, 'MAP_ROUTE22', 4)]          # 10,11 : ouest (route 22)
d['warp_events'] = W
d['connections'] = []
# ---- panneaux
S = {'ViridianCity_EventScript_TrainerTips1': [(23, 3)], 'ViridianCity_EventScript_GymSign': [(11, 13)], 'ViridianCity_EventScript_TrainerTips2': [(23, 31)],
     'ViridianCity_EventScript_CitySign': [(23, 16)], 'ViridianCity_EventScript_GymDoor': [tuple(DR['foundry'][0]), tuple(DR['foundry'][1])]}
bg = []
for b in d['bg_events']:
    cells = S[b['script']]
    for (x, y) in cells:
        nb = copy.deepcopy(b); nb['x'], nb['y'] = x, y; bg.append(nb)
d['bg_events'] = bg
# ---- declencheurs : vieil homme a la porte nord de la place (2 cases : il en bloque une, le declencheur couvre l'autre), arene verrouillee
def trig(x, y, var, val, script): return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": str(val), "script": script}
fx = DR['foundry']
d['coord_events'] = [trig(21, 2, 'VAR_MAP_SCENE_VIRIDIAN_CITY_OLD_MAN', 0, 'ViridianCity_EventScript_RoadBlocked'),
                     trig(21, 2, 'VAR_MAP_SCENE_VIRIDIAN_CITY_OLD_MAN', 1, 'ViridianCity_EventScript_TutorialTriggerRight'),
                     trig(fx[0][0], fx[0][1] + 1, 'VAR_MAP_SCENE_VIRIDIAN_CITY_GYM_DOOR', 0, 'ViridianCity_EventScript_GymDoorLocked'),
                     trig(fx[1][0], fx[1][1] + 1, 'VAR_MAP_SCENE_VIRIDIAN_CITY_GYM_DOOR', 0, 'ViridianCity_EventScript_GymDoorLocked')]
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# ---- scripts : positions du vieil homme
f = 'data/maps/ViridianCity/scripts.inc'; s = open(f).read()
s = s.replace('setobjectxyperm LOCALID_TUTORIAL_MAN, 21, 8', 'setobjectxyperm LOCALID_TUTORIAL_MAN, 20, 2').replace('setobjectxyperm LOCALID_TUTORIAL_MAN, 21, 11', 'setobjectxyperm LOCALID_TUTORIAL_MAN, 20, 2')
# la porte verrouillee de l'arene : le joueur est repousse de 2 cases vers la place (saut)
open(f, 'w').write(s)
# ---- textes propres a Opanihrum
f = 'data/maps/ViridianCity/text.inc'; s = open(f).read()
s = re.sub(r'(?s)ViridianCity_Text_CitySign::\n.*?\n\n', lambda m: 'ViridianCity_Text_CitySign::\n    .string "OPANIHRUM \\n"\n    .string "City of the Black Opal$"\n\n', s)
s = re.sub(r'(?s)ViridianCity_Text_GymSign::\n.*?\n\n', lambda m: 'ViridianCity_Text_GymSign::\n    .string "OPANIHRUM POKéMON GYM\\n"\n    .string "THE FOUNDRY - LEADER: HEPHA$"\n\n', s)
open(f, 'w').write(s)
# ---- soin : le joueur reapparait devant la porte du CENTRE
f = 'src/data/heal_locations.h'; s = open(f).read()
cx, cy = DR['center'][0]
s = re.sub(r'(\[HEAL_LOCATION_VIRIDIAN_CITY - 1\] = \{\n\s*\.mapGroup = MAP_GROUP\(MAP_VIRIDIAN_CITY\),\n\s*\.mapNum = MAP_NUM\(MAP_VIRIDIAN_CITY\),\n\s*\.x = )\d+(,\n\s*\.y = )\d+', lambda m: m.group(1) + str(cx) + m.group(2) + str(cy + 1), s)
open(f, 'w').write(s)
# ---- routes : warps a la place des connexions
def patch_route(name, drop_dir, new_warps, extra=None):
    f = 'data/maps/%s/map.json' % name; m = json.load(open(f))
    m['connections'] = [c for c in m['connections'] if c['direction'] != drop_dir]
    m['object_events'] = [o for o in m['object_events'] if not (o.get('type') == 'clone' and o.get('target_map') == 'MAP_VIRIDIAN_CITY')]
    m['warp_events'] = [w for w in m['warp_events'] if w['dest_map'] != 'MAP_VIRIDIAN_CITY'] + new_warps
    json.dump(m, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# route 1 (4 cases ouvertes en haut : x 10..13, y 0) -> sud d'Opanihrum ; indices 2..5 (0,1 = Grenalux)
patch_route('Route1', 'up', [warp(10, 0, 'MAP_VIRIDIAN_CITY', 8), warp(11, 0, 'MAP_VIRIDIAN_CITY', 8), warp(12, 0, 'MAP_VIRIDIAN_CITY', 9), warp(13, 0, 'MAP_VIRIDIAN_CITY', 9)])
# route 2 (x 7..11, y 79) -> nord ; les 10 warps existants gardent leurs indices, les nouveaux sont 10..14
patch_route('Route2', 'down', [warp(7, 79, 'MAP_VIRIDIAN_CITY', 6), warp(8, 79, 'MAP_VIRIDIAN_CITY', 6), warp(9, 79, 'MAP_VIRIDIAN_CITY', 6), warp(10, 79, 'MAP_VIRIDIAN_CITY', 7), warp(11, 79, 'MAP_VIRIDIAN_CITY', 7)])
# route 22 (x 47, y 6..9) -> ouest ; existants 0,1 ; nouveaux 2..5
patch_route('Route22', 'right', [warp(47, 6, 'MAP_VIRIDIAN_CITY', 10), warp(47, 7, 'MAP_VIRIDIAN_CITY', 10), warp(47, 8, 'MAP_VIRIDIAN_CITY', 11), warp(47, 9, 'MAP_VIRIDIAN_CITY', 11)])
# warps retour : indices de destination dans les routes (voir ci-dessus)
f = 'data/maps/ViridianCity/map.json'; d = json.load(open(f))
assert [w['dest_map'] for w in d['warp_events'][6:]] == ['MAP_ROUTE2', 'MAP_ROUTE2', 'MAP_ROUTE1', 'MAP_ROUTE1', 'MAP_ROUTE22', 'MAP_ROUTE22']
for k, name in ((6, 'Route2'), (7, 'Route2'), (8, 'Route1'), (9, 'Route1'), (10, 'Route22'), (11, 'Route22')): pass
print('evenements Opanihrum ecrits')
