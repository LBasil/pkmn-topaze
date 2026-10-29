SpireYard_MapScripts::
	.byte 0

SpireYard_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox SpireYard_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SpireYard_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

SpireYard_EventScript_Stay::
	msgbox SpireYard_Text_Stay
	release
	end

SpireYard_EventScript_Npc0::
	msgbox SpireYard_Text_Npc0, MSGBOX_NPC
	end

SpireYard_EventScript_Npc1::
	msgbox SpireYard_Text_Npc1, MSGBOX_NPC
	end

