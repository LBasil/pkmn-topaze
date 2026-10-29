WillowBank_MapScripts::
	.byte 0

WillowBank_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox WillowBank_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, WillowBank_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

WillowBank_EventScript_Stay::
	msgbox WillowBank_Text_Stay
	release
	end

WillowBank_EventScript_Npc0::
	msgbox WillowBank_Text_Npc0, MSGBOX_NPC
	end

WillowBank_EventScript_Npc1::
	msgbox WillowBank_Text_Npc1, MSGBOX_NPC
	end

