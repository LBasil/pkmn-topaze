EmberRidge_MapScripts::
	.byte 0

EmberRidge_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox EmberRidge_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EmberRidge_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

EmberRidge_EventScript_Stay::
	msgbox EmberRidge_Text_Stay
	release
	end

EmberRidge_EventScript_Npc0::
	msgbox EmberRidge_Text_Npc0, MSGBOX_NPC
	end

EmberRidge_EventScript_Npc1::
	msgbox EmberRidge_Text_Npc1, MSGBOX_NPC
	end

