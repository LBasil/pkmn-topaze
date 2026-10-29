CrickPond_MapScripts::
	.byte 0

CrickPond_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CrickPond_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CrickPond_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CrickPond_EventScript_Stay::
	msgbox CrickPond_Text_Stay
	release
	end

CrickPond_EventScript_Npc0::
	msgbox CrickPond_Text_Npc0, MSGBOX_NPC
	end

CrickPond_EventScript_Npc1::
	msgbox CrickPond_Text_Npc1, MSGBOX_NPC
	end

