EvolutionLibrary_MapScripts::
	.byte 0

EvolutionLibrary_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox EvolutionLibrary_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EvolutionLibrary_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

EvolutionLibrary_EventScript_Stay::
	msgbox EvolutionLibrary_Text_Stay
	release
	end

EvolutionLibrary_EventScript_Npc0::
	msgbox EvolutionLibrary_Text_Npc0, MSGBOX_NPC
	end

EvolutionLibrary_EventScript_Npc1::
	msgbox EvolutionLibrary_Text_Npc1, MSGBOX_NPC
	end

EvolutionLibrary_EventScript_Npc2::
	msgbox EvolutionLibrary_Text_Npc2, MSGBOX_NPC
	end

EvolutionLibrary_EventScript_Npc3::
	msgbox EvolutionLibrary_Text_Npc3, MSGBOX_NPC
	end

EvolutionLibrary_EventScript_Npc4::
	msgbox EvolutionLibrary_Text_Npc4, MSGBOX_NPC
	end

