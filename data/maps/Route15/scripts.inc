Route15_MapScripts::
	.byte 0

Route15_EventScript_RouteSign::
	msgbox Route15_Text_RouteSign, MSGBOX_SIGN
	end

@ Topaze: PROCHE GAUTHIER (optionnel, fort)
Route15_EventScript_ProcheGauthier::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, Route15_EventScript_ProcheGauthier_TooEarly
	goto_if_defeated TRAINER_PROCHE_GAUTHIER, Route15_EventScript_ProcheGauthier_After
	msgbox Route15_Text_ProcheGauthier_Intro
	checkitemspace ITEM_BLACK_BELT
	goto_if_eq VAR_RESULT, FALSE, Route15_EventScript_ProcheGauthier_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_GAUTHIER, Route15_Text_ProcheGauthier_Defeat
	msgbox Route15_Text_ProcheGauthier_Win
	giveitem ITEM_BLACK_BELT
	msgbox Route15_Text_ProcheGauthier_After
	release
	end

Route15_EventScript_ProcheGauthier_After::
	msgbox Route15_Text_ProcheGauthier_After
	release
	end

Route15_EventScript_ProcheGauthier_TooEarly::
	msgbox Route15_Text_ProcheGauthier_Early
	release
	end

Route15_EventScript_ProcheGauthier_NoRoom::
	msgbox Route15_Text_ProcheGauthier_NoRoom
	release
	end

@ Topaze: indice du temps deregle
Route15_EventScript_TimeHint::
	msgbox Route15_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: quete de route (THE LAST WISH)
Route15_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE15, Route15_EventScript_RQuest_Done
	checkitem ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, Route15_EventScript_RQuest_Ask
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, Route15_EventScript_RQuest_NoRoom
	removeitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_RQ_ROUTE15
	msgbox Route15_Text_RQuest_Ok
	giveitem ITEM_RARE_CANDY, 1
	release
	end

Route15_EventScript_RQuest_Ask::
	msgbox Route15_Text_RQuest_Ask
	release
	end

Route15_EventScript_RQuest_Done::
	msgbox Route15_Text_RQuest_Done
	release
	end

Route15_EventScript_RQuest_NoRoom::
	msgbox Route15_Text_RQuest_NoRoom
	release
	end
