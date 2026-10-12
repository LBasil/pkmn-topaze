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
# ---- maisons entrables : un interieur propre par porte (clone de SaffronCity_House, residents a replique placeholder), warps ville <-> interieur
import os, shutil
HOMES = sorted((k, v[0]) for k, v in D.items() if k.startswith('home'))
LET = 'ABCDEFGHIJKLMNOPQRST'
RES = [('OBJ_EVENT_GFX_LASS', "The streetlights never go out here.\nI stopped wondering why."), ('OBJ_EVENT_GFX_OLD_WOMAN', "I've lived here since before the TEAM came.\nThe sun? Barely remember it."),
       ('OBJ_EVENT_GFX_MAN', "Rent is cheap. The view is... grey."), ('OBJ_EVENT_GFX_BOY', "I found a red crystal in the alley!\nMom says don't touch it."),
       ('OBJ_EVENT_GFX_WORKER_M', "Night shift at the tower.\nOr is it day shift? Who can tell."), ('OBJ_EVENT_GFX_WOMAN_1', "Keep your curtains shut.\nThe glow from the tower is unsettling."),
       ('OBJ_EVENT_GFX_GENTLEMAN', "This was the biggest city in KANTO.\nIt still is. Just... quieter."), ('OBJ_EVENT_GFX_LITTLE_GIRL', "I drew the sun on my wall.\nDo you like it?"),
       ('OBJ_EVENT_GFX_FAT_MAN', "Business is slow, but the crowds\nnever leave this city."), ('OBJ_EVENT_GFX_BEAUTY', "NOX's POKéMON are everywhere at night.\nOr maybe it's always night."),
       ('OBJ_EVENT_GFX_YOUNGSTER', "I'm training for the GYM.\nThe dark types here are no joke!"), ('OBJ_EVENT_GFX_OLD_WOMAN', "My grandson says there is a sky\nabove the towers. I believe him."),
       ('OBJ_EVENT_GFX_MAN', "TEAM ONYBRIS patrols at dusk.\nBe polite and they leave you alone."), ('OBJ_EVENT_GFX_LASS', "Lights out? Never. We just\ndon't have a switch.")]
src = json.load(open('data/maps/SaffronCity_House/map.json')); grp = json.load(open('data/maps/map_groups.json'))
gname = next(k for k, v in grp.items() if isinstance(v, list) and 'SaffronCity_House' in v)
d['warp_events'] = [w for w in d['warp_events'] if not w['dest_map'].startswith('MAP_SAFFRON_CITY_HOME_')]
ev = open('data/event_scripts.s').read()
for i, (k, (hx, hy)) in enumerate(HOMES):
    nm = 'SaffronCity_Home' + LET[i]; mid = 'MAP_SAFFRON_CITY_HOME_' + LET[i]; widx = len(d['warp_events'])
    d['warp_events'].append({"x": hx, "y": hy, "elevation": 0, "dest_map": mid, "dest_warp_id": "1"})
    m = json.loads(json.dumps(src)); m['id'] = mid; m['name'] = nm
    gfx, txt = RES[i % len(RES)]
    m['object_events'] = [{"type": "object", "graphics_id": gfx, "x": 4, "y": 4, "elevation": 3, "movement_type": "MOVEMENT_TYPE_FACE_DOWN", "movement_range_x": 1, "movement_range_y": 1,
                           "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": nm + '_EventScript_Resident', "flag": "0"}]
    m['bg_events'] = []
    for w in m['warp_events']: w['dest_map'] = 'MAP_SAFFRON_CITY'; w['dest_warp_id'] = str(widx)
    os.makedirs('data/maps/' + nm, exist_ok=True); jdump(m, 'data/maps/%s/map.json' % nm)
    open('data/maps/%s/scripts.inc' % nm, 'w').write('%s_MapScripts::\n\t.byte 0\n\n%s_EventScript_Resident::\n\tmsgbox %s_Text_Resident, MSGBOX_NPC\n\tend\n' % (nm, nm, nm))
    open('data/maps/%s/text.inc' % nm, 'w').write('%s_Text_Resident::\n    .string "%s$"\n' % (nm, txt.replace('\n', '\\n').replace('\\n', '\\n')))
    if nm not in grp[gname]: grp[gname].append(nm)
    for kind, anchor in (('scripts', 'data/maps/SaffronCity_House/scripts.inc'), ('text', 'data/maps/SaffronCity_House/text.inc')):
        line = '\t.include "data/maps/%s/%s.inc"\n' % (nm, kind)
        if line not in ev: ev = ev.replace('\t.include "%s"\n' % anchor, '\t.include "%s"\n' % anchor + line, 1)
open('data/event_scripts.s', 'w').write(ev); jdump(grp, 'data/maps/map_groups.json')
print('interieurs de maisons', len(HOMES))
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
