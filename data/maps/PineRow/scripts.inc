PineRow_MapScripts::
	.byte 0

PineRow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox PineRow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PineRow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

PineRow_EventScript_Stay::
	msgbox PineRow_Text_Stay
	release
	end

PineRow_EventScript_Npc0::
	msgbox PineRow_Text_Npc0, MSGBOX_NPC
	end

PineRow_EventScript_Npc1::
	msgbox PineRow_Text_Npc1, MSGBOX_NPC
	end

