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


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
HoennWestReserve_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HOENNW_0, HoennWestReserve_EventScript_TopazeFind0_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_TopazeFind0_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_FIND_HOENNW_0
	release
	end

HoennWestReserve_EventScript_TopazeFind0_Done::
	release
	end

HoennWestReserve_EventScript_TopazeFind0_Full::
	msgbox HoennWestReserve_Text_TopazeFindFull
	release
	end

HoennWestReserve_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HOENNW_1, HoennWestReserve_EventScript_TopazeFind1_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_TopazeFind1_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_FIND_HOENNW_1
	release
	end

HoennWestReserve_EventScript_TopazeFind1_Done::
	release
	end

HoennWestReserve_EventScript_TopazeFind1_Full::
	msgbox HoennWestReserve_Text_TopazeFindFull
	release
	end

HoennWestReserve_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HOENNW_2, HoennWestReserve_EventScript_TopazeFind2_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_TopazeFind2_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_FIND_HOENNW_2
	release
	end

HoennWestReserve_EventScript_TopazeFind2_Done::
	release
	end

HoennWestReserve_EventScript_TopazeFind2_Full::
	msgbox HoennWestReserve_Text_TopazeFindFull
	release
	end

HoennWestReserve_EventScript_TopazeFind3::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HOENNW_3, HoennWestReserve_EventScript_TopazeFind3_Done
	checkitemspace ITEM_TINY_MUSHROOM, 1
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_TopazeFind3_Full
	giveitem ITEM_TINY_MUSHROOM, 1
	setflag FLAG_TOPAZE_FIND_HOENNW_3
	release
	end

HoennWestReserve_EventScript_TopazeFind3_Done::
	release
	end

HoennWestReserve_EventScript_TopazeFind3_Full::
	msgbox HoennWestReserve_Text_TopazeFindFull
	release
	end

HoennWestReserve_EventScript_TopazeFind4::
	lock
	goto_if_set FLAG_TOPAZE_HID_SUP_HOENNWESTRESERVE, HoennWestReserve_EventScript_TopazeFind4_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_TopazeFind4_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_HID_SUP_HOENNWESTRESERVE
	release
	end

HoennWestReserve_EventScript_TopazeFind4_Done::
	release
	end

HoennWestReserve_EventScript_TopazeFind4_Full::
	msgbox HoennWestReserve_Text_TopazeFindFull
	release
	end

HoennWestReserve_EventScript_TopazeFind5::
	lock
	goto_if_set FLAG_TOPAZE_HID_SUP_HOENNWESTRESERVE, HoennWestReserve_EventScript_TopazeFind5_Done
	checkitemspace ITEM_HEART_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, HoennWestReserve_EventScript_TopazeFind5_Full
	giveitem ITEM_HEART_SCALE, 1
	setflag FLAG_TOPAZE_HID_SUP_HOENNWESTRESERVE
	release
	end

HoennWestReserve_EventScript_TopazeFind5_Done::
	release
	end

HoennWestReserve_EventScript_TopazeFind5_Full::
	msgbox HoennWestReserve_Text_TopazeFindFull
	release
	end


HoennWestReserve_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
