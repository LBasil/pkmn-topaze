SaffronCity_HomeC_MapScripts::
	.byte 0

SaffronCity_HomeC_EventScript_Clerk::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_LOST_DONE, SaffronCity_HomeC_EventScript_Done
	checkitem ITEM_SCOPE_LENS, 1
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_HomeC_EventScript_Ask
	checkitem ITEM_KINGS_ROCK, 1
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_HomeC_EventScript_Ask
	checkitem ITEM_BLACK_GLASSES, 1
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_HomeC_EventScript_Ask
	checkitemspace ITEM_MAX_ELIXIR, 3
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_HomeC_EventScript_NoRoom
	removeitem ITEM_SCOPE_LENS, 1
	removeitem ITEM_KINGS_ROCK, 1
	removeitem ITEM_BLACK_GLASSES, 1
	setflag FLAG_TOPAZE_LOST_DONE
	msgbox SaffronCity_HomeC_Text_Thanks
	giveitem ITEM_MAX_ELIXIR, 3
	release
	end
SaffronCity_HomeC_EventScript_Ask::
	msgbox SaffronCity_HomeC_Text_Ask
	release
	end
SaffronCity_HomeC_EventScript_Done::
	msgbox SaffronCity_HomeC_Text_Done
	release
	end
SaffronCity_HomeC_EventScript_NoRoom::
	msgbox SaffronCity_HomeC_Text_NoRoom
	release
	end
