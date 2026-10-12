# HEMATOWN (ex-Saffron, LAYOUT_SAFFRON_CITY 66x55) : evenements. A lancer apres hematown_town.py. Idempotent.
# Les 4 tunnels (portes de ville) restent en place : warps et connexions des routes inchangees (les routes 5/6/7/8 pointent sur la "connection map").
import json, re
D = json.load(open('/tmp/hematown_doors.json')); N = json.load(open('/tmp/hematown_npc.json')); S = json.load(open('/tmp/hematown_signs.json'))
def jdump(o, f): json.dump(o, open(f, 'w'), indent=2); open(f, 'a').write('\n')
f = 'data/maps/SaffronCity/map.json'; d = json.load(open(f))
DM = {'MAP_SILPH_CO_1F': 'silph', 'MAP_SAFFRON_CITY_COPYCATS_HOUSE_1F': 'copy', 'MAP_SAFFRON_CITY_DOJO': 'dojo', 'MAP_SAFFRON_CITY_GYM': 'gym',
      'MAP_SAFFRON_CITY_HOUSE': 'house', 'MAP_SAFFRON_CITY_MART': 'mart', 'MAP_SAFFRON_CITY_POKEMON_CENTER_1F': 'pc',
      'MAP_SAFFRON_CITY_MR_PSYCHICS_HOUSE': 'psy', 'MAP_SAFFRON_CITY_POKEMON_TRAINER_FAN_CLUB': 'fan'}
for w in d['warp_events']:
    k = DM.get(w['dest_map'])
    if k: w['x'], w['y'] = D[k][0]
NP = {'RocketGrunt1': 'grunt1', 'RocketGrunt2': 'grunt2', 'RocketGrunt3': 'grunt3', 'RocketGrunt4': 'grunt4', 'RocketGrunt5': 'grunt5', 'RocketGrunt6': 'grunt6',
      'RocketGrunt7': 'grunt7', 'DoorGuardGrunt': 'guard', 'Youngster': 'youngster', 'WorkerM': 'worker', 'Man': 'man', 'Boy': 'boy', 'Pidgeot': 'pidgeot', 'Lass': 'lass', 'CrushGirl': 'crush'}
for o in d['object_events']:
    k = (o.get('script') or '').replace('SaffronCity_EventScript_', '')
    assert k in NP, k
    o['x'], o['y'] = N[NP[k]]
SG = {'CitySign': 'city', 'DojoSign': 'dojo', 'GymSign': 'gym', 'SilphProductSign': 'silphproduct', 'TrainerTips2': 'tips2', 'SilphCoSign': 'silphco',
      'TrainerTips1': 'tips1', 'MrPsychicsHouseSign': 'psy', 'TrainerFanClubSign': 'fanclub'}
for b in d['bg_events']:
    k = (b.get('script') or '').replace('SaffronCity_EventScript_', '')
    if b['type'] == 'sign' and k in SG: b['x'], b['y'] = S[SG[k]]; b['elevation'] = 0
d['connections'] = []          # joint de tileset visible sinon : les routes arrivent par les tunnels
d['weather'] = 'WEATHER_SHADE'  # "HEMATOWN never sees the sun" (repasser a WEATHER_SUNNY si trop sombre)
jdump(d, f)
f = 'data/maps/SaffronCity/text.inc'; s = open(f).read()
s = s.replace('    .string "Shining, Golden Land of Commerce$"', '    .string "The City the Sun Forgot$"'); open(f, 'w').write(s)
f = 'src/data/heal_locations.json'; s = open(f).read()
x, y = D['pc'][0]
s2 = re.sub(r'("id": "HEAL_LOCATION_SAFFRON_CITY",\s*"map": "MAP_SAFFRON_CITY",\s*"x": )\d+(,\s*"y": )\d+', lambda m: '%s%d%s%d' % (m.group(1), x, m.group(2), y + 1), s)
assert s2 != s or '"x": %d,' % x in s; open(f, 'w').write(s2)
print('evenements Hematown ecrits')
