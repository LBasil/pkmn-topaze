.equ NUM_BOULDERS_PRESENT, VAR_TEMP_2

SeafoamIslands_B4F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SeafoamIslands_B4F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SeafoamIslands_B4F_OnResume
	map_script MAP_SCRIPT_ON_LOAD, SeafoamIslands_B4F_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SeafoamIslands_B4F_OnWarp
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SeafoamIslands_B4F_OnFrame
	.byte 0

SeafoamIslands_B4F_OnResume::
	call_if_set FLAG_SYS_SPECIAL_WILD_BATTLE, SeafoamIslands_B4F_EventScript_TryRemoveArticuno
	end

SeafoamIslands_B4F_EventScript_TryRemoveArticuno::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, EventScript_Return
	removeobject VAR_LAST_TALKED
	return

SeafoamIslands_B4F_OnTransition::
	call SeafoamIslands_B4F_EventScript_CheckOnybris
	call_if_unset FLAG_FOUGHT_ARTICUNO, SeafoamIslands_B4F_EventScript_ShowArticuno
	call_if_unset FLAG_STOPPED_SEAFOAM_B4F_CURRENT, SeafoamIslands_B4F_EventScript_CheckStoppedCurrent
	call_if_set FLAG_STOPPED_SEAFOAM_B4F_CURRENT, SeafoamIslands_B4F_EventScript_SetNoCurrentLayout
	end

SeafoamIslands_B4F_EventScript_CheckStoppedCurrent::
	setvar NUM_BOULDERS_PRESENT, 0
	call_if_unset FLAG_HIDE_SEAFOAM_B4F_BOULDER_1, SeafoamIslands_B4F_EventScript_AddBoulderPresent
	call_if_unset FLAG_HIDE_SEAFOAM_B4F_BOULDER_2, SeafoamIslands_B4F_EventScript_AddBoulderPresent
	call_if_eq NUM_BOULDERS_PRESENT, 2, SeafoamIslands_B4F_EventScript_StoppedCurrent
	return

SeafoamIslands_B4F_EventScript_StoppedCurrent::
	setflag FLAG_STOPPED_SEAFOAM_B4F_CURRENT
	return

SeafoamIslands_B4F_EventScript_SetNoCurrentLayout::
	setmaplayoutindex LAYOUT_SEAFOAM_ISLANDS_B4F_CURRENT_STOPPED
	return

SeafoamIslands_B4F_EventScript_ShowArticuno::
	clearflag FLAG_HIDE_ARTICUNO
	return

SeafoamIslands_B4F_OnLoad::
	setvar NUM_BOULDERS_PRESENT, 0
	call_if_unset FLAG_HIDE_SEAFOAM_B4F_BOULDER_1, SeafoamIslands_B4F_EventScript_AddBoulderPresent
	call_if_unset FLAG_HIDE_SEAFOAM_B4F_BOULDER_2, SeafoamIslands_B4F_EventScript_AddBoulderPresent
	goto_if_eq NUM_BOULDERS_PRESENT, 2, SeafoamIslands_B4F_EventScript_SetCalmWaterNearStairs
	end

SeafoamIslands_B4F_EventScript_SetCalmWaterNearStairs::
	setmetatile 12, 14, METATILE_General_CalmWater, 0
	setmetatile 13, 14, METATILE_General_CalmWater, 0
	end

SeafoamIslands_B4F_OnWarp::
	map_script_2 VAR_MAP_SCENE_SEAFOAM_ISLANDS_B4F, 1, SeafoamIslands_B4F_EventScript_WarpInOnCurrent
	.2byte 0

SeafoamIslands_B4F_EventScript_WarpInOnCurrent::
	turnobject LOCALID_PLAYER, DIR_NORTH
	special ForcePlayerToStartSurfing
	end

SeafoamIslands_B4F_OnFrame::
	map_script_2 VAR_MAP_SCENE_SEAFOAM_ISLANDS_B4F, 1, SeafoamIslands_B4F_EventScript_EnterOnCurrent
	map_script_2 VAR_TEMP_1, 1, SeafoamIslands_B4F_EventScript_EnterByFalling
	map_script_2 VAR_TEMP_3, 1, SeafoamIslands_B4F_EventScript_KronosScene
	.2byte 0

@ The current the player is forced in on from B3F
SeafoamIslands_B4F_EventScript_EnterOnCurrent::
	lockall
	applymovement LOCALID_PLAYER, SeafoamIslands_B4F_Movement_EnterOnCurrent
	waitmovement 0
	setvar VAR_MAP_SCENE_SEAFOAM_ISLANDS_B4F, 0
	releaseall
	end

SeafoamIslands_B4F_Movement_EnterOnCurrent::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

@ The current the player lands on when entering the map by falling
SeafoamIslands_B4F_EventScript_EnterByFalling::
	lockall
	setvar NUM_BOULDERS_PRESENT, 0
	call_if_unset FLAG_HIDE_SEAFOAM_B4F_BOULDER_1, SeafoamIslands_B4F_EventScript_AddBoulderPresent
	call_if_unset FLAG_HIDE_SEAFOAM_B4F_BOULDER_2, SeafoamIslands_B4F_EventScript_AddBoulderPresent
	goto_if_eq NUM_BOULDERS_PRESENT, 2, SeafoamIslands_B4F_EventScript_CurrentBlocked
	getplayerxy VAR_0x8008, VAR_0x8009
	call_if_lt VAR_0x8008, 9, SeafoamIslands_B4F_EventScript_RideCurrentFar
	call_if_ge VAR_0x8008, 9, SeafoamIslands_B4F_EventScript_RideCurrentClose
	special SeafoamIslandsB4F_CurrentDumpsPlayerOnLand
	setvar VAR_TEMP_1, 0
	releaseall
	end

SeafoamIslands_B4F_EventScript_AddBoulderPresent::
	addvar NUM_BOULDERS_PRESENT, 1
	return

SeafoamIslands_B4F_EventScript_RideCurrentFar::
	applymovement LOCALID_PLAYER, SeafoamIslands_B4F_Movement_RideCurrentFar
	waitmovement 0
	return

SeafoamIslands_B4F_EventScript_RideCurrentClose::
	applymovement LOCALID_PLAYER, SeafoamIslands_B4F_Movement_RideCurrentClose
	waitmovement 0
	return

SeafoamIslands_B4F_EventScript_CurrentBlocked::
	setvar VAR_TEMP_1, 0
	releaseall
	end

SeafoamIslands_B4F_Movement_RideCurrentFar::
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	step_end

SeafoamIslands_B4F_Movement_RideCurrentClose::
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_up
	step_end

@ Triggers blocking re-entry to B3F
SeafoamIslands_B4F_EventScript_UpwardCurrent::
	lockall
	applymovement LOCALID_PLAYER, SeafoamIslands_B4F_Movement_WalkUp
	waitmovement 0
	releaseall
	end

SeafoamIslands_B4F_Movement_WalkUp::
	walk_up
	step_end

SeafoamIslands_B4F_EventScript_Articuno::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_MOLTRES, 55
	waitse
	playmoncry SPECIES_MOLTRES, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 10
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, SeafoamIslands_B4F_EventScript_DefeatedArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SeafoamIslands_B4F_EventScript_RanFromArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SeafoamIslands_B4F_EventScript_RanFromArticuno
	setflag FLAG_FOUGHT_ARTICUNO
	release
	end

SeafoamIslands_B4F_EventScript_DefeatedArticuno::
	setflag FLAG_FOUGHT_ARTICUNO
	goto EventScript_RemoveStaticMon
	end

SeafoamIslands_B4F_EventScript_RanFromArticuno::
	setvar VAR_0x8004, SPECIES_MOLTRES
	goto EventScript_MonFlewAway
	end

SeafoamIslands_B4F_EventScript_BoulderHintSign::
	msgbox SeafoamIslands_B4F_Text_BouldersMightChangeWaterFlow, MSGBOX_SIGN
	end

SeafoamIslands_B4F_EventScript_FastCurrentSign::
	msgbox SeafoamIslands_B4F_Text_DangerFastCurrent, MSGBOX_SIGN
	end

SeafoamIslands_B4F_EventScript_AllyStub::
	end

SeafoamIslands_B4F_EventScript_CheckOnybris::
	goto_if_set FLAG_SEAFOAM_BOSS_DONE, SeafoamIslands_B4F_EventScript_OnybrisDone
	goto_if_unset FLAG_SEAFOAM_ALLIES_MET, SeafoamIslands_B4F_EventScript_OnybrisDone
	setvar VAR_TEMP_3, 1
	return

SeafoamIslands_B4F_EventScript_OnybrisDone::
	setflag FLAG_TEMP_1
	goto_if_unset FLAG_SEAFOAM_BOSS_DONE, SeafoamIslands_B4F_EventScript_OnybrisHideAll
	return

SeafoamIslands_B4F_EventScript_OnybrisHideAll::
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	return

SeafoamIslands_B4F_EventScript_KronosScene::
	lockall
	msgbox SeafoamIslands_B4F_Text_FloorScene
	msgbox SeafoamIslands_B4F_Text_KronosIntro
	closemessage
	setvar VAR_LAST_TALKED, LOCALID_SEAFOAM_KRONOS
	trainerbattle_no_intro TRAINER_AQUA_ADMIN_MATT, SeafoamIslands_B4F_Text_KronosDefeat
	msgbox SeafoamIslands_B4F_Text_KronosPost
	closemessage
	playse SE_THUNDER
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 4
	special ShakeScreen
	waitstate
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_SEAFOAM_KRONOS
	delay 20
	fadescreen FADE_FROM_BLACK
	msgbox SeafoamIslands_B4F_Text_GoldAfterScene
	msgbox SeafoamIslands_B4F_Text_SilverAfterScene
	closemessage
	setflag FLAG_SEAFOAM_BOSS_DONE
	setvar VAR_TEMP_3, 0
	releaseall
	end

SeafoamIslands_B4F_EventScript_GoldBeaten::
	msgbox SeafoamIslands_B4F_Text_GoldBeaten, MSGBOX_NPC
	end

SeafoamIslands_B4F_EventScript_SilverBeaten::
	msgbox SeafoamIslands_B4F_Text_SilverBeaten, MSGBOX_NPC
	end
