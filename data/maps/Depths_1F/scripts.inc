Depths_1F_MapScripts::
	.byte 0

Depths_1F_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox Depths_1F_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Depths_1F_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

Depths_1F_EventScript_Stay::
	msgbox Depths_1F_Text_Stay
	release
	end

Depths_1F_EventScript_Npc0::
	msgbox Depths_1F_Text_Npc0, MSGBOX_NPC
	end


Depths_1F_EventScript_Down::
	lockall
	msgbox Depths_1F_Text_Down
	warp MAP_DEPTHS_2F, 255, 18, 21
	waitstate
	end
