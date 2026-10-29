DawnSummit_MapScripts::
	.byte 0

DawnSummit_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DawnSummit_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DawnSummit_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DawnSummit_EventScript_Stay::
	msgbox DawnSummit_Text_Stay
	release
	end

DawnSummit_EventScript_Npc0::
	msgbox DawnSummit_Text_Npc0, MSGBOX_NPC
	end

DawnSummit_EventScript_Npc1::
	msgbox DawnSummit_Text_Npc1, MSGBOX_NPC
	end

