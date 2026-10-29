Route22_MapScripts::
	.byte 0

Route22_EventScript_EarlyRivalTriggerTop::
	lockall
	setvar VAR_TEMP_1, 0
	setobjectxyperm LOCALID_ROUTE22_RIVAL, 29, 5
	goto Route22_EventScript_EarlyRival
	end

Route22_EventScript_EarlyRivalTriggerMid::
	lockall
	setvar VAR_TEMP_1, 1
	setobjectxyperm LOCALID_ROUTE22_RIVAL, 29, 5
	goto Route22_EventScript_EarlyRival
	end

Route22_EventScript_EarlyRivalTriggerBottom::
	lockall
	setvar VAR_TEMP_1, 2
	setobjectxyperm LOCALID_ROUTE22_RIVAL, 30, 5
	goto Route22_EventScript_EarlyRival
	end

Route22_EventScript_EarlyRival::
	textcolor NPC_TEXT_COLOR_MALE
	playbgm MUS_ENCOUNTER_RIVAL, 0
	addobject LOCALID_ROUTE22_RIVAL
	call_if_eq VAR_TEMP_1, 0, Route22_EventScript_EarlyRivalApproach
	call_if_eq VAR_TEMP_1, 1, Route22_EventScript_EarlyRivalApproach
	call_if_eq VAR_TEMP_1, 2, Route22_EventScript_EarlyRivalApproachBottom
	delay 6
	msgbox Route22_Text_EarlyRivalIntro
	call_if_eq VAR_STARTER_MON, 2, Route22_EventScript_EarlyRivalSquirtle
	call_if_eq VAR_STARTER_MON, 1, Route22_EventScript_EarlyRivalBulbasaur
	call_if_eq VAR_STARTER_MON, 0, Route22_EventScript_EarlyRivalCharmander
	msgbox Route22_Text_EarlyRivalPostBattle
	closemessage
	delay 10
	playbgm MUS_RIVAL_EXIT, 0
	call_if_eq VAR_TEMP_1, 0, Route22_EventScript_EarlyRivalExit
	call_if_eq VAR_TEMP_1, 1, Route22_EventScript_EarlyRivalExit
	call_if_eq VAR_TEMP_1, 2, Route22_EventScript_EarlyRivalExitBottom
	fadedefaultbgm
	removeobject LOCALID_ROUTE22_RIVAL
	setvar VAR_MAP_SCENE_ROUTE22, 2
	releaseall
	end

Route22_EventScript_EarlyRivalApproach::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_RivalApproach
	waitmovement 0
	call_if_eq VAR_TEMP_1, 0, Route22_EventScript_RivalStepUp
	return

Route22_EventScript_RivalStepUp::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_RivalStepUp
	waitmovement 0
	return

Route22_Movement_RivalStepUp::
	walk_up
	walk_in_place_faster_right
	step_end

Route22_EventScript_EarlyRivalApproachBottom::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_RivalApproachBottom
	applymovement LOCALID_PLAYER, Route22_Movement_PlayerFaceRival
	waitmovement 0
	return

Route22_EventScript_EarlyRivalSquirtle::
	trainerbattle_earlyrival TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE, 0, Route22_Text_EarlyRivalDefeat, Text_RivalVictory
	return

Route22_EventScript_EarlyRivalBulbasaur::
	trainerbattle_earlyrival TRAINER_RIVAL_ROUTE22_EARLY_BULBASAUR, 0, Route22_Text_EarlyRivalDefeat, Text_RivalVictory
	return

Route22_EventScript_EarlyRivalCharmander::
	trainerbattle_earlyrival TRAINER_RIVAL_ROUTE22_EARLY_CHARMANDER, 0, Route22_Text_EarlyRivalDefeat, Text_RivalVictory
	return

Route22_EventScript_EarlyRivalExit::
	call_if_eq VAR_TEMP_1, 0, Route22_EventScript_RivalStepDown
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_EarlyRivalExit
	waitmovement 0
	return

Route22_EventScript_RivalStepDown::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_RivalStepDown
	waitmovement 0
	return

Route22_Movement_RivalStepDown::
	walk_down
	step_end

Route22_EventScript_EarlyRivalExitBottom::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_EarlyRivalExitBottom
	waitmovement 0
	return

Route22_Movement_UnusedRivalExit:: @ 8
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

Route22_Movement_EarlyRivalExit::
	walk_left
	walk_left
	walk_left
	step_end

Route22_Movement_EarlyRivalExitBottom::
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Route22_Movement_RivalApproach::
	walk_right
	walk_right
	walk_right
	step_end

Route22_Movement_RivalApproachBottom::
	walk_right
	walk_right
	walk_right
	walk_in_place_faster_down
	step_end

Route22_Movement_PlayerFaceRival::
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_8
	walk_in_place_faster_up
	step_end

Route22_EventScript_LateRivalTriggerTop::
	lockall
	setvar VAR_TEMP_1, 0
	setobjectxyperm LOCALID_ROUTE22_RIVAL, 29, 5
	goto Route22_EventScript_LateRival
	end

Route22_EventScript_LateRivalTriggerMid::
	lockall
	setvar VAR_TEMP_1, 1
	setobjectxyperm LOCALID_ROUTE22_RIVAL, 29, 5
	goto Route22_EventScript_LateRival
	end

Route22_EventScript_LateRivalTriggerBottom::
	lockall
	setvar VAR_TEMP_1, 2
	setobjectxyperm LOCALID_ROUTE22_RIVAL, 30, 5
	goto Route22_EventScript_LateRival
	end

Route22_EventScript_LateRival::
	textcolor NPC_TEXT_COLOR_MALE
	playbgm MUS_ENCOUNTER_RIVAL, 0
	addobject LOCALID_ROUTE22_RIVAL
	call_if_eq VAR_TEMP_1, 0, Route22_EventScript_LateRivalApproach
	call_if_eq VAR_TEMP_1, 1, Route22_EventScript_LateRivalApproach
	call_if_eq VAR_TEMP_1, 2, Route22_EventScript_LateRivalApproachBottom
	msgbox Route22_Text_LateRivalIntro
	setvar VAR_LAST_TALKED, LOCALID_ROUTE22_RIVAL
	call_if_eq VAR_STARTER_MON, 2, Route22_EventScript_LateRivalSquirtle
	call_if_eq VAR_STARTER_MON, 1, Route22_EventScript_LateRivalBulbasaur
	call_if_eq VAR_STARTER_MON, 0, Route22_EventScript_LateRivalCharmander
	msgbox Route22_Text_LateRivalPostBattle
	closemessage
	delay 10
	playbgm MUS_RIVAL_EXIT, 0
	call_if_eq VAR_TEMP_1, 0, Route22_EventScript_RivalStepDown
	call_if_eq VAR_TEMP_1, 2, Route22_EventScript_LateRivalExtraLeft
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_LateRivalExit
	waitmovement 0
	fadedefaultbgm
	removeobject LOCALID_ROUTE22_RIVAL
	setvar VAR_MAP_SCENE_ROUTE22, 4
	releaseall
	end

Route22_EventScript_LateRivalApproach::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_RivalApproach
	waitmovement 0
	call_if_eq VAR_TEMP_1, 0, Route22_EventScript_RivalStepUp
	return

Route22_EventScript_LateRivalApproachBottom::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_RivalApproachBottom
	applymovement LOCALID_PLAYER, Route22_Movement_PlayerFaceRival
	waitmovement 0
	return

Route22_EventScript_LateRivalSquirtle::
	trainerbattle_no_intro TRAINER_RIVAL_ROUTE22_LATE_SQUIRTLE, Route22_Text_LateRivalDefeat
	return

Route22_EventScript_LateRivalBulbasaur::
	trainerbattle_no_intro TRAINER_RIVAL_ROUTE22_LATE_BULBASAUR, Route22_Text_LateRivalDefeat
	return

Route22_EventScript_LateRivalCharmander::
	trainerbattle_no_intro TRAINER_RIVAL_ROUTE22_LATE_CHARMANDER, Route22_Text_LateRivalDefeat
	return

Route22_Movement_LateRivalExit::
	walk_left
	walk_left
	walk_left
	step_end

Route22_EventScript_LeagueGateSign::
	msgbox Route22_Text_LeagueGateSign, MSGBOX_SIGN
	end

Route22_EventScript_LateRivalExtraLeft::
	applymovement LOCALID_ROUTE22_RIVAL, Route22_Movement_OneLeft
	waitmovement 0
	return

Route22_Movement_OneLeft::
	walk_left
	step_end

@ Topaze: PROCHE VINCENT (optionnel, fort)
Route22_EventScript_ProcheVincent::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, Route22_EventScript_ProcheVincent_TooEarly
	goto_if_defeated TRAINER_PROCHE_VINCENT, Route22_EventScript_ProcheVincent_After
	msgbox Route22_Text_ProcheVincent_Intro
	checkitemspace ITEM_MAGNET
	goto_if_eq VAR_RESULT, FALSE, Route22_EventScript_ProcheVincent_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_VINCENT, Route22_Text_ProcheVincent_Defeat
	msgbox Route22_Text_ProcheVincent_Win
	giveitem ITEM_MAGNET
	msgbox Route22_Text_ProcheVincent_After
	release
	end

Route22_EventScript_ProcheVincent_After::
	msgbox Route22_Text_ProcheVincent_After
	release
	end

Route22_EventScript_ProcheVincent_TooEarly::
	msgbox Route22_Text_ProcheVincent_Early
	release
	end

Route22_EventScript_ProcheVincent_NoRoom::
	msgbox Route22_Text_ProcheVincent_NoRoom
	release
	end

@ Topaze: indice du temps deregle
Route22_EventScript_TimeHint::
	setflag FLAG_TOPAZE_CLOCK_3
	msgbox Route22_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route22_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE22_0, Route22_EventScript_TopazeFind0_Done
	checkitemspace ITEM_HYPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, Route22_EventScript_TopazeFind0_Full
	giveitem ITEM_HYPER_POTION, 1
	setflag FLAG_TOPAZE_HID_ROUTE22_0
	release
	end

Route22_EventScript_TopazeFind0_Done::
	release
	end

Route22_EventScript_TopazeFind0_Full::
	msgbox Route22_Text_TopazeFindFull
	release
	end


Route22_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
