CliffsideCove_MapScripts::
	.byte 0

CliffsideCove_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CliffsideCove_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CliffsideCove_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CliffsideCove_EventScript_Stay::
	msgbox CliffsideCove_Text_Stay
	release
	end

CliffsideCove_EventScript_Npc0::
	msgbox CliffsideCove_Text_Npc0, MSGBOX_NPC
	end

CliffsideCove_EventScript_Npc1::
	msgbox CliffsideCove_Text_Npc1, MSGBOX_NPC
	end

