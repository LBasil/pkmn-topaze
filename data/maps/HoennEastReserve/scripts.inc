HoennEastReserve_MapScripts::
	.byte 0

HoennEastReserve_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox HoennEastReserve_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HoennEastReserve_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

HoennEastReserve_EventScript_Stay::
	msgbox HoennEastReserve_Text_Stay
	release
	end

HoennEastReserve_EventScript_Npc0::
	msgbox HoennEastReserve_Text_Npc0, MSGBOX_NPC
	end

HoennEastReserve_EventScript_Npc1::
	msgbox HoennEastReserve_Text_Npc1, MSGBOX_NPC
	end

HoennEastReserve_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_HOENNE, HoennEastReserve_EventScript_Quest0_After
	msgbox HoennEastReserve_Text_Quest0_Ask
	checkitem ITEM_SHOAL_SALT, 1
	goto_if_eq VAR_RESULT, FALSE, HoennEastReserve_EventScript_Quest0_Miss
	checkitemspace ITEM_BIG_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, HoennEastReserve_EventScript_Quest0_NoRoom
	removeitem ITEM_SHOAL_SALT, 1
	giveitem ITEM_BIG_PEARL, 1
	setflag FLAG_TOPAZE_QUEST_HOENNE
	msgbox HoennEastReserve_Text_Quest0_Done
	release
	end

HoennEastReserve_EventScript_Quest0_After::
	msgbox HoennEastReserve_Text_Quest0_AfterT
	release
	end

HoennEastReserve_EventScript_Quest0_Miss::
	msgbox HoennEastReserve_Text_Quest0_MissT
	release
	end

HoennEastReserve_EventScript_Quest0_NoRoom::
	msgbox HoennEastReserve_Text_Quest0_NoRoomT
	release
	end

