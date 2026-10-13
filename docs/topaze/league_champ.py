#!/usr/bin/env python3
"""Salle du Champion : Chen (OAK) en champion en titre, puis le boss s'incruste.
Réécrit scripts/text de PokemonLeague_ChampionsRoom, branche les warps."""
import json, re
P = 'PokemonLeague_ChampionsRoom'
f = f'data/maps/{P}/scripts.inc'; s = open(f).read()
mov_a = s.index(f'{P}_Movement_PlayerEnter::')
movements = s[mov_a:]
# Oak entry/exit movements no longer used by the script: keep PlayerEnter/PlayerExit, add boss + chen ones
keep = []
for name in ('PlayerEnter', 'PlayerExit'):
    a = movements.index(f'{P}_Movement_{name}::')
    b = movements.index('\n\n', a)
    keep.append(movements[a:b + 1])
head = f'''{P}_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, {P}_OnWarp
	map_script MAP_SCRIPT_ON_RESUME, {P}_OnResume
	map_script MAP_SCRIPT_ON_FRAME_TABLE, {P}_OnFrame
	.byte 0

{P}_OnResume::
	setvar VAR_0x8004, 4
	call PokemonLeague_EventScript_DoLightingEffect
	end

{P}_OnWarp::
	map_script_2 VAR_TEMP_1, 0, {P}_EventScript_TurnPlayerNorth
	.2byte 0

{P}_EventScript_TurnPlayerNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

{P}_OnFrame::
	map_script_2 VAR_TEMP_1, 0, {P}_EventScript_EnterRoom
	.2byte 0

@ Topaze: OAK is the reigning CHAMPION. After him the boss crashes in to claim
@ JIRACHI's wish. Both fights can be resumed after a blackout.
{P}_EventScript_EnterRoom::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	setflag FLAG_TEMP_2
	applymovement LOCALID_PLAYER, {P}_Movement_PlayerEnter
	waitmovement 0
	delay 20
	goto_if_defeated TRAINER_LEAGUE_BOSS, {P}_EventScript_AfterBoss
	goto_if_defeated TRAINER_LEAGUE_CHEN, {P}_EventScript_BossPart
	msgbox {P}_Text_OakIntro
	setflag FLAG_TEMP_3
	setflag FLAG_TEMP_5
	savebgm MUS_VICTORY_GYM_LEADER
	trainerbattle_no_intro TRAINER_LEAGUE_CHEN, {P}_Text_OakDefeat
	setflag FLAG_TEMP_4
	clearflag FLAG_TEMP_5
	setflag FLAG_DEFEATED_CHAMP
	msgbox {P}_Text_OakPostBattle
	closemessage
{P}_EventScript_BossPart::
	playbgm MUS_ENCOUNTER_ROCKET, 0
	addobject LOCALID_CHAMPIONS_ROOM_PROF_OAK
	applymovement LOCALID_CHAMPIONS_ROOM_PROF_OAK, {P}_Movement_BossEnter
	applymovement LOCALID_CHAMPIONS_ROOM_RIVAL, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox {P}_Text_BossIntro
	closemessage
	trainerbattle_no_intro TRAINER_LEAGUE_BOSS, {P}_Text_BossDefeat
	msgbox {P}_Text_BossPost
	closemessage
	applymovement LOCALID_CHAMPIONS_ROOM_PROF_OAK, {P}_Movement_BossExit
	waitmovement 0
	removeobject LOCALID_CHAMPIONS_ROOM_PROF_OAK
{P}_EventScript_AfterBoss::
	playbgm MUS_SLOW_PALLET, 0
	msgbox {P}_Text_OakCongratulations
	closemessage
	delay 13
	applymovement LOCALID_CHAMPIONS_ROOM_RIVAL, {P}_Movement_OakExit
	waitmovement 0
	removeobject LOCALID_CHAMPIONS_ROOM_RIVAL
	applymovement LOCALID_PLAYER, {P}_Movement_PlayerExit
	waitmovement 0
	setvar VAR_TEMP_1, 1
	warp MAP_POKEMON_LEAGUE_HALL_OF_FAME, 5, 12
	waitstate
	releaseall
	end

'''
extra = f'''
{P}_Movement_OakExit::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

{P}_Movement_BossEnter::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

{P}_Movement_BossExit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	delay_8
	set_invisible
	step_end
'''
open(f, 'w').write(head + '\n\n'.join(keep) + '\n' + extra)

# --- text
f = f'data/maps/{P}/text.inc'
t = f'''{P}_Text_OakIntro::
    .string "OAK: {{PLAYER}}! You made it.\\p"
    .string "The tournament is only a test.\\n"
    .string "Now you face the reigning\\l"
    .string "CHAMPION.\\p"
    .string "I have studied POKéMON all my life.\\n"
    .string "Show me what you have learned!$"

{P}_Text_OakDefeat::
    .string "OAK: Hm! Marvelous!$"

{P}_Text_OakPostBattle::
    .string "OAK: Your POKéMON trust you and\\n"
    .string "you trust them.\\p"
    .string "That is the whole secret.\\n"
    .string "You are the new CHAMPION!$"

{P}_Text_BossIntro::
    .string "???: So this is the new CHAMPION.\\p"
    .string "How touching. Do you know what\\n"
    .string "waits in the HALL OF FAME?\\p"
    .string "JIRACHI. A wish for the one who\\n"
    .string "stands at the top.\\p"
    .string "I did not come to be a CHAMPION.\\n"
    .string "I came for that wish.\\p"
    .string "Step aside, child. Or be\\n"
    .string "crushed!$"

{P}_Text_BossDefeat::
    .string "Impossible...\\n"
    .string "You... and that pendant...$"

{P}_Text_BossPost::
    .string "???: This is not over.\\p"
    .string "The wish will be mine, one day.\\n"
    .string "Remember that.$"

{P}_Text_OakCongratulations::
    .string "OAK: {{PLAYER}}, you were\\n"
    .string "magnificent.\\p"
    .string "You are the CHAMPION, and you\\n"
    .string "protected the wish from the\\l"
    .string "wrong hands.\\p"
    .string "Come with me. The HALL OF FAME\\n"
    .string "is waiting for you.$"
'''
open(f, 'w').write(t)

# --- warps
def edit(m, fn):
    p = f'data/maps/{m}/map.json'; d = json.load(open(p)); fn(d); json.dump(d, open(p, 'w'), indent=2); open(p, 'a').write('\n')
def lor(d):
    d['warp_events'][1]['dest_map'] = 'MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM'; d['warp_events'][1]['dest_warp_id'] = '0'
def champ(d):
    d['warp_events'][0]['dest_map'] = 'MAP_POKEMON_LEAGUE_LORELEIS_ROOM'; d['warp_events'][0]['dest_warp_id'] = '1'
    d['object_events'][0]['graphics_id'] = 'OBJ_EVENT_GFX_PROF_OAK'
    d['object_events'][1]['graphics_id'] = 'OBJ_EVENT_GFX_GIOVANNI'
edit('PokemonLeague_LoreleisRoom', lor)
edit('PokemonLeague_ChampionsRoom', champ)
print('champ ok')
