BerryBrook_MapScripts::
	.byte 0

BerryBrook_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BerryBrook_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BerryBrook_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BerryBrook_EventScript_Stay::
	msgbox BerryBrook_Text_Stay
	release
	end

BerryBrook_EventScript_Npc0::
	msgbox BerryBrook_Text_Npc0, MSGBOX_NPC
	end

BerryBrook_EventScript_Npc1::
	msgbox BerryBrook_Text_Npc1, MSGBOX_NPC
	end

