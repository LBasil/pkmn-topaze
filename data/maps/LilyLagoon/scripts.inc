LilyLagoon_MapScripts::
	.byte 0

LilyLagoon_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox LilyLagoon_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LilyLagoon_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

LilyLagoon_EventScript_Stay::
	msgbox LilyLagoon_Text_Stay
	release
	end

LilyLagoon_EventScript_Npc0::
	msgbox LilyLagoon_Text_Npc0, MSGBOX_NPC
	end

LilyLagoon_EventScript_Npc1::
	msgbox LilyLagoon_Text_Npc1, MSGBOX_NPC
	end

