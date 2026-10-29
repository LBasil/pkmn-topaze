BarterHouse_MapScripts::
	.byte 0

BarterHouse_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BarterHouse_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BarterHouse_EventScript_Stay::
	msgbox BarterHouse_Text_Stay
	release
	end

BarterHouse_EventScript_Clerk::
	lock
	faceplayer
	msgbox BarterHouse_Text_Hello
	goto_if_set FLAG_TOPAZE_BARTER_0, BarterHouse_EventScript_Clerk_1
	checkitem ITEM_HEART_SCALE, 3
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_1
	msgbox BarterHouse_Text_O0, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_1
	removeitem ITEM_HEART_SCALE, 3
	givemon SPECIES_FEEBAS, 20
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_0
	msgbox BarterHouse_Text_G0
	goto BarterHouse_EventScript_Clerk_1
BarterHouse_EventScript_Clerk_1::
	goto_if_set FLAG_TOPAZE_BARTER_1, BarterHouse_EventScript_Clerk_2
	checkitem ITEM_SHOAL_SHELL, 1
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_2
	msgbox BarterHouse_Text_O1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_2
	removeitem ITEM_SHOAL_SHELL, 1
	givemon SPECIES_SPHEAL, 25
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_1
	msgbox BarterHouse_Text_G1
	goto BarterHouse_EventScript_Clerk_2
BarterHouse_EventScript_Clerk_2::
	goto_if_set FLAG_TOPAZE_BARTER_2, BarterHouse_EventScript_Clerk_3
	checkitem ITEM_SHOAL_SALT, 1
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_3
	msgbox BarterHouse_Text_O2, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_3
	removeitem ITEM_SHOAL_SALT, 1
	givemon SPECIES_SNORUNT, 25
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_2
	msgbox BarterHouse_Text_G2
	goto BarterHouse_EventScript_Clerk_3
BarterHouse_EventScript_Clerk_3::
	goto_if_set FLAG_TOPAZE_BARTER_3, BarterHouse_EventScript_Clerk_4
	checkitem ITEM_TINY_MUSHROOM, 1
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_4
	msgbox BarterHouse_Text_O3, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_4
	removeitem ITEM_TINY_MUSHROOM, 1
	givemon SPECIES_SHROOMISH, 20
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_3
	msgbox BarterHouse_Text_G3
	goto BarterHouse_EventScript_Clerk_4
BarterHouse_EventScript_Clerk_4::
	goto_if_set FLAG_TOPAZE_BARTER_4, BarterHouse_EventScript_Clerk_5
	checkitem ITEM_BIG_MUSHROOM, 1
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_5
	msgbox BarterHouse_Text_O4, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_5
	removeitem ITEM_BIG_MUSHROOM, 1
	givemon SPECIES_BRELOOM, 30
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_4
	msgbox BarterHouse_Text_G4
	goto BarterHouse_EventScript_Clerk_5
BarterHouse_EventScript_Clerk_5::
	goto_if_set FLAG_TOPAZE_BARTER_5, BarterHouse_EventScript_Clerk_6
	checkitem ITEM_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_6
	msgbox BarterHouse_Text_O5, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_6
	removeitem ITEM_PEARL, 1
	givemon SPECIES_CLAMPERL, 25
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_5
	msgbox BarterHouse_Text_G5
	goto BarterHouse_EventScript_Clerk_6
BarterHouse_EventScript_Clerk_6::
	goto_if_set FLAG_TOPAZE_BARTER_6, BarterHouse_EventScript_Clerk_7
	checkitem ITEM_STARDUST, 1
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_7
	msgbox BarterHouse_Text_O6, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_7
	removeitem ITEM_STARDUST, 1
	givemon SPECIES_LUNATONE, 30
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_6
	msgbox BarterHouse_Text_G6
	goto BarterHouse_EventScript_Clerk_7
BarterHouse_EventScript_Clerk_7::
	goto_if_set FLAG_TOPAZE_BARTER_7, BarterHouse_EventScript_Clerk_End
	checkitem ITEM_STAR_PIECE, 2
	goto_if_eq VAR_RESULT, FALSE, BarterHouse_EventScript_Clerk_End
	msgbox BarterHouse_Text_O7, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BarterHouse_EventScript_Clerk_End
	removeitem ITEM_STAR_PIECE, 2
	givemon SPECIES_SOLROCK, 30
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_BARTER_7
	msgbox BarterHouse_Text_G7
	goto BarterHouse_EventScript_Clerk_End
BarterHouse_EventScript_Clerk_End::
	msgbox BarterHouse_Text_Nothing
	release
	end
