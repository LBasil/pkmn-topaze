IndigoPlateau_Exterior_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, IndigoPlateau_Exterior_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, IndigoPlateau_Exterior_OnFrame
	.byte 0

IndigoPlateau_Exterior_OnTransition::
	call IndigoPlateau_Exterior_EventScript_TitanSetup
	setworldmapflag FLAG_WORLD_MAP_INDIGO_PLATEAU_EXTERIOR
	call IndigoPlateau_Exterior_EventScript_GruntsCheck
	call_if_eq VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR, 1, IndigoPlateau_Exterior_EventScript_PlayCreditsMusic
	end

IndigoPlateau_Exterior_EventScript_PlayCreditsMusic::
	playbgm MUS_CREDITS, 0
	return

IndigoPlateau_Exterior_OnFrame::
	map_script_2 VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR, 1, IndigoPlateau_Exterior_EventScript_Credits
	.2byte 0


@ After beating the champion, you are warped to the main
@ entrance of Indigo Plateau. This script starts running
@ immediately after your walking animation.
@ The script is timed to the music.
IndigoPlateau_Exterior_EventScript_Credits::
	lockall
	delay 105

	@ Rival exits building. Spawn a dummy object to lock the camera.
	opendoor 11, 6
	waitdooranim
	special SpawnCameraObject
	addobject LOCALID_CREDITS_RIVAL
	applymovement LOCALID_CREDITS_RIVAL, IndigoPlateau_Exterior_Movement_RivalExitBuilding
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PushPlayerOutOfWay
	waitmovement 0
	closedoor 11, 6
	waitdooranim

	@ Rival runs off
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerWatchRivalLeave
	applymovement LOCALID_CREDITS_RIVAL, IndigoPlateau_Exterior_Movement_RivalLeave
	waitmovement 0
	delay 100

	@ Oak exits building
	opendoor 11, 6
	waitdooranim
	addobject LOCALID_CREDITS_PROF_OAK
	applymovement LOCALID_CREDITS_PROF_OAK, IndigoPlateau_Exterior_Movement_OakExitBuilding
	waitmovement 0
	closedoor 11, 6
	waitdooranim
	delay 160

	@ Oak looks at player, then walks off
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerWatchOakLeave
	applymovement LOCALID_CREDITS_PROF_OAK, IndigoPlateau_Exterior_Movement_OakLeave
	waitmovement 0
	delay 100

	@ Player begin to leave
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerBeginLeave
	waitmovement 0
	delay 155
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerFaceLeague
	waitmovement 0
	delay 90

	@ Player runs off
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerTurnAround
	waitmovement 0
	applymovement LOCALID_PLAYER, IndigoPlateau_Exterior_Movement_PlayerLeave
	waitmovement 0

	@ Reset the map state and roll the credits
	special RemoveCameraObject
	setvar VAR_MAP_SCENE_INDIGO_PLATEAU_EXTERIOR, 0
	removeobject LOCALID_CREDITS_RIVAL
	removeobject LOCALID_CREDITS_PROF_OAK
	special DoCredits
	waitstate
	releaseall
	end

IndigoPlateau_Exterior_Movement_PlayerLeave::
	player_run_down
	player_run_down
	player_run_down
	player_run_down
	player_run_down
	player_run_down
	step_end

@ Unused
IndigoPlateau_Exterior_Movement_PlayerExitBuilding::
	walk_down
	walk_down
	step_end

IndigoPlateau_Exterior_Movement_PlayerWatchRivalLeave::
	delay_16
	delay_4
	walk_in_place_faster_down
	step_end

IndigoPlateau_Exterior_Movement_PlayerWatchOakLeave::
	delay_8
	walk_in_place_faster_right
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_down
	step_end

IndigoPlateau_Exterior_Movement_PlayerBeginLeave::
	walk_right
	delay_16
	walk_down
	walk_down
	delay_16
	delay_16
	step_end

IndigoPlateau_Exterior_Movement_PlayerTurnAround::
	walk_in_place_faster_down
	step_end

IndigoPlateau_Exterior_Movement_PushPlayerOutOfWay::
	face_right
	lock_facing_direction
	walk_left
	unlock_facing_direction
	step_end

IndigoPlateau_Exterior_Movement_PlayerFaceLeague::
	walk_in_place_faster_up
	step_end

IndigoPlateau_Exterior_Movement_RivalLeave::
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

IndigoPlateau_Exterior_Movement_RivalExitBuilding::
	walk_fast_down
	step_end

IndigoPlateau_Exterior_Movement_OakLeave::
	walk_in_place_faster_left
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_down
	delay_16
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

IndigoPlateau_Exterior_Movement_OakExitBuilding::
	walk_down
	step_end

IndigoPlateau_Exterior_EventScript_TitanSetup::
	setflag FLAG_HIDE_TITAN_RAYQUAZA
	goto_if_set FLAG_FOUGHT_TITAN_RAYQUAZA, EventScript_Return
	goto_if_ne VAR_TOPAZE_ENDING, 3, EventScript_Return
	goto_if_ne VAR_REBELS_ROUND, 9, EventScript_Return
	clearflag FLAG_HIDE_TITAN_RAYQUAZA
	return

IndigoPlateau_Exterior_EventScript_Titan::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	msgbox IndigoPlateau_Exterior_Text_TitanIntro
	setwildbattle SPECIES_RAYQUAZA, 0
	waitse
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, IndigoPlateau_Exterior_EventScript_TitanWon
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, IndigoPlateau_Exterior_EventScript_TitanRan
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, IndigoPlateau_Exterior_EventScript_TitanRan
	setflag FLAG_FOUGHT_TITAN_RAYQUAZA
	setflag FLAG_HIDE_TITAN_RAYQUAZA
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	release
	end

IndigoPlateau_Exterior_EventScript_TitanWon::
	setflag FLAG_FOUGHT_TITAN_RAYQUAZA
	goto EventScript_RemoveStaticMon
	end

IndigoPlateau_Exterior_EventScript_TitanRan::
	setvar VAR_0x8004, SPECIES_RAYQUAZA
	goto EventScript_MonFlewAway
	end

IndigoPlateau_Exterior_Text_TitanIntro::
	.string "A presence older than the legends\n"
	.string "rises before you...\p"
	.string "It has waited for a ruler worthy\n"
	.string "of the throne. Show it yours!$"

@ --- Sbires silencieux (apres le repaire, avant le Champion)
IndigoPlateau_Exterior_EventScript_GruntsCheck::
	setflag FLAG_TOPAZE_HIDE_PLATEAU_GRUNTS
	goto_if_unset FLAG_VR_BOSS_DONE, IndigoPlateau_Exterior_GruntsEnd
	goto_if_set FLAG_SYS_GAME_CLEAR, IndigoPlateau_Exterior_GruntsEnd
	clearflag FLAG_TOPAZE_HIDE_PLATEAU_GRUNTS
IndigoPlateau_Exterior_GruntsEnd::
	return

IndigoPlateau_Exterior_EventScript_Grunt1::
	msgbox IndigoPlateau_Exterior_Text_Grunt1, MSGBOX_NPC
	end

IndigoPlateau_Exterior_Text_Grunt1::
	.string "GRUNT: ...We are only watching.$"

IndigoPlateau_Exterior_EventScript_Grunt2::
	msgbox IndigoPlateau_Exterior_Text_Grunt2, MSGBOX_NPC
	end

IndigoPlateau_Exterior_Text_Grunt2::
	.string "GRUNT: The BOSS asked us to keep the\nroad warm. Go ahead.$"

IndigoPlateau_Exterior_EventScript_Grunt3::
	msgbox IndigoPlateau_Exterior_Text_Grunt3, MSGBOX_NPC
	end

IndigoPlateau_Exterior_Text_Grunt3::
	.string "GRUNT: Nobody here will touch you.\nOrders.$"

IndigoPlateau_Exterior_EventScript_Grunt4::
	msgbox IndigoPlateau_Exterior_Text_Grunt4, MSGBOX_NPC
	end

IndigoPlateau_Exterior_Text_Grunt4::
	.string "GRUNT: Win. That is the whole job\ntoday.$"

IndigoPlateau_Exterior_EventScript_Grunt5::
	msgbox IndigoPlateau_Exterior_Text_Grunt5, MSGBOX_NPC
	end

IndigoPlateau_Exterior_Text_Grunt5::
	.string "GRUNT: We came from every town you\npassed.$"

IndigoPlateau_Exterior_EventScript_Grunt6::
	msgbox IndigoPlateau_Exterior_Text_Grunt6, MSGBOX_NPC
	end

IndigoPlateau_Exterior_Text_Grunt6::
	.string "GRUNT: Ten stones. One hand. We are\npatient.$"

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
IndigoPlateau_Exterior_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_TOWN_INDIGOPLATEAU_EXTERIOR, IndigoPlateau_Exterior_EventScript_TopazeFind0_Done
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, IndigoPlateau_Exterior_EventScript_TopazeFind0_Full
	giveitem ITEM_RARE_CANDY, 1
	setflag FLAG_TOPAZE_HID_TOWN_INDIGOPLATEAU_EXTERIOR
	release
	end

IndigoPlateau_Exterior_EventScript_TopazeFind0_Done::
	release
	end

IndigoPlateau_Exterior_EventScript_TopazeFind0_Full::
	msgbox IndigoPlateau_Exterior_Text_TopazeFindFull
	release
	end


IndigoPlateau_Exterior_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
