Route25_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route25_OnTransition
	.byte 0

Route25_OnTransition::
	goto_if_ne VAR_ROUTE25_MISTY, 0, Route25_EventScript_HideMisty
	end

Route25_EventScript_HideMisty::
	setflag FLAG_TEMP_10
	end

Route25_EventScript_MistyIdle::
	msgbox Route25_Text_MistyIdle, MSGBOX_NPC
	end

Route25_EventScript_MistyMeet::
	lockall
	textcolor NPC_TEXT_COLOR_FEMALE
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox Route25_Text_MistyMeet
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_ROUTE25_MISTY
	setvar VAR_ROUTE25_MISTY, 1
	fadescreen FADE_FROM_BLACK
	releaseall
	end

Route25_EventScript_SeaCottageSign::
	msgbox Route25_Text_SeaCottageSign, MSGBOX_SIGN
	end


@ Topaze: PROCHE LOLA (optionnel, fort)
Route25_EventScript_ProcheLola::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, Route25_EventScript_ProcheLola_TooEarly
	goto_if_defeated TRAINER_PROCHE_LOLA, Route25_EventScript_ProcheLola_After
	msgbox Route25_Text_ProcheLola_Intro
	checkitemspace ITEM_NEVER_MELT_ICE
	goto_if_eq VAR_RESULT, FALSE, Route25_EventScript_ProcheLola_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_LOLA, Route25_Text_ProcheLola_Defeat
	msgbox Route25_Text_ProcheLola_Win
	giveitem ITEM_NEVER_MELT_ICE
	msgbox Route25_Text_ProcheLola_After
	release
	end

Route25_EventScript_ProcheLola_After::
	msgbox Route25_Text_ProcheLola_After
	release
	end

Route25_EventScript_ProcheLola_TooEarly::
	msgbox Route25_Text_ProcheLola_Early
	release
	end

Route25_EventScript_ProcheLola_NoRoom::
	msgbox Route25_Text_ProcheLola_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route25_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE25_0, Route25_EventScript_TopazeFind0_Done
	checkitemspace ITEM_PP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, Route25_EventScript_TopazeFind0_Full
	giveitem ITEM_PP_UP, 1
	setflag FLAG_TOPAZE_HID_ROUTE25_0
	release
	end

Route25_EventScript_TopazeFind0_Done::
	release
	end

Route25_EventScript_TopazeFind0_Full::
	msgbox Route25_Text_TopazeFindFull
	release
	end

Route25_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE25_1, Route25_EventScript_TopazeFind1_Done
	checkitemspace ITEM_STAR_PIECE, 1
	goto_if_eq VAR_RESULT, FALSE, Route25_EventScript_TopazeFind1_Full
	giveitem ITEM_STAR_PIECE, 1
	setflag FLAG_TOPAZE_HID_ROUTE25_1
	release
	end

Route25_EventScript_TopazeFind1_Done::
	release
	end

Route25_EventScript_TopazeFind1_Full::
	msgbox Route25_Text_TopazeFindFull
	release
	end


Route25_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
