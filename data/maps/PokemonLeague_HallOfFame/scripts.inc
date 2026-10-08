PokemonLeague_HallOfFame_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, PokemonLeague_HallOfFame_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, PokemonLeague_HallOfFame_OnWarp
	.byte 0

PokemonLeague_HallOfFame_OnWarp::
	map_script_2 VAR_TEMP_1, 0, PokemonLeague_HallOfFame_EventScript_TurnPlayerNorth
	.2byte 0

PokemonLeague_HallOfFame_EventScript_TurnPlayerNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

PokemonLeague_HallOfFame_OnFrame::
	map_script_2 VAR_TEMP_1, 0, PokemonLeague_HallOfFame_EventScript_EnterRoom
	.2byte 0

PokemonLeague_HallOfFame_EventScript_EnterRoom::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	applymovement LOCALID_PLAYER, PokemonLeague_HallOfFame_Movement_EnterRoom
	waitmovement 0
	applymovement LOCALID_HALL_OF_FAME_PROF_OAK, Common_Movement_WalkInPlaceFasterLeft
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	delay 18
	msgbox PokemonLeague_HallOfFame_Text_OakCongratulations
	closemessage
	call PokemonLeague_HallOfFame_EventScript_JirachiWish
	applymovement LOCALID_HALL_OF_FAME_PROF_OAK, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 20
	dofieldeffect FLDEFF_HALL_OF_FAME_RECORD
	waitfieldeffect FLDEFF_HALL_OF_FAME_RECORD
	delay 40
	setvar VAR_TEMP_1, 1
	call EventScript_SetDefeatedEliteFourFlagsVars
	setrespawn HEAL_LOCATION_PALLET_TOWN
	fadescreenspeed FADE_TO_BLACK, 24
	special EnterHallOfFame
	waitstate
	releaseall
	end

PokemonLeague_HallOfFame_Movement_EnterRoom::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

@ Topaze: the three endings. The wish of JIRACHI is made by the player.
PokemonLeague_HallOfFame_EventScript_JirachiWish::
	msgbox PokemonLeague_HallOfFame_Text_JirachiAppears
	closemessage
	special ShakeScreen
	delay 30
	msgbox PokemonLeague_HallOfFame_Text_JirachiAsks
	multichoice 17, 3, MULTICHOICE_TOPAZE_WISH, FALSE
	switch VAR_RESULT
	case 0, PokemonLeague_HallOfFame_EventScript_WishLetGo
	case 1, PokemonLeague_HallOfFame_EventScript_WishNoBalls
	case 2, PokemonLeague_HallOfFame_EventScript_WishRuleAll
	goto PokemonLeague_HallOfFame_EventScript_WishLetGo
	end

PokemonLeague_HallOfFame_EventScript_WishLetGo::
	setvar VAR_TOPAZE_ENDING, 1
	setflag FLAG_TOPAZE_POSTGAME
	clearflag FLAG_HIDE_POSTGAME_STRANGER
	msgbox PokemonLeague_HallOfFame_Text_EndingLetGo
	closemessage
	return

PokemonLeague_HallOfFame_EventScript_WishNoBalls::
	setvar VAR_TOPAZE_ENDING, 2
	msgbox PokemonLeague_HallOfFame_Text_EndingNoBalls
	closemessage
	return

PokemonLeague_HallOfFame_EventScript_WishRuleAll::
	setvar VAR_TOPAZE_ENDING, 3
	msgbox PokemonLeague_HallOfFame_Text_EndingRuleAll
	closemessage
	return
