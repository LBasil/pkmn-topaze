Route9_MapScripts::
	.byte 0

Route9_EventScript_RouteSign::
	msgbox Route9_Text_RouteSign, MSGBOX_SIGN
	end

@ Topaze: mini-quete 3 (NO MORE BUGS)
Route9_EventScript_Quest3::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_3, Route9_EventScript_Quest3_Done
	checkitem ITEM_REPEL, 3
	goto_if_eq VAR_RESULT, FALSE, Route9_EventScript_Quest3_Ask
	checkitemspace ITEM_PROTEIN, 1
	goto_if_eq VAR_RESULT, FALSE, Route9_EventScript_Quest3_NoRoom
	removeitem ITEM_REPEL, 3
	setflag FLAG_TOPAZE_QUEST_3
	msgbox Route9_Text_Quest3_Ok
	giveitem ITEM_PROTEIN, 1
	release
	end

Route9_EventScript_Quest3_Ask::
	msgbox Route9_Text_Quest3_Ask
	release
	end

Route9_EventScript_Quest3_Done::
	msgbox Route9_Text_Quest3_Done
	release
	end

Route9_EventScript_Quest3_NoRoom::
	msgbox Route9_Text_Quest3_NoRoom
	release
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route9_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE9_0, Route9_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_REPEL, 1
	goto_if_eq VAR_RESULT, FALSE, Route9_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_REPEL, 1
	setflag FLAG_TOPAZE_HID_ROUTE9_0
	release
	end

Route9_EventScript_TopazeFind0_Done::
	release
	end

Route9_EventScript_TopazeFind0_Full::
	msgbox Route9_Text_TopazeFindFull
	release
	end

Route9_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE9_1, Route9_EventScript_TopazeFind1_Done
	checkitemspace ITEM_PP_UP, 1
	goto_if_eq VAR_RESULT, FALSE, Route9_EventScript_TopazeFind1_Full
	giveitem ITEM_PP_UP, 1
	setflag FLAG_TOPAZE_HID_ROUTE9_1
	release
	end

Route9_EventScript_TopazeFind1_Done::
	release
	end

Route9_EventScript_TopazeFind1_Full::
	msgbox Route9_Text_TopazeFindFull
	release
	end


Route9_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
