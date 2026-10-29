Route18_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route18_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Route18_OnWarp
	.byte 0

Route18_OnTransition::
	call_if_eq VAR_MAP_SCENE_ROUTE16, 1, Route18_OnTransitionCyclingRoad
	end

Route18_OnTransitionCyclingRoad::
	setflag FLAG_SYS_ON_CYCLING_ROAD
	return

Route18_OnWarp::
	map_script_2 VAR_MAP_SCENE_ROUTE16, 1, Route18_OnWarpCyclingRoad
	.2byte 0

Route18_OnWarpCyclingRoad::
	special ForcePlayerOntoBike
	end

Route18_EventScript_RouteSign::
	msgbox Route18_Text_RouteSign, MSGBOX_SIGN
	end

Route18_EventScript_CyclingRoadSign::
	msgbox Route18_Text_CyclingRoadSign, MSGBOX_SIGN
	end

@ Topaze: indice du temps deregle
Route18_EventScript_TimeHint::
	msgbox Route18_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: quete de route (THE ENDURANCE TEST)
Route18_EventScript_RQuest::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_RQ_ROUTE18, Route18_EventScript_RQuest_Done
	checkitem ITEM_MAX_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, Route18_EventScript_RQuest_Ask
	checkitemspace ITEM_PP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, Route18_EventScript_RQuest_NoRoom
	removeitem ITEM_MAX_POTION, 1
	setflag FLAG_TOPAZE_RQ_ROUTE18
	msgbox Route18_Text_RQuest_Ok
	giveitem ITEM_PP_UP, 1
	release
	end

Route18_EventScript_RQuest_Ask::
	msgbox Route18_Text_RQuest_Ask
	release
	end

Route18_EventScript_RQuest_Done::
	msgbox Route18_Text_RQuest_Done
	release
	end

Route18_EventScript_RQuest_NoRoom::
	msgbox Route18_Text_RQuest_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route18_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE18_0, Route18_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, Route18_EventScript_TopazeFind0_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_HID_ROUTE18_0
	release
	end

Route18_EventScript_TopazeFind0_Done::
	release
	end

Route18_EventScript_TopazeFind0_Full::
	msgbox Route18_Text_TopazeFindFull
	release
	end

Route18_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE18_1, Route18_EventScript_TopazeFind1_Done
	checkitemspace ITEM_STAR_PIECE, 1
	goto_if_eq VAR_RESULT, FALSE, Route18_EventScript_TopazeFind1_Full
	giveitem ITEM_STAR_PIECE, 1
	setflag FLAG_TOPAZE_HID_ROUTE18_1
	release
	end

Route18_EventScript_TopazeFind1_Done::
	release
	end

Route18_EventScript_TopazeFind1_Full::
	msgbox Route18_Text_TopazeFindFull
	release
	end


Route18_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
