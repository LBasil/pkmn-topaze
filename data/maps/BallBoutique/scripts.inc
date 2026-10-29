BallBoutique_MapScripts::
	.byte 0

BallBoutique_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox BallBoutique_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, BallBoutique_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

BallBoutique_EventScript_Stay::
	msgbox BallBoutique_Text_Stay
	release
	end

BallBoutique_EventScript_Shop::
	lock
	faceplayer
	msgbox BallBoutique_Text_ShopHi
	pokemart BallBoutique_Stock
	msgbox BallBoutique_Text_ShopBye
	release
	end

	.align 2
BallBoutique_Stock::
	.2byte ITEM_NET_BALL
	.2byte ITEM_NEST_BALL
	.2byte ITEM_DIVE_BALL
	.2byte ITEM_REPEAT_BALL
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_LUXURY_BALL
	.2byte ITEM_PREMIER_BALL
	.2byte ITEM_NONE

BallBoutique_EventScript_Npc0::
	msgbox BallBoutique_Text_Npc0, MSGBOX_NPC
	end

