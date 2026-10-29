SunsetRoad_MapScripts::
	.byte 0

SunsetRoad_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SunsetRoad_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SunsetRoad_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SunsetRoad_EventScript_Stay::
	msgbox SunsetRoad_Text_Stay
	release
	end

SunsetRoad_EventScript_Npc0::
	msgbox SunsetRoad_Text_Npc0, MSGBOX_NPC
	end

SunsetRoad_EventScript_Npc1::
	msgbox SunsetRoad_Text_Npc1, MSGBOX_NPC
	end

