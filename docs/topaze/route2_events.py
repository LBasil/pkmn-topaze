# ROUTE 2 (route du crepuscule) : evenements. A lancer apres route2_gradient.py. Idempotent.
# Warps : 0 portail nord -> foret (cote nord), 1 portail sud -> foret (cote sud), 2,3 sud -> Opanihrum, 4,5 nord -> Pyropia.
import json, re
info = json.load(open('/tmp/route2_info.json')); H = info['h']
def warp(x, y, dest, wid): return {"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
def rw(f, fn):
    d = json.load(open(f)); fn(d); json.dump(d, open(f, 'w'), indent=2); open(f, 'a').write('\n')
dn, ds = info['doorN'], info['doorS']
def route(d):
    d['warp_events'] = [warp(dn[0], dn[1], 'MAP_ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE', 3), warp(ds[0], ds[1], 'MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE', 1),
                        warp(12, H - 1, 'MAP_VIRIDIAN_CITY', 6), warp(13, H - 1, 'MAP_VIRIDIAN_CITY', 7),
                        warp(12, 0, 'MAP_PEWTER_CITY', 7), warp(13, 0, 'MAP_PEWTER_CITY', 8)]
    npc = info['npc']
    def obj(gfx, c, script, mv='MOVEMENT_TYPE_FACE_DOWN', rx=0, ry=0, flag='0'):
        return {"type": "object", "graphics_id": gfx, "x": c[0], "y": c[1], "elevation": 3, "movement_type": mv, "movement_range_x": rx, "movement_range_y": ry,
                "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": flag}
    d['object_events'] = [obj('OBJ_EVENT_GFX_ITEM_BALL', npc['ether'], 'Route2_EventScript_ItemEther', flag='FLAG_HIDE_ROUTE2_ETHER', rx=1, ry=1),
                          obj('OBJ_EVENT_GFX_ITEM_BALL', npc['heal'], 'Route2_EventScript_ItemParalyzeHeal', flag='FLAG_HIDE_ROUTE2_PARALYZE_HEAL', rx=1, ry=1),
                          obj('OBJ_EVENT_GFX_HIKER', npc['hiker'], 'Route2_EventScript_Hiker', 'MOVEMENT_TYPE_FACE_LEFT'),
                          obj('OBJ_EVENT_GFX_WORKER_M', npc['miner'], 'Route2_EventScript_Miner', 'MOVEMENT_TYPE_LOOK_AROUND')]
    sg = lambda c, s: {"type": "sign", "x": c[0], "y": c[1], "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": s}
    d['bg_events'] = [sg(info['signS'], 'Route2_EventScript_RouteSign'), sg(info['signN'], 'Route2_EventScript_ForestSign')]
    d['coord_events'] = []
rw('data/maps/Route2/map.json', route)
# portails : les interieurs de la foret ramenent a la bonne case
def south(d):
    for w in d['warp_events']:
        if w['dest_map'] == 'MAP_ROUTE2': w['dest_warp_id'] = '1'
rw('data/maps/Route2_ViridianForest_SouthEntrance/map.json', south)
def city(name, a, b, ia, ib, dest):
    def f(d):
        ws = [w for w in d['warp_events'] if w['dest_map'] == 'MAP_ROUTE2']
        assert len(ws) == 2, name
        ws[0]['dest_warp_id'] = str(ia); ws[1]['dest_warp_id'] = str(ib)
    rw('data/maps/%s/map.json' % name, f)
city('ViridianCity', 6, 7, 2, 3, 'MAP_VIRIDIAN_CITY'); city('PewterCity', 7, 8, 4, 5, 'MAP_PEWTER_CITY')
# scripts / textes
f = 'data/maps/Route2/scripts.inc'; s = open(f).read()
s = re.sub(r'Route2_EventScript_DiglettsCaveSign::\n\tmsgbox Route2_Text_DiglettsCave, MSGBOX_SIGN\n\tend\n', '', s)
for lbl in ('ForestSign', 'Hiker', 'Miner'):
    s = re.sub(r'\nRoute2_EventScript_%s::\n.*?\tend\n' % lbl, '\n', s, flags=re.S)
s = s.rstrip('\n') + '''

Route2_EventScript_ForestSign::
	msgbox Route2_Text_ForestSign, MSGBOX_SIGN
	end

Route2_EventScript_Hiker::
	msgbox Route2_Text_Hiker, MSGBOX_NPC
	end

Route2_EventScript_Miner::
	msgbox Route2_Text_Miner, MSGBOX_NPC
	end
'''
open(f, 'w').write(s)
f = 'data/maps/Route2/text.inc'
open(f, 'w').write('''Route2_Text_RouteSign::
    .string "ROUTE 2\\n"
    .string "OPANIHRUM - PYROPIA$"

Route2_Text_ForestSign::
    .string "CINDER FOREST\\n"
    .string "Nothing grows there anymore...$"

Route2_Text_Hiker::
    .string "See how the dusk follows the road?\\n"
    .string "Slate blue behind you, embers ahead.\\p"
    .string "The burnt wood under this cliff is the\\n"
    .string "only way through. Mind the bugs!$"

Route2_Text_Miner::
    .string "Obsidian forms where the mountain\\n"
    .string "bleeds. PYROPIA sits right on it.\\p"
    .string "Smell that smoke? The volcano is\\n"
    .string "just warming up.$"
''')
print('evenements Route 2 ecrits')
