BerryOrchard_MapScripts::
	.byte 0

BerryOrchard_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BerryOrchard_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BerryOrchard_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BerryOrchard_EventScript_Stay::
	msgbox BerryOrchard_Text_Stay
	release
	end

BerryOrchard_EventScript_Npc0::
	msgbox BerryOrchard_Text_Npc0, MSGBOX_NPC
	end

BerryOrchard_EventScript_Npc1::
	msgbox BerryOrchard_Text_Npc1, MSGBOX_NPC
	end

BerryOrchard_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_ORCHARD, BerryOrchard_EventScript_Quest0_After
	msgbox BerryOrchard_Text_Quest0_Ask
	checkitem ITEM_LUM_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_Quest0_Miss
	checkitemspace ITEM_WHITE_HERB, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_Quest0_NoRoom
	removeitem ITEM_LUM_BERRY, 1
	giveitem ITEM_WHITE_HERB, 1
	setflag FLAG_TOPAZE_QUEST_ORCHARD
	msgbox BerryOrchard_Text_Quest0_Done
	release
	end

BerryOrchard_EventScript_Quest0_After::
	msgbox BerryOrchard_Text_Quest0_AfterT
	release
	end

BerryOrchard_EventScript_Quest0_Miss::
	msgbox BerryOrchard_Text_Quest0_MissT
	release
	end

BerryOrchard_EventScript_Quest0_NoRoom::
	msgbox BerryOrchard_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
BerryOrchard_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_0, BerryOrchard_EventScript_TopazeFind0_Done
	checkitemspace ITEM_ORAN_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind0_Full
	giveitem ITEM_ORAN_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_0
	release
	end

BerryOrchard_EventScript_TopazeFind0_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind0_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end

BerryOrchard_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_1, BerryOrchard_EventScript_TopazeFind1_Done
	checkitemspace ITEM_PECHA_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind1_Full
	giveitem ITEM_PECHA_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_1
	release
	end

BerryOrchard_EventScript_TopazeFind1_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind1_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end

BerryOrchard_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_2, BerryOrchard_EventScript_TopazeFind2_Done
	checkitemspace ITEM_CHERI_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind2_Full
	giveitem ITEM_CHERI_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_2
	release
	end

BerryOrchard_EventScript_TopazeFind2_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind2_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end

BerryOrchard_EventScript_TopazeFind3::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_3, BerryOrchard_EventScript_TopazeFind3_Done
	checkitemspace ITEM_RAWST_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind3_Full
	giveitem ITEM_RAWST_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_3
	release
	end

BerryOrchard_EventScript_TopazeFind3_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind3_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end

BerryOrchard_EventScript_TopazeFind4::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_4, BerryOrchard_EventScript_TopazeFind4_Done
	checkitemspace ITEM_LUM_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind4_Full
	giveitem ITEM_LUM_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_4
	release
	end

BerryOrchard_EventScript_TopazeFind4_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind4_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end

BerryOrchard_EventScript_TopazeFind5::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_5, BerryOrchard_EventScript_TopazeFind5_Done
	checkitemspace ITEM_SITRUS_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind5_Full
	giveitem ITEM_SITRUS_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_5
	release
	end

BerryOrchard_EventScript_TopazeFind5_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind5_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end

BerryOrchard_EventScript_TopazeFind6::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_6, BerryOrchard_EventScript_TopazeFind6_Done
	checkitemspace ITEM_LEPPA_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind6_Full
	giveitem ITEM_LEPPA_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_6
	release
	end

BerryOrchard_EventScript_TopazeFind6_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind6_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end

BerryOrchard_EventScript_TopazeFind7::
	lock
	goto_if_set FLAG_TOPAZE_FIND_ORCHARD_7, BerryOrchard_EventScript_TopazeFind7_Done
	checkitemspace ITEM_PERSIM_BERRY, 1
	goto_if_eq VAR_RESULT, FALSE, BerryOrchard_EventScript_TopazeFind7_Full
	giveitem ITEM_PERSIM_BERRY, 1
	setflag FLAG_TOPAZE_FIND_ORCHARD_7
	release
	end

BerryOrchard_EventScript_TopazeFind7_Done::
	release
	end

BerryOrchard_EventScript_TopazeFind7_Full::
	msgbox BerryOrchard_Text_TopazeFindFull
	release
	end


BerryOrchard_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
