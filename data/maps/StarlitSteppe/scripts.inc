StarlitSteppe_MapScripts::
	.byte 0

StarlitSteppe_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox StarlitSteppe_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, StarlitSteppe_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

StarlitSteppe_EventScript_Stay::
	msgbox StarlitSteppe_Text_Stay
	release
	end

StarlitSteppe_EventScript_Npc0::
	msgbox StarlitSteppe_Text_Npc0, MSGBOX_NPC
	end

StarlitSteppe_EventScript_Npc1::
	msgbox StarlitSteppe_Text_Npc1, MSGBOX_NPC
	end

