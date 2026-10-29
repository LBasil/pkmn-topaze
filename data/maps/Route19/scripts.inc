Route19_MapScripts::
	.byte 0

Route19_EventScript_RouteSign::
	msgbox Route19_Text_RouteSign, MSGBOX_SIGN
	end

@ Topaze: indice du temps deregle
Route19_EventScript_TimeHint::
	msgbox Route19_Text_TimeHint, MSGBOX_SIGN
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
Route19_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_ROUTE19_0, Route19_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, Route19_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_HID_ROUTE19_0
	release
	end

Route19_EventScript_TopazeFind0_Done::
	release
	end

Route19_EventScript_TopazeFind0_Full::
	msgbox Route19_Text_TopazeFindFull
	release
	end


Route19_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
