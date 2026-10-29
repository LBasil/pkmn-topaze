DeepEmberCave_MapScripts::
	.byte 0

DeepEmberCave_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DeepEmberCave_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DeepEmberCave_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DeepEmberCave_EventScript_Stay::
	msgbox DeepEmberCave_Text_Stay
	release
	end

DeepEmberCave_EventScript_Npc0::
	msgbox DeepEmberCave_Text_Npc0, MSGBOX_NPC
	end

DeepEmberCave_EventScript_Npc1::
	msgbox DeepEmberCave_Text_Npc1, MSGBOX_NPC
	end

