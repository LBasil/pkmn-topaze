MuddyCreek_MapScripts::
	.byte 0

MuddyCreek_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MuddyCreek_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MuddyCreek_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MuddyCreek_EventScript_Stay::
	msgbox MuddyCreek_Text_Stay
	release
	end

MuddyCreek_EventScript_Npc0::
	msgbox MuddyCreek_Text_Npc0, MSGBOX_NPC
	end

MuddyCreek_EventScript_Npc1::
	msgbox MuddyCreek_Text_Npc1, MSGBOX_NPC
	end

