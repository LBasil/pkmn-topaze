FossilDig_MapScripts::
	.byte 0

FossilDig_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox FossilDig_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FossilDig_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

FossilDig_EventScript_Stay::
	msgbox FossilDig_Text_Stay
	release
	end

FossilDig_EventScript_Npc0::
	msgbox FossilDig_Text_Npc0, MSGBOX_NPC
	end

FossilDig_EventScript_Ghost1::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_GHOST_1, FossilDig_EventScript_Ghost1_Done
	msgbox FossilDig_Text_Ghost1_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FossilDig_EventScript_Ghost1_No
	givemon SPECIES_LARVITAR, 25
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_GHOST_1
	msgbox FossilDig_Text_Ghost1_Got
	release
	end

FossilDig_EventScript_Ghost1_Done::
	msgbox FossilDig_Text_Ghost1_After
	release
	end

FossilDig_EventScript_Ghost1_No::
	msgbox FossilDig_Text_Ghost1_Refuse
	release
	end

FossilDig_EventScript_Ghost2::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_GHOST_2, FossilDig_EventScript_Ghost2_Done
	msgbox FossilDig_Text_Ghost2_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FossilDig_EventScript_Ghost2_No
	givemon SPECIES_DRATINI, 25
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_GHOST_2
	msgbox FossilDig_Text_Ghost2_Got
	release
	end

FossilDig_EventScript_Ghost2_Done::
	msgbox FossilDig_Text_Ghost2_After
	release
	end

FossilDig_EventScript_Ghost2_No::
	msgbox FossilDig_Text_Ghost2_Refuse
	release
	end

FossilDig_EventScript_Ghost3::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_GHOST_3, FossilDig_EventScript_Ghost3_Done
	msgbox FossilDig_Text_Ghost3_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FossilDig_EventScript_Ghost3_No
	givemon SPECIES_BAGON, 25
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_GHOST_3
	msgbox FossilDig_Text_Ghost3_Got
	release
	end

FossilDig_EventScript_Ghost3_Done::
	msgbox FossilDig_Text_Ghost3_After
	release
	end

FossilDig_EventScript_Ghost3_No::
	msgbox FossilDig_Text_Ghost3_Refuse
	release
	end

FossilDig_EventScript_Ghost4::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_GHOST_4, FossilDig_EventScript_Ghost4_Done
	msgbox FossilDig_Text_Ghost4_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FossilDig_EventScript_Ghost4_No
	givemon SPECIES_BELDUM, 25
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_GHOST_4
	msgbox FossilDig_Text_Ghost4_Got
	release
	end

FossilDig_EventScript_Ghost4_Done::
	msgbox FossilDig_Text_Ghost4_After
	release
	end

FossilDig_EventScript_Ghost4_No::
	msgbox FossilDig_Text_Ghost4_Refuse
	release
	end

