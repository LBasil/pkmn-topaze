BreezeHill_MapScripts::
	.byte 0

BreezeHill_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BreezeHill_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BreezeHill_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BreezeHill_EventScript_Stay::
	msgbox BreezeHill_Text_Stay
	release
	end

BreezeHill_EventScript_Npc0::
	msgbox BreezeHill_Text_Npc0, MSGBOX_NPC
	end

BreezeHill_EventScript_Npc1::
	msgbox BreezeHill_Text_Npc1, MSGBOX_NPC
	end

