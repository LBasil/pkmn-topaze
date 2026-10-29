MistLake_MapScripts::
	.byte 0

MistLake_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MistLake_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MistLake_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MistLake_EventScript_Stay::
	msgbox MistLake_Text_Stay
	release
	end

MistLake_EventScript_Npc0::
	msgbox MistLake_Text_Npc0, MSGBOX_NPC
	end

MistLake_EventScript_Npc1::
	msgbox MistLake_Text_Npc1, MSGBOX_NPC
	end

