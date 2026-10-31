# v28 : le dome de verre de Tourmalia est une vraie salle visitable (CeruleanCity_GlassHall), clone de Route12_NorthEntrance_1F.
# Portes sud (5,11)/(6,11) <- portes du dome ; (v30 : plus de sortie nord, la colline se prend a pied) ; escalier (8,10) -> grotte (apres Biker 1).
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
      warps=[warp(5, 11, C, 7), warp(6, 11, C, 14), warp(8, 10, 'MAP_CERULEAN_CAVE_1F', 0)],
      coords=[{"type": "trigger", "x": 8, "y": 10, "elevation": 3, "var": "VAR_TEMP_0", "var_value": "0", "script": "CeruleanCity_GlassHall_EventScript_Stairs"}],
      scripts=scripts, txt=txt, region_map_section='MAPSEC_CERULEAN_CITY', music='MUS_FUCHSIA')
# la grotte ressort dans la salle (escalier) et non plus sur la porte du dome
f = 'data/maps/CeruleanCave_1F/map.json'; d = json.load(open(f))
d['warp_events'][0].update(dest_map='MAP_CERULEAN_CITY_GLASS_HALL', dest_warp_id='2'); jdump(d, f)
print('salle de verre ecrite')
