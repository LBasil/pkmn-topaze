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

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route7_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE7_0, Route7_EventScript_TopazeFind0_Done
	checkitemspace ITEM_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, Route7_EventScript_TopazeFind0_Full
	giveitem ITEM_REVIVE, 1
	setflag FLAG_TOPAZE_HID_ROUTE7_0
	release
	end

Route7_EventScript_TopazeFind0_Done::
	release
	end

Route7_EventScript_TopazeFind0_Full::
	msgbox Route7_Text_TopazeFindFull
	release
	end

Route7_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE7_1, Route7_EventScript_TopazeFind1_Done
	checkitemspace ITEM_NUGGET, 1
	goto_if_eq VAR_RESULT, FALSE, Route7_EventScript_TopazeFind1_Full
	giveitem ITEM_NUGGET, 1
	setflag FLAG_TOPAZE_HID_ROUTE7_1
	release
	end

Route7_EventScript_TopazeFind1_Done::
	release
	end

Route7_EventScript_TopazeFind1_Full::
	msgbox Route7_Text_TopazeFindFull
	release
	end


Route7_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
