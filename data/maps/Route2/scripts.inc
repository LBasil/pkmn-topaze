Route2_MapScripts::
	.byte 0

Route2_EventScript_RouteSign::
	msgbox Route2_Text_RouteSign, MSGBOX_SIGN
	end

Route2_EventScript_ForestSign::
	msgbox Route2_Text_ForestSign, MSGBOX_SIGN
	end

Route2_EventScript_Hiker::
	msgbox Route2_Text_Hiker, MSGBOX_NPC
	end

Route2_EventScript_Miner::
	msgbox Route2_Text_Miner, MSGBOX_NPC
	end

@ Topaze: mini-quete 1 (BUG BITES)
Route2_EventScript_Quest1::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_1, Route2_EventScript_Quest1_Done
	checkitem ITEM_ANTIDOTE, 3
	goto_if_eq VAR_RESULT, FALSE, Route2_EventScript_Quest1_Ask
	checkitemspace ITEM_PP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, Route2_EventScript_Quest1_NoRoom
	removeitem ITEM_ANTIDOTE, 3
	setflag FLAG_TOPAZE_QUEST_1
	msgbox Route2_Text_Quest1_Ok
	giveitem ITEM_PP_UP, 1
	release
	end

Route2_EventScript_Quest1_Ask::
	msgbox Route2_Text_Quest1_Ask
	release
	end

Route2_EventScript_Quest1_Done::
	msgbox Route2_Text_Quest1_Done
	release
	end

Route2_EventScript_Quest1_NoRoom::
	msgbox Route2_Text_Quest1_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route2_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE2_0, Route2_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, Route2_EventScript_TopazeFind0_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_HID_ROUTE2_0
	release
	end

Route2_EventScript_TopazeFind0_Done::
	release
	end

Route2_EventScript_TopazeFind0_Full::
	msgbox Route2_Text_TopazeFindFull
	release
	end

Route2_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE2_1, Route2_EventScript_TopazeFind1_Done
	checkitemspace ITEM_GREAT_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, Route2_EventScript_TopazeFind1_Full
	giveitem ITEM_GREAT_BALL, 1
	setflag FLAG_TOPAZE_HID_ROUTE2_1
	release
	end

Route2_EventScript_TopazeFind1_Done::
	release
	end

Route2_EventScript_TopazeFind1_Full::
	msgbox Route2_Text_TopazeFindFull
	release
	end


Route2_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
