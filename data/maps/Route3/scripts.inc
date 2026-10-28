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
