MirrorMarsh_MapScripts::
	.byte 0

MirrorMarsh_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MirrorMarsh_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MirrorMarsh_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MirrorMarsh_EventScript_Stay::
	msgbox MirrorMarsh_Text_Stay
	release
	end

MirrorMarsh_EventScript_Npc0::
	msgbox MirrorMarsh_Text_Npc0, MSGBOX_NPC
	end

MirrorMarsh_EventScript_Npc1::
	msgbox MirrorMarsh_Text_Npc1, MSGBOX_NPC
	end

