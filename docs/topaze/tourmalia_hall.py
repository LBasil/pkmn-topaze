# v28 : le dome de verre de Tourmalia est une vraie salle visitable (CeruleanCity_GlassHall), clone de Route12_NorthEntrance_1F.
# Portes sud (5,11)/(6,11) <- portes du dome ; (v33 : portes nord (5,1)/(6,1) -> pied de la colline) ; escalier (8,10) -> grotte (apres Biker 1).
# A lancer apres tourmalia_copy.py + tourmalia_river_events.py. Rejouable (clone reecrit tout).
import sys, json; sys.path.insert(0, 'docs/topaze')
from newmap import *
C = 'MAP_CERULEAN_CITY'
scripts = '''
CeruleanCity_GlassHall_EventScript_Guide::
	msgbox CeruleanCity_GlassHall_Text_Guide, MSGBOX_NPC
	end

CeruleanCity_GlassHall_EventScript_Stairs::
	lockall
	goto_if_defeated TRAINER_BIKER_1, CeruleanCity_GlassHall_EventScript_StairsOpen
	releaseall
	end

CeruleanCity_GlassHall_EventScript_StairsOpen::
	warp MAP_CERULEAN_CAVE_1F, 0
	waitstate
	end
'''
txt = text('CeruleanCity_GlassHall_Text_Guide', 'Welcome to the GLASS HALL! The stairs on the right go down to the CERULEAN CAVE.')
clone('CeruleanCity_GlassHall', 'Route12_NorthEntrance_1F',
      objects=[obj('POLICEMAN', 1, 5, 'CeruleanCity_GlassHall_EventScript_Guide', mv='MOVEMENT_TYPE_FACE_RIGHT')],
      warps=[warp(5, 11, C, 7), warp(6, 11, C, 14), warp(8, 10, 'MAP_CERULEAN_CAVE_1F', 0), warp(5, 1, C, 16)],
      coords=[{"type": "trigger", "x": 8, "y": 10, "elevation": 3, "var": "VAR_TEMP_0", "var_value": "0", "script": "CeruleanCity_GlassHall_EventScript_Stairs"}],
      scripts=scripts, txt=txt, region_map_section='MAPSEC_CERULEAN_CITY', music='MUS_FUCHSIA')
# la grotte ressort dans la salle (escalier) et non plus sur la porte du dome
f = 'data/maps/CeruleanCave_1F/map.json'; d = json.load(open(f))
d['warp_events'][0].update(dest_map='MAP_CERULEAN_CITY_GLASS_HALL', dest_warp_id='2'); jdump(d, f)
print('salle de verre ecrite')

# v31 : cabane-portail EST (remplace le raccord direct Tourmalia <-> Route 9). Clone de la salle de passage de la Route 6.
# Portes sud (4,9)/(5,9) -> porte de la cabane (59,27) ; portes nord (4,1)/(5,1) -> case-porte (2,4) de la cabane de l'extremite ouest de la Route 9 (route9_gate_art.py).
gscripts = '''
CeruleanCity_GateEast_EventScript_Guide::
	msgbox CeruleanCity_GateEast_Text_Guide, MSGBOX_NPC
	end
'''
gtxt = text('CeruleanCity_GateEast_Text_Guide', 'TOURMALIA lies behind you. Next stop: ROUTE 9 and the east!')
f9 = 'data/maps/Route9/map.json'; d9 = json.load(open(f9))
d9['connections'] = [c for c in (d9['connections'] or []) if c['map'] != 'MAP_CERULEAN_CITY']
d9['warp_events'] = [w for w in d9['warp_events'] if w['dest_map'] != 'MAP_CERULEAN_CITY_GATE_EAST']
RW = len(d9['warp_events']); d9['warp_events'].append(warp(6, 4, 'MAP_CERULEAN_CITY_GATE_EAST', 2, el=0)); jdump(d9, f9)
clone('CeruleanCity_GateEast', 'Route6_NorthEntrance',
      objects=[obj('POLICEMAN', 7, 5, 'CeruleanCity_GateEast_EventScript_Guide')],
      warps=[warp(4, 9, C, 17), warp(5, 9, C, 17), warp(4, 1, 'MAP_ROUTE9', RW), warp(5, 1, 'MAP_ROUTE9', RW)],
      scripts=gscripts, txt=gtxt, region_map_section='MAPSEC_CERULEAN_CITY', music='MUS_FUCHSIA')
print('cabane-portail est ecrite (warp Route 9 #%d)' % RW)
