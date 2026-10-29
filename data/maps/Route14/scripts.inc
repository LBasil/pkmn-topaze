Route14_MapScripts::
	.byte 0

Route14_EventScript_RouteSign::
	msgbox Route14_Text_RouteSign, MSGBOX_SIGN
	end

@ Topaze: quete de route (ENGINE TROUBLE)
Route14_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE14, Route14_EventScript_RQuest_Done
	checkitem ITEM_FULL_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, Route14_EventScript_RQuest_Ask
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, Route14_EventScript_RQuest_NoRoom
	removeitem ITEM_FULL_HEAL, 2
	setflag FLAG_TOPAZE_RQ_ROUTE14
	msgbox Route14_Text_RQuest_Ok
	giveitem ITEM_MAX_REVIVE, 1
	release
	end

Route14_EventScript_RQuest_Ask::
	msgbox Route14_Text_RQuest_Ask
	release
	end

Route14_EventScript_RQuest_Done::
	msgbox Route14_Text_RQuest_Done
	release
	end

Route14_EventScript_RQuest_NoRoom::
	msgbox Route14_Text_RQuest_NoRoom
	release
	end
