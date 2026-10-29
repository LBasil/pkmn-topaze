MythicSpring_MapScripts::
	.byte 0

MythicSpring_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MythicSpring_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MythicSpring_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MythicSpring_EventScript_Stay::
	msgbox MythicSpring_Text_Stay
	release
	end

MythicSpring_EventScript_Npc0::
	msgbox MythicSpring_Text_Npc0, MSGBOX_NPC
	end

MythicSpring_EventScript_Npc1::
	msgbox MythicSpring_Text_Npc1, MSGBOX_NPC
	end

