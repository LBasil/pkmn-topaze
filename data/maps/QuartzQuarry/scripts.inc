QuartzQuarry_MapScripts::
	.byte 0

QuartzQuarry_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox QuartzQuarry_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, QuartzQuarry_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

QuartzQuarry_EventScript_Stay::
	msgbox QuartzQuarry_Text_Stay
	release
	end

QuartzQuarry_EventScript_Npc0::
	msgbox QuartzQuarry_Text_Npc0, MSGBOX_NPC
	end

QuartzQuarry_EventScript_Npc1::
	msgbox QuartzQuarry_Text_Npc1, MSGBOX_NPC
	end

