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
