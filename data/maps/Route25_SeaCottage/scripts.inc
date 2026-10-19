Route25_SeaCottage_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route25_SeaCottage_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route25_SeaCottage_OnFrame
	.byte 0

Route25_SeaCottage_OnTransition::
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	goto_if_unset FLAG_TOPAZE_COUNCIL, Route25_SeaCottage_OnTransitionEnd
	goto_if_ne VAR_ROUTE25_MISTY, 2, Route25_SeaCottage_OnTransitionEnd
	clearflag FLAG_TEMP_4
Route25_SeaCottage_OnTransitionEnd::
	end

Route25_SeaCottage_OnFrame::
	map_script_2 VAR_ROUTE25_MISTY, 1, Route25_SeaCottage_EventScript_Ambush
	.2byte 0

Route25_SeaCottage_EventScript_Nobody::
	end

@ Topaze, post-game : MISTY revient a la chaumiere, un mot et un cadeau selon la fin choisie
Route25_SeaCottage_EventScript_MistyPost::
	lock
	faceplayer
	textcolor NPC_TEXT_COLOR_FEMALE
	goto_if_set FLAG_QUEST_MISTY_VISIT, Route25_SeaCottage_EventScript_MistyBye
	switch VAR_TOPAZE_ENDING
	case 1, Route25_SeaCottage_EventScript_MistyEnd1
	case 2, Route25_SeaCottage_EventScript_MistyEnd2
	case 3, Route25_SeaCottage_EventScript_MistyEnd3
	release
	end

Route25_SeaCottage_EventScript_MistyEnd1::
	msgbox Route25_SeaCottage_Text_MistyEnd1
	giveitem ITEM_WATER_STONE
	goto Route25_SeaCottage_EventScript_MistyDone
	end

Route25_SeaCottage_EventScript_MistyEnd2::
	msgbox Route25_SeaCottage_Text_MistyEnd2
	giveitem ITEM_FULL_RESTORE, 5
	goto Route25_SeaCottage_EventScript_MistyDone
	end

Route25_SeaCottage_EventScript_MistyEnd3::
	msgbox Route25_SeaCottage_Text_MistyEnd3
	giveitem ITEM_MAX_ELIXIR, 5
	goto Route25_SeaCottage_EventScript_MistyDone
	end

Route25_SeaCottage_EventScript_MistyDone::
	setflag FLAG_QUEST_MISTY_VISIT
	release
	end

Route25_SeaCottage_EventScript_MistyBye::
	msgbox Route25_SeaCottage_Text_MistyBye
	release
	end

Route25_SeaCottage_EventScript_Ambush::
	lockall
	textcolor NPC_TEXT_COLOR_FEMALE
	clearflag FLAG_TEMP_4
	addobject LOCALID_COTTAGE_MISTY
	delay 20
	msgbox Route25_SeaCottage_Text_MistyWhisper
	closemessage
	textcolor NPC_TEXT_COLOR_MALE
	clearflag FLAG_TEMP_5
	clearflag FLAG_TEMP_6
	addobject LOCALID_COTTAGE_GRUNT_A
	addobject LOCALID_COTTAGE_GRUNT_B
	playse SE_PIN
	delay 20
	msgbox Route25_SeaCottage_Text_GruntsAppear
	closemessage
	textcolor NPC_TEXT_COLOR_FEMALE
	msgbox Route25_SeaCottage_Text_MistySplit
	closemessage
	applymovement LOCALID_COTTAGE_MISTY, Route25_SeaCottage_Movement_MistyToGruntB
	waitmovement 0
	msgbox Route25_SeaCottage_Text_MistyBattle
	closemessage
	playse SE_M_SURF
	delay 40
	textcolor NPC_TEXT_COLOR_MALE
	msgbox Route25_SeaCottage_Text_GruntBDown
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_COTTAGE_GRUNT_B
	fadescreen FADE_FROM_BLACK
	setvar VAR_LAST_TALKED, LOCALID_COTTAGE_GRUNT_A
	@ Topaze: the grunt walks up to the player (no more duel from across the room)
	applymovement LOCALID_COTTAGE_GRUNT_A, Route25_SeaCottage_Movement_GruntAApproach
	waitmovement 0
	msgbox Route25_SeaCottage_Text_GruntAIntro
	trainerbattle_no_intro TRAINER_TEAM_ROCKET_GRUNT_5, Route25_SeaCottage_Text_GruntADefeat
	msgbox Route25_SeaCottage_Text_GruntADrops
	closemessage
	setflag FLAG_GOT_SS_TICKET
	setflag FLAG_GOT_SS_TICKET_DUP
	setflag FLAG_SYS_NOT_SOMEONES_PC
	giveitem_msg Route25_SeaCottage_Text_FoundSSTicket, ITEM_SS_TICKET, 1, MUS_OBTAIN_KEY_ITEM
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_COTTAGE_GRUNT_A
	fadescreen FADE_FROM_BLACK
	textcolor NPC_TEXT_COLOR_FEMALE
	applymovement LOCALID_COTTAGE_MISTY, Route25_SeaCottage_Movement_MistyBack
	waitmovement 0
	msgbox Route25_SeaCottage_Text_MistyFarewell
	closemessage
	applymovement LOCALID_COTTAGE_MISTY, Route25_SeaCottage_Movement_MistyLeaves
	waitmovement 0
	removeobject LOCALID_COTTAGE_MISTY
	setvar VAR_ROUTE25_MISTY, 2
	releaseall
	end

Route25_SeaCottage_Movement_GruntAApproach::
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	face_down
	step_end

Route25_SeaCottage_Movement_MistyToGruntB::
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	face_up
	step_end

Route25_SeaCottage_Movement_MistyBack::
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	face_right
	step_end

Route25_SeaCottage_Movement_MistyLeaves::
	walk_down
	step_end

Route25_SeaCottage_EventScript_Computer::
	msgbox Route25_SeaCottage_Text_AbandonedPC, MSGBOX_SIGN
	end
