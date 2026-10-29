DaisyHill_MapScripts::
	.byte 0

DaisyHill_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DaisyHill_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DaisyHill_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DaisyHill_EventScript_Stay::
	msgbox DaisyHill_Text_Stay
	release
	end

DaisyHill_EventScript_Npc0::
	msgbox DaisyHill_Text_Npc0, MSGBOX_NPC
	end

DaisyHill_EventScript_Npc1::
	msgbox DaisyHill_Text_Npc1, MSGBOX_NPC
	end

