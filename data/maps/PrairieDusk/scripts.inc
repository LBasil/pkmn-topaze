PrairieDusk_MapScripts::
	.byte 0

PrairieDusk_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox PrairieDusk_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PrairieDusk_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

PrairieDusk_EventScript_Stay::
	msgbox PrairieDusk_Text_Stay
	release
	end

PrairieDusk_EventScript_Npc0::
	msgbox PrairieDusk_Text_Npc0, MSGBOX_NPC
	end

PrairieDusk_EventScript_Npc1::
	msgbox PrairieDusk_Text_Npc1, MSGBOX_NPC
	end

