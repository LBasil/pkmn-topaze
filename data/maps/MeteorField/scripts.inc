MeteorField_MapScripts::
	.byte 0

MeteorField_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MeteorField_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MeteorField_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MeteorField_EventScript_Stay::
	msgbox MeteorField_Text_Stay
	release
	end

MeteorField_EventScript_Npc0::
	msgbox MeteorField_Text_Npc0, MSGBOX_NPC
	end

MeteorField_EventScript_Npc1::
	msgbox MeteorField_Text_Npc1, MSGBOX_NPC
	end

