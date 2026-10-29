NorthWind_MapScripts::
	.byte 0

NorthWind_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox NorthWind_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NorthWind_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

NorthWind_EventScript_Stay::
	msgbox NorthWind_Text_Stay
	release
	end

NorthWind_EventScript_Npc0::
	msgbox NorthWind_Text_Npc0, MSGBOX_NPC
	end

NorthWind_EventScript_Npc1::
	msgbox NorthWind_Text_Npc1, MSGBOX_NPC
	end

