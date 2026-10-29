GlimmerBay_MapScripts::
	.byte 0

GlimmerBay_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox GlimmerBay_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GlimmerBay_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

GlimmerBay_EventScript_Stay::
	msgbox GlimmerBay_Text_Stay
	release
	end

GlimmerBay_EventScript_Npc0::
	msgbox GlimmerBay_Text_Npc0, MSGBOX_NPC
	end

GlimmerBay_EventScript_Npc1::
	msgbox GlimmerBay_Text_Npc1, MSGBOX_NPC
	end

