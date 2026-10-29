Route11_MapScripts::
	.byte 0

Route11_EventScript_DiglettsCaveSign::
	msgbox Route11_Text_DiglettsCave, MSGBOX_SIGN
	end

@ Topaze: indice du temps deregle
Route11_EventScript_TimeHint::
	setflag FLAG_TOPAZE_CLOCK_2
	msgbox Route11_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: quete de route (COLD CATCH)
Route11_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE11, Route11_EventScript_RQuest_Done
	checkitem ITEM_ICE_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, Route11_EventScript_RQuest_Ask
	checkitemspace ITEM_GREAT_BALL, 5
	goto_if_eq VAR_RESULT, FALSE, Route11_EventScript_RQuest_NoRoom
	removeitem ITEM_ICE_HEAL, 2
	setflag FLAG_TOPAZE_RQ_ROUTE11
	msgbox Route11_Text_RQuest_Ok
	giveitem ITEM_GREAT_BALL, 5
	release
	end

Route11_EventScript_RQuest_Ask::
	msgbox Route11_Text_RQuest_Ask
	release
	end

Route11_EventScript_RQuest_Done::
	msgbox Route11_Text_RQuest_Done
	release
	end

Route11_EventScript_RQuest_NoRoom::
	msgbox Route11_Text_RQuest_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route11_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE11_0, Route11_EventScript_TopazeFind0_Done
	checkitemspace ITEM_HYPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, Route11_EventScript_TopazeFind0_Full
	giveitem ITEM_HYPER_POTION, 1
	setflag FLAG_TOPAZE_HID_ROUTE11_0
	release
	end

Route11_EventScript_TopazeFind0_Done::
	release
	end

Route11_EventScript_TopazeFind0_Full::
	msgbox Route11_Text_TopazeFindFull
	release
	end

Route11_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE11_1, Route11_EventScript_TopazeFind1_Done
	checkitemspace ITEM_NUGGET, 1
	goto_if_eq VAR_RESULT, FALSE, Route11_EventScript_TopazeFind1_Full
	giveitem ITEM_NUGGET, 1
	setflag FLAG_TOPAZE_HID_ROUTE11_1
	release
	end

Route11_EventScript_TopazeFind1_Done::
	release
	end

Route11_EventScript_TopazeFind1_Full::
	msgbox Route11_Text_TopazeFindFull
	release
	end


Route11_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
