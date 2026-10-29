ChampionsPath_MapScripts::
	.byte 0

ChampionsPath_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ChampionsPath_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ChampionsPath_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ChampionsPath_EventScript_Stay::
	msgbox ChampionsPath_Text_Stay
	release
	end

ChampionsPath_EventScript_Npc0::
	msgbox ChampionsPath_Text_Npc0, MSGBOX_NPC
	end

ChampionsPath_EventScript_Npc1::
	msgbox ChampionsPath_Text_Npc1, MSGBOX_NPC
	end

