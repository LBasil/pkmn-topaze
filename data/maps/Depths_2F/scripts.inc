Depths_2F_MapScripts::
	.byte 0

Depths_2F_EventScript_Fall::
	lockall
	msgbox Depths_2F_Text_Fall
	random 2
	goto_if_eq VAR_RESULT, 0, Depths_2F_EventScript_FallDown
	warp MAP_DEPTHS_1F, 255, 18, 21
	waitstate
	end

Depths_2F_EventScript_FallDown::
	warp MAP_DEPTHS_3F, 255, 18, 21
	waitstate
	end
