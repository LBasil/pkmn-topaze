SaltFlats_MapScripts::
	.byte 0

SaltFlats_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SaltFlats_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SaltFlats_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SaltFlats_EventScript_Stay::
	msgbox SaltFlats_Text_Stay
	release
	end

SaltFlats_EventScript_Npc0::
	msgbox SaltFlats_Text_Npc0, MSGBOX_NPC
	end

SaltFlats_EventScript_Npc1::
	msgbox SaltFlats_Text_Npc1, MSGBOX_NPC
	end

