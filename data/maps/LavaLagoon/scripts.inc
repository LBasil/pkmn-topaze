LavaLagoon_MapScripts::
	.byte 0

LavaLagoon_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox LavaLagoon_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LavaLagoon_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

LavaLagoon_EventScript_Stay::
	msgbox LavaLagoon_Text_Stay
	release
	end

LavaLagoon_EventScript_Npc0::
	msgbox LavaLagoon_Text_Npc0, MSGBOX_NPC
	end

LavaLagoon_EventScript_Npc1::
	msgbox LavaLagoon_Text_Npc1, MSGBOX_NPC
	end

