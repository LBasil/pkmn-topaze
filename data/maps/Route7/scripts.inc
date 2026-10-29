Route7_MapScripts::
	.byte 0

Route7_EventScript_UndergroundPathSign::
	msgbox Route7_Text_UndergroundPathSign, MSGBOX_SIGN
	end

@ Topaze: quete de route (PLAYING WITH FIRE)
Route7_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE7, Route7_EventScript_RQuest_Done
	checkitem ITEM_BURN_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, Route7_EventScript_RQuest_Ask
	checkitemspace ITEM_HYPER_POTION, 2
	goto_if_eq VAR_RESULT, FALSE, Route7_EventScript_RQuest_NoRoom
	removeitem ITEM_BURN_HEAL, 2
	setflag FLAG_TOPAZE_RQ_ROUTE7
	msgbox Route7_Text_RQuest_Ok
	giveitem ITEM_HYPER_POTION, 2
	release
	end

Route7_EventScript_RQuest_Ask::
	msgbox Route7_Text_RQuest_Ask
	release
	end

Route7_EventScript_RQuest_Done::
	msgbox Route7_Text_RQuest_Done
	release
	end

Route7_EventScript_RQuest_NoRoom::
	msgbox Route7_Text_RQuest_NoRoom
	release
	end
