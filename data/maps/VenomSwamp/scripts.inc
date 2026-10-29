VenomSwamp_MapScripts::
	.byte 0

VenomSwamp_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox VenomSwamp_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, VenomSwamp_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

VenomSwamp_EventScript_Stay::
	msgbox VenomSwamp_Text_Stay
	release
	end

VenomSwamp_EventScript_Npc0::
	msgbox VenomSwamp_Text_Npc0, MSGBOX_NPC
	end

VenomSwamp_EventScript_Npc1::
	msgbox VenomSwamp_Text_Npc1, MSGBOX_NPC
	end

