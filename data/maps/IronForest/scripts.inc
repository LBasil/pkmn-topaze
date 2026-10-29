IronForest_MapScripts::
	.byte 0

IronForest_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox IronForest_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, IronForest_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

IronForest_EventScript_Stay::
	msgbox IronForest_Text_Stay
	release
	end

IronForest_EventScript_Npc0::
	msgbox IronForest_Text_Npc0, MSGBOX_NPC
	end

IronForest_EventScript_Npc1::
	msgbox IronForest_Text_Npc1, MSGBOX_NPC
	end

