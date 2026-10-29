BuzzingMeadow_MapScripts::
	.byte 0

BuzzingMeadow_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BuzzingMeadow_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BuzzingMeadow_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BuzzingMeadow_EventScript_Stay::
	msgbox BuzzingMeadow_Text_Stay
	release
	end

BuzzingMeadow_EventScript_Npc0::
	msgbox BuzzingMeadow_Text_Npc0, MSGBOX_NPC
	end

BuzzingMeadow_EventScript_Npc1::
	msgbox BuzzingMeadow_Text_Npc1, MSGBOX_NPC
	end

