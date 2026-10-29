WeedPatch_MapScripts::
	.byte 0

WeedPatch_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox WeedPatch_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, WeedPatch_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

WeedPatch_EventScript_Stay::
	msgbox WeedPatch_Text_Stay
	release
	end

WeedPatch_EventScript_Npc0::
	msgbox WeedPatch_Text_Npc0, MSGBOX_NPC
	end

WeedPatch_EventScript_Npc1::
	msgbox WeedPatch_Text_Npc1, MSGBOX_NPC
	end

