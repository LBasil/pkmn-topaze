PokemonLeague_ChampionsRoom_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, PokemonLeague_ChampionsRoom_OnWarp
	map_script MAP_SCRIPT_ON_RESUME, PokemonLeague_ChampionsRoom_OnResume
	map_script MAP_SCRIPT_ON_FRAME_TABLE, PokemonLeague_ChampionsRoom_OnFrame
	.byte 0

PokemonLeague_ChampionsRoom_OnResume::
	setvar VAR_0x8004, 4
	call PokemonLeague_EventScript_DoLightingEffect
	end

PokemonLeague_ChampionsRoom_OnWarp::
	map_script_2 VAR_TEMP_1, 0, PokemonLeague_ChampionsRoom_EventScript_TurnPlayerNorth
	.2byte 0

PokemonLeague_ChampionsRoom_EventScript_TurnPlayerNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

PokemonLeague_ChampionsRoom_OnFrame::
	map_script_2 VAR_TEMP_1, 0, PokemonLeague_ChampionsRoom_EventScript_EnterRoom
	.2byte 0

@ Topaze: OAK is the reigning CHAMPION. After him the boss crashes in to claim
@ JIRACHI's wish. Both fights can be resumed after a blackout.
PokemonLeague_ChampionsRoom_EventScript_EnterRoom::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	setflag FLAG_TEMP_2
	applymovement LOCALID_PLAYER, PokemonLeague_ChampionsRoom_Movement_PlayerEnter
	waitmovement 0
	delay 20
	goto_if_defeated TRAINER_LEAGUE_BOSS_2, PokemonLeague_ChampionsRoom_EventScript_AfterBoss
	goto_if_defeated TRAINER_LEAGUE_BOSS, PokemonLeague_ChampionsRoom_EventScript_LegendsPart
	goto_if_defeated TRAINER_LEAGUE_CHEN, PokemonLeague_ChampionsRoom_EventScript_BossPart
	msgbox PokemonLeague_ChampionsRoom_Text_OakIntro
	setflag FLAG_TEMP_3
	setflag FLAG_TEMP_5
	savebgm MUS_VICTORY_GYM_LEADER
	trainerbattle_no_intro TRAINER_LEAGUE_CHEN, PokemonLeague_ChampionsRoom_Text_OakDefeat
	setflag FLAG_TEMP_4
	clearflag FLAG_TEMP_5
	setflag FLAG_DEFEATED_CHAMP
	msgbox PokemonLeague_ChampionsRoom_Text_OakPostBattle
	closemessage
PokemonLeague_ChampionsRoom_EventScript_BossPart::
	playbgm MUS_ENCOUNTER_ROCKET, 0
	addobject LOCALID_CHAMPIONS_ROOM_PROF_OAK
	applymovement LOCALID_CHAMPIONS_ROOM_PROF_OAK, PokemonLeague_ChampionsRoom_Movement_BossEnter
	applymovement LOCALID_CHAMPIONS_ROOM_RIVAL, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox PokemonLeague_ChampionsRoom_Text_BossIntro
	closemessage
	trainerbattle_no_intro TRAINER_LEAGUE_BOSS, PokemonLeague_ChampionsRoom_Text_BossDefeat
PokemonLeague_ChampionsRoom_EventScript_LegendsFight::
	msgbox PokemonLeague_ChampionsRoom_Text_BossLegends
	closemessage
	special ShakeScreen
	delay 30
	trainerbattle_no_intro TRAINER_LEAGUE_BOSS_2, PokemonLeague_ChampionsRoom_Text_BossDefeat2
	msgbox PokemonLeague_ChampionsRoom_Text_BossPost
	closemessage
	applymovement LOCALID_CHAMPIONS_ROOM_PROF_OAK, PokemonLeague_ChampionsRoom_Movement_BossExit
	waitmovement 0
	removeobject LOCALID_CHAMPIONS_ROOM_PROF_OAK
PokemonLeague_ChampionsRoom_EventScript_AfterBoss::
	playbgm MUS_SLOW_PALLET, 0
	msgbox PokemonLeague_ChampionsRoom_Text_OakCongratulations
	closemessage
	delay 13
	applymovement LOCALID_CHAMPIONS_ROOM_RIVAL, PokemonLeague_ChampionsRoom_Movement_OakExit
	waitmovement 0
	removeobject LOCALID_CHAMPIONS_ROOM_RIVAL
	applymovement LOCALID_PLAYER, PokemonLeague_ChampionsRoom_Movement_PlayerExit
	waitmovement 0
	setvar VAR_TEMP_1, 1
	warp MAP_POKEMON_LEAGUE_HALL_OF_FAME, 5, 12
	waitstate
	releaseall
	end

PokemonLeague_ChampionsRoom_EventScript_LegendsPart::
	playbgm MUS_ENCOUNTER_ROCKET, 0
	addobject LOCALID_CHAMPIONS_ROOM_PROF_OAK
	applymovement LOCALID_CHAMPIONS_ROOM_PROF_OAK, PokemonLeague_ChampionsRoom_Movement_BossEnter
	waitmovement 0
	goto PokemonLeague_ChampionsRoom_EventScript_LegendsFight
	end

PokemonLeague_ChampionsRoom_Movement_PlayerEnter::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end


PokemonLeague_ChampionsRoom_Movement_PlayerExit::
	delay_16
	walk_left
	walk_up
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	delay_8
	set_invisible
	step_end


PokemonLeague_ChampionsRoom_Movement_OakExit::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

PokemonLeague_ChampionsRoom_Movement_BossEnter::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

PokemonLeague_ChampionsRoom_Movement_BossExit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	delay_8
	set_invisible
	step_end
