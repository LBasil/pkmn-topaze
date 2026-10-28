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
