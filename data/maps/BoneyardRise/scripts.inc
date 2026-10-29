BoneyardRise_MapScripts::
	.byte 0

BoneyardRise_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BoneyardRise_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BoneyardRise_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BoneyardRise_EventScript_Stay::
	msgbox BoneyardRise_Text_Stay
	release
	end

BoneyardRise_EventScript_Npc0::
	msgbox BoneyardRise_Text_Npc0, MSGBOX_NPC
	end

BoneyardRise_EventScript_Npc1::
	msgbox BoneyardRise_Text_Npc1, MSGBOX_NPC
	end

