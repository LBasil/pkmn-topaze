HoennWestReserve_MapScripts::
	.byte 0

HoennWestReserve_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox HoennWestReserve_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HoennWestReserve_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

HoennWestReserve_EventScript_Stay::
	msgbox HoennWestReserve_Text_Stay
	release
	end

HoennWestReserve_EventScript_Npc0::
	msgbox HoennWestReserve_Text_Npc0, MSGBOX_NPC
	end

HoennWestReserve_EventScript_Npc1::
	msgbox HoennWestReserve_Text_Npc1, MSGBOX_NPC
	end

HoennWestReserve_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_HOENNW, HoennWestReserve_EventScript_Quest0_After
	msgbox HoennWestReserve_Text_Quest0_Ask
	checkitem ITEM_HEART_SCALE, 2
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_Quest0_Miss
	checkitemspace ITEM_SOOTHE_BELL, 1
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_Quest0_NoRoom
	removeitem ITEM_HEART_SCALE, 2
	giveitem ITEM_SOOTHE_BELL, 1
	setflag FLAG_TOPAZE_QUEST_HOENNW
	msgbox HoennWestReserve_Text_Quest0_Done
	release
	end

HoennWestReserve_EventScript_Quest0_After::
	msgbox HoennWestReserve_Text_Quest0_AfterT
	release
	end

HoennWestReserve_EventScript_Quest0_Miss::
	msgbox HoennWestReserve_Text_Quest0_MissT
	release
	end

HoennWestReserve_EventScript_Quest0_NoRoom::
	msgbox HoennWestReserve_Text_Quest0_NoRoomT
	release
	end

