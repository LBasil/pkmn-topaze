WindmillFlats_MapScripts::
	.byte 0

WindmillFlats_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox WindmillFlats_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, WindmillFlats_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

WindmillFlats_EventScript_Stay::
	msgbox WindmillFlats_Text_Stay
	release
	end

WindmillFlats_EventScript_Npc0::
	msgbox WindmillFlats_Text_Npc0, MSGBOX_NPC
	end

WindmillFlats_EventScript_Npc1::
	msgbox WindmillFlats_Text_Npc1, MSGBOX_NPC
	end

