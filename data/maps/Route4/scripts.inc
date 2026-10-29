Route4_MapScripts::
	.byte 0

Route4_EventScript_Unused::
	end

Route4_EventScript_Woman::
	msgbox Route4_Text_TrippedOverGeodude, MSGBOX_NPC
	end

Route4_EventScript_MtMoonSign::
	msgbox Route4_Text_MtMoonEntrance, MSGBOX_SIGN
	end

Route4_EventScript_RouteSign::
	msgbox Route4_Text_RouteSign, MSGBOX_SIGN
	end

@ Topaze: quete de route (LOST IN THE CAVE)
Route4_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE4, Route4_EventScript_RQuest_Done
	checkitem ITEM_ESCAPE_ROPE, 1
	goto_if_eq VAR_RESULT, FALSE, Route4_EventScript_RQuest_Ask
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, Route4_EventScript_RQuest_NoRoom
	removeitem ITEM_ESCAPE_ROPE, 1
	setflag FLAG_TOPAZE_RQ_ROUTE4
	msgbox Route4_Text_RQuest_Ok
	giveitem ITEM_REVIVE, 1
	release
	end

Route4_EventScript_RQuest_Ask::
	msgbox Route4_Text_RQuest_Ask
	release
	end

Route4_EventScript_RQuest_Done::
	msgbox Route4_Text_RQuest_Done
	release
	end

Route4_EventScript_RQuest_NoRoom::
	msgbox Route4_Text_RQuest_NoRoom
	release
	end
