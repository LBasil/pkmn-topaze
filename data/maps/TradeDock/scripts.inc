TradeDock_MapScripts::
	.byte 0

TradeDock_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox TradeDock_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, TradeDock_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

TradeDock_EventScript_Stay::
	msgbox TradeDock_Text_Stay
	release
	end

TradeDock_EventScript_Npc0::
	msgbox TradeDock_Text_Npc0, MSGBOX_NPC
	end

TradeDock_EventScript_Npc1::
	msgbox TradeDock_Text_Npc1, MSGBOX_NPC
	end

TradeDock_EventScript_Sage::
	lock
	faceplayer
	msgbox TradeDock_Text_Sage0
	random 3
	goto_if_eq VAR_RESULT, 0, TradeDock_EventScript_S1
	goto_if_eq VAR_RESULT, 1, TradeDock_EventScript_S2
	msgbox TradeDock_Text_Sage3
	release
	end

TradeDock_EventScript_S1::
	msgbox TradeDock_Text_Sage1
	release
	end

TradeDock_EventScript_S2::
	msgbox TradeDock_Text_Sage2
	release
	end

