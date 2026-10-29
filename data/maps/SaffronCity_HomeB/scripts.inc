SaffronCity_HomeB_MapScripts::
	.byte 0

SaffronCity_HomeB_EventScript_Clerk::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_LETTER, SaffronCity_HomeB_EventScript_Done
	goto_if_unset FLAG_TOPAZE_CLOCK_1, SaffronCity_HomeB_EventScript_None
	goto_if_unset FLAG_TOPAZE_CLOCK_2, SaffronCity_HomeB_EventScript_None
	goto_if_unset FLAG_TOPAZE_CLOCK_3, SaffronCity_HomeB_EventScript_None
	checkitemspace ITEM_MAX_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_HomeB_EventScript_NoRoom
	msgbox SaffronCity_HomeB_Text_Letter
	setflag FLAG_TOPAZE_LETTER
	giveitem ITEM_MAX_ELIXIR, 1
	msgbox SaffronCity_HomeB_Text_Read
	release
	end
SaffronCity_HomeB_EventScript_None::
	msgbox SaffronCity_HomeB_Text_None
	release
	end
SaffronCity_HomeB_EventScript_Done::
	msgbox SaffronCity_HomeB_Text_Done
	release
	end
SaffronCity_HomeB_EventScript_NoRoom::
	msgbox SaffronCity_HomeB_Text_NoRoom
	release
	end
