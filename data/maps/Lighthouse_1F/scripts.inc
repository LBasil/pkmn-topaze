Lighthouse_1F_MapScripts::
	.byte 0

Lighthouse_1F_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox Lighthouse_1F_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Lighthouse_1F_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

Lighthouse_1F_EventScript_Stay::
	msgbox Lighthouse_1F_Text_Stay
	release
	end

Lighthouse_1F_EventScript_Npc0::
	msgbox Lighthouse_1F_Text_Npc0, MSGBOX_NPC
	end

