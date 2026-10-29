RustyYard_MapScripts::
	.byte 0

RustyYard_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox RustyYard_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RustyYard_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

RustyYard_EventScript_Stay::
	msgbox RustyYard_Text_Stay
	release
	end

RustyYard_EventScript_Npc0::
	msgbox RustyYard_Text_Npc0, MSGBOX_NPC
	end

RustyYard_EventScript_Npc1::
	msgbox RustyYard_Text_Npc1, MSGBOX_NPC
	end

