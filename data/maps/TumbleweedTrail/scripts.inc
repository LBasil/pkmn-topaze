TumbleweedTrail_MapScripts::
	.byte 0

TumbleweedTrail_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox TumbleweedTrail_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, TumbleweedTrail_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

TumbleweedTrail_EventScript_Stay::
	msgbox TumbleweedTrail_Text_Stay
	release
	end

TumbleweedTrail_EventScript_Npc0::
	msgbox TumbleweedTrail_Text_Npc0, MSGBOX_NPC
	end

TumbleweedTrail_EventScript_Npc1::
	msgbox TumbleweedTrail_Text_Npc1, MSGBOX_NPC
	end

