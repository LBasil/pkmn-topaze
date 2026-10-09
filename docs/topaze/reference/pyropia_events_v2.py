# PYROPIA v2 : evenements de la ville (warps, PNJ, panneaux), sorties vers les routes 2 (sud) et 3 (est). Idempotent.
# A lancer apres pyropia_town.py (lit /tmp/pyropia_npc.json, _doors.json, _signs.json). Les liaisons routes sont des WARPS (tilesets differents).
import json, re, copy
NPC = json.load(open('/tmp/pyropia_npc.json')); DR = json.load(open('/tmp/pyropia_doors.json')); SG = json.load(open('/tmp/pyropia_signs.json'))
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
f = 'data/maps/PewterCity/map.json'; d = json.load(open(f))
# ---- objets : on garde la fille, le gros monsieur et le gamin ; plus de guide (courses scriptees), d'arbre a couper ni d'assistant
where = {'PewterCity_EventScript_Lass': 'lass', 'PewterCity_EventScript_FatMan': 'fatman', 'PewterCity_EventScript_BugCatcher': 'bugcatcher'}
objs = []
for o in d['object_events']:
    if o['script'] == 'EventScript_CutTree': continue
    if o['script'] in where: o['x'], o['y'] = NPC[where[o['script']]]
    else: o['x'], o['y'] = 3, 3          # guides / assistant : gardes pour leurs LOCALID (scripts d'origine), caches par OnTransition ci-dessous
    objs.append(o)
d['object_events'] = objs
# ---- warps : 0,1 musee (2 ailes), 2 arene, 3 boutique, 4 maison, 5 centre, 6 maison 2 (ordre d'origine : les interieurs y renvoient), 7,8 sud, 9,10 est
d['warp_events'] = [warp(*DR['museumA'], 'MAP_PEWTER_CITY_MUSEUM_1F', 1), warp(*DR['museumB'], 'MAP_PEWTER_CITY_MUSEUM_1F', 3),
                    warp(*DR['gym'], 'MAP_PEWTER_CITY_GYM', 1), warp(*DR['mart'], 'MAP_PEWTER_CITY_MART', 1), warp(*DR['house1'], 'MAP_PEWTER_CITY_HOUSE1', 1),
                    warp(*DR['center'], 'MAP_PEWTER_CITY_POKEMON_CENTER_1F', 1), warp(*DR['house2'], 'MAP_PEWTER_CITY_HOUSE2', 1),
                    warp(22, 39, 'MAP_ROUTE2', 15), warp(23, 39, 'MAP_ROUTE2', 16),
                    warp(47, 22, 'MAP_ROUTE3', 0), warp(47, 23, 'MAP_ROUTE3', 1)]
d['connections'] = []
d['coord_events'] = []
# ---- panneaux (les 5 d'origine) + objet cache
S = {'PewterCity_EventScript_MuseumSign': 'museum', 'PewterCity_EventScript_PoliceNotice': 'police', 'PewterCity_EventScript_GymSign': 'gym',
     'PewterCity_EventScript_TrainerTips': 'tips', 'PewterCity_EventScript_CitySign': 'city'}
for b in d['bg_events']:
    if b.get('script') in S: b['x'], b['y'] = SG[S[b['script']]]
    else: b['x'], b['y'] = NPC['hidden']
json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# ---- OnTransition : les 3 PNJ scriptes d'origine restent caches
f = 'data/maps/PewterCity/scripts.inc'; s = open(f).read()
add = '\tsetflag FLAG_HIDE_PEWTER_CITY_GYM_GUIDE\n\tsetflag FLAG_HIDE_PEWTER_MUSEUM_GUIDE\n\tsetflag FLAG_HIDE_PEWTER_CITY_RUNNING_SHOES_GUY\n'
if 'Pyropia' not in s:
    s = s.replace('\tsetvar VAR_MAP_SCENE_PEWTER_CITY_MUSEUM_1F, 0\n\tend\n', '\tsetvar VAR_MAP_SCENE_PEWTER_CITY_MUSEUM_1F, 0\n@ Pyropia: pas de guides scriptes (cf. docs/topaze/pyropia_events.py)\n' + add + '\tend\n', 1)
open(f, 'w').write(s)
# ---- textes propres a Pyropia
f = 'data/maps/PewterCity/text.inc'; s = open(f).read()
s = re.sub(r'(?s)PewterCity_Text_CitySign::\n.*?\n\n', lambda m: 'PewterCity_Text_CitySign::\n    .string "PYROPIA\\n"\n    .string "City at the Foot of the Volcano$"\n\n', s)
s = re.sub(r'(?s)PewterCity_Text_GymSign::\n.*?\n\n', lambda m: 'PewterCity_Text_GymSign::\n    .string "PYROPIA POKéMON GYM\\n"\n    .string "LEADER: KAY$"\n\n', s)
open(f, 'w').write(s)
# ---- soin : devant la porte du Centre (le .h est genere depuis le json et ignore par git)
f = 'src/data/heal_locations.json'; s = open(f).read()
cx, cy = DR['center']
s = re.sub(r'("id": "HEAL_LOCATION_PEWTER_CITY",\n\s*"map": "[A-Z_0-9]+",\n\s*"x": )\d+(,\n\s*"y": )\d+', lambda m: m.group(1) + str(cx) + m.group(2) + str(cy + 1), s)
open(f, 'w').write(s)
# ---- routes : warps a la place des connexions
def patch_route(name, drop_dir, new_warps):
    f = 'data/maps/%s/map.json' % name; m = json.load(open(f))
    m['connections'] = [c for c in m['connections'] if c['direction'] != drop_dir]
    m['warp_events'] = [w for w in m['warp_events'] if w['dest_map'] != 'MAP_PEWTER_CITY'] + new_warps
    json.dump(m, open(f, 'w'), indent=2); open(f, 'a').write('\n')
    return len(m['warp_events']) - len(new_warps)
i2 = patch_route('Route2', 'up', [warp(8, 0, 'MAP_PEWTER_CITY', 7), warp(9, 0, 'MAP_PEWTER_CITY', 7), warp(10, 0, 'MAP_PEWTER_CITY', 8), warp(11, 0, 'MAP_PEWTER_CITY', 8)])
i3 = patch_route('Route3', 'left', [warp(0, 9, 'MAP_PEWTER_CITY', 9), warp(0, 10, 'MAP_PEWTER_CITY', 9), warp(0, 11, 'MAP_PEWTER_CITY', 10), warp(0, 12, 'MAP_PEWTER_CITY', 10)])
assert (i2, i3) == (15, 0), (i2, i3)       # indices de destination utilises ci-dessus (Route2: 15,16 ; Route3: 0,1)
print('evenements Pyropia ecrits')
