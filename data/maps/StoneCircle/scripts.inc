StoneCircle_MapScripts::
	.byte 0

StoneCircle_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox StoneCircle_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StoneCircle_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

StoneCircle_EventScript_Stay::
	msgbox StoneCircle_Text_Stay
	release
	end

StoneCircle_EventScript_Npc0::
	msgbox StoneCircle_Text_Npc0, MSGBOX_NPC
	end

StoneCircle_EventScript_Npc1::
	msgbox StoneCircle_Text_Npc1, MSGBOX_NPC
	end

