SunriseMeadow_MapScripts::
	.byte 0

SunriseMeadow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SunriseMeadow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SunriseMeadow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SunriseMeadow_EventScript_Stay::
	msgbox SunriseMeadow_Text_Stay
	release
	end

SunriseMeadow_EventScript_Npc0::
	msgbox SunriseMeadow_Text_Npc0, MSGBOX_NPC
	end

SunriseMeadow_EventScript_Npc1::
	msgbox SunriseMeadow_Text_Npc1, MSGBOX_NPC
	end

SunriseMeadow_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_JOHTO, SunriseMeadow_EventScript_Quest0_After
	msgbox SunriseMeadow_Text_Quest0_Ask
	checkitem ITEM_STAR_PIECE, 1
	goto_if_eq VAR_RESULT, FALSE, SunriseMeadow_EventScript_Quest0_Miss
	checkitemspace ITEM_LUCKY_EGG, 1
	goto_if_eq VAR_RESULT, FALSE, SunriseMeadow_EventScript_Quest0_NoRoom
	removeitem ITEM_STAR_PIECE, 1
	giveitem ITEM_LUCKY_EGG, 1
	setflag FLAG_TOPAZE_QUEST_JOHTO
	msgbox SunriseMeadow_Text_Quest0_Done
	release
	end

SunriseMeadow_EventScript_Quest0_After::
	msgbox SunriseMeadow_Text_Quest0_AfterT
	release
	end

SunriseMeadow_EventScript_Quest0_Miss::
	msgbox SunriseMeadow_Text_Quest0_MissT
	release
	end

SunriseMeadow_EventScript_Quest0_NoRoom::
	msgbox SunriseMeadow_Text_Quest0_NoRoomT
	release
	end

SunriseMeadow_EventScript_Gift0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_GIFT_JOHTO, SunriseMeadow_EventScript_Gift0_Done
	msgbox SunriseMeadow_Text_Gift0_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SunriseMeadow_EventScript_Gift0_No
	givemon SPECIES_TOGEPI, 5
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_GIFT_JOHTO
	msgbox SunriseMeadow_Text_Gift0_Got
	release
	end

SunriseMeadow_EventScript_Gift0_Done::
	msgbox SunriseMeadow_Text_Gift0_After
	release
	end

SunriseMeadow_EventScript_Gift0_No::
	msgbox SunriseMeadow_Text_Gift0_Refuse
	release
	end

