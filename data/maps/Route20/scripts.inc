Route20_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route20_OnTransition
	.byte 0

Route20_OnTransition::
	call_if_set FLAG_CHRONDROLIA_RAID_DONE, Route20_EventScript_SeaOpen
	call_if_unset FLAG_STOPPED_SEAFOAM_B3F_CURRENT, Route20_EventScript_ResetSeafoamBouldersForB3F
	call_if_unset FLAG_STOPPED_SEAFOAM_B4F_CURRENT, Route20_EventScript_ResetSeafoamBouldersForB4F
	end

Route20_EventScript_ResetSeafoamBouldersForB3F::
	clearflag FLAG_HIDE_SEAFOAM_1F_BOULDER_1
	clearflag FLAG_HIDE_SEAFOAM_1F_BOULDER_2
	setflag FLAG_HIDE_SEAFOAM_B1F_BOULDER_1
	setflag FLAG_HIDE_SEAFOAM_B1F_BOULDER_2
	setflag FLAG_HIDE_SEAFOAM_B2F_BOULDER_1
	setflag FLAG_HIDE_SEAFOAM_B2F_BOULDER_2
	setflag FLAG_HIDE_SEAFOAM_B3F_BOULDER_1
	setflag FLAG_HIDE_SEAFOAM_B3F_BOULDER_2
	return

Route20_EventScript_ResetSeafoamBouldersForB4F::
	clearflag FLAG_HIDE_SEAFOAM_B3F_BOULDER_3
	clearflag FLAG_HIDE_SEAFOAM_B3F_BOULDER_4
	clearflag FLAG_HIDE_SEAFOAM_B3F_BOULDER_5
	clearflag FLAG_HIDE_SEAFOAM_B3F_BOULDER_6
	setflag FLAG_HIDE_SEAFOAM_B4F_BOULDER_1
	setflag FLAG_HIDE_SEAFOAM_B4F_BOULDER_2
	return

Route20_EventScript_SeafoamIslandsSign::
	msgbox Route20_Text_SeafoamIslands, MSGBOX_SIGN
	end

Route20_EventScript_SeaClosed::
	lockall
	msgbox Route20_Text_SeaClosed
	closemessage
	applymovement LOCALID_PLAYER, Route20_Movement_StepLeft
	waitmovement 0
	releaseall
	end

Route20_EventScript_CaveClosed::
	lockall
	msgbox Route20_Text_CaveClosed
	closemessage
	applymovement LOCALID_PLAYER, Route20_Movement_StepDown
	waitmovement 0
	releaseall
	end

Route20_Movement_StepLeft::
	walk_left
	step_end

Route20_Movement_StepDown::
	walk_down
	step_end

Route20_EventScript_SeaOpen::
	setvar VAR_TEMP_1, 1
	return

@ Topaze: mini-quete 6 (SEA MARATHON)
Route20_EventScript_Quest6::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_6, Route20_EventScript_Quest6_Done
	checkitem ITEM_ELIXIR, 2
	goto_if_eq VAR_RESULT, FALSE, Route20_EventScript_Quest6_Ask
	checkitemspace ITEM_CARBOS, 1
	goto_if_eq VAR_RESULT, FALSE, Route20_EventScript_Quest6_NoRoom
	removeitem ITEM_ELIXIR, 2
	setflag FLAG_TOPAZE_QUEST_6
	msgbox Route20_Text_Quest6_Ok
	giveitem ITEM_CARBOS, 1
	release
	end

Route20_EventScript_Quest6_Ask::
	msgbox Route20_Text_Quest6_Ask
	release
	end

Route20_EventScript_Quest6_Done::
	msgbox Route20_Text_Quest6_Done
	release
	end

Route20_EventScript_Quest6_NoRoom::
	msgbox Route20_Text_Quest6_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route20_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE20_0, Route20_EventScript_TopazeFind0_Done
	checkitemspace ITEM_PP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, Route20_EventScript_TopazeFind0_Full
	giveitem ITEM_PP_UP, 1
	setflag FLAG_TOPAZE_HID_ROUTE20_0
	release
	end

Route20_EventScript_TopazeFind0_Done::
	release
	end

Route20_EventScript_TopazeFind0_Full::
	msgbox Route20_Text_TopazeFindFull
	release
	end

Route20_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE20_1, Route20_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, Route20_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_ROUTE20_1
	release
	end

Route20_EventScript_TopazeFind1_Done::
	release
	end

Route20_EventScript_TopazeFind1_Full::
	msgbox Route20_Text_TopazeFindFull
	release
	end


Route20_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
