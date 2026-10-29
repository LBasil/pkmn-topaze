SkyPerch_MapScripts::
	.byte 0

SkyPerch_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SkyPerch_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SkyPerch_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SkyPerch_EventScript_Stay::
	msgbox SkyPerch_Text_Stay
	release
	end

SkyPerch_EventScript_Npc0::
	msgbox SkyPerch_Text_Npc0, MSGBOX_NPC
	end

SkyPerch_EventScript_Npc1::
	msgbox SkyPerch_Text_Npc1, MSGBOX_NPC
	end

