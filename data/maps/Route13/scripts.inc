Route13_MapScripts::
	.byte 0

Route13_EventScript_TrainerTips1::
	msgbox Route13_Text_LookToLeftOfThatPost, MSGBOX_SIGN
	end

Route13_EventScript_TrainerTips2::
	msgbox Route13_Text_SelectToSwitchItems, MSGBOX_SIGN
	end

Route13_EventScript_RouteSign::
	msgbox Route13_Text_RouteSign, MSGBOX_SIGN
	end

@ Topaze: mini-quete 4 (THE ANGLER)
Route13_EventScript_Quest4::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_4, Route13_EventScript_Quest4_Done
	checkitem ITEM_ETHER, 2
	goto_if_eq VAR_RESULT, FALSE, Route13_EventScript_Quest4_Ask
	checkitemspace ITEM_IRON, 1
	goto_if_eq VAR_RESULT, FALSE, Route13_EventScript_Quest4_NoRoom
	removeitem ITEM_ETHER, 2
	setflag FLAG_TOPAZE_QUEST_4
	msgbox Route13_Text_Quest4_Ok
	giveitem ITEM_IRON, 1
	release
	end

Route13_EventScript_Quest4_Ask::
	msgbox Route13_Text_Quest4_Ask
	release
	end

Route13_EventScript_Quest4_Done::
	msgbox Route13_Text_Quest4_Done
	release
	end

Route13_EventScript_Quest4_NoRoom::
	msgbox Route13_Text_Quest4_NoRoom
	release
	end
