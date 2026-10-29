Route17_MapScripts::
	.byte 0

Route17_EventScript_ItemsNotice::
	msgbox Route17_Text_WatchOutForDiscardedItems, MSGBOX_SIGN
	end

Route17_EventScript_TrainerTips1::
	msgbox Route17_Text_SameSpeciesGrowDifferentRates, MSGBOX_SIGN
	end

Route17_EventScript_TrainerTips2::
	msgbox Route17_Text_PressBToStayInPlace, MSGBOX_SIGN
	end

Route17_EventScript_RouteSign::
	msgbox Route17_Text_RouteSign, MSGBOX_SIGN
	end

Route17_EventScript_BallsNotice::
	msgbox Route17_Text_DontThrowGameThrowBalls, MSGBOX_SIGN
	end

Route17_EventScript_CyclingRoadSign::
	msgbox Route17_Text_CyclingRoadSign, MSGBOX_SIGN
	end

@ Topaze: mini-quete 5 (THE COLLECTOR)
Route17_EventScript_Quest5::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_5, Route17_EventScript_Quest5_Done
	checkitem ITEM_FIRE_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, Route17_EventScript_Quest5_Ask
	checkitemspace ITEM_CALCIUM, 1
	goto_if_eq VAR_RESULT, FALSE, Route17_EventScript_Quest5_NoRoom
	removeitem ITEM_FIRE_STONE, 1
	setflag FLAG_TOPAZE_QUEST_5
	msgbox Route17_Text_Quest5_Ok
	giveitem ITEM_CALCIUM, 1
	release
	end

Route17_EventScript_Quest5_Ask::
	msgbox Route17_Text_Quest5_Ask
	release
	end

Route17_EventScript_Quest5_Done::
	msgbox Route17_Text_Quest5_Done
	release
	end

Route17_EventScript_Quest5_NoRoom::
	msgbox Route17_Text_Quest5_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route17_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE17_0, Route17_EventScript_TopazeFind0_Done
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, Route17_EventScript_TopazeFind0_Full
	giveitem ITEM_RARE_CANDY, 1
	setflag FLAG_TOPAZE_HID_ROUTE17_0
	release
	end

Route17_EventScript_TopazeFind0_Done::
	release
	end

Route17_EventScript_TopazeFind0_Full::
	msgbox Route17_Text_TopazeFindFull
	release
	end

Route17_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE17_1, Route17_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, Route17_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_POTION, 1
	setflag FLAG_TOPAZE_HID_ROUTE17_1
	release
	end

Route17_EventScript_TopazeFind1_Done::
	release
	end

Route17_EventScript_TopazeFind1_Full::
	msgbox Route17_Text_TopazeFindFull
	release
	end


Route17_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
