Route6_MapScripts::
	.byte 0

Route6_EventScript_UndergroundPathSign::
	msgbox Route6_Text_UndergroundPathSign, MSGBOX_SIGN
	end

@ Topaze: PROCHE JORDAN (optionnel, fort)
Route6_EventScript_ProcheJordan::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, Route6_EventScript_ProcheJordan_TooEarly
	goto_if_defeated TRAINER_PROCHE_JORDAN, Route6_EventScript_ProcheJordan_After
	msgbox Route6_Text_ProcheJordan_Intro
	checkitemspace ITEM_SILK_SCARF
	goto_if_eq VAR_RESULT, FALSE, Route6_EventScript_ProcheJordan_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_JORDAN, Route6_Text_ProcheJordan_Defeat
	msgbox Route6_Text_ProcheJordan_Win
	giveitem ITEM_SILK_SCARF
	msgbox Route6_Text_ProcheJordan_After
	release
	end

Route6_EventScript_ProcheJordan_After::
	msgbox Route6_Text_ProcheJordan_After
	release
	end

Route6_EventScript_ProcheJordan_TooEarly::
	msgbox Route6_Text_ProcheJordan_Early
	release
	end

Route6_EventScript_ProcheJordan_NoRoom::
	msgbox Route6_Text_ProcheJordan_NoRoom
	release
	end

@ Topaze: indice du temps deregle
Route6_EventScript_TimeHint::
	msgbox Route6_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: quete de route (THE HURT PARTNER)
Route6_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE6, Route6_EventScript_RQuest_Done
	checkitem ITEM_SUPER_POTION, 2
	goto_if_eq VAR_RESULT, FALSE, Route6_EventScript_RQuest_Ask
	checkitemspace ITEM_ULTRA_BALL, 3
	goto_if_eq VAR_RESULT, FALSE, Route6_EventScript_RQuest_NoRoom
	removeitem ITEM_SUPER_POTION, 2
	setflag FLAG_TOPAZE_RQ_ROUTE6
	msgbox Route6_Text_RQuest_Ok
	giveitem ITEM_ULTRA_BALL, 3
	release
	end

Route6_EventScript_RQuest_Ask::
	msgbox Route6_Text_RQuest_Ask
	release
	end

Route6_EventScript_RQuest_Done::
	msgbox Route6_Text_RQuest_Done
	release
	end

Route6_EventScript_RQuest_NoRoom::
	msgbox Route6_Text_RQuest_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route6_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE6_0, Route6_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, Route6_EventScript_TopazeFind0_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_ROUTE6_0
	release
	end

Route6_EventScript_TopazeFind0_Done::
	release
	end

Route6_EventScript_TopazeFind0_Full::
	msgbox Route6_Text_TopazeFindFull
	release
	end

Route6_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE6_1, Route6_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, Route6_EventScript_TopazeFind1_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_HID_ROUTE6_1
	release
	end

Route6_EventScript_TopazeFind1_Done::
	release
	end

Route6_EventScript_TopazeFind1_Full::
	msgbox Route6_Text_TopazeFindFull
	release
	end


Route6_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
