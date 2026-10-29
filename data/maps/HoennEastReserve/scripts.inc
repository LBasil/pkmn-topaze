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


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
HoennEastReserve_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HOENNE_0, HoennEastReserve_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SHOAL_SALT, 1
	goto_if_eq VAR_RESULT, FALSE, HoennEastReserve_EventScript_TopazeFind0_Full
	giveitem ITEM_SHOAL_SALT, 1
	setflag FLAG_TOPAZE_FIND_HOENNE_0
	release
	end

HoennEastReserve_EventScript_TopazeFind0_Done::
	release
	end

HoennEastReserve_EventScript_TopazeFind0_Full::
	msgbox HoennEastReserve_Text_TopazeFindFull
	release
	end

HoennEastReserve_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HOENNE_1, HoennEastReserve_EventScript_TopazeFind1_Done
	checkitemspace ITEM_SHOAL_SHELL, 1
	goto_if_eq VAR_RESULT, FALSE, HoennEastReserve_EventScript_TopazeFind1_Full
	giveitem ITEM_SHOAL_SHELL, 1
	setflag FLAG_TOPAZE_FIND_HOENNE_1
	release
	end

HoennEastReserve_EventScript_TopazeFind1_Done::
	release
	end

HoennEastReserve_EventScript_TopazeFind1_Full::
	msgbox HoennEastReserve_Text_TopazeFindFull
	release
	end

HoennEastReserve_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HOENNE_2, HoennEastReserve_EventScript_TopazeFind2_Done
	checkitemspace ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, HoennEastReserve_EventScript_TopazeFind2_Full
	giveitem ITEM_PEARL, 1
	setflag FLAG_TOPAZE_FIND_HOENNE_2
	release
	end

HoennEastReserve_EventScript_TopazeFind2_Done::
	release
	end

HoennEastReserve_EventScript_TopazeFind2_Full::
	msgbox HoennEastReserve_Text_TopazeFindFull
	release
	end

HoennEastReserve_EventScript_TopazeFind3::
	lock
	goto_if_set FLAG_TOPAZE_HID_SUP_HOENNEASTRESERVE, HoennEastReserve_EventScript_TopazeFind3_Done
	checkitemspace ITEM_SHOAL_SALT, 1
	goto_if_eq VAR_RESULT, FALSE, HoennEastReserve_EventScript_TopazeFind3_Full
	giveitem ITEM_SHOAL_SALT, 1
	setflag FLAG_TOPAZE_HID_SUP_HOENNEASTRESERVE
	release
	end

HoennEastReserve_EventScript_TopazeFind3_Done::
	release
	end

HoennEastReserve_EventScript_TopazeFind3_Full::
	msgbox HoennEastReserve_Text_TopazeFindFull
	release
	end


HoennEastReserve_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
