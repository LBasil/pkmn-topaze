CopperCanyon_MapScripts::
	.byte 0

CopperCanyon_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox CopperCanyon_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CopperCanyon_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

CopperCanyon_EventScript_Stay::
	msgbox CopperCanyon_Text_Stay
	release
	end

CopperCanyon_EventScript_Npc0::
	msgbox CopperCanyon_Text_Npc0, MSGBOX_NPC
	end

CopperCanyon_EventScript_Npc1::
	msgbox CopperCanyon_Text_Npc1, MSGBOX_NPC
	end

