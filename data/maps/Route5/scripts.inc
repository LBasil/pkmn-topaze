Route5_MapScripts::
	.byte 0

Route5_EventScript_UndergroundPathSign::
	msgbox Route5_Text_UndergroundPathSign, MSGBOX_SIGN
	end

@ Topaze: mini-quete 2 (LOST HEIRLOOM)
Route5_EventScript_Quest2::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_2, Route5_EventScript_Quest2_Done
	checkitem ITEM_REVIVE, 2
	goto_if_eq VAR_RESULT, FALSE, Route5_EventScript_Quest2_Ask
	checkitemspace ITEM_HP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, Route5_EventScript_Quest2_NoRoom
	removeitem ITEM_REVIVE, 2
	setflag FLAG_TOPAZE_QUEST_2
	msgbox Route5_Text_Quest2_Ok
	giveitem ITEM_HP_UP, 1
	release
	end

Route5_EventScript_Quest2_Ask::
	msgbox Route5_Text_Quest2_Ask
	release
	end

Route5_EventScript_Quest2_Done::
	msgbox Route5_Text_Quest2_Done
	release
	end

Route5_EventScript_Quest2_NoRoom::
	msgbox Route5_Text_Quest2_NoRoom
	release
	end
