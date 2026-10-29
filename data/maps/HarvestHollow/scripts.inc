HarvestHollow_MapScripts::
	.byte 0

HarvestHollow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox HarvestHollow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HarvestHollow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

HarvestHollow_EventScript_Stay::
	msgbox HarvestHollow_Text_Stay
	release
	end

HarvestHollow_EventScript_Npc0::
	msgbox HarvestHollow_Text_Npc0, MSGBOX_NPC
	end

HarvestHollow_EventScript_Npc1::
	msgbox HarvestHollow_Text_Npc1, MSGBOX_NPC
	end

