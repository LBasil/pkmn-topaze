Route24_MapScripts::
	.byte 0

Route24_EventScript_Rocket::
	lock
	faceplayer
	goto_if_eq VAR_MAP_SCENE_ROUTE24, 2, Route24_EventScript_RocketGiveNugget
	msgbox Route24_Text_YoudBecomeTopRocketLeader
	release
	end

Route24_EventScript_RocketTriggerLeft::
	lockall
	setvar VAR_TEMP_1, 0
	goto Route24_EventScript_RocketTrigger
	end

Route24_EventScript_RocketTriggerMid::
	lockall
	setvar VAR_TEMP_1, 1
	goto Route24_EventScript_RocketTrigger
	end

Route24_EventScript_RocketTriggerRight::
	lockall
	setvar VAR_TEMP_1, 2
	goto Route24_EventScript_RocketTrigger
	end

Route24_EventScript_RocketTrigger::
	textcolor NPC_TEXT_COLOR_MALE
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	call_if_eq VAR_TEMP_1, 0, Route24_EventScript_RocketWalkLeft
	call_if_eq VAR_TEMP_1, 1, Route24_EventScript_RocketWalkMid
	call_if_eq VAR_TEMP_1, 2, Route24_EventScript_RocketWalkRight
	msgbox Route24_Text_JustEarnedFabulousPrize
	call Route24_EventScript_BattleRocket
	releaseall
	end

Route24_EventScript_RocketWalkLeft::
	applymovement LOCALID_ROUTE24_ROCKET, Route24_Movement_RocketWalkLeft
	waitmovement 0
	return

Route24_EventScript_RocketWalkMid::
	applymovement LOCALID_ROUTE24_ROCKET, Route24_Movement_RocketWalkMid
	waitmovement 0
	return

Route24_EventScript_RocketWalkRight::
	applymovement LOCALID_ROUTE24_ROCKET, Route24_Movement_RocketWalkRight
	waitmovement 0
	return

Route24_Movement_RocketWalkLeft::
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_left
	walk_in_place_faster_down
	step_end

Route24_Movement_RocketWalkMid::
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

Route24_Movement_RocketWalkRight::
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_right
	walk_in_place_faster_down
	step_end

Route24_EventScript_BattleRocket::
	message Route24_Text_JoinTeamRocket
	waitmessage
	playbgm MUS_ENCOUNTER_ROCKET, 0
	waitbuttonpress
	setvar VAR_LAST_TALKED, LOCALID_ROUTE24_ROCKET
	trainerbattle_no_intro TRAINER_TEAM_ROCKET_GRUNT_6, Route24_Text_RocketDefeat
	setvar VAR_MAP_SCENE_ROUTE24, 2
	msgbox Route24_Text_YoudBecomeTopRocketLeader
	goto Route24_EventScript_RocketGiveNugget
	end

Route24_EventScript_RocketGiveNugget::
	checkitemspace ITEM_NUGGET
	goto_if_eq VAR_RESULT, FALSE, Route24_EventScript_NoRoomForNugget
	giveitem_msg Route24_Text_ReceivedNuggetFromMysteryTrainer, ITEM_NUGGET
	msgbox Route24_Text_ImOutOfHere
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ROUTE24_ROCKET
	setflag FLAG_HIDE_NUGGET_BRIDGE_ROCKET
	setvar VAR_MAP_SCENE_ROUTE24, 1
	fadescreen FADE_FROM_BLACK
	release
	end

Route24_EventScript_NoRoomForNugget::
	msgbox Route24_Text_YouDontHaveAnyRoom
	release
	end

