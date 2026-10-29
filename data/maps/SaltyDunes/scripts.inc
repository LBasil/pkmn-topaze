SaltyDunes_MapScripts::
	.byte 0

SaltyDunes_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SaltyDunes_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SaltyDunes_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SaltyDunes_EventScript_Stay::
	msgbox SaltyDunes_Text_Stay
	release
	end

SaltyDunes_EventScript_Npc0::
	msgbox SaltyDunes_Text_Npc0, MSGBOX_NPC
	end

SaltyDunes_EventScript_Npc1::
	msgbox SaltyDunes_Text_Npc1, MSGBOX_NPC
	end

