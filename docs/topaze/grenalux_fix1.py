# Grenalux fix 1 (phone test): opening scene moved to the outdoor RANCH, 2 grunts, seams, Route 1 connection.
# NOT re-runnable (git checkout data include docs before a rerun).
import re, json, struct, collections
R = '/home/claude/pkmn-topaze/'
def rd(p): return open(R+p).read()
def wr(p, s): open(R+p, 'w').write(s)

# ---------- 0. texts (validate first)
newtexts = {
 'PalletTown_Text_RanchRivalChallenge': "{RIVAL}: {PLAYER}, you take the big one.\\nThe other one is mine!",
 'PalletTown_Text_RanchGrunt2Taunt': "A kid with a borrowed POKéMON?\\nThis will take two seconds!",
 'PalletTown_Text_RanchRivalWin': "{RIVAL}: Mine ran off after one hit!\\p...Yours too? Not bad, {PLAYER}.\\nBut next time I win first!",
}
for k, v in newtexts.items():
    for line in re.split(r'\\[nlp]', v):
        assert len(re.sub(r'\{[^}]*\}', '', line)) <= 36, (k, line)

# ---------- 1. flags / local ids
s = rd('include/constants/flags.h')
assert '#define FLAG_0x4CB               0x4CB\n' in s
s = s.replace('#define FLAG_0x4CB               0x4CB\n', '#define FLAG_HIDE_RANCH_GRUNT2           0x4CB // Topaze: second ONYBRIS grunt (fights the rival) in the ranch opening scene\n')
s = s.replace('// Topaze: father/OAK/rival inside the ranch during the opening', '// Topaze: father/OAK/rival at the ranch during the opening')
wr('include/constants/flags.h', s)

s = rd('include/constants/map_event_ids.h')
m = re.search(r'#define LOCALID_RANCH_FATHER 3\n#define LOCALID_RANCH_OAK 4\n#define LOCALID_RANCH_RIVAL 5\n#define LOCALID_RANCH_GRUNT 6\n#define LOCALID_RANCH_MOM 7\n', s)
assert m
s = s.replace(m.group(0), '')
s = s.replace('#define LOCALID_PALLET_RANCH_JIGGLYPUFF 11\n', '#define LOCALID_PALLET_RANCH_JIGGLYPUFF 11\n#define LOCALID_RANCH_FATHER 12\n#define LOCALID_RANCH_OAK 13\n#define LOCALID_RANCH_RIVAL 14\n#define LOCALID_RANCH_GRUNT 15\n#define LOCALID_RANCH_GRUNT2 16\n#define LOCALID_RANCH_MOM 17\n')
wr('include/constants/map_event_ids.h', s)

# ---------- 2. Ranch map.json: scene objects
def obj(lid, gfx, x, y, mv, flag):
    return {"local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": mv,
            "movement_range_x": 1, "movement_range_y": 1, "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0", "script": "0x0", "flag": flag}
j = json.load(open(R+'data/maps/PalletTown_Ranch/map.json'))
j['object_events'] += [
  obj('LOCALID_RANCH_FATHER', 'OBJ_EVENT_GFX_FAT_MAN', 13, 6, 'MOVEMENT_TYPE_FACE_LEFT', 'FLAG_HIDE_RANCH_SCENE'),
  obj('LOCALID_RANCH_OAK', 'OBJ_EVENT_GFX_PROF_OAK', 10, 7, 'MOVEMENT_TYPE_FACE_UP', 'FLAG_HIDE_RANCH_SCENE'),
  obj('LOCALID_RANCH_RIVAL', 'OBJ_EVENT_GFX_BLUE', 11, 7, 'MOVEMENT_TYPE_FACE_UP', 'FLAG_HIDE_RANCH_SCENE'),
  obj('LOCALID_RANCH_GRUNT', 'OBJ_EVENT_GFX_ROCKET_M', 19, 6, 'MOVEMENT_TYPE_FACE_LEFT', 'FLAG_HIDE_RANCH_GRUNT'),
  obj('LOCALID_RANCH_GRUNT2', 'OBJ_EVENT_GFX_ROCKET_M', 19, 7, 'MOVEMENT_TYPE_FACE_LEFT', 'FLAG_HIDE_RANCH_GRUNT2'),
  obj('LOCALID_RANCH_MOM', 'OBJ_EVENT_GFX_MOM', 1, 6, 'MOVEMENT_TYPE_FACE_RIGHT', 'FLAG_HIDE_RANCH_MOM'),
]
json.dump(j, open(R+'data/maps/PalletTown_Ranch/map.json', 'w'), indent=2); open(R+'data/maps/PalletTown_Ranch/map.json', 'a').write('\n')

# ---------- 3. Rival's house: remove the old scene
j = json.load(open(R+'data/maps/PalletTown_RivalsHouse/map.json'))
j['object_events'] = [o for o in j['object_events'] if o['local_id'] not in ('LOCALID_RANCH_FATHER', 'LOCALID_RANCH_OAK', 'LOCALID_RANCH_RIVAL', 'LOCALID_RANCH_GRUNT', 'LOCALID_RANCH_MOM')]
json.dump(j, open(R+'data/maps/PalletTown_RivalsHouse/map.json', 'w'), indent=2); open(R+'data/maps/PalletTown_RivalsHouse/map.json', 'a').write('\n')

rh = rd('data/maps/PalletTown_RivalsHouse/scripts.inc')
a = rh.index('@ Topaze: opening scene at the RANCH')
b = rh.index('PalletTown_RivalsHouse_OnTransition::')
scene = rh[a:b]
rh = rh[:a] + rh[b:]
rh = rh.replace('\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, PalletTown_RivalsHouse_OnFrame\n', '')
rh = re.sub(r'PalletTown_RivalsHouse_OnFrame::\n\tmap_script_2 .*\n\t\.2byte 0\n\n', '', rh)
rh = rh.replace('\tcall_if_eq VAR_GRENALUX_OPENING, 1, PalletTown_RivalsHouse_EventScript_ShowOpeningNpcs\n\tcall_if_ne VAR_GRENALUX_OPENING, 1, PalletTown_RivalsHouse_EventScript_HideOpeningNpcs\n', '')
a = rh.index('PalletTown_RivalsHouse_EventScript_ShowOpeningNpcs::')
rh = rh[:a].rstrip('\n') + '\n'
wr('data/maps/PalletTown_RivalsHouse/scripts.inc', rh)

# ---------- 4. Ranch scripts: scene (starter block re-used)
a = scene.index('PalletTown_RivalsHouse_EventScript_ChooseStarter::')
b = scene.index('PalletTown_RivalsHouse_EventScript_AfterStarter::')
starter = scene[a:b].replace('PalletTown_RivalsHouse_', 'PalletTown_Ranch_')
starter = starter.replace('goto PalletTown_Ranch_EventScript_AfterStarter\n\tend\n', 'goto PalletTown_Ranch_EventScript_AfterStarter\n\tend\n')
new_scene = '''
@ Topaze: opening scene at the outdoor RANCH. Calm talk -> ONYBRIS raid (2 grunts) -> urgent starter choice -> battles -> MOM and the pendant
PalletTown_Ranch_OnFrame::
	map_script_2 VAR_GRENALUX_OPENING, 0, PalletTown_Ranch_EventScript_OpeningScene
	map_script_2 VAR_GRENALUX_OPENING, 1, PalletTown_Ranch_EventScript_OpeningScene
	.2byte 0

PalletTown_Ranch_EventScript_OpeningScene::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	getplayerxy VAR_0x8004, VAR_0x8005
	call_if_eq VAR_0x8005, 6, PalletTown_Ranch_EventScript_WalkInRow6
	call_if_ne VAR_0x8005, 6, PalletTown_Ranch_EventScript_WalkInRow7
	applymovement LOCALID_RANCH_RIVAL, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox PalletTown_Text_RanchDadHello
	applymovement LOCALID_RANCH_OAK, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox PalletTown_Text_RanchOakIntro
	closemessage
	playse SE_PIN
	delay 40
	msgbox PalletTown_Text_RanchTrackersHowl
	closemessage
	clearflag FLAG_HIDE_RANCH_GRUNT
	clearflag FLAG_HIDE_RANCH_GRUNT2
	addobject LOCALID_RANCH_GRUNT
	addobject LOCALID_RANCH_GRUNT2
	playse SE_EXIT
	applymovement LOCALID_RANCH_GRUNT, PalletTown_Ranch_Movement_GruntsArrive
	applymovement LOCALID_RANCH_GRUNT2, PalletTown_Ranch_Movement_GruntsArrive
	waitmovement 0
	msgbox PalletTown_Text_RanchGruntEnter
	closemessage
	msgbox PalletTown_Text_RanchDadFlees
	closemessage
	applymovement LOCALID_RANCH_FATHER, PalletTown_Ranch_Movement_FatherRunsOut
	waitmovement 0
	removeobject LOCALID_RANCH_FATHER
	applymovement LOCALID_RANCH_GRUNT, PalletTown_Ranch_Movement_GruntsStep
	applymovement LOCALID_RANCH_GRUNT2, PalletTown_Ranch_Movement_GruntsStep
	waitmovement 0
	applymovement LOCALID_RANCH_OAK, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox PalletTown_Text_RanchOakPanic
	closemessage
''' + starter + '''PalletTown_Ranch_EventScript_AfterStarter::
	closemessage
	msgbox PalletTown_Text_RanchRivalTakes
	closemessage
	applymovement LOCALID_RANCH_RIVAL, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox PalletTown_Text_RanchRivalChallenge
	closemessage
	msgbox PalletTown_Text_RanchGrunt2Taunt
	closemessage
	msgbox PalletTown_Text_RanchGruntChallenge
	closemessage
	trainerbattle_earlyrival TRAINER_TEAM_ROCKET_GRUNT_22, RIVAL_BATTLE_TUTORIAL, PalletTown_Text_OnybrisGruntDefeat, PalletTown_Text_OnybrisGruntVictory
	special HealPlayerParty
	msgbox PalletTown_Text_RanchRivalWin
	closemessage
	msgbox PalletTown_Text_RanchGruntRetreat
	closemessage
	applymovement LOCALID_RANCH_GRUNT, PalletTown_Ranch_Movement_GruntsLeave
	applymovement LOCALID_RANCH_GRUNT2, PalletTown_Ranch_Movement_GruntsLeave
	waitmovement 0
	removeobject LOCALID_RANCH_GRUNT
	removeobject LOCALID_RANCH_GRUNT2
	setflag FLAG_HIDE_RANCH_GRUNT
	setflag FLAG_HIDE_RANCH_GRUNT2
	msgbox PalletTown_Text_RanchOakAfter
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_RANCH_OAK
	removeobject LOCALID_RANCH_RIVAL
	setflag FLAG_HIDE_RANCH_SCENE
	delay 30
	clearflag FLAG_HIDE_RANCH_MOM
	addobject LOCALID_RANCH_MOM
	fadescreen FADE_FROM_BLACK
	applymovement LOCALID_RANCH_MOM, PalletTown_Ranch_Movement_MomRunsIn
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox PalletTown_Text_RanchMom1
	closemessage
	giveitem_msg PalletTown_Text_ReceivedPendant, ITEM_RUBY, 1, MUS_OBTAIN_KEY_ITEM
	msgbox PalletTown_Text_RanchMom2
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_RANCH_MOM
	setflag FLAG_HIDE_RANCH_MOM
	@ the raid hits the whole town: ranch, school and lab
	setflag FLAG_GRENALUX_ONYBRIS_STRIKE
	setflag FLAG_HIDE_BULBASAUR_BALL
	setflag FLAG_HIDE_SQUIRTLE_BALL
	setflag FLAG_HIDE_CHARMANDER_BALL
	setflag FLAG_HIDE_RIVAL_IN_LAB
	setvar VAR_GRENALUX_OPENING, 2
	fadescreen FADE_FROM_BLACK
	releaseall
	end

PalletTown_Ranch_EventScript_WalkInRow6::
	applymovement LOCALID_PLAYER, PalletTown_Ranch_Movement_PlayerWalkInRow6
	waitmovement 0
	return

PalletTown_Ranch_EventScript_WalkInRow7::
	applymovement LOCALID_PLAYER, PalletTown_Ranch_Movement_PlayerWalkInRow7
	waitmovement 0
	return

PalletTown_Ranch_Movement_PlayerWalkInRow6::
''' + '\twalk_right\n'*11 + '''	walk_in_place_faster_right
	step_end

PalletTown_Ranch_Movement_PlayerWalkInRow7::
	walk_up
''' + '\twalk_right\n'*11 + '''	walk_in_place_faster_right
	step_end

PalletTown_Ranch_Movement_GruntsArrive::
''' + '\twalk_left\n'*5 + '''	step_end

PalletTown_Ranch_Movement_GruntsStep::
	walk_left
	walk_left
	step_end

PalletTown_Ranch_Movement_FatherRunsOut::
	walk_down
	walk_down
	walk_down
	step_end

PalletTown_Ranch_Movement_GruntsLeave::
''' + '\twalk_right\n'*8 + '''	step_end

PalletTown_Ranch_Movement_MomRunsIn::
''' + '\twalk_right\n'*9 + '''	walk_in_place_faster_right
	step_end

'''
rs = rd('data/maps/PalletTown_Ranch/scripts.inc')
rs = rs.replace('\tmap_script MAP_SCRIPT_ON_LOAD, PalletTown_Ranch_OnLoad\n', '\tmap_script MAP_SCRIPT_ON_LOAD, PalletTown_Ranch_OnLoad\n\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, PalletTown_Ranch_OnFrame\n')
rs = rs.replace('PalletTown_Ranch_OnTransition::\n\tsetflag FLAG_HIDE_RANCH_ANIMALS\n',
 'PalletTown_Ranch_OnTransition::\n\tcall_if_le VAR_GRENALUX_OPENING, 1, PalletTown_Ranch_EventScript_ShowOpeningNpcs\n\tcall_if_gt VAR_GRENALUX_OPENING, 1, PalletTown_Ranch_EventScript_HideOpeningNpcs\n\tsetflag FLAG_HIDE_RANCH_ANIMALS\n')
rs = rs.rstrip('\n') + '\n' + new_scene + '''PalletTown_Ranch_EventScript_ShowOpeningNpcs::
	clearflag FLAG_HIDE_RANCH_SCENE
	setflag FLAG_HIDE_RANCH_GRUNT
	setflag FLAG_HIDE_RANCH_GRUNT2
	setflag FLAG_HIDE_RANCH_MOM
	return

PalletTown_Ranch_EventScript_HideOpeningNpcs::
	setflag FLAG_HIDE_RANCH_SCENE
	setflag FLAG_HIDE_RANCH_GRUNT
	setflag FLAG_HIDE_RANCH_GRUNT2
	setflag FLAG_HIDE_RANCH_MOM
	return
'''
wr('data/maps/PalletTown_Ranch/scripts.inc', rs)

# ---------- 5. texts
t = rd('data/maps/PalletTown/text.inc')
t = t.replace('''PalletTown_Text_RanchGruntChallenge::
    .string "Hah! A kid with a brand new partner?\\p"''', '''PalletTown_Text_RanchGruntChallenge::
    .string "GRUNT: Hah! A kid with a brand new\\n"
    .string "partner?\\p"''')
add = ''
for k, v in newtexts.items():
    add += '\n%s::\n' % k + ''.join('    .string "%s%s"\n' % (l, '$' if i == len(v.split('\\n'))-1 else '\\n') for i, l in enumerate(v.split('\\n')))
add = add.replace('\\n"\n    .string', '\\n"\n    .string')
t = t.replace('\nPalletTown_Text_RanchGruntRetreat::', add + '\nPalletTown_Text_RanchGruntRetreat::')
wr('data/maps/PalletTown/text.inc', t)
print('step1-5 ok')
