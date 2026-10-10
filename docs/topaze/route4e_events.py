# ROUTE 4 EST « le sentier de tourmaline » : carte MAP_ROUTE4_EAST (plomberie, warps Route 4 <-> Route 4 Est <-> Tourmalia, panneaux). A lancer apres route4e_map.py. Idempotent.
import json, os
info = json.load(open('/tmp/route4e_info.json'))
W, H = info['w'], info['h']; R0, R1 = info['exit_rows']
M = 'Route4East'
def warp(x, y, dest, wid, el=0): return {"x": x, "y": y, "elevation": el, "dest_map": dest, "dest_warp_id": str(wid)}
ys = list(range(R0, R1 + 1))
warps = [warp(0, y, 'MAP_ROUTE4', 11 + i) for i, y in enumerate(ys)] + [warp(W - 1, y, 'MAP_CERULEAN_CITY', 14 + i) for i, y in enumerate(ys)]
def sign(c, name): return {"type": "sign", "x": c[0], "y": c[1], "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": "%s_EventScript_%s" % (M, name)}
bg = [sign(info['signs']['west'], 'WestSign'), sign(info['signs']['east'], 'EastSign')]
d = {"id": "MAP_ROUTE4_EAST", "name": M, "layout": "LAYOUT_ROUTE4_EAST", "music": "MUS_ROUTE3", "region_map_section": "MAPSEC_ROUTE_4",
     "requires_flash": False, "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_ROUTE", "allow_cycling": True, "allow_escaping": False,
     "allow_running": True, "show_map_name": True, "floor_number": 0, "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None,
     "object_events": [], "warp_events": warps, "coord_events": [], "bg_events": bg}
os.makedirs('data/maps/' + M, exist_ok=True)
json.dump(d, open('data/maps/%s/map.json' % M, 'w'), indent=2); open('data/maps/%s/map.json' % M, 'a').write('\n')
open('data/maps/%s/scripts.inc' % M, 'w').write('Route4East_MapScripts::\n\t.byte 0\n' + ''.join('\n%s_EventScript_%s::\n\tmsgbox %s_Text_%s, MSGBOX_SIGN\n\tend\n' % (M, n, M, n) for n in ('WestSign', 'EastSign')))
open('data/maps/%s/text.inc' % M, 'w').write('''Route4East_Text_WestSign::
    .string "TOURMALINE TRAIL\\n"
    .string "MT. MOON - TOURMALIA$"

Route4East_Text_EastSign::
    .string "TOURMALINE TRAIL\\n"
    .string "TOURMALIA - MT. MOON$"
''')
# Route 4 : sortie est -> Route 4 Est (ids 0..3)
f = 'data/maps/Route4/map.json'; r = json.load(open(f))
for w, i in zip(r['warp_events'][-4:], range(4)): w['dest_map'] = 'MAP_ROUTE4_EAST'; w['dest_warp_id'] = str(i)
json.dump(r, open(f, 'w'), indent=2); open(f, 'a').write('\n')
# groupe de cartes, inclusions
f = 'data/maps/map_groups.json'; g = json.load(open(f))
if M not in g['gMapGroup_TownsAndRoutes']: g['gMapGroup_TownsAndRoutes'].append(M)
json.dump(g, open(f, 'w'), indent=2); open(f, 'a').write('\n')
f = 'data/event_scripts.s'; e = open(f).read()
if M + '/scripts.inc' not in e:
    e = e.replace('\t.include "data/maps/Route4/scripts.inc"\n', '\t.include "data/maps/Route4/scripts.inc"\n\t.include "data/maps/%s/scripts.inc"\n' % M, 1)
    e = e.replace('\t.include "data/maps/Route4/text.inc"\n', '\t.include "data/maps/Route4/text.inc"\n\t.include "data/maps/%s/text.inc"\n' % M, 1)
    open(f, 'w').write(e)
f = 'src/field_control_avatar.c'; s = open(f).read()
if 'LAYOUT_ROUTE4_EAST' not in s:
    s = s.replace('|| gMapHeader.mapLayoutId == LAYOUT_ROUTE9;', '|| gMapHeader.mapLayoutId == LAYOUT_ROUTE9 || gMapHeader.mapLayoutId == LAYOUT_ROUTE4_EAST;'); open(f, 'w').write(s)
print('evenements route 4 est ecrits')
