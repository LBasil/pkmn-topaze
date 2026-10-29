SpiritFalls_MapScripts::
	.byte 0

SpiritFalls_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SpiritFalls_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SpiritFalls_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SpiritFalls_EventScript_Stay::
	msgbox SpiritFalls_Text_Stay
	release
	end

SpiritFalls_EventScript_Npc0::
	msgbox SpiritFalls_Text_Npc0, MSGBOX_NPC
	end

SpiritFalls_EventScript_Npc1::
	msgbox SpiritFalls_Text_Npc1, MSGBOX_NPC
	end

