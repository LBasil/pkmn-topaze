DozyDell_MapScripts::
	.byte 0

DozyDell_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DozyDell_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DozyDell_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DozyDell_EventScript_Stay::
	msgbox DozyDell_Text_Stay
	release
	end

DozyDell_EventScript_Npc0::
	msgbox DozyDell_Text_Npc0, MSGBOX_NPC
	end

DozyDell_EventScript_Npc1::
	msgbox DozyDell_Text_Npc1, MSGBOX_NPC
	end

