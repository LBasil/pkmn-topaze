Route3_MapScripts::
	.byte 0

Route3_EventScript_Youngster::
	msgbox Route3_Text_TunnelFromCeruleanTiring, MSGBOX_NPC
	end

Route3_EventScript_RouteSign::
	msgbox Route3_Text_RouteSign, MSGBOX_SIGN
	end

@ Topaze: PROCHE THOMAS (optionnel, fort)
Route3_EventScript_ProcheThomas::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, Route3_EventScript_ProcheThomas_TooEarly
	goto_if_defeated TRAINER_PROCHE_THOMAS, Route3_EventScript_ProcheThomas_After
	msgbox Route3_Text_ProcheThomas_Intro
	checkitemspace ITEM_SILVER_POWDER
	goto_if_eq VAR_RESULT, FALSE, Route3_EventScript_ProcheThomas_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_THOMAS, Route3_Text_ProcheThomas_Defeat
	msgbox Route3_Text_ProcheThomas_Win
	giveitem ITEM_SILVER_POWDER
	msgbox Route3_Text_ProcheThomas_After
	release
	end

Route3_EventScript_ProcheThomas_After::
	msgbox Route3_Text_ProcheThomas_After
	release
	end

Route3_EventScript_ProcheThomas_TooEarly::
	msgbox Route3_Text_ProcheThomas_Early
	release
	end

Route3_EventScript_ProcheThomas_NoRoom::
	msgbox Route3_Text_ProcheThomas_NoRoom
	release
	end

@ Topaze: indice du temps deregle
Route3_EventScript_TimeHint::
	msgbox Route3_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: quete de route (STIFF AS A BOARD)
Route3_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE3, Route3_EventScript_RQuest_Done
	checkitem ITEM_PARALYZE_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, Route3_EventScript_RQuest_Ask
	checkitemspace ITEM_SUPER_POTION, 2
	goto_if_eq VAR_RESULT, FALSE, Route3_EventScript_RQuest_NoRoom
	removeitem ITEM_PARALYZE_HEAL, 2
	setflag FLAG_TOPAZE_RQ_ROUTE3
	msgbox Route3_Text_RQuest_Ok
	giveitem ITEM_SUPER_POTION, 2
	release
	end

Route3_EventScript_RQuest_Ask::
	msgbox Route3_Text_RQuest_Ask
	release
	end

Route3_EventScript_RQuest_Done::
	msgbox Route3_Text_RQuest_Done
	release
	end

Route3_EventScript_RQuest_NoRoom::
	msgbox Route3_Text_RQuest_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route3_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE3_0, Route3_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, Route3_EventScript_TopazeFind0_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_HID_ROUTE3_0
	release
	end

Route3_EventScript_TopazeFind0_Done::
	release
	end

Route3_EventScript_TopazeFind0_Full::
	msgbox Route3_Text_TopazeFindFull
	release
	end

Route3_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE3_1, Route3_EventScript_TopazeFind1_Done
	checkitemspace ITEM_GREAT_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, Route3_EventScript_TopazeFind1_Full
	giveitem ITEM_GREAT_BALL, 1
	setflag FLAG_TOPAZE_HID_ROUTE3_1
	release
	end

Route3_EventScript_TopazeFind1_Done::
	release
	end

Route3_EventScript_TopazeFind1_Full::
	msgbox Route3_Text_TopazeFindFull
	release
	end


Route3_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
