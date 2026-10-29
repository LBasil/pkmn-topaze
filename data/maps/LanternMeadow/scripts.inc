LanternMeadow_MapScripts::
	.byte 0

LanternMeadow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox LanternMeadow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LanternMeadow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

LanternMeadow_EventScript_Stay::
	msgbox LanternMeadow_Text_Stay
	release
	end

LanternMeadow_EventScript_Npc0::
	msgbox LanternMeadow_Text_Npc0, MSGBOX_NPC
	end

LanternMeadow_EventScript_Npc1::
	msgbox LanternMeadow_Text_Npc1, MSGBOX_NPC
	end

