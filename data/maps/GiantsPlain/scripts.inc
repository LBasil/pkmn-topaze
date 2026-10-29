GiantsPlain_MapScripts::
	.byte 0

GiantsPlain_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox GiantsPlain_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GiantsPlain_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

GiantsPlain_EventScript_Stay::
	msgbox GiantsPlain_Text_Stay
	release
	end

GiantsPlain_EventScript_Npc0::
	msgbox GiantsPlain_Text_Npc0, MSGBOX_NPC
	end

GiantsPlain_EventScript_Npc1::
	msgbox GiantsPlain_Text_Npc1, MSGBOX_NPC
	end

GiantsPlain_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_GIANTSPLAIN, GiantsPlain_EventScript_Quest0_After
	msgbox GiantsPlain_Text_Quest0_Ask
	checkitem ITEM_SODA_POP, 2
	goto_if_eq VAR_RESULT, FALSE, GiantsPlain_EventScript_Quest0_Miss
	checkitemspace ITEM_BLACK_BELT, 1
	goto_if_eq VAR_RESULT, FALSE, GiantsPlain_EventScript_Quest0_NoRoom
	removeitem ITEM_SODA_POP, 2
	giveitem ITEM_BLACK_BELT, 1
	setflag FLAG_TOPAZE_QUEST_GIANTSPLAIN
	msgbox GiantsPlain_Text_Quest0_Done
	release
	end

GiantsPlain_EventScript_Quest0_After::
	msgbox GiantsPlain_Text_Quest0_AfterT
	release
	end

GiantsPlain_EventScript_Quest0_Miss::
	msgbox GiantsPlain_Text_Quest0_MissT
	release
	end

GiantsPlain_EventScript_Quest0_NoRoom::
	msgbox GiantsPlain_Text_Quest0_NoRoomT
	release
	end

GiantsPlain_EventScript_Gift0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_GIFT_GIANTSPLAIN, GiantsPlain_EventScript_Gift0_Done
	msgbox GiantsPlain_Text_Gift0_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GiantsPlain_EventScript_Gift0_No
	givemon SPECIES_PHANPY, 15
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_GIFT_GIANTSPLAIN
	msgbox GiantsPlain_Text_Gift0_Got
	release
	end

GiantsPlain_EventScript_Gift0_Done::
	msgbox GiantsPlain_Text_Gift0_After
	release
	end

GiantsPlain_EventScript_Gift0_No::
	msgbox GiantsPlain_Text_Gift0_Refuse
	release
	end

