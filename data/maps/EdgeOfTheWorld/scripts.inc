EdgeOfTheWorld_MapScripts::
	.byte 0

EdgeOfTheWorld_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox EdgeOfTheWorld_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EdgeOfTheWorld_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

EdgeOfTheWorld_EventScript_Stay::
	msgbox EdgeOfTheWorld_Text_Stay
	release
	end

EdgeOfTheWorld_EventScript_Npc0::
	msgbox EdgeOfTheWorld_Text_Npc0, MSGBOX_NPC
	end

EdgeOfTheWorld_EventScript_Npc1::
	msgbox EdgeOfTheWorld_Text_Npc1, MSGBOX_NPC
	end

