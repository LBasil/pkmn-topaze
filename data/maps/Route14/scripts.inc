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

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route14_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE14_0, Route14_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, Route14_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_HID_ROUTE14_0
	release
	end

Route14_EventScript_TopazeFind0_Done::
	release
	end

Route14_EventScript_TopazeFind0_Full::
	msgbox Route14_Text_TopazeFindFull
	release
	end

Route14_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE14_1, Route14_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, Route14_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_ROUTE14_1
	release
	end

Route14_EventScript_TopazeFind1_Done::
	release
	end

Route14_EventScript_TopazeFind1_Full::
	msgbox Route14_Text_TopazeFindFull
	release
	end


Route14_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
