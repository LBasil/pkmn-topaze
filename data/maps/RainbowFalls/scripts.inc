RainbowFalls_MapScripts::
	.byte 0

RainbowFalls_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox RainbowFalls_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, RainbowFalls_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

RainbowFalls_EventScript_Stay::
	msgbox RainbowFalls_Text_Stay
	release
	end

RainbowFalls_EventScript_Npc0::
	msgbox RainbowFalls_Text_Npc0, MSGBOX_NPC
	end

RainbowFalls_EventScript_Npc1::
	msgbox RainbowFalls_Text_Npc1, MSGBOX_NPC
	end

