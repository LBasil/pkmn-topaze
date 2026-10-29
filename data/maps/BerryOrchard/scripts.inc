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

