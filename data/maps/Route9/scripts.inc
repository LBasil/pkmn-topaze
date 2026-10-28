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
