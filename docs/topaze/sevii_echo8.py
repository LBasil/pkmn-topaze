#!/usr/bin/env python3
"""Echo 8 (post-game, ile 7) : scene SILVER / GIOVANNI (pere et fils) / RED (grand rival de Giovanni) a Sevault Canyon.
Declenchee en (17,8)/(18,8) au stage 21 ; combats : SILVER (TRAINER_ECHO_SILVER, nouveau, id 764) puis GIOVANNI (TRAINER_PLAYER_LEAF) ; stage 22 -> les legendes apparaissent.
FLAG_HIDE_ECHO_SCENE 0x0DA. Non rejouable."""
import json, re, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
S = 'SevenIsland_SevaultCanyon_Text_Scene'
if 'FLAG_HIDE_ECHO_SCENE' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
s = rd('include/constants/flags.h')
wr('include/constants/flags.h', s.replace('#define FLAG_0x0DA               0x0DA', '#define FLAG_HIDE_ECHO_SCENE     0x0DA // Topaze: Silver/Giovanni/Red scene objects', 1))
s = rd('include/constants/opponents.h')
s = s.replace('#define TRAINER_ELDER_WALLACE                763\n', '#define TRAINER_ELDER_WALLACE                763\n#define TRAINER_ECHO_SILVER                  764\n', 1)
s = re.sub(r'#define NUM_TRAINERS\s+\d+', '#define NUM_TRAINERS                             765', s)
wr('include/constants/opponents.h', s)
tr = rd('src/data/trainers.h')
i = tr.index('    [TRAINER_ELDER_WALLACE] = {'); j = tr.index('    },\n', i) + 7
tr = tr[:j] + '''    [TRAINER_ECHO_SILVER] = {
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .trainerName = _("SILVER"),
        .items = {ITEM_FULL_RESTORE, ITEM_FULL_RESTORE},
        .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_EchoSilver),
    },
''' + tr[j:]
wr('src/data/trainers.h', tr)
pa = rd('src/data/trainer_parties.h')
i = pa.index('static const struct TrainerMonNoItemDefaultMoves sParty_ElderWallace[]'); j = pa.index('\n};\n', i) + 4
party = [('SNEASEL', 68), ('CROBAT', 68), ('GENGAR', 69), ('ALAKAZAM', 69), ('MAGNETON', 70), ('FERALIGATR', 72)]
pa = pa[:j] + '\nstatic const struct TrainerMonNoItemDefaultMoves sParty_EchoSilver[] = {\n' + ''.join(
    f'    {{\n        .iv = 220,\n        .lvl = {lv},\n        .species = SPECIES_{sp},\n    }},\n' for sp, lv in party) + '};\n' + pa[j:]
wr('src/data/trainer_parties.h', pa)
# local ids
h = rd('include/constants/map_event_ids.h')
wr('include/constants/map_event_ids.h', h.rstrip('\n') + '\n#define LOCALID_ECHO_SILVER 28\n#define LOCALID_ECHO_GIOVANNI 29\n#define LOCALID_ECHO_RED 30\n')
P = 'SevenIsland_SevaultCanyon'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
# les legendes n'apparaissent qu'au stage 22
s = s.replace('goto_if_ne VAR_ECHO_STAGE, 21, EventScript_Return', 'goto_if_ne VAR_ECHO_STAGE, 22, EventScript_Return')
s = s.replace(f'{P}_OnTransition::\n', f'{P}_OnTransition::\n\tsetflag FLAG_HIDE_ECHO_SCENE\n', 1)
M = f'{P}_Movement_'
S = f'{P}_Text_Scene'
wr(f, s.rstrip('\n') + f'''

@ Topaze: SILVER / GIOVANNI / RED scene (father, son, great rivals)
{P}_EventScript_EchoScene::
	lockall
	clearflag FLAG_HIDE_ECHO_SCENE
	addobject LOCALID_ECHO_SILVER
	addobject LOCALID_ECHO_GIOVANNI
	addobject LOCALID_ECHO_RED
	applymovement LOCALID_PLAYER, {M}PlayerToScene
	waitmovement 0
	textcolor NPC_TEXT_COLOR_MALE
	applymovement LOCALID_ECHO_SILVER, Common_Movement_FacePlayer
	waitmovement 0
	msgbox {S}Silver1
	applymovement LOCALID_ECHO_SILVER, {M}FaceLeft
	waitmovement 0
	msgbox {S}Giovanni1
	msgbox {S}Silver2
	msgbox {S}Giovanni2
	msgbox {S}Silver3
	applymovement LOCALID_ECHO_SILVER, Common_Movement_FacePlayer
	waitmovement 0
	msgbox {S}Silver4
	trainerbattle_no_intro TRAINER_ECHO_SILVER, {S}SilverDefeat
	msgbox {S}Silver5
	applymovement LOCALID_ECHO_SILVER, {M}SilverStepAside
	applymovement LOCALID_ECHO_GIOVANNI, {M}GiovanniStepUp
	waitmovement 0
	applymovement LOCALID_ECHO_GIOVANNI, Common_Movement_FacePlayer
	waitmovement 0
	msgbox {S}Giovanni3
	trainerbattle_no_intro TRAINER_PLAYER_LEAF, {S}GiovanniDefeat
	msgbox {S}Giovanni4
	applymovement LOCALID_ECHO_RED, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox {S}Giovanni5
	msgbox {S}Red1
	msgbox {S}Giovanni6
	msgbox {S}Silver6
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ECHO_SILVER
	removeobject LOCALID_ECHO_GIOVANNI
	setflag FLAG_HIDE_ECHO_SCENE
	special HealPlayerParty
	fadescreen FADE_FROM_BLACK
	msgbox {S}Red2
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ECHO_RED
	fadescreen FADE_FROM_BLACK
	setvar VAR_ECHO_STAGE, 22
	releaseall
	end

{M}PlayerToScene::
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	step_end

{M}FaceLeft::
	face_left
	step_end

{M}SilverStepAside::
	walk_up
	face_down
	step_end

{M}GiovanniStepUp::
	walk_right
	walk_right
	step_end
''')
f = f'data/maps/{P}/text.inc'; s = rd(f)
def txt(lbl, body):
    toks = re.split(r'(\\n|\\l|\\p)', body); out = f'{S}{lbl}::\n'
    for k in range(0, len(toks), 2):
        line = toks[k]; sep = toks[k + 1] if k + 1 < len(toks) else '$'
        assert len(re.sub(r'\{[^}]*\}', 'X', line)) <= 35, line
        out += '    .string "%s%s"\n' % (line, sep)
    return out + '\n'
T = [
 ('Silver1', 'SILVER: ...You came. All the way\\nto the edge of time.\\pThe ECHO showed me something.\\nA boy in a dark room, waiting\\lfor a man who never came back.'),
 ('Giovanni1', '...I saw it too, SILVER.\\pI left because I was afraid of\\nwhat I would turn you into.'),
 ('Silver2', 'SILVER: Afraid?! You left me alone!\\pI became strong so you would\\nlook at me. Just once.'),
 ('Giovanni2', 'I looked.\\pEvery single day, from far away.\\pI am proud of you, son.\\nI never knew how to say it.'),
 ('Silver3', 'SILVER: ...\\pThen do not say it.\\nShow me. Let me earn it.'),
 ('Silver4', 'SILVER: {PLAYER}. Fight me.\\pIf I cannot face the one who\\nbeat the LEAGUE, I cannot stand\\lbefore my father.'),
 ('SilverDefeat', 'I lost. But for the first time...\\nI do not mind.'),
 ('Silver5', 'SILVER: Thank you. I will walk\\nbeside him now. Not behind.'),
 ('Giovanni3', 'GIOVANNI: CHAMPION. Let me see\\nwhat my son measured himself\\lagainst.'),
 ('GiovanniDefeat', 'Hm. The earth bows to you.'),
 ('Giovanni4', 'GIOVANNI: ...So that is what it\\nlooks like. A trainer worth\\lfollowing.'),
 ('Giovanni5', 'GIOVANNI: And you, RED. Still\\nstanding there in silence.\\pWe never settled it, you and I.'),
 ('Red1', '...'),
 ('Giovanni6', 'GIOVANNI: Not today. Today I walk\\nhome with my son.'),
 ('Silver6', 'SILVER: ...Come on. Father.'),
 ('Red2', 'RED: ...\\p(He tips his cap to you and\\nsmiles for the very first time.)'),
]
wr(f, s.rstrip('\n') + '\n\n' + ''.join(txt(a, b) for a, b in T))
j = json.load(open(f'data/maps/{P}/map.json'))
base = {'elevation': 3, 'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
        'trainer_sight_or_berry_tree_id': '0', 'script': '0x0', 'flag': 'FLAG_HIDE_ECHO_SCENE'}
j['object_events'] += [
 dict(base, local_id='LOCALID_ECHO_SILVER', graphics_id='OBJ_EVENT_GFX_BLUE', x=13, y=5, movement_type='MOVEMENT_TYPE_FACE_RIGHT'),
 dict(base, local_id='LOCALID_ECHO_GIOVANNI', graphics_id='OBJ_EVENT_GFX_GIOVANNI', x=11, y=5, movement_type='MOVEMENT_TYPE_FACE_RIGHT'),
 dict(base, local_id='LOCALID_ECHO_RED', graphics_id='OBJ_EVENT_GFX_RED_NORMAL', x=16, y=4, movement_type='MOVEMENT_TYPE_FACE_DOWN'),
]
for x in (17, 18):
    j['coord_events'].append({'type': 'trigger', 'x': x, 'y': 8, 'elevation': 3, 'var': 'VAR_ECHO_STAGE', 'var_value': '21', 'script': f'{P}_EventScript_EchoScene'})
json.dump(j, open(f'data/maps/{P}/map.json', 'w'), indent=2); open(f'data/maps/{P}/map.json', 'a').write('\n')
print('echo8 ok')
