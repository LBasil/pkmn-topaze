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
