TwilightGlen_MapScripts::
	.byte 0

TwilightGlen_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox TwilightGlen_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, TwilightGlen_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

TwilightGlen_EventScript_Stay::
	msgbox TwilightGlen_Text_Stay
	release
	end

TwilightGlen_EventScript_Npc0::
	msgbox TwilightGlen_Text_Npc0, MSGBOX_NPC
	end

TwilightGlen_EventScript_Npc1::
	msgbox TwilightGlen_Text_Npc1, MSGBOX_NPC
	end

