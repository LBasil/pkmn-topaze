GraniteBluff_MapScripts::
	.byte 0

GraniteBluff_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox GraniteBluff_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GraniteBluff_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

GraniteBluff_EventScript_Stay::
	msgbox GraniteBluff_Text_Stay
	release
	end

GraniteBluff_EventScript_Npc0::
	msgbox GraniteBluff_Text_Npc0, MSGBOX_NPC
	end

GraniteBluff_EventScript_Npc1::
	msgbox GraniteBluff_Text_Npc1, MSGBOX_NPC
	end

