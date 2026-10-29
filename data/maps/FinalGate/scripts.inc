FinalGate_MapScripts::
	.byte 0

FinalGate_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox FinalGate_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FinalGate_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

FinalGate_EventScript_Stay::
	msgbox FinalGate_Text_Stay
	release
	end

FinalGate_EventScript_Npc0::
	msgbox FinalGate_Text_Npc0, MSGBOX_NPC
	end

FinalGate_EventScript_Npc1::
	msgbox FinalGate_Text_Npc1, MSGBOX_NPC
	end

