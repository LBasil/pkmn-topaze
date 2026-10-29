GlassCavern_MapScripts::
	.byte 0

GlassCavern_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox GlassCavern_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GlassCavern_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

GlassCavern_EventScript_Stay::
	msgbox GlassCavern_Text_Stay
	release
	end

GlassCavern_EventScript_Npc0::
	msgbox GlassCavern_Text_Npc0, MSGBOX_NPC
	end

GlassCavern_EventScript_Npc1::
	msgbox GlassCavern_Text_Npc1, MSGBOX_NPC
	end

