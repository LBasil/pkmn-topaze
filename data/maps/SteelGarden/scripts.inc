SteelGarden_MapScripts::
	.byte 0

SteelGarden_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SteelGarden_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SteelGarden_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SteelGarden_EventScript_Stay::
	msgbox SteelGarden_Text_Stay
	release
	end

SteelGarden_EventScript_Npc0::
	msgbox SteelGarden_Text_Npc0, MSGBOX_NPC
	end

SteelGarden_EventScript_Npc1::
	msgbox SteelGarden_Text_Npc1, MSGBOX_NPC
	end

