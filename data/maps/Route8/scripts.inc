Route8_MapScripts::
	.byte 0

Route8_EventScript_UndergroundPathSign::
	msgbox Route8_Text_UndergroundPathSign, MSGBOX_SIGN
	end

Route8_EventScript_MonSpearow::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_SPEAROW, CRY_MODE_NORMAL
	msgbox Route8_Text_MonSpearow
	waitmoncry
	release
	end

Route8_EventScript_MonMeowth::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEOWTH, CRY_MODE_NORMAL
	msgbox Route8_Text_MonMeowth
	waitmoncry
	release
	end

@ Topaze: indice du temps deregle
Route8_EventScript_TimeHint::
	msgbox Route8_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: ECHO, le rival du passe
Route8_EventScript_EchoRival::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE04_GET, Route8_EventScript_EchoRival_Early
	goto_if_defeated TRAINER_ECHO_RIVAL, Route8_EventScript_EchoRival_After
	msgbox Route8_Text_Echo_Intro
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, Route8_EventScript_EchoRival_NoRoom
	trainerbattle_no_intro TRAINER_ECHO_RIVAL, Route8_Text_Echo_Defeat
	msgbox Route8_Text_Echo_Win
	giveitem ITEM_RARE_CANDY, 3
	msgbox Route8_Text_Echo_After
	release
	end

Route8_EventScript_EchoRival_After::
	msgbox Route8_Text_Echo_After
	release
	end

Route8_EventScript_EchoRival_Early::
	msgbox Route8_Text_Echo_Early
	release
	end

Route8_EventScript_EchoRival_NoRoom::
	msgbox Route8_Text_Echo_NoRoom
	release
	end
