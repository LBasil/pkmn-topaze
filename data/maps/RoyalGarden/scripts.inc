RoyalGarden_MapScripts::
	.byte 0

RoyalGarden_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox RoyalGarden_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RoyalGarden_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

RoyalGarden_EventScript_Stay::
	msgbox RoyalGarden_Text_Stay
	release
	end

RoyalGarden_EventScript_Npc0::
	msgbox RoyalGarden_Text_Npc0, MSGBOX_NPC
	end

RoyalGarden_EventScript_Npc1::
	msgbox RoyalGarden_Text_Npc1, MSGBOX_NPC
	end

