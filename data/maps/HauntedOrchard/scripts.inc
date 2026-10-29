HauntedOrchard_MapScripts::
	.byte 0

HauntedOrchard_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox HauntedOrchard_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HauntedOrchard_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

HauntedOrchard_EventScript_Stay::
	msgbox HauntedOrchard_Text_Stay
	release
	end

HauntedOrchard_EventScript_Npc0::
	msgbox HauntedOrchard_Text_Npc0, MSGBOX_NPC
	end

HauntedOrchard_EventScript_Npc1::
	msgbox HauntedOrchard_Text_Npc1, MSGBOX_NPC
	end

