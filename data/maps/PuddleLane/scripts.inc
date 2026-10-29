PuddleLane_MapScripts::
	.byte 0

PuddleLane_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox PuddleLane_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PuddleLane_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

PuddleLane_EventScript_Stay::
	msgbox PuddleLane_Text_Stay
	release
	end

PuddleLane_EventScript_Npc0::
	msgbox PuddleLane_Text_Npc0, MSGBOX_NPC
	end

PuddleLane_EventScript_Npc1::
	msgbox PuddleLane_Text_Npc1, MSGBOX_NPC
	end

