Route10_MapScripts::
	.byte 0

Route10_EventScript_Unused::
	end

Route10_EventScript_NorthRockTunnelSign::
	msgbox Route10_Text_RockTunnelDetourToLavender, MSGBOX_SIGN
	end

Route10_EventScript_SouthRockTunnelSign::
	msgbox Route10_Text_RockTunnel, MSGBOX_SIGN
	end

Route10_EventScript_PowerPlantSign::
	msgbox Route10_Text_PowerPlant, MSGBOX_SIGN
	end

@ Topaze: PROCHE EDOUARD (optionnel, fort)
Route10_EventScript_ProcheEdouard::
	lock
	faceplayer
	goto_if_unset FLAG_TOPAZE_POSTGAME, Route10_EventScript_ProcheEdouard_TooEarly
	goto_if_defeated TRAINER_PROCHE_EDOUARD, Route10_EventScript_ProcheEdouard_After
	msgbox Route10_Text_ProcheEdouard_Intro
	checkitemspace ITEM_HARD_STONE
	goto_if_eq VAR_RESULT, FALSE, Route10_EventScript_ProcheEdouard_NoRoom
	trainerbattle_no_intro TRAINER_PROCHE_EDOUARD, Route10_Text_ProcheEdouard_Defeat
	msgbox Route10_Text_ProcheEdouard_Win
	giveitem ITEM_HARD_STONE
	msgbox Route10_Text_ProcheEdouard_After
	release
	end

Route10_EventScript_ProcheEdouard_After::
	msgbox Route10_Text_ProcheEdouard_After
	release
	end

Route10_EventScript_ProcheEdouard_TooEarly::
	msgbox Route10_Text_ProcheEdouard_Early
	release
	end

Route10_EventScript_ProcheEdouard_NoRoom::
	msgbox Route10_Text_ProcheEdouard_NoRoom
	release
	end

@ Topaze: quete de route (THE FIELD RESEARCH)
Route10_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE10, Route10_EventScript_RQuest_Done
	checkitem ITEM_HYPER_POTION, 2
	goto_if_eq VAR_RESULT, FALSE, Route10_EventScript_RQuest_Ask
	checkitemspace ITEM_MAX_REPEL, 2
	goto_if_eq VAR_RESULT, FALSE, Route10_EventScript_RQuest_NoRoom
	removeitem ITEM_HYPER_POTION, 2
	setflag FLAG_TOPAZE_RQ_ROUTE10
	msgbox Route10_Text_RQuest_Ok
	giveitem ITEM_MAX_REPEL, 2
	release
	end

Route10_EventScript_RQuest_Ask::
	msgbox Route10_Text_RQuest_Ask
	release
	end

Route10_EventScript_RQuest_Done::
	msgbox Route10_Text_RQuest_Done
	release
	end

Route10_EventScript_RQuest_NoRoom::
	msgbox Route10_Text_RQuest_NoRoom
	release
	end
