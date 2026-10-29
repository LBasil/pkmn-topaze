BabyNursery_MapScripts::
	.byte 0

BabyNursery_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BabyNursery_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BabyNursery_EventScript_Stay::
	msgbox BabyNursery_Text_Stay
	release
	end

BabyNursery_EventScript_Clerk::
	lock
	faceplayer
	msgbox BabyNursery_Text_Hello
	goto_if_set FLAG_TOPAZE_NURSERY_0, BabyNursery_EventScript_Clerk_1
	goto_if_unset FLAG_BADGE02_GET, BabyNursery_EventScript_Clerk_1
	msgbox BabyNursery_Text_O0, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_1
	givemon SPECIES_PICHU, 10
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_0
	msgbox BabyNursery_Text_G0
	goto BabyNursery_EventScript_Clerk_1
BabyNursery_EventScript_Clerk_1::
	goto_if_set FLAG_TOPAZE_NURSERY_1, BabyNursery_EventScript_Clerk_2
	goto_if_unset FLAG_BADGE02_GET, BabyNursery_EventScript_Clerk_2
	msgbox BabyNursery_Text_O1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_2
	givemon SPECIES_CLEFFA, 10
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_1
	msgbox BabyNursery_Text_G1
	goto BabyNursery_EventScript_Clerk_2
BabyNursery_EventScript_Clerk_2::
	goto_if_set FLAG_TOPAZE_NURSERY_2, BabyNursery_EventScript_Clerk_3
	goto_if_unset FLAG_BADGE03_GET, BabyNursery_EventScript_Clerk_3
	msgbox BabyNursery_Text_O2, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_3
	givemon SPECIES_IGGLYBUFF, 10
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_2
	msgbox BabyNursery_Text_G2
	goto BabyNursery_EventScript_Clerk_3
BabyNursery_EventScript_Clerk_3::
	goto_if_set FLAG_TOPAZE_NURSERY_3, BabyNursery_EventScript_Clerk_4
	goto_if_unset FLAG_BADGE03_GET, BabyNursery_EventScript_Clerk_4
	msgbox BabyNursery_Text_O3, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_4
	givemon SPECIES_AZURILL, 10
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_3
	msgbox BabyNursery_Text_G3
	goto BabyNursery_EventScript_Clerk_4
BabyNursery_EventScript_Clerk_4::
	goto_if_set FLAG_TOPAZE_NURSERY_4, BabyNursery_EventScript_Clerk_5
	goto_if_unset FLAG_BADGE04_GET, BabyNursery_EventScript_Clerk_5
	msgbox BabyNursery_Text_O4, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_5
	givemon SPECIES_SMOOCHUM, 12
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_4
	msgbox BabyNursery_Text_G4
	goto BabyNursery_EventScript_Clerk_5
BabyNursery_EventScript_Clerk_5::
	goto_if_set FLAG_TOPAZE_NURSERY_5, BabyNursery_EventScript_Clerk_6
	goto_if_unset FLAG_BADGE05_GET, BabyNursery_EventScript_Clerk_6
	msgbox BabyNursery_Text_O5, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_6
	givemon SPECIES_ELEKID, 14
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_5
	msgbox BabyNursery_Text_G5
	goto BabyNursery_EventScript_Clerk_6
BabyNursery_EventScript_Clerk_6::
	goto_if_set FLAG_TOPAZE_NURSERY_6, BabyNursery_EventScript_Clerk_7
	goto_if_unset FLAG_BADGE06_GET, BabyNursery_EventScript_Clerk_7
	msgbox BabyNursery_Text_O6, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_7
	givemon SPECIES_MAGBY, 14
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_6
	msgbox BabyNursery_Text_G6
	goto BabyNursery_EventScript_Clerk_7
BabyNursery_EventScript_Clerk_7::
	goto_if_set FLAG_TOPAZE_NURSERY_7, BabyNursery_EventScript_Clerk_8
	goto_if_unset FLAG_BADGE07_GET, BabyNursery_EventScript_Clerk_8
	msgbox BabyNursery_Text_O7, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_8
	givemon SPECIES_TYROGUE, 16
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_7
	msgbox BabyNursery_Text_G7
	goto BabyNursery_EventScript_Clerk_8
BabyNursery_EventScript_Clerk_8::
	goto_if_set FLAG_TOPAZE_NURSERY_8, BabyNursery_EventScript_Clerk_End
	goto_if_unset FLAG_BADGE08_GET, BabyNursery_EventScript_Clerk_End
	msgbox BabyNursery_Text_O8, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BabyNursery_EventScript_Clerk_End
	givemon SPECIES_WYNAUT, 18
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	setflag FLAG_TOPAZE_NURSERY_8
	msgbox BabyNursery_Text_G8
	goto BabyNursery_EventScript_Clerk_End
BabyNursery_EventScript_Clerk_End::
	msgbox BabyNursery_Text_Nothing
	release
	end
