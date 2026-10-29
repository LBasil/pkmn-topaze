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


@ Topaze: indice du temps deregle
Route24_EventScript_TimeHint::
	msgbox Route24_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: quete de route (THE BRIDGE WATCH)
Route24_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE24, Route24_EventScript_RQuest_Done
	checkitem ITEM_MAX_REPEL, 2
	goto_if_eq VAR_RESULT, FALSE, Route24_EventScript_RQuest_Ask
	checkitemspace ITEM_RARE_CANDY, 2
	goto_if_eq VAR_RESULT, FALSE, Route24_EventScript_RQuest_NoRoom
	removeitem ITEM_MAX_REPEL, 2
	setflag FLAG_TOPAZE_RQ_ROUTE24
	msgbox Route24_Text_RQuest_Ok
	giveitem ITEM_RARE_CANDY, 2
	release
	end

Route24_EventScript_RQuest_Ask::
	msgbox Route24_Text_RQuest_Ask
	release
	end

Route24_EventScript_RQuest_Done::
	msgbox Route24_Text_RQuest_Done
	release
	end

Route24_EventScript_RQuest_NoRoom::
	msgbox Route24_Text_RQuest_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route24_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE24_0, Route24_EventScript_TopazeFind0_Done
	checkitemspace ITEM_NUGGET, 1
	goto_if_eq VAR_RESULT, FALSE, Route24_EventScript_TopazeFind0_Full
	giveitem ITEM_NUGGET, 1
	setflag FLAG_TOPAZE_HID_ROUTE24_0
	release
	end

Route24_EventScript_TopazeFind0_Done::
	release
	end

Route24_EventScript_TopazeFind0_Full::
	msgbox Route24_Text_TopazeFindFull
	release
	end

Route24_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE24_1, Route24_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, Route24_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_ELIXIR, 1
	setflag FLAG_TOPAZE_HID_ROUTE24_1
	release
	end

Route24_EventScript_TopazeFind1_Done::
	release
	end

Route24_EventScript_TopazeFind1_Full::
	msgbox Route24_Text_TopazeFindFull
	release
	end


Route24_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
