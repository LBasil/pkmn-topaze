#!/usr/bin/env python3
"""Un PNJ « MOVE COACH » dans chaque Centre POKéMON (rappel des capacites oubliees), l'infirmiere ne le fait plus. Idempotent."""
import json, os, re, sys, glob
sys.path.insert(0, 'tools/topaze/maps')
from place_npc import choose
p = 'data/scripts/pkmn_center_nurse.inc'; s = open(p).read()
s = s.replace('\tcall EventScript_PkmnCenterNurse_Relearner\n', '')
if 'EventScript_MoveCoach::' not in s:
    s = s.replace('@ Topaze: move relearner built into every POKéMON CENTER (free)', '''@ Topaze: the MOVE COACH (second NPC of every POKéMON CENTER) helps POKéMON remember forgotten moves (free)
EventScript_MoveCoach::
	lock
	faceplayer
	msgbox Text_MoveCoachHello
	call EventScript_PkmnCenterNurse_Relearner
	msgbox Text_MoveCoachBye
	release
	end

Text_MoveCoachHello::
	.string "MOVE COACH: I teach POKéMON to\\n"
	.string "remember what they have forgotten.$"

Text_MoveCoachBye::
	.string "MOVE COACH: Come back any time.$"

@ Topaze: move relearner (free)''')
    s = s.replace('.string "Would you also like me to help a\\n"\n\t.string "POKéMON remember a forgotten move?$"', '.string "Shall I help a POKéMON remember\\n"\n\t.string "a forgotten move?$"')
open(p, 'w').write(s)
n = 0
for d in sorted(glob.glob('data/maps/*PokemonCenter_1F')):
    m = os.path.basename(d)
    if not os.path.exists(d + '/map.json'): continue
    j = json.load(open(d + '/map.json'))
    if not any('Nurse' in (o.get('script') or '') for o in j['object_events']): continue
    if any(o.get('script') == 'EventScript_MoveCoach' for o in j['object_events']): continue
    anchor, c = choose(m)
    if not c: print('PAS DE PLACE', m); continue
    el = j['object_events'][0]['elevation']
    j['object_events'].append({'graphics_id': 'OBJ_EVENT_GFX_SCIENTIST', 'x': c[0], 'y': c[1], 'elevation': el, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1,
        'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0', 'script': 'EventScript_MoveCoach', 'flag': '0'})
    json.dump(j, open(d + '/map.json', 'w'), indent=2); open(d + '/map.json', 'a').write('\n'); n += 1
print('ajoutes', n)
