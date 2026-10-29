SkyGarden_MapScripts::
	.byte 0

SkyGarden_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SkyGarden_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SkyGarden_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SkyGarden_EventScript_Stay::
	msgbox SkyGarden_Text_Stay
	release
	end

SkyGarden_EventScript_Npc0::
	msgbox SkyGarden_Text_Npc0, MSGBOX_NPC
	end

SkyGarden_EventScript_Npc1::
	msgbox SkyGarden_Text_Npc1, MSGBOX_NPC
	end

