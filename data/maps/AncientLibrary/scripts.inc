AncientLibrary_MapScripts::
	.byte 0

AncientLibrary_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox AncientLibrary_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AncientLibrary_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

AncientLibrary_EventScript_Stay::
	msgbox AncientLibrary_Text_Stay
	release
	end

AncientLibrary_EventScript_Npc0::
	msgbox AncientLibrary_Text_Npc0, MSGBOX_NPC
	end

AncientLibrary_EventScript_Npc1::
	msgbox AncientLibrary_Text_Npc1, MSGBOX_NPC
	end

